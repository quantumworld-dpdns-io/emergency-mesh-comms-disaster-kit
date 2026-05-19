from __future__ import annotations

import asyncio


class SecurityAlerter:
    def __init__(self) -> None:
        self.queue: asyncio.Queue[dict[str, object]] = asyncio.Queue()

    async def emit_if_high(self, event: dict[str, object]) -> bool:
        if str(event.get("severity", "low")).lower() in {"high", "critical"}:
            await self.queue.put(event)
            return True
        return False
