---
title: Architecture
description: How si-protocols analyses text — the threat filter pipeline, topology module, engine tiers, and multi-language design.
order: 4
---

## Design Principles

Three principles guide every technical decision in si-protocols:

**Transparency over accuracy.** Every score, marker, and classification axis is inspectable. Users must be able to trace any result back to the specific patterns that triggered it. This rules out opaque ML classifiers as the primary scoring mechanism — static marker lists are version-controlled, culturally adaptable, and auditable without GPUs.

**Local-only by default.** The tool never hosts, collects, or analyses third-party content. The default engine runs entirely on the user's machine with no network calls. Higher-tier engines that call external APIs are opt-in and clearly labelled.

**Layered analysis.** No single technique catches every manipulation pattern. The system combines NLP pattern matching, probabilistic heuristics, and structural graph analysis so that each layer compensates for the others' blind spots.

## System Overview

![Architecture overview showing text input flowing through shared spaCy and marker infrastructure into two parallel modules: the threat filter (seven-dimension scoring) and the topology module (claim graph extraction)](/images/architecture-overview.svg)

si-protocols has two main analysis modules plus shared infrastructure:

| | Threat filter | Topology module |
|---|---|---|
| **Question it answers** | How suspicious is this text? | What claims does this text make, and how do they relate? |
| **Output** | `ThreatResult` — single 0–100 score with hit lists | `TopologyResult` — nodes, edges, variables, graph coordinates |
| **CLI** | `si-threat-filter` | `si-topology` |

Both modules share the marker registry (`marker_registry.py`) and spaCy model infrastructure, but maintain independent NLP caches to avoid import-time side effects.

## Threat Filter Pipeline

![Threat filter pipeline showing seven scoring dimensions with individual weights feeding into a 60/40 hybrid scoring system that produces an immutable ThreatResult](/images/threat-filter-pipeline.svg)

The threat filter produces a hybrid score by combining two analysis layers.

### Tech layer (60% weight)

A spaCy NLP pipeline that scores text across seven independent dimensions. Each dimension is normalised to 0–1, then combined with fixed weights:

| Dimension | Weight | Detection method |
|---|---|---|
| Vagueness | 17% | Adjective density against a curated list of semantically empty spiritual adjectives |
| Authority claims | 17% | Phrase matching — each distinct authority claim adds ~15 points (capped) |
| Urgency/fear | 13% | Pattern matching against time-pressure and fear-based phrases |
| Emotional manipulation | 13% | Lemma-based fear/euphoria detection with a contrast bonus when both polarities appear |
| Logical contradictions | 13% | Detecting when both poles of contradiction pairs appear in the same text |
| Source attribution | 13% | Unfalsifiable sources and unnamed authorities, offset by verifiable citations |
| Commitment escalation | 14% | Splits text into thirds using spaCy sentence boundaries and measures whether commitment intensity increases from mild to coercive |

The emotional manipulation dimension deserves special mention: it doesn't just count fear words or euphoria words individually, but applies a bonus when *both* polarities appear in the same text. Cycling between terror and promise — "you are in danger, but *we* can save you" — is a hallmark of manipulation. The contrast bonus captures this structural pattern.

### Heuristic layer (40% weight)

A probabilistic dissonance scanner using `random.Random`. This is an intentional placeholder — the randomness models a future biofeedback integration layer that bridges analytical and intuitive assessment. It accepts a `seed` parameter for deterministic testing.

### Hybrid scoring

`hybrid_score()` combines the two layers: 60% tech + 40% heuristic. The result is a frozen `ThreatResult` dataclass containing the composite score, the individual layer contributions, and hit lists for every dimension. Frozen dataclasses with tuple collections ensure the entire result graph is hashable and immutable — safe to cache, log, or pass between threads.

## Topology Module

The topology module answers a different question from the threat filter. Where the filter asks "how suspicious?", the topology module asks "what is this text *actually claiming*, and how do those claims relate to each other?"

### Claim extraction and classification

The module extracts individual claims (variables) from text and classifies each along four independent axes:

| Axis | Scale | What it measures |
|---|---|---|
| Falsifiability | 0.0 testable → 1.0 unfalsifiable | Can the claim be tested or disproved? |
| Verifiability | 0.0 has sources → 1.0 no checkable sources | Can the claim's sources be independently checked? |
| Domain coherence | 0.0 stays in domain → 1.0 crosses domains | Does the claim improperly mix domains (e.g. quantum physics + chakras)? |
| Logical dependency | 0.0 load-bearing → 1.0 decorative | Does the claim carry logical weight, or is it emotive filler? |

The mean of the four axes drives `VariableKind` derivation: `TRUE`, `PSEUDO`, or `INDETERMINATE`. The `TopologyLevel` enum (`MACRO`, `MESO`, `MICRO`) mirrors fractal analysis — zoom out for the whole-text summary, zoom in for individual claims.

### Engine tiers

| Tier | Engine | Trade-off |
|---|---|---|
| 0 | `RuleEngine` | Local, deterministic, fast. spaCy + marker heuristics. No API keys needed. |
| 1 | `AnthropicEngine` | Higher extraction quality via Claude API. Requires `anthropic` extra and `ANTHROPIC_API_KEY`. |
| 2 | `OllamaEngine` | Stub for future local-LLM integration. Interface defined, not yet functional. |

Tier 0 is the default and aligns with the local-only principle. Tier 1 trades local-only for extraction quality when the user explicitly opts in. Tier 2 exists as a declared interface so that contributors can implement it without changing the public API.

### SVG output

The renderer uses only `xml.etree.ElementTree` from the standard library — no external graphing packages. The intelligence-themed visual design (dark background, HUD frame, glow filters) matches the project's identity. Output is a self-contained SVG file that requires no JavaScript or external resources to render.

## Multi-Language Architecture

A `lang` parameter (`"en"` | `"ja"`) flows through the entire pipeline: CLI, API, and core library. Each language has its own spaCy model and marker set.

The marker registry (`marker_registry.py`) bundles all 12 marker categories into a frozen `MarkerSet` dataclass. `get_markers(lang)` dispatches to the correct language module with lazy loading and caching. Japanese markers (`markers_ja.py`) are culturally adapted — not naively translated from English. They cover Japanese-specific spiritual traditions: スピリチュアル (New Age), 霊感商法 (spiritual fraud), and cult rhetoric patterns specific to the Japanese context.

The spaCy models are lazy-loaded via `_get_nlp(lang)` to avoid import-time side effects. Tests that exercise the NLP pipeline are marked `@pytest.mark.slow` so that fast unit tests can run without loading the models.

## CVP Connection

![CVP layer mapping showing how the six consciousness layers (L1 Bare Metal through L6 Containers) connect to the topology module's variable classification and the threat filter's counterintelligence boundaries](/images/cvp-layer-mapping.svg)

The [Consciousness Virtualisation Platform (CVP)](https://github.com/lemur47/si-protocols/blob/main/cvp-ontology-v0.1.yaml) provides the theoretical framework that grounds the topology module's classification logic. It models consciousness as a six-layer infrastructure stack (L1 Bare Metal through L6 Containers), and the four classification axes act as layer detectors — measuring which layer of the stack a claim originates from.

The CVP connection is most visible in the [Quick-Check v0.2 Skill](/blog/ab-evaluation-quick-check-v02/), where the ontology preamble enables Claude to reason structurally about manipulation architectures rather than just counting pattern matches. The [A/B evaluation](/blog/ab-evaluation-quick-check-v02/) confirmed this adds analytical depth without inflating detection scores.

For the full model, see [The Virtualisation Model](https://spiritualintelligence.cc/the-virtualisation-model/) on the educational site.

## What's Not Here

This page covers the analysis architecture. For other aspects of the system:

- [Quickstart](/docs/quickstart/) — installation and first analysis in under five minutes
- [Python Library Reference](/docs/library/) — `hybrid_score()`, `tech_analysis()`, and the topology API
- [REST API Reference](/docs/api/) — HTTP endpoint schemas and examples
- [GitHub](https://github.com/lemur47/si-protocols) — source code, `docs/DESIGN.md` for contributor-facing architectural reasoning
