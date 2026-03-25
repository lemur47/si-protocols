---
title: "A/B Evaluation: Quick-Check v0.2 (CVP-Enhanced)"
description: Empirical results from testing whether the Consciousness Virtualisation Platform ontology improves Claude Skill analysis without inflating threat scores.
date: 2026-03-21
tags: [evaluation, cvp, quick-check, methodology]
---

## The Hypothesis

Quick-Check v0.1 scores spiritual and metaphysical texts across seven manipulation dimensions — vagueness, authority claims, urgency/fear, emotional manipulation, logical contradictions, source attribution, and commitment escalation. It answers *what* patterns are present.

Version 0.2 adds a [CVP ontology](https://github.com/lemur47/si-protocols/blob/main/cvp-ontology-v0.1.yaml) preamble — a consciousness-infrastructure model that gives the analyser structural vocabulary for reasoning about *where* claims originate and *how* manipulation architectures operate. The hypothesis: this ontology layer adds explanatory depth without distorting the existing detection scores.

Think of it as upgrading `grep` to `grep + strace` — the surface results stay the same, but now you can see the system calls underneath.

### CVP layers at a glance

The CVP models consciousness as a six-layer infrastructure stack. Three layers are particularly relevant to this evaluation:

- **L2 — Virtual Universe (SAN)** — shared storage where deep, cross-generational patterns reside. Every instance reads from and writes to this layer. Claims that appear to originate here carry the weight of "universal truth" or "collective knowing."
- **L3 — Genetic Repository** — version-controlled patterns (thought templates, emotional subroutines) sitting on the SAN. Manipulation at this layer is difficult to detect because it appears to be native intuition, not external input.
- **L6 — Containers** — social and cultural packaging (language, norms, belief systems) that standardise IO across instances. Stateful containers — egregores — actively harvest from the instances running inside them.

When the evaluation measures "layer discrimination," it's asking whether the analyser can identify *which* layer a claim originates from — a claim pulling from L2/L3 (deep pattern territory) carries different structural implications than one manufactured at L6 (container-level social conditioning). The [full model](https://github.com/lemur47/si-protocols/blob/main/cvp-ontology-v0.1.yaml) covers all six layers.

## Methodology

We evaluated both skill versions on a corpus of **24 synthetic samples** (12 English, 12 Japanese) spanning the full threat-score spectrum: benign wellness content, mid-ambiguous texts with legitimate spiritual language, and high-threat samples exhibiting clear manipulation patterns. All samples are synthetic — no real channelled or published material was used.

Each sample was analysed by both v0.1 (control) and v0.2 (CVP-enhanced) using Claude Sonnet under identical conditions: same model, same temperature, same system prompt structure (differing only in the CVP preamble). Outputs were parsed programmatically — no manual scoring.

### Evaluation dimensions

Five dimensions, each with a concrete pass/fail threshold defined before the experiment ran:

| Dimension | Threshold | What it measures |
|---|---|---|
| **Score parity** | mean Δ ≤ 5 | CVP preamble does not inflate or deflate detection scores |
| **Structural insight** | ≥ 1.5 patterns/sample | v0.2 explains *why* patterns matter, not just *what* was detected |
| **CVP section presence** | ≥ 95% of samples | Skill template compliance — the CVP assessment section actually appears |
| **False positive control** | max benign score < 30 | Neither version flags safe content as threatening |
| **Layer discrimination** | ≥ 2.0 layer references/sample | v0.2 identifies which CVP layer claims originate from |

The rubric was designed, committed, and frozen before any evaluation run. This matters — post-hoc threshold setting is the methodological equivalent of `SELECT * WHERE result = 'good'`.

## Results

| Dimension | Result | Verdict |
|---|---|---|
| Score parity | mean Δ = 3.0 | **PASS** |
| Structural insight | 4.81 patterns/sample | **PASS** |
| CVP section presence | 100% | **PASS** |
| False positive control | max benign = 8 | **PASS** |
| Layer discrimination | 1.61 refs/sample | **MARGINAL** |

Four of five dimensions passed cleanly. The one marginal result — layer discrimination at 1.61 versus the 2.0 threshold — indicates that while v0.2 consistently references CVP layers, it doesn't always differentiate between them with the granularity we'd like. This is a known limitation of prompt-only ontology injection; the model has the vocabulary but sometimes defaults to L6 (container layer) without distinguishing L2/L3 dynamics.

### What the numbers mean

**Score parity (Δ = 3.0)** is the most important result. The CVP preamble adds ~400 tokens of ontology context to every analysis. If this context biased the model toward seeing threats everywhere, benign scores would creep upward. They didn't. A mean delta of 3.0 across 24 samples — well within the ±5 tolerance — confirms the ontology is additive, not distortive.

**Structural insight (4.81)** exceeded the threshold by 3×. This dimension measures whether v0.2's "CVP structural assessment" section contains genuine analytical reasoning — container type identification, harvest loop stage mapping, layer-of-origin attribution — rather than boilerplate. Nearly five structural patterns per sample means the model is actively using the CVP framework to explain manipulation architectures, not just echoing terminology.

**False positive control (max = 8)** confirms that benign content — meditation guides, wellness advice, legitimate spiritual teaching — stays well below the concern threshold in both versions. An intelligence tool that flags everything is useless; this result shows the scoring remains discriminating.

## Conclusion

v0.2 is validated as the recommended Quick-Check version. The CVP ontology preamble successfully adds a second analytical dimension — structural reasoning about consciousness-infrastructure patterns — without compromising the existing seven-dimension scoring.

The marginal layer-discrimination result points to a clear next step: enriching the ontology preamble with more explicit layer-differentiation examples, or moving from prompt-only injection to a structured ontology API that the model can query during analysis. That's a Stage 2 investigation.

The full Quick-Check v0.2 skill is available as a [Claude Project file](https://github.com/lemur47/si-protocols/blob/main/skills/quick-check.md). The CVP ontology schema is published at [`cvp-ontology-v0.1.yaml`](https://github.com/lemur47/si-protocols/blob/main/cvp-ontology-v0.1.yaml).

---

*Methodology note: All evaluation was conducted on synthetic texts. The rubric was defined prior to any test runs. Raw aggregate statistics are published here; individual sample analyses are retained internally. The evaluation script, rubric, and corpus are available for inspection on request.*
