from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AdrDecision:
    spreading_factor: int
    tx_power_dbm: int


class AdaptiveDataRateController:
    def decide(self, snr_history: list[float]) -> AdrDecision:
        if not snr_history:
            return AdrDecision(spreading_factor=10, tx_power_dbm=17)
        avg = sum(snr_history) / len(snr_history)
        if avg > 8:
            return AdrDecision(spreading_factor=7, tx_power_dbm=10)
        if avg > 3:
            return AdrDecision(spreading_factor=9, tx_power_dbm=14)
        return AdrDecision(spreading_factor=11, tx_power_dbm=20)
