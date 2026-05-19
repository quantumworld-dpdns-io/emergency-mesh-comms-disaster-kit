from src.mesh.protocol.bundle import Bundle, EID, PrimaryBlock
from src.mesh.protocol.fragmentation import ReassemblyBuffer, fragment_payload
from src.mesh.protocol.serializer import decode_bundle, encode_bundle


def test_bundle_cbor_round_trip() -> None:
    b = Bundle(primary=PrimaryBlock(source=EID(value="dtn://a"), destination=EID(value="dtn://b")), payload=b"abc")
    out = decode_bundle(encode_bundle(b))
    assert out.bundle_id == b.bundle_id
    assert out.payload == b.payload


def test_fragment_reassembly() -> None:
    payload = b"x" * 100
    frags = fragment_payload("id1", payload, 16)
    buf = ReassemblyBuffer()
    res = None
    for f in frags:
        res = buf.add(f)
    assert res == payload
