"""Anthropic Claude API engine (Tier 1, optional) for topology variable extraction.

Requires the ``anthropic`` package and an ``ANTHROPIC_API_KEY`` environment variable.
Gracefully raises ``ImportError`` or ``EnvironmentError`` when unavailable.
"""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any

from si_protocols.marker_registry import SupportedLang
from si_protocols.topology.types import (
    TopologyLevel,
    Variable,
    VariableClassification,
    VariableKind,
)

if TYPE_CHECKING:
    import anthropic  # pyright: ignore[reportMissingImports]


_DEFAULT_MODEL = "claude-sonnet-4-20250514"

_SYSTEM_PROMPT = """\
You are a topology analysis engine. Given a text, extract claims/assertions and \
classify each along four axes (0.0-1.0 where higher = more suspicious):

1. falsifiability - 0.0 testable, 1.0 unfalsifiable
2. verifiability - 0.0 has checkable sources, 1.0 no checkable sources
3. domain_coherence - 0.0 stays in domain, 1.0 crosses domains improperly
4. logical_dependency - 0.0 load-bearing, 1.0 decorative/emotive

Return a JSON array of objects with fields:
- "text": the claim text
- "start": character offset start
- "end": character offset end
- "falsifiability": float 0-1
- "verifiability": float 0-1
- "domain_coherence": float 0-1
- "logical_dependency": float 0-1

Return ONLY the JSON array, no other text.\
"""


class AnthropicEngine:
    """Claude API engine for topology variable extraction.

    Satisfies the :class:`~si_protocols.topology.engine.AnalysisEngine` protocol.

    Parameters
    ----------
    model:
        Claude model ID. Defaults to ``claude-sonnet-4-20250514``.
    client:
        Pre-configured ``anthropic.Anthropic`` instance for testing.
        If ``None``, creates one from the ``ANTHROPIC_API_KEY`` env var.
    """

    def __init__(
        self,
        *,
        model: str = _DEFAULT_MODEL,
        client: anthropic.Anthropic | None = None,
    ) -> None:
        self._model = model

        if client is not None:
            self._client = client
            return

        try:
            import anthropic as _anthropic  # pyright: ignore[reportMissingImports]
        except ImportError:
            msg = (
                "The 'anthropic' package is required for AnthropicEngine. "
                "Install it with: uv pip install 'si-protocols[anthropic]'"
            )
            raise ImportError(msg) from None

        if not os.environ.get("ANTHROPIC_API_KEY"):
            msg = "ANTHROPIC_API_KEY environment variable is not set."
            raise EnvironmentError(msg)  # noqa: UP024

        self._client = _anthropic.Anthropic()

    @property
    def name(self) -> str:
        return "anthropic"

    def extract_variables(
        self,
        text: str,
        *,
        lang: SupportedLang = "en",
    ) -> list[Variable]:
        """Extract and classify variables via the Claude API."""
        lang_instruction = "Analyse the text in Japanese." if lang == "ja" else ""
        user_msg = f"{lang_instruction}\n\nText to analyse:\n\n{text}".strip()

        response = self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )

        raw_text = response.content[0].text  # type: ignore[union-attr]
        return self._parse_response(raw_text, text)

    def _parse_response(self, raw: str, source_text: str) -> list[Variable]:
        """Parse the JSON array returned by Claude into Variable instances."""
        # Strip markdown code fences if present
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = lines[1:]  # Remove opening fence
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines)

        items: list[dict[str, Any]] = json.loads(cleaned)
        variables: list[Variable] = []

        for i, item in enumerate(items):
            classification = VariableClassification(
                falsifiability=max(0.0, min(1.0, float(item.get("falsifiability", 0.5)))),
                verifiability=max(0.0, min(1.0, float(item.get("verifiability", 0.5)))),
                domain_coherence=max(0.0, min(1.0, float(item.get("domain_coherence", 0.0)))),
                logical_dependency=max(0.0, min(1.0, float(item.get("logical_dependency", 0.5)))),
            )

            mean = (
                classification.falsifiability
                + classification.verifiability
                + classification.domain_coherence
                + classification.logical_dependency
            ) / 4

            if mean >= 0.5:
                kind = VariableKind.PSEUDO
            elif mean <= 0.3:
                kind = VariableKind.TRUE
            else:
                kind = VariableKind.INDETERMINATE

            variables.append(
                Variable(
                    id=f"v{i + 1}",
                    text=str(item.get("text", "")),
                    source_span=(int(item.get("start", 0)), int(item.get("end", 0))),
                    classification=classification,
                    kind=kind,
                    level=TopologyLevel.MICRO,
                    confidence=0.7,
                )
            )

        return variables
