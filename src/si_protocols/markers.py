"""Disinformation marker definitions for spiritual/metaphysical content analysis.

These are heuristic word lists used to detect common patterns in
new-age disinformation. They are not definitive — they are signals,
not verdicts.
"""

# Adjectives commonly used in vague spiritual claims
VAGUE_ADJECTIVES: frozenset[str] = frozenset(
    {
        "ancient",
        "ascended",
        "celestial",
        "cosmic",
        "divine",
        "eternal",
        "hidden",
        "ineffable",
        "mysterious",
        "sacred",
        "secret",
        "sovereign",
        "transcendent",
        "veiled",
        "light",
    }
)

# Authority-claim phrases that bypass critical thinking
AUTHORITY_PHRASES: list[str] = [
    "the ascended masters say",
    "channelled directly from",
    "the galactic federation confirms",
    "it has been revealed that",
    "the akashic records show",
    "ancient prophecy states",
    "the council of light decrees",
    "the galactic federation of light tells",
    "ashtar speaks",
    "saint germain speaks",
]

# Urgency/fear patterns used to manipulate
URGENCY_PATTERNS: list[str] = [
    "you must act now",
    "time is running out",
    "only the chosen will",
    "if you do not awaken",
    "the window is closing",
    "failure to comply",
]

# Emotional manipulation: fear/doom words (lemma base forms for spaCy matching)
FEAR_WORDS: frozenset[str] = frozenset(
    {
        "annihilation",
        "calamity",
        "catastrophe",
        "collapse",
        "damnation",
        "despair",
        "destruction",
        "devastation",
        "doom",
        "peril",
        "ruin",
        "suffer",
        "torment",
        "tribulation",
        "wrath",
    }
)

# Emotional manipulation: fear/doom phrases (multi-word, matched via substring)
FEAR_PHRASES: list[str] = [
    "old earth",
]

# Emotional manipulation: euphoria/promise words (lemma base forms for spaCy matching)
EUPHORIA_WORDS: frozenset[str] = frozenset(
    {
        "abundance",
        "ascension",
        "awakening",
        "bliss",
        "enlightenment",
        "harmony",
        "liberation",
        "miracle",
        "nirvana",
        "paradise",
        "rapture",
        "rebirth",
        "salvation",
        "transcendence",
        "utopia",
    }
)

# Emotional manipulation: euphoria/promise phrases (multi-word, matched via substring)
EUPHORIA_PHRASES: list[str] = [
    "new earth",
]
