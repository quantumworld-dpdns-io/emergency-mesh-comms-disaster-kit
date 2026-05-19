from __future__ import annotations

import hashlib


class RollingDeduplicator:
    def __init__(self, max_entries: int = 50000) -> None:
        self.max_entries = max_entries
        self._entries: set[str] = set()

    @staticmethod
    def _fingerprint(bundle_id: str) -> str:
        return hashlib.sha256(bundle_id.encode("utf-8")).hexdigest()

    def seen(self, bundle_id: str) -> bool:
        fp = self._fingerprint(bundle_id)
        if fp in self._entries:
            return True
        if len(self._entries) >= self.max_entries:
            # Bounded-memory approximation for rolling behavior.
            self._entries.pop()
        self._entries.add(fp)
        return False
