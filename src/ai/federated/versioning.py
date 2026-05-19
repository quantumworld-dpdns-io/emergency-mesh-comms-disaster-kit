from __future__ import annotations

import json
from pathlib import Path

import duckdb


class FederatedModelVersioning:
    def __init__(self, conn: duckdb.DuckDBPyConnection, model_dir: str = "data/federated") -> None:
        self.conn = conn
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS federated_model_versions (
                version VARCHAR,
                path VARCHAR,
                created_ts TIMESTAMP DEFAULT NOW(),
                active BOOLEAN
            )
            """
        )

    def save_version(self, version: str, weights: list[float], active: bool = True) -> Path:
        path = self.model_dir / f"routing_model_{version}.json"
        path.write_text(json.dumps({"weights": weights}), encoding="utf-8")
        if active:
            self.conn.execute("UPDATE federated_model_versions SET active = FALSE")
        self.conn.execute(
            "INSERT INTO federated_model_versions(version, path, active) VALUES (?, ?, ?)",
            [version, str(path), active],
        )
        return path

    def rollback(self, version: str) -> Path:
        row = self.conn.execute(
            "SELECT path FROM federated_model_versions WHERE version = ?", [version]
        ).fetchone()
        if row is None:
            raise ValueError("unknown version")
        self.conn.execute("UPDATE federated_model_versions SET active = FALSE")
        self.conn.execute("UPDATE federated_model_versions SET active = TRUE WHERE version = ?", [version])
        return Path(str(row[0]))

    def active_model_path(self) -> Path | None:
        row = self.conn.execute(
            "SELECT path FROM federated_model_versions WHERE active = TRUE ORDER BY created_ts DESC LIMIT 1"
        ).fetchone()
        return Path(str(row[0])) if row else None
