"""Tests for the FastAPI REST API layer."""

import pytest
from app.main import app
from starlette.testclient import TestClient

BENIGN_TEXT = "The cat sat on the mat. It was a pleasant Tuesday afternoon."

SUSPICIOUS_TEXT = (
    "The ascended masters say that the hidden cosmic truth has been veiled "
    "from humanity. The galactic federation confirms that you must act now "
    "before the window is closing. Only the chosen will transcend."
)

SUSPICIOUS_TEXT_JA = (
    "アセンデッドマスターが言う、この宇宙的な真実は長い間秘められたものでした。"
    "銀河連合が確認した、今すぐ行動しなければ窓が閉じようとしている。"
    "選ばれた者だけがアセンションの道を歩むことができる。"
)

client = TestClient(app)


# --- GET /health ---


class TestHealthEndpoint:
    def test_returns_ok(self) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


# --- POST /analyse ---


class TestAnalyseEndpoint:
    @pytest.mark.slow
    def test_valid_text_returns_all_fields(self) -> None:
        response = client.post("/analyse", json={"text": BENIGN_TEXT, "seed": 42})
        assert response.status_code == 200
        data = response.json()
        expected_fields = [
            "overall_threat_score",
            "tech_contribution",
            "intuition_contribution",
            "detected_entities",
            "authority_hits",
            "urgency_hits",
            "emotion_hits",
            "contradiction_hits",
            "source_attribution_hits",
            "escalation_hits",
            "message",
        ]
        for field in expected_fields:
            assert field in data, f"Missing field: {field}"

    @pytest.mark.slow
    def test_suspicious_scores_higher_than_benign(self) -> None:
        benign = client.post("/analyse", json={"text": BENIGN_TEXT, "seed": 42}).json()
        suspicious = client.post("/analyse", json={"text": SUSPICIOUS_TEXT, "seed": 42}).json()
        assert suspicious["tech_contribution"] > benign["tech_contribution"]

    @pytest.mark.slow
    def test_deterministic_with_seed(self) -> None:
        payload = {"text": SUSPICIOUS_TEXT, "seed": 42}
        a = client.post("/analyse", json=payload).json()
        b = client.post("/analyse", json=payload).json()
        assert a == b

    @pytest.mark.slow
    def test_accepts_density_bias(self) -> None:
        response = client.post(
            "/analyse",
            json={"text": BENIGN_TEXT, "density_bias": 0.5, "seed": 42},
        )
        assert response.status_code == 200

    @pytest.mark.slow
    def test_message_contains_local_tool(self) -> None:
        data = client.post("/analyse", json={"text": BENIGN_TEXT, "seed": 42}).json()
        assert "local tool" in data["message"].lower()

    def test_rejects_empty_text(self) -> None:
        response = client.post("/analyse", json={"text": ""})
        assert response.status_code == 422

    def test_rejects_missing_text(self) -> None:
        response = client.post("/analyse", json={})
        assert response.status_code == 422

    def test_rejects_invalid_density_bias(self) -> None:
        response = client.post("/analyse", json={"text": "hello", "density_bias": 2.0})
        assert response.status_code == 422

    @pytest.mark.slow
    def test_accepts_lang_ja(self) -> None:
        response = client.post(
            "/analyse", json={"text": SUSPICIOUS_TEXT_JA, "lang": "ja", "seed": 42}
        )
        assert response.status_code == 200
        data = response.json()
        assert "overall_threat_score" in data

    @pytest.mark.slow
    def test_default_lang_still_works(self) -> None:
        response = client.post("/analyse", json={"text": BENIGN_TEXT, "seed": 42})
        assert response.status_code == 200

    def test_rejects_unsupported_lang(self) -> None:
        response = client.post("/analyse", json={"text": "hello", "lang": "fr"})
        assert response.status_code == 422


# --- JSON sanitising middleware ---


class TestSanitiseJsonMiddleware:
    @pytest.mark.slow
    def test_literal_newlines_in_text_accepted(self) -> None:
        raw_body = '{"text": "line one\nline two\nline three", "seed": 42}'
        response = client.post(
            "/analyse",
            content=raw_body,
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 200

    @pytest.mark.slow
    def test_crlf_newlines_accepted(self) -> None:
        raw_body = '{"text": "line one\r\nline two", "seed": 42}'
        response = client.post(
            "/analyse",
            content=raw_body,
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 200

    @pytest.mark.slow
    def test_tabs_in_text_accepted(self) -> None:
        raw_body = '{"text": "col one\tcol two", "seed": 42}'
        response = client.post(
            "/analyse",
            content=raw_body,
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 200

    @pytest.mark.slow
    def test_escaped_newlines_preserved(self) -> None:
        payload = {"text": "line one\nline two", "seed": 42}
        response = client.post("/analyse", json=payload)
        assert response.status_code == 200

    def test_valid_json_not_modified(self) -> None:
        response = client.post("/analyse", json={"text": "hello", "seed": 42})
        assert response.status_code == 200

    def test_still_rejects_truly_invalid_json(self) -> None:
        response = client.post(
            "/analyse",
            content="{not valid json at all",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422
