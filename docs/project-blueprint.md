# Project Blueprint

## Mission

Build an Enterprise RAG system that answers questions from internal documents
with source-backed responses, clear citations, and refusal behavior when
evidence is insufficient.

## Business Problem

Employees often need answers buried in handbooks, policies, SOPs, and
operations reports. Traditional search returns documents, but users still have
to inspect sources manually and decide which passages are trustworthy.

## Users

- Employees asking policy and operations questions
- Support, IT, and operations teams maintaining source documents
- Engineers evaluating retrieval quality, citations, and refusal behavior

## Inputs

- Implemented first: Markdown documents with front matter metadata
- Implemented now: user questions through the local Streamlit demo and FastAPI
  `/ask` endpoint
- Planned later: PDFs, SOPs, knowledge articles, S3 document sources, and
  authenticated users

## Outputs

- Phase 1: validated `Document` objects
- Phase 2: citeable `DocumentChunk` objects
- Implemented now: retrieved evidence, citation IDs, deterministic
  answer/refusal responses, Streamlit output, and FastAPI JSON responses
- Planned later: LLM-backed answers, citation verification, evaluation reports,
  and access-control-aware responses

## Success Criteria

- Valid documents load successfully
- Documents missing required metadata fail clearly
- Directory ingestion is deterministic
- Chunks have stable IDs and preserve metadata
- Unsupported questions refuse instead of hallucinating

## Current Architecture

```text
documents
  -> metadata validation
  -> chunking
  -> embeddings
  -> vector store
  -> retrieval
  -> grounded generation
  -> citation verification
  -> answer or refusal
```

## Current Phase

Project 1 local foundation is complete:

```text
Markdown files
  -> parse front matter and validate metadata
  -> chunk documents
  -> embed chunks
  -> store/search vectors
  -> retrieve evidence
  -> return answer/refusal through Streamlit or FastAPI
```

## AWS Mapping

| Local project | AWS production equivalent |
|---|---|
| Markdown files | S3 objects |
| Ingestion function | Lambda or container job |
| Metadata validation | Data quality gate / quarantine workflow |
| Local tests | CI checks |
| Local Chroma vector store | OpenSearch vector index or Bedrock Knowledge Bases |
| Future LLM-backed generation | Amazon Bedrock |

## Out Of Scope For Project 1

- LLM-backed generation
- Access-control enforcement
- Full evaluation harness
- AWS deployment
- PDF/document connector ingestion
