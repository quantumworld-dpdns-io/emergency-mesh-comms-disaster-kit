from __future__ import annotations

import struct
import zlib

from .types import LoRaPacket


# version(1), type(1), flags(1), seq(2), src(4), dst(4), len(2)
_HEADER_FORMAT = ">BBBHIIH"
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)


def encode_packet(packet: LoRaPacket) -> bytes:
    header = struct.pack(
        _HEADER_FORMAT,
        packet.version,
        int(packet.packet_type),
        int(packet.flags),
        packet.sequence,
        packet.source,
        packet.destination,
        len(packet.payload),
    )
    body = header + packet.payload
    crc = zlib.crc32(body) & 0xFFFFFFFF
    return body + struct.pack(">I", crc)


def max_payload_for_mtu(mtu: int) -> int:
    if mtu <= _HEADER_SIZE + 4:
        return 0
    return mtu - _HEADER_SIZE - 4
