from __future__ import annotations

from dataclasses import dataclass

from .task import RoutingModelTask, RoutingSample


@dataclass(slots=True)
class FlowerClientResult:
    weights: list[float]
    loss: float
    num_examples: int


class MeshFlowerClient:
    def __init__(self, node_id: str, task: RoutingModelTask, local_samples: list[RoutingSample]) -> None:
        self.node_id = node_id
        self.task = task
        self.local_samples = local_samples

    def get_parameters(self) -> list[float]:
        return list(self.task.weights)

    def fit(self, global_weights: list[float], epochs: int = 1) -> FlowerClientResult:
        self.task.weights = list(global_weights)
        loss = 0.0
        for _ in range(epochs):
            loss = self.task.train_step(self.local_samples)
        return FlowerClientResult(weights=self.get_parameters(), loss=loss, num_examples=len(self.local_samples))
