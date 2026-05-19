from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, IntFlag


class PacketType(IntEnum):
    DATA = 1
    ACK = 2
    BEACON = 3
    CONTROL = 4


class PacketFlags(IntFlag):
    NONE = 0
    FRAGMENTED = 1 << 0
    ENCRYPTED = 1 << 1
    RETRANSMIT = 1 << 2


@dataclass(slots=True)
class LoRaPacket:
    version: int
    packet_type: PacketType
    flags: PacketFlags
    sequence: int
    source: int
    destination: int
    payload: bytes
