# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is this?

Hybrid tech-psychic protocols for **Spiritual Intelligence** — open-source tools to detect disinformation in metaphysical/spiritual content. Think "cybersecurity for the soul". Local-only tool; never host/collect/analyse third-party content.

## Dev commands

```bash
uv sync --all-extras                          # Install all deps
uv pip install en_core_web_sm@https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl  # Required English NLP model
uv pip install ja_core_news_sm@https://github.com/explosion/spacy-models/releases/download/ja_core_news_sm-3.8.0/ja_core_news_sm-3.8.0-py3-none-any.whl  # Required Japanese NLP model
uv run pytest                                 # Run all tests
uv run pytest tests/test_markers.py           # Run a single test file
uv run pytest -k "test_deterministic"         # Run tests matching a name
uv run pytest -m "not slow"                   # Skip slow tests (spaCy-dependent)
uv run ruff check src/ tests/ app/             # Lint (CI also lints tests/)
uv run ruff format src/ tests/ app/           # Format
uv run pyright                                # Type check
uv run bandit -r src/                         # Security scan
pre-commit run --all-files                    # Run all hooks (lint, format, gitleaks, bandit, pytest)
uvicorn app.main:app --host 127.0.0.1 --port 8000  # Run API server (local-only)
```

CLI entry point: `uv run si-threat-filter examples/synthetic_suspicious.txt`

The CLI supports:
- `--format rich` (default, colour-coded) and `--format json` (machine-readable). Rich output respects the `NO_COLOR` env var automatically.
- `--lang en` (default) or `--lang ja` for Japanese language analysis.

### Site (Astro)

```bash
cd site && npm run dev           # Local dev server
cd site && npm run build         # Production build
```

## Architecture

The threat filter produces a 0–100 score by combining two analysis layers. The pipeline is **multi-language**: a `lang` parameter (`"en"` | `"ja"`, default `"en"`) flows through the CLI, API, and core library. Each language has its own spaCy model and marker set.

### Multi-language support

- **Marker registry** (`marker_registry.py`) — `MarkerSet` frozen dataclass bundles all 12 marker categories. `get_markers(lang)` dispatches to the correct language module with lazy loading and caching.
- **English markers** (`markers.py`) — original marker definitions (unchanged).
- **Japanese markers** (`markers_ja.py`) — culturally adapted markers for Japanese spiritual contexts (スピリチュアル, 霊感商法, カルト, etc.).
- **NLP models** — `_nlp_cache` dict in `threat_filter.py` lazily loads the appropriate spaCy model per language: `en_core_web_sm` for English, `ja_core_news_sm` for Japanese.

### Analysis pipeline

1. **Tech layer** (`threat_filter.py:tech_analysis`) — spaCy NLP pipeline that scores text across seven dimensions: vagueness (adjective density against `markers.vague_adjectives`), authority claims (phrase matching against `markers.authority_phrases`), urgency/fear patterns (`markers.urgency_patterns`), emotional manipulation (lemma-based matching against `markers.fear_words` and `markers.euphoria_words` with a contrast bonus when both polarities appear), logical contradictions (detecting when both poles of `markers.contradiction_pairs` appear in the same text — e.g. empowerment alongside dependency), source attribution analysis (detecting unfalsifiable sources via `markers.unfalsifiable_source_phrases`, unnamed authorities via `markers.unnamed_authority_phrases`, offset by verifiable citations via `markers.verifiable_citation_markers`), and commitment escalation (detecting foot-in-the-door progression via `markers.commitment_escalation_markers` — splits text into thirds using spaCy sentence boundaries and measures whether tiered commitment intensity increases from early to late segments). Weighted composite: 17% vagueness + 17% authority + 13% urgency + 13% emotion + 13% contradiction + 13% source attribution + 14% escalation.

2. **Heuristic layer** (`threat_filter.py:psychic_heuristic`) — probabilistic dissonance scanner using `random.Random` (intentional — placeholder for future biofeedback integration). Accepts a `seed` param for deterministic testing.

3. **Hybrid scoring** (`threat_filter.py:hybrid_score`) — combines the two: 60% tech + 40% heuristic. Returns a `ThreatResult` frozen dataclass. Accepts `lang` keyword-only param.

The spaCy models are lazy-loaded via `_get_nlp(lang)` to avoid import-time side effects in tests. Tests that exercise the NLP pipeline are marked `@pytest.mark.slow`.

4. **Output formatting** (`output.py`) — `render_rich()` produces colour-coded terminal output (green/yellow/red by threat level) with Rich panels and tables; `render_json()` emits `dataclasses.asdict()` as indented JSON. The `_threat_style()` helper maps score bands: 0-33 green, 34-66 yellow, 67-100 red bold. Output is language-agnostic — it renders whatever strings are in the ThreatResult.

`ThreatResult` frozen dataclass fields: `overall_threat_score`, `tech_contribution`, `intuition_contribution`, `detected_entities`, `authority_hits`, `urgency_hits`, `emotion_hits`, `contradiction_hits`, `source_attribution_hits`, `escalation_hits`, `message`.

5. **REST API** (`app/main.py`) — FastAPI application providing `POST /analyse` (wraps `hybrid_score()`) and `GET /health`. The `app/` package is a dev/deployment artifact separate from the core library — it is not included in the wheel. Pydantic request/response schemas live in `app/schemas.py`. The `/analyse` endpoint accepts a `lang` field (`"en"` | `"ja"`, default `"en"`). The endpoint is a sync `def` so FastAPI runs CPU-bound spaCy work in a thread pool. Run with `uvicorn app.main:app` on `127.0.0.1:8000` (local-only).

Marker definitions are static word/phrase lists (frozenset for adjectives, lists for phrases/patterns). English markers must be lowercase; Japanese markers use standard full-width forms. Markers span tradition-specific categories: generic New Age / スピリチュアル, prosperity gospel / 繁栄の福音, conspirituality / 陰謀論スピ, commercial exploitation / 霊感商法, high-demand group (cult) / カルト, and fraternal/secret society / 秘密結社 traditions.

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
- Adding a new language requires: a `markers_<lang>.py` file, a loader in `marker_registry.py`, a model entry in `_LANG_MODELS`, and the `SupportedLang` Literal updated
