# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is this?

Hybrid tech-psychic protocols for **Spiritual Intelligence** — open-source tools to detect disinformation in metaphysical/spiritual content. Think "cybersecurity for the soul". Local-only tool; never host/collect/analyse third-party content.

## Dev commands

```bash
uv sync --all-extras                          # Install all deps
uv pip install en_core_web_sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl  # Required NLP model
uv run pytest                                 # Run all tests
uv run pytest tests/test_markers.py           # Run a single test file
uv run pytest -k "test_deterministic"         # Run tests matching a name
uv run pytest -m "not slow"                   # Skip slow tests (spaCy-dependent)
uv run ruff check src/ tests/                 # Lint (CI also lints tests/)
uv run ruff format src/ tests/                # Format
uv run pyright                                # Type check
uv run bandit -r src/                         # Security scan
pre-commit run --all-files                    # Run all hooks (lint, format, gitleaks, bandit, pytest)
```

CLI entry point: `uv run si-threat-filter examples/synthetic_suspicious.txt`

The CLI supports `--format rich` (default, colour-coded) and `--format json` (machine-readable). Rich output respects the `NO_COLOR` env var automatically.

### Site (Astro)

```bash
cd site && npm run dev           # Local dev server
cd site && npm run build         # Production build
```

## Architecture

The threat filter produces a 0–100 score by combining two analysis layers:

1. **Tech layer** (`threat_filter.py:tech_analysis`) — spaCy NLP pipeline that scores text across seven dimensions: vagueness (adjective density against `markers.VAGUE_ADJECTIVES`), authority claims (phrase matching against `markers.AUTHORITY_PHRASES`), urgency/fear patterns (`markers.URGENCY_PATTERNS`), emotional manipulation (lemma-based matching against `markers.FEAR_WORDS` and `markers.EUPHORIA_WORDS` with a contrast bonus when both polarities appear), logical contradictions (detecting when both poles of `markers.CONTRADICTION_PAIRS` appear in the same text — e.g. empowerment alongside dependency), source attribution analysis (detecting unfalsifiable sources via `markers.UNFALSIFIABLE_SOURCE_PHRASES`, unnamed authorities via `markers.UNNAMED_AUTHORITY_PHRASES`, offset by verifiable citations via `markers.VERIFIABLE_CITATION_MARKERS`), and commitment escalation (detecting foot-in-the-door progression via `markers.COMMITMENT_ESCALATION_MARKERS` — splits text into thirds using spaCy sentence boundaries and measures whether tiered commitment intensity increases from early to late segments). Weighted composite: 17% vagueness + 17% authority + 13% urgency + 13% emotion + 13% contradiction + 13% source attribution + 14% escalation.

2. **Heuristic layer** (`threat_filter.py:psychic_heuristic`) — probabilistic dissonance scanner using `random.Random` (intentional — placeholder for future biofeedback integration). Accepts a `seed` param for deterministic testing.

3. **Hybrid scoring** (`threat_filter.py:hybrid_score`) — combines the two: 60% tech + 40% heuristic. Returns a `ThreatResult` frozen dataclass.

The spaCy model (`_nlp`) is lazy-loaded via `_get_nlp()` to avoid import-time side effects in tests. Tests that exercise the NLP pipeline are marked `@pytest.mark.slow`.

4. **Output formatting** (`output.py`) — `render_rich()` produces colour-coded terminal output (green/yellow/red by threat level) with Rich panels and tables; `render_json()` emits `dataclasses.asdict()` as indented JSON. The `_threat_style()` helper maps score bands: 0-33 green, 34-66 yellow, 67-100 red bold.

`ThreatResult` frozen dataclass fields: `overall_threat_score`, `tech_contribution`, `intuition_contribution`, `detected_entities`, `authority_hits`, `urgency_hits`, `emotion_hits`, `contradiction_hits`, `source_attribution_hits`, `escalation_hits`, `message`.

Marker definitions in `markers.py` are static word/phrase lists (frozenset for adjectives, lists for phrases/patterns). All markers must be lowercase. Markers span tradition-specific categories: generic New Age, prosperity gospel, conspirituality, New Age commercial exploitation, high-demand group (cult) rhetoric, and fraternal/secret society traditions.

## Git workflow

- **GitHub Flow** — always create a `feature/*` branch, push, and open a PR. Never commit directly to `main`.

## Key conventions

- **British English** in all docs and comments (e.g. "analyse", "colour", "licence")
- **src layout** — all library code under `src/si_protocols/`
- **`requires-python = ">=3.12"`** — dev on 3.13, CI tests 3.12 + 3.13. spaCy does not yet support 3.14
- **Synthetic examples only** — no real channelled material in repo
- `random` usage in heuristic layer is intentional — `S311`/`B311` suppressed in both ruff and bandit configs
- Ruff line length: 99. Ruff rules include isort (`I`), pyupgrade (`UP`), bugbear (`B`), bandit (`S`)
- Pre-commit hooks run ruff, gitleaks, bandit, and pytest on every commit
- Coverage threshold: 70% (`fail_under` in pyproject.toml)
