from __future__ import annotations

from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.chunking import chunk_document
from enterprise_rag.embeddings import embed_texts
from enterprise_rag.generation import answer_from_evidence
from enterprise_rag.ingestion import load_markdown_documents
from enterprise_rag.retrieval import retrieve
from enterprise_rag.vectorstore import build_index


def main() -> None:
    question = "Is multi-factor authentication required?"
    documents = load_markdown_documents(ROOT / "data" / "sample")
    chunks = [chunk for document in documents for chunk in chunk_document(document)]
    embeddings = embed_texts([chunk.text for chunk in chunks])

    with tempfile.TemporaryDirectory() as temp_dir:
        build_index(chunks, embeddings, persist_dir=temp_dir)
        retrieved = retrieve(question, k=2, persist_dir=temp_dir)
        answer = answer_from_evidence(question, retrieved)

    print(f"Question: {question}")
    print(f"Refused: {answer.refused}")
    print(f"Answer: {answer.text}")
    print("Citations:")
    for citation in answer.citations:
        print(f"- {citation}")


if __name__ == "__main__":
    main()
