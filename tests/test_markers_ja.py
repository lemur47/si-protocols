"""Tests for Japanese disinformation marker definitions."""

from si_protocols.markers_ja import (
    AUTHORITY_KEYWORD_GROUPS,
    AUTHORITY_PHRASES,
    COMMITMENT_ESCALATION_MARKERS,
    CONTRADICTION_KEYWORD_PAIRS,
    CONTRADICTION_PAIRS,
    ESCALATION_KEYWORD_MARKERS,
    EUPHORIA_PHRASES,
    EUPHORIA_WORDS,
    FEAR_PHRASES,
    FEAR_WORDS,
    UNFALSIFIABLE_KEYWORD_GROUPS,
    UNFALSIFIABLE_SOURCE_PHRASES,
    UNNAMED_AUTHORITY_KEYWORDS,
    UNNAMED_AUTHORITY_PHRASES,
    URGENCY_KEYWORDS,
    URGENCY_PATTERNS,
    VAGUE_ADJECTIVE_STEMS,
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


# --- Keyword-based matching data ---


class TestVagueAdjectiveStems:
    def test_is_frozenset(self) -> None:
        assert isinstance(VAGUE_ADJECTIVE_STEMS, frozenset)

    def test_not_empty(self) -> None:
        assert len(VAGUE_ADJECTIVE_STEMS) > 0

    def test_contains_known_stems(self) -> None:
        expected = {"神聖", "宇宙", "永遠", "神秘"}
        assert expected.issubset(VAGUE_ADJECTIVE_STEMS)


class TestAuthorityKeywordGroups:
    def test_is_list(self) -> None:
        assert isinstance(AUTHORITY_KEYWORD_GROUPS, list)

    def test_not_empty(self) -> None:
        assert len(AUTHORITY_KEYWORD_GROUPS) > 0

    def test_entries_are_label_keywords_tuples(self) -> None:
        for entry in AUTHORITY_KEYWORD_GROUPS:
            assert isinstance(entry, tuple)
            assert len(entry) == 2
            label, keywords = entry
            assert isinstance(label, str) and label
            assert isinstance(keywords, list) and len(keywords) > 0

    def test_no_duplicate_labels(self) -> None:
        labels = [label for label, _ in AUTHORITY_KEYWORD_GROUPS]
        assert len(labels) == len(set(labels)), "Duplicate labels"


class TestUrgencyKeywords:
    def test_is_list(self) -> None:
        assert isinstance(URGENCY_KEYWORDS, list)

    def test_not_empty(self) -> None:
        assert len(URGENCY_KEYWORDS) > 0

    def test_no_duplicates(self) -> None:
        assert len(URGENCY_KEYWORDS) == len(set(URGENCY_KEYWORDS))


class TestUnfalsifiableKeywordGroups:
    def test_is_list(self) -> None:
        assert isinstance(UNFALSIFIABLE_KEYWORD_GROUPS, list)

    def test_not_empty(self) -> None:
        assert len(UNFALSIFIABLE_KEYWORD_GROUPS) > 0

    def test_entries_are_label_keywords_tuples(self) -> None:
        for entry in UNFALSIFIABLE_KEYWORD_GROUPS:
            assert isinstance(entry, tuple)
            assert len(entry) == 2
            label, keywords = entry
            assert isinstance(label, str) and label
            assert isinstance(keywords, list) and len(keywords) > 0


class TestUnnamedAuthorityKeywords:
    def test_is_list(self) -> None:
        assert isinstance(UNNAMED_AUTHORITY_KEYWORDS, list)

    def test_not_empty(self) -> None:
        assert len(UNNAMED_AUTHORITY_KEYWORDS) > 0

    def test_no_duplicates(self) -> None:
        assert len(UNNAMED_AUTHORITY_KEYWORDS) == len(set(UNNAMED_AUTHORITY_KEYWORDS))


class TestContradictionKeywordPairs:
    def test_is_list(self) -> None:
        assert isinstance(CONTRADICTION_KEYWORD_PAIRS, list)

    def test_not_empty(self) -> None:
        assert len(CONTRADICTION_KEYWORD_PAIRS) > 0

    def test_entries_are_3_tuples(self) -> None:
        for entry in CONTRADICTION_KEYWORD_PAIRS:
            assert isinstance(entry, tuple)
            assert len(entry) == 3

    def test_labels_and_poles_non_empty(self) -> None:
        for label, pole_a, pole_b in CONTRADICTION_KEYWORD_PAIRS:
            assert label, "Label must not be empty"
            assert len(pole_a) > 0, f"Pole A empty for '{label}'"
            assert len(pole_b) > 0, f"Pole B empty for '{label}'"

    def test_no_keyword_in_both_poles(self) -> None:
        for label, pole_a, pole_b in CONTRADICTION_KEYWORD_PAIRS:
            overlap = set(pole_a) & set(pole_b)
            assert overlap == set(), f"Overlap in '{label}': {overlap}"


class TestEscalationKeywordMarkers:
    def test_is_list(self) -> None:
        assert isinstance(ESCALATION_KEYWORD_MARKERS, list)

    def test_not_empty(self) -> None:
        assert len(ESCALATION_KEYWORD_MARKERS) > 0

    def test_tiers_are_positive_integers(self) -> None:
        for tier, _ in ESCALATION_KEYWORD_MARKERS:
            assert isinstance(tier, int)
            assert tier > 0

    def test_tiers_in_ascending_order(self) -> None:
        tiers = [tier for tier, _ in ESCALATION_KEYWORD_MARKERS]
        assert tiers == sorted(tiers)

    def test_each_tier_non_empty(self) -> None:
        for tier, keywords in ESCALATION_KEYWORD_MARKERS:
            assert len(keywords) > 0, f"Tier {tier} must have at least one keyword"

    def test_no_duplicate_keywords_across_tiers(self) -> None:
        all_kws: list[str] = []
        for _, keywords in ESCALATION_KEYWORD_MARKERS:
            all_kws.extend(keywords)
        assert len(all_kws) == len(set(all_kws)), "Duplicate keywords across tiers"
