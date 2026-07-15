# Engineering Decisions

The prototype deliberately starts local so pipeline behavior can be understood and measured before AWS-managed components are introduced.

## 1. Validate Metadata Before Indexing

**Decision:** Require ownership, document type, effective date, and security classification before a document enters the index.

**Why:** Retrieval quality is not only semantic. Enterprise systems also need traceability, governance, and a future way to enforce access rules.

**Tradeoff:** Strict validation rejects incomplete documents and creates an onboarding step for content owners.

## 2. Use Deterministic, Section-Aware Chunking

**Decision:** Split Markdown content using stable rules while preserving headings, offsets, and source metadata.

**Why:** Stable chunks make tests repeatable and citations easier to inspect.

**Alternative:** Token-only or model-assisted chunking may improve some retrieval cases, but adds variability and complexity before a baseline exists.

## 3. Start With Local Embeddings and Chroma

**Decision:** Use `sentence-transformers` and Chroma for the first working retrieval loop.

**Why:** Local components keep the development cycle fast and expose how embeddings, indexing, scoring, and thresholds interact.

**Tradeoff:** Chroma is appropriate for a prototype, not the final choice for enterprise scale, identity-aware retrieval, or managed availability.

**AWS path:** Compare Amazon OpenSearch with Bedrock Knowledge Bases after the local baseline is stable.

## 4. Implement Refusal Before LLM Generation

**Decision:** Shape a deterministic answer or refusal from retrieved evidence before adding a generative model.

**Why:** This isolates retrieval and threshold behavior. A fluent model response can otherwise hide weak evidence.

**Tradeoff:** Current answers are intentionally limited and are not natural-language synthesis.

**Next step:** Add Bedrock-backed generation only after the prompt can require evidence use, citations, and refusal when support is insufficient.

## 5. Separate the Demo From the API

**Decision:** Use Streamlit for the human-facing demo and FastAPI for the application boundary.

**Why:** Streamlit makes the workflow easy to inspect. FastAPI shows how another application could submit a question and receive a structured response.

**Alternative:** A single UI-only application would be simpler, but would hide the integration contract.

## 6. Measure Before Migrating

**Decision:** Maintain a golden question set for retrieval and refusal behavior.

**Why:** The evaluation baseline distinguishes a genuine improvement from a change that merely looks better in a demo.

**Tradeoff:** A small dataset cannot represent every production question. It must expand as failures and new document types are discovered.

## Production Decision Gates

Before selecting final AWS components, evaluate:

- traffic pattern and latency requirements
- document volume and update frequency
- metadata filtering and authorization needs
- managed-service cost at expected scale
- operational ownership and observability requirements
- quality differences between the custom pipeline and Bedrock Knowledge Bases
