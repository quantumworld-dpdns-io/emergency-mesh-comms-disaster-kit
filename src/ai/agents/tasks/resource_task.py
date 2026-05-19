from __future__ import annotations


def optimize_bandwidth(total_kbps: int, emergency_share: float) -> dict[str, int]:
    emergency = int(total_kbps * emergency_share)
    general = max(total_kbps - emergency, 0)
    return {"emergency_kbps": emergency, "general_kbps": general}
