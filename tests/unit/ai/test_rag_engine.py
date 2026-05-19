from __future__ import annotations

import pytest

from src.ai.knowledge.qdrant_client import EmergencyQdrantClient, KnowledgeItem
from src.ai.knowledge.rag_engine import RAGEngine
from src.ai.models.ollama_client import OllamaClient


class _FakeOllama(OllamaClient):
    def __init__(self) -> None:
        super().__init__("http://localhost:11434")

    async def embed(self, model: str, text: str) -> list[float]:
        return [float(len(text) % 7), 1.0, 0.5]

    async def generate(self, model: str, prompt: str) -> str:
        return "mock-answer"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_rag_query_returns_answer_and_context() -> None:
    qdrant = EmergencyQdrantClient()
    qdrant.upsert(KnowledgeItem(doc_id="d1", text="first aid pressure", embedding=[1.0, 1.0, 0.2], metadata={"source": "first_aid.md"}))
    qdrant.upsert(KnowledgeItem(doc_id="d2", text="radio procedure", embedding=[0.1, 0.2, 0.3], metadata={"source": "ics_radio.md"}))

    rag = RAGEngine(qdrant=qdrant, ollama=_FakeOllama(), model="x", embed_model="y")
    out = await rag.query("how to stop bleeding")
    assert out.answer == "mock-answer"
    assert out.context_docs
