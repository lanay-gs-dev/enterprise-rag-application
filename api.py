from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys

from fastapi import FastAPI
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.pipeline import RagRuntime, answer_question, build_sample_index

app = FastAPI(title="Enterprise RAG API", version="0.1.0")


class AskRequest(BaseModel):
    question: str = Field(min_length=1)


class RetrievedChunkResponse(BaseModel):
    chunk_id: str
    source_id: str
    text: str
    metadata: dict[str, str]
    score: float
    rank: int


class AskResponse(BaseModel):
    answer: str
    citations: list[str]
    refused: bool
    retrieved: list[RetrievedChunkResponse]


@lru_cache
def get_runtime() -> RagRuntime:
    return build_sample_index(ROOT / "data" / "sample")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    runtime = get_runtime()
    answer, retrieved = answer_question(request.question, runtime, k=2)
    return AskResponse(
        answer=answer.text,
        citations=answer.citations,
        refused=answer.refused,
        retrieved=[
            RetrievedChunkResponse(
                chunk_id=chunk.chunk_id,
                source_id=chunk.source_id,
                text=chunk.text,
                metadata=chunk.metadata,
                score=chunk.score,
                rank=chunk.rank,
            )
            for chunk in retrieved
        ],
    )
