from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass

from .client import MeshRedisClient


@dataclass(slots=True)
class RedisEvent:
    channel: str
    payload: dict[str, object]


class RedisPubSubDispatcher:
    def __init__(self, redis_client: MeshRedisClient) -> None:
        self.redis_client = redis_client

    async def publish(self, channel: str, payload: dict[str, object]) -> int:
        return int(await self.redis_client.client.publish(channel, json.dumps(payload)))

    async def subscribe(self, channel: str) -> asyncio.Queue[RedisEvent]:
        queue: asyncio.Queue[RedisEvent] = asyncio.Queue()
        pubsub = self.redis_client.client.pubsub()
        await pubsub.subscribe(channel)

        async def _reader() -> None:
            async for msg in pubsub.listen():
                if msg.get("type") != "message":
                    continue
                raw = msg.get("data")
                data = json.loads(raw) if isinstance(raw, str) else {}
                await queue.put(RedisEvent(channel=channel, payload=data))

        asyncio.create_task(_reader())
        return queue
