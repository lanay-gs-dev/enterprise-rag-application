# Enterprise RAG Project

Retrieval-Augmented Generation system for answering questions from internal company documents with citations, refusal behavior, and explainable retrieval.

It exists to turn scattered company knowledge into trustworthy answers. The interesting part is the foundation: documents must be validated, owned, classified, chunked, and traceable before a model can answer safely.

Current implementation: Markdown ingestion, metadata validation, deterministic chunking, sample enterprise documents, and tests.

Run it:

```bash
python3 -m unittest discover -s tests
python3 scripts/ingest_demo.py
```

## What It Does

- Loads Markdown documents with required front matter.
- Rejects incomplete or invalid metadata before retrieval prep.
- Splits documents into stable, citeable chunks with source metadata.
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

Implemented today: documents -> metadata validation -> chunking.

## Local Development

Run the current test suite:

```bash
python3 -m unittest discover -s tests
```

Run the ingestion demo:

```bash
python3 scripts/ingest_demo.py
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
- [Engineering decisions](docs/decision-log.md)
- [Evaluation notes](docs/evaluation.md)
- [Retrospective](docs/retrospective.md)
- [Lessons learned](docs/lessons-learned.md)
- [Demo notes](docs/demo-notes.md)
- [Interview story bank](docs/interview-story-bank.md)

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
