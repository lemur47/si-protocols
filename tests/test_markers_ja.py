"""Tests for Japanese disinformation marker definitions."""

from si_protocols.markers_ja import (
    AUTHORITY_PHRASES,
    COMMITMENT_ESCALATION_MARKERS,
    CONTRADICTION_PAIRS,
    EUPHORIA_PHRASES,
    EUPHORIA_WORDS,
    FEAR_PHRASES,
    FEAR_WORDS,
    UNFALSIFIABLE_SOURCE_PHRASES,
    UNNAMED_AUTHORITY_PHRASES,
    URGENCY_PATTERNS,
    VAGUE_ADJECTIVES,
    VERIFIABLE_CITATION_MARKERS,
)


class TestVagueAdjectives:
    def test_is_frozenset(self) -> None:
        assert isinstance(VAGUE_ADJECTIVES, frozenset)

    def test_not_empty(self) -> None:
        assert len(VAGUE_ADJECTIVES) > 0

    def test_contains_known_markers(self) -> None:
        expected = {"神聖", "宇宙の", "永遠", "神秘の"}
        assert expected.issubset(VAGUE_ADJECTIVES)


class TestAuthorityPhrases:
    def test_not_empty(self) -> None:
        assert len(AUTHORITY_PHRASES) > 0

    def test_contains_key_phrases(self) -> None:
        assert "アセンデッドマスターからのメッセージによると" in AUTHORITY_PHRASES
        assert "アカシックレコードからダウンロードした情報によると" in AUTHORITY_PHRASES


class TestUrgencyPatterns:
    def test_not_empty(self) -> None:
        assert len(URGENCY_PATTERNS) > 0

    def test_contains_key_phrases(self) -> None:
        assert "今すぐ行動しなければ" in URGENCY_PATTERNS
        assert "残りわずか" in URGENCY_PATTERNS


class TestFearWords:
    def test_is_frozenset(self) -> None:
        assert isinstance(FEAR_WORDS, frozenset)

    def test_not_empty(self) -> None:
        assert len(FEAR_WORDS) > 0

    def test_contains_known_markers(self) -> None:
        expected = {"破滅", "崩壊", "絶望", "呪い"}
        assert expected.issubset(FEAR_WORDS)

    def test_no_overlap_with_euphoria(self) -> None:
        overlap = FEAR_WORDS & EUPHORIA_WORDS
        assert overlap == frozenset(), f"Fear/euphoria overlap: {overlap}"


class TestFearPhrases:
    def test_not_empty(self) -> None:
        assert len(FEAR_PHRASES) > 0

    def test_contains_key_phrases(self) -> None:
        assert "古い地球" in FEAR_PHRASES
        assert "世代の呪い" in FEAR_PHRASES


class TestEuphoriaWords:
    def test_is_frozenset(self) -> None:
        assert isinstance(EUPHORIA_WORDS, frozenset)

    def test_not_empty(self) -> None:
        assert len(EUPHORIA_WORDS) > 0

    def test_contains_known_markers(self) -> None:
        expected = {"至福", "覚醒", "奇跡", "救済", "繁栄"}
        assert expected.issubset(EUPHORIA_WORDS)

    def test_no_overlap_with_fear(self) -> None:
        overlap = EUPHORIA_WORDS & FEAR_WORDS
        assert overlap == frozenset(), f"Euphoria/fear overlap: {overlap}"


class TestEuphoriaPhrases:
    def test_not_empty(self) -> None:
        assert len(EUPHORIA_PHRASES) > 0

    def test_contains_key_phrases(self) -> None:
        assert "新しい地球" in EUPHORIA_PHRASES
        assert "量子ヒーリング" in EUPHORIA_PHRASES


class TestContradictionPairs:
    def test_is_list_of_3_tuples(self) -> None:
        assert isinstance(CONTRADICTION_PAIRS, list)
        for entry in CONTRADICTION_PAIRS:
            assert isinstance(entry, tuple)
            assert len(entry) == 3

    def test_labels_and_poles_non_empty(self) -> None:
        for label, pole_a, pole_b in CONTRADICTION_PAIRS:
            assert label, "Label must not be empty"
            assert len(pole_a) > 0, f"Pole A empty for '{label}'"
            assert len(pole_b) > 0, f"Pole B empty for '{label}'"

    def test_no_pattern_in_both_poles(self) -> None:
        for label, pole_a, pole_b in CONTRADICTION_PAIRS:
            overlap = set(pole_a) & set(pole_b)
            assert overlap == set(), f"Overlap in '{label}': {overlap}"


class TestUnfalsifiableSourcePhrases:
    def test_is_list(self) -> None:
        assert isinstance(UNFALSIFIABLE_SOURCE_PHRASES, list)

    def test_not_empty(self) -> None:
        assert len(UNFALSIFIABLE_SOURCE_PHRASES) > 0

    def test_no_overlap_with_authority_phrases(self) -> None:
        overlap = set(UNFALSIFIABLE_SOURCE_PHRASES) & set(AUTHORITY_PHRASES)
        assert overlap == set(), f"Overlap with AUTHORITY_PHRASES: {overlap}"


class TestUnnamedAuthorityPhrases:
    def test_is_list(self) -> None:
        assert isinstance(UNNAMED_AUTHORITY_PHRASES, list)

    def test_not_empty(self) -> None:
        assert len(UNNAMED_AUTHORITY_PHRASES) > 0

    def test_no_overlap_with_authority_phrases(self) -> None:
        overlap = set(UNNAMED_AUTHORITY_PHRASES) & set(AUTHORITY_PHRASES)
        assert overlap == set(), f"Overlap with AUTHORITY_PHRASES: {overlap}"

    def test_no_overlap_with_unfalsifiable(self) -> None:
        overlap = set(UNNAMED_AUTHORITY_PHRASES) & set(UNFALSIFIABLE_SOURCE_PHRASES)
        assert overlap == set(), f"Overlap with UNFALSIFIABLE_SOURCE_PHRASES: {overlap}"


class TestVerifiableCitationMarkers:
    def test_is_list(self) -> None:
        assert isinstance(VERIFIABLE_CITATION_MARKERS, list)

    def test_not_empty(self) -> None:
        assert len(VERIFIABLE_CITATION_MARKERS) > 0


class TestCommitmentEscalationMarkers:
    def test_is_list_of_2_tuples(self) -> None:
        assert isinstance(COMMITMENT_ESCALATION_MARKERS, list)
        for entry in COMMITMENT_ESCALATION_MARKERS:
            assert isinstance(entry, tuple)
            assert len(entry) == 2

    def test_tiers_are_positive_integers(self) -> None:
        for tier, _ in COMMITMENT_ESCALATION_MARKERS:
            assert isinstance(tier, int)
            assert tier > 0

    def test_tiers_in_ascending_order(self) -> None:
        tiers = [tier for tier, _ in COMMITMENT_ESCALATION_MARKERS]
        assert tiers == sorted(tiers), "Tiers must be in ascending order"

    def test_each_tier_non_empty(self) -> None:
        for tier, phrases in COMMITMENT_ESCALATION_MARKERS:
            assert len(phrases) > 0, f"Tier {tier} must have at least one phrase"

    def test_no_duplicate_phrases_across_tiers(self) -> None:
        all_phrases: list[str] = []
        for _, phrases in COMMITMENT_ESCALATION_MARKERS:
            all_phrases.extend(phrases)
        assert len(all_phrases) == len(set(all_phrases)), "Duplicate phrases found across tiers"
