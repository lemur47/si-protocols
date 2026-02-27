# Design

This document captures the architectural reasoning behind si-protocols. It bridges [STRATEGY.md](STRATEGY.md) (mission, audience, roadmap) and [CLAUDE.md](../CLAUDE.md) (developer reference). The target readers are contributors and security researchers who want to understand *why* the system is built the way it is, not just *how* to use it.

## Design Philosophy

Three principles guide every technical decision:

1. **Transparency over accuracy** — si-protocols is a detection *aid*, not an oracle. Every score, marker, and classification axis is inspectable. Users must be able to trace any result back to the specific patterns that triggered it. This rules out opaque ML classifiers as the primary scoring mechanism.

2. **Local-only by default** — the tool never hosts, collects, or analyses third-party content. The default engine (Tier 0 `RuleEngine`) runs entirely on the user's machine with no network calls. Higher-tier engines that call external APIs are opt-in and clearly labelled.

3. **Layered analysis** — no single technique catches every manipulation pattern. The system combines NLP pattern matching (tech layer), probabilistic heuristics (heuristic layer), and structural graph analysis (topology module) so that each layer compensates for the others' blind spots.

## Architecture Overview

si-protocols has two main analysis modules plus shared infrastructure:

| | Threat filter | Topology |
|---|---|---|
| **Purpose** | Score text 0–100 for disinformation markers | Extract claims, classify them, and build a structural graph |
| **Output** | `ThreatResult` (single score + hit lists) | `TopologyResult` (nodes, edges, variables, counts) |
| **Layers** | Tech (60%) + Heuristic (40%) | Engine-based extraction → graph builder → renderer |
| **CLI** | `si-threat-filter` | `si-topology` |
| **Shared** | Marker registry, spaCy models, multi-language support | — |

Both modules share the marker registry (`marker_registry.py`) and spaCy model infrastructure, but maintain independent NLP caches to avoid import-time side effects.

## Threat Filter Design

### Why seven dimensions

Each dimension targets a specific manipulation tactic commonly found in spiritual disinformation. The seven dimensions were chosen to cover the most prevalent patterns across the tradition categories (New Age, prosperity gospel, conspirituality, commercial exploitation, high-demand groups, and fraternal/secret society rhetoric).

| Dimension | Weight | Tactic it detects |
|---|---|---|
| Vagueness | 17% | Adjective inflation that sounds profound but conveys nothing testable |
| Authority claims | 17% | Appeals to unnamed or unfalsifiable authorities |
| Urgency/fear | 13% | Time-pressure and fear-based persuasion |
| Emotional manipulation | 13% | Alternating fear and euphoria to destabilise judgement |
| Logical contradictions | 13% | Holding opposing claims simultaneously (e.g. empowerment + dependency) |
| Source attribution | 13% | Unfalsifiable sources and unnamed authorities, offset by verifiable citations |
| Commitment escalation | 14% | Foot-in-the-door progression that increases demands over the course of a text |

### Why 60/40 hybrid

The tech layer is deterministic and auditable — given the same text and markers, it always produces the same score. The heuristic layer introduces controlled randomness as a placeholder for future biofeedback integration (bridging analytical and intuitive assessment). The 60/40 split ensures the score is predominantly driven by transparent NLP patterns while leaving room for the heuristic signal.

### Why markers over ML

Static marker lists are inspectable, version-controlled, and culturally adaptable without retraining. A contributor can add a new manipulation phrase by editing a Python file and submitting a pull request — no training data, no GPU, no black box. This aligns with the transparency principle.

## Topology Module Design

### Why separate from the threat filter

The threat filter answers "how suspicious is this text?" with a single score. The topology module answers "what claims does this text make, and how do they relate to each other?" These are complementary but structurally different questions. Merging them would compromise the clarity of both outputs.

### Why four classification axes

Each axis captures a distinct dimension of claim quality that is relevant to spiritual disinformation:

| Axis | Scale | What it measures |
|---|---|---|
| `falsifiability` | 0.0 testable → 1.0 unfalsifiable | Can the claim be tested or disproved? |
| `verifiability` | 0.0 has sources → 1.0 no checkable sources | Can the claim's sources be independently checked? |
| `domain_coherence` | 0.0 stays in domain → 1.0 crosses domains | Does the claim improperly mix domains (e.g. quantum physics + chakras)? |
| `logical_dependency` | 0.0 load-bearing → 1.0 decorative | Does the claim carry logical weight, or is it emotive filler? |

These four axes are independent — a claim can be unfalsifiable yet cite real sources, or cross domains while being logically load-bearing. The mean of the four axes drives `VariableKind` derivation.

### Why three levels

The `TopologyLevel` enum (`MACRO`, `MESO`, `MICRO`) mirrors fractal analysis: zoom out for the whole-text summary, zoom in for individual claims, with kind-group summaries in between. This lets the SVG renderer place nodes in horizontal bands and draw hierarchical containment edges.

### Why tiered engines

| Tier | Engine | Trade-off |
|---|---|---|
| 0 | `RuleEngine` | Local, deterministic, fast. Uses spaCy + marker heuristics. No API keys needed. |
| 1 | `AnthropicEngine` | Higher extraction quality via Claude API. Requires `anthropic` extra and `ANTHROPIC_API_KEY`. |
| 2 | `OllamaEngine` | Stub for future local-LLM integration. Not yet functional. |

Tier 0 is the default and aligns with the local-only principle. Tier 1 trades local-only for extraction quality when the user explicitly opts in. Tier 2 is a declared interface for future work — it exists so that contributors can implement it without changing the public API.

### Why SVG

SVG is a text-based, version-controllable, zero-dependency output format. The renderer uses only `xml.etree.ElementTree` from the standard library — no external SVG or graphing packages. The intelligence-themed visual design (dark background, HUD frame, glow filters) matches the project's "cybersecurity for the soul" identity.

## Immutability Decisions

All result types (`ThreatResult`, `TopologyResult`, `Variable`, `VariableClassification`, `TopologyNode`, `TopologyEdge`) are frozen dataclasses. Collections inside them use `tuple` rather than `list` so that the entire object graph is hashable and cannot be mutated after construction. This prevents accidental state changes in downstream code and makes results safe to cache, log, or pass between threads.
