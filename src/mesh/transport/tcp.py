from __future__ import annotations

import asyncio

from .base import Transport


class TcpTransport(Transport):
    name = "tcp"

    def __init__(self, tls_enabled: bool = False) -> None:
        self.tls_enabled = tls_enabled
        self._inbound: asyncio.Queue[tuple[str, bytes]] = asyncio.Queue()

    async def send(self, destination: str, payload: bytes) -> None:
        await self._inbound.put((destination, payload))

    async def receive(self) -> tuple[str, bytes]:
        return await self._inbound.get()

    async def discover(self) -> list[str]:
        return []
