# Project Blueprint

## Mission

Build an enterprise RAG system that answers questions from internal documents with retrieved evidence, citations, and refusal behavior when support is insufficient.

## Business Problem

Employees often need answers buried in policies, procedures, and operating documents. Traditional search returns files, but users still have to locate the relevant passage and decide whether it supports the answer.

## Current Scope

Implemented:

- Markdown ingestion and metadata validation
- deterministic, section-aware chunking
- local embeddings and Chroma vector retrieval
- deterministic answer/refusal response shaping with citations
- Streamlit and FastAPI interfaces
- Docker packaging
- unit tests and a 25-question evaluation harness

Planned:

- LLM-backed grounded generation
- AWS deployment
- PDF and additional document connectors
- authentication and retrieval-time access controls

## Users

- Employees asking policy and operations questions
- Document owners maintaining source content
- Engineers evaluating retrieval quality, citations, and refusal behavior

## Key Outputs

- validated `Document` objects
- citeable `DocumentChunk` objects
- ranked `RetrievedChunk` evidence
- structured `Answer` responses with citation IDs and a refusal flag
- repeatable retrieval and refusal evaluation results

## Success Criteria

- Invalid metadata fails clearly before indexing.
- Chunk IDs are stable and preserve source metadata.
- Supported questions retrieve expected evidence.
- Responses identify their source chunks.
- Unsupported questions are refused instead of presented as grounded answers.
- Changes can be checked against a repeatable evaluation baseline.

## AWS Mapping

| Local component | AWS production option |
| --- | --- |
| Markdown files | Amazon S3 |
| Ingestion pipeline | AWS Lambda or an ECS task |
| Local embedding model | Amazon Bedrock embedding model |
| Chroma vector index | Amazon OpenSearch or Bedrock Knowledge Bases |
| Dockerized FastAPI service | Amazon ECR and Amazon ECS |
| Planned LLM generation | Amazon Bedrock |
| Local logs and configuration | CloudWatch, IAM, and Secrets Manager |

## Current Boundaries

This prototype does not yet claim production deployment, LLM-generated answers, user authentication, authorization-aware retrieval, or production-scale performance.
