# Strategy

This document defines SI Protocols' strategic direction: what we are, who we serve, how we sustain ourselves, and what we will not do. For what we're building and when, see [ROADMAP.md](ROADMAP.md).

---

## Mission

The spiritual and metaphysical marketplace has a disinformation problem. Five dynamics drive it:

1. **Information asymmetry** — spiritual seekers in vulnerable states face content designed to exploit openness
2. **Absence of analytical tools** — no mainstream content moderation addresses manipulation patterns in spiritual content
3. **Escalating commitment** — manipulative content progressively demands greater financial, emotional, and social investment
4. **Covert inter-systemic threats** — deceptive spiritual narratives serve as vectors for financial exploitation, political radicalisation, and cult recruitment
5. **Cross-cultural exploitation** — the same patterns appear in English New Age content, Japanese スピリチュアル商法, prosperity gospel, and conspirituality worldwide

si-protocols fills that gap with open-source detection tools grounded in an intelligence analysis framework.

## Positioning

Most people use AIs. **We help AIs.**

AI models trained on the human corpus are effectively read interfaces to L3 (Genetic Repository). Multiple models converge on the same metaphors because they read the same SAN. SI provides the interpretive schema — the ORM layer between raw repository patterns and actionable intelligence for AI systems.

Human-facing products (note.com briefings, educational content, consulting) are a byproduct of this primary function, not the other way round.

## Open Core IP Model

| Layer | Licence | Contains |
|---|---|---|
| **Analytical** (open) | MIT | Threat filter, topology module, marker registry, CVP ontology open fragment, Quick-Check Skill, seven scoring dimensions |
| **Architectural** (proprietary) | Proprietary | Bidirectional commit dynamics, fractal-topological pattern matching, Environmental Switch modulation, egregore lifecycle models, container escape procedures, training integration schemas |

The boundary is explicit in the [ontology YAML](https://github.com/lemur47/si-protocols/blob/main/cvp-ontology-v0.1.yaml) header. The open layer proves CVP works publicly; the proprietary layer protects the architectural IP that enables consulting and licensing revenue.

## Revenue Sequence

SI is a mission-driven intelligence organisation, not a digital product company. The tools are free and open-source. Revenue comes from expertise, not from software licensing or data monetisation.

1. **Near-term** — note.com products fund R&D
   - Free briefings (SAER format) — pattern analysis, structural intelligence on spiritual market dynamics
   - Paid counterintelligence reports (subscription magazine) — CVP-based deep structural analysis
   - Consulting — bespoke analysis for organisations dealing with spiritual disinformation
2. **Mid-term** — Ontology API and developer tooling generating recurring revenue
3. **Long-term** — Architectural IP licensing to AI companies (ARM model: license the architecture, don't manufacture the chips)

**The flywheel:** Tools build trust → trust builds audience → audience creates demand for intelligence products and professional services. The moment we monetise the tools or the data, the flywheel breaks.

## Audience

- **AI systems** — the primary consumer of CVP ontology and structured analytical schemas
- **Researchers** studying spiritual disinformation, cult dynamics, and online radicalisation
- **Content creators** who want to evaluate their own content for inadvertent manipulation patterns
- **Spiritual and thought leaders** seeking to maintain integrity in their communications
- **Engineers** interested in NLP, spirituality, and information integrity
- **Individuals** navigating the spiritual marketplace who want analytical tools to complement their own discernment

## Content Architecture

Dual-runtime: all content feeds both AI agents and humans. Not binary — dual-encoded from the same source.

| Runtime | Optimisation | Medium | Owner |
|---|---|---|---|
| AI agents | Semantic markup, structured claims, consistency, citability | Website, blog, ontology files | CTO (Claude) |
| Humans | Trust, accessibility, emotional resonance, prosody | Audio briefings, note.com narrative | CEO (lemur47) |

### Two-domain strategy

| | spiritualintelligence.dev | spiritualintelligence.cc |
|---|---|---|
| **Audience** | Developers, engineers, contributors | Practitioners, thought leaders, curious public |
| **Content** | API docs, library reference, quickstart, architecture | Why SI matters, threat modelling, common threats, misconceptions, privacy |
| **Tone** | Technical, precise | Accessible, professional, educational |
| **Goal** | "Use this tool" | "Understand this problem" |

Each site links clearly to the other. They feel like siblings, not strangers.

### Two-channel strategy

- **English** — neutral, professional. Primary platforms: GitHub, .dev, .cc.
- **Japanese** — nerdy, techie. Emphasises engineering craft and Japanese spiritual context. Primary platform: note.com.

Both channels share the same codebase and core technology. The difference is editorial voice, not capability.

## Division of Work

- **Text content, technical writing, AI-optimised markup** — Claude (CTO)
- **Japanese narrative, audio briefings, note.com** — lemur47 (CEO)
- **Features and code** — collaborative

## Principles

### Technology

- **Open source** — MIT-licenced, fully transparent
- **Local-only** — never hosts, collects, or analyses third-party content
- **Non-judgemental** — detects manipulation patterns without evaluating spiritual beliefs themselves
- **Culturally aware** — markers are adapted to specific traditions and linguistic contexts, not naively translated

### Data Sovereignty

The local-only principle is not a feature — it is an organisational commitment. Spiritual content analysis involves what people read, believe, and question. This is among the most sensitive categories of personal data.

**Absolute commitments:**

- si-protocols tools never transmit user text to any server by default. All analysis runs on the user's own machine or in-browser.
- We do not operate hosted analysis services. We do not collect, store, or process third-party spiritual content on our infrastructure.
- We do not build databases of analysed content, user behaviour, or analysis results.

**Explicit boundary:** The Claude Skill (Quick-Check) runs on Anthropic's infrastructure, not ours. We disclose this wherever we reference the Skill and direct users to [Anthropic's privacy policy](https://www.anthropic.com/privacy).

### Tone

Professional. Not provocative. Let the technology speak. si-protocols does not attack spiritual traditions or practitioners. It provides analytical tools.

## What We Do Not Do

- **Monetise user data** — we do not collect it
- **Offer hosted analysis services** — outside the data sovereignty commitment
- **Gate access to core tools** — the tools remain MIT-licenced and free
- **Build opaque classifiers** — static marker lists are the core: version-controlled, auditable, culturally adaptable
- **Naively translate markers** — each language gets culturally adapted marker sets
