from __future__ import annotations


def generate_sitrep(state: dict[str, object]) -> str:
    return (
        "SITREP: "
        f"routing={state.get('routing_strategy', 'unknown')}; "
        f"triage={state.get('triage_label', 'unknown')}; "
        f"queue_depth={state.get('queue_depth', 0)}; "
        f"topology_size={state.get('topology_size', 0)}; "
        f"anomalies={state.get('anomalies', [])}."
    )
