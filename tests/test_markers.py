"""Tests for disinformation marker definitions."""

from si_protocols.markers import (
    AUTHORITY_PHRASES,
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
        expected = {"ancient", "cosmic", "divine", "hidden", "secret"}
        assert expected.issubset(VAGUE_ADJECTIVES)


class TestAuthorityPhrases:
    def test_not_empty(self) -> None:
        assert len(AUTHORITY_PHRASES) > 0

    def test_all_lowercase(self) -> None:
        for phrase in AUTHORITY_PHRASES:
            assert phrase == phrase.lower(), f"Phrase '{phrase}' should be lowercase"


class TestUrgencyPatterns:
    def test_not_empty(self) -> None:
        assert len(URGENCY_PATTERNS) > 0

    def test_all_lowercase(self) -> None:
        for pattern in URGENCY_PATTERNS:
            assert pattern == pattern.lower(), f"Pattern '{pattern}' should be lowercase"


class TestFearWords:
    def test_is_frozenset(self) -> None:
        assert isinstance(FEAR_WORDS, frozenset)

    def test_all_lowercase(self) -> None:
        for word in FEAR_WORDS:
            assert word == word.lower(), f"Marker '{word}' should be lowercase"

    def test_not_empty(self) -> None:
        assert len(FEAR_WORDS) > 0

    def test_contains_known_markers(self) -> None:
        expected = {"doom", "catastrophe", "destruction", "despair", "wrath"}
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


class TestEuphoriaWords:
    def test_is_frozenset(self) -> None:
        assert isinstance(EUPHORIA_WORDS, frozenset)

    def test_all_lowercase(self) -> None:
        for word in EUPHORIA_WORDS:
            assert word == word.lower(), f"Marker '{word}' should be lowercase"

    def test_not_empty(self) -> None:
        assert len(EUPHORIA_WORDS) > 0

    def test_contains_known_markers(self) -> None:
        expected = {"bliss", "paradise", "miracle", "salvation", "rapture"}
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


class TestVerifiableCitationMarkers:
    def test_is_list(self) -> None:
        assert isinstance(VERIFIABLE_CITATION_MARKERS, list)

    def test_not_empty(self) -> None:
        assert len(VERIFIABLE_CITATION_MARKERS) > 0

    def test_all_lowercase(self) -> None:
        for marker in VERIFIABLE_CITATION_MARKERS:
            assert marker == marker.lower(), f"Marker '{marker}' should be lowercase"
