from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FhssController:
    channels_mhz: list[float]
    beacon_seed: int = 0

    def __post_init__(self) -> None:
        if not self.channels_mhz:
            raise ValueError("channels_mhz must not be empty")

    def channel_for_slot(self, slot: int) -> float:
        idx = (slot + self.beacon_seed) % len(self.channels_mhz)
        return self.channels_mhz[idx]
