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

# Topology module
from si_protocols.topology import (
    RuleEngine,
    build_topology,
    render_svg,
    save_svg,
    render_topology_json,
    TopologyResult,
    Variable,
    VariableClassification,
    VariableKind,
    TopologyLevel,
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

## Topology Module

The topology module extracts claims (variables) from text, classifies them along four axes, and builds a layered graph with nodes, edges, and layout coordinates.

### `RuleEngine`

The default, local engine. Uses spaCy NLP and marker heuristics to extract and classify variables.

```python
def extract_variables(
    self,
    text: str,
    *,
    lang: SupportedLang = "en",
) -> list[Variable]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | (required) | The text to analyse |
| `lang` | `SupportedLang` | `"en"` | Language of the input text (`"en"` or `"ja"`) |

**Example:**

```python
from si_protocols.topology import RuleEngine

engine = RuleEngine()
text = open("examples/synthetic_topology_suspicious.txt").read()
variables = engine.extract_variables(text, lang="en")

for var in variables:
    print(f"[{var.kind.value}] {var.text[:60]}")
    print(f"  falsifiability={var.classification.falsifiability}")
```

### `build_topology()`

Constructs a complete topology graph from extracted variables.

```python
def build_topology(
    variables: list[Variable],
    *,
    lang: SupportedLang = "en",
    engine_name: str = "",
    canvas_width: float = 900.0,
) -> TopologyResult
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `variables` | `list[Variable]` | (required) | Variables extracted by an engine |
| `lang` | `SupportedLang` | `"en"` | Language of the source text |
| `engine_name` | `str` | `""` | Name of the engine that produced the variables |
| `canvas_width` | `float` | `900.0` | Width of the SVG coordinate space |

**Example:**

```python
from si_protocols.topology import RuleEngine, build_topology

engine = RuleEngine()
variables = engine.extract_variables(text)
result = build_topology(variables, lang="en", engine_name=engine.name)

print(f"Nodes: {len(result.nodes)}")
print(f"Edges: {len(result.edges)}")
print(f"Pseudo: {result.pseudo_count}, True: {result.true_count}")
```

### `render_svg()` / `save_svg()`

Render a `TopologyResult` as an intelligence-themed SVG.

```python
from si_protocols.topology import render_svg, save_svg

svg_string = render_svg(result)           # Returns SVG as a string
save_svg(result, "output.topology.svg")   # Writes to file
```

### `render_topology_json()`

Serialise a `TopologyResult` to indented JSON.

```python
from si_protocols.topology import render_topology_json

json_string = render_topology_json(result)  # Prints to stdout, returns string

# Write to file instead:
with open("output.json", "w") as f:
    render_topology_json(result, file=f)
```

### `TopologyResult` fields

`TopologyResult` is a frozen dataclass returned by `build_topology()`.

| Field | Type | Description |
|-------|------|-------------|
| `nodes` | `tuple[TopologyNode, ...]` | Nodes in the topology graph |
| `edges` | `tuple[TopologyEdge, ...]` | Directed edges between nodes |
| `variables` | `tuple[Variable, ...]` | All extracted variables |
| `pseudo_count` | `int` | Number of pseudo-variables |
| `true_count` | `int` | Number of true-variables |
| `indeterminate_count` | `int` | Number of indeterminate variables |
| `lang` | `SupportedLang` | Language used for analysis |
| `engine_name` | `str` | Name of the engine that produced the result |
| `message` | `str` | Summary message |

### `VariableClassification` axes

Each variable is classified along four independent axes (0.0–1.0, higher = more suspicious):

| Axis | Scale | What it measures |
|------|-------|-----------------|
| `falsifiability` | 0.0 testable → 1.0 unfalsifiable | Can the claim be tested or disproved? |
| `verifiability` | 0.0 has sources → 1.0 no checkable sources | Can the claim's sources be independently checked? |
| `domain_coherence` | 0.0 stays in domain → 1.0 crosses domains | Does the claim improperly mix domains (e.g. quantum physics + chakras)? |
| `logical_dependency` | 0.0 load-bearing → 1.0 decorative | Does the claim carry logical weight, or is it emotive filler? |

### `VariableKind`

Derived from the mean of the four classification axes:

| Kind | Derivation rule |
|------|----------------|
| `PSEUDO` | Mean ≥ 0.4, or mean ≥ 0.25 with any single axis ≥ 0.5 |
| `TRUE` | Mean ≤ 0.15 |
| `INDETERMINATE` | Everything else |

### Engine tiers

| Tier | Engine | Description |
|------|--------|-------------|
| 0 | `RuleEngine` | Local, deterministic. Uses spaCy + marker heuristics. No API keys needed. |
| 1 | `AnthropicEngine` | Claude API-based extraction. Requires `anthropic` extra and `ANTHROPIC_API_KEY`. |
| 2 | `OllamaEngine` | Stub for future local-LLM integration. Not yet functional. |

All engines implement the `AnalysisEngine` protocol and expose `name` (property) and `extract_variables(text, *, lang)` (method).
