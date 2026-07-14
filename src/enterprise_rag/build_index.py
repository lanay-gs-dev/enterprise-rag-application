"""
build_index.py — The ingestion pipeline, end to end. Run: python -m src.build_index

WHY A SEPARATE SCRIPT: indexing is a BATCH job (run when docs change);
answering is INTERACTIVE (run per question). Separating them means the
Streamlit app starts fast and never re-embeds anything. In AWS terms:
this script is the Lambda-triggered-by-S3-upload; app.py is the always-on
service. Same separation, local edition.
"""

from src.chunking import chunk_all
from src.embeddings import embed_texts
from src.ingestion import load_documents
from src.vectorstore import build_index


def main() -> None:
    print("1/4 Loading documents...")
    docs = load_documents()
    print(f"    {len(docs)} documents loaded")

    print("2/4 Chunking (section-aware)...")
    chunks = chunk_all(docs)
    print(f"    {len(chunks)} chunks created")

    print("3/4 Embedding locally (first run downloads the model, ~80MB)...")
    embeddings = embed_texts([c.text for c in chunks])

    print("4/4 Writing vector index...")
    count = build_index(chunks, embeddings)
    print(f"Done. Index contains {count} chunks. Run: streamlit run app.py")


if __name__ == "__main__":
    main()
