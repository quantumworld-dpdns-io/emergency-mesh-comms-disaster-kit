from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RetentionPolicy:
    table: str
    timestamp_column: str
    keep_days: int


class RetentionManager:
    def __init__(self, conn) -> None:
        self.conn = conn

    def purge(self, policy: RetentionPolicy) -> int:
        q = (
            f"DELETE FROM {policy.table} "
            f"WHERE {policy.timestamp_column} < NOW() - INTERVAL '{policy.keep_days} days'"
        )
        cur = self.conn.execute(q)
        return cur.rowcount if hasattr(cur, "rowcount") else 0
