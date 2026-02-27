"""Tests for the topology graph builder."""

from __future__ import annotations

from si_protocols.topology.topology_builder import build_topology
from si_protocols.topology.types import (
    EdgeKind,
    TopologyLevel,
    Variable,
    VariableClassification,
    VariableKind,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_var(
    var_id: str,
    kind: VariableKind = VariableKind.INDETERMINATE,
    **kwargs: object,
) -> Variable:
    defaults: dict[str, object] = {
        "text": f"claim {var_id}",
        "source_span": (0, 10),
        "classification": VariableClassification(),
        "level": TopologyLevel.MICRO,
        "confidence": 0.5,
    }
    defaults.update(kwargs)
    return Variable(id=var_id, kind=kind, **defaults)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestEmptyInput:
    def test_empty_variables(self) -> None:
        result = build_topology([])
        assert result.nodes == ()
        assert result.edges == ()
        assert result.pseudo_count == 0

    def test_lang_and_engine_passed_through(self) -> None:
        result = build_topology([], lang="ja", engine_name="test")
        assert result.lang == "ja"
        assert result.engine_name == "test"


class TestNodeConstruction:
    def test_micro_nodes_created(self) -> None:
        variables = [_make_var("v1"), _make_var("v2")]
        result = build_topology(variables)
        micro_nodes = [n for n in result.nodes if n.level == TopologyLevel.MICRO]
        assert len(micro_nodes) == 2

    def test_meso_nodes_by_kind(self) -> None:
        variables = [
            _make_var("v1", kind=VariableKind.PSEUDO),
            _make_var("v2", kind=VariableKind.TRUE),
        ]
        result = build_topology(variables)
        meso_nodes = [n for n in result.nodes if n.level == TopologyLevel.MESO]
        assert len(meso_nodes) == 2

    def test_single_macro_node(self) -> None:
        variables = [_make_var("v1"), _make_var("v2"), _make_var("v3")]
        result = build_topology(variables)
        macro_nodes = [n for n in result.nodes if n.level == TopologyLevel.MACRO]
        assert len(macro_nodes) == 1

    def test_macro_label_includes_count(self) -> None:
        variables = [_make_var("v1"), _make_var("v2")]
        result = build_topology(variables)
        macro = next(n for n in result.nodes if n.level == TopologyLevel.MACRO)
        assert "2 vars" in macro.label


class TestEdgeConstruction:
    def test_contains_edges_exist(self) -> None:
        variables = [_make_var("v1"), _make_var("v2")]
        result = build_topology(variables)
        contains = [e for e in result.edges if e.kind == EdgeKind.CONTAINS]
        assert len(contains) > 0

    def test_supports_edges_for_same_kind(self) -> None:
        variables = [
            _make_var("v1", kind=VariableKind.PSEUDO),
            _make_var("v2", kind=VariableKind.PSEUDO),
        ]
        result = build_topology(variables)
        supports = [e for e in result.edges if e.kind == EdgeKind.SUPPORTS]
        assert len(supports) >= 1

    def test_contradicts_edges_for_opposing_kinds(self) -> None:
        variables = [
            _make_var("v1", kind=VariableKind.PSEUDO),
            _make_var("v2", kind=VariableKind.TRUE),
        ]
        result = build_topology(variables)
        contradicts = [e for e in result.edges if e.kind == EdgeKind.CONTRADICTS]
        assert len(contradicts) >= 1

    def test_escalation_edges(self) -> None:
        """Sequential nodes with increasing scores should get ESCALATES_TO edges."""
        low_cls = VariableClassification(
            falsifiability=0.1,
            verifiability=0.1,
            domain_coherence=0.0,
            logical_dependency=0.1,
        )
        high_cls = VariableClassification(
            falsifiability=0.9,
            verifiability=0.9,
            domain_coherence=0.5,
            logical_dependency=0.9,
        )
        variables = [
            _make_var("v1", classification=low_cls),
            _make_var("v2", classification=high_cls),
        ]
        result = build_topology(variables)
        escalates = [e for e in result.edges if e.kind == EdgeKind.ESCALATES_TO]
        assert len(escalates) >= 1


class TestLayout:
    def test_nodes_have_coordinates(self) -> None:
        variables = [_make_var("v1")]
        result = build_topology(variables)
        for node in result.nodes:
            # At least one coordinate should be non-zero after layout
            assert node.x > 0 or node.y > 0

    def test_macro_y_band(self) -> None:
        variables = [_make_var("v1")]
        result = build_topology(variables)
        macro = next(n for n in result.nodes if n.level == TopologyLevel.MACRO)
        assert 50 <= macro.y <= 120

    def test_micro_y_below_meso(self) -> None:
        variables = [_make_var("v1"), _make_var("v2")]
        result = build_topology(variables)
        micro_ys = [n.y for n in result.nodes if n.level == TopologyLevel.MICRO]
        meso_ys = [n.y for n in result.nodes if n.level == TopologyLevel.MESO]
        if micro_ys and meso_ys:
            assert min(micro_ys) > max(meso_ys)


class TestCounts:
    def test_pseudo_count(self) -> None:
        variables = [
            _make_var("v1", kind=VariableKind.PSEUDO),
            _make_var("v2", kind=VariableKind.PSEUDO),
            _make_var("v3", kind=VariableKind.TRUE),
        ]
        result = build_topology(variables)
        assert result.pseudo_count == 2

    def test_true_count(self) -> None:
        variables = [
            _make_var("v1", kind=VariableKind.TRUE),
            _make_var("v2", kind=VariableKind.INDETERMINATE),
        ]
        result = build_topology(variables)
        assert result.true_count == 1

    def test_indeterminate_count(self) -> None:
        variables = [_make_var("v1")]
        result = build_topology(variables)
        assert result.indeterminate_count == 1
