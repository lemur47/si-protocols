# Mid-Term Roadmap

**Timeframe:** 6–12 months (from February 2026)

This roadmap covers three pillars: educational content across two domains, Japanese-language narrative on note.com, and user-facing tools (web demo + Chrome extension) that make the technology accessible beyond the CLI.

---

## Two-Domain Strategy

The project maintains two complementary websites:

| | spiritualintelligence.dev | spiritualintelligence.cc |
|---|---|---|
| **Audience** | Developers, engineers, contributors | Practitioners, thought leaders, curious public |
| **Content** | API docs, library reference, quickstart, architecture, contributing guide | Why SI matters, threat modelling, common threats, misconceptions, privacy |
| **Tone** | Technical, precise | Accessible, professional, educational |
| **Goal** | "Use this tool" | "Understand this problem" |
| **Stack** | Astro (current) | TBD (Astro or CMS-friendly) |

Each site links clearly to the other. The .cc site has a "For Developers" call-to-action pointing to .dev. The .dev site has a "Why This Matters" link pointing to .cc. They feel like siblings, not strangers.

---

## Completed

### Topology module v1

Fractal-topology analysis that extracts claims from text, classifies them along four axes, and builds a layered graph. Delivered infrastructure:

- **Rule engine** (Tier 0) — local, deterministic analysis using spaCy + marker heuristics
- **Anthropic engine** (Tier 1) — Claude API-based claim extraction and classification
- **Output formats** — SVG visualisation (intelligence-themed dark HUD) and JSON
- **CLI** — `si-topology` command with `--engine`, `--format`, `--lang`, and `-o` options
- **Multi-language support** — English and Japanese

---

## Counterintelligence Integration (Proposed)

A new work stream extending the CVP model with counterintelligence capabilities. Theory first, tooling later.

### Phase A: Theory (current)

Document the conceptual extensions to the CVP model:

- Upgrade Layer 6 to distinguish stateless containers from stateful containers (egregores / parasitic orchestration middleware)
- Document egregoric access to the Genetic Repository (Layer 3) — systematic contamination vs random noise
- Map inbound/outbound counterintelligence boundaries explicitly in the layer stack
- Explain the three-layer resistance pattern (L6 + L3 + L4) that egregores deploy against escaping instances
- Publish deep-dive page on egregores and blog post demonstrating the model's analytical power

### Phase B: Detection (extends existing tools)

Expand the threat filter and topology module to cover outbound analysis:

- Exposure scoring — given a file or behavioural trace, how much does it reveal about the instance's container configuration?
- Outbound topology analysis — the same visualisation framework mapping metadata claims

### Phase C: Active Defence (reference implementations)

Small tools as concrete implementations of CVP counterintelligence:

- Metadata stripping (ExifTool wrapper) — outbound container hygiene
- Exposure audit — what does a file, post, or profile reveal about you?
- These are CVP-native tools demonstrating the model's outbound defence layer, not generic privacy utilities

### Phase D: Operational Capability (future)

- Steganographic watermarking — provenance and leak detection
- Covert channel APIs — for specialised use cases

---

## Phase 1: Foundation (Months 1–3)

### spiritualintelligence.cc — launch

Core educational pages:

- **Why Spiritual Intelligence Matters** — the problem space, real-world harm, why existing tools don't cover this
- **Threat Modelling for Spiritual Content** — the seven analysis dimensions explained for non-technical readers, with illustrative examples
- **Common Threats and Patterns** — taxonomy of manipulation tactics (escalation funnels, unfalsifiable claims, emotional whiplash, covert exploitation)
- **Common Misconceptions** — "this judges beliefs" vs "this detects manipulation patterns"; "AI can't understand spirituality"; "this replaces discernment"
- **Cybersecurity and Privacy** — why local-only processing matters, data sovereignty, how SI connects to broader information security thinking

### spiritualintelligence.dev — refine

- Architecture deep-dive (for contributors and security researchers)
- Contributing guide (adding languages, refining markers, extending dimensions)
- Embedded web demo (see below)

### note.com — establish presence

- 2–3 narrative posts establishing voice and context
- Topics: why this project exists, cultural context of 霊感商法 / スピリチュアル商法, the engineering story behind Japanese marker adaptation

### Feature: web demo MVP

- Svelte + Astro interactive interface on .dev
- Paste text, see threat score with dimension breakdown
- Zero install, zero data collection — runs analysis via local API or client-side
- Embeddable widget version for .cc (lets visitors try it without leaving the educational context)

---

## Phase 2: Reach (Months 4–6)

### Chrome extension MVP

- Right-click context menu: "Analyse this text for manipulation patterns"
- Select text on any webpage → inline threat score overlay
- Local-only processing — no data leaves the browser (major trust signal for the target audience)
- Architecture options: bundled lightweight JS scoring for basic analysis, with optional connection to local API for full spaCy pipeline
- Landing page on .cc explaining what it does and why it's safe

### Content expansion

- **.cc** — case studies, pattern library ("anatomy of an escalation funnel"), "how to read a threat score" guide
- **.dev** — tutorial series, integration examples
- **note.com** — regular posting cadence, building JA community narrative, connecting to consumer protection discussions

### Feature: batch analysis

- Analyse multiple texts and compare scores side by side
- Useful for researchers tracking patterns across a corpus

---

## Phase 3: Community (Months 7–12)

### Chrome extension polish

- Settings panel (sensitivity, marker categories)
- Marker customisation — let users add domain-specific markers for their tradition or context
- Clear local-only guarantees visible in the UI and extension store listing

### Interactive educational content

- **.cc** — embedded demos, interactive threat pattern explorer, guided walkthroughs
- **.dev** — contributor onboarding, language addition tutorial

### Contributor programme

- Language contributions (community-submitted marker sets for new languages)
- Marker review process (tradition experts validating and refining marker lists)
- Recognition and attribution for contributors

### Feature: report generation

- Shareable PDF/HTML reports for practitioners and researchers
- Structured output suitable for academic citation or organisational review

---

## Web Demo and Chrome Extension: Complementary Roles

Both tools are developed and maintained because they serve different moments in the user journey:

| | Web demo (Svelte + Astro) | Chrome extension |
|---|---|---|
| **When** | "Let me try this" — first encounter | "I use this daily" — habitual use |
| **Where** | .dev site, embeddable on .cc | In-situ on any webpage |
| **Friction** | Zero install, paste text, see results | One-time install, then seamless |
| **Audience** | Evaluators, developers, curious visitors | Practitioners, followers, researchers |
| **Role** | Top of funnel — converts curiosity into understanding | Retention layer — converts understanding into daily practice |

The web demo is the gateway; the extension is the habit. Without the demo, people won't trust the extension enough to install it. Without the extension, the tool stays a novelty rather than a practice.

---

## Division of Work

- **English content and technical writing** — Claude (with review)
- **Japanese narrative and note.com** — human lead (with internal collaboration on technical accuracy and consistency)
- **Features and code** — collaborative

---

## What This Roadmap Does Not Cover

- Additional language support beyond EN/JA (deferred until contributor programme is established)
- Consulting/SaaS services (deferred until community traction is demonstrated)
- Mobile applications
- Social media integrations beyond the Chrome extension
