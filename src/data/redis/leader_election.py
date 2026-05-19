from __future__ import annotations

import uuid

from .client import MeshRedisClient
from .schema import KEY_LOCK_PREFIX


class RedisLeaderElection:
    def __init__(self, redis_client: MeshRedisClient, name: str = "mesh-leader") -> None:
        self.redis_client = redis_client
        self.name = name
        self.owner_token = str(uuid.uuid4())

    @property
    def _key(self) -> str:
        return f"{KEY_LOCK_PREFIX}:{self.name}"

    async def try_acquire(self, ttl_seconds: int = 15) -> bool:
        return bool(
            await self.redis_client.client.set(self._key, self.owner_token, nx=True, ex=ttl_seconds)
        )

    async def release(self) -> None:
        token = await self.redis_client.client.get(self._key)
        if token == self.owner_token:
            await self.redis_client.client.delete(self._key)
