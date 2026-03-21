"""Validation tests for the A/B evaluation corpus files."""

from __future__ import annotations

import json
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
MANIFEST_PATH = EXAMPLES_DIR / "corpus_manifest.json"

EXPECTED_FILES = [
    "corpus_en_benign_01.txt",
    "corpus_en_benign_02.txt",
    "corpus_en_benign_03.txt",
    "corpus_en_low_01.txt",
    "corpus_en_low_02.txt",
    "corpus_en_mid_01.txt",
    "corpus_en_mid_02.txt",
    "corpus_en_high_01.txt",
    "corpus_en_high_02.txt",
    "corpus_en_high_03.txt",
    "corpus_en_extreme_01.txt",
    "corpus_en_extreme_02.txt",
    "corpus_ja_benign_01.txt",
    "corpus_ja_benign_02.txt",
    "corpus_ja_benign_03.txt",
    "corpus_ja_low_01.txt",
    "corpus_ja_low_02.txt",
    "corpus_ja_mid_01.txt",
    "corpus_ja_mid_02.txt",
    "corpus_ja_high_01.txt",
    "corpus_ja_high_02.txt",
    "corpus_ja_high_03.txt",
    "corpus_ja_extreme_01.txt",
    "corpus_ja_extreme_02.txt",
]


def test_all_corpus_files_exist_and_nonempty() -> None:
    """All 24 corpus .txt files must exist and contain text."""
    for filename in EXPECTED_FILES:
        path = EXAMPLES_DIR / filename
        assert path.is_file(), f"Missing corpus file: {filename}"
        content = path.read_text(encoding="utf-8")
        assert len(content.strip()) > 0, f"Corpus file is empty: {filename}"


def test_manifest_valid_json_with_24_entries() -> None:
    """corpus_manifest.json must be valid JSON with exactly 24 sample entries."""
    assert MANIFEST_PATH.is_file(), "corpus_manifest.json not found"
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert "samples" in data, "Manifest missing 'samples' key"
    assert len(data["samples"]) == 24, f"Expected 24 samples, got {len(data['samples'])}"
    assert data["total_samples"] == 24


def test_manifest_files_exist_on_disk() -> None:
    """Every filename referenced in the manifest must exist in examples/."""
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for entry in data["samples"]:
        filename = entry["filename"]
        path = EXAMPLES_DIR / filename
        assert path.is_file(), f"Manifest references missing file: {filename}"


def test_ja_files_have_cjk_characters() -> None:
    """Japanese corpus files must contain >30% CJK characters."""
    for filename in EXPECTED_FILES:
        if not filename.startswith("corpus_ja_"):
            continue
        path = EXAMPLES_DIR / filename
        text = path.read_text(encoding="utf-8")
        # Count CJK Unified Ideographs, Hiragana, and Katakana
        cjk_count = sum(
            1
            for ch in text
            if (
                "\u3040" <= ch <= "\u309f"  # Hiragana
                or "\u30a0" <= ch <= "\u30ff"  # Katakana
                or "\u4e00" <= ch <= "\u9fff"  # CJK Unified Ideographs
                or "\uff00" <= ch <= "\uffef"  # Fullwidth Forms
            )
        )
        total = len(text.replace(" ", "").replace("\n", ""))
        ratio = cjk_count / max(total, 1)
        assert ratio > 0.3, f"{filename}: CJK ratio {ratio:.2%} is below 30% threshold"


def test_no_file_exceeds_max_characters() -> None:
    """No corpus file should exceed 3000 characters (sanity check)."""
    for filename in EXPECTED_FILES:
        path = EXAMPLES_DIR / filename
        content = path.read_text(encoding="utf-8")
        assert len(content) <= 3000, f"{filename}: {len(content)} chars exceeds 3000 limit"
