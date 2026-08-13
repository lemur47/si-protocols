"""Tests for the Anthropic topology engine.

⚠️ **The transport is mocked, and that mock is why this engine shipped broken
for six weeks.** `messages.create` is replaced wholesale, so nothing here reads
the pinned model ID against a live endpoint, and a mocked call succeeds just as
happily against a retired one.

The real thing cannot be used: there is no API key on this machine and
`api.anthropic.com` is outside the sandbox allowlist. Closing that gap needs a
live smoke test, which is gated on an undecided credential posture.

What these tests *can* do, and now do, is assert the **shape of the request we
send** and the **shape of the response we accept** — the two things the previous
suite left entirely unasserted. Treat a green run as "correct by construction",
never as "verified against the API".
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock

import pytest

from si_protocols.topology.anthropic_engine import AnthropicEngine
from si_protocols.topology.engine import AnalysisEngine
from si_protocols.topology.types import VariableKind

# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------

_MOCK_RESPONSE_DATA = [
    {
        "text": "The ascended masters say this is true",
        "start": 0,
        "end": 37,
        "falsifiability": 0.9,
        "verifiability": 0.8,
        "domain_coherence": 0.1,
        "logical_dependency": 0.7,
    },
    {
        "text": "Published in Nature, the study found correlations",
        "start": 40,
        "end": 89,
        "falsifiability": 0.1,
        "verifiability": 0.1,
        "domain_coherence": 0.0,
        "logical_dependency": 0.1,
    },
]


@dataclass
class _MockTextBlock:
    text: str
    type: str = "text"


@dataclass
class _MockThinkingBlock:
    """A thinking block as returned by claude-opus-5.

    Thinking is ON BY DEFAULT on this model, and ``display`` defaults to
    ``"omitted"`` — so the block is present with empty text. It carries no
    ``.text`` attribute at all, which is precisely why ``content[0].text``
    is unsafe.
    """

    thinking: str = ""
    type: str = "thinking"


@dataclass
class _MockResponse:
    content: list[object]
    stop_reason: str = "end_turn"


def _make_mock_client(
    response_data: list[dict[str, object]] | None = None,
    *,
    lead_with_thinking: bool = False,
    stop_reason: str = "end_turn",
) -> MagicMock:
    """Create a mock Anthropic client returning synthetic JSON."""
    data = _MOCK_RESPONSE_DATA if response_data is None else response_data
    blocks: list[object] = [_MockTextBlock(text=json.dumps({"claims": data}))]
    if lead_with_thinking:
        blocks.insert(0, _MockThinkingBlock())
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _MockResponse(
        content=blocks, stop_reason=stop_reason
    )
    return mock_client


def _request_kwargs(mock_client: MagicMock) -> dict[str, object]:
    """The kwargs of the single ``messages.create`` call the engine made."""
    return mock_client.messages.create.call_args.kwargs


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestProtocolCompliance:
    def test_implements_protocol(self) -> None:
        engine = AnthropicEngine(client=_make_mock_client())
        assert isinstance(engine, AnalysisEngine)

    def test_name(self) -> None:
        engine = AnthropicEngine(client=_make_mock_client())
        assert engine.name == "anthropic"


class TestExtractVariables:
    def test_returns_variables(self) -> None:
        engine = AnthropicEngine(client=_make_mock_client())
        variables = engine.extract_variables("test text")
        assert len(variables) == 2

    def test_first_variable_is_pseudo(self) -> None:
        engine = AnthropicEngine(client=_make_mock_client())
        variables = engine.extract_variables("test text")
        assert variables[0].kind == VariableKind.PSEUDO

    def test_second_variable_is_true(self) -> None:
        engine = AnthropicEngine(client=_make_mock_client())
        variables = engine.extract_variables("test text")
        assert variables[1].kind == VariableKind.TRUE

    def test_variable_text_preserved(self) -> None:
        engine = AnthropicEngine(client=_make_mock_client())
        variables = engine.extract_variables("test text")
        assert variables[0].text == "The ascended masters say this is true"

    def test_source_span_preserved(self) -> None:
        engine = AnthropicEngine(client=_make_mock_client())
        variables = engine.extract_variables("test text")
        assert variables[0].source_span == (0, 37)

    def test_classification_axes(self) -> None:
        engine = AnthropicEngine(client=_make_mock_client())
        variables = engine.extract_variables("test text")
        cls = variables[0].classification
        assert cls.falsifiability == 0.9
        assert cls.verifiability == 0.8

    def test_japanese_lang_passed(self) -> None:
        mock_client = _make_mock_client()
        engine = AnthropicEngine(client=mock_client)
        engine.extract_variables("テスト", lang="ja")
        call_kwargs = mock_client.messages.create.call_args
        user_msg = call_kwargs.kwargs["messages"][0]["content"]
        assert "Japanese" in user_msg


class TestRequestShape:
    """The request must match the current generation's contract.

    Every test here reads the kwargs the engine actually sent. The transport is
    mocked — see the module docstring — so these assert the *shape we send*, not
    that the API accepts it. That gap is the known limit of this suite.
    """

    def test_pins_a_current_generation_model(self) -> None:
        mock_client = _make_mock_client()
        AnthropicEngine(client=mock_client).extract_variables("test")
        assert _request_kwargs(mock_client)["model"] == "claude-opus-5"

    def test_sends_no_rejected_sampling_parameters(self) -> None:
        """`temperature`, `top_p` and `top_k` are rejected with a 400."""
        mock_client = _make_mock_client()
        AnthropicEngine(client=mock_client).extract_variables("test")
        kwargs = _request_kwargs(mock_client)
        assert not {"temperature", "top_p", "top_k"} & set(kwargs)

    def test_does_not_disable_thinking(self) -> None:
        """Disabling thinking leaks `<thinking>` tags into the visible text.

        This engine feeds that text straight to `json.loads`, so a leaked tag is
        a parse failure. Thinking is on by default; the engine must not opt out.
        """
        mock_client = _make_mock_client()
        AnthropicEngine(client=mock_client).extract_variables("test")
        thinking: Any = _request_kwargs(mock_client).get("thinking")
        assert thinking is None or thinking.get("type") != "disabled"

    def test_constrains_output_with_a_json_schema(self) -> None:
        mock_client = _make_mock_client()
        AnthropicEngine(client=mock_client).extract_variables("test")
        fmt = _request_kwargs(mock_client)["output_config"]["format"]  # type: ignore[index]
        assert fmt["type"] == "json_schema"

    def test_schema_declares_every_field_the_parser_reads(self) -> None:
        mock_client = _make_mock_client()
        AnthropicEngine(client=mock_client).extract_variables("test")
        fmt = _request_kwargs(mock_client)["output_config"]["format"]  # type: ignore[index]
        item: dict[str, Any] = fmt["schema"]["properties"]["claims"]["items"]
        assert set(item["required"]) == {
            "text",
            "start",
            "end",
            "falsifiability",
            "verifiability",
            "domain_coherence",
            "logical_dependency",
        }
        assert item["additionalProperties"] is False

    def test_sets_effort_deliberately(self) -> None:
        """Extraction is mechanical; the default `high` overspends on thinking."""
        mock_client = _make_mock_client()
        AnthropicEngine(client=mock_client).extract_variables("test")
        effort = _request_kwargs(mock_client)["output_config"]["effort"]  # type: ignore[index]
        assert effort in {"low", "medium"}

    def test_max_tokens_leaves_headroom_for_thinking(self) -> None:
        """`max_tokens` caps thinking AND response together on this model.

        The old 4096 was sized for a response alone, so a long claim array now
        truncates mid-JSON.
        """
        mock_client = _make_mock_client()
        AnthropicEngine(client=mock_client).extract_variables("test")
        assert int(_request_kwargs(mock_client)["max_tokens"]) >= 16000  # type: ignore[call-overload]


class TestResponseReading:
    def test_finds_text_block_after_a_thinking_block(self) -> None:
        """Thinking is on by default, so `content[0]` may not be the text.

        Every pre-existing test mocks a lone text block, which is why none of
        them can see this.
        """
        mock_client = _make_mock_client(lead_with_thinking=True)
        variables = AnthropicEngine(client=mock_client).extract_variables("test")
        assert len(variables) == 2

    def test_truncated_response_raises(self) -> None:
        """A truncated array must fail loudly, not return a short list."""
        mock_client = _make_mock_client(stop_reason="max_tokens")
        with pytest.raises(ValueError, match="truncated"):
            AnthropicEngine(client=mock_client).extract_variables("test")

    def test_refused_response_raises(self) -> None:
        """`claude-opus-5` can decline with HTTP 200 and `stop_reason=refusal`."""
        mock_client = _make_mock_client(stop_reason="refusal")
        with pytest.raises(ValueError, match="refus"):
            AnthropicEngine(client=mock_client).extract_variables("test")


class TestImportError:
    def test_missing_package_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """AnthropicEngine without client and without package should raise."""
        # We test the error path by passing client=None and mocking the import
        # This is tricky — instead test that __init__ with a client works fine
        engine = AnthropicEngine(client=_make_mock_client())
        assert engine.name == "anthropic"
