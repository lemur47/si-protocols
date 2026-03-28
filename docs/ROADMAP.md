# Roadmap

What we're building and when. For strategic direction, positioning, IP model, and revenue sequence, see [STRATEGY.md](STRATEGY.md). For architectural reasoning, see [DESIGN.md](DESIGN.md).

**Last synced from PMO:** 2026-03-28
**Sprint cadence:** 1 week

---

## Completed

### Topology module v1

Fractal-topology analysis extracting claims from text, classifying each along four axes, and building a layered graph:

- **Rule engine** (Tier 0) — local, deterministic, spaCy + marker heuristics
- **Anthropic engine** (Tier 1) — Claude API-based claim extraction
- **Output** — SVG visualisation (intelligence-themed dark HUD) and JSON
- **CLI** — `si-topology` with `--engine`, `--format`, `--lang`, `-o`
- **Multi-language** — English and Japanese

### CVP ontology v0.1

Machine-readable schema: [`cvp-ontology-v0.1.yaml`](https://github.com/lemur47/si-protocols/blob/main/cvp-ontology-v0.1.yaml). Six layers (L1–L6), container type taxonomy, threat pattern schemas (harvest loop, container trap), seven analysis dimensions, four topology classification axes, bilingual terminology (EN/JA). Open analytical fragment only — proprietary components listed in the YAML header.

### Quick-Check v0.2 (CVP-enhanced)

Claude Skill with CVP ontology preamble. The Skill functions as an L6 static container — both a distribution channel and an empirical instrument for measuring CVP's effect on AI reasoning. A/B evaluation on 24 samples (12 EN, 12 JA) confirmed: score parity (Δ = 3.0), structural insight (4.81/sample), FP control (max benign = 8). [Full results](https://spiritualintelligence.dev/blog/ab-evaluation-quick-check-v02/).

### Two-domain web presence

Both sites live on Cloudflare Pages, deployed from the GitHub monorepo (`site/` and `site-cc/`):

- **spiritualintelligence.dev** — [quickstart](https://spiritualintelligence.dev/docs/quickstart/), [library reference](https://spiritualintelligence.dev/docs/library/), [API reference](https://spiritualintelligence.dev/docs/api/), [architecture deep-dive](https://spiritualintelligence.dev/docs/architecture/) with three SI-branded SVG diagrams, [blog](https://spiritualintelligence.dev/blog/) (five posts including [A/B evaluation](https://spiritualintelligence.dev/blog/ab-evaluation-quick-check-v02/))
- **spiritualintelligence.cc** — eight educational pages covering threat modelling, common threats, the virtualisation model, egregores, misconceptions, cybersecurity/privacy, mapping claims and patterns, why SI matters
- **Cross-site linking** — both sites link to each other with `sameAs` JSON-LD cross-references
- **JSON-LD structured data** — Organization, WebSite, Article, TechArticle, and WebPage schemas across both sites

### note.com presence

- Two notes published; target cadence 2–3 notes/month
- Japanese-language briefings in SAER format (状況→分析→評価→推奨)

### Infrastructure

- **R2 classified storage** — Cloudflare R2 for internal evaluation data and operational artefacts
- **Classification gate** — pre-commit hook preventing classified content from reaching public branches
- **Airtable PMO** — Projects, Sprints, Work Items, Decisions, Documents
- **17 pre-commit hooks** — ruff, pyright, pytest, opengrep, osv-scanner, gitleaks, Astro build checks
- **Dependabot** — weekly automated dependency PRs for pip and npm (site/ and site-cc/)

---

## Phase 1: Foundation (Months 1–3)

### In progress

- **Web demo MVP** — architecture spike underway (Svelte + Astro integration path). Svelte interactive interface on .dev; paste text, see threat score with dimension breakdown; zero install, zero data collection; embeddable widget version for .cc
- **note.com expansion** — audio briefing pilot: MP3/AAC uploads, voice-led delivery (CEO-led); paid counterintelligence reports (subscription magazine)

### Remaining

- **.cc** — expand educational pages beyond initial eight
- **.dev** — tutorial series, integration examples

---

## Phase 2: Reach (Months 4–6)

### Chrome extension MVP

- Right-click context menu: "Analyse this text for manipulation patterns"
- Select text on any webpage → inline threat score overlay
- Local-only processing — no data leaves the browser
- Landing page on .cc

### Content expansion

- **.cc** — case studies, pattern library
- **.dev** — tutorial series, integration examples
- **note.com** — maintain 2–3 notes/month cadence, expand JA community narrative

### Batch analysis

- Analyse multiple texts and compare scores side by side

---

## Phase 3: Community & Ontology (Months 7–12)

### Ontology API

Machine-readable CVP ontology as a queryable API with developer tooling. First step toward the architectural IP licensing ambition (see [STRATEGY.md](STRATEGY.md) § Revenue Sequence).

### Counterintelligence integration

- **Phase A (Theory)** — L6 stateless/stateful container distinction, egregoric access to L3, three-layer resistance pattern, inbound/outbound CI boundaries
- **Phase B (Detection)** — exposure scoring, container escape detection, egregore signature matching

### Contributor programme

- Language contributions (community-submitted marker sets)
- Marker review process (prerequisite: design validation process to prevent adversarial submissions — see Decisions log)

### Chrome extension polish

- Settings panel, marker customisation for tradition-specific contexts

---

## Web Demo and Chrome Extension

| | Web demo | Chrome extension |
|---|---|---|
| **When** | First encounter | Daily use |
| **Where** | .dev site, embeddable on .cc | In-situ on any webpage |
| **Friction** | Zero install | One-time install |
| **Role** | Top of funnel | Retention layer |

---

## What This Roadmap Does Not Cover

- Additional language support beyond EN/JA (deferred until contributor programme established)
- Hosted analysis services (outside data sovereignty commitment — see [STRATEGY.md](STRATEGY.md))
- Mobile applications
- Social media integrations beyond the Chrome extension
