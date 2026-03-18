"""si-protocols — Hybrid tech-psychic protocols for Spiritual Intelligence."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from si_protocols.marker_registry import MarkerSet, SupportedLang, get_markers
    from si_protocols.threat_filter import ThreatResult, hybrid_score, tech_analysis

__all__ = [
    "MarkerSet",
    "SupportedLang",
    "ThreatResult",
    "get_markers",
    "hybrid_score",
    "tech_analysis",
]

__version__ = "0.1.0"


def __getattr__(name: str) -> object:
    """Lazy imports to avoid loading spaCy at import time."""
    if name in {"hybrid_score", "tech_analysis", "ThreatResult"}:
        from si_protocols import threat_filter

        return getattr(threat_filter, name)
    if name in {"get_markers", "MarkerSet", "SupportedLang"}:
        from si_protocols import marker_registry

        return getattr(marker_registry, name)
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
