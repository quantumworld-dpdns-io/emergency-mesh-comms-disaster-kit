from __future__ import annotations

import duckdb


class NeighborAnalytics:
    def __init__(self, conn: duckdb.DuckDBPyConnection) -> None:
        self.conn = conn

    def contact_frequency(self) -> list[tuple[str, int]]:
        rows = self.conn.execute(
            "SELECT neighbor_id, COUNT(*) AS c FROM neighbor_contacts GROUP BY neighbor_id ORDER BY c DESC"
        ).fetchall()
        return [(str(r[0]), int(r[1])) for r in rows]

    def avg_uptime_seconds(self) -> float:
        row = self.conn.execute(
            """
            SELECT COALESCE(AVG(EXTRACT(EPOCH FROM (ended_ts - started_ts))), 0.0)
            FROM neighbor_contacts
            """
        ).fetchone()
        return float(row[0])
