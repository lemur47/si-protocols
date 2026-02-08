# si-protocols

Hybrid tech-psychic protocols for Spiritual Intelligence — open-source tools to detect and safeguard against disinformation in metaphysical narratives.

Cybersecurity for the soul. Run locally on your own texts only.

## Quickstart

```bash
# Clone and set up (requires Python 3.12+ and uv)
git clone https://github.com/lemur47/si-protocols.git
cd si-protocols
uv sync --all-extras
uv run python -m spacy download en_core_web_sm

# Analyse a text file
uv run si-threat-filter examples/synthetic_suspicious.txt

# Run tests
uv run pytest
```

## What this does

The threat filter combines two analysis layers:

- **Tech layer** — NLP-based detection of vagueness patterns, authority claims, and urgency/fear triggers commonly found in spiritual disinformation
- **Heuristic layer** — probabilistic dissonance scanner (placeholder for future biofeedback integration)

Output is a 0–100 threat score with a breakdown of what triggered it.

## Project layout

```
src/si_protocols/
  threat_filter.py    # Hybrid NLP + heuristic threat scorer
  markers.py          # Disinformation marker definitions
tests/                # pytest suite
examples/             # Synthetic sample texts (never real material)
```

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
