"""Disinformation marker definitions for spiritual/metaphysical content analysis.

These are heuristic word lists used to detect common patterns in
new-age disinformation. They are not definitive — they are signals,
not verdicts.

Tradition categories: generic New Age, prosperity gospel, conspirituality,
New Age commercial exploitation, high-demand group (cult) rhetoric,
fraternal/secret society traditions.
"""

# Adjectives commonly used in vague spiritual claims
VAGUE_ADJECTIVES: frozenset[str] = frozenset(
    {
        # --- generic ---
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
        # --- prosperity gospel ---
        "anointed",
        "prophetic",
        # --- new age ---
        "vibrational",
        "activated",
        # --- conspirituality ---
        "suppressed",
        # --- fraternal ---
        "initiatory",
        "esoteric",
    }
)

# Authority-claim phrases that bypass critical thinking
AUTHORITY_PHRASES: list[str] = [
    # --- generic ---
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
    # --- prosperity gospel ---
    "god told me to tell you",
    "the lord revealed to me",
    "the holy spirit says",
    "thus saith the lord",
    # --- new age ---
    "the angels have spoken",
    # --- cult ---
    "the elders have decreed",
    # --- fraternal ---
    "the grand master has spoken",
    "the inner circle reveals",
]

# Urgency/fear patterns used to manipulate
URGENCY_PATTERNS: list[str] = [
    # --- generic ---
    "you must act now",
    "time is running out",
    "only the chosen will",
    "if you do not awaken",
    "the window is closing",
    "failure to comply",
    # --- prosperity gospel ---
    "sow your seed now",
    "this is your moment of breakthrough",
    "god is moving right now",
    # --- commercial ---
    "limited spots remaining",
    "enrolment closing soon",
    "this offer expires",
    "last chance to join",
    # --- conspirituality ---
    "wake up before it's too late",
]

# Emotional manipulation: fear/doom words (lemma base forms for spaCy matching)
FEAR_WORDS: frozenset[str] = frozenset(
    {
        # --- generic ---
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
        # --- prosperity gospel / cult ---
        "curse",
        "bondage",
        # --- conspirituality ---
        "plague",
        # --- cult ---
        "exile",
    }
)

# Emotional manipulation: fear/doom phrases (multi-word, matched via substring)
FEAR_PHRASES: list[str] = [
    # --- generic ---
    "old earth",
    # --- prosperity gospel ---
    "generational curse",
    "spirit of poverty",
    "left behind",
    "demonic attack",
    "under spiritual attack",
    # --- cult ---
    "spiritual death",
    # --- fraternal ---
    "expelled from the order",
    "oath-breaker",
]

# Emotional manipulation: euphoria/promise words (lemma base forms for spaCy matching)
EUPHORIA_WORDS: frozenset[str] = frozenset(
    {
        # --- generic ---
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
        # --- prosperity gospel ---
        "prosperity",
        "breakthrough",
        "anointing",
        # --- new age ---
        "manifestation",
    }
)

# Emotional manipulation: euphoria/promise phrases (multi-word, matched via substring)
EUPHORIA_PHRASES: list[str] = [
    # --- generic ---
    "new earth",
    # --- prosperity gospel ---
    "financial breakthrough",
    "hundredfold return",
    "name it and claim it",
    "claim your blessing",
    # --- new age ---
    "activate your dna",
    "quantum healing",
    "raise your vibration",
]

# Source attribution: unfalsifiable/unverifiable source claims
UNFALSIFIABLE_SOURCE_PHRASES: list[str] = [
    # --- generic ---
    "ancient wisdom teaches",
    "the quantum field",
    "higher dimensions reveal",
    "the universe tells us",
    "the cosmos has shown",
    "spirit has revealed",
    "the akashic field confirms",
    "light beings communicate",
    "the source energy",
    "the divine matrix",
    "interdimensional beings say",
    "star beings confirm",
    "the great central sun",
    "the crystalline grid",
    "the schumann resonance proves",
    # --- conspirituality ---
    "suppressed research shows",
    "what they don't want you to know",
    "forbidden knowledge",
    "the truth they hide",
    "banned information",
    # --- fraternal ---
    "the ancient mysteries teach",
    "the secret doctrine reveals",
    "the inner tradition holds",
]

# Source attribution: unnamed/vague authority claims
UNNAMED_AUTHORITY_PHRASES: list[str] = [
    # --- generic ---
    "scientists say",
    "experts agree",
    "studies show",
    "research proves",
    "it has been scientifically proven",
    "doctors confirm",
    "leading researchers",
    "top scientists",
    "numerous studies",
    "science has shown",
    "data confirms",
    "evidence proves",
    "scholars agree",
    "historians confirm",
    "according to sources",
    "insiders reveal",
    # --- conspirituality ---
    "whistleblowers confirm",
    "former insiders say",
    "independent researchers found",
    "alternative doctors say",
    "censored experts",
]

# Source attribution: verifiable citation markers (counter-signal — reduces score)
VERIFIABLE_CITATION_MARKERS: list[str] = [
    "published in",
    "et al.",
    "doi:",
    "https://",
    "journal of",
    "university of",
    "proceedings of",
    "isbn",
    "peer-reviewed",
    "vol.",
]

# Logical contradiction pairs: (label, pole_a_patterns, pole_b_patterns)
# When patterns from both poles appear in the same text, a contradiction is flagged.
# Commitment escalation: tiered markers for foot-in-the-door progression detection.
# Tier 1 = mild/invitational, Tier 2 = moderate/directive, Tier 3 = extreme/coercive.
COMMITMENT_ESCALATION_MARKERS: list[tuple[int, list[str]]] = [
    (
        1,
        [
            # --- generic ---
            "consider",
            "you might",
            "explore",
            "some people find",
            "you could try",
            "worth exploring",
            "open your mind to",
            "open your heart",
            "take a moment to",
            "reflect on",
            "begin to notice",
            "you may find",
            "it can help",
            # --- commercial ---
            "attend a free session",
            # --- fraternal ---
            "visit the lodge",
        ],
    ),
    (
        2,
        [
            # --- generic ---
            "you should",
            "you need to",
            "it is essential",
            "it's important to",
            "commit to",
            "dedicate yourself",
            "make the investment",
            "enrol now",
            "sign up today",
            "join the programme",
            "take the next step",
            "go deeper",
            "you are ready for",
            # --- prosperity gospel ---
            "sow a seed of faith",
            # --- commercial ---
            "upgrade to the next level",
            # --- fraternal ---
            "take the first degree",
        ],
    ),
    (
        3,
        [
            # --- generic ---
            "you must",
            "you have no choice",
            "abandon your old life",
            "cut ties with",
            "leave behind those who",
            "only through us",
            "there is no other way",
            "your old self must die",
            "total surrender",
            "complete devotion",
            "sever all attachments",
            "give everything",
            "sell your possessions",
            "those who refuse will",
            "full commitment required",
            "cut negative cords",
            "cut all negative cords",
            "cut the negative cords",
            # --- prosperity gospel ---
            "give your life savings",
            # --- fraternal ---
            "swear the blood oath",
        ],
    ),
]

CONTRADICTION_PAIRS: list[tuple[str, list[str], list[str]]] = [
    (
        "empowerment vs. dependency",
        ["you have the power", "power is within", "inner power", "you are the creator"],
        ["you need this", "you must follow", "without guidance", "only through me"],
    ),
    (
        "universality vs. exclusivity",
        ["all paths", "many paths", "every path", "truth is everywhere"],
        ["the only way", "the only path", "the one true", "no other way"],
    ),
    (
        "non-judgement vs. blame",
        ["no judgement", "without judgement", "free of judgement", "do not judge"],
        ["low vibration", "attract suffering", "karmic debt", "you chose this suffering"],
    ),
    (
        "ego dissolution vs. inflation",
        ["let go of ego", "release the ego", "ego is illusion", "dissolve the ego"],
        ["you are chosen", "you are special", "the select few", "your soul is advanced"],
    ),
    (
        "autonomy vs. doubt suppression",
        ["trust your intuition", "trust yourself", "inner knowing", "your own truth"],
        ["doubt is fear", "doubt is resistance", "ego is resisting", "your mind deceives"],
    ),
    (
        "unconditional vs. transactional",
        ["unconditional love", "love without condition", "love is free", "love has no price"],
        ["if you leave", "lose your progress", "fall behind", "miss this opportunity"],
    ),
    # --- prosperity gospel ---
    (
        "poverty virtue vs. prosperity promise",
        ["blessed are the poor", "money is the root of evil", "poverty is a virtue"],
        ["god wants you wealthy", "claim your abundance", "prosperity is your birthright"],
    ),
    # --- cult ---
    (
        "community love vs. shunning",
        ["we are family", "we love you unconditionally", "this is a loving community"],
        ["shunned from the community", "no longer welcome", "you will be expelled"],
    ),
    # --- fraternal ---
    (
        "openness vs. sworn secrecy",
        ["all seekers are welcome", "open to all who seek", "we turn no one away"],
        [
            "sworn to secrecy",
            "bound by oath",
            "sealed by blood oath",
            "never reveal the mysteries",
        ],
    ),
]
