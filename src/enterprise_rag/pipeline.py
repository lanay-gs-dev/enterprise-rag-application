from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tempfile

from enterprise_rag.chunking import chunk_document
from enterprise_rag.embeddings import embed_texts
from enterprise_rag.generation import answer_from_evidence
from enterprise_rag.ingestion import load_markdown_documents
from enterprise_rag.models import Answer, RetrievedChunk
from enterprise_rag.retrieval import retrieve
from enterprise_rag.vectorstore import build_index


@dataclass(frozen=True)
class RagRuntime:
    persist_dir: str
    chunk_count: int


def build_sample_index(docs_path: str | Path) -> RagRuntime:
    """Load, chunk, embed, and index the sample document corpus."""
    documents = load_markdown_documents(docs_path)
    chunks = [chunk for document in documents for chunk in chunk_document(document)]
    embeddings = embed_texts([chunk.text for chunk in chunks])
    persist_dir = tempfile.mkdtemp(prefix="enterprise-rag-demo-")
    chunk_count = build_index(chunks, embeddings, persist_dir=persist_dir)
    return RagRuntime(persist_dir=persist_dir, chunk_count=chunk_count)


def answer_question(
    question: str,
    runtime: RagRuntime,
    k: int = 2,
) -> tuple[Answer, list[RetrievedChunk]]:
    """Retrieve evidence and return the answer contract plus retrieved chunks."""
    retrieved = retrieve(question, k=k, persist_dir=runtime.persist_dir)
    answer = answer_from_evidence(question, retrieved)
    return answer, retrieved
