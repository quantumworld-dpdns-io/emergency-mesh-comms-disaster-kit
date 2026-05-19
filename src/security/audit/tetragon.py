from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(slots=True)
class TetragonEvent:
    event_type: str
    process: str
    source_ip: str | None
    dest_ip: str | None
    metadata: dict[str, object]
    ts: datetime


class TetragonEventReader:
    """gRPC stream reader facade (mock-friendly baseline)."""

    async def stream_events(self) -> AsyncIterator[TetragonEvent]:
        # Placeholder stream for integration; real gRPC hookup comes with runtime deployment.
        yield TetragonEvent(
            event_type="ProcessEvent",
            process="mesh-router",
            source_ip=None,
            dest_ip=None,
            metadata={"action": "exec"},
            ts=datetime.now(UTC),
        )
