from __future__ import annotations

from pathlib import Path

from src.ai.models.ollama_client import OllamaClient

from .qdrant_client import EmergencyQdrantClient, KnowledgeItem


def _chunk_text(text: str, chunk_chars: int = 2000) -> list[str]:
    text = text.strip()
    if not text:
        return []
    return [text[i : i + chunk_chars] for i in range(0, len(text), chunk_chars)]


class KnowledgeIngestionPipeline:
    def __init__(self, qdrant: EmergencyQdrantClient, ollama: OllamaClient, embed_model: str) -> None:
        self.qdrant = qdrant
        self.ollama = ollama
        self.embed_model = embed_model

    async def ingest_markdown_file(self, path: str) -> int:
        source = Path(path)
        text = source.read_text(encoding="utf-8")
        chunks = _chunk_text(text)
        inserted = 0
        for idx, chunk in enumerate(chunks):
            try:
                emb = await self.ollama.embed(self.embed_model, chunk)
            except Exception:
                emb = [float((ord(c) % 13) / 13.0) for c in chunk[:64]] or [0.0]
            item = KnowledgeItem(
                doc_id=f"{source.stem}-{idx}",
                text=chunk,
                embedding=emb,
                metadata={"source": source.name, "chunk": idx},
            )
            self.qdrant.upsert(item)
            inserted += 1
        return inserted
