from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RoutingSample:
    lqi: float
    queue_depth: float
    topology_size: float
    delivered: float


class RoutingModelTask:
    """Simple linear model task abstraction for delivery probability."""

    def __init__(self, weights: list[float] | None = None) -> None:
        self.weights = weights or [0.4, -0.2, 0.1, 0.0]

    def predict(self, sample: RoutingSample) -> float:
        x = [sample.lqi / 100.0, sample.queue_depth / 500.0, sample.topology_size / 20.0, 1.0]
        z = sum(w * v for w, v in zip(self.weights, x, strict=True))
        return 1.0 / (1.0 + pow(2.718281828, -z))

    def train_step(self, batch: list[RoutingSample], lr: float = 0.05) -> float:
        if not batch:
            return 0.0
        grads = [0.0, 0.0, 0.0, 0.0]
        loss = 0.0
        for s in batch:
            yhat = self.predict(s)
            y = s.delivered
            err = yhat - y
            x = [s.lqi / 100.0, s.queue_depth / 500.0, s.topology_size / 20.0, 1.0]
            for i in range(4):
                grads[i] += err * x[i]
            loss += err * err
        n = float(len(batch))
        for i in range(4):
            self.weights[i] -= lr * (grads[i] / n)
        return loss / n
