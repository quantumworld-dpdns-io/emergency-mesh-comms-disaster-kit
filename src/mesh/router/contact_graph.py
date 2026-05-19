from __future__ import annotations

import heapq
from dataclasses import dataclass


@dataclass(slots=True)
class ContactEdge:
    to_node: str
    rssi: float
    duration_seconds: float

    @property
    def cost(self) -> float:
        # Lower cost is better. Stronger RSSI and longer contact reduce cost.
        rssi_score = max(1.0, 100.0 - abs(self.rssi))
        duration_score = max(1.0, 100.0 / max(self.duration_seconds, 1.0))
        return rssi_score + duration_score


class ContactGraph:
    def __init__(self) -> None:
        self.adj: dict[str, list[ContactEdge]] = {}

    def add_edge(self, src: str, dst: str, rssi: float, duration_seconds: float) -> None:
        self.adj.setdefault(src, []).append(ContactEdge(dst, rssi, duration_seconds))

    def shortest_path(self, src: str, dst: str) -> list[str]:
        pq: list[tuple[float, str, list[str]]] = [(0.0, src, [src])]
        best: dict[str, float] = {src: 0.0}
        while pq:
            cost, node, path = heapq.heappop(pq)
            if node == dst:
                return path
            for edge in self.adj.get(node, []):
                new_cost = cost + edge.cost
                if new_cost < best.get(edge.to_node, float("inf")):
                    best[edge.to_node] = new_cost
                    heapq.heappush(pq, (new_cost, edge.to_node, path + [edge.to_node]))
        return []
