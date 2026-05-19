from __future__ import annotations

import asyncio

from redis.asyncio import Redis


class MeshRedisClient:
    def __init__(self, url: str, max_retries: int = 3, base_backoff_seconds: float = 0.2) -> None:
        self.url = url
        self.max_retries = max_retries
        self.base_backoff_seconds = base_backoff_seconds
        self._client: Redis | None = None

    @property
    def client(self) -> Redis:
        if self._client is None:
            raise RuntimeError("redis client not connected")
        return self._client

    async def connect(self) -> None:
        self._client = Redis.from_url(self.url, decode_responses=True)
        await self._with_retry(self._client.ping)

    async def close(self) -> None:
        if self._client is not None:
            await self._client.close()
            self._client = None

    async def ping(self) -> bool:
        return bool(await self._with_retry(self.client.ping))

    async def _with_retry(self, fn):
        last_err: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                return await fn()
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                if attempt >= self.max_retries:
                    break
                await asyncio.sleep(self.base_backoff_seconds * (2**attempt))
        raise RuntimeError("redis operation failed") from last_err
