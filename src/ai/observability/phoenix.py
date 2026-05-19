from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(slots=True)
class TraceEvent:
    name: str
    started_at: datetime
    ended_at: datetime
    attributes: dict[str, object]


class PhoenixTracer:
    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    @contextmanager
    def span(self, name: str, **attributes: object):
        start = datetime.now(UTC)
        try:
            yield
        finally:
            end = datetime.now(UTC)
            self.events.append(TraceEvent(name=name, started_at=start, ended_at=end, attributes=attributes))

    def record(self, name: str, **attributes: object) -> None:
        now = datetime.now(UTC)
        self.events.append(TraceEvent(name=name, started_at=now, ended_at=now, attributes=attributes))
