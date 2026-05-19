from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ProphetConfig:
    p_init: float = 0.75
    beta: float = 0.25
    gamma: float = 0.98


class ProphetRouter:
    def __init__(self, config: ProphetConfig | None = None) -> None:
        self.config = config or ProphetConfig()
        self.predictability: dict[tuple[str, str], float] = {}

    def on_encounter(self, a: str, b: str) -> None:
        key = (a, b)
        p_old = self.predictability.get(key, 0.0)
        self.predictability[key] = p_old + (1 - p_old) * self.config.p_init

    def age(self) -> None:
        for key, value in list(self.predictability.items()):
            self.predictability[key] = value * self.config.gamma

    def transitive_update(self, a: str, b: str, c: str) -> None:
        pab = self.predictability.get((a, b), 0.0)
        pbc = self.predictability.get((b, c), 0.0)
        pac = self.predictability.get((a, c), 0.0)
        self.predictability[(a, c)] = max(pac, pab * pbc * self.config.beta)
