from __future__ import annotations

import asyncio
import time

import duckdb

from src.config import settings
from src.data.arrow.flight_server import MeshFlightServer
from src.data.duckdb.schema import initialize_schema
from src.data.redis.client import MeshRedisClient
from src.logging_config import configure_logging
from src.mesh.protocol.bundle import Bundle
from src.mesh.router.bundle_store import BundleStore
from src.mesh.router.expiry_worker import ExpiryWorker
from src.mesh.router.factory import RouterFactory


class MeshApplication:
    def __init__(self, strategy: str = "epidemic", db_path: str = ":memory:") -> None:
        self.router = RouterFactory.create(strategy)
        self.store = BundleStore(db_path=db_path)
        self.expiry_worker = ExpiryWorker(self.store, poll_interval_seconds=30.0)

        self.redis = MeshRedisClient(settings.redis_url)
        self.duck_conn = duckdb.connect(settings.duckdb_path)
        self.flight_server = MeshFlightServer(settings.arrow_flight_host, settings.arrow_flight_port)

        self._running = False

    async def enqueue_bundle(self, bundle: Bundle) -> None:
        now = int(time.time())
        expires = now + bundle.primary.ttl_seconds
        priority = {"general": 1, "medical": 2, "emergency": 3}[bundle.primary.priority.value]
        await self.store.enqueue(bundle, expires_at_epoch=expires, priority=priority)

    async def start(self) -> None:
        await self.redis.connect()
        initialize_schema(self.duck_conn)
        await self.store.initialize()
        self._running = True
        self.expiry_worker.start()
        while self._running:
            _bundle = await self.store.dequeue_next()
            await asyncio.sleep(0.2)

    async def stop(self) -> None:
        self._running = False
        await self.expiry_worker.stop()
        await self.redis.close()
        self.duck_conn.close()


def main() -> None:
    configure_logging()
    asyncio.run(MeshApplication().start())


if __name__ == "__main__":
    main()
