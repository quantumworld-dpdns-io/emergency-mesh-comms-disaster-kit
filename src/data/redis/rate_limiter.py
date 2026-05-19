from __future__ import annotations

import time

from .client import MeshRedisClient
from .schema import KEY_RATE_LIMIT_PREFIX


class RedisRateLimiter:
    def __init__(self, redis_client: MeshRedisClient) -> None:
        self.redis_client = redis_client

    async def allow(self, key: str, limit: int, window_seconds: int) -> bool:
        now = time.time()
        bucket = f"{KEY_RATE_LIMIT_PREFIX}:{key}"
        min_score = now - window_seconds
        pipe = self.redis_client.client.pipeline()
        pipe.zremrangebyscore(bucket, "-inf", min_score)
        pipe.zadd(bucket, {f"{now}": now})
        pipe.zcard(bucket)
        pipe.expire(bucket, window_seconds)
        _, _, count, _ = await pipe.execute()
        return int(count) <= limit
