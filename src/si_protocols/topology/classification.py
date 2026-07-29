"""Kind derivation — the single place where axes become a ``VariableKind``.

Engines classify claims along the four axes and nothing more. Collapsing those
axes into a kind happens here, so every engine tier reaches the same verdict
from the same numbers: the ``--engine`` flag chooses how claims are extracted,
never how they are judged.

The thresholds below are the canon recorded in ``docs/DESIGN.md``. They live in
this module alone — an engine that hard-codes its own is drifting, not
calibrating.
"""

from __future__ import annotations

from si_protocols.topology.types import VariableClassification, VariableKind

# ---------------------------------------------------------------------------
# Canonical thresholds (docs/DESIGN.md)
# ---------------------------------------------------------------------------

#: Mean across the four axes at or above which a claim is PSEUDO outright.
PSEUDO_MEAN = 0.4

#: A single strongly suspicious axis can carry a claim to PSEUDO, but only once
#: the mean has also cleared ``PSEUDO_MIXED_MEAN`` — one loud axis against three
#: quiet ones is not enough on its own.
PSEUDO_MIXED_MEAN = 0.25
PSEUDO_AXIS = 0.5

#: Mean at or below which a claim is TRUE. Between the two bands lies
#: INDETERMINATE.
TRUE_MEAN = 0.15


def classification_mean(classification: VariableClassification) -> float:
    """Mean of the four classification axes."""
    return (
        classification.falsifiability
        + classification.verifiability
        + classification.domain_coherence
        + classification.logical_dependency
    ) / 4


def derive_kind(classification: VariableClassification) -> VariableKind:
    """Collapse a four-axis classification into a :class:`VariableKind`.

    PSEUDO when the mean reaches :data:`PSEUDO_MEAN`, or when a moderate mean
    (:data:`PSEUDO_MIXED_MEAN`) coincides with a single axis at
    :data:`PSEUDO_AXIS`. TRUE at or below :data:`TRUE_MEAN`. Otherwise
    INDETERMINATE.
    """
    mean = classification_mean(classification)
    max_axis = max(
        classification.falsifiability,
        classification.verifiability,
        classification.domain_coherence,
        classification.logical_dependency,
    )

    if mean >= PSEUDO_MEAN or (mean >= PSEUDO_MIXED_MEAN and max_axis >= PSEUDO_AXIS):
        return VariableKind.PSEUDO
    if mean <= TRUE_MEAN:
        return VariableKind.TRUE
    return VariableKind.INDETERMINATE
