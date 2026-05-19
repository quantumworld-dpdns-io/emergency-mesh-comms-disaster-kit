from __future__ import annotations

from collections import OrderedDict

from .ollama_client import OllamaClient


class ModelRegistry:
    def __init__(self, ollama: OllamaClient, max_models_cached: int = 4) -> None:
        self.ollama = ollama
        self.max_models_cached = max_models_cached
        self._loaded: OrderedDict[str, bool] = OrderedDict()

    async def ensure_model(self, model: str) -> None:
        # Touch model by trivial generation. Pull behavior left to Ollama daemon config.
        if model in self._loaded:
            self._loaded.move_to_end(model)
            return
        try:
            await self.ollama.generate(model=model, prompt="ping")
        except Exception:
            # keep registry resilient in offline mode
            pass
        self._loaded[model] = True
        while len(self._loaded) > self.max_models_cached:
            self._loaded.popitem(last=False)

    def loaded_models(self) -> list[str]:
        return list(self._loaded.keys())
