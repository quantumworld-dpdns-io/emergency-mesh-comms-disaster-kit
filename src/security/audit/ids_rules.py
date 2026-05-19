from __future__ import annotations

from .tetragon import TetragonEvent


def detect_replay(event: TetragonEvent) -> bool:
    return bool(event.metadata.get("replay_detected", False))


def detect_signature_flood(event: TetragonEvent) -> bool:
    return int(event.metadata.get("signature_errors", 0)) > 20


def detect_routing_loop(event: TetragonEvent) -> bool:
    return int(event.metadata.get("hop_count", 0)) > 30
