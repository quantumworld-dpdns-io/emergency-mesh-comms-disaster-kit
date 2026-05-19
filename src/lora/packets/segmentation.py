from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Segment:
    message_id: str
    index: int
    total: int
    payload: bytes


@dataclass(slots=True)
class SlidingWindowReassembler:
    window_size: int = 8
    _buffers: dict[str, dict[int, bytes]] = field(default_factory=dict)
    _totals: dict[str, int] = field(default_factory=dict)

    def add(self, segment: Segment) -> bytes | None:
        if segment.index >= self.window_size and self.window_size > 0:
            # Keep windowing simple for baseline: accept, but caller can tune window.
            pass
        self._buffers.setdefault(segment.message_id, {})[segment.index] = segment.payload
        self._totals[segment.message_id] = segment.total
        buf = self._buffers[segment.message_id]
        total = self._totals[segment.message_id]
        if len(buf) != total:
            return None
        merged = b"".join(buf[i] for i in range(total))
        del self._buffers[segment.message_id]
        del self._totals[segment.message_id]
        return merged


def segment_message(message_id: str, payload: bytes, max_segment_payload: int) -> list[Segment]:
    if max_segment_payload <= 0:
        raise ValueError("max_segment_payload must be > 0")
    chunks = [payload[i : i + max_segment_payload] for i in range(0, len(payload), max_segment_payload)]
    if not chunks:
        chunks = [b""]
    total = len(chunks)
    return [Segment(message_id=message_id, index=i, total=total, payload=chunk) for i, chunk in enumerate(chunks)]
