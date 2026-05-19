from __future__ import annotations

import heapq
from dataclasses import dataclass, field

from src.mesh.protocol.bundle import Bundle, Priority


PRIORITY_WEIGHT = {Priority.emergency: 3, Priority.medical: 2, Priority.general: 1}


@dataclass(order=True)
class _Item:
    sort_key: int
    seq: int
    bundle: Bundle = field(compare=False)


class BundleScheduler:
    def __init__(self) -> None:
        self._heap: list[_Item] = []
        self._seq = 0

    def push(self, bundle: Bundle) -> None:
        weight = PRIORITY_WEIGHT[bundle.primary.priority]
        self._seq += 1
        heapq.heappush(self._heap, _Item(sort_key=-weight, seq=self._seq, bundle=bundle))

    def pop(self) -> Bundle | None:
        if not self._heap:
            return None
        return heapq.heappop(self._heap).bundle
