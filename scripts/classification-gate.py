#!/usr/bin/env python3
"""SI Protocols — Classification Gate.

Prevents INTERNAL or CLASSIFIED content from reaching the public si-protocols
repository. Runs in two places, and the second is not optional: the pre-commit
hook can be bypassed with --no-verify, so CI re-runs the same gate on every
pull request. Integrate via the pre-commit framework (do NOT copy to
.git/hooks/, and never set core.hooksPath — it silently disables the whole
pre-commit chain).

Modes:
    (no arguments)        staged files — the pre-commit hook path
    --range BASE HEAD     files changed between two revisions — the CI path
    --all                 every tracked file — CI on push and on schedule

Usage with pre-commit framework (.pre-commit-config.yaml):
    - repo: local
      hooks:
        - id: classification-gate
          name: SI classification gate
          entry: python scripts/classification-gate.py
          language: python
          always_run: true
          pass_filenames: false

Fail-closed: a file the gate cannot read is a violation, not a pass. Binary
types the repo legitimately carries are exempted through an explicit
allowlist, so every exemption is visible in one place rather than implied by
a silent skip.

Exit codes:
    0 — all clear
    1 — classified content detected, or a file could not be scanned
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

# --- Configuration ---

# Classification markers (case-insensitive regex)
CLASSIFICATION_MARKERS: list[re.Pattern[str]] = [
    re.compile(r"CLASSIFICATION:\s*(INTERNAL|CLASSIFIED)", re.IGNORECASE),
    re.compile(r"分類:\s*(内部|機密)", re.IGNORECASE),  # Japanese equivalents
]

# Airtable identifier patterns — 3-char prefix + 14 alphanumerics.
# These belong in CLAUDE.local.md (gitignored) or R2, never the public repo.
AIRTABLE_ID_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bapp[A-Za-z0-9]{14}\b"),
    re.compile(r"\btbl[A-Za-z0-9]{14}\b"),
    re.compile(r"\brec[A-Za-z0-9]{14}\b"),
    re.compile(r"\bfld[A-Za-z0-9]{14}\b"),
]

# Directories exempted from the Airtable ID content check.
# tmp/ is gitignored; the others are blocked outright by SENSITIVE_DIR_PATTERNS
# but are listed here for defence-in-depth and documentation clarity.
AIRTABLE_ID_ALLOWLISTED_DIRS: tuple[str, ...] = (
    "tmp/",
    "local-only/",
    "classified/",
    ".secrets/",
)

# Filename patterns that should never appear in the public repo
SENSITIVE_FILENAME_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"audit[-_]report", re.IGNORECASE),
    re.compile(r"vulnerability[-_]analysis", re.IGNORECASE),
    re.compile(r"revenue[-_]model", re.IGNORECASE),
    re.compile(r"exposure[-_]scoring", re.IGNORECASE),
    re.compile(r"operational[-_]intel", re.IGNORECASE),
    re.compile(r"meeting[-_]notes", re.IGNORECASE),
]

# Directory patterns that should never be committed
SENSITIVE_DIR_PATTERNS: list[str] = [
    "local-only/",
    "classified/",
    ".secrets/",
]

# Binary file types this repo legitimately carries. Their content cannot be
# scanned for classification markers, so they are exempted EXPLICITLY here.
#
# This list is the only way past the gate without being read. It replaced an
# extension allowlist that decided what to *scan*: everything outside that list
# — .svg, .sh, uv.lock, LICENSE, .gitignore — passed silently unexamined, which
# is the failure mode this gate exists to prevent. Anything that decodes as
# UTF-8 is now scanned regardless of extension; anything that does not must
# appear below or it is a violation.
BINARY_ALLOWLIST: frozenset[str] = frozenset(
    {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".ico",
    }
)

# Maximum file size to read (bytes). Larger files are a violation unless their
# type is allowlisted above — the pre-commit chain independently caps added
# files at 1000 KiB, so a text file above this is already anomalous.
MAX_SCAN_SIZE: int = 1_048_576  # 1 MiB


GIT = shutil.which("git") or "git"


def _git(*args: str) -> list[str]:
    """Run a git command and return its non-empty output lines."""
    # S603: arguments are passed as an argv list with no shell, so there is no
    # command-injection surface. The only externally supplied values are the
    # two revisions in --range mode, and _require_revision rejects anything
    # option-shaped before it reaches here.
    result = subprocess.run(  # noqa: S603
        [GIT, *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _require_revision(value: str) -> str:
    """Reject revisions that git would read as options.

    A leading dash turns a revision argument into an option — the argv-list
    call above stops shell injection, but not git's own argument parsing.
    """
    if not value or value.startswith("-"):
        print(f"refusing option-shaped revision: {value!r}", file=sys.stderr)
        raise SystemExit(2)
    return value


def get_changed_files(argv: list[str]) -> list[str]:
    """Return the file paths this invocation should check.

    Three modes, so the same gate covers both the pre-commit hook and CI:
    staged files by default, a revision range with ``--range BASE HEAD``, or
    every tracked file with ``--all``.
    """
    if argv and argv[0] == "--all":
        return _git("ls-files")

    if argv and argv[0] == "--range":
        if len(argv) != 3:
            print("usage: classification-gate.py --range BASE HEAD", file=sys.stderr)
            raise SystemExit(2)
        base = _require_revision(argv[1])
        head = _require_revision(argv[2])
        # Three-dot: changes on HEAD since it diverged from BASE, so unrelated
        # commits already on the base branch are not attributed to this change.
        return _git("diff", "--name-only", "--diff-filter=ACM", f"{base}...{head}")

    return _git("diff", "--cached", "--name-only", "--diff-filter=ACM")


def check_filename(filepath: str) -> str | None:
    """Check if filename matches a sensitive pattern."""
    name = Path(filepath).name
    for pattern in SENSITIVE_FILENAME_PATTERNS:
        if pattern.search(name):
            return f"Sensitive filename pattern: {pattern.pattern}"
    return None


def check_directory(filepath: str) -> str | None:
    """Check if file is in a sensitive directory."""
    for dir_pattern in SENSITIVE_DIR_PATTERNS:
        if dir_pattern in filepath:
            return f"Sensitive directory: {dir_pattern}"
    return None


def load_text(filepath: str) -> tuple[str | None, str | None]:
    """Read a file as UTF-8 text, or explain why it cannot be scanned.

    Returns ``(text, None)`` when the file was read, ``(None, None)`` when it is
    an allowlisted binary type and deliberately not scanned, and
    ``(None, reason)`` when it cannot be scanned and no exemption applies.

    That last case is the point of this function. A gate that silently skips
    what it cannot parse gives no protection against precisely the file someone
    would use to smuggle content past it.
    """
    path = Path(filepath)
    exempt = path.suffix.lower() in BINARY_ALLOWLIST

    if not path.exists():
        if exempt:
            return None, None
        return None, "Listed as changed but absent from the working tree; cannot be scanned"

    if path.stat().st_size > MAX_SCAN_SIZE:
        if exempt:
            return None, None
        limit_kib = MAX_SCAN_SIZE // 1024
        return None, f"Larger than {limit_kib} KiB and not an allowlisted binary type"

    try:
        return path.read_text(encoding="utf-8"), None
    except (UnicodeDecodeError, OSError):
        if exempt:
            return None, None
        return None, "Not decodable as UTF-8 and not an allowlisted binary type"


def check_content(content: str) -> str | None:
    """Scan file content for classification markers."""
    for marker in CLASSIFICATION_MARKERS:
        match = marker.search(content)
        if match:
            return f"Classification marker found: {match.group(0)}"

    return None


def check_airtable_ids(filepath: str, content: str) -> str | None:
    """Scan for Airtable identifier leakage in public-path files."""
    for allowed in AIRTABLE_ID_ALLOWLISTED_DIRS:
        if filepath.startswith(allowed):
            return None

    for pattern in AIRTABLE_ID_PATTERNS:
        match = pattern.search(content)
        if match:
            return f"Airtable identifier leaked: {match.group(0)}"

    return None


def main(argv: list[str] | None = None) -> int:
    """Run the classification gate. Returns 0 if clear, 1 if blocked."""
    changed = get_changed_files(list(sys.argv[1:] if argv is None else argv))

    if not changed:
        return 0

    violations: list[tuple[str, str]] = []

    for filepath in changed:
        # Check filename
        reason = check_filename(filepath)
        if reason:
            violations.append((filepath, reason))
            continue

        # Check directory
        reason = check_directory(filepath)
        if reason:
            violations.append((filepath, reason))
            continue

        # Read once, then run both content checks over the same text.
        content, reason = load_text(filepath)
        if reason:
            violations.append((filepath, reason))
            continue
        if content is None:
            continue  # allowlisted binary type, deliberately not scanned

        # Check content for classification markers
        reason = check_content(content)
        if reason:
            violations.append((filepath, reason))
            continue

        # Check for Airtable identifier leakage (scoped to public paths)
        reason = check_airtable_ids(filepath, content)
        if reason:
            violations.append((filepath, reason))

    if violations:
        print("\n" + "=" * 60)
        print("  SI PROTOCOLS — CLASSIFICATION GATE BLOCKED")
        print("=" * 60)
        print()
        print("  The following files violate the classification policy.")
        print("  This is a PUBLIC repository: every pushed branch is")
        print("  world-readable the moment it lands.")
        print()

        for filepath, reason in violations:
            print(f"  ✗ {filepath}")
            print(f"    → {reason}")
            print()

        print("  Action required:")
        print("    1. Remove the file(s) from staging:  git reset HEAD <file>")
        print("    2. Upload to R2 instead:  wrangler r2 object put si-classified/...")
        print("    3. Or reclassify as OPEN if appropriate")
        print()
        print("  If a file was blocked because it could not be scanned, do not")
        print("  work around it by renaming: either make it scannable, or add")
        print("  its type to BINARY_ALLOWLIST so the exemption is reviewable.")
        print()
        print("=" * 60 + "\n")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
