from __future__ import annotations


def knowledge_markdown(answer: str, context_docs: list[str]) -> str:
    docs = ", ".join(context_docs) if context_docs else "none"
    return f"# Knowledge Base Response\n\nSources: {docs}\n\n{answer}\n"
