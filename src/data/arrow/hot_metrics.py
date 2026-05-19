from __future__ import annotations

from collections import deque

import pyarrow as pa


class HotMetricsTable:
    def __init__(self, max_events: int = 10_000) -> None:
        self.max_events = max_events
        self._events: deque[dict[str, object]] = deque(maxlen=max_events)

    def append(self, event: dict[str, object]) -> None:
        self._events.append(event)

    def to_arrow(self) -> pa.Table:
        if not self._events:
            return pa.table({})
        keys = sorted({k for e in self._events for k in e.keys()})
        cols = {k: [e.get(k) for e in self._events] for k in keys}
        return pa.table(cols)
