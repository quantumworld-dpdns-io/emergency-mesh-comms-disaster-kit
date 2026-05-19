from __future__ import annotations


async def inspect_bundle_queue(depth: int, emergency_count: int) -> dict[str, int]:
    return {"depth": depth, "emergency_count": emergency_count}
