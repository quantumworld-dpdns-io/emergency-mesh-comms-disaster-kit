from __future__ import annotations

import asyncio
import os

from src.lora.drivers.detector import detect_lora_driver
from src.lora.lora_transport import LoRaTransport

from .base import Transport
from .event_bus import MeshEventBus
from .health import TransportHealthMonitor
from .registry import TransportRegistry
from .stats import StatsCollector


class TransportManager:
    def __init__(self) -> None:
        self.registry = TransportRegistry()
        self.stats = StatsCollector()
        self.bus = MeshEventBus()
        self.health = TransportHealthMonitor(poll_seconds=10.0)
        self._receive_tasks: list[asyncio.Task[None]] = []
        self._running = False

    def register(self, transport: Transport) -> None:
        self.registry.register(transport)

    def auto_register_lora(self) -> bool:
        enabled = os.getenv("LORA_ENABLED", "false").lower() == "true"
        if not enabled:
            return False
        node_id = int(os.getenv("LORA_NODE_ID", "1"))
        self.register(LoRaTransport(node_id=node_id, driver=detect_lora_driver()))
        return True

    async def send(self, transport_name: str, destination: str, payload: bytes) -> None:
        transport = self.registry.get(transport_name)
        if transport is None:
            raise KeyError(f"unknown transport: {transport_name}")
        await transport.send(destination, payload)
        self.stats.record_tx(transport_name, len(payload))
        await self.bus.publish("tx", transport_name, {"destination": destination, "bytes": len(payload)})

    async def _receive_loop(self, transport: Transport) -> None:
        while self._running:
            try:
                src, payload = await transport.receive()
                self.stats.record_rx(transport.name, len(payload))
                await self.bus.publish("rx", transport.name, {"source": src, "bytes": len(payload)})
            except Exception as exc:
                self.stats.record_error(transport.name)
                await self.bus.publish("error", transport.name, {"error": str(exc)})

    def start(self) -> None:
        self._running = True
        for transport in self.registry.transports.values():
            self._receive_tasks.append(asyncio.create_task(self._receive_loop(transport)))

    async def stop(self) -> None:
        self._running = False
        for task in self._receive_tasks:
            task.cancel()
        if self._receive_tasks:
            await asyncio.gather(*self._receive_tasks, return_exceptions=True)
        self._receive_tasks.clear()

    async def health_snapshot(self) -> list[dict[str, object]]:
        statuses = await self.health.watch_once(list(self.registry.transports.values()))
        return [
            {"transport": s.transport, "healthy": s.healthy, "checked_at": s.checked_at.isoformat()}
            for s in statuses
        ]
