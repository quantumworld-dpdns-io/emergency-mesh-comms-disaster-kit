from __future__ import annotations

from .coordinator_state import CoordinatorState


def anomaly_detection_node(state: CoordinatorState) -> CoordinatorState:
    anomalies: list[str] = []
    if int(state.get("queue_depth", 0)) > 500:
        anomalies.append("queue_backpressure")
    if int(state.get("topology_size", 0)) <= 1:
        anomalies.append("network_partition")
    state["anomalies"] = anomalies
    return state
