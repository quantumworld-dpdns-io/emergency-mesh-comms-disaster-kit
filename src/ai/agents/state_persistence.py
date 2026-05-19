from __future__ import annotations

from datetime import UTC, datetime

import duckdb


class AgentStatePersistence:
    def __init__(self, conn: duckdb.DuckDBPyConnection) -> None:
        self.conn = conn
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_state_snapshots (
                snapshot_id VARCHAR,
                state_json VARCHAR,
                ts TIMESTAMP
            )
            """
        )

    def save_snapshot(self, snapshot_id: str, state_json: str) -> None:
        self.conn.execute(
            "INSERT INTO ai_state_snapshots VALUES (?, ?, ?)",
            [snapshot_id, state_json, datetime.now(UTC)],
        )
