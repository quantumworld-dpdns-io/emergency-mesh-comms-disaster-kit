from __future__ import annotations

import asyncio
import time

from src.mesh.transport.base import Transport

from .drivers.adr import AdaptiveDataRateController
from .drivers.base import LoRaDriver
from .drivers.csma_ca import CsmaCaController
from .drivers.duty_cycle import DutyCycleLimiter
from .drivers.fhss import FhssController
from .drivers.simulator import SimulatedLoRaDriver
from .packets.decoder import decode_packet
from .packets.encoder import encode_packet
from .packets.types import LoRaPacket, PacketFlags, PacketType


class LoRaTransport(Transport):
    name = "lora"

    def __init__(
        self,
        node_id: int,
        driver: LoRaDriver | None = None,
        channels_mhz: list[float] | None = None,
    ) -> None:
        self.node_id = node_id
        self.driver = driver or SimulatedLoRaDriver()
        self.csma = CsmaCaController()
        self.fhss = FhssController(channels_mhz or [902.3 + (i * 0.2) for i in range(50)])
        self.duty = DutyCycleLimiter()
        self.adr = AdaptiveDataRateController()
        self._seq = 0
        self._inbound: asyncio.Queue[tuple[str, bytes]] = asyncio.Queue()
        self._snr_history: list[float] = []

    def _next_seq(self) -> int:
        self._seq = (self._seq + 1) % 65536
        return self._seq

    async def send(self, destination: str, payload: bytes) -> None:
        if not self.csma.wait_for_clear_channel(self.driver):
            return
        if not self.duty.allow_tx(time.time(), airtime_seconds=max(0.05, len(payload) / 6000)):
            return

        snr = self.driver.read_snr()
        self._snr_history.append(snr)
        self._snr_history = self._snr_history[-20:]
        decision = self.adr.decide(self._snr_history)
        self.driver.configure(self.fhss.channel_for_slot(self._seq), decision.spreading_factor, decision.tx_power_dbm)

        pkt = LoRaPacket(
            version=1,
            packet_type=PacketType.DATA,
            flags=PacketFlags.NONE,
            sequence=self._next_seq(),
            source=self.node_id,
            destination=int(destination),
            payload=payload,
        )
        self.driver.send(encode_packet(pkt))

    async def receive(self) -> tuple[str, bytes]:
        raw = self.driver.receive()
        if raw is not None:
            pkt = decode_packet(raw)
            return str(pkt.source), pkt.payload
        return await self._inbound.get()

    async def discover(self) -> list[str]:
        return []
