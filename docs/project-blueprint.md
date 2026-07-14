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
- Planned later: PDFs, SOPs, knowledge articles, and user questions

## Outputs

- Phase 1: validated `Document` objects
- Phase 2: citeable `DocumentChunk` objects
- Later phases: retrieved evidence, grounded answers, citations, debug info,
  refusals, and evaluation results

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

Phase 1 focuses on ingestion:

```text
Markdown file
  -> parse front matter
  -> validate metadata
  -> return Document
```

## AWS Mapping

| Local project | AWS production equivalent |
|---|---|
| Markdown files | S3 objects |
| Ingestion function | Lambda or container job |
| Metadata validation | Data quality gate / quarantine workflow |
| Local tests | CI checks |
| Future vector store | OpenSearch vector index |
| Future LLM calls | Amazon Bedrock |

## Out Of Scope For Phase 1

- Embeddings
- Vector search
- LLM generation
- UI
- Access-control enforcement
- Full evaluation harness
