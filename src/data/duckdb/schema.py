from __future__ import annotations

import duckdb


def initialize_schema(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS bundle_events (
            event_id BIGINT,
            bundle_id VARCHAR,
            action VARCHAR,
            node_id VARCHAR,
            ts TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS bundle_delivery (
            bundle_id VARCHAR,
            created_ts TIMESTAMP,
            delivered_ts TIMESTAMP,
            hops INTEGER
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS neighbor_contacts (
            node_id VARCHAR,
            neighbor_id VARCHAR,
            started_ts TIMESTAMP,
            ended_ts TIMESTAMP,
            lqi DOUBLE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lora_telemetry (
            node_id VARCHAR,
            rssi DOUBLE,
            snr DOUBLE,
            recorded_at TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ai_state_snapshots (
            snapshot_id VARCHAR,
            state_json VARCHAR,
            ts TIMESTAMP
        )
        """
    )
