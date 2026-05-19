import pytest

from src.ai.agents.coordinator_graph import CoordinatorGraph
from src.ai.models.ollama_client import OllamaClient


class _FailOllama(OllamaClient):
    def __init__(self) -> None:
        super().__init__("http://localhost:11434")

    async def generate(self, model: str, prompt: str) -> str:
        raise RuntimeError("offline")


@pytest.mark.asyncio
async def test_graph_fallback_path() -> None:
    g = CoordinatorGraph(_FailOllama())
    out = await g.run({"topology_size": 1, "queue_depth": 0, "latest_incident": "medical injury"})
    assert out["routing_strategy"] in {"epidemic", "prophet", "spray_wait"}
