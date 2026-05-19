from __future__ import annotations

import os

from .base import LoRaDriver
from .rfm95w import RFM95WDriver
from .sx127x import SX127xDriver


def detect_lora_driver() -> LoRaDriver:
    preferred = os.getenv("LORA_DRIVER", "sx127x").lower()
    if preferred == "rfm95w":
        return RFM95WDriver()
    return SX127xDriver()
