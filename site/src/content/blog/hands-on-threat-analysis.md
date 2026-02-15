---
title: "Hands-On Threat Analysis: A Step-by-Step Tutorial"
description: Walk through analysing spiritual content with si-protocols — from CLI to API to Python library.
date: 2026-02-15
tags: [tutorial, getting-started]
---

## What We're Analysing

Let's walk through a complete threat analysis using a synthetic example. The file `examples/synthetic_suspicious.txt` ships with the repository — it was written specifically for testing and contains a concentration of common disinformation markers:

> The ancient and hidden cosmic truth has been veiled from humanity for millennia. The ascended masters say that only those who awaken to the divine frequency will transcend the matrix of illusion. The galactic federation confirms that a great shift is upon us. You must act now — the window is closing, and only the chosen will ascend to the fifth dimension.

This passage alone packs vague adjectives (*ancient*, *hidden*, *cosmic*, *divine*), authority claims (*the ascended masters say*, *the galactic federation confirms*), and urgency patterns (*you must act now*, *the window is closing*). The full file also includes emotional manipulation, logical contradictions, unfalsifiable source claims, and unnamed authority phrases.

All examples in this tutorial are synthetic. We never include real channelled or spiritual material in the repository.

## Method 1 — The CLI

The fastest way to analyse a file is the command-line interface.

**Setup** (if you haven't already):

```bash
git clone https://github.com/lemur47/si-protocols.git
cd si-protocols
uv sync --all-extras
uv pip install en_core_web_sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

**Run the analysis:**

```bash
uv run si-threat-filter examples/synthetic_suspicious.txt
```

The Rich output shows a colour-coded threat score (green for low, yellow for medium, red for high) with a breakdown of the tech and heuristic contributions. Below the score, a table lists every detected marker by category — authority claims, urgency patterns, emotion triggers, contradictions, source attribution, and escalation hits.

For machine-readable output, use `--format json`:

```bash
uv run si-threat-filter examples/synthetic_suspicious.txt --format json
```

This emits the full `ThreatResult` as indented JSON — useful for piping into other tools.

## Method 2 — The REST API

If you want to integrate threat analysis into a web application or call it from another language, the FastAPI-based API is the way to go.

**Start the server:**

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Send a request:**

```bash
curl -X POST http://127.0.0.1:8000/analyse \
  -H "Content-Type: application/json" \
  -d '{"text": "The ascended masters say you must act now. The galactic federation confirms the window is closing.", "seed": 42}'
```

The response mirrors the `ThreatResult` dataclass — every hit category is listed so you can see exactly which markers fired. The `seed` parameter makes the heuristic layer reproducible, which is handy for testing.

You can also explore the API interactively at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), where Swagger UI lets you paste text and execute requests from the browser.

See the [REST API Reference](/docs/api/) for full endpoint documentation.

## Method 3 — Python Library

For the most flexibility, import si-protocols directly into your Python code.

**Basic analysis:**

```python
from si_protocols.threat_filter import hybrid_score

text = open("examples/synthetic_suspicious.txt").read()
result = hybrid_score(text, seed=42)

print(f"Overall threat score: {result.overall_threat_score}/100")
print(f"Tech layer: {result.tech_contribution}")
print(f"Heuristic layer: {result.intuition_contribution}")

if result.authority_hits:
    print(f"Authority claims: {', '.join(result.authority_hits)}")
if result.contradiction_hits:
    print(f"Contradictions: {', '.join(result.contradiction_hits)}")
if result.escalation_hits:
    print(f"Escalation: {', '.join(result.escalation_hits)}")
```

**Analysing multiple files:**

```python
from pathlib import Path
from si_protocols.threat_filter import hybrid_score

for path in Path("examples").glob("*.txt"):
    result = hybrid_score(path.read_text(), seed=42)
    print(f"{path.name}: {result.overall_threat_score}/100")
```

**Tech layer only** (deterministic, no heuristic):

```python
from si_protocols.threat_filter import tech_analysis

score, entities, auth, urgency, emotion, contra, source, escalation = tech_analysis(text)
print(f"Deterministic tech score: {score}/100")
```

See the [Python Library Reference](/docs/library/) for full API documentation.

## Understanding the Scores

The tech layer scores text across seven dimensions, each weighted independently:

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| Vagueness | 17% | Density of vague spiritual adjectives |
| Authority claims | 17% | Phrases that bypass critical thinking |
| Urgency/fear | 13% | Manufactured time pressure |
| Emotional manipulation | 13% | Fear and euphoria words, with a contrast bonus when both appear |
| Logical contradictions | 13% | Opposing claims that create dependency |
| Source attribution | 13% | Unfalsifiable and unnamed authority sources |
| Commitment escalation | 14% | Foot-in-the-door progression from mild to coercive |

A high score means the text contains many markers of potential disinformation — but **a high score is not a verdict**. Genuine spiritual content can trigger some of these patterns. The tool surfaces structure so you can examine it yourself; it does not tell you what to believe or disbelieve. For more on this philosophy, see [A Tool for Thinking, Not a Truth Oracle](/blog/beyond-nlp-detecting-deception-without-llms/#a-tool-for-thinking-not-a-truth-oracle) in our "Beyond NLP" post.

## What's Next

- **[Python Library Reference](/docs/library/)** — full documentation of `hybrid_score()`, `tech_analysis()`, and `ThreatResult`
- **[REST API Reference](/docs/api/)** — endpoint schemas, examples, and error handling
- **[GitHub](https://github.com/lemur47/si-protocols)** — file issues, contribute marker sets, or suggest new scoring dimensions
