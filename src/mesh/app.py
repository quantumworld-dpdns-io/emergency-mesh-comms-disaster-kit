from __future__ import annotations

import asyncio

from src.logging_config import configure_logging


class MeshApplication:
    def __init__(self) -> None:
        self._running = False

    async def start(self) -> None:
        self._running = True
        while self._running:
            await asyncio.sleep(0.5)

    async def stop(self) -> None:
        self._running = False


def main() -> None:
    configure_logging()
    asyncio.run(MeshApplication().start())


if __name__ == "__main__":
    main()
