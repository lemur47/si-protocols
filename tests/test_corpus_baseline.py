"""Regression tests locking the tech layer's corpus scores against drift.

These assert against **recorded actuals**, not against the manifest's published
``expected_score_range``. The two are different claims: the manifest states what the
shared rubric says a sample should score, and the implementation currently meets that
for only 6 of 24 samples. Asserting the manifest here would produce a suite that is
mostly ``xfail`` — a gate scanning almost nothing. Asserting recorded actuals gives a
test that genuinely fails on all 24 when the pipeline moves.

A red here is not flake. It means markers, weights or the spaCy pinning changed, and
the baseline must be re-recorded deliberately as part of that change.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from si_protocols.marker_registry import SupportedLang
from si_protocols.threat_filter import tech_analysis

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
MANIFEST_PATH = EXAMPLES_DIR / "corpus_manifest.json"
BASELINE_PATH = Path(__file__).resolve().parent / "data" / "corpus_tech_baseline.json"


def _baseline() -> dict:
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def _lang_of(filename: str) -> SupportedLang:
    return "ja" if filename.startswith("corpus_ja_") else "en"


def test_baseline_covers_every_manifest_sample() -> None:
    """The baseline must score exactly the manifest's samples — no more, no fewer.

    Without this, adding a 25th corpus sample would leave it silently uncovered by the
    regression test below, which would keep passing and mean less than it appears to.
    """
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_files = {entry["filename"] for entry in manifest["samples"]}
    baseline_files = set(_baseline()["scores"])

    assert baseline_files == manifest_files, (
        "Baseline and manifest disagree on which samples exist. "
        f"Missing from baseline: {sorted(manifest_files - baseline_files)}. "
        f"Unknown to manifest: {sorted(baseline_files - manifest_files)}. "
        "Re-record tests/data/corpus_tech_baseline.json as part of the change."
    )


@pytest.mark.slow
def test_tech_scores_match_recorded_baseline() -> None:
    """Every sample must score within the recorded tolerance of its recorded actual.

    The tolerance is measured rather than guessed, and is deliberately tight — see
    ``tolerance_rationale`` in the baseline file. Observed variance across repeated runs
    and across Python 3.12 and 3.13 is exactly zero, while the smallest real change
    measured (removing one marker) moves affected samples by ~0.04. A loose tolerance
    here would mask most of a genuine change's blast radius: at 0.01, a one-unit weight
    change reported 11 drifted samples where 24 had actually moved.
    """
    baseline = _baseline()
    tolerance = baseline["tolerance"]
    recorded: dict[str, float] = baseline["scores"]

    deviations = []
    for filename, expected in sorted(recorded.items()):
        text = (EXAMPLES_DIR / filename).read_text(encoding="utf-8")
        actual = tech_analysis(text, lang=_lang_of(filename)).score
        delta = abs(actual - expected)
        if delta > tolerance:
            deviations.append(
                f"  {filename}: recorded {expected:.6f}, got {actual:.6f} (delta {delta:.6f})"
            )

    assert not deviations, (
        f"{len(deviations)} of {len(recorded)} samples drifted beyond the "
        f"{tolerance} tolerance:\n" + "\n".join(deviations) + "\n\n"
        "If this change was intended (markers, weights, or a spaCy/model version bump), "
        "re-record tests/data/corpus_tech_baseline.json in the same change and say why "
        "in the PR. Do not widen the tolerance to make this pass."
    )
