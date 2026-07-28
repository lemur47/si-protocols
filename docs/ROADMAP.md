# Roadmap

What we're building and when. For strategic direction, see [STRATEGY.md](STRATEGY.md). For architectural reasoning, see [DESIGN.md](DESIGN.md). For the technical stack, see [STACK.md](STACK.md).

**Sprint cadence:** 3 days.

---

## Shipped

- **Topology module v1** — fractal-topology claim analysis; rule and Anthropic engines; SVG/JSON output; English and Japanese support
- **CVP ontology v0.1** — [machine-readable schema](https://github.com/lemur47/si-protocols/blob/main/cvp-ontology-v0.1.yaml); open analytical fragment covering the layer model L0 through L6, container taxonomy, threat pattern schemas, seven analysis dimensions, four classification axes
- **Quick-Check v0.3** — CVP-enhanced Claude Skill, restructured to Anthropic's official Agent Skill format (`SKILL.md`); A/B validation from v0.2 carries forward unchanged, as v0.3 is a behaviour-preserving format migration ([results](https://spiritualintelligence.dev/blog/ab-evaluation-quick-check-v02/))
- **Two-domain web presence** — shipped as `spiritualintelligence.dev` and `spiritualintelligence.cc` on Cloudflare Pages, **retired July 2026**: the content migrated into ohoran.org and both domains now serve redirects only
- **AI-readable surface** — structured markdown plus the machine-readable ontology as the canonical machine-addressable format; the per-page JSON-LD and cross-site `sameAs` links left with the websites
- **note.com presence** — two notes published in SAER format (状況→分析→評価→推奨); the channel has since been repurposed for progressive book publishing
- **PMO and CI posture** — Airtable work-item flow, classification gate, Dependabot, full pre-commit chain

For the current state of any of these, see [STACK.md](STACK.md).

---

## Phase 1: Foundation

What the strategy needs shipped to start working in the market.

- **Spiritual counterintelligence product surface** — Skills, Plugins, MCP server, and CLI as the intelligence-product distribution surface; local-only and zero-install where the channel supports it
- **Dual-track content cadence** — Track 1 (R&D → Blog → Briefing) and Track 2 (Book → Blog → Briefing). Publication moved to ohoran.org with the web handover, so the cadence is no longer this repository's to run; what remains here is supplying the R&D that Track 1 draws on

---

## Phase 2: Reach

What gets the tools into daily use.

- **Batch analysis** — multiple texts compared side-by-side
- **Audio analysis** — extend the analytical surface beyond text into audio waveforms; capability covers synthetic-speech detection (AI-generated content patterns) and acoustic forensic indicators (human stress, environmental dissonance); local-only processing consistent with the data sovereignty commitment
- **Audio briefing pilot** — CEO-led; trust-layer for non-readers
- **Sustained cadence** — two to three published pieces per month across both tracks, run by the web line

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
- Browser extensions (superseded by the intelligence-product surface in Phase 1)
- Anonymous contribution channels (open-core licensing does not imply open collaboration)
