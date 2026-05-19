from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LinkStateAdvertisement:
    origin: str
    sequence: int
    neighbors: list[str]


class LSAManager:
    def __init__(self) -> None:
        self.latest_seq_by_origin: dict[str, int] = {}

    def should_accept(self, lsa: LinkStateAdvertisement) -> bool:
        current = self.latest_seq_by_origin.get(lsa.origin, -1)
        if lsa.sequence <= current:
            return False
        self.latest_seq_by_origin[lsa.origin] = lsa.sequence
        return True
