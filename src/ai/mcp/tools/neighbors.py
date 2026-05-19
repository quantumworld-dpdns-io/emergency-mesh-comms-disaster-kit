from __future__ import annotations

import httpx


async def query_neighbors(api_base_url: str, bearer_token: str) -> list[dict[str, object]]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"{api_base_url.rstrip('/')}/api/v1/neighbors",
            headers={"Authorization": f"Bearer {bearer_token}"},
        )
        resp.raise_for_status()
        return list(resp.json())
