# Strategy

## Mission

**Spiritual Intelligence** — cybersecurity for the soul and planetary defence.

si-protocols provides open-source tools that detect disinformation patterns in metaphysical and spiritual content. The project operates at the intersection of natural language processing, pattern recognition, and spiritual literacy — giving individuals and communities the means to evaluate the content they consume.

## What Is Spiritual Intelligence?

Spiritual Intelligence (SI / 霊的知能) is the capacity to discern, evaluate, and navigate spiritual and metaphysical information with clarity. It encompasses:

- **Critical discernment** — the ability to distinguish authentic spiritual teaching from manipulative rhetoric
- **Pattern recognition** — identifying recurring disinformation tactics across traditions, cultures, and languages
- **Emotional sovereignty** — maintaining independent judgement when confronted with fear-based or euphoria-driven persuasion
- **Systemic awareness** — understanding how spiritual narratives interact with social, economic, and political systems
- **Outbound awareness** — recognising how your own signals, metadata, and behavioural patterns are collected and used to craft targeted manipulation — the counterintelligence dimension of spiritual literacy

SI is not about debunking spirituality. It is about raising the standard of spiritual discourse by making manipulation patterns visible.

## Problem Statement

Spiritual and metaphysical content is uniquely vulnerable to disinformation because:

1. **Emotion-driven persuasion** — spiritual claims often bypass rational evaluation by targeting fear, hope, and identity
2. **Unfalsifiable authority** — appeals to channelled messages, ancient wisdom, or divine revelation resist fact-checking
3. **Escalating commitment** — manipulative content progressively demands greater financial, emotional, and social investment
4. **Covert inter-systemic threats** — deceptive spiritual narratives can serve as vectors for financial exploitation, political radicalisation, and cult recruitment
5. **Cross-cultural exploitation** — the same manipulation patterns appear in English-language New Age content, Japanese スピリチュアル商法, prosperity gospel, and conspirituality movements worldwide

No mainstream content moderation tool addresses these patterns. si-protocols fills that gap.

## Approach

### Technology

- **NLP-based pattern detection** — spaCy pipelines analyse text across seven dimensions: vagueness, authority claims, urgency/fear, emotional manipulation, logical contradictions, source attribution, and commitment escalation
- **Heuristic layer** — probabilistic dissonance scanner (placeholder for future biofeedback integration)
- **Multi-language architecture** — extensible marker registry supports English and Japanese, with a clean path to additional languages
- **Hybrid scoring** — weighted combination of tech and heuristic layers produces a 0–100 threat score

### Principles

- **Open source** — MIT-licenced, fully transparent
- **Local-only** — never hosts, collects, or analyses third-party content
- **Non-judgemental** — detects manipulation patterns without evaluating spiritual beliefs themselves
- **Culturally aware** — markers are adapted to specific spiritual traditions and linguistic contexts, not naively translated

### Data Sovereignty

The local-only principle is not a feature — it is an organisational commitment. Spiritual content analysis involves what people read, believe, and question. This is among the most sensitive categories of personal data. Routing it through external servers — even our own — would create an attack surface that contradicts our mission.

**Absolute commitments:**

- si-protocols tools (CLI, API, web demo, Chrome extension) never transmit user text to any server by default. All analysis runs on the user's own machine or in-browser.
- We do not operate hosted analysis services. We do not collect, store, or process third-party spiritual content on our infrastructure.
- We do not build databases of analysed content, user behaviour, or analysis results.
- The Chrome extension, when delivered, will use client-side JavaScript for marker-based scoring. Full-pipeline analysis (spaCy, topology) will connect to the user's own local API server — never to ours.

**Explicit boundary — third-party processing:**

The Claude Skill (Quick-Check) runs on Anthropic's infrastructure, not ours. We disclose this clearly wherever we reference the Skill, and direct users to Anthropic's privacy policy. We do not control Anthropic's data handling. This is the one analysis path that is not local-only, and we state it openly.

**Why this matters:**

An intelligence organisation that collects the data it claims to help you protect is structurally compromised. Our credibility depends on never being in a position where we benefit from analysing your content. The tools are the gift. The intelligence is the service. The data is yours.

## Audience

- **Researchers** studying spiritual disinformation, cult dynamics, and online radicalisation
- **Content creators** (YouTubers, bloggers, podcasters) who want to evaluate their own content for inadvertent manipulation patterns
- **Spiritual and thought leaders** seeking to maintain integrity in their communications
- **Engineers** interested in the intersection of NLP, spirituality, and information integrity
- **Individuals** navigating the spiritual marketplace who want analytical tools to complement their own discernment

## Roadmap

### Completed

1. **Multi-language analysis** — Japanese language support (markers, NLP pipeline, CLI, API) ✓

### Mid-term (6–12 months)

2. **Two-domain web presence** — educational content on spiritualintelligence.cc, technical docs and tools on spiritualintelligence.dev
3. **Web demo** — Svelte + Astro interactive interface for browser-based analysis, embeddable across both domains
4. **Chrome extension** — in-situ text analysis on any webpage, local-only processing
5. **note.com launch** — Japanese-language narrative articles and community engagement

### Mid-term

6. **Counterintelligence integration** — extending the CVP model with outbound vulnerability analysis, egregore theory, and exposure scoring (see [ROADMAP.md](ROADMAP.md) for phasing)

### Longer-term

7. **Community building** — contributor programme, marker refinement, tradition-specific modules, language contributions
8. **Professional services** — consulting, training, and bespoke analysis for organisations dealing with spiritual disinformation (see Revenue Model)

See [ROADMAP.md](ROADMAP.md) for detailed phasing and milestones. See [CVP.md](CVP.md) for the theoretical framework (Cosmic-Virtualisation-Protocol) that grounds the topology module's classification logic.

## Two-Domain Strategy

The project maintains two complementary websites with distinct audiences:

- **spiritualintelligence.dev** — technical documentation, API reference, quickstart guides, architecture deep-dives, and the interactive web demo. Audience: developers, engineers, contributors, security researchers.
- **spiritualintelligence.cc** — educational content explaining why spiritual intelligence matters, threat modelling, common manipulation patterns, misconceptions, and cybersecurity/privacy principles. Audience: practitioners, thought leaders, researchers, and the curious public.

Each site links clearly to the other. They share visual identity but differ in depth and assumed knowledge.

## Two-Channel Strategy

- **English channel** — neutral, professional tone. Focused on the technology, research applications, and open-source community. Primary platforms: GitHub, spiritualintelligence.dev, spiritualintelligence.cc.
- **Japanese channel** — nerdy, techie tone. Emphasises the engineering craft and Japanese spiritual context (スピリチュアル, 霊感商法, カルト対策). Primary platform: note.com.

Both channels share the same codebase and core technology. The difference is editorial voice, not capability.

## Revenue Model

SI is a mission-driven intelligence organisation, not a digital product company. The tools are free and open-source. Revenue comes from expertise, not from software licensing or data monetisation.

### Free tier — trust infrastructure

- **Open-source tools** (CLI, API, web demo, Chrome extension) — MIT-licenced, local-only, zero cost. These are the organisation's public goods and the entry point to the flywheel.
- **Claude Skill** (Quick-Check) — zero-install analysis via Claude Projects. Free to distribute.
- **Educational content** (spiritualintelligence.cc, spiritualintelligence.dev) — threat modelling guides, pattern libraries, CVP model documentation.

### Intelligence products — analysis capability

- **note.com free briefings** — pattern analysis, structural intelligence on spiritual market dynamics. OSINT-style reporting in Japanese.
- **note.com paid reports** (subscription magazine) — counterintelligence briefings. CVP-based deep structural analysis, operational defence techniques, exposure management. Readers pay for sustained access to analytical capability, not for information fragments.

### Professional services — high-value engagements

- **Consulting** — bespoke analysis for organisations dealing with spiritual disinformation (cult recovery groups, consumer protection agencies, media organisations, educational institutions, religious bodies).
- **Education and training** — workshops, lectures, and courses on the CVP model, threat modelling for spiritual content, and counterintelligence awareness. Online and in-person.
- **Custom analysis and system tailoring** — specialist engagements where si-protocols tooling is adapted to an organisation's specific context, tradition, or language. This includes marker customisation, tradition-specific module development, and integration consulting.
- **Cross-organisational collaboration** — joint research, co-developed tooling, or embedded analytical support with partner organisations in other jurisdictions.

### What we explicitly do not monetise

- User data, analysis results, or behavioural patterns — we do not collect these.
- SaaS subscriptions for hosted analysis — we do not offer this.
- Gated access to the core tools — the tools remain MIT-licenced and free.

### Principle

The tools build trust. Trust builds audience. Audience creates demand for intelligence products and professional services. This is the flywheel. The moment we monetise the tools or the data, the flywheel breaks.

## Tone

Professional. Not provocative. Let the technology speak.

si-protocols does not attack spiritual traditions or practitioners. It provides analytical tools. The project's credibility comes from technical rigour, transparent methodology, and respect for the complexity of spiritual experience.
