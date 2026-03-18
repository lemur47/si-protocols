"""Tests for the Ollama engine stub — verifies protocol conformance and NotImplementedError."""

from __future__ import annotations

import pytest

from si_protocols.topology.engine import AnalysisEngine
from si_protocols.topology.ollama_engine import OllamaEngine


class TestOllamaEngine:
    """Verify the stub engine satisfies the AnalysisEngine protocol."""

    def test_conforms_to_analysis_engine_protocol(self) -> None:
        engine = OllamaEngine()
        assert isinstance(engine, AnalysisEngine)

    def test_name_property(self) -> None:
        engine = OllamaEngine()
        assert engine.name == "ollama"

    def test_extract_variables_raises_not_implemented(self) -> None:
        engine = OllamaEngine()
        with pytest.raises(NotImplementedError, match="stub for future local-LLM"):
            engine.extract_variables("Some text to analyse.")

    def test_extract_variables_raises_not_implemented_ja(self) -> None:
        engine = OllamaEngine()
        with pytest.raises(NotImplementedError, match="stub for future local-LLM"):
            engine.extract_variables("テスト用テキスト", lang="ja")
