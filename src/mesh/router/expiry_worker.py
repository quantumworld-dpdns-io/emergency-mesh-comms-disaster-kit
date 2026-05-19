from __future__ import annotations

import asyncio
import time

from .bundle_store import BundleStore


class ExpiryWorker:
    def __init__(self, store: BundleStore, poll_interval_seconds: float = 30.0) -> None:
        self.store = store
        self.poll_interval_seconds = poll_interval_seconds
        self._task: asyncio.Task[None] | None = None
        self._stop = asyncio.Event()

    async def _run(self) -> None:
        while not self._stop.is_set():
            await self.store.delete_expired(int(time.time()))
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=self.poll_interval_seconds)
            except TimeoutError:
                continue

    def start(self) -> None:
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        self._stop.set()
        if self._task:
            await self._task
