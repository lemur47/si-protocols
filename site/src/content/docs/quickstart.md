---
title: Quickstart
description: Get started with si-protocols in under five minutes.
order: 1
---

## Prerequisites

- **Python 3.12+** (developed on 3.13)
- **[uv](https://docs.astral.sh/uv/)** package manager

## Installation

```bash
git clone https://github.com/lemur47/si-protocols.git
cd si-protocols
uv sync --all-extras
uv pip install en_core_web_sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

## Analyse a Text

Run the threat filter against any local text file:

```bash
uv run si-threat-filter examples/synthetic_suspicious.txt
```

## Output

The filter produces a **0–100 threat score** with a breakdown:

- **Tech score** — NLP-based detection of vagueness, authority claims, urgency patterns, emotional manipulation, logical contradictions, and source attribution analysis
- **Heuristic score** — probabilistic dissonance scanner
- **Hybrid score** — weighted composite: 60% tech + 40% heuristic

Higher scores indicate more markers of disinformation were detected.

## Running Tests

```bash
uv run pytest                    # All tests
uv run pytest -m "not slow"     # Skip spaCy-dependent tests
```

## What Next?

- Read the [source code](https://github.com/lemur47/si-protocols) to understand the analysis layers
- Check `markers.py` to see which patterns are detected
- File issues or contribute on [GitHub](https://github.com/lemur47/si-protocols)
