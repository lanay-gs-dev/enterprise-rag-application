from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.models import RetrievedChunk
from enterprise_rag.retrieval import retrieve


class RetrievalTests(unittest.TestCase):
    def test_retrieve_embeds_question_and_queries_index(self) -> None:
        expected = [
            RetrievedChunk(
                chunk_id="security-policy::chunk-0000",
                source_id="security-policy",
                text="Employees must use multi-factor authentication.",
                metadata={"title": "Security Policy"},
                start_char=0,
                end_char=48,
                score=0.91,
                rank=1,
            )
        ]

        with (
            patch("enterprise_rag.retrieval.embed_query", return_value=[1.0, 0.0, 0.0]) as embed,
            patch("enterprise_rag.retrieval.query_index", return_value=expected) as query,
        ):
            results = retrieve("Is MFA required?", k=1)

        embed.assert_called_once_with("Is MFA required?")
        query.assert_called_once_with([1.0, 0.0, 0.0], k=1)
        self.assertEqual(results, expected)

    def test_rejects_blank_question(self) -> None:
        with self.assertRaises(ValueError):
            retrieve("   ")


if __name__ == "__main__":
    unittest.main()
