from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class KnowledgeItem:
    doc_id: str
    text: str
    embedding: list[float]
    metadata: dict[str, object]


class EmergencyQdrantClient:
    """In-memory fallback client with Qdrant-like surface for offline dev."""

    def __init__(self, collection_name: str = "emergency_knowledge") -> None:
        self.collection_name = collection_name
        self._items: dict[str, KnowledgeItem] = {}

    def upsert(self, item: KnowledgeItem) -> None:
        self._items[item.doc_id] = item

    def search(self, query_embedding: list[float], limit: int = 5) -> list[KnowledgeItem]:
        # Dot-product ranking baseline
        def score(it: KnowledgeItem) -> float:
            n = min(len(query_embedding), len(it.embedding))
            return sum(query_embedding[i] * it.embedding[i] for i in range(n))

        return sorted(self._items.values(), key=score, reverse=True)[:limit]

    def export_snapshot(self) -> dict[str, object]:
        return {
            "collection": self.collection_name,
            "items": [
                {
                    "doc_id": i.doc_id,
                    "text": i.text,
                    "embedding": i.embedding,
                    "metadata": i.metadata,
                }
                for i in self._items.values()
            ],
        }

    def restore_snapshot(self, snapshot: dict[str, object]) -> None:
        self.collection_name = str(snapshot.get("collection", self.collection_name))
        self._items.clear()
        for obj in snapshot.get("items", []):
            self.upsert(
                KnowledgeItem(
                    doc_id=str(obj["doc_id"]),
                    text=str(obj["text"]),
                    embedding=[float(x) for x in obj.get("embedding", [])],
                    metadata=dict(obj.get("metadata", {})),
                )
            )
