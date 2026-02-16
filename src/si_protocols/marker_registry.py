"""Language-aware marker registry for multi-language analysis.

Provides a ``MarkerSet`` frozen dataclass bundling all marker categories and
a ``get_markers(lang)`` dispatch function that loads the appropriate language
module on first access.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

SupportedLang = Literal["en", "ja"]

_SUPPORTED_LANGS: set[str] = {"en", "ja"}


@dataclass(frozen=True)
class MarkerSet:
    """Immutable bundle of all 12 marker categories for a single language."""

    vague_adjectives: frozenset[str]
    authority_phrases: list[str] = field(default_factory=list)
    urgency_patterns: list[str] = field(default_factory=list)
    fear_words: frozenset[str] = field(default_factory=frozenset)
    fear_phrases: list[str] = field(default_factory=list)
    euphoria_words: frozenset[str] = field(default_factory=frozenset)
    euphoria_phrases: list[str] = field(default_factory=list)
    unfalsifiable_source_phrases: list[str] = field(default_factory=list)
    unnamed_authority_phrases: list[str] = field(default_factory=list)
    verifiable_citation_markers: list[str] = field(default_factory=list)
    commitment_escalation_markers: list[tuple[int, list[str]]] = field(default_factory=list)
    contradiction_pairs: list[tuple[str, list[str], list[str]]] = field(default_factory=list)


# Cache loaded marker sets to avoid repeated imports
_cache: dict[str, MarkerSet] = {}


def _load_en() -> MarkerSet:
    """Build a MarkerSet from the existing English markers module."""
    from si_protocols import markers

    return MarkerSet(
        vague_adjectives=markers.VAGUE_ADJECTIVES,
        authority_phrases=markers.AUTHORITY_PHRASES,
        urgency_patterns=markers.URGENCY_PATTERNS,
        fear_words=markers.FEAR_WORDS,
        fear_phrases=markers.FEAR_PHRASES,
        euphoria_words=markers.EUPHORIA_WORDS,
        euphoria_phrases=markers.EUPHORIA_PHRASES,
        unfalsifiable_source_phrases=markers.UNFALSIFIABLE_SOURCE_PHRASES,
        unnamed_authority_phrases=markers.UNNAMED_AUTHORITY_PHRASES,
        verifiable_citation_markers=markers.VERIFIABLE_CITATION_MARKERS,
        commitment_escalation_markers=markers.COMMITMENT_ESCALATION_MARKERS,
        contradiction_pairs=markers.CONTRADICTION_PAIRS,
    )


def _load_ja() -> MarkerSet:
    """Build a MarkerSet from the Japanese markers module."""
    from si_protocols import markers_ja

    return MarkerSet(
        vague_adjectives=markers_ja.VAGUE_ADJECTIVES,
        authority_phrases=markers_ja.AUTHORITY_PHRASES,
        urgency_patterns=markers_ja.URGENCY_PATTERNS,
        fear_words=markers_ja.FEAR_WORDS,
        fear_phrases=markers_ja.FEAR_PHRASES,
        euphoria_words=markers_ja.EUPHORIA_WORDS,
        euphoria_phrases=markers_ja.EUPHORIA_PHRASES,
        unfalsifiable_source_phrases=markers_ja.UNFALSIFIABLE_SOURCE_PHRASES,
        unnamed_authority_phrases=markers_ja.UNNAMED_AUTHORITY_PHRASES,
        verifiable_citation_markers=markers_ja.VERIFIABLE_CITATION_MARKERS,
        commitment_escalation_markers=markers_ja.COMMITMENT_ESCALATION_MARKERS,
        contradiction_pairs=markers_ja.CONTRADICTION_PAIRS,
    )


_LOADERS: dict[str, callable] = {  # type: ignore[type-arg]
    "en": _load_en,
    "ja": _load_ja,
}


def get_markers(lang: SupportedLang = "en") -> MarkerSet:
    """Return the MarkerSet for the given language.

    Raises:
        ValueError: If ``lang`` is not a supported language code.
    """
    if lang not in _SUPPORTED_LANGS:
        msg = f"Unsupported language: {lang!r}. Supported: {sorted(_SUPPORTED_LANGS)}"
        raise ValueError(msg)
    if lang not in _cache:
        _cache[lang] = _LOADERS[lang]()
    return _cache[lang]
