from __future__ import annotations

from dataclasses import dataclass

from .tasks.prioritize_task import prioritize_messages
from .tasks.resource_task import optimize_bandwidth
from .tasks.sitrep_task import generate_sitrep


@dataclass(slots=True)
class DisasterCrewResult:
    prioritized: list[dict[str, object]]
    allocation: dict[str, int]
    sitrep: str


class DisasterResponseCrew:
    def run(self, messages: list[dict[str, object]], state: dict[str, object]) -> DisasterCrewResult:
        prioritized = prioritize_messages(messages)
        triage = str(state.get("triage_label", "comms"))
        emergency_share = 0.6 if triage in {"medical", "rescue"} else 0.4
        allocation = optimize_bandwidth(total_kbps=1000, emergency_share=emergency_share)
        sitrep = generate_sitrep(state)
        return DisasterCrewResult(prioritized=prioritized, allocation=allocation, sitrep=sitrep)
