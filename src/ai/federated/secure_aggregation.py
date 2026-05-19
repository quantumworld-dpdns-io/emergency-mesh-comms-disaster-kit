from __future__ import annotations

import random


class ShamirSecureAggregationStub:
    """Educational stub for splitting scalar secrets into additive shares."""

    @staticmethod
    def split(secret: float, n_shares: int = 3) -> list[float]:
        if n_shares < 2:
            raise ValueError("n_shares must be >= 2")
        shares = [random.uniform(-1, 1) for _ in range(n_shares - 1)]
        shares.append(secret - sum(shares))
        return shares

    @staticmethod
    def combine(shares: list[float]) -> float:
        return sum(shares)
