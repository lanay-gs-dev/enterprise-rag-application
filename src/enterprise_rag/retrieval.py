"""
retrieval.py — Find the right evidence. Two modes: baseline + improved.

THE EXPERIMENT AT THE HEART OF THIS PROJECT
-------------------------------------------
Your resume bullet says "improved retrieval hit rate from X% → Y%".
THIS file is where X and Y come from.

  BASELINE: pure vector search. Embed the question, take top-k nearest
  chunks. Simple, and it fails in a predictable way: embeddings capture
  MEANING but blur EXACT TERMS. Ask about "DojoTrack" or "90 days" and
  semantic search may prefer a thematically-similar chunk that never
  mentions DojoTrack at all.

  IMPROVED: hybrid retrieval. Over-fetch (top 3k candidates by vector),
  then re-score each as
      0.75 × semantic similarity + 0.25 × keyword overlap
  and keep the new top-k. Keyword overlap rescues exact-term questions;
  semantic similarity still handles paraphrases. This is a hand-rolled,
  inspectable version of what BM25-fusion / rerankers do in production
  (Cohere Rerank, cross-encoders — see future_ladder.md).

WHY BUILD IT BY HAND INSTEAD OF IMPORTING A RERANKER: because then you
can explain every number in the score. That's the difference between
"I used a reranker" and "I understand reranking" in an interview.

TRY IT YOURSELF FIRST ▸ Write keyword_overlap(question, text) on paper:
lowercase both, split into word sets, remove stopwords, return
|intersection| / |question words|. Then compare.
"""

from src.config import get_settings
from src.embeddings import embed_query
from src.schemas import RetrievedChunk
from src.vectorstore import query_index

# Tiny stopword list — enough to stop "the/is/of" dominating overlap scores.
# (Production would use a real list; this keeps v1 dependency-free.)
STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "what", "which", "who",
    "how", "when", "where", "why", "do", "does", "did", "for", "of", "in",
    "on", "at", "to", "and", "or", "our", "their", "it", "its", "be", "with",
}

SEMANTIC_WEIGHT = 0.75
KEYWORD_WEIGHT = 0.25


def keyword_overlap(question: str, text: str) -> float:
    """Fraction of the question's meaningful words that appear in the text.
    Range 0..1. Crude, transparent, effective — in that order."""
    q_words = {w.strip("?.,:;()").lower() for w in question.split()} - STOPWORDS
    t_words = {w.strip("?.,:;()").lower() for w in text.split()}
    if not q_words:
        return 0.0
    return len(q_words & t_words) / len(q_words)


def hybrid_score(semantic: float, keyword: float) -> float:
    """Weighted fusion. The 0.75/0.25 split is a starting point, not gospel —
    the eval harness is the tool for tuning it. (Try 0.6/0.4. Measure.)"""
    return SEMANTIC_WEIGHT * semantic + KEYWORD_WEIGHT * keyword


def retrieve(question: str, mode: str = "improved") -> list[RetrievedChunk]:
    """The one function the rest of the app calls.

    mode="baseline" → pure vector top-k       (results_baseline.csv)
    mode="improved" → hybrid rerank of top-3k (results_improved.csv)
    """
    k = get_settings().top_k
    q_emb = embed_query(question)

    if mode == "baseline":
        return query_index(q_emb, k)

    # IMPROVED: over-fetch, re-score, re-rank, trim.
    candidates = query_index(q_emb, k * 3)
    for rc in candidates:
        rc.score = hybrid_score(rc.score, keyword_overlap(question, rc.chunk.text))

    candidates.sort(key=lambda rc: rc.score, reverse=True)
    top = candidates[:k]
    for rank, rc in enumerate(top, start=1):  # re-number ranks after re-sort
        rc.rank = rank
    return top
