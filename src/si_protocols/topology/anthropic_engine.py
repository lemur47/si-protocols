"""Anthropic Claude API engine (Tier 1, optional) for topology variable extraction.

Requires the ``anthropic`` package and an ``ANTHROPIC_API_KEY`` environment variable.
Gracefully raises ``ImportError`` or ``EnvironmentError`` when unavailable.
"""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any

from si_protocols.marker_registry import SupportedLang
from si_protocols.topology.classification import derive_kind
from si_protocols.topology.types import (
    TopologyLevel,
    Variable,
    VariableClassification,
)

if TYPE_CHECKING:
    import anthropic  # pyright: ignore[reportMissingImports]
    from anthropic.types import (  # pyright: ignore[reportMissingImports]
        OutputConfigParam,
    )


_DEFAULT_MODEL = "claude-opus-5"


def _text_block(content: list[Any]) -> str:
    """Return the text of the first ``text`` block in a response.

    Thinking is on by default on this model and ``display`` defaults to
    ``"omitted"``, so a response normally opens with an empty thinking block.
    Indexing ``content[0]`` therefore reads the wrong block.
    """
    for block in content:
        if getattr(block, "type", None) == "text":
            return str(block.text)
    msg = "Claude returned no text block to parse."
    raise ValueError(msg)


# Extraction is mechanical, so the default `high` overspends on thinking.
_EFFORT = "low"

# Thinking and response share this budget; sized for a long claim array.
# Above roughly this figure the request would need streaming to dodge the
# SDK's HTTP timeout, which this engine does not use.
_MAX_TOKENS = 16000

_AXES = ("falsifiability", "verifiability", "domain_coherence", "logical_dependency")

# The schema guarantees a parseable response, so no markdown fence has to be
# stripped. Deliberately carries no `minimum`/`maximum` on the axes: numeric
# constraints are unsupported, and `_parse_response` clamps to 0-1 anyway.
_OUTPUT_CONFIG: OutputConfigParam = {
    "effort": _EFFORT,
    "format": {
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "claims": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "start": {"type": "integer"},
                            "end": {"type": "integer"},
                            **{axis: {"type": "number"} for axis in _AXES},
                        },
                        "required": ["text", "start", "end", *_AXES],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["claims"],
            "additionalProperties": False,
        },
    },
}

_SYSTEM_PROMPT = """\
You are a topology analysis engine. Given a text, extract claims/assertions and \
classify each along four axes (0.0-1.0 where higher = more suspicious):

1. falsifiability - 0.0 testable, 1.0 unfalsifiable
2. verifiability - 0.0 has checkable sources, 1.0 no checkable sources
3. domain_coherence - 0.0 stays in domain, 1.0 crosses domains improperly
4. logical_dependency - 0.0 load-bearing, 1.0 decorative/emotive

Return a JSON object with a "claims" array. Each claim has fields:
- "text": the claim text
- "start": character offset start
- "end": character offset end
- "falsifiability": float 0-1
- "verifiability": float 0-1
- "domain_coherence": float 0-1
- "logical_dependency": float 0-1\
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
            # Caps thinking AND response together on this generation, and
            # thinking is on by default — 4096 truncated long claim arrays.
            max_tokens=_MAX_TOKENS,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
            output_config=_OUTPUT_CONFIG,
        )

        stop_reason = getattr(response, "stop_reason", None)
        if stop_reason == "max_tokens":
            msg = (
                "Claude truncated the response at max_tokens; the claim array is "
                "incomplete. Raise max_tokens or lower output_config.effort."
            )
            raise ValueError(msg)
        if stop_reason == "refusal":
            msg = "Claude refused to analyse this text (stop_reason='refusal')."
            raise ValueError(msg)

        return self._parse_response(_text_block(response.content), text)

    def _parse_response(self, raw: str, source_text: str) -> list[Variable]:
        """Parse the JSON object returned by Claude into Variable instances.

        The response shape is guaranteed by ``output_config.format``, so there
        is no markdown fence to strip.
        """
        payload: dict[str, Any] = json.loads(raw)
        items: list[dict[str, Any]] = payload["claims"]
        variables: list[Variable] = []

        for i, item in enumerate(items):
            classification = VariableClassification(
                falsifiability=max(0.0, min(1.0, float(item.get("falsifiability", 0.5)))),
                verifiability=max(0.0, min(1.0, float(item.get("verifiability", 0.5)))),
                domain_coherence=max(0.0, min(1.0, float(item.get("domain_coherence", 0.0)))),
                logical_dependency=max(0.0, min(1.0, float(item.get("logical_dependency", 0.5)))),
            )

            variables.append(
                Variable(
                    id=f"v{i + 1}",
                    text=str(item.get("text", "")),
                    source_span=(int(item.get("start", 0)), int(item.get("end", 0))),
                    classification=classification,
                    kind=derive_kind(classification),
                    level=TopologyLevel.MICRO,
                    confidence=0.7,
                )
            )

        return variables
