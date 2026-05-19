from __future__ import annotations


def prioritize_messages(messages: list[dict[str, object]]) -> list[dict[str, object]]:
    weight = {"emergency": 3, "medical": 2, "general": 1}
    return sorted(messages, key=lambda m: weight.get(str(m.get("priority", "general")), 1), reverse=True)
