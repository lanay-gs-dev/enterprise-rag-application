# RAG Mental Roadmap

## The Core Idea

RAG does not train the model. RAG gives the model better context at answer time.

```text
User question
  -> retrieve relevant source material
  -> give that evidence to the model
  -> generate a grounded answer
  -> cite sources or refuse
```

## Business Problem To Engineering Translation

| What the client says | Engineering translation |
|---|---|
| "Our documents are hard to search." | Build ingestion, chunking, and retrieval. |
| "People find stale or conflicting guidance." | Require metadata like owner, source ID, and effective date. |
| "We need to know where the answer came from." | Preserve source metadata and create stable chunk IDs. |
| "Some content is confidential." | Add security labels and later enforce access filtering. |
| "The system cannot make things up." | Add grounded prompts, citation checks, and refusal behavior. |
| "We need to know if it works." | Add tests, golden questions, and evaluation metrics. |

## RAG Component Map

| Need | Component | Common tools |
|---|---|---|
| Read files | Ingestion | `pathlib`, file loaders, PDF/docx parsers |
| Enforce required fields | Validation | `dataclass`, Pydantic, custom validation |
| Represent clean data | Data shapes | classes, dataclasses, typed schemas |
| Split documents | Chunking | custom logic, text splitters |
| Search by meaning | Embeddings | sentence-transformers, Bedrock embeddings |
| Store vectors | Vector store | Chroma, FAISS, OpenSearch |
| Find evidence | Retrieval | vector search, keyword search, hybrid rerank |
| Generate answer | LLM provider | OpenAI, Anthropic, Ollama, Bedrock |
| Prevent guessing | Grounding/refusal | prompt rules, citation verification |
| Prove quality | Evaluation | unit tests, golden datasets, hit rate, refusal tests |

## Phase Roadmap

```text
Phase 1: Ingestion
  Raw documents become validated Document objects.

Phase 2: Chunking
  Documents become smaller citeable chunks.

Phase 3: Embeddings + Vector Store
  Chunks become searchable vectors.

Phase 4: Retrieval
  A user question returns the best evidence chunks.

Phase 5: Generation
  The model answers only from retrieved evidence.

Phase 6: Evaluation + UI
  Users can test the system and engineers can measure quality.
```

## Meeting Framework

When hearing a client problem, ask:

1. What is the business pain?
2. What data exists?
3. What data can be trusted?
4. What output should users see?
5. What risks are unacceptable?
6. What system component handles each risk?

## SAS-To-Python Mental Bridge

| SAS habit | Python/RAG equivalent |
|---|---|
| Define input dataset | Define document/data shape |
| Check variables | Validate metadata fields |
| `PROC FREQ` | Inspect counts, categories, missing values |
| `PROC PRINT` | Print sample records/chunks |
| Data quality rules | Validation functions and tests |
| Output dataset | Clean object passed to the next pipeline step |

## Interview Line

When a client asks for RAG, I do not start with the model. I first identify the
source documents, metadata requirements, trust boundaries, and failure modes.
Then I map each risk to a system component: ingestion validates the data,
chunking preserves traceable evidence, retrieval finds relevant context, and
generation answers only from that context.
