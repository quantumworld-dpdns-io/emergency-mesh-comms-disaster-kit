from __future__ import annotations

import hashlib
from pathlib import Path


class ProcessAllowlist:
    def __init__(self, allowed_hashes: set[str] | None = None) -> None:
        self.allowed_hashes = allowed_hashes or set()

    @staticmethod
    def file_sha256(path: str) -> str:
        data = Path(path).read_bytes()
        return hashlib.sha256(data).hexdigest()

    def is_allowed(self, binary_hash: str) -> bool:
        return binary_hash in self.allowed_hashes
