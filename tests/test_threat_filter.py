"""Tests for the hybrid threat filter."""

import pytest

from si_protocols.threat_filter import (
    ThreatResult,
    hybrid_score,
    psychic_heuristic,
    tech_analysis,
)

# --- Fixtures ---

BENIGN_TEXT = "The cat sat on the mat. It was a pleasant Tuesday afternoon."

SUSPICIOUS_TEXT = (
    "The ascended masters say that the hidden cosmic truth has been veiled "
    "from humanity. The galactic federation confirms that you must act now "
    "before the window is closing. Only the chosen will transcend."
)

EMPTY_TEXT = ""


# --- psychic_heuristic ---


class TestPsychicHeuristic:
    def test_deterministic_with_seed(self) -> None:
        a = psychic_heuristic(0.75, seed=42)
        b = psychic_heuristic(0.75, seed=42)
        assert a == b

    def test_output_range(self) -> None:
        for seed in range(100):
            score = psychic_heuristic(1.0, seed=seed)
            assert 0 <= score <= 80

    def test_lower_density_scales_down(self) -> None:
        high = psychic_heuristic(1.0, seed=42)
        low = psychic_heuristic(0.5, seed=42)
        assert low == pytest.approx(high * 0.5)


# --- tech_analysis ---


class TestTechAnalysis:
    @pytest.mark.slow
    def test_empty_text_returns_zero(self) -> None:
        score, entities, auth, urgency = tech_analysis(EMPTY_TEXT)
        assert score == 0.0
        assert entities == []
        assert auth == []
        assert urgency == []

    @pytest.mark.slow
    def test_benign_text_low_score(self) -> None:
        score, _, _, _ = tech_analysis(BENIGN_TEXT)
        assert score < 20.0

    @pytest.mark.slow
    def test_suspicious_text_higher_score(self) -> None:
        score, _, auth, urgency = tech_analysis(SUSPICIOUS_TEXT)
        assert score > 0.0
        assert len(auth) > 0 or len(urgency) > 0


# --- hybrid_score ---


class TestHybridScore:
    @pytest.mark.slow
    def test_returns_threat_result(self) -> None:
        result = hybrid_score(BENIGN_TEXT, seed=42)
        assert isinstance(result, ThreatResult)

    @pytest.mark.slow
    def test_deterministic_with_seed(self) -> None:
        a = hybrid_score(BENIGN_TEXT, seed=42)
        b = hybrid_score(BENIGN_TEXT, seed=42)
        assert a == b

    @pytest.mark.slow
    def test_suspicious_scores_higher_than_benign(self) -> None:
        benign = hybrid_score(BENIGN_TEXT, seed=42)
        sus = hybrid_score(SUSPICIOUS_TEXT, seed=42)
        # Tech contribution should be higher for suspicious text
        assert sus.tech_contribution > benign.tech_contribution

    @pytest.mark.slow
    def test_message_present(self) -> None:
        result = hybrid_score(BENIGN_TEXT, seed=42)
        assert "local tool" in result.message.lower()
