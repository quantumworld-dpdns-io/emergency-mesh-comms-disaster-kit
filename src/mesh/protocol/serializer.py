from __future__ import annotations

from datetime import datetime

import cbor2

from .bundle import Bundle


def encode_bundle(bundle: Bundle) -> bytes:
    data = bundle.model_dump(mode="python")
    data["primary"]["creation_ts"] = bundle.primary.creation_ts.isoformat()
    return cbor2.dumps(data)


def decode_bundle(raw: bytes) -> Bundle:
    data = cbor2.loads(raw)
    primary = data.get("primary", {})
    creation_ts = primary.get("creation_ts")
    if isinstance(creation_ts, str):
        primary["creation_ts"] = datetime.fromisoformat(creation_ts)
    if isinstance(data.get("payload"), str):
        data["payload"] = data["payload"].encode("utf-8")
    if isinstance(data.get("payload"), bytearray):
        data["payload"] = bytes(data["payload"])
    return Bundle.model_validate(data)
