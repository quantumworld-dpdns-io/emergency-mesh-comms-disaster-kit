from __future__ import annotations

import struct
import zlib

from .types import LoRaPacket, PacketFlags, PacketType

_HEADER_FORMAT = ">BBBHIIH"
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)


class PacketDecodeError(ValueError):
    pass


def decode_packet(raw: bytes) -> LoRaPacket:
    if len(raw) < _HEADER_SIZE + 4:
        raise PacketDecodeError("packet too short")

    body, crc_raw = raw[:-4], raw[-4:]
    expected_crc = struct.unpack(">I", crc_raw)[0]
    actual_crc = zlib.crc32(body) & 0xFFFFFFFF
    if expected_crc != actual_crc:
        raise PacketDecodeError("CRC mismatch")

    version, ptype, flags, seq, src, dst, payload_len = struct.unpack(_HEADER_FORMAT, body[:_HEADER_SIZE])
    payload = body[_HEADER_SIZE:]
    if len(payload) != payload_len:
        raise PacketDecodeError("payload length mismatch")

    return LoRaPacket(
        version=version,
        packet_type=PacketType(ptype),
        flags=PacketFlags(flags),
        sequence=seq,
        source=src,
        destination=dst,
        payload=payload,
    )
