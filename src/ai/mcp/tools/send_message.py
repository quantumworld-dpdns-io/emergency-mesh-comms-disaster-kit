from __future__ import annotations

import httpx


async def send_message(api_base_url: str, bearer_token: str, to_eid: str, text: str) -> dict[str, object]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{api_base_url.rstrip('/')}/api/v1/messages",
            headers={"Authorization": f"Bearer {bearer_token}", "X-API-Key": "dev-api-key"},
            json={"to_eid": to_eid, "text": text, "priority": "general"},
        )
        resp.raise_for_status()
        return dict(resp.json())
