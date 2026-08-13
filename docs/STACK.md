# STACK

**What we run.** For strategic *why*, see [STRATEGY.md](STRATEGY.md). For architectural *why*, see [DESIGN.md](DESIGN.md). For *when* things land, see [ROADMAP.md](ROADMAP.md).

This document is honest about the state of the build. Where something is planned rather than shipped, it says so.

Classification: Open.

---

## Runtime

The core library is Python. This repository is the toolkit only — the former editorial websites were handed over to a separate web line in July 2026.

| Component | Version / spec | Notes |
|---|---|---|
| Python | `>=3.12` (dev on 3.13; CI tests both) | spaCy does not yet support 3.14 |
| Package manager | `uv` | Locked via `uv.lock`; Dependabot reviews weekly |
| NLP | `spaCy` (`en_core_web_sm`, `ja_core_news_sm`) | Lazy-loaded to avoid import-time side effects |
| API surface | `FastAPI` | Local-only — `uvicorn app.main:app` on `127.0.0.1:8000` |
| Output | `Rich` (terminal), `xml.etree` (SVG) | No external SVG/graphing packages |
| Immutability | `frozen` dataclasses, `tuple` not `list` | Full object-graph hashability |

---

## Infrastructure

Persistent state lives in R2. The API is local-only by design — no hosted analysis service, and since the web handover this repository deploys nothing at all.

| Layer | Tool | Status |
|---|---|---|
| Object storage | Cloudflare R2 | Shipped — internal artefacts; public-asset bucket still planned |
| Edge compute | Cloudflare Workers + Durable Objects | **Planned** for the Stage 5 CVP Simulation Testbed |
| Dev environment | Isolated dev VM | Operator-local configuration |
| Domains | `spiritualintelligence.dev`, `spiritualintelligence.cc` | **Retired** — content migrated to ohoran.org; both domains now serve redirects only |

The local-only principle is architectural, not aspirational — it is enforced by the absence of any hosted analysis endpoint, not by promise.

---

## AI / LLM layer

Three tiers of analysis engine, plus a machine-readable ontology and skill-based distribution.

| Component | Role | Status |
|---|---|---|
| `RuleEngine` (Tier 0) | Deterministic, local spaCy + markers | Shipped, default engine |
| `AnthropicEngine` (Tier 1) | Claude API claim extraction (opt-in extra) | Model pin and request shape restored for the current generation — **verified against a live endpoint 2026-08-13** (EN + JA) |
| `OllamaEngine` (Tier 2) | Future local-LLM | Stub only |
| CVP ontology | Machine-readable YAML (`cvp-ontology-v0.1.yaml`) | Shipped — open analytical fragment |
| Quick-Check skill | Zero-install Claude skill; doubles as an empirical instrument for CVP impact on reasoning | v0.3 shipped — Agent Skill format; carries forward the v0.2 A/B validation on 24 samples |
| Briefing skill | Claude skill for SAER-format structured briefings | Scaffold present; publication cadence belongs to the separate web line |

The tiered engines implement a single `AnalysisEngine` protocol, so a new engine slots in without changing the public API.

---

## PMO stack

The programme is managed as code: work items, sprints, and decisions are structured records, not meeting notes.

| Surface | Purpose | Notes |
|---|---|---|
| Airtable base | Projects, Sprints, Work Items, Decisions | Specific IDs and protocol in `CLAUDE.local.md` (operator-local) |
| GitHub (`lemur47/si-protocols`) | Public repo: library, app, skills, ontology, docs, scripts | `feature/*` branch discipline, PR review, Dependabot |
| Claude Code | CTO function and DevSecOps execution (isolated dev environment) | Drafts specs, executes, writes `## Execution Log` |
| Claude (chat) | Design and ad-hoc research | No longer authors specs or reviews work items |

The Structured Notes Protocol on Work Items (`## Spec` → `## Execution Log` → `## Review`) keeps intent, execution and feedback in one record. Claude Code holds both the CTO and DevSecOps roles, so objective review comes from a fresh reviewer without authoring context, and the approval gate is human.

---

## CI & security

Every commit runs through a gate chain before it can land on `main`. The principle is defence-in-depth: each hook catches a different failure mode.

| Stage | Hook | What it catches |
|---|---|---|
| Lint / format | `ruff` (check + format) | Style drift, unused imports, bug-prone patterns (`B`, `S`, `UP`, `I`) |
| Secrets | `gitleaks` | API keys, tokens, private keys |
| SAST | `opengrep` (`src/`, `app/`) | Known vulnerable patterns |
| Dep vulns | `osv-scanner` (`--recursive`) | CVEs across `uv.lock` |
| Types | `pyright` | Type regressions |
| Tests | `pytest` (coverage `fail_under = 70`) | Behaviour regressions |
| Classification | `scripts/classification-gate.py` | Prevents Internal / Classified content reaching the public repo |
| Hygiene | trailing whitespace, large files, private keys, YAML/TOML/JSON validity | Cheap guardrails |

CI matrix: Python 3.12 and 3.13 on GitHub Actions. Dependabot runs weekly on the Python ecosystem; the GitHub Actions ecosystem is queued for restoration, and npm left with the websites. Major-version jumps are reviewed before merge (some are deferred — see `.github/dependabot.yml` and the Decisions record that scheduled them).

The classification gate runs twice: as a pre-commit hook, and again in CI where it is a required status check — so it cannot be skipped with `--no-verify`.

---

## Content & distribution

The dual-audience split — developers and AI agents on one side, practitioners and the curious public on the other — outlived the two sites that used to express it. Publishing now happens elsewhere; what this repository still owns is listed first.

| Channel | Audience | Optimisation | Status |
|---|---|---|---|
| This repository | Developers, AI systems | Structured markdown, machine-readable ontology, citable claims | Shipped — library and API reference, architecture, methodology docs |
| Claude skills (`skills/`) | Analysts, practitioners | Zero-install; no toolchain required | Shipped — Quick-Check v0.3, briefing scaffold |
| ohoran.org | Both audiences, one site | Editorial voice per piece rather than per domain | Live — carries the migrated `.dev` and `.cc` content |
| `spiritualintelligence.dev`, `spiritualintelligence.cc` | — | — | **Retired** — redirect shells; the content moved to ohoran.org |
| Audio briefings | Trust-layer for non-readers | Voice, prosody, narrative | Planned |

Same codebase, same core technology, different editorial voice — that was never two products, which is why one site can carry both.

---

## What is deliberately missing

A few things people ask about that we do not run and will not:

- **Hosted analysis API** — we do not operate one. Data sovereignty is an organisational commitment, not a feature we ration.
- **Content database** — we do not store analysed text, user behaviour, or results on our infrastructure.
- **Opaque ML classifier** — markers are version-controlled lists; every score is traceable to a rule. No black boxes as the primary scoring mechanism.

If a new component would break any of those three, it does not ship here.
