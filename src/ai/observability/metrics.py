from __future__ import annotations


class AIMetrics:
    def __init__(self) -> None:
        self.ai_decisions_total = 0
        self.ai_errors_total = 0

    def inc_decisions(self) -> None:
        self.ai_decisions_total += 1

    def inc_errors(self) -> None:
        self.ai_errors_total += 1

    def snapshot(self) -> dict[str, int]:
        return {
            "ai_decisions_total": self.ai_decisions_total,
            "ai_errors_total": self.ai_errors_total,
        }
