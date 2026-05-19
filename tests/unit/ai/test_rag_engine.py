from __future__ import annotations

from src.ai.agents.tasks.prioritize_task import prioritize_messages
from src.ai.models.fallback import fallback_route_decision, fallback_triage


def test_fallback_route_decision() -> None:
    assert fallback_route_decision(topology_size=1, queue_depth=0) == "epidemic"
    assert fallback_route_decision(topology_size=10, queue_depth=200) == "spray_wait"


def test_fallback_triage() -> None:
    assert fallback_triage("medical bleeding") == "medical"
    assert fallback_triage("fire rescue needed") == "rescue"


def test_prioritize_messages() -> None:
    ordered = prioritize_messages(
        [
            {"priority": "general", "id": 1},
            {"priority": "emergency", "id": 2},
            {"priority": "medical", "id": 3},
        ]
    )
    assert [m["id"] for m in ordered] == [2, 3, 1]
