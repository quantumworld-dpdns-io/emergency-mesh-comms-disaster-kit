from __future__ import annotations

from pathlib import Path

import duckdb


class DuckDBExporter:
    def __init__(self, conn: duckdb.DuckDBPyConnection) -> None:
        self.conn = conn

    def export_table_parquet(self, table: str, output_path: str) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn.execute(f"COPY {table} TO '{path.as_posix()}' (FORMAT PARQUET)")
