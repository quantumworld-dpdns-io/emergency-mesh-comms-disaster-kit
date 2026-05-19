from __future__ import annotations

from collections import deque


class TransportPriorityQueue:
    def __init__(self) -> None:
        self._q: dict[int, deque[tuple[str, bytes]]] = {0: deque(), 1: deque(), 2: deque()}

    def put(self, destination: str, payload: bytes, tier: int) -> None:
        if tier not in self._q:
            raise ValueError("tier must be one of 0,1,2")
        self._q[tier].append((destination, payload))

    def get(self) -> tuple[str, bytes] | None:
        for tier in (2, 1, 0):
            if self._q[tier]:
                return self._q[tier].popleft()
        return None
