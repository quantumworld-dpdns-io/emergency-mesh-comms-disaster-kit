from __future__ import annotations

import time


class ReplayProtector:
    def __init__(self, window_seconds: int = 120) -> None:
        self.window_seconds = window_seconds
        self._seen: dict[str, float] = {}

    def is_replay(self, nonce: str, ts_epoch: float) -> bool:
        now = time.time()
        if abs(now - ts_epoch) > self.window_seconds:
            return True
        self._seen = {k: v for k, v in self._seen.items() if now - v <= self.window_seconds}
        if nonce in self._seen:
            return True
        self._seen[nonce] = ts_epoch
        return False
