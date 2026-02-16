"""Tests for the language-aware marker registry."""

import pytest

from si_protocols.marker_registry import MarkerSet, get_markers


class TestGetMarkersEnglish:
    def test_returns_marker_set(self) -> None:
        ms = get_markers("en")
        assert isinstance(ms, MarkerSet)

    def test_vague_adjectives_match_english_module(self) -> None:
        from si_protocols.markers import VAGUE_ADJECTIVES

        ms = get_markers("en")
        assert ms.vague_adjectives == VAGUE_ADJECTIVES

    def test_authority_phrases_match_english_module(self) -> None:
        from si_protocols.markers import AUTHORITY_PHRASES

        ms = get_markers("en")
        assert ms.authority_phrases == AUTHORITY_PHRASES

    def test_all_categories_populated(self) -> None:
        ms = get_markers("en")
        assert len(ms.vague_adjectives) > 0
        assert len(ms.authority_phrases) > 0
        assert len(ms.urgency_patterns) > 0
        assert len(ms.fear_words) > 0
        assert len(ms.fear_phrases) > 0
        assert len(ms.euphoria_words) > 0
        assert len(ms.euphoria_phrases) > 0
        assert len(ms.unfalsifiable_source_phrases) > 0
        assert len(ms.unnamed_authority_phrases) > 0
        assert len(ms.verifiable_citation_markers) > 0
        assert len(ms.commitment_escalation_markers) > 0
        assert len(ms.contradiction_pairs) > 0

    def test_is_frozen(self) -> None:
        ms = get_markers("en")
        with pytest.raises(AttributeError):
            ms.vague_adjectives = frozenset()  # type: ignore[misc]

    def test_cached(self) -> None:
        a = get_markers("en")
        b = get_markers("en")
        assert a is b


class TestGetMarkersUnsupported:
    def test_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unsupported language"):
            get_markers("fr")  # type: ignore[arg-type]

    def test_error_message_lists_supported(self) -> None:
        with pytest.raises(ValueError, match="en"):
            get_markers("zz")  # type: ignore[arg-type]


class TestGetMarkersJapanese:
    def test_returns_marker_set(self) -> None:
        ms = get_markers("ja")
        assert isinstance(ms, MarkerSet)

    def test_vague_adjectives_match_japanese_module(self) -> None:
        from si_protocols.markers_ja import VAGUE_ADJECTIVES

        ms = get_markers("ja")
        assert ms.vague_adjectives == VAGUE_ADJECTIVES

    def test_all_categories_populated(self) -> None:
        ms = get_markers("ja")
        assert len(ms.vague_adjectives) > 0
        assert len(ms.authority_phrases) > 0
        assert len(ms.urgency_patterns) > 0
        assert len(ms.fear_words) > 0
        assert len(ms.fear_phrases) > 0
        assert len(ms.euphoria_words) > 0
        assert len(ms.euphoria_phrases) > 0
        assert len(ms.unfalsifiable_source_phrases) > 0
        assert len(ms.unnamed_authority_phrases) > 0
        assert len(ms.verifiable_citation_markers) > 0
        assert len(ms.commitment_escalation_markers) > 0
        assert len(ms.contradiction_pairs) > 0

    def test_cached(self) -> None:
        a = get_markers("ja")
        b = get_markers("ja")
        assert a is b


class TestDefaultLang:
    def test_default_is_english(self) -> None:
        default = get_markers()
        english = get_markers("en")
        assert default is english
