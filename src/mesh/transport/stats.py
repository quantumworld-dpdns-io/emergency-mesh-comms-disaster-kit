from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TransportStats:
    tx_bytes: int = 0
    rx_bytes: int = 0
    errors: int = 0
    latency_ms_avg: float = 0.0


class StatsCollector:
    def __init__(self) -> None:
        self._stats: dict[str, TransportStats] = {}

    def _get(self, name: str) -> TransportStats:
        if name not in self._stats:
            self._stats[name] = TransportStats()
        return self._stats[name]

    def record_tx(self, name: str, size: int) -> None:
        self._get(name).tx_bytes += size

    def record_rx(self, name: str, size: int) -> None:
        self._get(name).rx_bytes += size

    def record_error(self, name: str) -> None:
        self._get(name).errors += 1

    def record_latency(self, name: str, latency_ms: float, alpha: float = 0.2) -> None:
        s = self._get(name)
        s.latency_ms_avg = alpha * latency_ms + (1 - alpha) * s.latency_ms_avg

    def snapshot(self) -> dict[str, TransportStats]:
        return dict(self._stats)
