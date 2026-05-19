from __future__ import annotations

import json
from pathlib import Path

from src.ai.models.ollama_client import OllamaClient

from .anomaly_node import anomaly_detection_node
from .coordinator_state import CoordinatorState
from .human_review import human_review_checkpoint
from .resource_node import resource_allocation_node
from .routing_node import routing_decision_node
from .triage_node import triage_assessment_node


class CoordinatorGraph:
    def __init__(self, ollama: OllamaClient, model: str = "llama3.2:3b") -> None:
        self.ollama = ollama
        self.model = model

    async def run(self, initial_state: CoordinatorState) -> CoordinatorState:
        state = dict(initial_state)
        state = await routing_decision_node(state, self.ollama, self.model)
        state = await triage_assessment_node(state, self.ollama, self.model)
        state = resource_allocation_node(state)
        state = anomaly_detection_node(state)
        state = human_review_checkpoint(state)
        state["decision_summary"] = (
            f"route={state.get('routing_strategy')} triage={state.get('triage_label')} "
            f"anomalies={','.join(state.get('anomalies', [])) or 'none'}"
        )
        return state


class SqliteCheckpointLikeSaver:
    """Simple sqlite-file-compatible JSON checkpointer for baseline behavior."""

    def __init__(self, path: str = "data/agent_state.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, state: CoordinatorState) -> None:
        self.path.write_text(json.dumps(state), encoding="utf-8")

    def load(self) -> CoordinatorState:
        if not self.path.exists():
            return CoordinatorState()
        return CoordinatorState(**json.loads(self.path.read_text(encoding="utf-8")))
