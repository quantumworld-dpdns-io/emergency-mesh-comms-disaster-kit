from __future__ import annotations

import random
import time

from .base import LoRaDriver


class CsmaCaController:
    def __init__(self, rssi_busy_threshold_dbm: float = -95.0, max_backoff_seconds: float = 0.25) -> None:
        self.rssi_busy_threshold_dbm = rssi_busy_threshold_dbm
        self.max_backoff_seconds = max_backoff_seconds

    def wait_for_clear_channel(self, driver: LoRaDriver, attempts: int = 5) -> bool:
        for _ in range(attempts):
            if driver.read_rssi() < self.rssi_busy_threshold_dbm:
                return True
            time.sleep(random.uniform(0, self.max_backoff_seconds))
        return False
