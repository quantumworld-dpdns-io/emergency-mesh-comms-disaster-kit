from __future__ import annotations


class LoRaLibrary:
    def set_packet_loss_rate(self, rate: float) -> float:
        return max(0.0, min(rate, 1.0))
