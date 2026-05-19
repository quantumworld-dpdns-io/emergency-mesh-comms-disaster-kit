from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(slots=True)
class ChainedAuditRecord:
    payload: dict[str, object]
    prev_hash: str
    hash: str


class AuditIntegrityChain:
    def __init__(self) -> None:
        self._last_hash = "0" * 64

    def append(self, payload: dict[str, object]) -> ChainedAuditRecord:
        material = json.dumps(payload, sort_keys=True).encode("utf-8") + self._last_hash.encode("utf-8")
        digest = hashlib.sha256(material).hexdigest()
        record = ChainedAuditRecord(payload=payload, prev_hash=self._last_hash, hash=digest)
        self._last_hash = digest
        return record
