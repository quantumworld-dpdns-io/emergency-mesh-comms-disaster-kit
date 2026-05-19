from __future__ import annotations


def emergency_triage_prompt(mesh_context: str, incident_text: str) -> str:
    return (
        "You are an emergency triage assistant for a DTN mesh network. "
        "Classify severity, propose immediate actions, and identify message priority.\n\n"
        f"Mesh context:\n{mesh_context}\n\n"
        f"Incident:\n{incident_text}\n"
    )
