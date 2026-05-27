"""Tests for the Airtable ID leak guard (scripts/check-airtable-ids.py).

Both layers are exercised through the script's two CLI modes:
- commit-msg mode (Layer 2): message file argument, exit 1 on a leak.
- ``--hook`` mode (Layer 1): PreToolUse JSON on stdin, a "deny" decision on a leak.

Per the "describe, don't embed" rule for sensitive-shape patterns, no literal
17-character identifier ever appears in this source — fake IDs are assembled at
runtime from a 3-char prefix plus 14 filler characters. That keeps the test file
itself clean for both the classification gate and the guard under test.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-airtable-ids.py"

# The four Airtable identifier prefixes the guard must catch.
PREFIXES = ("app", "tbl", "rec", "fld")


def fake_id(prefix: str) -> str:
    """Assemble a syntactically valid Airtable ID without embedding a literal."""
    return prefix + ("0" * 14)


def run_commit_msg(message: str, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    """Invoke the guard in commit-msg mode against a message file."""
    msg_file = tmp_path / "COMMIT_EDITMSG"
    msg_file.write_text(message, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(msg_file)],
        capture_output=True,
        text=True,
        check=False,
    )


def run_hook(command: str) -> subprocess.CompletedProcess[str]:
    """Invoke the guard in PreToolUse hook mode with a Bash command payload."""
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--hook"],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )


def hook_denied(result: subprocess.CompletedProcess[str]) -> bool:
    """True if the hook emitted a structured 'deny' decision."""
    if not result.stdout.strip():
        return False
    decision = json.loads(result.stdout)
    return decision["hookSpecificOutput"]["permissionDecision"] == "deny"


# --- Layer 2: commit-msg stage ------------------------------------------------


@pytest.mark.parametrize("prefix", PREFIXES)
def test_commit_msg_blocks_each_prefix(prefix: str, tmp_path: Path) -> None:
    result = run_commit_msg(f"fix: tidy up\n\nrefs {fake_id(prefix)}\n", tmp_path)
    assert result.returncode == 1
    assert fake_id(prefix) in result.stderr


def test_commit_msg_allows_clean_message(tmp_path: Path) -> None:
    result = run_commit_msg("fix: tidy up the scanner\n\nNo identifiers here.\n", tmp_path)
    assert result.returncode == 0


def test_commit_msg_ignores_comment_lines(tmp_path: Path) -> None:
    # IDs on git comment lines are stripped before commit, so must not block.
    message = f"docs: update notes\n\n# refs {fake_id('rec')} (stripped by git)\n"
    result = run_commit_msg(message, tmp_path)
    assert result.returncode == 0


def test_commit_msg_no_false_positive_on_short_word(tmp_path: Path) -> None:
    # "reconciliation" is rec + 11 chars — not a 17-char ID.
    result = run_commit_msg("chore: reconciliation of the ledger\n", tmp_path)
    assert result.returncode == 0


# --- Layer 1: PreToolUse hook -------------------------------------------------


@pytest.mark.parametrize("prefix", PREFIXES)
def test_hook_blocks_git_commit_each_prefix(prefix: str) -> None:
    result = run_hook(f'git commit -m "fixes {fake_id(prefix)}"')
    assert hook_denied(result)
    assert fake_id(prefix) in result.stdout


def test_hook_allows_clean_git_commit() -> None:
    result = run_hook('git commit -m "fix: tidy up the scanner"')
    assert not hook_denied(result)


def test_hook_blocks_compound_command() -> None:
    result = run_hook(f'cd site && git commit -m "wip {fake_id("rec")}"')
    assert hook_denied(result)


def test_hook_blocks_gh_pr_and_gh_issue() -> None:
    assert hook_denied(run_hook(f'gh pr create --title "x" --body "see {fake_id("tbl")}"'))
    assert hook_denied(run_hook(f'gh issue create --body "{fake_id("app")}"'))


def test_hook_ignores_non_guarded_command_with_id() -> None:
    # An ID in an unrelated command (e.g. reading a tmp handoff) is not a leak.
    result = run_hook(f"cat tmp/handoff_{fake_id('rec')}.md")
    assert not hook_denied(result)


def test_hook_ignores_non_bash_tool() -> None:
    payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": fake_id("rec")}})
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--hook"],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )
    assert not hook_denied(result)


def test_hook_scans_referenced_body_file(tmp_path: Path) -> None:
    body = tmp_path / "body.md"
    body.write_text(f"PR description referencing {fake_id('fld')}\n", encoding="utf-8")
    result = run_hook(f'gh pr create --title "x" --body-file {body}')
    assert hook_denied(result)
