from __future__ import annotations

import asyncio
import base64

from .base import Transport


class SmsTransport(Transport):
    name = "sms"

    def __init__(self, max_chars: int = 140) -> None:
        self.max_chars = max_chars
        self._inbound: asyncio.Queue[tuple[str, bytes]] = asyncio.Queue()

    def _encode(self, payload: bytes) -> bytes:
        encoded = base64.b64encode(payload)
        if len(encoded) > self.max_chars:
            return encoded[: self.max_chars]
        return encoded

    async def send(self, destination: str, payload: bytes) -> None:
        await self._inbound.put((destination, self._encode(payload)))

    async def receive(self) -> tuple[str, bytes]:
        src, payload = await self._inbound.get()
        return src, base64.b64decode(payload)

    async def discover(self) -> list[str]:
        return []
