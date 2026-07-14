from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.pipeline import answer_question, build_sample_index


def main() -> None:
    question = "Is multi-factor authentication required?"
    runtime = build_sample_index(ROOT / "data" / "sample")
    answer, _ = answer_question(question, runtime, k=2)

    print(f"Question: {question}")
    print(f"Refused: {answer.refused}")
    print(f"Answer: {answer.text}")
    print("Citations:")
    for citation in answer.citations:
        print(f"- {citation}")


if __name__ == "__main__":
    main()
