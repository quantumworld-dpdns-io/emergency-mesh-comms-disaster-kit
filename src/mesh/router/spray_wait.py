from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SprayTokenState:
    bundle_id: str
    remaining_tokens: int


class SprayWaitRouter:
    def __init__(self, initial_tokens: int = 8) -> None:
        if initial_tokens < 1:
            raise ValueError("initial_tokens must be >= 1")
        self.initial_tokens = initial_tokens
        self.tokens: dict[str, SprayTokenState] = {}

    def init_bundle(self, bundle_id: str) -> None:
        self.tokens[bundle_id] = SprayTokenState(bundle_id=bundle_id, remaining_tokens=self.initial_tokens)

    def can_spray(self, bundle_id: str) -> bool:
        state = self.tokens.get(bundle_id)
        return bool(state and state.remaining_tokens > 1)

    def spray(self, bundle_id: str) -> int:
        state = self.tokens[bundle_id]
        given = state.remaining_tokens // 2
        state.remaining_tokens -= given
        return max(given, 1)
