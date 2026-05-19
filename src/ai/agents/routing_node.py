from __future__ import annotations

import json
from pathlib import Path

from src.ai.models.fallback import fallback_route_decision
from src.ai.models.ollama_client import OllamaClient

from .coordinator_state import CoordinatorState


async def routing_decision_node(state: CoordinatorState, ollama: OllamaClient, model: str) -> CoordinatorState:
    model_path = state.get("routing_model_path")
    if isinstance(model_path, str) and model_path:
        p = Path(model_path)
        if p.exists():
            try:
                payload = json.loads(p.read_text(encoding="utf-8"))
                weights = [float(v) for v in payload.get("weights", [])]
                if len(weights) >= 3:
                    # Basic model-guided heuristic from federated weights.
                    lqi_score = weights[0]
                    queue_penalty = weights[1]
                    topo_score = weights[2]
                    if queue_penalty < -0.15:
                        state["routing_strategy"] = "spray_wait"
                    elif lqi_score + topo_score > 0.4:
                        state["routing_strategy"] = "prophet"
                    else:
                        state["routing_strategy"] = "epidemic"
                    return state
            except Exception:
                pass

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
