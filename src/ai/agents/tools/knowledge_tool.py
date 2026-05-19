from __future__ import annotations

from src.ai.knowledge.rag_engine import RAGEngine


async def query_knowledge(engine: RAGEngine, question: str) -> dict[str, object]:
    result = await engine.query(question)
    return {"answer": result.answer, "context_docs": result.context_docs}
