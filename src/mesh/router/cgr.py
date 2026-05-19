from __future__ import annotations

from .contact_graph import ContactGraph


class CgrRouter:
    def __init__(self, graph: ContactGraph | None = None) -> None:
        self.graph = graph or ContactGraph()

    def next_hop(self, src: str, dst: str) -> str | None:
        path = self.graph.shortest_path(src, dst)
        if len(path) < 2:
            return None
        return path[1]
