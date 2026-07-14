"""
Embedding utilities for turning text into vectors.

This module uses a local sentence-transformers model so we can embed document
chunks and user questions without sending source text to an external API.

Local embeddings are useful for development because they reduce cost, preserve
privacy, and keep retrieval experiments repeatable. In production, the embedding
model should be evaluated against retrieval quality, latency, and cost before
being finalized.
"""

from functools import lru_cache

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache
def get_model():
    """Load the embedding model once per Python process."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Turn multiple text strings into embedding vectors."""
    model = get_model()
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return embeddings.tolist()


def embed_query(question: str) -> list[float]:
    """Turn one user question into one embedding vector."""
    return embed_texts([question])[0]
