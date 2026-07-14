# Build Checklist

## Current Phase: Project 1 Closeout

### Objective

Finish a local Enterprise RAG foundation that can be tested, demonstrated, and
explained before moving to an AWS-native version.

### Where We Are

- [x] Scenario reviewed at a high level
- [x] Business problem connected to messy internal knowledge repositories
- [x] Phase 1 input/output clarified
- [x] Project 1 source-of-truth folder clarified
- [x] Phase 1 ingestion implemented and reviewed
- [x] Phase 2 chunking implemented and reviewed
- [x] Embeddings and vector store implemented
- [x] Retrieval and answer/refusal contract implemented
- [x] Streamlit demo added
- [x] FastAPI service layer added
- [x] Docker files added
- [x] Tests run successfully
- [x] Project closeout summary added

### Before Coding

- [x] What problem are we solving?
- [x] What are the inputs?
- [x] What are the outputs?
- [x] How will we test it?
- [x] What could fail?

### Definition Of Done

- [x] I can explain what ingestion does.
- [x] Loader reads one Markdown file.
- [x] Loader reads a folder of Markdown files.
- [x] Required metadata is validated.
- [x] Missing metadata fails loudly.
- [x] Invalid security level fails loudly.
- [x] Chunking creates stable, citeable chunks.
- [x] Embeddings convert text and questions into vectors.
- [x] Vector store can build and query a local index.
- [x] Retrieval returns ranked evidence chunks.
- [x] Answer/refusal layer refuses when no evidence exists.
- [x] Streamlit and FastAPI demos run locally.
- [x] Tests pass.
- [x] I can explain the AWS equivalent.

### Files

- `data/sample/*.md`
- `src/enterprise_rag/models.py`
- `src/enterprise_rag/ingestion.py`
- `src/enterprise_rag/chunking.py`
- `src/enterprise_rag/embeddings.py`
- `src/enterprise_rag/vectorstore.py`
- `src/enterprise_rag/retrieval.py`
- `src/enterprise_rag/generation.py`
- `src/enterprise_rag/pipeline.py`
- `api.py`
- `app.py`
- `tests/test_ingestion_chunking.py`
- `tests/test_embeddings.py`
- `tests/test_vectorstore.py`
- `tests/test_retrieval.py`
- `tests/test_generation.py`
- `tests/test_api.py`

### Project 1 Data Flow

```text
Markdown file
  -> read raw text
  -> split front matter metadata from body content
  -> validate required metadata
  -> return Document object
  -> create DocumentChunk objects
  -> embed chunk text
  -> build/query vector index
  -> retrieve evidence
  -> answer or refuse
```

### Why Predictable Folder Loading Matters

Folder order is an engineering reliability issue. If files load in a different
order every run, tests can become flaky and chunk IDs can be harder to debug.
Sorting files gives the same input order every time.

### Common Failure Modes

- Missing required metadata
- Blank metadata values
- Invalid `security_level`
- Bad `effective_date` format
- Missing or malformed front matter
- Wrong source folder path
- Empty or unusable content

### AWS Equivalent

Local Markdown files are like objects in S3. The ingestion loader is like a
Lambda function or container job that validates documents before they are
chunked, embedded, and indexed.

### Interview Explanation Draft

Ingestion is the quality gate for the RAG system. Before documents can be
chunked or retrieved, the system validates that each source has required
metadata like owner, security level, source ID, and effective date. This
prevents unowned, stale, or improperly classified content from entering the
retrieval pipeline.
