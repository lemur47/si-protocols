"""Topology module data types — enums and frozen dataclasses.

All types are immutable. Collections inside frozen dataclasses use ``tuple``
rather than ``list`` so that the entire object graph is hashable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from si_protocols.marker_registry import SupportedLang

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class VariableKind(Enum):
    """Whether a variable (claim) is deceptive, verifiable, or unclear."""

    PSEUDO = "pseudo"
    TRUE = "true"
    INDETERMINATE = "indeterminate"


class TopologyLevel(Enum):
    """Fractal level of analysis."""

    MACRO = "macro"
    MESO = "meso"
    MICRO = "micro"


class EdgeKind(Enum):
    """Relationship between topology nodes."""

    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    ESCALATES_TO = "escalates_to"
    CONTAINS = "contains"
    DEPENDS_ON = "depends_on"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class VariableClassification:
    """Four-axis classification of a variable.

    Each axis ranges 0.0-1.0 where higher = more suspicious.

    * ``falsifiability`` - 0.0 testable, 1.0 unfalsifiable
    * ``verifiability`` - 0.0 has sources, 1.0 no checkable sources
    * ``domain_coherence`` - 0.0 stays in domain, 1.0 crosses domains
    * ``logical_dependency`` - 0.0 load-bearing, 1.0 decorative
    """

    falsifiability: float = 0.0
    verifiability: float = 0.0
    domain_coherence: float = 0.0
    logical_dependency: float = 0.0

    def __post_init__(self) -> None:
        for name in ("falsifiability", "verifiability", "domain_coherence", "logical_dependency"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                msg = f"{name} must be between 0.0 and 1.0, got {value}"
                raise ValueError(msg)


@dataclass(frozen=True)
class Variable:
    """A single claim/assertion extracted from the source text."""

    id: str
    text: str
    source_span: tuple[int, int]
    classification: VariableClassification
    kind: VariableKind
    level: TopologyLevel
    confidence: float = 0.5


@dataclass(frozen=True)
class TopologyNode:
    """A node in the topology graph, carrying one or more variables."""

    id: str
    label: str
    level: TopologyLevel
    kind: VariableKind
    variables: tuple[Variable, ...] = ()
    x: float = 0.0
    y: float = 0.0


@dataclass(frozen=True)
class TopologyEdge:
    """A directed edge between two topology nodes."""

    source_id: str
    target_id: str
    kind: EdgeKind
    weight: float = 1.0


@dataclass(frozen=True)
class TopologyResult:
    """Complete result of a topology analysis run."""

    nodes: tuple[TopologyNode, ...] = ()
    edges: tuple[TopologyEdge, ...] = ()
    variables: tuple[Variable, ...] = ()
    pseudo_count: int = 0
    true_count: int = 0
    indeterminate_count: int = 0
    lang: SupportedLang = "en"
    engine_name: str = ""
    message: str = field(
        default="Topology analysis completed. Variables classified along "
        "falsifiability, verifiability, domain coherence, and logical dependency axes."
    )
