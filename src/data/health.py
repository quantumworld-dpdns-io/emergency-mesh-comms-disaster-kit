from __future__ import annotations

import time


class DataHealth:
    def __init__(self, redis_client, duck_conn, arrow_server) -> None:
        self.redis_client = redis_client
        self.duck_conn = duck_conn
        self.arrow_server = arrow_server

    async def check(self) -> dict[str, object]:
        start = time.perf_counter()
        redis_ok = await self.redis_client.ping()
        redis_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        self.duck_conn.execute("SELECT 1")
        duck_ms = (time.perf_counter() - start) * 1000

        arrow_ok = self.arrow_server is not None

        return {
            "redis": {"ok": redis_ok, "latency_ms": round(redis_ms, 2)},
            "duckdb": {"ok": True, "latency_ms": round(duck_ms, 2)},
            "arrow": {"ok": arrow_ok},
        }
