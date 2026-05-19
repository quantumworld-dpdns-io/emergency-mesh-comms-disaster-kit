import pytest

from src.mesh.protocol.bundle import Bundle, EID, PrimaryBlock
from src.mesh.router.bundle_store import BundleStore


@pytest.mark.asyncio
async def test_bundle_store_enqueue_dequeue(tmp_path) -> None:
    db = str(tmp_path / "bundles.db")
    store = BundleStore(db)
    await store.initialize()
    b = Bundle(primary=PrimaryBlock(source=EID(value="dtn://a"), destination=EID(value="dtn://b")), payload=b"p")
    await store.enqueue(b, expires_at_epoch=9999999999, priority=2)
    out = await store.dequeue_next()
    assert out is not None
    assert out.bundle_id == b.bundle_id
