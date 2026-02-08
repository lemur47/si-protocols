"""Tests for disinformation marker definitions."""

from si_protocols.markers import AUTHORITY_PHRASES, URGENCY_PATTERNS, VAGUE_ADJECTIVES


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
