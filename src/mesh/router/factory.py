from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Router:
    strategy: str


class RouterFactory:
    @staticmethod
    def create(strategy: str) -> Router:
        allowed = {"epidemic", "prophet", "spray_wait", "cgr"}
        if strategy not in allowed:
            raise ValueError(f"unsupported strategy: {strategy}")
        return Router(strategy=strategy)
