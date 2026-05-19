from __future__ import annotations

import pytest

from src.security.audit.classifier import classify_event
from src.security.audit.integrity import AuditIntegrityChain
from src.security.audit.tetragon import TetragonEvent


@pytest.mark.integration
def test_classify_unknown_eid() -> None:
    event = TetragonEvent(
        event_type="NetworkEvent",
        process="mesh-router",
        source_ip="10.0.0.2",
        dest_ip="10.0.0.3",
        metadata={"eid_known": False},
        ts=__import__("datetime").datetime.now(__import__("datetime").UTC),
    )
    out = classify_event(event)
    assert out.category == "unknown_eid"


@pytest.mark.integration
def test_integrity_chain_advances_hash() -> None:
    chain = AuditIntegrityChain()
    r1 = chain.append({"a": 1})
    r2 = chain.append({"a": 2})
    assert r1.hash != r2.hash
    assert r2.prev_hash == r1.hash
