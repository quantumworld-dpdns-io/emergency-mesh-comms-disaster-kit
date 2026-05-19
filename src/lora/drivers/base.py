from __future__ import annotations

from abc import ABC, abstractmethod


class LoRaDriver(ABC):
    @abstractmethod
    def configure(self, frequency_mhz: float, sf: int, tx_power_dbm: int) -> None: ...

    @abstractmethod
    def send(self, payload: bytes) -> None: ...

    @abstractmethod
    def receive(self, timeout_seconds: float = 0.1) -> bytes | None: ...

    @abstractmethod
    def read_rssi(self) -> float: ...

    @abstractmethod
    def read_snr(self) -> float: ...
