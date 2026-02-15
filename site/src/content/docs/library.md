---
title: Python Library Reference
description: Use si-protocols as a Python library for programmatic threat analysis.
order: 2
---

## Importing the Library

```python
from si_protocols.threat_filter import hybrid_score, tech_analysis, ThreatResult
from si_protocols.markers import (
    VAGUE_ADJECTIVES,
    AUTHORITY_PHRASES,
    URGENCY_PATTERNS,
    FEAR_WORDS,
    EUPHORIA_WORDS,
    CONTRADICTION_PAIRS,
    UNFALSIFIABLE_SOURCE_PHRASES,
    COMMITMENT_ESCALATION_MARKERS,
)
```

## `hybrid_score()`

The main entry point. Combines the NLP tech layer (60%) with the heuristic layer (40%) and returns a `ThreatResult`.

```python
def hybrid_score(
    text: str,
    density_bias: float = 0.75,
    *,
    seed: int | None = None,
) -> ThreatResult
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | (required) | The text to analyse |
| `density_bias` | `float` | `0.75` | Information density bias for the heuristic layer (0.0–1.0). Lower values increase suspicion. |
| `seed` | `int \| None` | `None` | Optional RNG seed for the heuristic layer. Use a fixed seed for reproducible results. |

**Example:**

```python
from si_protocols.threat_filter import hybrid_score

text = open("examples/synthetic_suspicious.txt").read()
result = hybrid_score(text, seed=42)

print(f"Threat score: {result.overall_threat_score}/100")
print(f"Tech layer: {result.tech_contribution}")
print(f"Heuristic layer: {result.intuition_contribution}")
print(f"Authority claims: {result.authority_hits}")
```

## `tech_analysis()`

Runs only the NLP tech layer, skipping the heuristic. Useful when you want deterministic results without a random seed.

```python
def tech_analysis(
    text: str,
) -> tuple[float, list[str], list[str], list[str], list[str], list[str], list[str], list[str]]
```

Returns an 8-element tuple:

| Index | Value |
|-------|-------|
| 0 | Tech score (0–100) |
| 1 | Detected named entities |
| 2 | Authority claim hits |
| 3 | Urgency pattern hits |
| 4 | Emotion trigger hits |
| 5 | Logical contradiction hits |
| 6 | Source attribution hits |
| 7 | Commitment escalation hits |

**Example:**

```python
from si_protocols.threat_filter import tech_analysis

score, entities, auth, urgency, emotion, contra, source, escalation = tech_analysis(text)
print(f"Tech score: {score}/100")
```

## `ThreatResult` Fields

`ThreatResult` is a frozen dataclass returned by `hybrid_score()`.

| Field | Type | Description |
|-------|------|-------------|
| `overall_threat_score` | `float` | Hybrid score (0–100): 60% tech + 40% heuristic |
| `tech_contribution` | `float` | Tech layer score (0–100) |
| `intuition_contribution` | `float` | Heuristic layer score |
| `detected_entities` | `list[str]` | Named entities found by spaCy |
| `authority_hits` | `list[str]` | Matched authority claim phrases |
| `urgency_hits` | `list[str]` | Matched urgency/fear patterns |
| `emotion_hits` | `list[str]` | Matched fear and euphoria words/phrases |
| `contradiction_hits` | `list[str]` | Labels of detected contradiction pairs |
| `source_attribution_hits` | `list[str]` | Unfalsifiable and unnamed authority phrases |
| `escalation_hits` | `list[str]` | Commitment escalation labels by segment |
| `message` | `str` | Disclaimer: "Run on your own texts only — this is a local tool." |

## Scoring Dimensions

The tech layer scores text across seven independent dimensions, each normalised to 0–1 and combined with the following weights:

| Dimension | Weight | What it detects |
|-----------|--------|-----------------|
| Vagueness | 17% | Adjective density against `VAGUE_ADJECTIVES` |
| Authority claims | 17% | Phrase matching against `AUTHORITY_PHRASES` |
| Urgency/fear | 13% | Pattern matching against `URGENCY_PATTERNS` |
| Emotional manipulation | 13% | Lemma-based fear/euphoria detection with a contrast bonus when both polarities appear |
| Logical contradictions | 13% | Both poles of `CONTRADICTION_PAIRS` appearing in the same text |
| Source attribution | 13% | Unfalsifiable sources and unnamed authorities, offset by verifiable citations |
| Commitment escalation | 14% | Foot-in-the-door progression — splits text into thirds and measures whether commitment intensity increases |

## Markers

All marker definitions live in `markers.py` as static word/phrase lists. They are plain data — no models, no magic.

**Tradition categories** covered:

- Generic New Age
- Prosperity gospel
- Conspirituality
- New Age commercial exploitation
- High-demand group (cult) rhetoric
- Fraternal/secret society traditions

You can inspect the markers programmatically:

```python
from si_protocols.markers import VAGUE_ADJECTIVES, CONTRADICTION_PAIRS

# List all vague adjectives
print(sorted(VAGUE_ADJECTIVES))

# List contradiction pair labels
for label, pole_a, pole_b in CONTRADICTION_PAIRS:
    print(f"{label}: {pole_a[0]} vs. {pole_b[0]}")
```

All markers are lowercase. Matching is case-insensitive (the analyser lowercases input text before comparison).
