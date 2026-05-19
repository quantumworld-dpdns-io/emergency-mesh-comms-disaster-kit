from __future__ import annotations


class BandwidthEstimator:
    def __init__(self, alpha: float = 0.2) -> None:
        self.alpha = alpha
        self._ewma: dict[str, float] = {}

    def record(self, transport: str, bytes_sent: int, seconds: float) -> float:
        rate = 0.0 if seconds <= 0 else bytes_sent / seconds
        previous = self._ewma.get(transport, rate)
        updated = self.alpha * rate + (1 - self.alpha) * previous
        self._ewma[transport] = updated
        return updated

    def get(self, transport: str) -> float:
        return self._ewma.get(transport, 0.0)
