from __future__ import annotations

import aiosqlite

from src.mesh.protocol.bundle import Bundle
from src.mesh.protocol.serializer import decode_bundle, encode_bundle


class BundleStore:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path

    async def initialize(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS bundles (
                    bundle_id TEXT PRIMARY KEY,
                    priority INTEGER NOT NULL,
                    expires_at INTEGER NOT NULL,
                    payload BLOB NOT NULL
                )
                """
            )
            await db.commit()

    async def enqueue(self, bundle: Bundle, expires_at_epoch: int, priority: int) -> None:
        raw = encode_bundle(bundle)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO bundles(bundle_id, priority, expires_at, payload) VALUES (?, ?, ?, ?)",
                (bundle.bundle_id, priority, expires_at_epoch, raw),
            )
            await db.commit()

    async def dequeue_next(self) -> Bundle | None:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT bundle_id, payload FROM bundles ORDER BY priority DESC, expires_at ASC LIMIT 1"
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            await db.execute("DELETE FROM bundles WHERE bundle_id = ?", (row[0],))
            await db.commit()
            return decode_bundle(row[1])

    async def delete_expired(self, now_epoch: int) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("DELETE FROM bundles WHERE expires_at < ?", (now_epoch,))
            await db.commit()
            return cursor.rowcount
