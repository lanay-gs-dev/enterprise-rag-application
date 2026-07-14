from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag import ChunkingConfig, chunk_document, load_markdown_documents


def main() -> None:
    documents = load_markdown_documents(ROOT / "data" / "sample")
    chunk_count = 0

    for document in documents:
        chunks = chunk_document(document, ChunkingConfig(max_chars=320, overlap_chars=60))
        chunk_count += len(chunks)
        print(f"{document.source_id}: {len(chunks)} chunks from {document.title}")
        for chunk in chunks:
            print(f"  - {chunk.chunk_id}: {len(chunk.text)} chars")

    print(f"\nLoaded {len(documents)} documents and created {chunk_count} chunks.")


if __name__ == "__main__":
    main()
