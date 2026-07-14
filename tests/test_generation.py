from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.generation import REFUSAL_TEXT, answer_from_evidence
from enterprise_rag.models import RetrievedChunk


class GenerationTests(unittest.TestCase):
    def test_refuses_when_no_evidence_is_available(self) -> None:
        answer = answer_from_evidence("What is the travel policy?", [])

        self.assertTrue(answer.refused)
        self.assertEqual(answer.text, REFUSAL_TEXT)
        self.assertEqual(answer.citations, [])

    def test_returns_answer_with_citation_when_evidence_exists(self) -> None:
        chunk = RetrievedChunk(
            chunk_id="security-policy-2026::chunk-0000",
            source_id="security-policy-2026",
            text="Employees must use multi-factor authentication.",
            metadata={"title": "Security Policy"},
            start_char=0,
            end_char=48,
            score=0.92,
            rank=1,
        )

        answer = answer_from_evidence("Is MFA required?", [chunk])

        self.assertFalse(answer.refused)
        self.assertEqual(answer.citations, ["security-policy-2026::chunk-0000"])
        self.assertIn("multi-factor authentication", answer.text)

    def test_refuses_when_best_evidence_score_is_too_low(self) -> None:
        chunk = RetrievedChunk(
            chunk_id="handbook-2026::chunk-0000",
            source_id="handbook-2026",
            text="Vacation days do not roll over.",
            metadata={"title": "Employee Handbook"},
            start_char=0,
            end_char=31,
            score=0.05,
            rank=1,
        )

        answer = answer_from_evidence("What is the travel policy?", [chunk])

        self.assertTrue(answer.refused)
        self.assertEqual(answer.citations, [])

    def test_rejects_blank_question(self) -> None:
        with self.assertRaises(ValueError):
            answer_from_evidence("   ", [])


if __name__ == "__main__":
    unittest.main()
