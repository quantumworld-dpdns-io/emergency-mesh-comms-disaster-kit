import pytest

from src.data.redis.client import MeshRedisClient


@pytest.mark.asyncio
async def test_redis_client_init_only() -> None:
    c = MeshRedisClient("redis://localhost:6379/0")
    assert c.url.startswith("redis://")
