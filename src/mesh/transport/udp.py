from __future__ import annotations

import asyncio

from .base import Transport


class UdpTransport(Transport):
    name = "udp"

    def __init__(self, mtu: int = 1200) -> None:
        self.mtu = mtu
        self._inbound: asyncio.Queue[tuple[str, bytes]] = asyncio.Queue()

    def fragment(self, payload: bytes) -> list[bytes]:
        return [payload[i : i + self.mtu] for i in range(0, len(payload), self.mtu)] or [b""]

    async def send(self, destination: str, payload: bytes) -> None:
        for fragment in self.fragment(payload):
            await self._inbound.put((destination, fragment))

    async def receive(self) -> tuple[str, bytes]:
        return await self._inbound.get()

    async def discover(self) -> list[str]:
        return []
