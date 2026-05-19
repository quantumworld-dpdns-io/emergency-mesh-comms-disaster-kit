from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime

from .base import Transport


@dataclass(slots=True)
class TransportHealth:
    transport: str
    healthy: bool
    checked_at: datetime


class TransportHealthMonitor:
    def __init__(self, poll_seconds: float = 10.0) -> None:
        self.poll_seconds = poll_seconds

    async def ping(self, transport: Transport) -> TransportHealth:
        try:
            await transport.discover()
            healthy = True
        except Exception:
            healthy = False
        return TransportHealth(transport=transport.name, healthy=healthy, checked_at=datetime.now(UTC))

    async def watch_once(self, transports: list[Transport]) -> list[TransportHealth]:
        return await asyncio.gather(*(self.ping(t) for t in transports))
