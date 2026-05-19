from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from src.data.redis.schema import KEY_AUDIT_STREAM

from ..redis.client import MeshRedisClient


class StreamETL:
    def __init__(self, redis_client: MeshRedisClient, duck_conn) -> None:
        self.redis_client = redis_client
        self.duck_conn = duck_conn
        self._running = False

    async def run_once(self, count: int = 100) -> int:
        rows = await self.redis_client.client.xrevrange(KEY_AUDIT_STREAM, count=count)
        inserted = 0
        for event_id, payload in rows:
            self.duck_conn.execute(
                "INSERT INTO bundle_events VALUES (?, ?, ?, ?, ?)",
                [
                    int(str(event_id).split("-")[0]),
                    payload.get("bundle_id", ""),
                    payload.get("action", ""),
                    payload.get("node_id", ""),
                    datetime.now(UTC),
                ],
            )
            inserted += 1
        return inserted

    async def run_forever(self, poll_seconds: float = 60.0) -> None:
        self._running = True
        while self._running:
            await self.run_once()
            await asyncio.sleep(poll_seconds)

    def stop(self) -> None:
        self._running = False
