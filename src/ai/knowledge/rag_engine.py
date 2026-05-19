from __future__ import annotations

from dataclasses import dataclass

from src.ai.models.ollama_client import OllamaClient

from .qdrant_client import EmergencyQdrantClient


@dataclass(slots=True)
class RAGResult:
    answer: str
    context_docs: list[str]


class RAGEngine:
    def __init__(self, qdrant: EmergencyQdrantClient, ollama: OllamaClient, model: str, embed_model: str) -> None:
        self.qdrant = qdrant
        self.ollama = ollama
        self.model = model
        self.embed_model = embed_model

    async def query(self, question: str, limit: int = 3) -> RAGResult:
        try:
            qvec = await self.ollama.embed(self.embed_model, question)
        except Exception:
            qvec = [float((ord(c) % 13) / 13.0) for c in question[:64]] or [0.0]

        hits = self.qdrant.search(qvec, limit=limit)
        context = "\n\n".join(h.text for h in hits)

        prompt = (
            "Answer using the context below. If unsure, say unknown.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        try:
            answer = await self.ollama.generate(self.model, prompt)
        except Exception:
            answer = f"Offline fallback answer based on {len(hits)} context chunks."

        return RAGResult(answer=answer, context_docs=[h.metadata.get("source", h.doc_id) for h in hits])
