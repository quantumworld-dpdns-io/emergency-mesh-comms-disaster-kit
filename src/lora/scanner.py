from __future__ import annotations

from dataclasses import dataclass

from .drivers.base import LoRaDriver


@dataclass(slots=True)
class ChannelNoise:
    frequency_mhz: float
    noise_dbm: float


class LoRaChannelScanner:
    def __init__(self, driver: LoRaDriver) -> None:
        self.driver = driver

    def scan(self, channels_mhz: list[float]) -> list[ChannelNoise]:
        result: list[ChannelNoise] = []
        for ch in channels_mhz:
            self.driver.configure(ch, sf=7, tx_power_dbm=2)
            result.append(ChannelNoise(frequency_mhz=ch, noise_dbm=self.driver.read_rssi()))
        return result
