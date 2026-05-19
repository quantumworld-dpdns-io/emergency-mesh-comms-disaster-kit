from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(slots=True)
class MeshEvent:
    event_type: str
    transport: str
    payload: dict[str, object]
    timestamp: datetime


class MeshEventBus:
    def __init__(self) -> None:
        self._subscribers: list[asyncio.Queue[MeshEvent]] = []

    def subscribe(self) -> asyncio.Queue[MeshEvent]:
        q: asyncio.Queue[MeshEvent] = asyncio.Queue()
        self._subscribers.append(q)
        return q

    async def publish(self, event_type: str, transport: str, payload: dict[str, object]) -> None:
        event = MeshEvent(event_type, transport, payload, datetime.now(UTC))
        for q in self._subscribers:
            await q.put(event)
