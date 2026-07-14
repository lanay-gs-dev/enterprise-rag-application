# Architecture Summary

## Current Implemented Flow

```text
data/sample/*.md
  -> enterprise_rag.ingestion.load_markdown_documents
  -> enterprise_rag.models.validate_metadata
  -> enterprise_rag.chunking.chunk_document
  -> enterprise_rag.embeddings.embed_texts
  -> enterprise_rag.vectorstore.build_index
  -> enterprise_rag.retrieval.retrieve
  -> enterprise_rag.generation.answer_from_evidence
  -> Streamlit app or FastAPI /ask response
```

## Target Enterprise RAG Flow

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
- `RetrievedChunk`: retrieved evidence with rank and score
- `Answer`: final response text, citation IDs, and refusal flag

## Design Principle

Each phase should produce a clear object that the next phase can trust.

```text
Raw file -> Document -> DocumentChunk -> embedding -> RetrievedChunk -> Answer
```

## AWS Production Mapping

```text
S3
  -> ingestion Lambda or container job
  -> Bedrock embeddings
  -> OpenSearch vector index
  -> FastAPI service on App Runner or ECS
  -> Bedrock generation
  -> CloudWatch logs and metrics
```

## Security Notes

- Metadata should include ownership and security classification.
- Retrieval must eventually enforce access controls before evidence reaches the
  model.
- Prompts should instruct the model to answer only from retrieved evidence.
- Logs should avoid leaking sensitive document contents unnecessarily.
