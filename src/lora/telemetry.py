from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

import duckdb


@dataclass(slots=True)
class LoRaTelemetryRecord:
    node_id: str
    rssi: float
    snr: float
    recorded_at: datetime


class LoRaTelemetryStore:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = duckdb.connect(db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS lora_telemetry (
                node_id VARCHAR,
                rssi DOUBLE,
                snr DOUBLE,
                recorded_at TIMESTAMP
            )
            """
        )

    def add(self, node_id: str, rssi: float, snr: float) -> None:
        self.conn.execute(
            "INSERT INTO lora_telemetry VALUES (?, ?, ?, ?)",
            [node_id, rssi, snr, datetime.now(UTC)],
        )
