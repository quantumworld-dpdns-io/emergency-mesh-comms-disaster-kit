from __future__ import annotations

from .coordinator_state import CoordinatorState


def human_review_checkpoint(state: CoordinatorState) -> CoordinatorState:
    high_risk = "network_partition" in state.get("anomalies", [])
    state["require_human_review"] = bool(high_risk)
    return state
