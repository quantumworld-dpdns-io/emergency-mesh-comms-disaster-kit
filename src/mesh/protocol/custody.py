from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CustodyDisposition(str, Enum):
    accepted = "accepted"
    rejected = "rejected"
    failed = "failed"


@dataclass(slots=True)
class CustodySignal:
    bundle_id: str
    from_node: str
    disposition: CustodyDisposition
    reason: str | None = None


@dataclass(slots=True)
class RetransmissionPolicy:
    max_retries: int = 3
    base_delay_seconds: float = 1.0

    def next_delay(self, attempt: int) -> float:
        bounded = min(attempt, self.max_retries)
        return self.base_delay_seconds * (2**bounded)
