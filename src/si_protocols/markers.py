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
