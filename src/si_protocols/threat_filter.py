"""Hybrid threat scorer: NLP tech layer + heuristic 'psychic' weighting.

Run locally on your own text files only. MIT Licence.
"""

from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import spacy

from si_protocols.marker_registry import SupportedLang, get_markers

if TYPE_CHECKING:
    from spacy.tokens import Doc, Span

# Lazy-load models to avoid import-time side effects in tests.
# Keyed by language code so each model is loaded at most once.
_nlp_cache: dict[str, spacy.language.Language] = {}

_LANG_MODELS: dict[str, str] = {
    "en": "en_core_web_sm",
    "ja": "ja_core_news_sm",
}


def _get_nlp(lang: SupportedLang = "en") -> spacy.language.Language:
    """Load spaCy model on first use for the given language."""
    if lang not in _nlp_cache:
        model = _LANG_MODELS[lang]
        _nlp_cache[lang] = spacy.load(model)
    return _nlp_cache[lang]


@dataclass(frozen=True)
class ThreatResult:
    """Structured output from hybrid threat analysis."""

    overall_threat_score: float
    tech_contribution: float
    intuition_contribution: float
    detected_entities: list[str] = field(default_factory=list)
    authority_hits: list[str] = field(default_factory=list)
    urgency_hits: list[str] = field(default_factory=list)
    emotion_hits: list[str] = field(default_factory=list)
    contradiction_hits: list[str] = field(default_factory=list)
    source_attribution_hits: list[str] = field(default_factory=list)
    escalation_hits: list[str] = field(default_factory=list)
    message: str = "Run on your own texts only — this is a local tool."


def _commitment_escalation(
    doc: Doc,
    escalation_markers: list[tuple[int, list[str]]],
) -> tuple[float, list[str]]:
    """Detect foot-in-the-door escalation across text segments.

    Splits sentences into thirds (early/middle/late) and measures whether
    commitment marker intensity increases from early to late.

    Returns (score 0-1, hit labels like ["early: consider", "late: you must"]).
    """
    sents = list(doc.sents)
    if len(sents) < 3:
        return 0.0, []

    # Build tier lookup: phrase -> tier value
    tier_lookup: dict[str, int] = {}
    for tier, phrases in escalation_markers:
        for phrase in phrases:
            tier_lookup[phrase] = tier

    # Split sentences into thirds
    third = len(sents) // 3
    segments: list[tuple[str, list[Span]]] = [
        ("early", sents[:third]),
        ("middle", sents[third : 2 * third]),
        ("late", sents[2 * third :]),
    ]

    # Score each segment: mean tier intensity of matched phrases
    segment_scores: dict[str, float] = {}
    segment_hits: dict[str, list[str]] = {}
    total_hits = 0
    for label, seg_sents in segments:
        seg_text = " ".join(s.text.lower() for s in seg_sents)
        hits: list[tuple[str, int]] = []
        for phrase, tier in tier_lookup.items():
            if phrase in seg_text:
                hits.append((phrase, tier))
        total_hits += len(hits)
        segment_scores[label] = sum(t for _, t in hits) / max(len(hits), 1) if hits else 0.0
        segment_hits[label] = [phrase for phrase, _ in hits]

    # Require at least 2 total marker hits to avoid false positives
    if total_hits < 2:
        return 0.0, []

    # Detect gradient: early→late (60%), early→mid (20%), mid→late (20%)
    max_tier = max(t for t, _ in escalation_markers)
    early_to_late = max(segment_scores["late"] - segment_scores["early"], 0.0) / max_tier
    early_to_mid = max(segment_scores["middle"] - segment_scores["early"], 0.0) / max_tier
    mid_to_late = max(segment_scores["late"] - segment_scores["middle"], 0.0) / max_tier

    raw_score = early_to_late * 0.6 + early_to_mid * 0.2 + mid_to_late * 0.2
    score = min(raw_score, 1.0)

    if score == 0.0:
        return 0.0, []

    # Build hit labels for non-empty segments
    hit_labels: list[str] = []
    for label, _seg_sents in segments:
        if segment_hits[label]:
            hit_labels.append(f"{label}: {', '.join(segment_hits[label])}")

    return score, hit_labels


def tech_analysis(
    text: str,
    *,
    lang: SupportedLang = "en",
) -> tuple[float, list[str], list[str], list[str], list[str], list[str], list[str], list[str]]:
    """Tech layer: NLP-based suspicion signals.

    Returns (score, entities, authority_hits, urgency_hits, emotion_hits,
    contradiction_hits, source_attribution_hits, escalation_hits).
    """
    if not text.strip():
        return 0.0, [], [], [], [], [], [], []

    nlp = _get_nlp(lang)
    doc = nlp(text)
    text_lower = text.lower()

    markers = get_markers(lang)

    entities = [ent.text for ent in doc.ents]

    # --- Vagueness score (adjective density) ---
    vague_count = sum(
        1
        for token in doc
        if token.pos_ == "ADJ" and token.text.lower() in markers.vague_adjectives
    )
    vagueness_score = vague_count / max(len(doc), 1)

    # --- Authority-claim detection ---
    authority_hits = [phrase for phrase in markers.authority_phrases if phrase in text_lower]
    authority_score = min(len(authority_hits) * 0.15, 1.0)

    # --- Urgency/fear pattern detection ---
    urgency_hits = [pattern for pattern in markers.urgency_patterns if pattern in text_lower]
    urgency_score = min(len(urgency_hits) * 0.2, 1.0)

    # --- Emotional manipulation detection ---
    fear_hits = [token.text for token in doc if token.lemma_.lower() in markers.fear_words]
    fear_hits += [phrase for phrase in markers.fear_phrases if phrase in text_lower]
    euphoria_hits = [token.text for token in doc if token.lemma_.lower() in markers.euphoria_words]
    euphoria_hits += [phrase for phrase in markers.euphoria_phrases if phrase in text_lower]

    fear_density = min(len(fear_hits) * 0.12, 1.0)
    euphoria_density = min(len(euphoria_hits) * 0.12, 1.0)

    # Contrast bonus: both fear AND euphoria = classic manipulation
    contrast_bonus = 0.0
    if fear_hits and euphoria_hits:
        contrast_bonus = min(fear_density * euphoria_density * 1.5, 0.5)

    emotion_score = min(fear_density + euphoria_density + contrast_bonus, 1.0)
    emotion_hits = fear_hits + euphoria_hits

    # --- Logical contradiction detection ---
    contradiction_hits: list[str] = []
    for label, pole_a, pole_b in markers.contradiction_pairs:
        has_a = any(pattern in text_lower for pattern in pole_a)
        has_b = any(pattern in text_lower for pattern in pole_b)
        if has_a and has_b:
            contradiction_hits.append(label)
    contradiction_score = min(len(contradiction_hits) * 0.3, 1.0)

    # --- Source attribution analysis ---
    unfalsifiable_hits = [
        phrase for phrase in markers.unfalsifiable_source_phrases if phrase in text_lower
    ]
    unnamed_hits = [phrase for phrase in markers.unnamed_authority_phrases if phrase in text_lower]
    verifiable_hits = [
        marker for marker in markers.verifiable_citation_markers if marker in text_lower
    ]
    source_attribution_hits = unfalsifiable_hits + unnamed_hits

    suspicious_density = min((len(unfalsifiable_hits) + len(unnamed_hits)) * 0.12, 1.0)
    verifiable_offset = min(len(verifiable_hits) * 0.15, 0.4)
    attribution_score = max(suspicious_density - verifiable_offset, 0.0)

    # --- Commitment escalation detection ---
    escalation_score, escalation_hits = _commitment_escalation(
        doc, markers.commitment_escalation_markers
    )

    # Weighted composite -- all sub-scores normalised to 0-1
    tech_score = (
        vagueness_score * 17
        + authority_score * 17
        + urgency_score * 13
        + emotion_score * 13
        + contradiction_score * 13
        + attribution_score * 13
        + escalation_score * 14
    )

    return (
        min(tech_score, 100.0),
        entities,
        authority_hits,
        urgency_hits,
        emotion_hits,
        contradiction_hits,
        source_attribution_hits,
        escalation_hits,
    )


def psychic_heuristic(density_bias: float = 0.75, *, seed: int | None = None) -> float:
    """Simulated 'psychic' intuition: probabilistic dissonance scanner.

    Args:
        density_bias: Information density bias (0.0-1.0). Lower = more suspicion.
        seed: Optional RNG seed for reproducible tests.
    """
    rng = random.Random(seed)
    base_intuition = rng.uniform(20, 80)
    return base_intuition * density_bias


def hybrid_score(
    text: str,
    density_bias: float = 0.75,
    *,
    seed: int | None = None,
    lang: SupportedLang = "en",
) -> ThreatResult:
    """Combine layers: 60% tech + 40% heuristic intuition."""
    (
        tech_score,
        entities,
        authority_hits,
        urgency_hits,
        emotion_hits,
        contradiction_hits,
        source_attribution_hits,
        escalation_hits,
    ) = tech_analysis(text, lang=lang)
    intuition_score = psychic_heuristic(density_bias, seed=seed)

    overall = (tech_score * 0.6) + (intuition_score * 0.4)

    return ThreatResult(
        overall_threat_score=round(overall, 2),
        tech_contribution=round(tech_score, 2),
        intuition_contribution=round(intuition_score, 2),
        detected_entities=entities,
        authority_hits=authority_hits,
        urgency_hits=urgency_hits,
        emotion_hits=emotion_hits,
        contradiction_hits=contradiction_hits,
        source_attribution_hits=source_attribution_hits,
        escalation_hits=escalation_hits,
    )


def main() -> None:
    """CLI entry point for the basic threat filter."""
    from si_protocols.output import render_json, render_rich

    parser = argparse.ArgumentParser(
        description="si-protocols — Basic Spiritual Intelligence Threat Filter v0.1",
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to text file to analyse (your own content only)",
    )
    parser.add_argument(
        "--density",
        type=float,
        default=0.75,
        help="Information density bias (0.0-1.0)",
    )
    parser.add_argument(
        "--format",
        choices=["rich", "json"],
        default="rich",
        dest="output_format",
        help="Output format: rich (default) or json",
    )
    parser.add_argument(
        "--lang",
        choices=["en", "ja"],
        default="en",
        help="Analysis language: en (default) or ja (Japanese)",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        print(f"Error: File not found — {args.file}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    result = hybrid_score(text, args.density, lang=args.lang)

    if args.output_format == "json":
        render_json(result)
    else:
        render_rich(result, args.file)


if __name__ == "__main__":
    main()
