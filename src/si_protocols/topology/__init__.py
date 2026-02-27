"""Topology module — fractal-topology analysis for variable extraction and graph building.

Public API re-exports for convenient access.
"""

from si_protocols.topology.engine import AnalysisEngine
from si_protocols.topology.output import render_topology_json
from si_protocols.topology.rule_engine import RuleEngine
from si_protocols.topology.svg_renderer import render_svg, save_svg
from si_protocols.topology.topology_builder import build_topology
from si_protocols.topology.types import (
    EdgeKind,
    TopologyEdge,
    TopologyLevel,
    TopologyNode,
    TopologyResult,
    Variable,
    VariableClassification,
    VariableKind,
)

__all__ = [
    "AnalysisEngine",
    "EdgeKind",
    "RuleEngine",
    "TopologyEdge",
    "TopologyLevel",
    "TopologyNode",
    "TopologyResult",
    "Variable",
    "VariableClassification",
    "VariableKind",
    "build_topology",
    "render_svg",
    "render_topology_json",
    "save_svg",
]
