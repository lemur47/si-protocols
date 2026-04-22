# Roadmap

What we're building and when. For strategic direction, see [STRATEGY.md](STRATEGY.md). For architectural reasoning, see [DESIGN.md](DESIGN.md). For the technical stack, see [STACK.md](STACK.md).

**Sprint cadence:** 1 week.

---

## Shipped

- **Topology module v1** — fractal-topology claim analysis; rule and Anthropic engines; SVG/JSON output; English and Japanese support
- **CVP ontology v0.1** — [machine-readable schema](https://github.com/lemur47/si-protocols/blob/main/cvp-ontology-v0.1.yaml); open analytical fragment covering the layer model L0 through L6, container taxonomy, threat pattern schemas, seven analysis dimensions, four classification axes
- **Quick-Check v0.2** — CVP-enhanced Claude Skill; A/B validated on 24 samples ([results](https://spiritualintelligence.dev/blog/ab-evaluation-quick-check-v02/))
- **Two-domain web presence** — [spiritualintelligence.dev](https://spiritualintelligence.dev) and [spiritualintelligence.cc](https://spiritualintelligence.cc) live on Cloudflare Pages; cross-linked via JSON-LD
- **note.com presence** — two notes published in SAER format (状況→分析→評価→推奨)
- **PMO and CI posture** — Airtable work-item flow, classification gate, Dependabot, full pre-commit chain

For the current state of any of these, see [STACK.md](STACK.md).

---

## Phase 1: Foundation

What the strategy needs shipped to start working in the market.

- **Web demo MVP** — browser analysis tool on `.dev`, embeddable on `.cc`; zero install, zero data collection
- **note.com expansion** — audio briefing pilot (CEO-led); paid counterintelligence reports
- **Content filling** — `.cc` pattern library; `.dev` tutorial series; `llms.txt` / `llms-full.txt` for AI agent discoverability

---

## Phase 2: Reach

What gets the tools into daily use.

- **Chrome extension MVP** — right-click analysis on any webpage; local-only processing; landing page on `.cc`
- **Batch analysis** — multiple texts compared side-by-side
- **note.com cadence** — two to three notes per month sustained

---

## Phase 3: Community and ontology

What opens the technical surface up for external engagement.

- **Ontology API** — machine-readable CVP as a queryable service with developer tooling; first step toward architectural IP licensing (see [STRATEGY.md](STRATEGY.md) § Revenue Sequence)
- **CVP ontology v0.2** — adds WAN as a cross-cutting attribute on traffic descriptors (not a new layer); partial-disclosure posture preserved
- **Counterintelligence integration** — exposure scoring, container-escape detection, egregore signature matching
- **Language expansion** — EN and JA marker sets maintained by the core team; additional languages considered only through trusted, named partnerships (si-protocols does not accept anonymous contributions — see [STRATEGY.md](STRATEGY.md) § Principles)

---

## Not in scope

- Additional language support beyond EN and JA until language expansion process is established
- Hosted analysis services (outside data sovereignty commitment — see [STRATEGY.md](STRATEGY.md))
- Mobile applications
- Social-media integrations beyond the Chrome extension
- Anonymous contribution channels (open-core licensing does not imply open collaboration)
