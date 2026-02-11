---
title: "Beyond NLP: Detecting Deception Without LLMs"
description: Creative approaches to spotting disinformation in spiritual content — no large language models or social media graphs required.
date: 2026-02-09
tags: [research, detection, architecture]
---

## The Obvious Tools Aren't the Only Tools

When people think about disinformation detection, they usually reach for two things: large language models or social network analysis. LLMs are powerful but opaque — they trade one black box (the deceptive text) for another (the model's reasoning). Social graph analysis requires access to platform data, user accounts, and sharing patterns, which conflicts with our local-only, privacy-first design.

So we asked a different question: **what structural, psychological, and information-theoretic signals are hiding in the text itself?**

It turns out there are quite a few — and most of them are underexplored in the spiritual and metaphysical domain.

## Approaches We're Investigating

### 1. Logical contradiction detection

This one is particularly relevant to spiritual deception. Manipulative texts frequently contain internal contradictions that serve a strategic purpose — they keep the reader off-balance and dependent on the authority figure to resolve the tension.

The general problem of automated logical consistency checking is extremely hard. But spiritual deception relies on a surprisingly small set of **recurring contradiction archetypes**:

| Claim A | Claim B | Tension |
|---|---|---|
| "You have infinite power within" | "You need this course/teacher/tool" | Empowerment vs. dependency |
| "All paths lead to truth" | "This is the only way" | Universality vs. exclusivity |
| "There is no judgement" | "Low-vibration people attract suffering" | Non-judgement vs. blame |
| "Let go of ego" | "You are a chosen/special soul" | Ego dissolution vs. inflation |
| "Trust your intuition" | "Your doubts are resistance/fear" | Autonomy vs. doubt suppression |
| "Love is unconditional" | "If you leave, you'll lose progress" | Unconditional vs. transactional |

These can be implemented as **contradiction pairs** — two pattern sets representing opposing poles. When both poles appear in the same text, that's a signal worth examining. This approach is structurally similar to how our existing emotional manipulation scorer works (detecting both fear and euphoria words, with a contrast bonus when both polarities appear). It fits naturally into our marker-based architecture.

It won't catch every logical inconsistency. But it catches the ones that frequently appear in this domain.

### 2. Influence technique fingerprinting

Rather than asking "does this text contain manipulative language?", we can ask "**which specific influence techniques is this text deploying?**"

Robert Cialdini's six principles of influence (reciprocity, scarcity, authority, consistency, liking, consensus) and Steven Hassan's BITE model (Behaviour, Information, Thought, Emotional control) provide well-researched frameworks with detectable textual markers.

A text that activates one or two influence vectors might be ordinary persuasion. A text that simultaneously activates four or five is worth scrutinising. The output could be a radar chart showing which influence channels a text is using — giving readers a structural map of the persuasion attempt rather than just a single score.

### 3. Source attribution analysis

How does a text justify its claims? We can categorise every assertion into an attribution type:

- **No source** — claim presented as self-evident
- **Self-referential** — "as I channelled", "in my experience"
- **Unfalsifiable** — "ancient wisdom", "the Akashic records", "higher dimensions"
- **Appeal to unnamed authority** — "scientists say", "experts agree"
- **Verifiable citation** — a specific, checkable reference

The distribution across these categories reveals structural patterns. A text where 90% of claims fall into the "unfalsifiable" or "no source" categories looks structurally different from one that mixes personal experience with verifiable references — even if both discuss the same topic.

This is purely structural pattern matching. No NLP model needed beyond basic sentence segmentation.

### 4. Commitment escalation patterns

Classic persuasion follows a "foot-in-the-door" structure: start with universally agreeable claims, then gradually escalate to extraordinary ones. "We all want peace" becomes "and that's why you must cut ties with anyone who questions this teaching."

We can measure **claim intensity over a document's progression**. A monotonically increasing intensity curve — where each section asks for more belief or commitment than the last — is a well-documented persuasion technique. Honest exploration doesn't need to boil the frog.

### 5. Cognitive load manipulation

Deceptive spiritual content often alternates between deliberately obscure passages (to create a feeling of profundity) and oversimplified conclusions (to implant the desired belief). The reader is first confused, then offered a simple resolution — and the relief of understanding feels like truth.

We can detect this by measuring **readability variance within a single text**. High variance in readability scores across paragraphs — some passages at postgraduate level, others at primary school level — is a signal of deliberate cognitive manipulation. Genuine complex ideas maintain relatively consistent complexity throughout.

### 6. Stylometric entropy

Manipulative texts often exhibit low information density — they say a lot without saying much. We can measure Shannon entropy at the word and sentence level to compute a "substance ratio": unique semantic content versus total word count.

Zipf's law deviations offer another angle. Genuine expert writing follows predictable word frequency distributions. Manipulative writing — with its repetitive hammering of key phrases and emotional triggers — often doesn't.

### 7. Hedging-to-assertion ratio

Honest communicators hedge proportionally to uncertainty: "I believe", "in my experience", "one interpretation is". Manipulative content tends toward either extreme — zero hedging (absolute authority) or strategic hedging that creates plausible deniability ("I'm not saying X, but...").

The insight is that measuring the **distribution** of hedging matters more than measuring its presence or absence. A text that alternates between absolute claims and strategic disclaimers has a different hedging signature than one that hedges consistently.

## A Tool for Thinking, Not a Truth Oracle

An important caveat runs through all of these approaches: **flagging a pattern is not the same as declaring something false.**

Not every unfalsifiable claim is deceptive. Some of the most important truths in human experience — subjective, contemplative, emergent — have no conventional evidence and may never have any. A genuine spiritual insight and a manipulative fabrication can both lack citations. The difference isn't in the evidence — it's in how the claim relates to the reader's autonomy.

Similarly, the contradiction pairs listed above are not automatically deceptive. "You have inner power" and "a teacher can help you" coexist naturally in any honest learning relationship. The signal worth examining is not the mere presence of opposing ideas, but whether they're being wielded to create dependency, suppress doubt, or shut down critical thinking.

This is the core design principle of si-protocols: **we don't tell you what to believe — or disbelieve.** We surface structural patterns so you can examine them yourself, with your own thinking *and* your own feeling. The goal is threefold:

- **Don't swallow information uncritically** — the patterns we detect are worth pausing over, not ignoring.
- **Don't jump to oversimplistic conclusions** — reality is rarely as clean as "empowerment vs. dependency" or "white lodge vs. dark lodge". Dichotomous framing is itself a manipulation pattern.
- **Don't jump to "this is deception" either** — a high score is not a verdict. Before dismissing something as manipulative, examine it yourself. Content that triggers pattern detectors might be genuinely challenging, unconventional, or ahead of its time. The tool invites deeper examination, not automatic rejection.

A disinformation detection tool that makes people reflexively *dismiss* content is just as harmful as one that makes them reflexively *accept* it. Both bypass genuine thinking. We're building a tool that sits between those extremes — one that asks you to slow down, look at the structure, and decide for yourself.

## What These Approaches Share

None of these require:
- Large language models or cloud APIs
- Social media data or user accounts
- Training data from real victims
- Black-box classifiers

They all work on **structural properties of text** — patterns that can be detected with transparent, auditable rules. They complement rather than replace NLP-based analysis. And they can all be implemented as additional scoring dimensions in our existing marker-based architecture.

## What's Next

We're planning to implement these as new dimensions in si-protocols' threat filter, starting with **logical contradiction detection** and **source attribution analysis** — the two approaches that offer the highest signal with the least implementation complexity.

Each will follow our existing pattern: define markers in `markers.py`, score in `threat_filter.py`, test with synthetic examples. Transparent, local-only, and open-source.

If you work in cult recovery, undue influence research, or digital literacy education, we'd love to hear which of these signals match what you see in practice. Open an issue on [GitHub](https://github.com/lemur47/si-protocols) or reach out directly.

---

*si-protocols is MIT-licenced. We analyse text structure, not people. Your content never leaves your machine.*
