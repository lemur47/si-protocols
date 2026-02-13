"""Output formatting for the threat filter CLI.

Provides Rich (colour-coded) and JSON output modes.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from typing import IO, TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from si_protocols.threat_filter import ThreatResult


def _threat_style(score: float) -> str:
    """Return a Rich style string based on threat score.

    Green for low (0-33), yellow for medium (34-66), red bold for high (67-100).
    """
    if score <= 33:
        return "green"
    if score <= 66:
        return "yellow"
    return "red bold"


def render_rich(
    result: ThreatResult,
    filepath: str,
    *,
    console: Console | None = None,
) -> None:
    """Render threat analysis results with Rich formatting.

    Args:
        result: The ThreatResult from hybrid_score.
        filepath: Path to the analysed file.
        console: Optional Console instance for testability.
    """
    if console is None:
        console = Console()

    style = _threat_style(result.overall_threat_score)

    # --- Header ---
    console.print(
        Panel(
            f"[bold]si-protocols Threat Analysis v0.1[/bold]\nFile: {filepath}",
            expand=False,
        )
    )

    # --- Score breakdown ---
    score_text = Text()
    score_text.append("Overall Threat Score: ")
    score_text.append(f"{result.overall_threat_score}/100", style=style)
    console.print(score_text)
    console.print(f"  \u251c\u2500\u2500 Tech layer: {result.tech_contribution}")
    console.print(f"  \u2514\u2500\u2500 Heuristic intuition: {result.intuition_contribution}")

    # --- Detected hits table ---
    hit_rows: list[tuple[str, list[str]]] = [
        ("Detected entities", result.detected_entities),
        ("Authority claims", result.authority_hits),
        ("Urgency patterns", result.urgency_hits),
        ("Emotion triggers", result.emotion_hits),
        ("Logical contradictions", result.contradiction_hits),
        ("Source attribution", result.source_attribution_hits),
        ("Commitment escalation", result.escalation_hits),
    ]
    visible_rows = [(label, hits) for label, hits in hit_rows if hits]

    if visible_rows:
        table = Table(show_header=True, expand=False)
        table.add_column("Category", style="bold")
        table.add_column("Hits")
        for label, hits in visible_rows:
            table.add_row(label, ", ".join(hits))
        console.print(table)

    # --- Disclaimer footer ---
    console.print(Panel(result.message, title="Disclaimer", style="dim"))


def render_json(
    result: ThreatResult,
    *,
    file: IO[str] | None = None,
) -> None:
    """Render threat analysis results as JSON.

    Args:
        result: The ThreatResult from hybrid_score.
        file: Optional file object for output (defaults to sys.stdout).
    """
    out = file if file is not None else sys.stdout
    json.dump(asdict(result), out, indent=2)
    print(file=out)  # trailing newline
