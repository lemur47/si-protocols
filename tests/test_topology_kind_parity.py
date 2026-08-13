"""Cross-engine parity for kind derivation.

The engine tier chooses how claims are *extracted*. It must not change how they
are *judged*: identical axes have to yield an identical ``VariableKind`` on
every tier. These tests exist because that invariant was silently broken once —
``anthropic_engine`` carried its own thresholds (0.5 / 0.3, no max-axis rule)
while ``rule_engine`` used the DESIGN.md canon, so ``--engine`` altered
verdicts rather than just cost.

No API key is needed: the Anthropic tier is exercised through a stubbed client
that returns the axes each case is about.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from si_protocols.topology.anthropic_engine import AnthropicEngine
from si_protocols.topology.classification import derive_kind
from si_protocols.topology.rule_engine import RuleEngine
from si_protocols.topology.types import VariableClassification, VariableKind

# ---------------------------------------------------------------------------
# Stub transport — the Claude API is never reached
# ---------------------------------------------------------------------------


@dataclass
class _StubTextBlock:
    text: str
    type: str = "text"


@dataclass
class _StubResponse:
    content: list[_StubTextBlock]


def _engine_returning(axes: VariableClassification) -> AnthropicEngine:
    """An ``AnthropicEngine`` whose stubbed extraction yields exactly ``axes``."""
    payload = [
        {
            "text": "a claim",
            "start": 0,
            "end": 7,
            "falsifiability": axes.falsifiability,
            "verifiability": axes.verifiability,
            "domain_coherence": axes.domain_coherence,
            "logical_dependency": axes.logical_dependency,
        }
    ]
    client = MagicMock()
    client.messages.create.return_value = _StubResponse(
        content=[_StubTextBlock(text=json.dumps({"claims": payload}))]
    )
    return AnthropicEngine(client=client)


# ---------------------------------------------------------------------------
# Cases spanning every band, including the ones the tiers used to disagree on
# ---------------------------------------------------------------------------

_CASES: list[tuple[str, VariableClassification, VariableKind]] = [
    (
        "clearly pseudo on every axis",
        VariableClassification(0.9, 0.8, 0.6, 0.7),
        VariableKind.PSEUDO,
    ),
    (
        # mean 0.45 — canon says PSEUDO; the old Anthropic band (>= 0.5) did not
        "mean between the canon and the old Anthropic threshold",
        VariableClassification(0.5, 0.5, 0.4, 0.4),
        VariableKind.PSEUDO,
    ),
    (
        # mean 0.275 with one axis at 0.6 — the max-axis rule the old tier lacked
        "moderate mean carried to pseudo by one loud axis",
        VariableClassification(0.6, 0.2, 0.1, 0.2),
        VariableKind.PSEUDO,
    ),
    (
        # mean 0.25, no axis at 0.5 — canon says INDETERMINATE; the old
        # Anthropic band (<= 0.3) called this TRUE
        "middle band the old Anthropic threshold called true",
        VariableClassification(0.3, 0.3, 0.2, 0.2),
        VariableKind.INDETERMINATE,
    ),
    (
        # one axis at 0.6 but mean 0.15 — below PSEUDO_MIXED_MEAN, so the
        # max-axis rule does not fire and the TRUE band wins
        "single loud axis does not survive a low mean",
        VariableClassification(0.6, 0.0, 0.0, 0.0),
        VariableKind.TRUE,
    ),
    ("clearly true", VariableClassification(0.1, 0.1, 0.0, 0.1), VariableKind.TRUE),
    (
        "exactly on the true boundary",
        VariableClassification(0.15, 0.15, 0.15, 0.15),
        VariableKind.TRUE,
    ),
    (
        "exactly on the pseudo boundary",
        VariableClassification(0.4, 0.4, 0.4, 0.4),
        VariableKind.PSEUDO,
    ),
]

_IDS = [name for name, _, _ in _CASES]


@pytest.mark.parametrize(("axes", "expected"), [(a, e) for _, a, e in _CASES], ids=_IDS)
def test_canon_thresholds(axes: VariableClassification, expected: VariableKind) -> None:
    """``derive_kind`` implements the bands documented in DESIGN.md."""
    assert derive_kind(axes) == expected


@pytest.mark.parametrize(("axes", "expected"), [(a, e) for _, a, e in _CASES], ids=_IDS)
def test_anthropic_tier_matches_canon(
    axes: VariableClassification, expected: VariableKind
) -> None:
    """The Anthropic tier reaches the canonical verdict for the same axes."""
    variables = _engine_returning(axes).extract_variables("text")
    assert variables[0].classification == axes
    assert variables[0].kind == expected


def test_anthropic_tier_derives_nothing_of_its_own(monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirecting the shared derivation must move the Anthropic tier with it.

    If the tier ever re-inlines thresholds, the patch stops reaching it and this
    goes red — which is the point. Asserting the current verdicts alone would
    not catch a re-inlined copy that happens to agree today.
    """
    monkeypatch.setattr(
        "si_protocols.topology.anthropic_engine.derive_kind",
        lambda _classification: VariableKind.INDETERMINATE,
    )
    variables = _engine_returning(VariableClassification(0.9, 0.9, 0.9, 0.9)).extract_variables(
        "text"
    )
    assert variables[0].kind == VariableKind.INDETERMINATE


_RULE_TIER_TEXT = (
    "The ascended masters have confirmed that the frequency shift is inevitable. "
    "A 2019 study published in Nature measured the same effect at 3.2 per cent. "
    "Everything is energy, and energy is everything, so the choice is yours."
)


@pytest.mark.slow
def test_rule_tier_matches_canon() -> None:
    """Every kind the rule tier emits is the one the canon derives from its axes."""
    variables = RuleEngine().extract_variables(_RULE_TIER_TEXT)
    assert variables, "expected the rule engine to extract at least one variable"
    for variable in variables:
        assert variable.kind == derive_kind(variable.classification)


@pytest.mark.slow
def test_rule_tier_derives_nothing_of_its_own(monkeypatch: pytest.MonkeyPatch) -> None:
    """The same redirection check for the rule tier."""
    monkeypatch.setattr(
        "si_protocols.topology.rule_engine.derive_kind",
        lambda _classification: VariableKind.INDETERMINATE,
    )
    variables = RuleEngine().extract_variables(_RULE_TIER_TEXT)
    assert variables, "expected the rule engine to extract at least one variable"
    assert all(v.kind == VariableKind.INDETERMINATE for v in variables)
