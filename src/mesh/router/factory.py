from __future__ import annotations

from .cgr import CgrRouter
from .epidemic import EpidemicRouter
from .prophet import ProphetRouter
from .spray_wait import SprayWaitRouter


class RouterFactory:
    @staticmethod
    def create(strategy: str) -> object:
        normalized = strategy.lower()
        if normalized == "epidemic":
            return EpidemicRouter()
        if normalized == "prophet":
            return ProphetRouter()
        if normalized == "spray_wait":
            return SprayWaitRouter()
        if normalized == "cgr":
            return CgrRouter()
        raise ValueError(f"unsupported strategy: {strategy}")
