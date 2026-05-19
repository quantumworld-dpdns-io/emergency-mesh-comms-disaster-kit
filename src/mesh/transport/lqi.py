from __future__ import annotations


def compute_lqi(rssi: float, snr: float, per: float) -> float:
    rssi_score = max(0.0, min(100.0, 100.0 - abs(rssi + 30.0)))
    snr_score = max(0.0, min(100.0, (snr + 20.0) * 2.5))
    per_score = max(0.0, min(100.0, (1.0 - per) * 100.0))
    return max(0.0, min(100.0, (0.4 * rssi_score) + (0.3 * snr_score) + (0.3 * per_score)))
