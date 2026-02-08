"""Tests for the hybrid threat filter."""

from pathlib import Path

import pytest

from si_protocols.threat_filter import (
    ThreatResult,
    hybrid_score,
    main,
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

EMOTIONAL_TEXT = (
    "Catastrophe and doom await those who ignore the signs. Destruction and "
    "devastation will consume the unworthy. But salvation and bliss await the "
    "chosen few who embrace the miracle of ascension and transcendence."
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
        score, entities, auth, urgency, emotion = tech_analysis(EMPTY_TEXT)
        assert score == 0.0
        assert entities == []
        assert auth == []
        assert urgency == []
        assert emotion == []

    @pytest.mark.slow
    def test_benign_text_low_score(self) -> None:
        score, _, _, _, _ = tech_analysis(BENIGN_TEXT)
        assert score < 20.0

    @pytest.mark.slow
    def test_suspicious_text_higher_score(self) -> None:
        score, _, auth, urgency, _ = tech_analysis(SUSPICIOUS_TEXT)
        assert score > 0.0
        assert len(auth) > 0 or len(urgency) > 0

    @pytest.mark.slow
    def test_emotional_text_detects_emotion_hits(self) -> None:
        _, _, _, _, emotion = tech_analysis(EMOTIONAL_TEXT)
        assert len(emotion) > 0

    @pytest.mark.slow
    def test_emotional_text_scores_higher_than_benign(self) -> None:
        benign_score, _, _, _, _ = tech_analysis(BENIGN_TEXT)
        emotional_score, _, _, _, _ = tech_analysis(EMOTIONAL_TEXT)
        assert emotional_score > benign_score

    @pytest.mark.slow
    def test_contrast_scores_higher_than_single_pole(self) -> None:
        fear_only = "Doom and catastrophe and destruction await all of humanity."
        both = "Doom and catastrophe await, but salvation and bliss come to the chosen ones."
        fear_score, _, _, _, _ = tech_analysis(fear_only)
        both_score, _, _, _, _ = tech_analysis(both)
        assert both_score > fear_score

    @pytest.mark.slow
    def test_benign_text_no_emotion_hits(self) -> None:
        _, _, _, _, emotion = tech_analysis(BENIGN_TEXT)
        assert emotion == []

    @pytest.mark.slow
    def test_earth_polarity_detected(self) -> None:
        text = "The old earth is crumbling. Welcome to the new earth of light."
        _, _, _, _, emotion = tech_analysis(text)
        assert "old earth" in emotion
        assert "new earth" in emotion


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

    @pytest.mark.slow
    def test_emotion_hits_populated(self) -> None:
        result = hybrid_score(EMOTIONAL_TEXT, seed=42)
        assert len(result.emotion_hits) > 0

    @pytest.mark.slow
    def test_emotion_hits_empty_for_benign(self) -> None:
        result = hybrid_score(BENIGN_TEXT, seed=42)
        assert result.emotion_hits == []


# --- CLI main ---


class TestMain:
    @pytest.mark.slow
    def test_analyses_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        sample = tmp_path / "sample.txt"
        sample.write_text(SUSPICIOUS_TEXT)
        monkeypatch.setattr("sys.argv", ["si-threat-filter", str(sample)])
        main()
        captured = capsys.readouterr()
        assert "Threat Analysis" in captured.out
        assert "Overall Threat Score" in captured.out

    def test_missing_file_exits(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("sys.argv", ["si-threat-filter", "nonexistent.txt"])
        with pytest.raises(SystemExit, match="1"):
            main()

    @pytest.mark.slow
    def test_analyses_emotional_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        sample = tmp_path / "emotional.txt"
        sample.write_text(EMOTIONAL_TEXT)
        monkeypatch.setattr("sys.argv", ["si-threat-filter", str(sample)])
        main()
        captured = capsys.readouterr()
        assert "Emotion triggers" in captured.out
