# Architecture Summary

## Current Slice

```text
data/sample/*.md
  -> enterprise_rag.ingestion.load_markdown_documents
  -> enterprise_rag.models.validate_metadata
  -> Document objects ready for chunking
```

## Target RAG Flow

```text
User question
  -> query normalization
  -> embedding
  -> vector retrieval
  -> optional metadata filtering
  -> evidence selection
  -> grounded prompt
  -> LLM answer
  -> citation verification
  -> answer, citations, debug info, or refusal
```

## Key Data Objects

- `Document`: source path, content, and validated metadata
- `DocumentChunk`: stable chunk ID, source ID, chunk text, copied metadata, and
  character offsets

## Design Principle

Each phase should produce a clear object that the next phase can trust.

```text
Raw file -> Document -> DocumentChunk -> embedding record -> retrieved evidence
```

## AWS Production Mapping

```text
S3
  -> ingestion Lambda or container job
  -> Bedrock embeddings
  -> OpenSearch vector index
  -> API Lambda
  -> Bedrock generation
  -> CloudWatch logs and metrics
```

## Security Notes

- Metadata should include ownership and security classification.
- Retrieval must eventually enforce access controls before evidence reaches the
  model.
- Prompts should instruct the model to answer only from retrieved evidence.
- Logs should avoid leaking sensitive document contents unnecessarily.
