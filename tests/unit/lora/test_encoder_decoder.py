from __future__ import annotations

import pytest

from src.lora.packets.decoder import PacketDecodeError, decode_packet
from src.lora.packets.encoder import encode_packet
from src.lora.packets.types import LoRaPacket, PacketFlags, PacketType


def test_round_trip_encode_decode() -> None:
    pkt = LoRaPacket(
        version=1,
        packet_type=PacketType.DATA,
        flags=PacketFlags.ENCRYPTED,
        sequence=7,
        source=100,
        destination=200,
        payload=b"hello-lora",
    )
    raw = encode_packet(pkt)
    decoded = decode_packet(raw)
    assert decoded == pkt


def test_crc_error_raises() -> None:
    pkt = LoRaPacket(
        version=1,
        packet_type=PacketType.ACK,
        flags=PacketFlags.NONE,
        sequence=1,
        source=1,
        destination=2,
        payload=b"ok",
    )
    raw = bytearray(encode_packet(pkt))
    raw[-1] ^= 0xFF
    with pytest.raises(PacketDecodeError):
        decode_packet(bytes(raw))


def test_all_packet_types_encode_decode() -> None:
    for ptype in PacketType:
        pkt = LoRaPacket(
            version=1,
            packet_type=ptype,
            flags=PacketFlags.NONE,
            sequence=42,
            source=10,
            destination=20,
            payload=b"x",
        )
        assert decode_packet(encode_packet(pkt)).packet_type == ptype
