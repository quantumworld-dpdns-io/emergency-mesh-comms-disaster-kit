from __future__ import annotations

import duckdb

from src.data.duckdb.bundle_analytics import BundleAnalytics
from src.data.duckdb.schema import initialize_schema


def test_duckdb_schema_and_analytics_smoke() -> None:
    conn = duckdb.connect(":memory:")
    initialize_schema(conn)
    conn.execute(
        "INSERT INTO bundle_delivery VALUES ('b1', NOW() - INTERVAL '5 seconds', NOW(), 1)"
    )
    a = BundleAnalytics(conn)
    assert a.delivery_ratio() == 1.0
    assert a.avg_latency_seconds() >= 0.0
