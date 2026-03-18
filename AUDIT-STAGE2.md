# Stage 2 Readiness Audit

**Date:** 2026-03-18
**Sprint:** Sprint 1
**Assignee:** Claude Code
**Classification:** Internal
**Branch:** `feature/stage2-audit`

---

## Executive Summary

1. **The codebase is structurally ready for Stage 2.** No circular dependencies, no blocking tech debt, and the package layout can absorb an ontology submodule cleanly (mirroring the existing `topology/` pattern).
2. **Test health is strong:** 315 tests, 100% pass rate, 93.66% coverage (threshold: 70%). One intentional stub (`OllamaEngine`) accounts for the only file at 0%.
3. **The .cc site is complete** against ROADMAP Phase 1 (5/5 required pages + 3 bonus). The .dev site is missing 3 promised items: architecture deep-dive, contributing guide, and web demo MVP.
4. **CVP naming inconsistency identified and resolved:** the canonical expansion is "Consciousness Virtualisation Platform" (post-audit decision). `docs/CVP.md` and other files using "Cosmic-Virtualisation-Protocol" need updating; the blog post was already correct.
5. **Japanese marker coverage exceeds English** (190 vs 171 core markers), but three candidate expansion categories (`JA_ISOLATION_PHRASES`, `JA_UNFALSIFIABLE_SOURCES`, `JA_PSEUDOSCIENCE_PHRASES`) are net new — no stubs exist.

---

## 1. CVP Terminology Consistency

**Source of truth:** `docs/CVP.md`

### Critical Finding

**Post-audit decision (2026-03-18):** The canonical CVP expansion has been determined as **"Consciousness Virtualisation Platform"**, not "Cosmic-Virtualisation-Protocol". Rationale: "Platform" is architecturally correct (CVP models a virtualisation platform, not a protocol); "Consciousness" precisely describes what is being virtualised; "Cosmic" is vague and would trigger the project's own vagueness dimension.

| File | Line | Current | Should Be |
|------|------|---------|-----------|
| `docs/CVP.md` | 1 | "Cosmic-Virtualisation-Protocol (CVP)" | "Consciousness Virtualisation Platform (CVP)" |
| Other files referencing "Cosmic-Virtualisation-Protocol" | various | old form | "Consciousness Virtualisation Platform" |

The blog post `site/src/content/blog/the-guru-retreat-as-egregoric-parasite.md:14` already uses the correct form.

### Verified Consistent

- **Layer numbering (L1–L6):** consistent across all 11 CVP-related files.
- **Layer names:** Bare Metal, Virtual Universe (SAN), Genetic Repository, Environmental Switch, Mental Instances (VMs), Illusion Layer — all correct everywhere.
- **Stateless vs stateful container distinction:** consistently applied in `site-cc/` pages, `docs/CVP.md`, and blog posts.
- **No orphaned or undefined layer references** (no L0, L7+, or missing layers).
- **Japanese translations:** CVP terminology appears only in English across both sites. Japanese content is limited to note.com (external, not in this repo). No missing JA translations within the repo scope.

---

## 2. Technical Debt Blocking Stage 2

### No Blockers Identified

The codebase is architecturally clean. Key findings below are improvement opportunities, not blockers.

### High Priority (fix before 0.2.0 release)

| Finding | File | Line(s) | Why It Matters |
|---------|------|---------|----------------|
| README references removed `bandit` command | `README.md` | 78 | Users following README get a command that doesn't work; CI uses `opengrep` + `osv-scanner` |
| Python 3.14 classifier contradicts CLAUDE.md | `pyproject.toml` | 17 | Classifier claims 3.14 support but spaCy doesn't support it yet |

### Medium Priority (improve before ontology work)

| Finding | File | Line(s) | Why It Matters |
|---------|------|---------|----------------|
| CI missing `app/` in lint steps | `.github/workflows/ci.yml` | 19–20 | Pre-commit lints `app/` but CI doesn't — drift between local and CI checks |
| Root `__init__.py` has no `__all__` or public API exports | `src/si_protocols/__init__.py` | — | `topology/` has a clean 37-line `__all__`; root package should follow same discipline before ontology module is added |
| `callable` type annotation (lowercase) | `src/si_protocols/marker_registry.py` | 97 | Suppressed with `# type: ignore`; should be `Callable[[], MarkerSet]` from `collections.abc` |

### Healthy Patterns

- **No TODO/FIXME/HACK comments** found anywhere in the codebase.
- **Lazy imports** used strategically to avoid circular dependencies (e.g., `output.py` uses `TYPE_CHECKING` for `ThreatResult`).
- **Dependency graph is acyclic:** `marker_registry ← threat_filter, topology/*, output`; `app/main → threat_filter`.
- **Pre-commit hooks** are comprehensive and well-ordered: ruff → gitleaks → opengrep → osv-scanner → pyright → pytest → Astro checks.

### Ontology Module Integration Path

The existing `topology/` subpackage provides a proven template:

```
src/si_protocols/
  ontology/               # new — mirror topology/ structure
    __init__.py            # export public API with __all__
    types.py               # frozen dataclasses, tuples not lists
    loader.py              # YAML loading
    validator.py           # schema validation
    cli.py                 # si-ontology entry point (lazy imports)
```

---

## 3. Marker Coverage Analysis

### Core Marker Counts (EN vs JA)

| Category | EN | JA | Gap | Status |
|----------|----|----|-----|--------|
| Vague adjectives | 18 | 16 | −2 | JA slightly under |
| Authority phrases | 10 | 14 | +4 | JA exceeds |
| Urgency patterns | 12 | 14 | +2 | JA exceeds |
| Fear words | 17 | 21 | +4 | JA exceeds |
| Fear phrases | 8 | 9 | +1 | Near parity |
| Euphoria words | 16 | 23 | +7 | JA significantly exceeds |
| Euphoria phrases | 6 | 6 | 0 | Perfect parity |
| Unfalsifiable source phrases | 21 | 21 | 0 | Perfect parity |
| Unnamed authority phrases | 20 | 20 | 0 | Perfect parity |
| Verifiable citation markers | 10 | 10 | 0 | Perfect parity |
| Contradiction pairs | 9 | 9 | 0 | Perfect parity |
| Commitment escalation (3 tiers) | 33 | 36 | +3 | JA slightly exceeds |
| **Totals** | **171** | **190** | **+19** | **JA +11%** |

JA also has 132 additional keyword/stem entries (7 extension fields) for morphological matching — these have no EN equivalent and are architecturally appropriate.

### Three Candidate Expansions

| Field | Status |
|-------|--------|
| `JA_ISOLATION_PHRASES` | **Not found** — net new work required |
| `JA_UNFALSIFIABLE_SOURCES` | **Not found** — net new work required |
| `JA_PSEUDOSCIENCE_PHRASES` | **Not found** — net new work required |

None of these exist as stubs, fields in `MarkerSet`, or placeholder definitions. Adding them requires modifying the `MarkerSet` dataclass in `marker_registry.py` and creating corresponding entries in `markers_ja.py`.

### Dimension Alignment

All 12 `MarkerSet` fields map correctly to the 7 analysis dimensions in `threat_filter.py` (lines 202–333). The Quick-Check Skill (`skills/quick-check.md`) encodes the same 7 dimensions with matching weights and scoring logic.

---

## 4. Website Content Gaps

### spiritualintelligence.cc — 100% Complete

All 5 ROADMAP Phase 1 pages are published, plus 3 bonus pages:

| Page | File | Status |
|------|------|--------|
| Why Spiritual Intelligence Matters | `site-cc/src/content/pages/why-spiritual-intelligence-matters.md` | ✓ |
| Threat Modelling for Spiritual Content | `site-cc/src/content/pages/threat-modelling.md` | ✓ |
| Common Threats and Patterns | `site-cc/src/content/pages/common-threats.md` | ✓ |
| Common Misconceptions | `site-cc/src/content/pages/common-misconceptions.md` | ✓ |
| Cybersecurity and Privacy | `site-cc/src/content/pages/cybersecurity-and-privacy.md` | ✓ |
| Mapping Claims and Patterns *(bonus)* | `site-cc/src/content/pages/mapping-claims-and-patterns.md` | ✓ |
| The Virtualisation Model *(bonus)* | `site-cc/src/content/pages/the-virtualisation-model.md` | ✓ |
| Egregores *(bonus)* | `site-cc/src/content/pages/egregores.md` | ✓ |

10 SVG images in `site-cc/public/images/` — all present and correctly linked.

### spiritualintelligence.dev — 3 Gaps

Published: homepage, docs (quickstart, library, API reference), 4 blog posts.

| ROADMAP Commitment | Status | Severity |
|-------------------|--------|----------|
| Architecture deep-dive | **Missing** | Medium |
| Contributing guide | **Missing** | Medium |
| Web demo MVP (Svelte + Astro) | **Missing** | High |

### Blog Posts (4 published)

1. "Introducing si-protocols" (2026-02-08)
2. "Beyond NLP: Detecting Deception Without LLMs" (2026-02-09)
3. "Hands-On Threat Analysis: A Step-by-Step Tutorial" (2026-02-15)
4. "The Guru Retreat as Egregoric Parasite" (2026-03-07)

### Broken Links: None Detected

All internal navigation verified working across both sites and cross-domain links.

### Old Positioning: Clean

No pre-"we help AIs" language found. Content consistently frames SI as a tool for both humans and (implicitly) AI reasoning enhancement.

---

## 5. Test and Example Coverage

### Test Suite

| Metric | Value |
|--------|-------|
| Total tests | 315 |
| Passed | 315 (100%) |
| Failed | 0 |
| Duration | ~3.2s |
| Coverage | **93.66%** |
| Threshold | 70% |

### Coverage by File

| File | Cover | Notes |
|------|-------|-------|
| `__init__.py` | 100% | — |
| `marker_registry.py` | 100% | — |
| `markers.py` | 100% | — |
| `markers_ja.py` | 100% | — |
| `output.py` | 100% | — |
| `threat_filter.py` | 92% | Uncovered: JA keyword escalation branch (lines 107, 115–131), CLI guard (line 432) |
| `topology/__init__.py` | 100% | — |
| `topology/anthropic_engine.py` | 83% | Uncovered: real API call path (lines 75–88), mocked in tests |
| `topology/cli.py` | 91% | Minor branch edges |
| `topology/engine.py` | 100% | — |
| `topology/ollama_engine.py` | **0%** | Intentional stub — raises `NotImplementedError` |
| `topology/output.py` | 94% | Uncovered: `super().default()` fallback (line 20) |
| `topology/rule_engine.py` | 92% | Scattered branch edges |
| `topology/svg_renderer.py` | 99% | — |
| `topology/topology_builder.py` | 98% | — |
| `topology/types.py` | 100% | — |

### Example Files (7 total)

| File | Threat Profile |
|------|---------------|
| `synthetic_benign.txt` | Low (benign) |
| `synthetic_suspicious.txt` | High (manipulative) |
| `synthetic_escalation.txt` | High (escalation) |
| `synthetic_tradition_markers.txt` | High (multi-tradition) |
| `synthetic_topology_suspicious.txt` | High (topology input) |
| `synthetic_suspicious_ja.txt` | High (JA) |
| `synthetic_topology_suspicious_ja.txt` | High (JA topology) |

**Gap:** No mid-range / ambiguous examples (score ~40–60). The test corpus needs expansion for the A/B evaluation (Sprint 1 work item #3 requires 20+ samples including ambiguous range).

### Untested Public Functions

- **`OllamaEngine`** — entirely untested (no test validates `NotImplementedError` or protocol conformance).
- **`save_svg()`** and **`render_topology_json()`** — no direct unit tests, but covered indirectly via CLI integration tests.

### Test Infrastructure

- **No shared `conftest.py`** — tests use pytest built-in fixtures. Acceptable for current scale.
- **`@pytest.mark.slow`** properly configured with `--strict-markers`. 70+ tests marked.
- **Coverage tool** (`pytest-cov>=6.0`) is a declared dev dependency with `fail_under = 70` in `pyproject.toml`.

---

## 6. Skills Alignment

### Quick-Check Skill Version

**Discrepancy found:**

| Source | Version |
|--------|---------|
| `skills/quick-check.md` (line 3) | v0.1 |
| `skills/quick-check.md` (line 141) | v0.1 |
| Airtable Documents table | v2.0 |

**Action required:** Reconcile — either update the skill file to v2.0 or correct the Airtable entry.

### Weight Alignment: Perfect Match

| Dimension | Skill | `threat_filter.py` | Match |
|-----------|-------|---------------------|-------|
| Vagueness | 17% | `* 17` (line 313) | ✓ |
| Authority claims | 17% | `* 17` (line 314) | ✓ |
| Urgency/fear | 13% | `* 13` (line 315) | ✓ |
| Emotional manipulation | 13% | `* 13` (line 316) | ✓ |
| Logical contradictions | 13% | `* 13` (line 317) | ✓ |
| Source attribution | 13% | `* 13` (line 318) | ✓ |
| Commitment escalation | 14% | `* 14` (line 319) | ✓ |

### Scoring Logic: Perfect Match

All 7 dimension calculations in the Skill match the Python implementation to exact precision:
- Vagueness: count / text length ✓
- Authority: 15 points per claim, capped at 100 ✓
- Urgency: 20 points per pattern ✓
- Emotion: 12 points per word, contrast bonus up to +50 ✓
- Contradiction: 30 points per pair ✓
- Source attribution: 12 per suspicious, −15 per verifiable ✓
- Escalation: gradient-based early-to-late detection ✓

### Marker Sampling: Aligned

100% of marker examples cited in the Skill exist in `markers.py` / `markers_ja.py`. The Skill intentionally samples representative examples (e.g., 6/19 authority phrases, 10/21 vague adjectives) rather than listing exhaustively. All 6 tradition categories match.

### Minor Gaps

- **3 tradition-specific contradiction pairs** (prosperity gospel, cult, fraternal) are in `markers.py` but not listed in the Skill. Acceptable simplification for a quick-check tool.
- **Heuristic layer** correctly noted as excluded from the Skill (tech dimensions only).
- **Topology module** not referenced in the Skill. Correct — it is a separate analysis path.

### Other Skills

Only `skills/quick-check.md` exists. No other skill files found.

---

## Prioritised Refactoring Candidates

| # | What to Fix | Where | Why It Matters for Stage 2 | Effort |
|---|-------------|-------|---------------------------|--------|
| 1 | Fix CVP name expansion ("Cosmic-Virtualisation-Protocol" → "Consciousness Virtualisation Platform") | `docs/CVP.md` + other files using old form | Canonical name decided post-audit; blog post was already correct | Small |
| 2 | Update README to replace `bandit` with `opengrep` + `osv-scanner` | `README.md:78` | Users following README get broken commands | Small |
| 3 | Remove Python 3.14 classifier | `pyproject.toml:17` | Contradicts CLAUDE.md; spaCy doesn't support 3.14 | Small |
| 4 | Add `app/` to CI lint steps | `.github/workflows/ci.yml:19–20` | Align CI with pre-commit (which already lints `app/`) | Small |
| 5 | Reconcile Quick-Check version (v0.1 in file vs v2.0 in Airtable) | `skills/quick-check.md` + Airtable Documents | Prevents confusion when creating v3 | Small |
| 6 | Define root `__all__` with public API exports | `src/si_protocols/__init__.py` | Ontology module needs a coherent export surface | Small |
| 7 | Fix `callable` type annotation | `src/si_protocols/marker_registry.py:97` | Currently suppressed with `type: ignore`; should use `Callable` | Small |
| 8 | Add `OllamaEngine` stub test | `tests/` | Only file at 0% coverage; one test validating `NotImplementedError` would close it | Small |
| 9 | Create architecture deep-dive page on .dev | `site/src/content/docs/` | ROADMAP Phase 1 commitment; needed for contributor onboarding | Medium |
| 10 | Create contributing guide on .dev | `site/src/content/docs/` | ROADMAP Phase 1 commitment; needed before community contributions | Medium |
| 11 | Add mid-range synthetic examples | `examples/` | Current corpus has only benign + high-threat; A/B evaluation needs ambiguous range (~40–60) | Medium |
| 12 | Implement web demo MVP | `site/` | ROADMAP Phase 1 commitment; "top of funnel" conversion tool | Large |

---

## Metrics Snapshot

| Metric | Value |
|--------|-------|
| **Tests** | 315 (100% pass) |
| **Coverage** | 93.66% (threshold: 70%) |
| **EN markers** | 171 core |
| **JA markers** | 190 core + 132 keyword extensions |
| **Pages (.cc)** | 8 (5 required + 3 bonus) |
| **Pages (.dev)** | 7 (3 docs + 4 blog posts) |
| **Example files** | 7 (1 benign, 6 high-threat; 5 EN, 2 JA) |
| **Skill files** | 1 (`quick-check.md`) |
| **CVP terminology errors** | 1 |
| **Broken links** | 0 |
| **TODO/FIXME/HACK comments** | 0 |
| **Circular dependencies** | 0 |
