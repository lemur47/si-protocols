# Roadmap

What we're building and when. For strategic direction, positioning, IP model, and revenue sequence, see [STRATEGY.md](STRATEGY.md). For architectural reasoning, see [DESIGN.md](DESIGN.md).

**Last synced from PMO:** 2026-03-25

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

Both sites live on Cloudflare Pages:

- **spiritualintelligence.dev** — [quickstart](https://spiritualintelligence.dev/docs/quickstart/), [library reference](https://spiritualintelligence.dev/docs/library/), [API reference](https://spiritualintelligence.dev/docs/api/), [architecture deep-dive](https://spiritualintelligence.dev/docs/architecture/) with three SI-branded SVG diagrams, [blog](https://spiritualintelligence.dev/blog/) (two posts)
- **spiritualintelligence.cc** — seven educational pages covering threat modelling, common threats, the virtualisation model, egregores, misconceptions, cybersecurity/privacy

### Infrastructure

- **R2 classified storage** — Cloudflare R2 for internal evaluation data and operational artefacts
- **Classification gate** — pre-commit hook preventing classified content from reaching public branches
- **Airtable PMO** — Projects, Sprints, Work Items, Decisions, Documents
- **17 pre-commit hooks** — ruff, pyright, pytest, opengrep, osv-scanner, gitleaks, Astro build checks

---

## Phase 1: Foundation (Months 1–3)

### note.com launch

- Free briefings in SAER format (状況→分析→評価→推奨)
- Audio briefing pilot: MP3/AAC uploads, voice-led delivery making rigorous analysis accessible (CEO-led)
- Paid counterintelligence reports (subscription magazine)

### Content expansion

- **.cc** — expand educational pages
- **.dev** — tutorial series, integration examples

### Web demo MVP

- Svelte + Astro interactive interface on .dev
- Paste text, see threat score with dimension breakdown
- Zero install, zero data collection
- Embeddable widget version for .cc

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
- **note.com** — regular cadence, JA community narrative

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
