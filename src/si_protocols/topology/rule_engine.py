"""Local, deterministic rule engine (Tier 0) for topology variable extraction.

Uses spaCy NLP + existing marker sets to extract claims from text and classify
them along four axes: falsifiability, verifiability, domain coherence, and
logical dependency.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import spacy

from si_protocols.marker_registry import SupportedLang, get_markers
from si_protocols.topology.types import (
    TopologyLevel,
    Variable,
    VariableClassification,
    VariableKind,
)

if TYPE_CHECKING:
    from spacy.tokens import Doc, Span

    from si_protocols.marker_registry import MarkerSet


# ---------------------------------------------------------------------------
# Own NLP cache — independent from threat_filter
# ---------------------------------------------------------------------------

_nlp_cache: dict[str, spacy.language.Language] = {}

_LANG_MODELS: dict[str, str] = {
    "en": "en_core_web_sm",
    "ja": "ja_core_news_sm",
}


def _get_nlp(lang: SupportedLang = "en") -> spacy.language.Language:
    """Load spaCy model on first use for the given language."""
    if lang not in _nlp_cache:
        model = _LANG_MODELS[lang]
        _nlp_cache[lang] = spacy.load(model)
    return _nlp_cache[lang]


# ---------------------------------------------------------------------------
# Domain markers (module-level constants)
# ---------------------------------------------------------------------------

_SCIENTIFIC_DOMAIN_EN: frozenset[str] = frozenset(
    {
        "quantum",
        "dna",
        "frequency",
        "electron",
        "photon",
        "molecule",
        "neuroscience",
        "electromagnetic",
        "genome",
        "cellular",
        "particle",
        "wavelength",
        "resonance",
        "atomic",
        "neural",
        "dimension",
    }
)

_SCIENTIFIC_DOMAIN_JA: frozenset[str] = frozenset(
    {
        "量子",
        "dna",
        "周波数",
        "電子",
        "光子",
        "分子",
        "脳科学",
        "電磁",
        "ゲノム",
        "細胞",
        "粒子",
        "波長",
        "共鳴",
        "原子",
        "神経",
        "次元",
    }
)

_SPIRITUAL_DOMAIN_EN: frozenset[str] = frozenset(
    {
        "chakra",
        "ascension",
        "vibration",
        "karma",
        "aura",
        "enlightenment",
        "kundalini",
        "meditation",
        "astral",
        "etheric",
        "reincarnation",
        "mantra",
        "dharma",
        "nirvana",
        "samsara",
        "soul",
        # New-age / conspirituality terms
        "galactic federation",
        "ascended masters",
        "lightworker",
        "twin flame",
        "starseed",
        "fifth dimension",
        "awakening",
        "chosen",
        "sacred",
        "divine",
        "cosmic",
        "new earth",
    }
)

_SPIRITUAL_DOMAIN_JA: frozenset[str] = frozenset(
    {
        "チャクラ",
        "アセンション",
        "波動",
        "カルマ",
        "オーラ",
        "悟り",
        "クンダリーニ",
        "瞑想",
        "アストラル",
        "エーテル",
        "輪廻",
        "マントラ",
        "ダルマ",
        "涅槃",
        "輪廻転生",
        "魂",
        # New-age / conspirituality terms common in JA manipulation texts
        "銀河連合",
        "アセンデッドマスター",
        "ライトワーカー",
        "ツインソウル",
        "ツインレイ",
        "次元上昇",
        "転生",
        "覚醒",
        "選ばれた",
        "光の存在",
        "エネルギーコード",
        "タイムライン",
        "スターシード",
        "プレアデス",
        "アルクトゥルス",
        "ネガティブ",
        "新しい地球",
        "古い地球",
    }
)

_LOGICAL_CONNECTORS_EN: frozenset[str] = frozenset(
    {
        "therefore",
        "because",
        "since",
        "thus",
        "hence",
        "consequently",
        "as a result",
        "so that",
        "in order to",
        "given that",
        "due to",
        "for this reason",
        "it follows that",
        "accordingly",
    }
)

_LOGICAL_CONNECTORS_JA: frozenset[str] = frozenset(
    {
        "したがって",
        "なぜなら",
        "だから",
        "そのため",
        "よって",
        "ゆえに",
        "その結果",
        "つまり",
        "すなわち",
    }
)


def _get_domain_markers(
    lang: SupportedLang,
) -> tuple[frozenset[str], frozenset[str], frozenset[str]]:
    """Return (scientific, spiritual, logical_connectors) for the language."""
    if lang == "ja":
        return _SCIENTIFIC_DOMAIN_JA, _SPIRITUAL_DOMAIN_JA, _LOGICAL_CONNECTORS_JA
    return _SCIENTIFIC_DOMAIN_EN, _SPIRITUAL_DOMAIN_EN, _LOGICAL_CONNECTORS_EN


# ---------------------------------------------------------------------------
# Claim detection helpers
# ---------------------------------------------------------------------------


def _is_claim(sent_text: str, markers: MarkerSet) -> bool:
    """Heuristic: is this sentence a 'claim' worth classifying?

    Returns True if the sentence matches any authority/urgency/source markers
    or contains a high density of vague adjectives.
    """
    lower = sent_text.lower()

    # Authority phrases
    for phrase in markers.authority_phrases:
        if phrase in lower:
            return True

    # Urgency patterns
    for pattern in markers.urgency_patterns:
        if pattern in lower:
            return True

    # Unfalsifiable sources
    for phrase in markers.unfalsifiable_source_phrases:
        if phrase in lower:
            return True

    # Unnamed authorities
    for phrase in markers.unnamed_authority_phrases:
        if phrase in lower:
            return True

    # Vague adjective density
    vague_count = sum(1 for adj in markers.vague_adjectives if adj in lower)
    if vague_count >= 2:
        return True

    # Keyword-based checks for Japanese
    if markers.authority_keyword_groups:
        for _label, keywords in markers.authority_keyword_groups:
            if all(kw in lower for kw in keywords):
                return True

    if markers.urgency_keywords:
        for kw in markers.urgency_keywords:
            if kw in lower:
                return True

    if markers.unfalsifiable_keyword_groups:
        for _label, keywords in markers.unfalsifiable_keyword_groups:
            if all(kw in lower for kw in keywords):
                return True

    if markers.unnamed_authority_keywords:
        for kw in markers.unnamed_authority_keywords:
            if kw in lower:
                return True

    # Verifiable citations are also claims — just verifiable ones
    for marker in markers.verifiable_citation_markers:
        if marker in lower:
            return True

    return False


def _classify_sentence(
    sent_text: str,
    markers: MarkerSet,
    lang: SupportedLang,
) -> VariableClassification:
    """Score a sentence along the four classification axes."""
    lower = sent_text.lower()
    sci_markers, spi_markers, connectors = _get_domain_markers(lang)

    # --- Falsifiability ---
    falsifiability = 0.0
    for phrase in markers.unfalsifiable_source_phrases:
        if phrase in lower:
            falsifiability += 0.3
    if markers.unfalsifiable_keyword_groups:
        for _label, keywords in markers.unfalsifiable_keyword_groups:
            if all(kw in lower for kw in keywords):
                falsifiability += 0.3

    # Vague adjectives (phrase-based for EN, stem-based for JA)
    vague_count = sum(1 for adj in markers.vague_adjectives if adj in lower)
    if markers.vague_adjective_stems:
        vague_count += sum(1 for stem in markers.vague_adjective_stems if stem in lower)
    if vague_count >= 2:
        falsifiability += min(vague_count * 0.15, 0.5)

    # Authority phrases / keyword groups also suggest unfalsifiable framing
    for phrase in markers.authority_phrases:
        if phrase in lower:
            falsifiability += 0.2
            break
    if markers.authority_keyword_groups:
        for _label, keywords in markers.authority_keyword_groups:
            if all(kw in lower for kw in keywords):
                falsifiability += 0.3
                break

    # Urgency markers raise falsifiability (urgent claims resist verification)
    urgency_hit = False
    for pattern in markers.urgency_patterns:
        if pattern in lower:
            urgency_hit = True
            break
    if not urgency_hit and markers.urgency_keywords:
        for kw in markers.urgency_keywords:
            if kw in lower:
                urgency_hit = True
                break
    if urgency_hit:
        falsifiability += 0.2

    # Spiritual-domain vocabulary raises falsifiability (unfalsifiable claims)
    spi_count_f = sum(1 for term in spi_markers if term in lower)
    if spi_count_f >= 1:
        falsifiability += min(spi_count_f * 0.15, 0.4)

    # Spiritual-domain sentences without verifiable citations are inherently unfalsifiable
    has_citation_f = any(marker in lower for marker in markers.verifiable_citation_markers)
    if spi_count_f >= 1 and not has_citation_f:
        falsifiability += 0.2

    if has_citation_f:
        falsifiability -= 0.3

    falsifiability = max(0.0, min(1.0, falsifiability))

    # --- Verifiability ---
    verifiability = 0.0
    for phrase in markers.unnamed_authority_phrases:
        if phrase in lower:
            verifiability += 0.4
    if markers.unnamed_authority_keywords:
        for kw in markers.unnamed_authority_keywords:
            if kw in lower:
                verifiability += 0.4
                break

    # Authority phrases/keywords without named sources = unverifiable
    authority_hit = False
    for phrase in markers.authority_phrases:
        if phrase in lower:
            authority_hit = True
            break
    if not authority_hit and markers.authority_keyword_groups:
        for _label, keywords in markers.authority_keyword_groups:
            if all(kw in lower for kw in keywords):
                authority_hit = True
                break
    if authority_hit:
        verifiability += 0.3

    for marker in markers.verifiable_citation_markers:
        if marker in lower:
            verifiability -= 0.2

    # Named entities with context — skip sentence-initial word (always capitalised)
    words = sent_text.split()
    non_initial_caps = [w for w in words[1:] if w[0:1].isupper() and len(w) > 1]
    verifiability -= len(non_initial_caps) * 0.05

    # Spiritual-domain sentences without verifiable citations are unverifiable
    has_citation = any(marker in lower for marker in markers.verifiable_citation_markers)
    if any(term in lower for term in spi_markers) and not has_citation:
        verifiability += 0.3

    verifiability = max(0.0, min(1.0, verifiability))

    # --- Domain coherence ---
    sci_count = sum(1 for term in sci_markers if term in lower)
    spi_count = sum(1 for term in spi_markers if term in lower)
    domain_coherence = min(sci_count * spi_count * 0.2, 1.0)

    # --- Logical dependency ---
    logical_dependency = 0.0

    # Check for emotional words (fear + euphoria)
    emotion_count = sum(1 for w in markers.fear_words if w in lower)
    emotion_count += sum(1 for w in markers.euphoria_words if w in lower)
    for phrase in markers.fear_phrases:
        if phrase in lower:
            emotion_count += 1
    for phrase in markers.euphoria_phrases:
        if phrase in lower:
            emotion_count += 1
    if emotion_count >= 1:
        logical_dependency += 0.3

    # Urgency also inflates logical dependency (emotional pressure)
    if urgency_hit:
        logical_dependency += 0.2

    has_connector = False
    for connector in connectors:
        if connector in lower:
            has_connector = True
            break

    if has_connector:
        logical_dependency -= 0.3
    else:
        logical_dependency += 0.2

    logical_dependency = max(0.0, min(1.0, logical_dependency))

    return VariableClassification(
        falsifiability=round(falsifiability, 3),
        verifiability=round(verifiability, 3),
        domain_coherence=round(domain_coherence, 3),
        logical_dependency=round(logical_dependency, 3),
    )


def _derive_kind(classification: VariableClassification) -> VariableKind:
    """Derive variable kind from the mean of the four axes.

    Thresholds: PSEUDO >= 0.4, TRUE <= 0.15, else INDETERMINATE.
    Also checks if any single axis is notably suspicious (>= 0.5).
    """
    mean = (
        classification.falsifiability
        + classification.verifiability
        + classification.domain_coherence
        + classification.logical_dependency
    ) / 4

    # A strongly suspicious single axis can push towards PSEUDO
    max_axis = max(
        classification.falsifiability,
        classification.verifiability,
        classification.domain_coherence,
        classification.logical_dependency,
    )

    if mean >= 0.4 or (mean >= 0.25 and max_axis >= 0.5):
        return VariableKind.PSEUDO
    if mean <= 0.15:
        return VariableKind.TRUE
    return VariableKind.INDETERMINATE


def _assign_level(
    sent_idx: int,
    total_sents: int,
    para_idx: int,
    total_paras: int,
) -> TopologyLevel:
    """Assign a topology level based on position in the text.

    Single-paragraph texts yield MACRO. Multi-paragraph texts assign MESO to
    paragraph-level groupings and MICRO to individual sentences.
    """
    if total_paras <= 1 and total_sents <= 3:
        return TopologyLevel.MACRO
    if total_sents <= 1:
        return TopologyLevel.MESO
    return TopologyLevel.MICRO


# ---------------------------------------------------------------------------
# RuleEngine
# ---------------------------------------------------------------------------


class RuleEngine:
    """Local, deterministic analysis engine using spaCy + marker heuristics.

    Satisfies the :class:`~si_protocols.topology.engine.AnalysisEngine` protocol.
    """

    @property
    def name(self) -> str:
        return "rule"

    def extract_variables(
        self,
        text: str,
        *,
        lang: SupportedLang = "en",
    ) -> list[Variable]:
        """Extract and classify variables (claims) from *text*."""
        nlp = _get_nlp(lang)
        markers = get_markers(lang)

        # Segment into paragraphs
        paragraphs: list[str] = [p.strip() for p in text.split("\n\n") if p.strip()]
        total_paras = len(paragraphs)

        variables: list[Variable] = []
        var_counter = 0
        global_sent_idx = 0

        for para_idx, para in enumerate(paragraphs):
            doc: Doc = nlp(para)
            sents: list[Span] = list(doc.sents)
            total_sents = len(sents)

            # For agglutinative languages (e.g. Japanese), keyword groups
            # may span across sentence boundaries within a paragraph.
            # Check at paragraph level as fallback.
            para_is_claim = _is_claim(para, markers)

            for sent_idx, sent in enumerate(sents):
                sent_text = sent.text.strip()
                if not sent_text:
                    continue

                if not _is_claim(sent_text, markers) and not para_is_claim:
                    global_sent_idx += 1
                    continue

                classification = _classify_sentence(sent_text, markers, lang)
                kind = _derive_kind(classification)
                level = _assign_level(sent_idx, total_sents, para_idx, total_paras)

                # Calculate approximate character offset in original text
                start = text.find(sent_text)
                end = start + len(sent_text) if start >= 0 else 0

                var_counter += 1
                variables.append(
                    Variable(
                        id=f"v{var_counter}",
                        text=sent_text,
                        source_span=(max(0, start), max(0, end)),
                        classification=classification,
                        kind=kind,
                        level=level,
                        confidence=0.5,
                    )
                )
                global_sent_idx += 1

        return variables
