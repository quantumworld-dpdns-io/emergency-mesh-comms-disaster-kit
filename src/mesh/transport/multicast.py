from __future__ import annotations

import asyncio

from .base import Transport


class MulticastOverlayTransport(Transport):
    name = "multicast"

    def __init__(self, cluster_id: str = "default") -> None:
        self.cluster_id = cluster_id
        self._inbound: asyncio.Queue[tuple[str, bytes]] = asyncio.Queue()

    async def send(self, destination: str, payload: bytes) -> None:
        await self._inbound.put((destination, payload))

    async def receive(self) -> tuple[str, bytes]:
        return await self._inbound.get()

    async def discover(self) -> list[str]:
        return [self.cluster_id]
