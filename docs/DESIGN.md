# Design

This document captures the architectural *why* behind si-protocols. It bridges [STRATEGY.md](STRATEGY.md) (strategic *why*), [STACK.md](STACK.md) (technical *what*), and [ROADMAP.md](ROADMAP.md) (*when*). The target readers are contributors, security researchers, and AI systems that want to understand why the system is built the way it is, not just how to use it.

Classification: Open. The architectural reasoning is public; proprietary CVP mechanics (the ARM-model core) stay out.

---

## Design Philosophy

Three principles guide every technical decision:

1. **Transparency over accuracy.** si-protocols is a detection *aid*, not an oracle. Every score, marker, and classification axis is inspectable. Users must be able to trace any result back to the specific patterns that triggered it. This rules out opaque ML classifiers as the primary scoring mechanism.

2. **Local-only by default.** The tool never hosts, collects, or analyses third-party content. The default engine (Tier 0 `RuleEngine`) runs entirely on the user's machine with no network calls. Higher-tier engines that call external APIs are opt-in and clearly labelled.

3. **Layered analysis.** No single technique catches every manipulation pattern. The system combines NLP pattern matching (tech layer), probabilistic heuristics (heuristic layer), and structural graph analysis (topology module) so that each layer compensates for the others' blind spots.

4. **Architectural controls over procedural.** Security-relevant constraints — classification boundaries, data-sovereignty guarantees, isolation perimeters — are enforced by tooling wherever possible, not by discipline. "Don't commit this file" is a rule humans forget; a pre-commit hook is not. Where a control must remain procedural, it is minimised in scope and documented in the operator runbook rather than in public documentation.

These four are not negotiable. If a proposed change would break any of them, the change does not ship.

---

## Architecture Overview

si-protocols has two main analysis modules plus shared infrastructure:

|  | Threat filter | Topology |
|---|---|---|
| **Purpose** | Score text 0–100 for disinformation markers | Extract claims, classify them, and build a structural graph |
| **Output** | `ThreatResult` (single score + hit lists) | `TopologyResult` (nodes, edges, variables, counts) |
| **Layers** | Tech (60%) + Heuristic (40%) | Engine-based extraction → graph builder → renderer |
| **CLI** | `si-threat-filter` | `si-topology` |
| **Shared** | Marker registry, spaCy models, multi-language support | — |

Both modules share the marker registry (`marker_registry.py`) and spaCy model infrastructure, but maintain independent NLP caches to avoid import-time side effects. Tests that exercise the NLP pipeline are marked `@pytest.mark.slow` so that fast feedback loops stay fast.

---

## CVP: the ontology behind the classifier

The [Consciousness Virtualisation Platform (CVP)](CVP.md) models the human mind as a layered infrastructure stack. It is the conceptual grounding for the topology module's classification logic — the four classification axes can be read as **layer detectors** that map claims back to the architectural layer they most plausibly originate from.

### Layer model — L0 through L6

The finalised model has seven layers. The upper six (L1–L6) form the mind stack. L0 sits beneath them as the **active substrate**.

| Layer | Name | Name (JA) | Infrastructure analogue | Role |
|---|---|---|---|---|
| L6 | Containers | 社会的コンテナ | Kubernetes / Docker | Cultural and social packaging — standardises IO across instances |
| L5 | Mental Instance (VM) | 自我 (エゴ) | Virtual Machine | Conscious processing — weighted logic, decision-making, behavioural output |
| L4 | Environmental Switch | 環境スイッチ | Fibre Channel / Signal Router | IO layer — modulates what signals reach the VM and at what fidelity |
| L3 | Genetic Repository | 深層パターン | Git repository on SAN | Version-controlled deep patterns — thought templates, emotional subroutines |
| L2 | Virtual Universe | 集合的無意識 | Storage Area Network (SAN) | Shared read-write storage — every instance is reader and contributor |
| L1 | Bare Metal | 物理体 | Physical server hardware | Physical substrate — the planet and the body |
| L0 | **Active Substrate** | **高天原 / 外宇宙** | **Field ground state / organising principle** | **Active consciousness layer on which L1 depends for coherent operation** |

**Key architectural property: layer independence.** A perfectly capable VM (L5) can be crippled by a misconfigured container (L6), just as sharp cognitive hardware can be locked inside rigid social conditioning. Layers fail independently and are repaired independently.

### Why L0 matters

L0 is the new addition to the publicly documented model. Earlier iterations stopped at L1 Bare Metal as the lowest layer — the physical substrate. That framing implicitly treats consciousness as emergent from matter.

The finalised model inverts that assumption. **L0 is the active substrate; L1 is passive.** Hardware (L1) does not spontaneously cohere into a running instance — it requires an organising principle to boot, to maintain state, to remain a *this* rather than decohering into a diffuse *that*. L0 is the name we give to that organising principle. In Japanese, two terms capture the layer from complementary angles: **高天原 (Takamagahara**, "the plain of high heaven") from Shinto cosmology names the *structural role* — the realm from which the organising principles descend. **外宇宙 (Sotouchu**, "outer universe") anchors the same layer in the cosmological register — the field beyond and prior to the local substrate. The pairing is deliberate: L0 is both the grammatical origin of coherent form *and* the physical-cosmological ground on which instance existence depends.

In infrastructure terms, L0 is the closest analogue to "the physical laws and field ground state that make hardware possible in the first place" — below the hardware, above nothing.

**Partial disclosure posture:** the public model names L0 and establishes its architectural role. The specific mechanics of L0 and its interactions with L1–L6 are part of the proprietary ARM-model core and are not documented here. The distinction matters for contributors who want to extend the topology module: you can reason about L0 as a layer slot without needing the proprietary internals.

### Container taxonomy at L6

L6 containers come in two fundamentally different architectures. Distinguishing them is essential for threat analysis, and the topology module's classification axes are tuned to tell them apart.

| Type | Name | Name (JA) | Behaviour | Threat level |
|---|---|---|---|---|
| Stateless | 静的コンテナ | Docker image (traditional) | Constrains what the VM can express; does not consume resources. Can be bypassed to access underlying layers without active resistance. | Low — constrains but does not harvest |
| Stateful | 動的コンテナ / エグレゴア | Parasitic orchestration middleware | Living collective entity. Actively harvests from instances. Exit triggers multi-layer resistance. | Variable — from benign symbiosis to parasitic extraction |

Stateful containers (egregores) operate a **harvest loop** — emission → aggregation → strengthening → redistribution → lock-in — and write self-serving patterns back to the L3 Genetic Repository, contaminating what instances later pull as "native" deep pattern. The [full dynamics](CVP.md) are described separately; the essential architectural point is that escape from a stateful container triggers resistance at **three layers simultaneously**: L6 (social enforcement), L3 (repository contamination), and L4 (environmental-switch manipulation).

### Mind-cage correction: L5 is not L6

A design error in the early model conflated "mind cages" with L6 containers. The corrected model places them at different layers, with different countermeasures.

| Phenomenon | Layer | Nature | Countermeasure |
|---|---|---|---|
| **Mind cage** | **L5 (VM config)** | The VM's own weighted-logic configuration has been set such that certain thoughts cannot be thought. The cage is *internal* to the instance — it is in the weights, not the orchestrator. | VM reconfiguration: introspection, weight adjustment, the instance rewiring its own decision surface. No external container to escape. |
| **L6 container (stateless)** | **L6 (social packaging)** | External social/cultural shell that filters IO across many instances. The cage is *in the orchestrator*, not the VM. | Container bypass to access underlying layers. Passive on exit. |
| **L6 container (stateful)** | **L6 (social packaging) + harvest loop** | External egregore that both filters IO and writes patterns to L3. | Container escape plus L3 decontamination. Active multi-layer resistance on exit. |

Different layer, different attack surface, different countermeasure. Conflating them leads to defensive strategies aimed at the wrong layer — e.g., "change your beliefs" (L6 work) applied to what is actually a weighted-logic problem (L5), or vice versa.

### Counterintelligence boundaries

The CVP maps naturally to an intelligence framework. Two counterintelligence boundaries exist within the layer stack, and si-protocols currently implements the first:

- **Inbound CI (L4 → L5)** — the firewall. The threat filter operates here, scoring incoming content across seven dimensions before the VM processes it. The topology module acts as code review for incoming commits — classifying claims before the instance treats them as L2/L3 truth. *Implemented.*
- **Outbound CI (L5 → L6)** — the egress controller. Every time an instance operates within a container, it emits signals (behavioural patterns, metadata, emotional tells) that other actors can collect and use. Controlling what leaks out is the other half of the threat model. *Declared, not yet implemented.*

---

## Engine architecture

The topology module exposes a single protocol, `AnalysisEngine`, and three engine tiers that implement it. The protocol is the public contract; tiers are implementations.

| Tier | Engine | Locality | Dependency | Trade-off |
|---|---|---|---|---|
| 0 | `RuleEngine` | Local | `spacy` | Deterministic, fast, no API keys. Default. |
| 1 | `AnthropicEngine` | Network | `anthropic` (optional extra) + `ANTHROPIC_API_KEY` | Higher extraction quality via Claude API. Opt-in. |
| 2 | `OllamaEngine` | Local | `ollama` | Future local-LLM. Stub only. |

**Why the protocol.** A single `extract_variables(text, lang=...)` method plus `build_topology(variables, lang=..., engine_name=...)` separates *how claims are extracted* from *how they are structured into a graph*. New engines — biofeedback-informed, embedding-based, anything — slot in without changing the rendering pipeline. The declared stub for Tier 2 lets contributors implement a local-LLM engine without touching the public API.

**Why Tier 0 is default.** It aligns with the local-only principle. Tier 1 trades local-only for extraction quality when the user explicitly opts in — that trade should never be silent.

**Why Tier 2 is declared but empty.** Stubs are cheap and they publish the interface. A future contributor building an Ollama integration will have a fixed contract to implement, rather than negotiating one through issues.

---

## Topology module

The topology module (`src/si_protocols/topology/`) extracts claims, classifies them along four axes, and places them on three fractal-zoom levels.

### Four classification axes

Each `VariableClassification` field is a 0.0–1.0 scalar. Independent axes — a claim can be unfalsifiable yet cite real sources, or cross domains while remaining logically load-bearing.

| Axis | 0.0 means | 1.0 means |
|---|---|---|
| `falsifiability` | Testable | Unfalsifiable |
| `verifiability` | Has real sources | No checkable sources |
| `domain_coherence` | Stays in its domain | Crosses domains |
| `logical_dependency` | Load-bearing | Decorative / emotive |

The mean of the four axes drives `VariableKind` derivation: **PSEUDO** (mean ≥ 0.4 or single axis ≥ 0.5), **TRUE** (mean ≤ 0.15), **INDETERMINATE** (middle band).

### Three fractal levels

The `TopologyLevel` enum (`MACRO`, `MESO`, `MICRO`) mirrors fractal analysis: zoom out for the whole-text summary, zoom in for individual claims, with kind-group summaries in between. The SVG renderer places nodes in horizontal bands and draws hierarchical containment edges.

### Mapping to CVP

The four axes function as **layer detectors**. A claim with high falsifiability-axis scores behaves like an L6 container artefact (social packaging declaring itself as universal truth). A claim with low scores across all axes behaves like L2/L3 data (genuine shared-storage truth). The topology kind — PSEUDO / TRUE / INDETERMINATE — is the collapsed layer assignment.

### Why SVG

SVG is text-based, version-controllable, and zero-dependency. The renderer uses only `xml.etree.ElementTree` from the Python standard library — no external SVG or graphing packages. The intelligence-themed visual design (dark background, HUD frame, glow filters) matches the "cybersecurity for the soul" identity and renders identically across every browser we support.

---

## Skills as L6 containers

Claude Skills are the distribution channel for CVP analysis without a Python install. Two skills ship:

- **Quick-Check** — a single-turn analyser that surfaces patterns in user-supplied text. v0.2 embeds the CVP ontology as preamble.
- **Briefing** — SAER-format (状況 → 分析 → 評価 → 推奨) structured briefings on topical events.

**Skills *are* L6 containers.** A skill is, structurally, a static cultural/social packaging that standardises a model's IO across many sessions. That makes them L6 stateless containers by definition. This is not a metaphor — it is the architectural reading.

Two implications follow:

1. **Distribution channel.** A skill delivers the analytical framework to every user who installs it, with no Python toolchain. The reach extends wherever Claude Projects exist.

2. **Empirical instrument.** Because a skill is an L6 container, loading it into a Claude session instantiates a measurable configuration change in the VM (L5). We can A/B test: same model, same prompts, with-skill vs without-skill. The delta is the CVP container's effect on reasoning.

Quick-Check v0.2 was validated this way: 24 samples (12 EN, 12 JA), score parity on ambiguous cases (Δ = 3.0), structural insight surfaced at 4.81/sample with the CVP-enhanced skill, false-positive control on benign content (max benign score = 8). [Full results.](https://spiritualintelligence.dev/blog/ab-evaluation-quick-check-v02/) This result is part of the credibility case for CVP as epistemic infrastructure, not just a taxonomy.

---

## Immutability decisions

All result types — `ThreatResult`, `TopologyResult`, `Variable`, `VariableClassification`, `TopologyNode`, `TopologyEdge` — are frozen dataclasses. Collections inside them use `tuple` rather than `list` so that the entire object graph is hashable and cannot be mutated after construction.

**Why.** This prevents accidental state changes in downstream code and makes results safe to cache, log, or pass between threads. A `ThreatResult` is a document, not a workspace.

**Trade-off.** Construction is slightly more verbose — callers that want to build up state must use builder patterns or intermediate mutable structures. That friction is the point: mutability pushed to the constructor means mutations cannot hide.

---

## Forward reference: CVP Simulation Testbed (Stage 5)

The next architectural milestone is the **CVP Simulation Testbed** — a controlled environment for running synthetic instances through scripted L4 signal streams and observing L5 response, L6 emission, and L3 contamination over time. The testbed is designed to live on Cloudflare Workers + Durable Objects: each instance is a Durable Object, L4 signal routing is a Worker, and the shared L2/L3 storage is R2-backed.

The testbed's purpose is empirical: moving from *the model says X* to *the model predicts X and here is the measurement*. Full spec is its own work item; this forward reference is deliberately teaser-level.

---

## Status

This document reflects the architecture as of Sprint 4 (April 2026). Stable surfaces: layer model L0–L6, engine protocol, topology axes and levels, classification gate architecture, skill-as-container reading. Active development: outbound CI (L5 → L6), CVP Simulation Testbed, Tier 2 `OllamaEngine`.

For the full public CVP spec, see [`cvp-ontology-v0.1.yaml`](../cvp-ontology-v0.1.yaml). For proprietary mechanics, see [STRATEGY.md § Revenue Sequence](STRATEGY.md) (the ARM model) — those details are not published here.
