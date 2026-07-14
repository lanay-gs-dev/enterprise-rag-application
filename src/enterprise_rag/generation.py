"""
Answer generation and refusal helpers.

This first version keeps generation deterministic so the response contract is
easy to test: answers must be grounded in retrieved chunks, and unsupported
questions must be refused.
"""

from __future__ import annotations

from enterprise_rag.models import Answer, RetrievedChunk

REFUSAL_TEXT = "I cannot answer that from the available documents."
MINIMUM_EVIDENCE_SCORE = 0.25


def answer_from_evidence(
    question: str,
    retrieved: list[RetrievedChunk],
    minimum_score: float = MINIMUM_EVIDENCE_SCORE,
) -> Answer:
    """Return a grounded placeholder answer or refuse when evidence is missing."""
    if not question.strip():
        raise ValueError("question cannot be blank")

    if not retrieved:
        return Answer(text=REFUSAL_TEXT, citations=[], refused=True)

    best_chunk = retrieved[0]
    if best_chunk.score < minimum_score:
        return Answer(text=REFUSAL_TEXT, citations=[], refused=True)

    return Answer(
        text=_grounded_placeholder(question, best_chunk),
        citations=[best_chunk.chunk_id],
        refused=False,
    )


def _grounded_placeholder(question: str, chunk: RetrievedChunk) -> str:
    return (
        "The available documents contain relevant evidence for this question. "
        f"The top supporting source is {chunk.chunk_id}: {chunk.text}"
    )
