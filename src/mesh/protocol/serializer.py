from __future__ import annotations

import cbor2

from .bundle import Bundle


def encode_bundle(bundle: Bundle) -> bytes:
    return cbor2.dumps(bundle.model_dump(mode="json"))


def decode_bundle(raw: bytes) -> Bundle:
    data = cbor2.loads(raw)
    if isinstance(data.get("payload"), str):
        data["payload"] = data["payload"].encode("utf-8")
    return Bundle.model_validate(data)
