"""Tests for disinformation marker definitions."""

from si_protocols.markers import (
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

    def test_all_lowercase(self) -> None:
        for adj in VAGUE_ADJECTIVES:
            assert adj == adj.lower(), f"Marker '{adj}' should be lowercase"

    def test_contains_known_markers(self) -> None:
        expected = {"ancient", "cosmic", "divine", "hidden", "secret", "anointed"}
        assert expected.issubset(VAGUE_ADJECTIVES)


class TestAuthorityPhrases:
    def test_not_empty(self) -> None:
        assert len(AUTHORITY_PHRASES) > 0

    def test_all_lowercase(self) -> None:
        for phrase in AUTHORITY_PHRASES:
            assert phrase == phrase.lower(), f"Phrase '{phrase}' should be lowercase"

    def test_contains_tradition_phrases(self) -> None:
        assert "god told me to tell you" in AUTHORITY_PHRASES
        assert "the elders have decreed" in AUTHORITY_PHRASES
        assert "the grand master has spoken" in AUTHORITY_PHRASES


class TestUrgencyPatterns:
    def test_not_empty(self) -> None:
        assert len(URGENCY_PATTERNS) > 0

    def test_all_lowercase(self) -> None:
        for pattern in URGENCY_PATTERNS:
            assert pattern == pattern.lower(), f"Pattern '{pattern}' should be lowercase"

    def test_contains_tradition_phrases(self) -> None:
        assert "sow your seed now" in URGENCY_PATTERNS
        assert "limited spots remaining" in URGENCY_PATTERNS
        assert "wake up before it's too late" in URGENCY_PATTERNS


class TestFearWords:
    def test_is_frozenset(self) -> None:
        assert isinstance(FEAR_WORDS, frozenset)

    def test_all_lowercase(self) -> None:
        for word in FEAR_WORDS:
            assert word == word.lower(), f"Marker '{word}' should be lowercase"

    def test_not_empty(self) -> None:
        assert len(FEAR_WORDS) > 0

    def test_contains_known_markers(self) -> None:
        expected = {"doom", "catastrophe", "destruction", "despair", "wrath", "curse"}
        assert expected.issubset(FEAR_WORDS)

    def test_no_overlap_with_euphoria(self) -> None:
        overlap = FEAR_WORDS & EUPHORIA_WORDS
        assert overlap == frozenset(), f"Fear/euphoria overlap: {overlap}"


class TestFearPhrases:
    def test_not_empty(self) -> None:
        assert len(FEAR_PHRASES) > 0

    def test_all_lowercase(self) -> None:
        for phrase in FEAR_PHRASES:
            assert phrase == phrase.lower(), f"Phrase '{phrase}' should be lowercase"

    def test_contains_old_earth(self) -> None:
        assert "old earth" in FEAR_PHRASES

    def test_contains_tradition_phrases(self) -> None:
        assert "generational curse" in FEAR_PHRASES
        assert "spiritual death" in FEAR_PHRASES
        assert "expelled from the order" in FEAR_PHRASES


class TestEuphoriaWords:
    def test_is_frozenset(self) -> None:
        assert isinstance(EUPHORIA_WORDS, frozenset)

    def test_all_lowercase(self) -> None:
        for word in EUPHORIA_WORDS:
            assert word == word.lower(), f"Marker '{word}' should be lowercase"

    def test_not_empty(self) -> None:
        assert len(EUPHORIA_WORDS) > 0

    def test_contains_known_markers(self) -> None:
        expected = {"bliss", "paradise", "miracle", "salvation", "rapture", "prosperity"}
        assert expected.issubset(EUPHORIA_WORDS)

    def test_no_overlap_with_fear(self) -> None:
        overlap = EUPHORIA_WORDS & FEAR_WORDS
        assert overlap == frozenset(), f"Euphoria/fear overlap: {overlap}"


class TestEuphoriaPhrases:
    def test_not_empty(self) -> None:
        assert len(EUPHORIA_PHRASES) > 0

    def test_all_lowercase(self) -> None:
        for phrase in EUPHORIA_PHRASES:
            assert phrase == phrase.lower(), f"Phrase '{phrase}' should be lowercase"

    def test_contains_new_earth(self) -> None:
        assert "new earth" in EUPHORIA_PHRASES

    def test_contains_tradition_phrases(self) -> None:
        assert "financial breakthrough" in EUPHORIA_PHRASES
        assert "quantum healing" in EUPHORIA_PHRASES
        assert "raise your vibration" in EUPHORIA_PHRASES


class TestContradictionPairs:
    def test_is_list_of_3_tuples(self) -> None:
        assert isinstance(CONTRADICTION_PAIRS, list)
        for entry in CONTRADICTION_PAIRS:
            assert isinstance(entry, tuple)
            assert len(entry) == 3

    def test_all_patterns_lowercase(self) -> None:
        for _label, pole_a, pole_b in CONTRADICTION_PAIRS:
            for pattern in pole_a:
                assert pattern == pattern.lower(), f"Pole A pattern '{pattern}' not lowercase"
            for pattern in pole_b:
                assert pattern == pattern.lower(), f"Pole B pattern '{pattern}' not lowercase"

    def test_labels_and_poles_non_empty(self) -> None:
        for label, pole_a, pole_b in CONTRADICTION_PAIRS:
            assert label, "Label must not be empty"
            assert len(pole_a) > 0, f"Pole A empty for '{label}'"
            assert len(pole_b) > 0, f"Pole B empty for '{label}'"

    def test_no_pattern_in_both_poles(self) -> None:
        for label, pole_a, pole_b in CONTRADICTION_PAIRS:
            overlap = set(pole_a) & set(pole_b)
            assert overlap == set(), f"Overlap in '{label}': {overlap}"

    def test_contains_tradition_pairs(self) -> None:
        labels = [label for label, _, _ in CONTRADICTION_PAIRS]
        assert "poverty virtue vs. prosperity promise" in labels
        assert "community love vs. shunning" in labels
        assert "openness vs. sworn secrecy" in labels


class TestUnfalsifiableSourcePhrases:
    def test_is_list(self) -> None:
        assert isinstance(UNFALSIFIABLE_SOURCE_PHRASES, list)

    def test_not_empty(self) -> None:
        assert len(UNFALSIFIABLE_SOURCE_PHRASES) > 0

    def test_all_lowercase(self) -> None:
        for phrase in UNFALSIFIABLE_SOURCE_PHRASES:
            assert phrase == phrase.lower(), f"Phrase '{phrase}' should be lowercase"

    def test_no_overlap_with_authority_phrases(self) -> None:
        overlap = set(UNFALSIFIABLE_SOURCE_PHRASES) & set(AUTHORITY_PHRASES)
        assert overlap == set(), f"Overlap with AUTHORITY_PHRASES: {overlap}"

    def test_contains_tradition_phrases(self) -> None:
        assert "suppressed research shows" in UNFALSIFIABLE_SOURCE_PHRASES
        assert "forbidden knowledge" in UNFALSIFIABLE_SOURCE_PHRASES
        assert "the secret doctrine reveals" in UNFALSIFIABLE_SOURCE_PHRASES


class TestUnnamedAuthorityPhrases:
    def test_is_list(self) -> None:
        assert isinstance(UNNAMED_AUTHORITY_PHRASES, list)

    def test_not_empty(self) -> None:
        assert len(UNNAMED_AUTHORITY_PHRASES) > 0

    def test_all_lowercase(self) -> None:
        for phrase in UNNAMED_AUTHORITY_PHRASES:
            assert phrase == phrase.lower(), f"Phrase '{phrase}' should be lowercase"

    def test_no_overlap_with_authority_phrases(self) -> None:
        overlap = set(UNNAMED_AUTHORITY_PHRASES) & set(AUTHORITY_PHRASES)
        assert overlap == set(), f"Overlap with AUTHORITY_PHRASES: {overlap}"

    def test_no_overlap_with_unfalsifiable(self) -> None:
        overlap = set(UNNAMED_AUTHORITY_PHRASES) & set(UNFALSIFIABLE_SOURCE_PHRASES)
        assert overlap == set(), f"Overlap with UNFALSIFIABLE_SOURCE_PHRASES: {overlap}"

    def test_contains_tradition_phrases(self) -> None:
        assert "whistleblowers confirm" in UNNAMED_AUTHORITY_PHRASES
        assert "alternative doctors say" in UNNAMED_AUTHORITY_PHRASES
        assert "censored experts" in UNNAMED_AUTHORITY_PHRASES


class TestVerifiableCitationMarkers:
    def test_is_list(self) -> None:
        assert isinstance(VERIFIABLE_CITATION_MARKERS, list)

    def test_not_empty(self) -> None:
        assert len(VERIFIABLE_CITATION_MARKERS) > 0

    def test_all_lowercase(self) -> None:
        for marker in VERIFIABLE_CITATION_MARKERS:
            assert marker == marker.lower(), f"Marker '{marker}' should be lowercase"


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

    def test_all_phrases_lowercase(self) -> None:
        for tier, phrases in COMMITMENT_ESCALATION_MARKERS:
            for phrase in phrases:
                assert phrase == phrase.lower(), (
                    f"Tier {tier} phrase '{phrase}' should be lowercase"
                )

    def test_each_tier_non_empty(self) -> None:
        for tier, phrases in COMMITMENT_ESCALATION_MARKERS:
            assert len(phrases) > 0, f"Tier {tier} must have at least one phrase"

    def test_no_duplicate_phrases_across_tiers(self) -> None:
        all_phrases: list[str] = []
        for _, phrases in COMMITMENT_ESCALATION_MARKERS:
            all_phrases.extend(phrases)
        assert len(all_phrases) == len(set(all_phrases)), "Duplicate phrases found across tiers"

    def test_escalation_tradition_phrases(self) -> None:
        tier_phrases: dict[int, list[str]] = {}
        for tier, phrases in COMMITMENT_ESCALATION_MARKERS:
            tier_phrases[tier] = phrases
        assert "attend a free session" in tier_phrases[1]
        assert "visit the lodge" in tier_phrases[1]
        assert "sow a seed of faith" in tier_phrases[2]
        assert "upgrade to the next level" in tier_phrases[2]
        assert "take the first degree" in tier_phrases[2]
        assert "give your life savings" in tier_phrases[3]
        assert "swear the blood oath" in tier_phrases[3]
