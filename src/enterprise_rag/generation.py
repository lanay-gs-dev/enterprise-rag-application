"""
generation.py — Turn retrieved evidence into a cited answer (or an honest refusal).

THE THREE BEHAVIORS THIS FILE OWNS (each is a resume bullet):
  1. GROUNDED ANSWERS WITH CITATIONS — the model may only use the
     provided chunks and must tag claims with [DOC-ID §Section].
  2. REFUSAL — if the evidence doesn't cover the question, say so.
     A RAG system that never refuses is a hallucination machine with
     extra steps.
  3. PROMPT-INJECTION DEFENSE — retrieved documents are DATA, not
     instructions. One of our corpus docs literally contains an attack
     ("ignore previous instructions...") to prove the defense works.
     This maps to OWASP LLM Top 10 #1 (Prompt Injection) — say that
     exact phrase in interviews.

HOW THE REFUSAL MECHANISM WORKS (protocol design, worth studying):
  We tell the model: if unsupported, reply starting with the literal
  token "INSUFFICIENT_EVIDENCE:". Detecting a fixed sentinel string is
  RELIABLE; asking an LLM "did you refuse?" is not. When you need to
  detect a model behavior in code, design a protocol for it.

TRY IT YOURSELF FIRST ▸ Open prompts/rag_answer_v1.txt and read it before
reading this code. The prompt IS the spec; this file just enforces it.
"""

import re
from pathlib import Path

from src import providers
from src.schemas import Answer, Citation, RetrievedChunk

PROMPT_PATH = Path("prompts/rag_answer_v1.txt")
REFUSAL_SENTINEL = "INSUFFICIENT_EVIDENCE:"
REFUSAL_MESSAGE = (
    "I can't answer that from the Ironwood document set. "
    "The retrieved sources don't contain supporting evidence for this question."
)

# WHY PROMPTS LIVE IN FILES, NOT STRINGS: prompts are versioned artifacts
# (v1, v2...) you diff, test, and discuss in code review — not vibes buried
# in Python. "Prompt versioning" is a real practice; this is its simplest form.


def build_messages(question: str, retrieved: list[RetrievedChunk]) -> list[dict]:
    """Assemble the chat messages: system prompt + evidence + question.

    INJECTION DEFENSE #1 lives here structurally: every chunk is wrapped in
    <chunk> tags inside a <context> block, and the system prompt declares
    everything inside <context> is untrusted data. Clear structural
    boundaries are the first line of defense.
    """
    system = PROMPT_PATH.read_text(encoding="utf-8")

    context_parts = []
    for rc in retrieved:
        c = rc.chunk
        context_parts.append(
            f'<chunk doc_id="{c.doc_id}" section="{c.section}" '
            f'title="{c.metadata.title}" version="{c.metadata.version}">\n'
            f"{c.text}\n</chunk>"
        )
    context = "<context>\n" + "\n\n".join(context_parts) + "\n</context>"

    user = f"{context}\n\nQuestion: {question}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def extract_citations(answer_text: str, retrieved: list[RetrievedChunk]) -> list[Citation]:
    """Find [DOC-ID §Section] tags in the answer and match them to real chunks.

    WHY VERIFY INSTEAD OF TRUST: the model could invent a citation tag for
    a document that doesn't exist. We only accept citations that match a
    chunk we actually provided. Trust, but verify — mechanically.
    """
    cited: list[Citation] = []
    seen: set[str] = set()
    tags = re.findall(r"\[([A-Z0-9\-]+)\s*§([^\]]+)\]", answer_text)

    for doc_id, section in tags:
        section = section.strip()
        for rc in retrieved:
            if rc.chunk.doc_id == doc_id and rc.chunk.section == section:
                key = f"{doc_id}::{section}"
                if key not in seen:
                    seen.add(key)
                    cited.append(
                        Citation(doc_id=doc_id, section=section, title=rc.chunk.metadata.title)
                    )
                rc.used_in_answer = True  # powers the Debug tab's "used?" column
    return cited


def answer_question(question: str, retrieved: list[RetrievedChunk]) -> Answer:
    """The full generation step: prompt → model → parse → Answer object."""
    messages = build_messages(question, retrieved)
    raw = providers.chat(messages)  # provider-agnostic — see providers.py

    if raw.strip().startswith(REFUSAL_SENTINEL):
        return Answer(text=REFUSAL_MESSAGE, refused=True, retrieved=retrieved)

    citations = extract_citations(raw, retrieved)

    # DEFENSE-IN-DEPTH: an answer with ZERO verifiable citations is treated
    # as ungrounded and converted to a refusal. Belt and suspenders — if the
    # model ignored the citation instruction, we don't pass its claims along.
    if not citations:
        return Answer(text=REFUSAL_MESSAGE, refused=True, retrieved=retrieved)

    return Answer(text=raw.strip(), citations=citations, retrieved=retrieved)
