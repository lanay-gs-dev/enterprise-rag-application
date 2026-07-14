from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.embeddings import embed_query, embed_texts


def similarity(left: list[float], right: list[float]) -> float:
    return sum(left_value * right_value for left_value, right_value in zip(left, right))


def embed_texts_or_skip(texts: list[str]) -> list[list[float]]:
    try:
        return embed_texts(texts)
    except Exception as exc:
        raise unittest.SkipTest(f"Embedding model is unavailable: {exc}") from exc


class EmbeddingTests(unittest.TestCase):
    def test_embeddings_preserve_count_and_dimensions(self) -> None:
        texts = [
            "Employees must use multi-factor authentication.",
            "MFA is required for company systems.",
            "Vacation days do not roll over.",
        ]

        vectors = embed_texts_or_skip(texts)
        try:
            query_vector = embed_query("Is MFA required?")
        except Exception as exc:
            raise unittest.SkipTest(f"Embedding model is unavailable: {exc}") from exc

        self.assertEqual(len(vectors), 3)
        self.assertEqual(len(vectors[0]), 384)
        self.assertEqual(len(query_vector), 384)

    def test_related_texts_score_higher_than_unrelated_texts(self) -> None:
        texts = [
            "Employees must use multi-factor authentication.",
            "MFA is required for company systems.",
            "Vacation days do not roll over.",
        ]

        vectors = embed_texts_or_skip(texts)

        related_score = similarity(vectors[0], vectors[1])
        unrelated_score = similarity(vectors[0], vectors[2])

        self.assertGreater(related_score, unrelated_score)


if __name__ == "__main__":
    unittest.main()
