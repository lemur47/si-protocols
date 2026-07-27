"""Tests for scripts/classification-gate.py.

Two layers of testing, because the gate has two kinds of behaviour:

- **Unit** — the check functions, loaded via importlib because the script's
  filename contains a hyphen and cannot be imported normally.
- **End-to-end** — the CLI modes (staged, ``--range``, ``--all``) driven as a
  subprocess inside a throwaway git repository, since they are the paths CI
  actually invokes.

Neither an Airtable ID nor a classification marker is ever written as a literal
here. The gate scans test files too, so an embedded literal would leave the
suite unable to commit itself — the "describe, don't embed" rule is a hard
constraint in this file, not a stylistic preference.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

GATE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "classification-gate.py"

# Resolved once, so the subprocess calls below carry a full executable path
# rather than relying on PATH resolution at call time.
GIT = shutil.which("git") or "git"

_BODY_14 = "0123456789" + "abcd"
_BODY_13 = "0123456789" + "abc"
_BODY_15 = "0123456789" + "abcde"
SAMPLE_APP_ID = "app" + _BODY_14
SAMPLE_TBL_ID = "tbl" + _BODY_14
SAMPLE_REC_ID = "rec" + _BODY_14
SAMPLE_FLD_ID = "fld" + _BODY_14
SPEC_AC4_LITERAL = "app" + _BODY_15

# One byte past the gate's read limit, and bytes that are not valid UTF-8.
OVERSIZE = 1_048_576 + 1
UNDECODABLE = b"\xff\xfe\x00\x80binary payload\xff"


def marker_text() -> str:
    """Assemble a classification marker without embedding one."""
    return "notes\n" + ": ".join(["CLASSIFICATION", "INTERNAL"]) + "\n"


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
    def test_airtable_id_in_public_path_blocked(self, gate: ModuleType) -> None:
        reason = gate.check_airtable_ids("docs/notes.md", f"Base ID is {SAMPLE_APP_ID} today.\n")
        assert reason is not None
        assert SAMPLE_APP_ID in reason

    def test_airtable_id_in_tmp_allowed(self, gate: ModuleType) -> None:
        assert gate.check_airtable_ids("tmp/handoff.md", f"Base ID is {SAMPLE_APP_ID}.\n") is None

    def test_local_only_dir_allowlisted(self, gate: ModuleType) -> None:
        assert gate.check_airtable_ids("local-only/notes.md", f"Base: {SAMPLE_APP_ID}\n") is None

    def test_each_prefix_detected(self, gate: ModuleType) -> None:
        for prefix, ident in (
            ("app", SAMPLE_APP_ID),
            ("tbl", SAMPLE_TBL_ID),
            ("rec", SAMPLE_REC_ID),
            ("fld", SAMPLE_FLD_ID),
        ):
            reason = gate.check_airtable_ids("docs/notes.md", f"ID: {ident}\n")
            assert reason is not None, f"expected block for prefix {prefix}"
            assert ident in reason

    def test_spec_ac4_literal_string_not_matched(self, gate: ModuleType) -> None:
        """Spec AC #4's example string is 15 chars after the prefix — one
        longer than a real Airtable ID (3-char prefix + 14 alphanumerics =
        17 chars). The canonical regex ``{14}`` rejects the 18-char typo.
        Clarification raised in the execution log.
        """
        assert gate.check_airtable_ids("docs/notes.md", f"Bad: {SPEC_AC4_LITERAL}\n") is None

    def test_thirteen_char_lookalike_not_blocked(self, gate: ModuleType) -> None:
        body = f"app{_BODY_13} tbl{_BODY_13} rec{_BODY_13} fld{_BODY_13}\n"
        assert gate.check_airtable_ids("docs/notes.md", body) is None

    def test_fifteen_char_lookalike_not_blocked(self, gate: ModuleType) -> None:
        body = f"app{_BODY_15} tbl{_BODY_15} rec{_BODY_15} fld{_BODY_15}\n"
        assert gate.check_airtable_ids("docs/notes.md", body) is None

    def test_angle_bracket_placeholders_not_blocked(self, gate: ModuleType) -> None:
        """Angle-bracket placeholders like ``app<14-char-id>`` must pass through."""
        body = "Base ID: `app<14-char-id>` Work Items: `tbl<14-char-id>`\n"
        assert gate.check_airtable_ids("placeholders.md", body) is None


class TestClassificationMarkers:
    def test_marker_detected(self, gate: ModuleType) -> None:
        reason = gate.check_content(marker_text())
        assert reason is not None

    def test_clean_prose_passes(self, gate: ModuleType) -> None:
        assert gate.check_content("Ordinary documentation about analysis.\n") is None


class TestUnscannableFilesFailClosed:
    """The three unscannable classes. Each used to be a silent pass."""

    def test_undecodable_is_a_violation(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        (tmp_path / "payload.dat").write_bytes(UNDECODABLE)
        _content, reason = gate.load_text("payload.dat")
        assert reason is not None
        assert "UTF-8" in reason

    def test_oversize_is_a_violation(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        (tmp_path / "huge.txt").write_bytes(b"a" * OVERSIZE)
        _content, reason = gate.load_text("huge.txt")
        assert reason is not None
        assert "KiB" in reason

    def test_missing_file_is_a_violation(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _content, reason = gate.load_text("never-written.md")
        assert reason is not None

    def test_unknown_extension_is_read_not_skipped(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """An extension the gate has never seen is scanned, not waved through."""
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "artefact.weirdext", f"ID: {SAMPLE_APP_ID}\n")
        content, reason = gate.load_text("artefact.weirdext")
        assert reason is None
        assert content is not None
        assert gate.check_airtable_ids("artefact.weirdext", content) is not None

    def test_svg_is_read(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """SVG is text, and was silently exempt under the old extension list."""
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "figure.svg", f"<svg><desc>{marker_text()}</desc></svg>")
        content, reason = gate.load_text("figure.svg")
        assert reason is None
        assert content is not None
        assert gate.check_content(content) is not None


class TestBinaryAllowlist:
    """The deliberate exemption that keeps the fail-closed rule liveable."""

    def test_allowlisted_binary_is_exempt(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        (tmp_path / "diagram.png").write_bytes(UNDECODABLE)
        content, reason = gate.load_text("diagram.png")
        assert reason is None
        assert content is None  # exempt, and deliberately not scanned

    def test_allowlisted_binary_over_size_limit_is_exempt(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        (tmp_path / "big.png").write_bytes(b"\xff" * OVERSIZE)
        _content, reason = gate.load_text("big.png")
        assert reason is None

    def test_exemption_is_by_type_not_by_name(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Renaming an unreadable file to look image-ish must not get it through."""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "png.dat").write_bytes(UNDECODABLE)
        _content, reason = gate.load_text("png.dat")
        assert reason is not None


class TestGateMainExitCode:
    def test_main_exits_1_for_public_airtable_id(
        self,
        gate: ModuleType,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "notes.md", f"Base: {SAMPLE_APP_ID}\n")
        monkeypatch.setattr(gate, "get_changed_files", lambda _argv: ["notes.md"])
        assert gate.main([]) == 1
        captured = capsys.readouterr()
        assert "Airtable identifier leaked" in captured.out
        assert SAMPLE_APP_ID in captured.out

    def test_main_exits_1_for_unscannable_file(
        self,
        gate: ModuleType,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        monkeypatch.chdir(tmp_path)
        (tmp_path / "payload.dat").write_bytes(UNDECODABLE)
        monkeypatch.setattr(gate, "get_changed_files", lambda _argv: ["payload.dat"])
        assert gate.main([]) == 1
        assert "payload.dat" in capsys.readouterr().out

    def test_main_exits_0_when_clean(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "notes.md", "No secrets here.\n")
        monkeypatch.setattr(gate, "get_changed_files", lambda _argv: ["notes.md"])
        assert gate.main([]) == 0

    def test_success_reports_what_it_scanned(
        self,
        gate: ModuleType,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """A silent green cannot be told apart from a gate that scanned nothing."""
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "notes.md", "Clean.\n")
        (tmp_path / "diagram.png").write_bytes(UNDECODABLE)
        monkeypatch.setattr(gate, "get_changed_files", lambda _argv: ["notes.md", "diagram.png"])
        assert gate.main([]) == 0
        out = capsys.readouterr().out
        assert "1 file(s) scanned" in out
        assert "1 allowlisted binary" in out

    def test_main_exits_0_when_id_in_tmp(
        self, gate: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _write(tmp_path / "tmp" / "handoff.md", f"Base: {SAMPLE_APP_ID}\n")
        monkeypatch.setattr(gate, "get_changed_files", lambda _argv: ["tmp/handoff.md"])
        assert gate.main([]) == 0


# --- End-to-end: the CLI modes CI actually invokes ------------------------


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A throwaway git repository the gate can run inside."""
    subprocess.run([GIT, "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run([GIT, "config", "user.email", "t@example.com"], cwd=tmp_path, check=True)
    subprocess.run([GIT, "config", "user.name", "Test"], cwd=tmp_path, check=True)
    return tmp_path


def _stage(repo: Path, name: str, content: str) -> None:
    _write(repo / name, content)
    subprocess.run([GIT, "add", "--force", name], cwd=repo, check=True)


def _commit(repo: Path, message: str) -> None:
    subprocess.run([GIT, "commit", "-qm", message], cwd=repo, check=True)


def _run_gate(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GATE_PATH), *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )


class TestCliModes:
    def test_staged_mode_blocks(self, repo: Path) -> None:
        _stage(repo, "leak.md", marker_text())
        result = _run_gate(repo)
        assert result.returncode == 1
        assert "leak.md" in result.stdout

    def test_nothing_staged_passes(self, repo: Path) -> None:
        assert _run_gate(repo).returncode == 0

    def test_range_mode_blocks_violation_in_range(self, repo: Path) -> None:
        _stage(repo, "base.md", "clean\n")
        _commit(repo, "base")
        _stage(repo, "leak.md", marker_text())
        _commit(repo, "change")

        result = _run_gate(repo, "--range", "HEAD~1", "HEAD")
        assert result.returncode == 1
        assert "leak.md" in result.stdout

    def test_range_mode_ignores_files_outside_range(self, repo: Path) -> None:
        """A violation already on the base branch is not this change's problem."""
        _stage(repo, "leak.md", marker_text())
        _commit(repo, "pre-existing")
        _stage(repo, "clean.md", "fine\n")
        _commit(repo, "change")

        assert _run_gate(repo, "--range", "HEAD~1", "HEAD").returncode == 0

    def test_all_mode_scans_every_tracked_file(self, repo: Path) -> None:
        """The push and schedule path: no diff to lean on, so scan the lot."""
        _stage(repo, "leak.md", marker_text())
        _commit(repo, "committed")

        result = _run_gate(repo, "--all")
        assert result.returncode == 1
        assert "leak.md" in result.stdout

    def test_range_mode_rejects_bad_arguments(self, repo: Path) -> None:
        assert _run_gate(repo, "--range", "HEAD").returncode == 2
