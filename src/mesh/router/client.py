from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MeshRouterClient:
    target: str

    async def enqueue_bundle(self, bundle_id: str, payload: bytes) -> dict[str, object]:
        # Placeholder until generated gRPC stubs are added.
        return {"target": self.target, "bundle_id": bundle_id, "accepted": True, "size": len(payload)}

    async def get_neighbor_summary(self) -> list[dict[str, object]]:
        return []
