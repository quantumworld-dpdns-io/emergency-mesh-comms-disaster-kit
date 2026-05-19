from __future__ import annotations

import httpx


async def send_emergency_broadcast(api_base_url: str, message: str, bearer_token: str) -> dict[str, object]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{api_base_url.rstrip('/')}/api/v1/emergency",
            params={"message": message},
            headers={"Authorization": f"Bearer {bearer_token}"},
        )
        resp.raise_for_status()
        return dict(resp.json())
