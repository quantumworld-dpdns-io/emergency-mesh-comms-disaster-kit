from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass(slots=True)
class RotationSchedule:
    interval_days: int = 7
    last_rotated_at: datetime = datetime.now(UTC)

    def due(self, now: datetime | None = None) -> bool:
        current = now or datetime.now(UTC)
        return current >= self.last_rotated_at + timedelta(days=self.interval_days)

    def mark_rotated(self, when: datetime | None = None) -> None:
        self.last_rotated_at = when or datetime.now(UTC)
