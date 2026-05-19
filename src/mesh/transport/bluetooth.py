from __future__ import annotations

import asyncio

from .base import Transport


class BluetoothTransport(Transport):
    name = "bluetooth"

    def __init__(self) -> None:
        self._inbound: asyncio.Queue[tuple[str, bytes]] = asyncio.Queue()

    async def send(self, destination: str, payload: bytes) -> None:
        await self._inbound.put((destination, payload))

    async def receive(self) -> tuple[str, bytes]:
        return await self._inbound.get()

    async def discover(self) -> list[str]:
        return []
