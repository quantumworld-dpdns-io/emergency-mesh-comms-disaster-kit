from __future__ import annotations

import duckdb


class BundleAnalytics:
    def __init__(self, conn: duckdb.DuckDBPyConnection) -> None:
        self.conn = conn

    def delivery_ratio(self) -> float:
        row = self.conn.execute(
            """
            SELECT
              CASE WHEN COUNT(*) = 0 THEN 0.0
              ELSE SUM(CASE WHEN delivered_ts IS NOT NULL THEN 1 ELSE 0 END)::DOUBLE / COUNT(*)
              END
            FROM bundle_delivery
            """
        ).fetchone()
        return float(row[0])

    def avg_latency_seconds(self) -> float:
        row = self.conn.execute(
            """
            SELECT COALESCE(AVG(EXTRACT(EPOCH FROM (delivered_ts - created_ts))), 0.0)
            FROM bundle_delivery
            WHERE delivered_ts IS NOT NULL
            """
        ).fetchone()
        return float(row[0])
