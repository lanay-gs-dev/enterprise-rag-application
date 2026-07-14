"""
schemas.py — The data shapes that flow through the pipeline.

WHY THIS FILE EXISTS
--------------------
Every stage of a RAG pipeline hands data to the next stage. If those
hand-offs are loose dicts, bugs hide: someone renames "doc_id" to "id"
in one place and retrieval silently breaks. Pydantic models make each
hand-off a CONTRACT — wrong shape, loud error, immediately.

Read this file FIRST when learning the codebase. If you understand these
five shapes, you understand the whole system's data flow:

    DocumentMetadata → what a source document IS
    Chunk            → a retrievable slice of a document
    RetrievedChunk   → a Chunk plus "how relevant was it"
    Citation         → proof a claim came from somewhere
    Answer           → what the user finally sees

TRY IT YOURSELF FIRST ▸ Before reading my version: sketch on paper what
fields a "chunk" needs so that (a) you can cite it, (b) you can debug
why it was retrieved, (c) you can filter by document type. Then compare.
"""

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """Everything we know about a source document BESIDES its text.

    INTERVIEW NOTE: metadata is not decoration — it powers citations
    (title, doc_id), trust signals (owner, version, effective_date),
    and filtering (doc_type, locations). "Metadata-aware ingestion" on
    your resume means exactly this model.
    """

    doc_id: str                      # stable ID, e.g. "MEM-001" — citations point here
    title: str
    doc_type: str                    # policy | sop | report | glossary | matrix | newsletter
    business_area: str               # e.g. "Member Services", "Safety & Compliance"
    owner: str                       # accountable role — enterprise docs always have one
    version: str
    effective_date: str              # ISO date string; "is this current?" lives here
    locations: str = "all"           # comma-separated location scope


class Chunk(BaseModel):
    """One retrievable slice of a document. The atom of RAG."""

    chunk_id: str                    # f"{doc_id}::{section}::{n}" — unique + human-readable
    doc_id: str
    section: str                     # the "## heading" this text lives under
    text: str
    metadata: DocumentMetadata

    def citation_tag(self) -> str:
        """How this chunk is labeled inside the prompt AND in citations.
        Keeping one canonical format means the model can echo it back
        and we can detect which chunks it actually used."""
        return f"[{self.doc_id} §{self.section}]"


class RetrievedChunk(BaseModel):
    """A Chunk + retrieval evidence. This is what the Debug tab shows.

    WHY 'used' EXISTS: retrieved ≠ used. The model may get 5 chunks and
    cite 2. Showing both is what separates a debuggable system from a
    black box — and it's a great interview talking point.
    """

    chunk: Chunk
    score: float = Field(description="similarity/hybrid score, higher = better")
    rank: int
    used_in_answer: bool = False


class Citation(BaseModel):
    doc_id: str
    section: str
    title: str


class Answer(BaseModel):
    """The final product. Either grounded text + citations, or an honest refusal."""

    text: str
    citations: list[Citation] = []
    refused: bool = False
    retrieved: list[RetrievedChunk] = []   # kept for the Debug tab
