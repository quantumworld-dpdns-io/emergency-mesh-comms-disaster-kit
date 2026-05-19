from __future__ import annotations

from src.ai.models.fallback import fallback_triage
from src.ai.models.ollama_client import OllamaClient

from .coordinator_state import CoordinatorState


async def triage_assessment_node(state: CoordinatorState, ollama: OllamaClient, model: str) -> CoordinatorState:
    incident = str(state.get("latest_incident", ""))
    try:
        prompt = (
            f"Classify incident into one label: medical, rescue, supply, comms. Incident: {incident}"
        )
        response = (await ollama.generate(model=model, prompt=prompt)).lower()
        for label in ("medical", "rescue", "supply", "comms"):
            if label in response:
                state["triage_label"] = label
                return state
    except Exception:
        pass

    state["triage_label"] = fallback_triage(incident)
    return state
