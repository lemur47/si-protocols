"""Tests for scripts/classification-gate.py — Airtable ID detection.

The gate script uses a hyphen in its filename, so it cannot be imported as a
normal module. We load it via importlib and exercise the check functions
directly plus integration tests that mock git staging.

Airtable IDs are never written as literals in this file — the gate scans test
files too, and would correctly flag them. All sample IDs are assembled at
import time from a shared 14-char body fragment.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

GATE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "classification-gate.py"

_BODY_14 = "0123456789" + "abcd"
_BODY_13 = "0123456789" + "abc"
_BODY_15 = "0123456789" + "abcde"
SAMPLE_APP_ID = "app" + _BODY_14
SAMPLE_TBL_ID = "tbl" + _BODY_14
SAMPLE_REC_ID = "rec" + _BODY_14
SAMPLE_FLD_ID = "fld" + _BODY_14
SPEC_AC4_LITERAL = "app" + _BODY_15


def _load_gate_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("classification_gate", GATE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["classification_gate"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def gate() -> ModuleType:
    return _load_gate_module()


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class TestAirtableIdDetection:
    def test_airtable_id_in_public_path_blocked(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "docs" / "notes.md", f"Base ID is {SAMPLE_APP_ID} today.\n")
        reason = gate.check_airtable_ids("docs/notes.md")
        assert reason is not None
        assert SAMPLE_APP_ID in reason

    def test_airtable_id_in_tmp_allowed(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "tmp" / "handoff.md", f"Base ID is {SAMPLE_APP_ID}.\n")
        assert gate.check_airtable_ids("tmp/handoff.md") is None

    def test_local_only_dir_allowlisted(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "local-only" / "notes.md", f"Base: {SAMPLE_APP_ID}\n")
        assert gate.check_airtable_ids("local-only/notes.md") is None

    def test_each_prefix_detected(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        target = tmp_path / "docs" / "notes.md"
        for prefix, ident in (
            ("app", SAMPLE_APP_ID),
            ("tbl", SAMPLE_TBL_ID),
            ("rec", SAMPLE_REC_ID),
            ("fld", SAMPLE_FLD_ID),
        ):
            _write(target, f"ID: {ident}\n")
            reason = gate.check_airtable_ids("docs/notes.md")
            assert reason is not None, f"expected block for prefix {prefix}"
            assert ident in reason

    def test_spec_ac4_literal_string_not_matched(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Spec AC #4's example string is 15 chars after the prefix — one
        longer than a real Airtable ID (3-char prefix + 14 alphanumerics =
        17 chars). The canonical regex ``{14}`` rejects the 18-char typo.
        Clarification raised in the execution log.
        """
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "docs" / "notes.md", f"Bad: {SPEC_AC4_LITERAL}\n")
        assert gate.check_airtable_ids("docs/notes.md") is None

    def test_thirteen_char_lookalike_not_blocked(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        body = f"app{_BODY_13} tbl{_BODY_13} rec{_BODY_13} fld{_BODY_13}\n"
        _write(tmp_path / "docs" / "notes.md", body)
        assert gate.check_airtable_ids("docs/notes.md") is None

    def test_fifteen_char_lookalike_not_blocked(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        body = f"app{_BODY_15} tbl{_BODY_15} rec{_BODY_15} fld{_BODY_15}\n"
        _write(tmp_path / "docs" / "notes.md", body)
        assert gate.check_airtable_ids("docs/notes.md") is None

    def test_angle_bracket_placeholders_not_blocked(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Template placeholders like ``app<14-char-id>`` must pass through."""
        monkeypatch.chdir(tmp_path)
        body = "Base ID: `app<14-char-id>` Work Items: `tbl<14-char-id>`\n"
        _write(tmp_path / "CLAUDE-internal.md.template", body)
        assert gate.check_airtable_ids("CLAUDE-internal.md.template") is None

    def test_non_scannable_extension_skipped(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "asset.bin", SAMPLE_APP_ID)
        assert gate.check_airtable_ids("asset.bin") is None


class TestGateMainExitCode:
    def test_main_exits_1_for_public_airtable_id(
        self,
        gate: ModuleType,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """AC #4 (intent): the gate against a file with a real-shape Airtable
        ID exits 1."""
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "notes.md", f"Base: {SAMPLE_APP_ID}\n")
        monkeypatch.setattr(gate, "get_staged_files", lambda: ["notes.md"])
        assert gate.main() == 1
        captured = capsys.readouterr()
        assert "Airtable identifier leaked" in captured.out
        assert SAMPLE_APP_ID in captured.out

    def test_main_exits_0_when_clean(
        self,
        gate: ModuleType,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "notes.md", "No secrets here.\n")
        monkeypatch.setattr(gate, "get_staged_files", lambda: ["notes.md"])
        assert gate.main() == 0

    def test_main_exits_0_when_id_in_tmp(
        self,
        gate: ModuleType,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "tmp" / "handoff.md", f"Base: {SAMPLE_APP_ID}\n")
        monkeypatch.setattr(gate, "get_staged_files", lambda: ["tmp/handoff.md"])
        assert gate.main() == 0
