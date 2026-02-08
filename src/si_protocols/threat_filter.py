"""Hybrid threat scorer: NLP tech layer + heuristic 'psychic' weighting.

Run locally on your own text files only. MIT Licence.
"""

import argparse
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

import spacy

from si_protocols.markers import (
    AUTHORITY_PHRASES,
    EUPHORIA_PHRASES,
    EUPHORIA_WORDS,
    FEAR_PHRASES,
    FEAR_WORDS,
    URGENCY_PATTERNS,
    VAGUE_ADJECTIVES,
)

# Lazy-load to avoid import-time side effects in tests
_nlp = None


def _get_nlp() -> spacy.language.Language:
    """Load spaCy model on first use."""
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


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
    message: str = "Run on your own texts only — this is a local tool."


def tech_analysis(
    text: str,
) -> tuple[float, list[str], list[str], list[str], list[str]]:
    """Tech layer: NLP-based suspicion signals.

    Returns (score, entities, authority_hits, urgency_hits, emotion_hits).
    """
    if not text.strip():
        return 0.0, [], [], [], []

    nlp = _get_nlp()
    doc = nlp(text)
    text_lower = text.lower()

    entities = [ent.text for ent in doc.ents]

    # --- Vagueness score (adjective density) ---
    vague_count = sum(
        1 for token in doc if token.pos_ == "ADJ" and token.text.lower() in VAGUE_ADJECTIVES
    )
    vagueness_score = vague_count / max(len(doc), 1)

    # --- Authority-claim detection ---
    authority_hits = [phrase for phrase in AUTHORITY_PHRASES if phrase in text_lower]
    authority_score = min(len(authority_hits) * 0.15, 1.0)

    # --- Urgency/fear pattern detection ---
    urgency_hits = [pattern for pattern in URGENCY_PATTERNS if pattern in text_lower]
    urgency_score = min(len(urgency_hits) * 0.2, 1.0)

    # --- Emotional manipulation detection ---
    fear_hits = [token.text for token in doc if token.lemma_.lower() in FEAR_WORDS]
    fear_hits += [phrase for phrase in FEAR_PHRASES if phrase in text_lower]
    euphoria_hits = [token.text for token in doc if token.lemma_.lower() in EUPHORIA_WORDS]
    euphoria_hits += [phrase for phrase in EUPHORIA_PHRASES if phrase in text_lower]

    fear_density = min(len(fear_hits) * 0.12, 1.0)
    euphoria_density = min(len(euphoria_hits) * 0.12, 1.0)

    # Contrast bonus: both fear AND euphoria = classic manipulation
    contrast_bonus = 0.0
    if fear_hits and euphoria_hits:
        contrast_bonus = min(fear_density * euphoria_density * 1.5, 0.5)

    emotion_score = min(fear_density + euphoria_density + contrast_bonus, 1.0)
    emotion_hits = fear_hits + euphoria_hits

    # Weighted composite -- all sub-scores normalised to 0-1
    tech_score = (
        vagueness_score * 30 + authority_score * 30 + urgency_score * 20 + emotion_score * 20
    )

    return min(tech_score, 100.0), entities, authority_hits, urgency_hits, emotion_hits


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
) -> ThreatResult:
    """Combine layers: 60% tech + 40% heuristic intuition."""
    tech_score, entities, authority_hits, urgency_hits, emotion_hits = tech_analysis(text)
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
    )


def main() -> None:
    """CLI entry point for the basic threat filter."""
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
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        print(f"Error: File not found — {args.file}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    result = hybrid_score(text, args.density)

    print("\n=== si-protocols Threat Analysis v0.1 ===")
    print(f"File: {args.file}")
    print(f"Overall Threat Score: {result.overall_threat_score}/100")
    print(f"  └─ Tech layer: {result.tech_contribution}")
    print(f"  └─ Heuristic intuition: {result.intuition_contribution}")
    if result.detected_entities:
        print(f"Detected entities: {', '.join(result.detected_entities)}")
    if result.authority_hits:
        print(f"Authority claims: {', '.join(result.authority_hits)}")
    if result.urgency_hits:
        print(f"Urgency patterns: {', '.join(result.urgency_hits)}")
    if result.emotion_hits:
        print(f"Emotion triggers: {', '.join(result.emotion_hits)}")
    print(f"\n{result.message}")


if __name__ == "__main__":
    main()
