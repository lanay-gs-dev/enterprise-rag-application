"""
vectorstore.py — Store vectors, find neighbors. Chroma edition.

WHY CHROMA (vs FAISS, vs pgvector, vs OpenSearch — know this table):
  • Chroma  — embedded DB, persists to disk, stores metadata alongside
              vectors, zero servers. Perfect for local apps + demos. ← us
  • FAISS   — a raw index LIBRARY (Meta). Blazing fast, but no metadata
              storage and no persistence layer — you build those yourself.
  • pgvector— vectors inside Postgres. Right answer when you already run
              Postgres and want SQL + vectors together.
  • OpenSearch/managed — the AWS-native path; where this design maps in
              production (see docs/aws_architecture_mapping.md).

The skill being taught here: we wrap Chroma behind our OWN two functions
(build_index / query_index). If we ever swap Chroma for OpenSearch, only
THIS FILE changes. Wrapping third-party libraries behind your own thin
interface is one of the highest-value habits in engineering.
"""

import chromadb

from src.config import get_settings
from src.schemas import Chunk, DocumentMetadata, RetrievedChunk

COLLECTION = "ironwood_docs"


def _client():
    return chromadb.PersistentClient(path=get_settings().chroma_dir)


def build_index(chunks: list[Chunk], embeddings: list[list[float]]) -> int:
    """(Re)build the collection from scratch.

    WHY DELETE-THEN-CREATE: for a small corpus, full rebuilds are simpler
    and safer than incremental updates — no stale chunks from renamed
    sections. Incremental indexing is a real production concern; it's in
    docs/future_ladder.md, not in v1. Scope control in action.

    GOTCHA: Chroma metadata values must be primitives (str/int/float/bool),
    so we flatten our Pydantic model with model_dump() — every field is
    already a string by design. That wasn't luck; schemas.py chose str
    types partly for this reason. Design decisions ripple.
    """
    client = _client()
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass  # first run — nothing to delete

    col = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    col.upsert(
        ids=[c.chunk_id for c in chunks],
        embeddings=embeddings,
        documents=[c.text for c in chunks],
        metadatas=[
            {**c.metadata.model_dump(), "section": c.section, "doc_id": c.doc_id}
            for c in chunks
        ],
    )
    return col.count()


def query_index(query_embedding: list[float], k: int) -> list[RetrievedChunk]:
    """Nearest-neighbor search → our RetrievedChunk schema.

    SCORE MATH: Chroma returns cosine DISTANCE (0 = identical). We convert
    to similarity = 1 - distance so "bigger = better" everywhere in the
    app. Mixed score directions cause real bugs — pick one convention.
    """
    col = _client().get_collection(COLLECTION)
    res = col.query(query_embeddings=[query_embedding], n_results=k)

    retrieved: list[RetrievedChunk] = []
    for rank, (cid, text, meta, dist) in enumerate(
        zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]),
        start=1,
    ):
        section = meta.pop("section")
        doc_id = meta.pop("doc_id")
        chunk = Chunk(
            chunk_id=cid,
            doc_id=doc_id,
            section=section,
            text=text,
            metadata=DocumentMetadata(**meta),
        )
        retrieved.append(RetrievedChunk(chunk=chunk, score=1 - dist, rank=rank))
    return retrieved
