"""Tests for topology data types — enums, frozen dataclasses, validation."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, asdict

import pytest

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

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class TestVariableKind:
    def test_members(self) -> None:
        assert set(VariableKind) == {
            VariableKind.PSEUDO,
            VariableKind.TRUE,
            VariableKind.INDETERMINATE,
        }

    def test_values(self) -> None:
        assert VariableKind.PSEUDO.value == "pseudo"
        assert VariableKind.TRUE.value == "true"
        assert VariableKind.INDETERMINATE.value == "indeterminate"


class TestTopologyLevel:
    def test_members(self) -> None:
        assert set(TopologyLevel) == {
            TopologyLevel.MACRO,
            TopologyLevel.MESO,
            TopologyLevel.MICRO,
        }


class TestEdgeKind:
    def test_members(self) -> None:
        assert set(EdgeKind) == {
            EdgeKind.SUPPORTS,
            EdgeKind.CONTRADICTS,
            EdgeKind.ESCALATES_TO,
            EdgeKind.CONTAINS,
            EdgeKind.DEPENDS_ON,
        }


# ---------------------------------------------------------------------------
# VariableClassification
# ---------------------------------------------------------------------------


class TestVariableClassification:
    def test_defaults(self) -> None:
        vc = VariableClassification()
        assert vc.falsifiability == 0.0
        assert vc.verifiability == 0.0
        assert vc.domain_coherence == 0.0
        assert vc.logical_dependency == 0.0

    def test_frozen(self) -> None:
        vc = VariableClassification(falsifiability=0.5)
        with pytest.raises(FrozenInstanceError):
            vc.falsifiability = 0.9  # type: ignore[misc]

    def test_valid_range(self) -> None:
        vc = VariableClassification(
            falsifiability=0.0,
            verifiability=1.0,
            domain_coherence=0.5,
            logical_dependency=0.3,
        )
        assert vc.verifiability == 1.0

    def test_out_of_range_low(self) -> None:
        with pytest.raises(ValueError, match="falsifiability"):
            VariableClassification(falsifiability=-0.1)

    def test_out_of_range_high(self) -> None:
        with pytest.raises(ValueError, match="verifiability"):
            VariableClassification(verifiability=1.1)


# ---------------------------------------------------------------------------
# Variable
# ---------------------------------------------------------------------------


class TestVariable:
    def _make(self, **kwargs: object) -> Variable:
        defaults: dict[str, object] = {
            "id": "v1",
            "text": "test claim",
            "source_span": (0, 10),
            "classification": VariableClassification(),
            "kind": VariableKind.INDETERMINATE,
            "level": TopologyLevel.MICRO,
        }
        defaults.update(kwargs)
        return Variable(**defaults)  # type: ignore[arg-type]

    def test_frozen(self) -> None:
        v = self._make()
        with pytest.raises(FrozenInstanceError):
            v.text = "changed"  # type: ignore[misc]

    def test_fields(self) -> None:
        v = self._make(id="v42", text="claim", source_span=(5, 20), confidence=0.9)
        assert v.id == "v42"
        assert v.source_span == (5, 20)
        assert v.confidence == 0.9

    def test_default_confidence(self) -> None:
        v = self._make()
        assert v.confidence == 0.5


# ---------------------------------------------------------------------------
# TopologyNode
# ---------------------------------------------------------------------------


class TestTopologyNode:
    def test_frozen(self) -> None:
        node = TopologyNode(
            id="n1", label="test", level=TopologyLevel.MACRO, kind=VariableKind.TRUE
        )
        with pytest.raises(FrozenInstanceError):
            node.x = 100.0  # type: ignore[misc]

    def test_empty_variables_default(self) -> None:
        node = TopologyNode(
            id="n1", label="test", level=TopologyLevel.MACRO, kind=VariableKind.TRUE
        )
        assert node.variables == ()

    def test_coordinates_default(self) -> None:
        node = TopologyNode(
            id="n1", label="test", level=TopologyLevel.MACRO, kind=VariableKind.TRUE
        )
        assert node.x == 0.0
        assert node.y == 0.0


# ---------------------------------------------------------------------------
# TopologyEdge
# ---------------------------------------------------------------------------


class TestTopologyEdge:
    def test_frozen(self) -> None:
        edge = TopologyEdge(source_id="n1", target_id="n2", kind=EdgeKind.SUPPORTS)
        with pytest.raises(FrozenInstanceError):
            edge.weight = 2.0  # type: ignore[misc]

    def test_default_weight(self) -> None:
        edge = TopologyEdge(source_id="n1", target_id="n2", kind=EdgeKind.CONTAINS)
        assert edge.weight == 1.0


# ---------------------------------------------------------------------------
# TopologyResult
# ---------------------------------------------------------------------------


class TestTopologyResult:
    def test_frozen(self) -> None:
        result = TopologyResult()
        with pytest.raises(FrozenInstanceError):
            result.pseudo_count = 5  # type: ignore[misc]

    def test_defaults(self) -> None:
        result = TopologyResult()
        assert result.nodes == ()
        assert result.edges == ()
        assert result.variables == ()
        assert result.pseudo_count == 0
        assert result.true_count == 0
        assert result.indeterminate_count == 0
        assert result.lang == "en"
        assert result.engine_name == ""

    def test_message_default(self) -> None:
        result = TopologyResult()
        assert "Topology analysis completed" in result.message

    def test_asdict_structure(self) -> None:
        """Verify the dataclass serialises cleanly via asdict."""
        result = TopologyResult(lang="ja", engine_name="rule", pseudo_count=3, true_count=1)
        d = asdict(result)
        assert d["lang"] == "ja"
        assert d["engine_name"] == "rule"
        assert d["pseudo_count"] == 3
        assert isinstance(d["nodes"], (list, tuple))
