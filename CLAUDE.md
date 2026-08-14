# CLAUDE.md

Guidance for Claude Code (claude.ai/code) working in this repository.

**Boot note.** If `CLAUDE.local.md` exists at the project root, read it before starting work — it is the operator runbook (operating model, KV-TMS boot ritual, work-tracker protocol, trust boundaries) and changes independently of this file. It is classified INTERNAL and gitignored, so it is absent from public clones — that's fine, proceed without it.

## What is this?

**VEGA** — the open-source Spiritual Intelligence tooling stream. Hybrid tech-psychic protocols to detect disinformation in metaphysical and spiritual content. Think "cybersecurity for the soul".

**Local-only: never host, collect, or analyse third-party content.**

The repo carries the Python toolkit, the zero-install Claude skills, and the documentation. The former editorial websites were handed over to a separate web line in July 2026, preserved at tag `web-handover-2026-07`; their toolkit docs now live under `docs/`.

## Commands

The usual `uv` / `ruff` / `pytest` / `pyright` invocations behave as expected. These are the ones worth knowing:

```bash
bash scripts/post-sync.sh                    # (re)install the spaCy models — needed after uv sync
uv run pytest -m "not slow"                  # skip the spaCy-dependent tests
osv-scanner scan source --config=osv-scanner.toml --recursive .   # the config flag is required
uvicorn app.main:app --host 127.0.0.1 --port 8000                 # loopback only; the API is not hosted
```

CLI entry points:

- `uv run si-threat-filter <file>` — `--format rich|json`, `--lang en|ja`
- `uv run si-topology <file>` — `--engine rule|anthropic`, `--format svg|json`, `--lang en|ja`, `-o OUTPUT`

`AnthropicEngine` needs the `anthropic` extra and an `ANTHROPIC_API_KEY`. Its retired model pin and request shape were restored for the current generation and **verified against the live endpoint on 2026-08-13** — EN and JA corpus samples, request accepted, response parsed, variables classified. No key is kept on this machine, so re-verification needs a fresh one. Rich output respects `NO_COLOR`.

## Architecture

Two tools. The **threat filter** scores 0–100 via `hybrid_score(text, lang)`, combining a tech layer (60%, spaCy marker matching) with a heuristic layer (40%, probabilistic dissonance scanner). The **topology** module extracts claims, classifies them on four axes, and builds a layered graph, behind three engine tiers — `RuleEngine` (local, default), `AnthropicEngine` (Claude API), `OllamaEngine` (stub). Both return frozen dataclasses.

Full architectural reasoning: [`docs/DESIGN.md`](docs/DESIGN.md).

## Gotchas

- spaCy models are lazy-loaded via `_get_nlp(lang)` to keep import-time side effects out of tests; NLP-exercising tests are marked `@pytest.mark.slow`.
- `random` in the heuristic layer is deliberate — `S311` is suppressed in the ruff config, not an oversight.
- Python 3.14 is blocked by spaCy. `requires-python = ">=3.12"`; CI tests 3.12 and 3.13.
- **`uv.lock` drift fails CI.** After editing `pyproject.toml`, run `uv lock`. For Dependabot PRs that bump lower bounds, run `uv lock` locally and push the refreshed lock to the Dependabot branch before merging.
- Adding a language takes four coordinated edits: a `markers_<lang>.py` file, a loader in `marker_registry.py`, an entry in `_LANG_MODELS`, and the `SupportedLang` literal.
- **Editing markers or weights turns `tests/test_corpus_baseline.py` red, and that red is correct.** It pins all 24 corpus samples to recorded scores within 1e-6. Re-record `tests/data/corpus_tech_baseline.json` in the same change and say why in the PR. **Never widen the tolerance to make it pass** — it is deliberately far below the smallest real change (0.0036 measured), because observed variance is zero.
- Topology types are frozen dataclasses using `tuple`, not `list` — they must stay hashable.
- Two guard layers, because one cannot see the other's surface: `classification-gate.py` scans staged file *content*, while `check-airtable-ids.py` runs at the `commit-msg` stage to scan the commit *message*. `default_install_hook_types` wires both on a plain `pre-commit install`.
- **Never give the `gitleaks` pre-commit hook an `args` list.** pre-commit *appends* `args` to the hook's own `entry` (`gitleaks git --pre-commit --redact --staged --verbose`), so anything positional becomes the scan *path* and the hook exits 0 having scanned nothing — a green tick over an unscanned commit. `.gitleaks.toml` is auto-discovered at the repo root and needs no flag. When checking this gate, read the **bytes** scanned: in `--staged` mode it always prints `0 commits scanned`, so the commit count tells you nothing.
- **`GITLEAKS_VERSION` in `.github/workflows/ci.yml` must stay in step with the gitleaks `rev` in `.pre-commit-config.yaml`.** Nothing enforces it — Dependabot covers neither a bare env var nor a pre-commit rev, so both move by hand or not at all. Unset, the action resolves the *latest* release at run time, which means a SHA-pinned action downloading an unpinned binary.
- British English in docs and comments ("analyse", "colour", "licence").
- Examples are synthetic only — never real channelled material.

## Classification and git workflow

**The repo is public. Every pushed branch is world-readable the moment it lands.**

- Only **Open**-classified content goes to remote. Internal and Classified stay local — never push them.
- Use `tmp/` (gitignored) for classified working files and handoffs.
- **Never bypass `scripts/classification-gate.py`.**
- Always work on a `feature/*` branch and open a PR. All pre-commit hooks must pass before pushing.

Operator-local material — work-tracker protocol, sprints, decision logging, trust-boundary config — lives in `CLAUDE.local.md`.

## Directories worth a note

`skills/` holds standalone prompt files encoding the detection methodology, for use in Claude Projects without installing the Python toolkit. `examples/` holds synthetic sample texts. The rest of the layout is conventional src-layout and reads clearly from `ls`.

## Docs map

Everything below lives under `docs/`.

- **Canon** — `STRATEGY.md` (strategic *why*) · `DESIGN.md` (architectural *why*) · `STACK.md` (technical *what*) · `ROADMAP.md` (*when*)
- **User docs** — `quickstart.md`, `library.md`, `api.md`, `architecture.md`, plus the `hands-on-threat-analysis.md` tutorial and the `ab-evaluation-quick-check-v02.md` evaluation
- **Methodology** — `the-virtualisation-model.md` (conceptual) and `CVP.md` (technical), `egregores.md`, `mapping-claims-and-patterns.md`, `threat-modelling.md`

## Licence

MIT
