from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enterprise_rag.chunking import ChunkingConfig, chunk_document
from enterprise_rag.ingestion import load_markdown_document, load_markdown_documents
from enterprise_rag.models import MetadataValidationError


VALID_DOCUMENT = """---
title: Test Policy
source_id: test-policy
document_type: policy
department: Test
effective_date: 2026-01-01
owner: test@example.com
security_level: internal
---

# Test Policy

This is the first paragraph.

This is the second paragraph with more detail.
"""


class IngestionTests(unittest.TestCase):
    def test_loads_markdown_document_with_valid_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "policy.md"
            path.write_text(VALID_DOCUMENT, encoding="utf-8")

            document = load_markdown_document(path)

        self.assertEqual(document.source_id, "test-policy")
        self.assertEqual(document.title, "Test Policy")
        self.assertIn("first paragraph", document.content)

    def test_rejects_missing_required_metadata(self) -> None:
        invalid_document = VALID_DOCUMENT.replace("owner: test@example.com\n", "")

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "invalid.md"
            path.write_text(invalid_document, encoding="utf-8")

            with self.assertRaises(MetadataValidationError):
                load_markdown_document(path)

    def test_rejects_invalid_security_level(self) -> None:
        invalid_document = VALID_DOCUMENT.replace("security_level: internal", "security_level: secret")

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "invalid-security.md"
            path.write_text(invalid_document, encoding="utf-8")

            with self.assertRaises(MetadataValidationError):
                load_markdown_document(path)

    def test_loads_directory_in_sorted_order(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "b.md").write_text(VALID_DOCUMENT.replace("test-policy", "b"), encoding="utf-8")
            (root / "a.md").write_text(VALID_DOCUMENT.replace("test-policy", "a"), encoding="utf-8")

            documents = load_markdown_documents(root)

        self.assertEqual([document.source_id for document in documents], ["a", "b"])


class ChunkingTests(unittest.TestCase):
    def test_chunks_document_with_stable_ids_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "policy.md"
            path.write_text(VALID_DOCUMENT, encoding="utf-8")
            document = load_markdown_document(path)

            chunks = chunk_document(document, ChunkingConfig(max_chars=80, overlap_chars=20))

        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0].chunk_id, "test-policy::chunk-0000")
        self.assertEqual(chunks[0].metadata["department"], "Test")
        self.assertTrue(all(chunk.text for chunk in chunks))

    def test_rejects_invalid_chunking_config(self) -> None:
        with self.assertRaises(ValueError):
            ChunkingConfig(max_chars=100, overlap_chars=100)


if __name__ == "__main__":
    unittest.main()
