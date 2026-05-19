from __future__ import annotations

import pyarrow as pa


def to_ipc_stream(table: pa.Table) -> bytes:
    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchStreamWriter(sink, table.schema) as writer:
        writer.write_table(table)
    return sink.getvalue().to_pybytes()


def from_ipc_stream(payload: bytes) -> pa.Table:
    reader = pa.ipc.RecordBatchStreamReader(pa.BufferReader(payload))
    return reader.read_all()
