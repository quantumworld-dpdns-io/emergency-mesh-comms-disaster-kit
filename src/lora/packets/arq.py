from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ArqConfig:
    max_retries: int = 3
    timeout_seconds: float = 1.0


class StopAndWaitArq:
    def __init__(self, config: ArqConfig | None = None) -> None:
        self.config = config or ArqConfig()
        self._expected_ack_seq: int | None = None

    def begin_send(self, seq: int) -> None:
        self._expected_ack_seq = seq

    def on_ack(self, ack_seq: int) -> bool:
        if self._expected_ack_seq is None:
            return False
        if ack_seq != self._expected_ack_seq:
            return False
        self._expected_ack_seq = None
        return True

    def retry_schedule(self) -> list[float]:
        return [self.config.timeout_seconds * (2**i) for i in range(self.config.max_retries)]
