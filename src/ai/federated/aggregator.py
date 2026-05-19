from __future__ import annotations


class ModelAggregator:
    def __init__(self) -> None:
        self.latest_weights: list[float] | None = None
        self.notifications: list[dict[str, object]] = []

    def publish(self, weights: list[float], version: str) -> None:
        self.latest_weights = list(weights)
        self.notifications.append({"event": "model_updated", "version": version})
