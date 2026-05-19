from src.mesh.protocol.bundle import Bundle, EID, PrimaryBlock


def test_bundle_invariant() -> None:
    b = Bundle(primary=PrimaryBlock(source=EID(value="dtn://a"), destination=EID(value="dtn://b")), payload=b"x")
    assert b.primary.ttl_seconds > 0
