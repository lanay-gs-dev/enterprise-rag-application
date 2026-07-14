from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from fastapi.testclient import TestClient

from api import app
from enterprise_rag.models import Answer, RetrievedChunk
from enterprise_rag.pipeline import RagRuntime


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        app.dependency_overrides.clear()

    def test_health_returns_ok(self) -> None:
        client = TestClient(app)

        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_ask_returns_answer_contract(self) -> None:
        retrieved = [
            RetrievedChunk(
                chunk_id="security-policy-2026::chunk-0000",
                source_id="security-policy-2026",
                text="Employees must use multi-factor authentication.",
                metadata={"title": "Security Policy"},
                start_char=0,
                end_char=48,
                score=0.91,
                rank=1,
            )
        ]
        answer = Answer(
            text="Employees must use multi-factor authentication.",
            citations=["security-policy-2026::chunk-0000"],
            refused=False,
        )

        with (
            patch("api.get_runtime", return_value=RagRuntime(persist_dir="/tmp/test", chunk_count=1)),
            patch("api.answer_question", return_value=(answer, retrieved)),
        ):
            client = TestClient(app)
            response = client.post("/ask", json={"question": "Is MFA required?"})

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertFalse(body["refused"])
        self.assertEqual(body["citations"], ["security-policy-2026::chunk-0000"])
        self.assertEqual(body["retrieved"][0]["chunk_id"], "security-policy-2026::chunk-0000")


if __name__ == "__main__":
    unittest.main()
