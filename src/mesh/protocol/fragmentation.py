from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass(slots=True)
class Fragment:
    bundle_id: str
    fragment_index: int
    total_fragments: int
    payload: bytes


@dataclass(slots=True)
class ReassemblyBuffer:
    _parts: dict[str, dict[int, bytes]] = field(default_factory=lambda: defaultdict(dict))
    _totals: dict[str, int] = field(default_factory=dict)

    def add(self, fragment: Fragment) -> bytes | None:
        self._parts[fragment.bundle_id][fragment.fragment_index] = fragment.payload
        self._totals[fragment.bundle_id] = fragment.total_fragments
        parts = self._parts[fragment.bundle_id]
        total = self._totals[fragment.bundle_id]
        if len(parts) != total:
            return None
        payload = b"".join(parts[i] for i in range(total))
        del self._parts[fragment.bundle_id]
        del self._totals[fragment.bundle_id]
        return payload


def fragment_payload(bundle_id: str, payload: bytes, max_payload: int) -> list[Fragment]:
    if max_payload <= 0:
        raise ValueError("max_payload must be > 0")
    chunks = [payload[i : i + max_payload] for i in range(0, len(payload), max_payload)]
    total = len(chunks) or 1
    if not chunks:
        chunks = [b""]
    return [
        Fragment(bundle_id=bundle_id, fragment_index=i, total_fragments=total, payload=chunk)
        for i, chunk in enumerate(chunks)
    ]
