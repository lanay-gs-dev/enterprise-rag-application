# Future-State Modules

This project is being built in phases. The runnable package should only contain
code that matches the current data model and can be explained end to end.

## Current Package Scope

- `models.py`: document, chunk, retrieved chunk, and metadata validation shapes
- `ingestion.py`: Markdown front matter parsing and metadata validation
- `chunking.py`: deterministic paragraph-aware chunking
- `embeddings.py`: local text and query embeddings
- `vectorstore.py`: local Chroma index for embedded chunks
- `retrieval.py`: query embedding and vector search for ranked evidence chunks

## Deferred Modules

These capabilities are planned, but should be added only after the previous
phase is working and tested:

- `generation.py`: prompt assembly, answer generation, citation checks, refusals
- `providers.py`: local/API/Bedrock LLM provider routing
- `config.py`: typed settings and environment configuration
- `build_index.py`: batch indexing command for full document refreshes
- optional hybrid reranking for improved retrieval quality

Keeping these out of the runnable package until they are integrated prevents the
repository from looking more complete than it is and keeps the code easier to
explain in interviews.
