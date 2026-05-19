from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


@dataclass(slots=True)
class DutyCycleLimiter:
    duty_cycle_limit: float = 0.01
    window_seconds: int = 3600
    _tx_windows: deque[tuple[float, float]] = field(default_factory=deque)

    def allow_tx(self, now: float, airtime_seconds: float) -> bool:
        cutoff = now - self.window_seconds
        while self._tx_windows and self._tx_windows[0][0] < cutoff:
            self._tx_windows.popleft()
        used = sum(a for _, a in self._tx_windows)
        if used + airtime_seconds > self.window_seconds * self.duty_cycle_limit:
            return False
        self._tx_windows.append((now, airtime_seconds))
        return True
