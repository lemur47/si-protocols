"""Tests for the output formatting module."""

import json
import re
from io import StringIO

from rich.console import Console

from si_protocols.output import _threat_style, render_json, render_rich
from si_protocols.threat_filter import ThreatResult

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _make_result(
    overall: float = 42.5,
    tech: float = 30.0,
    intuition: float = 20.0,
    entities: list[str] | None = None,
    authority: list[str] | None = None,
    urgency: list[str] | None = None,
    emotion: list[str] | None = None,
    contradictions: list[str] | None = None,
    attribution: list[str] | None = None,
    escalation: list[str] | None = None,
) -> ThreatResult:
    """Build a ThreatResult with overridable defaults."""
    return ThreatResult(
        overall_threat_score=overall,
        tech_contribution=tech,
        intuition_contribution=intuition,
        detected_entities=entities or [],
        authority_hits=authority or [],
        urgency_hits=urgency or [],
        emotion_hits=emotion or [],
        contradiction_hits=contradictions or [],
        source_attribution_hits=attribution or [],
        escalation_hits=escalation or [],
    )


class TestThreatStyle:
    def test_low_score_green(self) -> None:
        assert _threat_style(0) == "green"
        assert _threat_style(33) == "green"

    def test_medium_score_yellow(self) -> None:
        assert _threat_style(34) == "yellow"
        assert _threat_style(66) == "yellow"

    def test_high_score_red(self) -> None:
        assert _threat_style(67) == "red bold"
        assert _threat_style(100) == "red bold"


class TestRenderRich:
    def _capture(self, result: ThreatResult, filepath: str = "test.txt") -> str:
        buf = StringIO()
        console = Console(file=buf, force_terminal=True, width=120)
        render_rich(result, filepath, console=console)
        return _ANSI_RE.sub("", buf.getvalue())

    def test_header_contains_title_and_filepath(self) -> None:
        output = self._capture(_make_result(), "my_file.txt")
        assert "si-protocols Threat Analysis v0.1" in output
        assert "my_file.txt" in output

    def test_score_breakdown_shown(self) -> None:
        result = _make_result(overall=55.0, tech=40.0, intuition=25.0)
        output = self._capture(result)
        assert "55.0/100" in output
        assert "Tech layer: 40.0" in output
        assert "Heuristic intuition: 25.0" in output

    def test_hits_shown_when_present(self) -> None:
        result = _make_result(
            authority=["the masters say"],
            emotion=["doom", "bliss"],
        )
        output = self._capture(result)
        assert "Authority claims" in output
        assert "the masters say" in output
        assert "Emotion triggers" in output
        assert "doom" in output
        assert "bliss" in output

    def test_empty_categories_hidden(self) -> None:
        result = _make_result()  # all hit lists empty
        output = self._capture(result)
        assert "Authority claims" not in output
        assert "Urgency patterns" not in output
        assert "Emotion triggers" not in output
        assert "Commitment escalation" not in output

    def test_escalation_hits_shown(self) -> None:
        result = _make_result(
            escalation=["early: consider, explore", "late: you must, total surrender"],
        )
        output = self._capture(result)
        assert "Commitment escalation" in output
        assert "early: consider, explore" in output

    def test_disclaimer_shown(self) -> None:
        output = self._capture(_make_result())
        assert "local tool" in output.lower()

    def test_low_threat_colour(self) -> None:
        result = _make_result(overall=10.0)
        output = self._capture(result)
        assert "10.0/100" in output

    def test_high_threat_colour(self) -> None:
        result = _make_result(overall=85.0)
        output = self._capture(result)
        assert "85.0/100" in output


class TestRenderJson:
    def _capture(self, result: ThreatResult) -> str:
        buf = StringIO()
        render_json(result, file=buf)
        return buf.getvalue()

    def test_valid_json(self) -> None:
        output = self._capture(_make_result())
        data = json.loads(output)
        assert isinstance(data, dict)

    def test_all_fields_present(self) -> None:
        output = self._capture(_make_result())
        data = json.loads(output)
        expected_keys = {
            "overall_threat_score",
            "tech_contribution",
            "intuition_contribution",
            "detected_entities",
            "authority_hits",
            "urgency_hits",
            "emotion_hits",
            "contradiction_hits",
            "source_attribution_hits",
            "escalation_hits",
            "message",
        }
        assert set(data.keys()) == expected_keys

    def test_hits_serialised(self) -> None:
        result = _make_result(authority=["ancient wisdom"], emotion=["fear", "bliss"])
        data = json.loads(self._capture(result))
        assert data["authority_hits"] == ["ancient wisdom"]
        assert data["emotion_hits"] == ["fear", "bliss"]

    def test_empty_lists_preserved(self) -> None:
        data = json.loads(self._capture(_make_result()))
        assert data["detected_entities"] == []
        assert data["urgency_hits"] == []

    def test_scores_match(self) -> None:
        result = _make_result(overall=72.5, tech=50.0, intuition=30.0)
        data = json.loads(self._capture(result))
        assert data["overall_threat_score"] == 72.5
        assert data["tech_contribution"] == 50.0
        assert data["intuition_contribution"] == 30.0
