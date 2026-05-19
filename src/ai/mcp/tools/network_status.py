from __future__ import annotations

import httpx


async def get_network_status(api_base_url: str, bearer_token: str) -> dict[str, object]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        status = await client.get(
            f"{api_base_url.rstrip('/')}/api/v1/status",
            headers={"Authorization": f"Bearer {bearer_token}"},
        )
        status.raise_for_status()
        neighbors = await client.get(
            f"{api_base_url.rstrip('/')}/api/v1/neighbors",
            headers={"Authorization": f"Bearer {bearer_token}"},
        )
        neighbors.raise_for_status()
    return {"status": dict(status.json()), "neighbor_count": len(neighbors.json())}
