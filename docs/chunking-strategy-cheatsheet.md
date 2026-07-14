# Chunking Strategy Cheat Sheet

## Why Chunking Matters

Chunking decides what evidence the retriever can find.

```text
bad chunks -> weak retrieval -> weak answers
good chunks -> focused evidence -> better grounded answers
```

Chunking is not just a formatting step. It is one of the biggest quality levers
in a RAG system.

## Chunking Methods

| Method | How it works | Strengths | Tradeoffs | When to use |
|---|---|---|---|---|
| Fixed-size | Split every N characters or tokens. | Simple, fast, easy to code. | Can cut sentences, tables, or ideas in half. | Good for first prototype or uniform text. |
| Paragraph-aware | Keep paragraphs together when possible. | More readable chunks, preserves local context. | More code than fixed-size; still not topic-aware. | Good for policies, SOPs, handbooks, Markdown docs. |
| Section-aware | Split by headings or document sections. | Preserves human-authored structure. | Needs reliable headings; tables/edge cases need care. | Best when docs have clean headings like `## Policy`. |
| Semantic | Split where meaning/topic changes, often using embeddings or an LLM. | Can create highly relevant topic-based chunks. | More complex, slower, costlier, harder to debug. | Use after evals show simpler methods are failing. |

## Current Project Choice

Project 1 uses **paragraph-aware chunking**.

Why:

- It is more reliable than raw fixed-size slicing.
- It keeps human-readable paragraphs together.
- It is deterministic and testable.
- It is easier to explain than semantic chunking.
- It fits Markdown policy/SOP-style documents.

## Why Not Semantic Chunking First?

Semantic chunking sounds best, but it is not automatically the best first move.

Potential benefits:

- Cleaner topic boundaries
- Better retrieval for concept-based questions
- Less unrelated text in each chunk

Costs:

- More moving parts
- More expensive if it uses embeddings or LLM calls
- Less deterministic
- Harder to debug when retrieval behaves oddly
- Requires evaluation to prove it is actually better

## Chunk Size And Overlap

Current defaults:

```python
max_chars = 900
overlap_chars = 150
```

These are starting assumptions, not magic numbers.

`max_chars = 900`:

- focused enough for retrieval
- large enough to hold a useful passage
- small enough to embed cheaply

`overlap_chars = 150`:

- preserves context across boundaries
- about 16-17% of 900
- avoids making every chunk mostly duplicate text

## Interview Line

I started with deterministic paragraph-aware chunking because it is explainable,
testable, and a good fit for structured Markdown policies and SOPs. I would only
move to semantic chunking after retrieval evals show that paragraph or
section-aware chunking is failing. Chunk size is not a belief; it is an
evaluation parameter.

## AWS / Enterprise Connection

In production, chunking might run in a batch job after documents land in S3.
The resulting chunks would be embedded with Bedrock and indexed in OpenSearch.
Metadata and character offsets should travel with every chunk so retrieved
evidence remains traceable, filterable, and auditable.
