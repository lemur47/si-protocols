"""SVG renderer for topology graphs.

Uses ``xml.etree.ElementTree`` - no external SVG library. Matches the
intelligence-themed design system from ``site-cc/public/images/``.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET  # nosec B405 — generating SVG, not parsing untrusted XML
from pathlib import Path

from si_protocols.topology.types import (
    EdgeKind,
    TopologyLevel,
    TopologyResult,
    VariableKind,
)

# ---------------------------------------------------------------------------
# Design system constants
# ---------------------------------------------------------------------------

_BG = "#0a0a0f"
_TEXT_PRIMARY = "#e0e0e8"
_TEXT_SECONDARY = "#8888a0"
_FRAME_STROKE = "#2a2a3a"
_HUD_ACCENT = "#00ffa3"

_NODE_COLOURS: dict[VariableKind, str] = {
    VariableKind.PSEUDO: "#ff4444",
    VariableKind.TRUE: "#00ffa3",
    VariableKind.INDETERMINATE: "#ffaa00",
}

_EDGE_STYLES: dict[EdgeKind, tuple[str, str, str]] = {
    # (stroke, dasharray, opacity)
    EdgeKind.CONTAINS: (_FRAME_STROKE, "4,4", "0.4"),
    EdgeKind.SUPPORTS: ("#00ffa3", "none", "0.6"),
    EdgeKind.CONTRADICTS: ("#ff4444", "none", "0.6"),
    EdgeKind.ESCALATES_TO: ("#ffaa00", "none", "0.5"),
    EdgeKind.DEPENDS_ON: ("#4488ff", "2,4", "0.5"),
}

_NODE_RADII: dict[TopologyLevel, int] = {
    TopologyLevel.MACRO: 16,
    TopologyLevel.MESO: 10,
    TopologyLevel.MICRO: 6,
}

_FONT = "'Courier New','Lucida Console',monospace"


# ---------------------------------------------------------------------------
# SVG construction helpers
# ---------------------------------------------------------------------------


def _el(parent: ET.Element, tag: str, attrs: dict[str, str]) -> ET.Element:
    """Create a subelement with an explicit attribute dict.

    Accepts hyphenated attribute names (``stroke-width``, ``font-size``, etc.)
    without triggering pyright keyword-argument errors.
    """
    return ET.SubElement(parent, tag, attrib=attrs)


def _add_defs(svg: ET.Element) -> None:
    """Add reusable filter and pattern definitions."""
    defs = ET.SubElement(svg, "defs")

    # Glow filter
    glow = ET.SubElement(defs, "filter", id="glow")
    ET.SubElement(glow, "feGaussianBlur", stdDeviation="3", result="b")
    merge = ET.SubElement(glow, "feMerge")
    _el(merge, "feMergeNode", {"in": "b"})
    _el(merge, "feMergeNode", {"in": "SourceGraphic"})

    # Scan-line overlay
    pattern = _el(
        defs,
        "pattern",
        {"id": "scan", "width": "4", "height": "4", "patternUnits": "userSpaceOnUse"},
    )
    ET.SubElement(pattern, "rect", width="4", height="2", fill="#fff", opacity="0.015")


def _add_background(svg: ET.Element, width: int, height: int) -> None:
    """Draw background, scan overlay, HUD frame, and border."""
    sw, sh = str(width), str(height)
    ET.SubElement(svg, "rect", width=sw, height=sh, fill=_BG)
    ET.SubElement(svg, "rect", width=sw, height=sh, fill="url(#scan)")

    # HUD corner brackets
    corners = [
        "M 24 8 L 8 8 L 8 36",
        f"M {width - 24} 8 L {width - 8} 8 L {width - 8} 36",
        f"M 8 {height - 36} L 8 {height - 8} L 24 {height - 8}",
        f"M {width - 8} {height - 36} L {width - 8} {height - 8} L {width - 24} {height - 8}",
    ]
    for d in corners:
        _el(
            svg,
            "path",
            {
                "d": d,
                "stroke": _HUD_ACCENT,
                "fill": "none",
                "stroke-width": "1.5",
                "opacity": "0.5",
            },
        )

    # Border
    _el(
        svg,
        "rect",
        {
            "x": "4",
            "y": "4",
            "width": str(width - 8),
            "height": str(height - 8),
            "rx": "2",
            "fill": "none",
            "stroke": _FRAME_STROKE,
            "stroke-width": "0.5",
        },
    )


def _add_title(svg: ET.Element, width: int) -> None:
    """Draw title bar."""
    _el(
        svg,
        "line",
        {
            "x1": "20",
            "y1": "44",
            "x2": str(width - 20),
            "y2": "44",
            "stroke": _FRAME_STROKE,
            "stroke-width": "0.5",
        },
    )
    title = _el(
        svg,
        "text",
        {
            "x": str(width // 2),
            "y": "32",
            "fill": _HUD_ACCENT,
            "opacity": "0.9",
            "font-size": "13",
            "font-family": _FONT,
            "text-anchor": "middle",
        },
    )
    title.text = "SI-PROTOCOLS // TOPOLOGY ANALYSIS"


def _add_edges(svg: ET.Element, result: TopologyResult) -> None:
    """Draw edges between nodes."""
    node_map = {n.id: n for n in result.nodes}
    for edge in result.edges:
        src = node_map.get(edge.source_id)
        tgt = node_map.get(edge.target_id)
        if not src or not tgt:
            continue

        colour, dash, opacity = _EDGE_STYLES.get(edge.kind, (_FRAME_STROKE, "none", "0.3"))
        attrs: dict[str, str] = {
            "x1": str(round(src.x)),
            "y1": str(round(src.y)),
            "x2": str(round(tgt.x)),
            "y2": str(round(tgt.y)),
            "stroke": colour,
            "stroke-width": "1",
            "opacity": opacity,
        }
        if dash != "none":
            attrs["stroke-dasharray"] = dash
        _el(svg, "line", attrs)


def _add_nodes(svg: ET.Element, result: TopologyResult) -> None:
    """Draw nodes as circles with labels."""
    for node in result.nodes:
        r = _NODE_RADII.get(node.level, 6)
        colour = _NODE_COLOURS.get(node.kind, _TEXT_SECONDARY)
        cx, cy = str(round(node.x)), str(round(node.y))

        _el(
            svg,
            "circle",
            {
                "cx": cx,
                "cy": cy,
                "r": str(r),
                "fill": colour,
                "opacity": "0.8",
                "filter": "url(#glow)",
            },
        )

        # Label (to right for micro, above for others)
        if node.level == TopologyLevel.MICRO:
            label_text = node.label[:30] + "..." if len(node.label) > 30 else node.label
            lbl = _el(
                svg,
                "text",
                {
                    "x": str(round(node.x) + r + 8),
                    "y": str(round(node.y) + 4),
                    "fill": _TEXT_SECONDARY,
                    "opacity": "0.7",
                    "font-size": "8",
                    "font-family": _FONT,
                },
            )
            lbl.text = label_text
        else:
            lbl = _el(
                svg,
                "text",
                {
                    "x": cx,
                    "y": str(round(node.y) - r - 6),
                    "fill": _TEXT_PRIMARY,
                    "opacity": "0.8",
                    "font-size": "10",
                    "font-family": _FONT,
                    "text-anchor": "middle",
                },
            )
            lbl.text = node.label


def _add_legend(svg: ET.Element, height: int) -> None:
    """Draw a legend panel in the bottom-left."""
    base_y = height - 80

    hdr = _el(
        svg,
        "text",
        {
            "x": "24",
            "y": str(base_y),
            "fill": _TEXT_PRIMARY,
            "opacity": "0.7",
            "font-size": "9",
            "font-family": _FONT,
        },
    )
    hdr.text = "LEGEND"

    items = [
        (_NODE_COLOURS[VariableKind.PSEUDO], "Pseudo-variable"),
        (_NODE_COLOURS[VariableKind.TRUE], "True-variable"),
        (_NODE_COLOURS[VariableKind.INDETERMINATE], "Indeterminate"),
    ]
    for i, (colour, label) in enumerate(items):
        y = base_y + 16 + i * 16
        _el(
            svg,
            "circle",
            {"cx": "32", "cy": str(y - 3), "r": "4", "fill": colour, "opacity": "0.8"},
        )
        txt = _el(
            svg,
            "text",
            {
                "x": "44",
                "y": str(y),
                "fill": _TEXT_SECONDARY,
                "opacity": "0.7",
                "font-size": "8",
                "font-family": _FONT,
            },
        )
        txt.text = label


def _add_stats(svg: ET.Element, result: TopologyResult, width: int, height: int) -> None:
    """Draw a statistics panel in the bottom-right."""
    base_y = height - 80
    base_x = width - 160

    hdr = _el(
        svg,
        "text",
        {
            "x": str(base_x),
            "y": str(base_y),
            "fill": _TEXT_PRIMARY,
            "opacity": "0.7",
            "font-size": "9",
            "font-family": _FONT,
        },
    )
    hdr.text = "STATISTICS"

    lines = [
        f"Variables: {len(result.variables)}",
        f"Pseudo: {result.pseudo_count}",
        f"True: {result.true_count}",
        f"Indeterminate: {result.indeterminate_count}",
    ]
    for i, line in enumerate(lines):
        txt = _el(
            svg,
            "text",
            {
                "x": str(base_x),
                "y": str(base_y + 16 + i * 14),
                "fill": _TEXT_SECONDARY,
                "opacity": "0.7",
                "font-size": "8",
                "font-family": _FONT,
            },
        )
        txt.text = line


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def render_svg(result: TopologyResult, *, width: int = 900, height: int = 600) -> str:
    """Render a ``TopologyResult`` as an SVG string.

    Dynamically grows the canvas height to fit all micro-level nodes.
    """
    # Auto-size height based on micro node count
    micro_count = sum(1 for n in result.nodes if n.level == TopologyLevel.MICRO)
    min_height = max(height, 400 + micro_count * 50)
    height = min(min_height, 2000)

    svg = ET.Element(
        "svg",
        attrib={
            "xmlns": "http://www.w3.org/2000/svg",
            "viewBox": f"0 0 {width} {height}",
            "font-family": _FONT,
        },
    )

    _add_defs(svg)
    _add_background(svg, width, height)
    _add_title(svg, width)
    _add_edges(svg, result)
    _add_nodes(svg, result)
    _add_legend(svg, height)
    _add_stats(svg, result, width, height)

    ET.indent(svg, space="  ")
    return ET.tostring(svg, encoding="unicode", xml_declaration=False)


def save_svg(result: TopologyResult, path: str | Path) -> None:
    """Render and save topology SVG to *path*."""
    content = render_svg(result)
    Path(path).write_text(content, encoding="utf-8")
