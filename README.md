# Enterprise RAG Project

Retrieval-Augmented Generation system for answering questions from internal company documents with citations, refusal behavior, and explainable retrieval.

It exists to turn scattered company knowledge into trustworthy answers. The interesting part is the foundation: documents must be validated, owned, classified, chunked, and traceable before a model can answer safely.

Current implementation: Markdown ingestion, metadata validation, deterministic chunking, local embedding utilities, a local Chroma vector store wrapper, retrieval, deterministic refusal/answer response shaping, a local Streamlit demo, a FastAPI service layer, sample enterprise documents, and tests.

Run it:

```bash
python3 -m unittest discover -s tests
python3 main.py
```

## What It Does

- Loads Markdown documents with required front matter.
- Rejects incomplete or invalid metadata before retrieval prep.
- Splits documents into stable, citeable chunks with source metadata.
- Embeds text locally with `sentence-transformers`.
- Stores and queries chunk vectors through a small Chroma wrapper.
- Retrieves ranked evidence chunks for a user question.
- Refuses unsupported questions when no evidence is available.
- Provides a local Streamlit interface for asking questions against the sample corpus.
- Provides a FastAPI `/ask` endpoint for production-style integration.
- Provides a demo ingestion script and focused tests.

## Architecture

```text
Documents
  -> metadata validation
  -> chunking
  -> embeddings
  -> vector store
  -> retrieval
  -> grounded generation
  -> citation verification
  -> answer or refusal
  -> evaluation and logging
```

Implemented today: documents -> metadata validation -> chunking -> embeddings -> vector store -> retrieval -> answer/refusal shaping.

The Streamlit app is a local demo interface. AWS deployment, authentication,
managed vector search, and LLM provider routing are planned production layers.

## Local Development

Run the current test suite:

```bash
python3 -m unittest discover -s tests
```

Run the ingestion demo:

```bash
python3 main.py
```

Run the end-to-end local RAG demo:

```bash
python3 scripts/run_rag_demo.py
```

Run the local Streamlit app:

```bash
streamlit run app.py
```

Run the local FastAPI service:

```bash
uvicorn api:app --reload
```

Example API request:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Is multi-factor authentication required?"}'
```

Build and run the FastAPI service with Docker:

```bash
docker build -t enterprise-rag-api .
docker run -p 8000:8000 enterprise-rag-api
```

## Repository Layout

```text
data/sample/              Sample company documents
docs/                     Blueprint, architecture, decisions, evaluation notes
scripts/                  Small local demos and utilities
src/enterprise_rag/       Application package
tests/                    Focused tests
```

## Documentation

- [Project blueprint](docs/project-blueprint.md)
- [Architecture summary](docs/architecture.md)
- [Build checklist](docs/build-checklist.md)
- [Client interview](docs/client-interview.md)
- [RAG mental roadmap](docs/rag-mental-roadmap.md)
- [Chunking strategy notes](docs/chunking-strategy-cheatsheet.md)
- [Future-state modules](docs/future-state-modules.md)
- [Project 1 closeout](docs/project-1-closeout.md)

## Production Mapping

| Local development | AWS production equivalent |
| --- | --- |
| Local files | S3 |
| Local Python pipeline | Lambda or containerized jobs |
| Chroma | OpenSearch vector index |
| Local LLM calls | Amazon Bedrock |
| Local logs | CloudWatch |
| Local config | IAM, Secrets Manager, parameter store |

## Definition of Done

This project is complete when the system can be demonstrated end to end, major engineering decisions can be defended, evaluation results are visible, and unsupported questions are refused instead of hallucinated.
