#!/usr/bin/env python3
"""SI Protocols — Airtable ID leak guard.

Stops Airtable record/table/field IDs leaking into *public artefacts*:
commit messages, PR titles/bodies, and issue bodies. These IDs are
operator-local intelligence — they belong in CLAUDE-internal.md (gitignored)
or R2, never on the public repo.

Companion to ``scripts/classification-gate.py``, which scans staged FILE
content on the pre-commit stage. That gate cannot see the commit *message*,
nor the payload of a ``gh pr``/``gh issue`` command issued by the agent.
This script covers exactly those vectors, in two modes:

commit-msg mode (pre-commit ``commit-msg`` stage)::

    python scripts/check-airtable-ids.py <commit-msg-file>

  Reads the message file, drops git comment lines (which never reach the
  committed message), and scans the body. Exit 1 on match (blocks the
  commit), 0 otherwise.

PreToolUse hook mode (Claude Code, ``--hook``)::

    python3 scripts/check-airtable-ids.py --hook   # JSON payload on stdin

  For ``git commit`` / ``gh pr`` / ``gh issue`` commands, scans the command
  string plus any file referenced by ``-F``/``--file``/``--body-file``.
  Emits a ``hookSpecificOutput`` "deny" decision on match. Always exits 0 —
  the block is carried by the JSON decision, per the Claude Code hook spec.

Exit codes (commit-msg mode):
    0 — clear, commit proceeds
    1 — Airtable ID detected, commit blocked
"""

from __future__ import annotations

import json
import re
import shlex
import sys
from pathlib import Path

# Airtable identifier patterns — 3-char prefix + 14 alphanumerics.
# Mirrors scripts/classification-gate.py (the patterns are already public there).
AIRTABLE_ID_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bapp[A-Za-z0-9]{14}\b"),
    re.compile(r"\btbl[A-Za-z0-9]{14}\b"),
    re.compile(r"\brec[A-Za-z0-9]{14}\b"),
    re.compile(r"\bfld[A-Za-z0-9]{14}\b"),
)

# Command families whose payloads land in public artefacts and are worth scanning.
_GUARDED_COMMANDS: tuple[tuple[str, ...], ...] = (
    ("git", "commit"),
    ("gh", "pr"),
    ("gh", "issue"),
)

# Flags whose value is a path to a file whose contents should also be scanned
# (e.g. ``gh pr create --body-file body.md``, ``git commit -F msg.txt``).
_FILE_VALUE_FLAGS: tuple[str, ...] = ("-F", "--file", "--body-file")


def find_airtable_id(text: str) -> str | None:
    """Return the first Airtable ID found in *text*, or None."""
    for pattern in AIRTABLE_ID_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0)
    return None


def _strip_comment_lines(message: str) -> str:
    """Drop git comment lines (those beginning with '#').

    Git's default 'strip' cleanup removes these before the message is
    committed, so scanning them would only produce false positives (e.g. on
    the commented diff of a ``commit --verbose`` template).
    """
    return "\n".join(line for line in message.splitlines() if not line.startswith("#"))


def _contains_guarded_command(tokens: list[str]) -> bool:
    """True if a guarded invocation (git commit / gh pr / gh issue) appears
    anywhere in the token stream — also catches compound commands such as
    ``cd site && git commit -m ...``."""
    for prefix in _GUARDED_COMMANDS:
        width = len(prefix)
        for i in range(len(tokens) - width + 1):
            if tuple(tokens[i : i + width]) == prefix:
                return True
    return False


def _referenced_files(tokens: list[str]) -> list[str]:
    """Paths named by ``-F``/``--file``/``--body-file`` (both ``flag value``
    and ``flag=value`` forms)."""
    files: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in _FILE_VALUE_FLAGS:
            if index + 1 < len(tokens):
                files.append(tokens[index + 1])
            index += 2
            continue
        for flag in _FILE_VALUE_FLAGS:
            if token.startswith(f"{flag}="):
                files.append(token[len(flag) + 1 :])
                break
        index += 1
    return files


def _emit_deny(found: str) -> None:
    """Print the PreToolUse 'deny' decision (structured form, exit 0)."""
    reason = (
        f"Airtable ID '{found}' detected in a git/gh command. Record/table/field "
        "IDs must not leak into commit messages, PR titles/bodies, or issue bodies — "
        "they are operator-local (CLAUDE-internal.md / R2). Remove the ID and retry."
    )
    decision = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(decision))


def _print_commit_block(found: str) -> None:
    """Human-facing block message for the commit-msg stage (to stderr)."""
    lines = (
        "",
        "=" * 60,
        "  SI PROTOCOLS — AIRTABLE ID GUARD BLOCKED COMMIT",
        "=" * 60,
        "",
        f"  Airtable ID leaked into the commit message: {found}",
        "",
        "  Record/table/field IDs are operator-local intelligence. They",
        "  belong in CLAUDE-internal.md (gitignored) or R2 — never in a",
        "  public commit message, PR title/body, or issue body.",
        "",
        "  Action: remove the ID from your commit message and retry.",
        "",
        "=" * 60,
        "",
    )
    print("\n".join(lines), file=sys.stderr)


def _run_hook() -> int:
    """PreToolUse mode: read JSON from stdin, deny guarded commands carrying IDs."""
    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        return 0  # Malformed payload — let the normal permission flow proceed.

    if payload.get("tool_name") != "Bash":
        return 0

    command = (payload.get("tool_input") or {}).get("command", "")
    if not command:
        return 0

    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()

    if not _contains_guarded_command(tokens):
        return 0

    haystack = command
    for path in _referenced_files(tokens):
        try:
            haystack += "\n" + Path(path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # Unreadable referenced file — scan what we have.

    found = find_airtable_id(haystack)
    if found is not None:
        _emit_deny(found)
    return 0


def _scan_commit_msg(path: str) -> int:
    """commit-msg mode: scan the message file, exit 1 on match."""
    try:
        message = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        # The guard fails open on an unreadable message file (git itself would
        # have failed first) — but says so rather than dying silently.
        print(f"airtable-id-guard: could not read {path!r}: {exc}", file=sys.stderr)
        return 0

    found = find_airtable_id(_strip_comment_lines(message))
    if found is None:
        return 0
    _print_commit_block(found)
    return 1


def main(argv: list[str]) -> int:
    if "--hook" in argv:
        return _run_hook()

    positional = [arg for arg in argv if not arg.startswith("-")]
    if not positional:
        print(
            "usage: check-airtable-ids.py <commit-msg-file> | --hook",
            file=sys.stderr,
        )
        return 0
    return _scan_commit_msg(positional[0])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
