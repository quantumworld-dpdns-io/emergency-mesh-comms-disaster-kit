from __future__ import annotations

import httpx


async def query_topology(api_base_url: str) -> dict[str, object]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{api_base_url.rstrip('/')}/api/v1/topology")
        resp.raise_for_status()
        return dict(resp.json())
