from __future__ import annotations

from src.ai.models.fallback import fallback_route_decision
from src.ai.models.ollama_client import OllamaClient

from .coordinator_state import CoordinatorState


async def routing_decision_node(state: CoordinatorState, ollama: OllamaClient, model: str) -> CoordinatorState:
    try:
        prompt = (
            f"Topology size={state.get('topology_size', 0)}, queue depth={state.get('queue_depth', 0)}. "
            "Choose one strategy: epidemic, prophet, spray_wait."
        )
        response = (await ollama.generate(model=model, prompt=prompt)).lower()
        for candidate in ("epidemic", "prophet", "spray_wait"):
            if candidate in response:
                state["routing_strategy"] = candidate
                return state
    except Exception:
        pass

    state["routing_strategy"] = fallback_route_decision(
        topology_size=int(state.get("topology_size", 0)),
        queue_depth=int(state.get("queue_depth", 0)),
    )
    return state
