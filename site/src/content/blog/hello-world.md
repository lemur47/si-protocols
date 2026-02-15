---
title: Introducing si-protocols
description: Why we built open-source tools for detecting disinformation in spiritual content.
date: 2026-02-08
tags: [announcement, open-source]
---

## Cybersecurity for the Soul

The spiritual and metaphysical space has a disinformation problem. Vague authority claims, manufactured urgency, emotional manipulation, logical contradictions, and fear-based patterns are common in channelled material, self-help content, and new-age narratives. Yet there are virtually no tools to help people identify these patterns.

**si-protocols** is our attempt to change that.

## What It Does

The threat filter analyses text across two layers:

1. **Tech layer** — a spaCy NLP pipeline that detects vagueness patterns (adjective density), authority claims (phrase matching), urgency/fear triggers, emotional manipulation (lemma-based fear/euphoria detection with a contrast bonus when both polarities appear), logical contradictions (detecting when both poles of common contradiction archetypes appear in the same text), source attribution analysis (detecting unfalsifiable sources and unnamed authorities, offset by verifiable citations), and commitment escalation (foot-in-the-door progression detection that splits text into thirds and measures whether commitment intensity increases from mild to coercive). Each dimension is scored independently, then combined with weights (17/17/13/13/13/13/14). Markers span six tradition-specific categories: generic New Age, prosperity gospel, conspirituality, New Age commercial exploitation, high-demand group rhetoric, and fraternal/secret society traditions.

2. **Heuristic layer** — a probabilistic dissonance scanner. Currently a randomised placeholder, this layer is designed to eventually integrate biofeedback signals for a more holistic analysis.

The final output is a **0–100 hybrid score** — higher values indicate more markers of potential disinformation.

## Design Principles

- **Local-only** — your texts never leave your machine. We do not host, collect, or analyse third-party content.
- **Transparent** — all marker definitions are plain word/phrase lists in `markers.py`. No black-box models.
- **Synthetic testing** — the repository contains only synthetic example texts. No real channelled material is included.

## Getting Started

```bash
git clone https://github.com/lemur47/si-protocols.git
cd si-protocols
uv sync --all-extras
uv run si-threat-filter examples/synthetic_suspicious.txt
```

See the [quickstart guide](/docs/quickstart/) for full setup instructions.

## What's Next

Since launch we've shipped several major additions:

- **Commitment escalation detection** — a 7th scoring dimension that detects foot-in-the-door progression
- **Tradition-specific markers** — expanded dictionaries covering prosperity gospel, conspirituality, cult rhetoric, and more
- **REST API** — a FastAPI-based `POST /analyse` endpoint for HTTP integration ([API Reference](/docs/api/))

Still exploring:

- Biofeedback integration for the heuristic layer
- Browser extension for real-time analysis
- Community-contributed marker sets

The project is MIT-licenced and contributions are welcome. Check the [GitHub repository](https://github.com/lemur47/si-protocols) to get involved.
