#!/usr/bin/env python3
"""SI Protocols — Classification Gate (pre-commit hook).

Prevents INTERNAL or CLASSIFIED content from being committed
to the public si-protocols repository. Integrate with the
pre-commit framework (do NOT copy to .git/hooks/).

Usage with pre-commit framework (.pre-commit-config.yaml):
    - repo: local
      hooks:
        - id: classification-gate
          name: SI classification gate
          entry: python scripts/classification-gate.py
          language: python
          always_run: true
          pass_filenames: false

Exit codes:
    0 — all clear, commit proceeds
    1 — classified content detected, commit blocked
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# --- Configuration ---

# Classification markers (case-insensitive regex)
CLASSIFICATION_MARKERS: list[re.Pattern[str]] = [
    re.compile(r"CLASSIFICATION:\s*(INTERNAL|CLASSIFIED)", re.IGNORECASE),
    re.compile(r"分類:\s*(内部|機密)", re.IGNORECASE),  # Japanese equivalents
]

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

# File extensions to scan for classification markers
SCANNABLE_EXTENSIONS: set[str] = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".py",
    ".js",
    ".ts",
    ".html",
    ".astro",
    ".svelte",
}

# Maximum file size to scan (bytes) — skip large binaries
MAX_SCAN_SIZE: int = 1_048_576  # 1 MiB


def get_staged_files() -> list[str]:
    """Return list of staged file paths (added, modified, or copied)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],  # noqa: S607
        capture_output=True,
        text=True,
        check=True,
    )
    return [f.strip() for f in result.stdout.splitlines() if f.strip()]


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


def check_content(filepath: str) -> str | None:
    """Scan file content for classification markers."""
    path = Path(filepath)

    if path.suffix.lower() not in SCANNABLE_EXTENSIONS:
        return None

    if not path.exists():
        return None

    if path.stat().st_size > MAX_SCAN_SIZE:
        return None

    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None

    for marker in CLASSIFICATION_MARKERS:
        match = marker.search(content)
        if match:
            return f"Classification marker found: {match.group(0)}"

    return None


def main() -> int:
    """Run the classification gate. Returns 0 if clear, 1 if blocked."""
    staged = get_staged_files()

    if not staged:
        return 0

    violations: list[tuple[str, str]] = []

    for filepath in staged:
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

        # Check content
        reason = check_content(filepath)
        if reason:
            violations.append((filepath, reason))

    if violations:
        print("\n" + "=" * 60)
        print("  SI PROTOCOLS — CLASSIFICATION GATE BLOCKED COMMIT")
        print("=" * 60)
        print()
        print("  The following files violate the classification policy.")
        print("  This is a PUBLIC repository. All branches are visible")
        print("  and trigger Cloudflare Pages preview deployments.")
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
        print("=" * 60 + "\n")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
