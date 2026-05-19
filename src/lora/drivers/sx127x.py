from __future__ import annotations

from .simulator import SimulatedLoRaDriver


class SX127xDriver(SimulatedLoRaDriver):
    """Baseline-compatible SX127x driver surface.

    Real register-level SPI access is deferred to hardware integration hardening.
    """

    pass
