from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta


@dataclass(slots=True)
class Neighbor:
    node_id: str
    eid: str
    lqi: float
    last_seen: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(slots=True)
class RoutingEntry:
    destination_eid: str
    next_hop: str
    cost: float
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class RoutingTable:
    def __init__(self, neighbor_ttl_seconds: int = 90) -> None:
        self.neighbor_ttl = timedelta(seconds=neighbor_ttl_seconds)
        self.neighbors: dict[str, Neighbor] = {}
        self.routes: dict[str, RoutingEntry] = {}

    def upsert_neighbor(self, neighbor: Neighbor) -> None:
        neighbor.last_seen = datetime.now(UTC)
        self.neighbors[neighbor.node_id] = neighbor

    def set_route(self, entry: RoutingEntry) -> None:
        entry.updated_at = datetime.now(UTC)
        self.routes[entry.destination_eid] = entry

    def get_route(self, destination_eid: str) -> RoutingEntry | None:
        self.evict_stale_neighbors()
        return self.routes.get(destination_eid)

    def evict_stale_neighbors(self) -> None:
        now = datetime.now(UTC)
        expired = [nid for nid, n in self.neighbors.items() if now - n.last_seen > self.neighbor_ttl]
        for nid in expired:
            del self.neighbors[nid]
