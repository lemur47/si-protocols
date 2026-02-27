"""Tests for the topology CLI entry point."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


@pytest.mark.slow
class TestCli:
    def test_svg_output(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """CLI creates an SVG file from a text input."""
        input_file = tmp_path / "input.txt"
        input_file.write_text(
            "The ascended masters say that only those who awaken to the divine frequency "
            "will transcend. You must act now. Scientists say this is proven.",
            encoding="utf-8",
        )
        output_file = tmp_path / "output.svg"

        monkeypatch.setattr(
            sys,
            "argv",
            ["si-topology", str(input_file), "-o", str(output_file)],
        )

        from si_protocols.topology.cli import main

        main()

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "<svg" in content

    def test_json_output(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """CLI produces valid JSON output."""
        input_file = tmp_path / "input.txt"
        input_file.write_text(
            "The ascended masters say that only those who awaken to the divine frequency "
            "will transcend. Scientists say this is proven.",
            encoding="utf-8",
        )
        output_file = tmp_path / "output.json"

        monkeypatch.setattr(
            sys,
            "argv",
            ["si-topology", str(input_file), "--format", "json", "-o", str(output_file)],
        )

        from si_protocols.topology.cli import main

        main()

        assert output_file.exists()
        data = json.loads(output_file.read_text(encoding="utf-8"))
        assert "nodes" in data
        assert "variables" in data

    def test_missing_file_exits(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """CLI exits with status 1 for missing input file."""
        monkeypatch.setattr(
            sys,
            "argv",
            ["si-topology", "/nonexistent/file.txt"],
        )

        from si_protocols.topology.cli import main

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    def test_default_output_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """CLI defaults to <input>.topology.svg output."""
        input_file = tmp_path / "test.txt"
        input_file.write_text(
            "Ancient wisdom teaches that the quantum field reveals all truth. "
            "Scientists say this is proven many times.",
            encoding="utf-8",
        )

        monkeypatch.setattr(
            sys,
            "argv",
            ["si-topology", str(input_file)],
        )

        from si_protocols.topology.cli import main

        main()

        expected = tmp_path / "test.topology.svg"
        assert expected.exists()
