from __future__ import annotations


def fallback_route_decision(topology_size: int, queue_depth: int) -> str:
    if topology_size <= 2:
        return "epidemic"
    if queue_depth > 100:
        return "spray_wait"
    return "prophet"


def fallback_triage(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["bleeding", "injury", "medical"]):
        return "medical"
    if any(k in t for k in ["fire", "rescue", "trapped"]):
        return "rescue"
    if any(k in t for k in ["water", "food", "supply"]):
        return "supply"
    return "comms"
