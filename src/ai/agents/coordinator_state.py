from __future__ import annotations

from typing import TypedDict


class CoordinatorState(TypedDict, total=False):
    node_id: str
    topology_size: int
    queue_depth: int
    latest_incident: str
    routing_strategy: str
    triage_label: str
    resource_plan: str
    anomalies: list[str]
    require_human_review: bool
    decision_summary: str
