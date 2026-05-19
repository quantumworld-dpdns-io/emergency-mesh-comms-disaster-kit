from __future__ import annotations

from .client import MeshRedisClient
from .schema import KEY_NODE_GEO


class RedisGeoIndex:
    def __init__(self, redis_client: MeshRedisClient) -> None:
        self.redis_client = redis_client

    async def set_node_position(self, node_id: str, lon: float, lat: float) -> int:
        return int(await self.redis_client.client.geoadd(KEY_NODE_GEO, [lon, lat, node_id]))

    async def nearby(self, lon: float, lat: float, radius_km: float) -> list[str]:
        rows = await self.redis_client.client.georadius(KEY_NODE_GEO, lon, lat, radius_km, unit="km")
        return [str(r) for r in rows]
