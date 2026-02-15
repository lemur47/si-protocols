# si-protocols

Hybrid tech-psychic protocols for Spiritual Intelligence — open-source tools to detect and safeguard against disinformation in metaphysical narratives.

Cybersecurity for the soul. Run locally on your own texts only.

## Quickstart

```bash
# Clone and set up (requires Python 3.12+ and uv)
git clone https://github.com/lemur47/si-protocols.git
cd si-protocols
uv sync --all-extras
uv pip install en_core_web_sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl

# Analyse a text file
uv run si-threat-filter examples/synthetic_suspicious.txt

# Run tests
uv run pytest
```

## What this does

The threat filter combines two analysis layers:

- **Tech layer** — NLP-based detection across seven dimensions: vagueness patterns, authority claims, urgency/fear triggers, emotional manipulation, logical contradictions, source attribution analysis, and commitment escalation. Markers span six tradition-specific categories (generic New Age, prosperity gospel, conspirituality, commercial exploitation, cult rhetoric, fraternal/secret society).
- **Heuristic layer** — probabilistic dissonance scanner (placeholder for future biofeedback integration)

Output is a 0–100 threat score with a breakdown of what triggered it.

## Project layout

```
src/si_protocols/
  threat_filter.py    # Hybrid NLP + heuristic threat scorer
  markers.py          # Disinformation marker definitions
  output.py           # Rich and JSON output formatting
app/
  main.py             # FastAPI REST API (POST /analyse, GET /health)
  schemas.py          # Pydantic request/response models
site/                 # Astro documentation site
tests/                # pytest suite
examples/             # Synthetic sample texts (never real material)
```

## REST API

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Local-only FastAPI server with `POST /analyse` and `GET /health`. Interactive docs at `/docs`.

## Dev

```bash
uv sync --all-extras
pre-commit install
uv run pytest                 # Tests
uv run ruff check src/        # Lint
uv run pyright                # Type check
uv run bandit -r src/         # Security scan
```

## Disclaimer

This tool is designed for **local use on your own texts only**. We do not host, collect, or analyse third-party, copyrighted, or channelled material. All example texts in this repo are synthetic.

## Licence

MIT
