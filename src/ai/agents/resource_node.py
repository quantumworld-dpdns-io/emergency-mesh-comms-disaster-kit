from __future__ import annotations

from .coordinator_state import CoordinatorState


def resource_allocation_node(state: CoordinatorState) -> CoordinatorState:
    label = str(state.get("triage_label", "comms"))
    if label == "medical":
        plan = "Reserve 60% bandwidth for medical priority bundles"
    elif label == "rescue":
        plan = "Reserve 50% bandwidth for rescue coordination"
    elif label == "supply":
        plan = "Reserve 40% bandwidth for logistics traffic"
    else:
        plan = "Balanced allocation across normal comms"
    state["resource_plan"] = plan
    return state
