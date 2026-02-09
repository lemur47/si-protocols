---
title: Introducing si-protocols
description: Why we built open-source tools for detecting disinformation in spiritual content.
date: 2026-02-08
tags: [announcement, open-source]
---

## Cybersecurity for the soul

The spiritual and metaphysical space has a disinformation problem. Vague authority claims, manufactured urgency, emotional manipulation, logical contradictions, and fear-based patterns are common in channelled material, self-help content, and new-age narratives. Yet there are virtually no tools to help people identify these patterns.

**si-protocols** is our attempt to change that.

## What it does

The threat filter analyses text across two layers:

1. **Tech layer** — a spaCy NLP pipeline that detects vagueness patterns (adjective density), authority claims (phrase matching), urgency/fear triggers, emotional manipulation (lemma-based fear/euphoria detection with a contrast bonus when both polarities appear), and logical contradictions (detecting when both poles of common contradiction archetypes appear in the same text). Each dimension is scored independently, then combined with configurable weights (25/25/15/15/20).

2. **Heuristic layer** — a probabilistic dissonance scanner. Currently a randomised placeholder, this layer is designed to eventually integrate biofeedback signals for a more holistic analysis.

The final output is a **0–100 hybrid score** — higher values indicate more markers of potential disinformation.

## Design principles

- **Local-only** — your texts never leave your machine. We do not host, collect, or analyse third-party content.
- **Transparent** — all marker definitions are plain word/phrase lists in `markers.py`. No black-box models.
- **Synthetic testing** — the repository contains only synthetic example texts. No real channelled material is included.

## Getting started

```bash
git clone https://github.com/lemur47/si-protocols.git
cd si-protocols
uv sync --all-extras
uv run si-threat-filter examples/synthetic_suspicious.txt
```

See the [quickstart guide](/docs/quickstart/) for full setup instructions.

## What's next

This is v0.1 — the foundation. We're exploring:

- Expanded marker dictionaries for different spiritual traditions
- Biofeedback integration for the heuristic layer
- Browser extension for real-time analysis
- Community-contributed marker sets

The project is MIT-licenced and contributions are welcome. Check the [GitHub repository](https://github.com/lemur47/si-protocols) to get involved.
