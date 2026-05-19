from __future__ import annotations

import asyncio
import random

from .base import Transport


class SimulatedTransport(Transport):
    name = "simulated"

    def __init__(self, loss_rate: float = 0.0, delay_ms: int = 0, bandwidth_bps: int = 1_000_000) -> None:
        self.loss_rate = max(0.0, min(loss_rate, 1.0))
        self.delay_ms = max(delay_ms, 0)
        self.bandwidth_bps = max(bandwidth_bps, 1)
        self._inbound: asyncio.Queue[tuple[str, bytes]] = asyncio.Queue()

    async def send(self, destination: str, payload: bytes) -> None:
        if random.random() < self.loss_rate:
            return
        tx_delay = len(payload) * 8 / self.bandwidth_bps
        await asyncio.sleep((self.delay_ms / 1000) + tx_delay)
        await self._inbound.put((destination, payload))

    async def receive(self) -> tuple[str, bytes]:
        return await self._inbound.get()

    async def discover(self) -> list[str]:
        return []
