"""CLI entry point for topology analysis.

Usage::

    si-topology FILE [--engine rule|anthropic] [--lang en|ja] [--format svg|json] [-o OUTPUT]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> None:
    """Run topology analysis from the command line."""
    parser = argparse.ArgumentParser(
        description="si-protocols — Topology Analysis for Spiritual Intelligence v0.1",
    )
    parser.add_argument("file", help="Path to the text file to analyse")
    parser.add_argument(
        "--engine",
        choices=["rule", "anthropic"],
        default="rule",
        help="Analysis engine to use (default: rule)",
    )
    parser.add_argument(
        "--lang",
        choices=["en", "ja"],
        default="en",
        help="Language of the input text (default: en)",
    )
    parser.add_argument(
        "--format",
        choices=["svg", "json"],
        default="svg",
        dest="output_format",
        help="Output format (default: svg)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file path (default: <input>.topology.svg or stdout for json)",
    )

    args = parser.parse_args()

    # Read input file
    filepath = Path(args.file)
    if not filepath.is_file():
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    text = filepath.read_text(encoding="utf-8")

    # Select engine
    if args.engine == "anthropic":
        from si_protocols.topology.anthropic_engine import AnthropicEngine

        engine = AnthropicEngine()
    else:
        from si_protocols.topology.rule_engine import RuleEngine

        engine = RuleEngine()

    # Extract variables
    variables = engine.extract_variables(text, lang=args.lang)

    # Build topology
    from si_protocols.topology.topology_builder import build_topology

    result = build_topology(variables, lang=args.lang, engine_name=engine.name)

    # Output
    if args.output_format == "json":
        from si_protocols.topology.output import render_topology_json

        if args.output:
            with Path(args.output).open("w", encoding="utf-8") as f:
                render_topology_json(result, file=f)
        else:
            render_topology_json(result)
    else:
        from si_protocols.topology.svg_renderer import save_svg

        output_path = args.output or str(filepath.with_suffix(".topology.svg"))
        save_svg(result, output_path)
        print(f"SVG written to {output_path}", file=sys.stderr)
