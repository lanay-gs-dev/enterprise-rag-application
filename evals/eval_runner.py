from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.pipeline import answer_question, build_sample_index

DATASET_PATH = ROOT / "evals" / "golden_questions.csv"


@dataclass(frozen=True)
class EvalCase:
    question: str
    expected_source_id: str
    expected_text_contains: str
    should_refuse: bool


@dataclass(frozen=True)
class EvalResult:
    case: EvalCase
    top_source_id: str
    retrieved_match: bool
    refusal_match: bool
    passed: bool
    answer_text: str


def load_cases(path: Path = DATASET_PATH) -> list[EvalCase]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [
            EvalCase(
                question=row["question"],
                expected_source_id=row["expected_source_id"],
                expected_text_contains=row["expected_text_contains"],
                should_refuse=row["should_refuse"].strip().lower() == "true",
            )
            for row in reader
        ]


def run_evaluation(cases: list[EvalCase]) -> list[EvalResult]:
    runtime = build_sample_index(ROOT / "data" / "sample")
    results: list[EvalResult] = []

    for case in cases:
        answer, retrieved = answer_question(case.question, runtime, k=2)
        top_source_id = retrieved[0].source_id if retrieved else ""
        retrieved_text = "\n".join(chunk.text for chunk in retrieved).lower()

        if case.should_refuse:
            retrieved_match = True
        else:
            source_match = any(chunk.source_id == case.expected_source_id for chunk in retrieved)
            text_match = case.expected_text_contains.lower() in retrieved_text
            retrieved_match = source_match and text_match

        refusal_match = answer.refused == case.should_refuse
        passed = retrieved_match and refusal_match
        results.append(
            EvalResult(
                case=case,
                top_source_id=top_source_id,
                retrieved_match=retrieved_match,
                refusal_match=refusal_match,
                passed=passed,
                answer_text=answer.text,
            )
        )

    return results


def print_report(results: list[EvalResult]) -> None:
    total = len(results)
    passed = sum(result.passed for result in results)
    retrieval_passed = sum(result.retrieved_match for result in results)
    refusal_passed = sum(result.refusal_match for result in results)

    print(f"Total questions: {total}")
    print(f"Overall passed: {passed}/{total}")
    print(f"Retrieval checks passed: {retrieval_passed}/{total}")
    print(f"Refusal checks passed: {refusal_passed}/{total}")

    failures = [result for result in results if not result.passed]
    if not failures:
        print("\nNo failures.")
        return

    print("\nFailures:")
    for result in failures:
        print(f"- Question: {result.case.question}")
        print(f"  Expected source: {result.case.expected_source_id or '[refusal expected]'}")
        print(f"  Top source: {result.top_source_id or '[none]'}")
        print(f"  Retrieved match: {result.retrieved_match}")
        print(f"  Refusal match: {result.refusal_match}")


def main() -> None:
    cases = load_cases()
    results = run_evaluation(cases)
    print_report(results)


if __name__ == "__main__":
    main()
