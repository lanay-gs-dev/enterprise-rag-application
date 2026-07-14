from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.models import DocumentChunk
from enterprise_rag.vectorstore import build_index, query_index


class VectorStoreTests(unittest.TestCase):
    def test_builds_and_queries_chunk_index(self) -> None:
        chunks = [
            DocumentChunk(
                chunk_id="security-policy::chunk-0000",
                source_id="security-policy",
                text="Employees must use multi-factor authentication.",
                metadata={
                    "title": "Security Policy",
                    "department": "IT",
                    "security_level": "internal",
                },
                start_char=0,
                end_char=48,
            ),
            DocumentChunk(
                chunk_id="handbook::chunk-0000",
                source_id="handbook",
                text="Vacation days do not roll over.",
                metadata={
                    "title": "Employee Handbook",
                    "department": "People",
                    "security_level": "internal",
                },
                start_char=0,
                end_char=31,
            ),
        ]
        embeddings = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            count = build_index(chunks, embeddings, persist_dir=temp_dir)
            results = query_index([1.0, 0.0, 0.0], k=1, persist_dir=temp_dir)

        self.assertEqual(count, 2)
        self.assertEqual(results[0].chunk_id, "security-policy::chunk-0000")
        self.assertEqual(results[0].metadata["title"], "Security Policy")
        self.assertEqual(results[0].rank, 1)


if __name__ == "__main__":
    unittest.main()
