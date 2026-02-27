"""Ollama engine stub (Tier 2, experimental).

This is an interface-only placeholder. The ``extract_variables`` method raises
``NotImplementedError`` with a clear message.
"""

from __future__ import annotations

from si_protocols.marker_registry import SupportedLang
from si_protocols.topology.types import Variable


class OllamaEngine:
    """Stub engine for future Ollama/local-LLM integration.

    Satisfies the :class:`~si_protocols.topology.engine.AnalysisEngine`
    protocol signature but is not yet functional.
    """

    @property
    def name(self) -> str:
        return "ollama"

    def extract_variables(
        self,
        text: str,
        *,
        lang: SupportedLang = "en",
    ) -> list[Variable]:
        """Not yet implemented — raises ``NotImplementedError``."""
        msg = (
            "OllamaEngine is a stub for future local-LLM integration. "
            "Use 'rule' or 'anthropic' engine instead."
        )
        raise NotImplementedError(msg)
