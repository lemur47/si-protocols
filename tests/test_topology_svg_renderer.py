"""Tests for the topology SVG renderer."""

from __future__ import annotations

import xml.etree.ElementTree as ET

from si_protocols.topology.svg_renderer import render_svg
from si_protocols.topology.topology_builder import build_topology
from si_protocols.topology.types import (
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
    kind: VariableKind = VariableKind.PSEUDO,
) -> Variable:
    return Variable(
        id=var_id,
        text=f"claim {var_id}",
        source_span=(0, 10),
        classification=VariableClassification(
            falsifiability=0.8 if kind == VariableKind.PSEUDO else 0.1,
            verifiability=0.7 if kind == VariableKind.PSEUDO else 0.1,
        ),
        kind=kind,
        level=TopologyLevel.MICRO,
    )


def _sample_result():
    variables = [
        _make_var("v1", VariableKind.PSEUDO),
        _make_var("v2", VariableKind.TRUE),
        _make_var("v3", VariableKind.INDETERMINATE),
    ]
    return build_topology(variables, engine_name="rule")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRenderSvg:
    def test_returns_string(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        assert isinstance(svg_str, str)

    def test_valid_xml(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        root = ET.fromstring(svg_str)
        assert root.tag == "{http://www.w3.org/2000/svg}svg" or root.tag == "svg"

    def test_has_circles(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        root = ET.fromstring(svg_str)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        circles = root.findall(".//svg:circle", ns) or root.findall(".//circle")
        assert len(circles) > 0

    def test_has_lines_for_edges(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        root = ET.fromstring(svg_str)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        lines = root.findall(".//svg:line", ns) or root.findall(".//line")
        # At least one edge + title separator line
        assert len(lines) >= 1

    def test_has_text_elements(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        root = ET.fromstring(svg_str)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        texts = root.findall(".//svg:text", ns) or root.findall(".//text")
        assert len(texts) > 0

    def test_background_colour(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        assert "#0a0a0f" in svg_str

    def test_pseudo_colour(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        assert "#ff4444" in svg_str

    def test_true_colour(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        assert "#00ffa3" in svg_str

    def test_indeterminate_colour(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        assert "#ffaa00" in svg_str

    def test_hud_frame_present(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        root = ET.fromstring(svg_str)
        ns = {"svg": "http://www.w3.org/2000/svg"}
        paths = root.findall(".//svg:path", ns) or root.findall(".//path")
        # 4 corner brackets
        assert len(paths) >= 4

    def test_title_present(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        assert "TOPOLOGY ANALYSIS" in svg_str

    def test_legend_present(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        assert "LEGEND" in svg_str

    def test_statistics_present(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        assert "STATISTICS" in svg_str

    def test_glow_filter_defined(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        assert 'id="glow"' in svg_str

    def test_scan_pattern_defined(self) -> None:
        result = _sample_result()
        svg_str = render_svg(result)
        assert 'id="scan"' in svg_str


class TestEmptyResult:
    def test_empty_result_renders(self) -> None:
        from si_protocols.topology.types import TopologyResult

        result = TopologyResult()
        svg_str = render_svg(result)
        assert "TOPOLOGY ANALYSIS" in svg_str
        root = ET.fromstring(svg_str)
        assert root is not None
