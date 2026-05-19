from __future__ import annotations

import pyarrow as pa

BUNDLE_EVENT_SCHEMA = pa.schema(
    [
        ("event_id", pa.int64()),
        ("bundle_id", pa.string()),
        ("action", pa.string()),
        ("node_id", pa.string()),
        ("ts", pa.timestamp("us")),
    ]
)

NEIGHBOR_SCHEMA = pa.schema(
    [
        ("node_id", pa.string()),
        ("neighbor_id", pa.string()),
        ("lqi", pa.float64()),
    ]
)
