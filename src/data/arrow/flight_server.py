from __future__ import annotations

import pyarrow as pa
import pyarrow.flight as flight


class MeshFlightServer(flight.FlightServerBase):
    def __init__(self, host: str = "0.0.0.0", port: int = 8815) -> None:
        super().__init__(location=f"grpc://{host}:{port}")
        self._tables: dict[str, pa.Table] = {}

    def put_table(self, name: str, table: pa.Table) -> None:
        self._tables[name] = table

    def do_get(self, _context, ticket: flight.Ticket):
        key = ticket.ticket.decode("utf-8")
        table = self._tables.get(key, pa.table({}))
        return flight.RecordBatchStream(table)
