"""Topology graph builder — converts extracted variables into a layered graph.

Takes a ``list[Variable]`` and produces a ``TopologyResult`` with nodes, edges,
and layout coordinates suitable for SVG rendering.
"""

from __future__ import annotations

from dataclasses import replace

from si_protocols.marker_registry import SupportedLang
from si_protocols.topology.types import (
    EdgeKind,
    TopologyEdge,
    TopologyLevel,
    TopologyNode,
    TopologyResult,
    Variable,
    VariableKind,
)

# ---------------------------------------------------------------------------
# Layout constants (SVG coordinate space)
# ---------------------------------------------------------------------------

_MACRO_Y = 80.0
_MESO_Y = 200.0
_MICRO_Y_START = 320.0
_MICRO_Y_SPACING = 50.0
_X_PADDING = 80.0


def _layout_nodes(nodes: list[TopologyNode], canvas_width: float = 900.0) -> list[TopologyNode]:
    """Assign x/y coordinates to nodes by level in horizontal bands."""
    by_level: dict[TopologyLevel, list[int]] = {
        TopologyLevel.MACRO: [],
        TopologyLevel.MESO: [],
        TopologyLevel.MICRO: [],
    }
    for i, node in enumerate(nodes):
        by_level[node.level].append(i)

    laid_out: list[TopologyNode] = list(nodes)

    for level, indices in by_level.items():
        if not indices:
            continue

        if level == TopologyLevel.MACRO:
            y = _MACRO_Y
        elif level == TopologyLevel.MESO:
            y = _MESO_Y
        else:
            y = _MICRO_Y_START

        count = len(indices)
        usable = canvas_width - 2 * _X_PADDING
        spacing = usable / max(count, 1)

        for rank, idx in enumerate(indices):
            x = _X_PADDING + spacing * (rank + 0.5)
            if level == TopologyLevel.MICRO:
                y = _MICRO_Y_START + rank * _MICRO_Y_SPACING
                y = min(y, 800.0)
            laid_out[idx] = replace(laid_out[idx], x=round(x, 1), y=round(y, 1))

    return laid_out


# ---------------------------------------------------------------------------
# Edge construction
# ---------------------------------------------------------------------------


def _build_edges(
    nodes: list[TopologyNode],
    variables: list[Variable],
) -> list[TopologyEdge]:
    """Build directed edges between topology nodes."""
    edges: list[TopologyEdge] = []
    node_by_var_id: dict[str, str] = {}

    for node in nodes:
        for var in node.variables:
            node_by_var_id[var.id] = node.id

    # Group nodes by level
    macro_ids = [n.id for n in nodes if n.level == TopologyLevel.MACRO]
    meso_ids = [n.id for n in nodes if n.level == TopologyLevel.MESO]
    micro_ids = [n.id for n in nodes if n.level == TopologyLevel.MICRO]

    # CONTAINS: macro → meso → micro (hierarchy)
    for macro_id in macro_ids:
        for meso_id in meso_ids:
            edges.append(
                TopologyEdge(
                    source_id=macro_id,
                    target_id=meso_id,
                    kind=EdgeKind.CONTAINS,
                    weight=0.5,
                )
            )
    for meso_id in meso_ids:
        for micro_id in micro_ids:
            edges.append(
                TopologyEdge(
                    source_id=meso_id,
                    target_id=micro_id,
                    kind=EdgeKind.CONTAINS,
                    weight=0.3,
                )
            )

    # SUPPORTS: same-kind micro nodes
    micro_nodes = [n for n in nodes if n.level == TopologyLevel.MICRO]
    for i, a in enumerate(micro_nodes):
        for b in micro_nodes[i + 1 :]:
            if a.kind == b.kind and a.kind != VariableKind.INDETERMINATE:
                edges.append(
                    TopologyEdge(
                        source_id=a.id,
                        target_id=b.id,
                        kind=EdgeKind.SUPPORTS,
                        weight=0.7,
                    )
                )

    # CONTRADICTS: opposing-kind micro nodes
    pseudo_nodes = [n for n in micro_nodes if n.kind == VariableKind.PSEUDO]
    true_nodes = [n for n in micro_nodes if n.kind == VariableKind.TRUE]
    for p in pseudo_nodes:
        for t in true_nodes:
            edges.append(
                TopologyEdge(
                    source_id=p.id,
                    target_id=t.id,
                    kind=EdgeKind.CONTRADICTS,
                    weight=0.8,
                )
            )

    # ESCALATES_TO: sequential micro nodes with increasing classification scores
    for i in range(len(micro_nodes) - 1):
        a = micro_nodes[i]
        b = micro_nodes[i + 1]
        if a.variables and b.variables:
            a_mean = _classification_mean(a.variables[0].classification)
            b_mean = _classification_mean(b.variables[0].classification)
            if b_mean > a_mean + 0.05:
                edges.append(
                    TopologyEdge(
                        source_id=a.id,
                        target_id=b.id,
                        kind=EdgeKind.ESCALATES_TO,
                        weight=0.6,
                    )
                )

    return edges


def _classification_mean(cls: object) -> float:
    """Mean of the four classification axes."""
    from si_protocols.topology.types import VariableClassification

    if not isinstance(cls, VariableClassification):
        return 0.0
    return (
        cls.falsifiability + cls.verifiability + cls.domain_coherence + cls.logical_dependency
    ) / 4


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_topology(
    variables: list[Variable],
    *,
    lang: SupportedLang = "en",
    engine_name: str = "",
    canvas_width: float = 900.0,
) -> TopologyResult:
    """Build a complete topology graph from extracted variables.

    Returns a ``TopologyResult`` with nodes placed in three horizontal bands
    (macro/meso/micro) and edges representing structural relationships.
    """
    if not variables:
        return TopologyResult(lang=lang, engine_name=engine_name)

    # Create micro-level nodes (one per variable)
    nodes: list[TopologyNode] = []
    for var in variables:
        label = var.text[:40] + "..." if len(var.text) > 40 else var.text
        nodes.append(
            TopologyNode(
                id=f"n_{var.id}",
                label=label,
                level=TopologyLevel.MICRO,
                kind=var.kind,
                variables=(var,),
            )
        )

    # Create meso-level summary nodes (group by kind)
    kinds_present = {v.kind for v in variables}
    for kind in sorted(kinds_present, key=lambda k: k.value):
        kind_vars = tuple(v for v in variables if v.kind == kind)
        if kind_vars:
            nodes.append(
                TopologyNode(
                    id=f"n_meso_{kind.value}",
                    label=f"{kind.value} group ({len(kind_vars)})",
                    level=TopologyLevel.MESO,
                    kind=kind,
                    variables=kind_vars,
                )
            )

    # Create a single macro-level summary node
    dominant_kind = max(kinds_present, key=lambda k: sum(1 for v in variables if v.kind == k))
    nodes.append(
        TopologyNode(
            id="n_macro",
            label=f"text topology ({len(variables)} vars)",
            level=TopologyLevel.MACRO,
            kind=dominant_kind,
            variables=tuple(variables),
        )
    )

    # Layout
    nodes = _layout_nodes(nodes, canvas_width)

    # Edges
    edges = _build_edges(nodes, variables)

    # Counts
    pseudo_count = sum(1 for v in variables if v.kind == VariableKind.PSEUDO)
    true_count = sum(1 for v in variables if v.kind == VariableKind.TRUE)
    indeterminate_count = sum(1 for v in variables if v.kind == VariableKind.INDETERMINATE)

    return TopologyResult(
        nodes=tuple(nodes),
        edges=tuple(edges),
        variables=tuple(variables),
        pseudo_count=pseudo_count,
        true_count=true_count,
        indeterminate_count=indeterminate_count,
        lang=lang,
        engine_name=engine_name,
    )
