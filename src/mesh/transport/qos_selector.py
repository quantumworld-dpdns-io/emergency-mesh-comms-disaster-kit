from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class QoSMetric:
    bandwidth_bps: float
    lqi: float
    latency_ms: float


def qos_score(metric: QoSMetric) -> float:
    latency = max(metric.latency_ms, 1.0)
    return (metric.bandwidth_bps * metric.lqi) / latency


class QoSSelector:
    def select(self, metrics: dict[str, QoSMetric]) -> str | None:
        if not metrics:
            return None
        return max(metrics.items(), key=lambda kv: qos_score(kv[1]))[0]
