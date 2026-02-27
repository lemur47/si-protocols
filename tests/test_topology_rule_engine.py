"""Tests for the rule-based topology analysis engine."""

from __future__ import annotations

import pytest

from si_protocols.topology.engine import AnalysisEngine
from si_protocols.topology.rule_engine import RuleEngine, _classify_sentence, _is_claim
from si_protocols.topology.types import VariableKind

# ---------------------------------------------------------------------------
# Fixtures (module-level text constants)
# ---------------------------------------------------------------------------

BENIGN = (
    "Published in the Journal of Consciousness Studies (doi:10.1234/example), "
    "Dr. Sarah Chen at the University of Oxford found that mindfulness meditation "
    "reduces cortisol levels by 23% in a peer-reviewed double-blind trial."
)

SUSPICIOUS = (
    "The ascended masters say that only those who awaken to the divine frequency "
    "will transcend the matrix of illusion. The galactic federation confirms that "
    "a great shift is upon us. You must act now — the window is closing."
)

PSEUDO_HEAVY = (
    "Ancient wisdom teaches that the quantum field connects all living beings. "
    "Scientists say this has been proven many times. Experts agree that the "
    "source energy is real. Higher dimensions reveal the truth that leading "
    "researchers have always known but insiders reveal only now. "
    "The hidden cosmic divine frequency will transform your sacred vibration."
)

TRUE_HEAVY = (
    "Published in Nature (doi:10.1038/example), the University of Cambridge "
    "study found a statistically significant correlation. The peer-reviewed "
    "results were replicated in vol. 42 of the journal. Because the methodology "
    "was sound, therefore the conclusions are reliable."
)

MIXED = (
    "The peer-reviewed study in Nature showed promising results for meditation. "
    "However, ancient wisdom teaches that chakra alignment through quantum "
    "vibration activates your DNA. Scientists say this is proven."
)


# ---------------------------------------------------------------------------
# Protocol compliance
# ---------------------------------------------------------------------------


class TestProtocolCompliance:
    def test_implements_protocol(self) -> None:
        engine = RuleEngine()
        assert isinstance(engine, AnalysisEngine)

    def test_name(self) -> None:
        engine = RuleEngine()
        assert engine.name == "rule"


# ---------------------------------------------------------------------------
# Variable extraction
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestExtractVariables:
    def test_suspicious_text_extracts_variables(self) -> None:
        engine = RuleEngine()
        variables = engine.extract_variables(SUSPICIOUS)
        assert len(variables) > 0

    def test_benign_text_may_extract_fewer(self) -> None:
        engine = RuleEngine()
        suspicious_vars = engine.extract_variables(SUSPICIOUS)
        benign_vars = engine.extract_variables(BENIGN)
        assert len(suspicious_vars) >= len(benign_vars)

    def test_pseudo_heavy_text_produces_pseudo_variables(self) -> None:
        engine = RuleEngine()
        variables = engine.extract_variables(PSEUDO_HEAVY)
        pseudo_count = sum(1 for v in variables if v.kind == VariableKind.PSEUDO)
        assert pseudo_count >= 1

    def test_true_heavy_text_produces_true_variables(self) -> None:
        engine = RuleEngine()
        variables = engine.extract_variables(TRUE_HEAVY)
        true_count = sum(1 for v in variables if v.kind == VariableKind.TRUE)
        assert true_count >= 1

    def test_mixed_text_produces_both_kinds(self) -> None:
        engine = RuleEngine()
        variables = engine.extract_variables(MIXED)
        kinds = {v.kind for v in variables}
        assert len(kinds) >= 2, f"Expected >=2 kinds, got {kinds}"

    def test_variable_ids_unique(self) -> None:
        engine = RuleEngine()
        variables = engine.extract_variables(SUSPICIOUS)
        ids = [v.id for v in variables]
        assert len(ids) == len(set(ids))

    def test_variable_fields_populated(self) -> None:
        engine = RuleEngine()
        variables = engine.extract_variables(SUSPICIOUS)
        for v in variables:
            assert v.id.startswith("v")
            assert v.text
            assert v.source_span[0] >= 0
            assert v.classification is not None


# ---------------------------------------------------------------------------
# Classification axes
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestClassification:
    def test_unfalsifiable_raises_falsifiability(self) -> None:
        from si_protocols.marker_registry import get_markers

        markers = get_markers("en")
        text = "Ancient wisdom teaches that the quantum field reveals all truth."
        cls = _classify_sentence(text, markers, "en")
        assert cls.falsifiability > 0.0

    def test_verifiable_lowers_falsifiability(self) -> None:
        from si_protocols.marker_registry import get_markers

        markers = get_markers("en")
        text = "Published in the Journal of Physics (doi:10.1234), the result was confirmed."
        cls = _classify_sentence(text, markers, "en")
        assert cls.falsifiability <= 0.3

    def test_unnamed_authority_raises_verifiability(self) -> None:
        from si_protocols.marker_registry import get_markers

        markers = get_markers("en")
        text = "Scientists say and experts agree that this is true."
        cls = _classify_sentence(text, markers, "en")
        assert cls.verifiability > 0.0

    def test_domain_crossing(self) -> None:
        from si_protocols.marker_registry import get_markers

        markers = get_markers("en")
        text = "Quantum vibration connects all chakra through the DNA frequency of ascension."
        cls = _classify_sentence(text, markers, "en")
        assert cls.domain_coherence > 0.0

    def test_logical_connectors_lower_dependency(self) -> None:
        from si_protocols.marker_registry import get_markers

        markers = get_markers("en")
        text_with = "Because the data shows, therefore the conclusion follows."
        text_without = "The energy is amazing and wonderful and divine."
        cls_with = _classify_sentence(text_with, markers, "en")
        cls_without = _classify_sentence(text_without, markers, "en")
        assert cls_with.logical_dependency < cls_without.logical_dependency


# ---------------------------------------------------------------------------
# Japanese support
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestJapaneseSupport:
    def test_japanese_extraction(self) -> None:
        engine = RuleEngine()
        text = (
            "銀河連合がついに動き出しました。日本への緊急介入が決定されました。\n\n"
            "量子波動がチャクラシステムを通じてすべての生命をつなげています。"
        )
        variables = engine.extract_variables(text, lang="ja")
        assert len(variables) >= 1


# ---------------------------------------------------------------------------
# Claim detection
# ---------------------------------------------------------------------------


class TestIsClaim:
    def test_authority_phrase_is_claim(self) -> None:
        from si_protocols.marker_registry import get_markers

        markers = get_markers("en")
        assert _is_claim("the ascended masters say this is true", markers)

    def test_plain_sentence_not_claim(self) -> None:
        from si_protocols.marker_registry import get_markers

        markers = get_markers("en")
        assert not _is_claim("The cat sat on the mat.", markers)
