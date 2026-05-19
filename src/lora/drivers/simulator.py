from __future__ import annotations

import random
from collections import deque

from .base import LoRaDriver


class SimulatedLoRaDriver(LoRaDriver):
    def __init__(self, noise_floor_dbm: float = -120.0, loss_rate: float = 0.0) -> None:
        self.noise_floor_dbm = noise_floor_dbm
        self.loss_rate = max(0.0, min(1.0, loss_rate))
        self._rx: deque[bytes] = deque()
        self._freq = 915.0
        self._sf = 7
        self._tx_power = 14

    def configure(self, frequency_mhz: float, sf: int, tx_power_dbm: int) -> None:
        self._freq = frequency_mhz
        self._sf = sf
        self._tx_power = tx_power_dbm

    def send(self, payload: bytes) -> None:
        if random.random() < self.loss_rate:
            return
        self._rx.append(payload)

    def receive(self, timeout_seconds: float = 0.1) -> bytes | None:
        if self._rx:
            return self._rx.popleft()
        return None

    def read_rssi(self) -> float:
        return self.noise_floor_dbm + random.uniform(10, 40)

    def read_snr(self) -> float:
        return random.uniform(-10, 12)
