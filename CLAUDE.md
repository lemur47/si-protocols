# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is this?

Hybrid tech-psychic protocols for **Spiritual Intelligence** — open-source tools to detect disinformation in metaphysical and spiritual content. Think "cybersecurity for the soul". Local-only tool; never host, collect, or analyse third-party content.

## Dev commands

```bash
uv sync --all-extras                                # Install all deps
bash scripts/post-sync.sh                           # (Re)install required spaCy models
uv run pytest                                       # Run all tests
uv run pytest tests/test_markers.py                 # Run a single test file
uv run pytest -k "test_deterministic"               # Run tests matching a name
uv run pytest -m "not slow"                         # Skip slow tests (spaCy-dependent)
uv run ruff check src/ tests/ app/                  # Lint
uv run ruff format src/ tests/ app/                 # Format
uv run pyright                                      # Type check
opengrep scan --config auto --error src/ app/       # SAST scan
osv-scanner scan source --config=osv-scanner.toml --recursive .  # Dep vuln scan
pre-commit run --all-files                          # Run all hooks
uvicorn app.main:app --host 127.0.0.1 --port 8000   # Local API server
```

### CLI entry points

- `uv run si-threat-filter examples/synthetic_suspicious.txt` — threat filter. Flags: `--format rich|json`, `--lang en|ja`.
- `uv run si-topology examples/synthetic_topology_suspicious.txt` — topology analysis. Flags: `--engine rule|anthropic`, `--format svg|json`, `--lang en|ja`, `-o OUTPUT`.

Rich output respects the `NO_COLOR` env var. `AnthropicEngine` requires the `anthropic` optional extra (`uv sync --extra anthropic`) and an `ANTHROPIC_API_KEY` environment variable.

### Astro sites

```bash
cd site && npm run dev       # .dev domain local dev
cd site && npm run build     # .dev production build
cd site-cc && npm run dev    # .cc domain local dev (port 3001)
cd site-cc && npm run build  # .cc production build
```

## Architecture

The threat filter produces a 0–100 score combining two analysis layers:

1. **Tech layer** (60%) — NLP marker matching in `src/si_protocols/threat_filter.py` using spaCy pipelines.
2. **Heuristic layer** (40%) — probabilistic dissonance scanner (placeholder for future biofeedback integration).

Core entry point: `hybrid_score(text, lang="en")` returning a `ThreatResult` frozen dataclass. spaCy models are lazy-loaded via `_get_nlp(lang)` to avoid import-time side effects in tests; NLP-exercising tests are marked `@pytest.mark.slow`.

The topology module (`src/si_protocols/topology/`) extracts claims, classifies them along four axes (falsifiability, verifiability, domain coherence, logical dependency), and builds a layered graph. Claims are assigned a `VariableKind` (`PSEUDO`, `TRUE`, `INDETERMINATE`) and placed at one of three `TopologyLevel`s (`MACRO`, `MESO`, `MICRO`). Three engine tiers implement the `AnalysisEngine` protocol:

- **Tier 0 `RuleEngine`** — deterministic, local spaCy + markers
- **Tier 1 `AnthropicEngine`** — Claude API-based extraction
- **Tier 2 `OllamaEngine`** — stub for future local-LLM integration

Output: `TopologyResult` frozen dataclass. `render_svg(result)` / `save_svg(result, path)` produce intelligence-themed SVGs; `render_topology_json(result)` serialises to JSON.

For full architectural reasoning, see [`docs/DESIGN.md`](docs/DESIGN.md).

## Project layout

```
src/si_protocols/
  threat_filter.py    # Hybrid NLP + heuristic scorer
  markers.py          # Disinformation marker definitions
  marker_registry.py  # Multi-language marker loader
  output.py           # Rich and JSON output formatting
  topology/           # Fractal-topology claim analysis
app/
  main.py             # FastAPI REST API (POST /analyse, GET /health)
  schemas.py          # Pydantic request/response models
skills/               # Claude Project skills (zero-install analysis)
site/                 # Astro docs (.dev)
site-cc/              # Astro docs (.cc)
scripts/              # Ops scripts incl. classification-gate.py
tests/                # pytest suite
examples/             # Synthetic sample texts (never real material)
docs/                 # STRATEGY.md, DESIGN.md, STACK.md, ROADMAP.md
```

## Key conventions

- **British English** in all docs and comments (e.g. "analyse", "colour", "licence")
- **src layout** — all library code under `src/si_protocols/`
- **`requires-python = ">=3.12"`** — dev on 3.13, CI tests 3.12 + 3.13. spaCy does not yet support 3.14.
- **Synthetic examples only** — no real channelled material in repo
- `random` usage in heuristic layer is intentional — `S311` suppressed in ruff config
- Ruff line length: 99. Rules include isort (`I`), pyupgrade (`UP`), bugbear (`B`), bandit (`S`)
- Pre-commit hooks: ruff, gitleaks, opengrep, osv-scanner, classification-gate.py, pytest, `uv lock --locked` (lockfile drift)
- **`uv.lock` drift** — CI runs `uv lock --locked` and fails on drift; the same check runs in pre-commit when `pyproject.toml` or `uv.lock` change. After editing `pyproject.toml`, run `uv lock`. For Dependabot PRs that bump pyproject lower bounds, run `uv lock` locally and push the refreshed lock to the Dependabot branch before merging.
- Coverage threshold: 70% (`fail_under` in `pyproject.toml`)
- Topology types are frozen dataclasses with `tuple` (not `list`) for full immutability and hashability
- Adding a new language: a `markers_<lang>.py` file, a loader in `marker_registry.py`, a model entry in `_LANG_MODELS`, and the `SupportedLang` Literal updated
- Skills in `skills/` are standalone prompt files encoding the detection methodology for use in Claude Projects (claude.ai) without installing the Python toolkit

## Classification & git workflow

The `si-protocols` repo is **public**. All remote branches (including `feature/*`) are publicly visible and trigger Cloudflare Pages preview deployments.

- Only **Open**-classified content goes to remote. Internal and Classified docs stay local — never `git push`.
- Use `tmp/` (gitignored) for classified working files and handoffs.
- The `scripts/classification-gate.py` pre-commit hook enforces this — never bypass it.
- Always work on a `feature/*` branch; open a PR for review; all pre-commit hooks must pass before pushing.

**PMO operations** (Airtable protocol, sprints, work items, firing pin drills, capacity anchor reviews, decision logging, trust-boundary config) live in `CLAUDE-internal.md` — operator-local, gitignored, populated from CTO handoff.

## Docs map

- [`docs/STRATEGY.md`](docs/STRATEGY.md) — strategic *why*
- [`docs/DESIGN.md`](docs/DESIGN.md) — architectural *why*
- [`docs/STACK.md`](docs/STACK.md) — technical *what*
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — *when* things land

## Licence

MIT
