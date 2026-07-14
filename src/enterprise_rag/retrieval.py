"""
Retrieval utilities for finding evidence chunks for a user question.

Retrieval is the bridge between vector search and answer generation. It does
not answer the question itself. It returns the best available source chunks so
the next layer can cite them, inspect them, or refuse to answer when evidence is
weak.
"""

from __future__ import annotations

from enterprise_rag.embeddings import embed_query
from enterprise_rag.models import RetrievedChunk
from enterprise_rag.vectorstore import query_index


def retrieve(question: str, k: int = 3) -> list[RetrievedChunk]:
    """Embed a question and return the most relevant indexed chunks."""
    if not question.strip():
        raise ValueError("question cannot be blank")

    query_embedding = embed_query(question)
    return query_index(query_embedding, k=k)
