"""
Vector store utilities for saving and searching embedded chunks.

This module wraps Chroma behind a small local interface. Keeping Chroma usage
inside this file makes the rest of the RAG pipeline easier to change later if
we move from local development to a managed vector store such as OpenSearch.
"""

from __future__ import annotations

from pathlib import Path

import chromadb

from enterprise_rag.models import DocumentChunk, RetrievedChunk

DEFAULT_COLLECTION_NAME = "enterprise_rag_chunks"
DEFAULT_PERSIST_DIR = "chroma_db"


def get_client(persist_dir: str | Path = DEFAULT_PERSIST_DIR):
    """Create a persistent Chroma client."""
    return chromadb.PersistentClient(path=str(persist_dir))


def build_index(
    chunks: list[DocumentChunk],
    embeddings: list[list[float]],
    collection_name: str = DEFAULT_COLLECTION_NAME,
    persist_dir: str | Path = DEFAULT_PERSIST_DIR,
) -> int:
    """Rebuild a Chroma collection from chunks and matching embeddings."""
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length")

    client = get_client(persist_dir)
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(collection_name, metadata={"hnsw:space": "cosine"})
    collection.add(
        ids=[chunk.chunk_id for chunk in chunks],
        embeddings=embeddings,
        documents=[chunk.text for chunk in chunks],
        metadatas=[_metadata_for_chroma(chunk) for chunk in chunks],
    )
    return collection.count()


def query_index(
    query_embedding: list[float],
    k: int = 3,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    persist_dir: str | Path = DEFAULT_PERSIST_DIR,
) -> list[RetrievedChunk]:
    """Return the nearest chunks for a query embedding."""
    collection = get_client(persist_dir).get_collection(collection_name)
    results = collection.query(query_embeddings=[query_embedding], n_results=k)

    retrieved: list[RetrievedChunk] = []
    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for rank, (chunk_id, text, metadata, distance) in enumerate(
        zip(ids, documents, metadatas, distances),
        start=1,
    ):
        chunk_metadata = {
            key.removeprefix("metadata_"): value
            for key, value in metadata.items()
            if key.startswith("metadata_")
        }
        retrieved.append(
            RetrievedChunk(
                chunk_id=chunk_id,
                source_id=str(metadata["source_id"]),
                text=text,
                metadata=chunk_metadata,
                start_char=int(metadata["start_char"]),
                end_char=int(metadata["end_char"]),
                score=1 - float(distance),
                rank=rank,
            )
        )

    return retrieved


def _metadata_for_chroma(chunk: DocumentChunk) -> dict[str, str | int | float | bool]:
    chroma_metadata: dict[str, str | int | float | bool] = {
        "source_id": chunk.source_id,
        "start_char": chunk.start_char,
        "end_char": chunk.end_char,
    }
    for key, value in chunk.metadata.items():
        chroma_metadata[f"metadata_{key}"] = value
    return chroma_metadata
