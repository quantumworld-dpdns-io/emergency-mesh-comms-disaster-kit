from __future__ import annotations

from dataclasses import dataclass

from src.ai.observability.phoenix import PhoenixTracer

from .flower_client import MeshFlowerClient


@dataclass(slots=True)
class RoundMetrics:
    round_num: int
    avg_loss: float
    accuracy: float


class MeshFlowerServer:
    def __init__(self, min_clients: int = 2, rounds: int = 3, tracer: PhoenixTracer | None = None) -> None:
        self.min_clients = min_clients
        self.rounds = rounds
        self.tracer = tracer or PhoenixTracer()
        self.metrics: list[RoundMetrics] = []

    def _fedavg(self, weighted: list[tuple[list[float], int]]) -> list[float]:
        total = sum(n for _, n in weighted)
        if total == 0:
            return [0.0, 0.0, 0.0, 0.0]
        dim = len(weighted[0][0])
        out = [0.0] * dim
        for w, n in weighted:
            for i in range(dim):
                out[i] += w[i] * n
        return [v / total for v in out]

    def train(self, clients: list[MeshFlowerClient], initial_weights: list[float]) -> list[float]:
        if len(clients) < self.min_clients:
            raise ValueError("not enough clients")

        global_weights = list(initial_weights)
        for r in range(1, self.rounds + 1):
            with self.tracer.span("fl_round", round=r):
                local = [c.fit(global_weights, epochs=1) for c in clients]
                global_weights = self._fedavg([(res.weights, res.num_examples) for res in local])
                avg_loss = sum(res.loss for res in local) / max(len(local), 1)
                acc = max(0.0, min(1.0, 1.0 - avg_loss))
                self.metrics.append(RoundMetrics(round_num=r, avg_loss=avg_loss, accuracy=acc))
                self.tracer.record(
                    "fl_round_metrics",
                    round_number=r,
                    loss=avg_loss,
                    accuracy=acc,
                )
        return global_weights
