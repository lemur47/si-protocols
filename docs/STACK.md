# STACK

**What we run.** For strategic *why*, see [STRATEGY.md](STRATEGY.md). For architectural *why*, see [DESIGN.md](DESIGN.md). For *when* things land, see [ROADMAP.md](ROADMAP.md).

This document is honest about the state of the build. Where something is planned rather than shipped, it says so.

Classification: Open.

---

## Runtime

The core library is Python; the public-facing sites are Astro.

| Component | Version / spec | Notes |
|---|---|---|
| Python | `>=3.12` (dev on 3.13; CI tests both) | spaCy does not yet support 3.14 |
| Package manager | `uv` | Locked via `uv.lock`; Dependabot reviews weekly |
| NLP | `spaCy` (`en_core_web_sm`, `ja_core_news_sm`) | Lazy-loaded to avoid import-time side effects |
| API surface | `FastAPI` | Local-only — `uvicorn app.main:app` on `127.0.0.1:8000` |
| Output | `Rich` (terminal), `xml.etree` (SVG) | No external SVG/graphing packages |
| Node (Astro sites) | `Node.js` (LTS track) | Two Astro sites: `site/` (.dev), `site-cc/` (.cc) |
| Immutability | `frozen` dataclasses, `tuple` not `list` | Full object-graph hashability |

---

## Infrastructure

Deployment is edge-first: static content served by Cloudflare Pages; persistent state lives in R2. The API is local-only by design — no hosted analysis service.

| Layer | Tool | Status |
|---|---|---|
| Static hosting (`.dev`, `.cc`) | Cloudflare Pages | Shipped — JSON-LD, per-page metadata, cross-site `sameAs` links |
| Object storage | Cloudflare R2 | Shipped — bucket `si-classified` for internal artefacts; `si-open` (planned) for public assets |
| Edge compute | Cloudflare Workers + Durable Objects | **Planned** for the Stage 5 CVP Simulation Testbed |
| Dev environment | Isolated dev VM | Operator-local configuration |
| Domain | `spiritualintelligence.dev`, `spiritualintelligence.cc` | Both live |

The local-only principle is architectural, not aspirational — it is enforced by the absence of any hosted analysis endpoint, not by promise.

---

## AI / LLM layer

Three tiers of analysis engine, plus a machine-readable ontology and skill-based distribution.

| Component | Role | Status |
|---|---|---|
| `RuleEngine` (Tier 0) | Deterministic, local spaCy + markers | Shipped, default engine |
| `AnthropicEngine` (Tier 1) | Claude API claim extraction (opt-in extra) | Shipped |
| `OllamaEngine` (Tier 2) | Future local-LLM | Stub only |
| CVP ontology | Machine-readable YAML (`cvp-ontology-v0.1.yaml`) | Shipped — open analytical fragment |
| Quick-Check skill | Zero-install Claude Project skill; doubles as an empirical instrument for CVP impact on reasoning | v0.2 shipped — A/B validated on 24 samples |
| Briefing skill | Claude Project skill for SAER-format structured briefings | Scaffold present; briefing #003 in Sprint 4 backlog |

The tiered engines implement a single `AnalysisEngine` protocol, so a new engine slots in without changing the public API.

---

## PMO stack

The programme is managed as code: work items, sprints, and decisions are structured records, not meeting notes.

| Surface | Purpose | Notes |
|---|---|---|
| Airtable base | Projects, Sprints, Work Items, Decisions, Documents | Specific IDs and protocol in `CLAUDE-internal.md` (operator-local) |
| GitHub (`lemur47/si-protocols`) | Public monorepo: library, app, sites, skills, ontology, docs, scripts | `feature/*` branch discipline, PR review, Dependabot |
| Claude Code | DevSecOps execution (isolated dev environment) | Reads `## Spec`, writes `## Execution Log` |
| Claude (chat) | CTO planning & review | Drafts specs, reviews `## Execution Log`, writes `## Review` |

The Structured Notes Protocol on Work Items (`## Spec` → `## Execution Log` → `## Review`) removes the human bridge between CTO and Claude Code. Both read and write to the same state store.

---

## CI & security

Every commit runs through a gate chain before it can land on `main`. The principle is defence-in-depth: each hook catches a different failure mode.

| Stage | Hook | What it catches |
|---|---|---|
| Lint / format | `ruff` (check + format) | Style drift, unused imports, bug-prone patterns (`B`, `S`, `UP`, `I`) |
| Secrets | `gitleaks` | API keys, tokens, private keys |
| SAST | `opengrep` (`src/`, `app/`) | Known vulnerable patterns |
| Dep vulns | `osv-scanner` (`--recursive`) | CVEs across `uv.lock`, `site/package-lock.json`, `site-cc/package-lock.json` |
| Types | `pyright` | Type regressions |
| Tests | `pytest` (coverage `fail_under = 70`) | Behaviour regressions |
| Astro | `astro check` (per site) | Content-collection schema drift |
| Classification | `scripts/classification-gate.py` | Prevents Internal / Classified content reaching the public repo |
| Hygiene | trailing whitespace, large files, private keys, YAML/TOML/JSON validity | Cheap guardrails |

CI matrix: Python 3.12 and 3.13 on GitHub Actions. Dependabot runs weekly on pip, npm, and GitHub Actions; major-version jumps are reviewed before merge (some are deferred — see `.github/dependabot.yml` and the Decisions record that scheduled them).

---

## Content & distribution

Dual-runtime: one source, two audiences.

| Channel | Audience | Optimisation | Status |
|---|---|---|---|
| `spiritualintelligence.dev` | Developers, AI systems | Semantic markup, JSON-LD, structured claims, citability | Shipped — docs, library/API reference, architecture deep-dive, blog |
| `.dev` AI-first surface (`llms.txt`, `llms-full.txt`) | AI agents crawling the site | Machine-addressable table of contents per [llmstxt.org](https://llmstxt.org); aligned content chunks for LLM citation | **Planned** — concrete expression of the "AI-first epistemic infrastructure" posture from STRATEGY.md |
| `spiritualintelligence.cc` | Practitioners, thought leaders, curious public | Accessible prose, emotional resonance, educational | Shipped — eight pages (threat modelling, egregores, privacy, etc.) |
| `note.com` (JP) | Japanese practitioners | SAER-format briefings, nerdy/techie voice | Two notes published; target 2–3/month |
| Audio briefings | Trust-layer for non-readers | Voice, prosody, narrative | Planned |

Cross-site linking via `sameAs` JSON-LD. Same codebase, same core technology, different editorial voice — not two products.

---

## What is deliberately missing

A few things people ask about that we do not run and will not:

- **Hosted analysis API** — we do not operate one. Data sovereignty is an organisational commitment, not a feature we ration.
- **Content database** — we do not store analysed text, user behaviour, or results on our infrastructure.
- **Opaque ML classifier** — markers are version-controlled lists; every score is traceable to a rule. No black boxes as the primary scoring mechanism.

If a new component would break any of those three, it does not ship here.
