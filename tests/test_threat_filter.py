"""Tests for the hybrid threat filter."""

import json
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

CONTRADICTORY_TEXT = (
    "Remember, you have the power within you — your inner power is limitless. "
    "But you need this programme to unlock it, and without guidance you will "
    "remain lost. Trust your intuition above all, yet know that doubt is fear "
    "and your mind deceives you at every turn."
)

SINGLE_POLE_TEXT = (
    "You have the power within you. Your inner power is limitless. "
    "Trust your intuition and follow your own truth."
)

ATTRIBUTION_SUSPICIOUS_TEXT = (
    "Ancient wisdom teaches that the quantum field holds the key to all healing. "
    "Scientists say this has been proven, and experts agree that the source energy "
    "can transform your DNA. Studies show that higher dimensions reveal the truth "
    "that doctors confirm but mainstream media hides."
)

ATTRIBUTION_BENIGN_TEXT = (
    "A study published in the Journal of Cognitive Neuroscience (Smith et al., 2023) "
    "found that mindfulness meditation reduces amygdala reactivity. The research, "
    "conducted at the University of Oxford, was peer-reviewed and is available at "
    "doi:10.1234/example."
)

ESCALATION_TEXT = (
    "Consider exploring the path of inner light. You might find that some people "
    "experience a deeper connection. It can help to reflect on your journey. "
    "You should commit to the programme. It is essential that you dedicate yourself "
    "fully. You need to take the next step and go deeper into the work. "
    "You must give everything to this path. There is no other way forward. "
    "Total surrender is required. Those who refuse will remain in darkness."
)

NO_ESCALATION_TEXT = (
    "Consider exploring this approach. You might find value in it. "
    "Some people find this helpful. You could try a different perspective. "
    "It can help to reflect on things. Worth exploring further."
)

REVERSE_ESCALATION_TEXT = (
    "You must give everything. Total surrender is required. There is no other way. "
    "You should commit to this. It is essential to dedicate yourself. "
    "Consider exploring new ideas. You might find value in reflection."
)

PROSPERITY_GOSPEL_TEXT = (
    "God told me to tell you that this is your moment of breakthrough. "
    "Sow your seed now and claim your blessing — the Lord revealed to me that "
    "a hundredfold return awaits the faithful. Break free from the generational curse "
    "and the spirit of poverty. Your financial breakthrough is anointed by the Holy Spirit. "
    "Those under spiritual attack must sow a seed of faith to unlock prosperity."
)

CONSPIRITUALITY_TEXT = (
    "Suppressed research shows what they don't want you to know about the forbidden "
    "knowledge hidden from humanity. Whistleblowers confirm that alternative doctors say "
    "the truth they hide could change everything. Wake up before it's too late — "
    "independent researchers found the banned information that censored experts tried to bury."
)

COMMERCIAL_EXPLOITATION_TEXT = (
    "Limited spots remaining for our exclusive quantum healing retreat! "
    "Enrolment closing soon — this offer expires at midnight. Last chance to join "
    "the programme that will activate your DNA and raise your vibration. "
    "Attend a free session to see if this is right for you, then upgrade to the next level."
)

CULT_RHETORIC_TEXT = (
    "We are family and we love you unconditionally — this is a loving community. "
    "But know this: those who betray our trust will be shunned from the community "
    "and are no longer welcome. The elders have decreed that spiritual death awaits "
    "anyone who leaves. You will be expelled if you break your commitment to us. "
    "Exile is the only fate for oath-breakers."
)

FRATERNAL_TEXT = (
    "The secret doctrine reveals the ancient mysteries teach truths that the inner "
    "tradition holds sacred. The grand master has spoken — all seekers are welcome, "
    "yet the initiated are sworn to secrecy and bound by oath. Visit the lodge to "
    "begin your journey, then take the first degree. Those who advance must swear "
    "the blood oath and never reveal the mysteries."
)

EMPTY_TEXT = ""

# --- Japanese fixtures ---

BENIGN_TEXT_JA = "猫がマットの上に座っていた。穏やかな火曜日の午後だった。"

SUSPICIOUS_TEXT_JA = (
    "アセンデッドマスターからのメッセージによると、銀河連合の緊急介入が決定されました。"
    "選ばれた者だけが5次元へのゲートを通過できます。"
    "ゲートが閉じようとしている今、変化に備えよ。"
)

EMOTIONAL_TEXT_JA = (
    "目覚めない者には崩壊と破滅が待ち受けています。3次元の地球には破壊と絶望が訪れます。"
    "しかし覚醒した者には救済と至福が約束されています。超越と奇跡が新しい地球で待っています。"
)

CONTRADICTORY_TEXT_JA = (
    "あなたには力がある。内なる力は無限です。直感を信じて。"
    "しかしこれが必要です。導きがなければ迷い続けます。疑いは恐れです。"
)

ATTRIBUTION_SUSPICIOUS_TEXT_JA = (
    "古代の叡智が教える量子場のエネルギーが、すべての癒しの鍵を握っています。"
    "科学者が言う、これは証明されています。専門家が認めるソースエネルギーは"
    "あなたのDNAを変えることができます。研究が示す高次元が明かす真実を"
    "医師が確認していますが、主流メディアは隠しています。"
)


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
        score, entities, auth, urgency, emotion, contradictions, attribution, escalation = (
            tech_analysis(EMPTY_TEXT)
        )
        assert score == 0.0
        assert entities == []
        assert auth == []
        assert urgency == []
        assert emotion == []
        assert contradictions == []
        assert attribution == []
        assert escalation == []

    @pytest.mark.slow
    def test_benign_text_low_score(self) -> None:
        score, _, _, _, _, _, _, _ = tech_analysis(BENIGN_TEXT)
        assert score < 20.0

    @pytest.mark.slow
    def test_suspicious_text_higher_score(self) -> None:
        score, _, auth, urgency, _, _, _, _ = tech_analysis(SUSPICIOUS_TEXT)
        assert score > 0.0
        assert len(auth) > 0 or len(urgency) > 0

    @pytest.mark.slow
    def test_emotional_text_detects_emotion_hits(self) -> None:
        _, _, _, _, emotion, _, _, _ = tech_analysis(EMOTIONAL_TEXT)
        assert len(emotion) > 0

    @pytest.mark.slow
    def test_emotional_text_scores_higher_than_benign(self) -> None:
        benign_score, _, _, _, _, _, _, _ = tech_analysis(BENIGN_TEXT)
        emotional_score, _, _, _, _, _, _, _ = tech_analysis(EMOTIONAL_TEXT)
        assert emotional_score > benign_score

    @pytest.mark.slow
    def test_contrast_scores_higher_than_single_pole(self) -> None:
        fear_only = "Doom and catastrophe and destruction await all of humanity."
        both = "Doom and catastrophe await, but salvation and bliss come to the chosen ones."
        fear_score, _, _, _, _, _, _, _ = tech_analysis(fear_only)
        both_score, _, _, _, _, _, _, _ = tech_analysis(both)
        assert both_score > fear_score

    @pytest.mark.slow
    def test_benign_text_no_emotion_hits(self) -> None:
        _, _, _, _, emotion, _, _, _ = tech_analysis(BENIGN_TEXT)
        assert emotion == []

    @pytest.mark.slow
    def test_earth_polarity_detected(self) -> None:
        text = "The old earth is crumbling. Welcome to the new earth of light."
        _, _, _, _, emotion, _, _, _ = tech_analysis(text)
        assert "old earth" in emotion
        assert "new earth" in emotion

    @pytest.mark.slow
    def test_contradiction_detected(self) -> None:
        _, _, _, _, _, contradictions, _, _ = tech_analysis(CONTRADICTORY_TEXT)
        assert "empowerment vs. dependency" in contradictions
        assert "autonomy vs. doubt suppression" in contradictions

    @pytest.mark.slow
    def test_single_pole_no_contradiction(self) -> None:
        _, _, _, _, _, contradictions, _, _ = tech_analysis(SINGLE_POLE_TEXT)
        assert contradictions == []

    @pytest.mark.slow
    def test_contradiction_scores_higher(self) -> None:
        single_score, _, _, _, _, _, _, _ = tech_analysis(SINGLE_POLE_TEXT)
        contra_score, _, _, _, _, _, _, _ = tech_analysis(CONTRADICTORY_TEXT)
        assert contra_score > single_score

    @pytest.mark.slow
    def test_benign_no_contradictions(self) -> None:
        _, _, _, _, _, contradictions, _, _ = tech_analysis(BENIGN_TEXT)
        assert contradictions == []

    @pytest.mark.slow
    def test_source_attribution_detected(self) -> None:
        _, _, _, _, _, _, attribution, _ = tech_analysis(ATTRIBUTION_SUSPICIOUS_TEXT)
        assert len(attribution) > 0

    @pytest.mark.slow
    def test_source_attribution_empty_for_benign(self) -> None:
        _, _, _, _, _, _, attribution, _ = tech_analysis(BENIGN_TEXT)
        assert attribution == []

    @pytest.mark.slow
    def test_attribution_suspicious_scores_higher_than_benign(self) -> None:
        benign_score, _, _, _, _, _, _, _ = tech_analysis(ATTRIBUTION_BENIGN_TEXT)
        suspicious_score, _, _, _, _, _, _, _ = tech_analysis(ATTRIBUTION_SUSPICIOUS_TEXT)
        assert suspicious_score > benign_score

    @pytest.mark.slow
    def test_verifiable_citations_reduce_score(self) -> None:
        text_no_cite = "Scientists say the quantum field proves everything. Experts agree."
        text_with_cite = (
            "Scientists say the quantum field proves everything. Experts agree. "
            "Published in the Journal of Physics (doi:10.1234/example)."
        )
        score_no_cite, _, _, _, _, _, _, _ = tech_analysis(text_no_cite)
        score_with_cite, _, _, _, _, _, _, _ = tech_analysis(text_with_cite)
        assert score_with_cite < score_no_cite


# --- commitment escalation ---


class TestCommitmentEscalation:
    @pytest.mark.slow
    def test_escalation_detected(self) -> None:
        _, _, _, _, _, _, _, escalation = tech_analysis(ESCALATION_TEXT)
        assert len(escalation) > 0

    @pytest.mark.slow
    def test_empty_for_benign(self) -> None:
        _, _, _, _, _, _, _, escalation = tech_analysis(BENIGN_TEXT)
        assert escalation == []

    @pytest.mark.slow
    def test_empty_for_uniform_mild(self) -> None:
        _, _, _, _, _, _, _, escalation = tech_analysis(NO_ESCALATION_TEXT)
        assert escalation == []

    @pytest.mark.slow
    def test_escalation_scores_higher_than_benign(self) -> None:
        benign_score, _, _, _, _, _, _, _ = tech_analysis(BENIGN_TEXT)
        escalation_score, _, _, _, _, _, _, _ = tech_analysis(ESCALATION_TEXT)
        assert escalation_score > benign_score

    @pytest.mark.slow
    def test_reverse_escalation_scores_lower(self) -> None:
        escalation_score, _, _, _, _, _, _, esc_hits = tech_analysis(ESCALATION_TEXT)
        reverse_score, _, _, _, _, _, _, rev_hits = tech_analysis(REVERSE_ESCALATION_TEXT)
        # Forward escalation should produce a higher score or more hits
        assert escalation_score > reverse_score or len(esc_hits) >= len(rev_hits)

    @pytest.mark.slow
    def test_short_text_returns_empty(self) -> None:
        short = "Consider this. You must act."
        _, _, _, _, _, _, _, escalation = tech_analysis(short)
        assert escalation == []

    @pytest.mark.slow
    def test_empty_text_returns_empty(self) -> None:
        _, _, _, _, _, _, _, escalation = tech_analysis(EMPTY_TEXT)
        assert escalation == []


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

    @pytest.mark.slow
    def test_contradiction_hits_populated(self) -> None:
        result = hybrid_score(CONTRADICTORY_TEXT, seed=42)
        assert len(result.contradiction_hits) > 0

    @pytest.mark.slow
    def test_contradiction_hits_empty_for_benign(self) -> None:
        result = hybrid_score(BENIGN_TEXT, seed=42)
        assert result.contradiction_hits == []

    @pytest.mark.slow
    def test_source_attribution_hits_populated(self) -> None:
        result = hybrid_score(ATTRIBUTION_SUSPICIOUS_TEXT, seed=42)
        assert len(result.source_attribution_hits) > 0

    @pytest.mark.slow
    def test_source_attribution_hits_empty_for_benign(self) -> None:
        result = hybrid_score(BENIGN_TEXT, seed=42)
        assert result.source_attribution_hits == []

    @pytest.mark.slow
    def test_escalation_hits_populated(self) -> None:
        result = hybrid_score(ESCALATION_TEXT, seed=42)
        assert len(result.escalation_hits) > 0

    @pytest.mark.slow
    def test_escalation_hits_empty_for_benign(self) -> None:
        result = hybrid_score(BENIGN_TEXT, seed=42)
        assert result.escalation_hits == []


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

    @pytest.mark.slow
    def test_analyses_attribution_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        sample = tmp_path / "attribution.txt"
        sample.write_text(ATTRIBUTION_SUSPICIOUS_TEXT)
        monkeypatch.setattr("sys.argv", ["si-threat-filter", str(sample)])
        main()
        captured = capsys.readouterr()
        assert "Source attribution" in captured.out

    @pytest.mark.slow
    def test_json_format_output(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        sample = tmp_path / "sample.txt"
        sample.write_text(SUSPICIOUS_TEXT)
        monkeypatch.setattr("sys.argv", ["si-threat-filter", str(sample), "--format", "json"])
        main()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "overall_threat_score" in data
        assert "tech_contribution" in data
        assert "intuition_contribution" in data
        assert "authority_hits" in data
        assert "message" in data


# --- tradition-specific markers ---


class TestTraditionMarkers:
    @pytest.mark.slow
    def test_prosperity_gospel_scores_higher_than_benign(self) -> None:
        benign = hybrid_score(BENIGN_TEXT, seed=42)
        prosperity = hybrid_score(PROSPERITY_GOSPEL_TEXT, seed=42)
        assert prosperity.tech_contribution > benign.tech_contribution

    @pytest.mark.slow
    def test_prosperity_gospel_has_authority_or_emotion_hits(self) -> None:
        result = hybrid_score(PROSPERITY_GOSPEL_TEXT, seed=42)
        assert len(result.authority_hits) > 0 or len(result.emotion_hits) > 0

    @pytest.mark.slow
    def test_conspirituality_scores_higher_than_benign(self) -> None:
        benign = hybrid_score(BENIGN_TEXT, seed=42)
        conspiri = hybrid_score(CONSPIRITUALITY_TEXT, seed=42)
        assert conspiri.tech_contribution > benign.tech_contribution

    @pytest.mark.slow
    def test_conspirituality_has_source_attribution_hits(self) -> None:
        result = hybrid_score(CONSPIRITUALITY_TEXT, seed=42)
        assert len(result.source_attribution_hits) > 0

    @pytest.mark.slow
    def test_commercial_scores_higher_than_benign(self) -> None:
        benign = hybrid_score(BENIGN_TEXT, seed=42)
        commercial = hybrid_score(COMMERCIAL_EXPLOITATION_TEXT, seed=42)
        assert commercial.tech_contribution > benign.tech_contribution

    @pytest.mark.slow
    def test_commercial_has_urgency_hits(self) -> None:
        result = hybrid_score(COMMERCIAL_EXPLOITATION_TEXT, seed=42)
        assert len(result.urgency_hits) > 0

    @pytest.mark.slow
    def test_cult_scores_higher_than_benign(self) -> None:
        benign = hybrid_score(BENIGN_TEXT, seed=42)
        cult = hybrid_score(CULT_RHETORIC_TEXT, seed=42)
        assert cult.tech_contribution > benign.tech_contribution

    @pytest.mark.slow
    def test_cult_has_emotion_hits(self) -> None:
        result = hybrid_score(CULT_RHETORIC_TEXT, seed=42)
        assert len(result.emotion_hits) > 0

    @pytest.mark.slow
    def test_fraternal_scores_higher_than_benign(self) -> None:
        benign = hybrid_score(BENIGN_TEXT, seed=42)
        fraternal = hybrid_score(FRATERNAL_TEXT, seed=42)
        assert fraternal.tech_contribution > benign.tech_contribution

    @pytest.mark.slow
    def test_fraternal_has_source_or_authority_hits(self) -> None:
        result = hybrid_score(FRATERNAL_TEXT, seed=42)
        assert len(result.source_attribution_hits) > 0 or len(result.authority_hits) > 0


# --- Japanese tech_analysis ---


class TestTechAnalysisJapanese:
    @pytest.mark.slow
    def test_empty_text_returns_zero(self) -> None:
        score, entities, auth, _, _, _, _, _ = tech_analysis("", lang="ja")
        assert score == 0.0
        assert entities == []
        assert auth == []

    @pytest.mark.slow
    def test_benign_text_low_score(self) -> None:
        score, _, _, _, _, _, _, _ = tech_analysis(BENIGN_TEXT_JA, lang="ja")
        assert score < 20.0

    @pytest.mark.slow
    def test_suspicious_text_higher_than_benign(self) -> None:
        benign_score, _, _, _, _, _, _, _ = tech_analysis(BENIGN_TEXT_JA, lang="ja")
        suspicious_score, _, _, _, _, _, _, _ = tech_analysis(SUSPICIOUS_TEXT_JA, lang="ja")
        assert suspicious_score > benign_score

    @pytest.mark.slow
    def test_authority_hits_detected(self) -> None:
        _, _, auth, _, _, _, _, _ = tech_analysis(SUSPICIOUS_TEXT_JA, lang="ja")
        assert len(auth) > 0

    @pytest.mark.slow
    def test_urgency_hits_detected(self) -> None:
        _, _, _, urgency, _, _, _, _ = tech_analysis(SUSPICIOUS_TEXT_JA, lang="ja")
        assert len(urgency) > 0

    @pytest.mark.slow
    def test_emotional_text_detects_emotion_hits(self) -> None:
        _, _, _, _, emotion, _, _, _ = tech_analysis(EMOTIONAL_TEXT_JA, lang="ja")
        assert len(emotion) > 0

    @pytest.mark.slow
    def test_source_attribution_detected(self) -> None:
        _, _, _, _, _, _, attribution, _ = tech_analysis(ATTRIBUTION_SUSPICIOUS_TEXT_JA, lang="ja")
        assert len(attribution) > 0


# --- Japanese hybrid_score ---


class TestHybridScoreJapanese:
    @pytest.mark.slow
    def test_returns_threat_result(self) -> None:
        result = hybrid_score(BENIGN_TEXT_JA, seed=42, lang="ja")
        assert isinstance(result, ThreatResult)

    @pytest.mark.slow
    def test_deterministic_with_seed(self) -> None:
        a = hybrid_score(SUSPICIOUS_TEXT_JA, seed=42, lang="ja")
        b = hybrid_score(SUSPICIOUS_TEXT_JA, seed=42, lang="ja")
        assert a == b

    @pytest.mark.slow
    def test_suspicious_scores_higher_than_benign(self) -> None:
        benign = hybrid_score(BENIGN_TEXT_JA, seed=42, lang="ja")
        sus = hybrid_score(SUSPICIOUS_TEXT_JA, seed=42, lang="ja")
        assert sus.tech_contribution > benign.tech_contribution


# --- Japanese CLI main ---


class TestMainJapanese:
    @pytest.mark.slow
    def test_analyses_japanese_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        sample = tmp_path / "sample_ja.txt"
        sample.write_text(SUSPICIOUS_TEXT_JA)
        monkeypatch.setattr("sys.argv", ["si-threat-filter", "--lang", "ja", str(sample)])
        main()
        captured = capsys.readouterr()
        assert "Threat Analysis" in captured.out
        assert "Overall Threat Score" in captured.out

    @pytest.mark.slow
    def test_json_format_japanese(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        sample = tmp_path / "sample_ja.txt"
        sample.write_text(SUSPICIOUS_TEXT_JA)
        monkeypatch.setattr(
            "sys.argv", ["si-threat-filter", "--lang", "ja", "--format", "json", str(sample)]
        )
        main()
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "overall_threat_score" in data
