"""Analysis engine protocol for topology variable extraction.

Any engine that can extract and classify variables from text should implement
the :class:`AnalysisEngine` protocol.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from si_protocols.marker_registry import SupportedLang
from si_protocols.topology.types import Variable


@runtime_checkable
class AnalysisEngine(Protocol):
    """Minimal contract for a topology analysis engine.

    Implementations must provide a ``name`` property and an
    ``extract_variables`` method that performs both extraction and
    classification in a single call.
    """

    @property
    def name(self) -> str: ...

    def extract_variables(
        self,
        text: str,
        *,
        lang: SupportedLang = "en",
    ) -> list[Variable]: ...
