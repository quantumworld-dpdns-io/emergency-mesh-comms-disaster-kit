from __future__ import annotations

from .client import MeshRedisClient
from .schema import KEY_AUDIT_STREAM


class RedisAuditStream:
    def __init__(self, redis_client: MeshRedisClient) -> None:
        self.redis_client = redis_client

    async def add_event(self, action: str, bundle_id: str, node_id: str) -> str:
        return str(
            await self.redis_client.client.xadd(
                KEY_AUDIT_STREAM,
                {"action": action, "bundle_id": bundle_id, "node_id": node_id},
            )
        )
