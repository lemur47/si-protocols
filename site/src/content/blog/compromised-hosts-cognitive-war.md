---
title: "Compromised Hosts: How a Spiritual Business Becomes a Node in Someone Else's Cognitive War"
description: A structural analysis of how well-meaning spiritual creators end up amplifying cognitive-warfare payloads they would not endorse — and what hardening looks like at the node.
date: 2026-05-30
tags: [cognitive-warfare, cvp, threat-analysis, egregore]
---

## A Reframe Before We Start

This post is not about deceptive spiritual entrepreneurs operating in bad faith. It's about the structural condition where well-intentioned creators find themselves serving as relay nodes in cognitive-warfare campaigns they would not endorse if they could see them clearly.

The analogy doing the most work here is the **botnet**. A botnet is built from ordinary machines whose owners haven't done anything wrong. They opened an email, or installed a browser extension, or downloaded a free utility that asked for permissions they didn't fully read. The machine then forwards traffic, amplifies attacks, and contributes computational resources to operations its owner would never knowingly support. The owner's machine is doing the work. The owner does not know.

That's the structural position this post describes. The spiritual creator is the host. The cognitive payload is the traffic. The audience is downstream.

This is not a moral claim about the host. It's a structural claim about what the host is being asked to do.

## Cognitive Warfare Has a Kill Chain

The military domain has been formalising cognitive warfare faster than the civilian one. The clearest taxonomy of how a cognitive campaign actually runs comes from [Plaza et al. (2023)](https://doi.org/10.1145/3600160.3605080), a peer-reviewed systematic review published at the ARES conference and funded under the European Defence Fund. Their model — the **Cognitive Cyber Kill Chain** — describes five sequential phases:

1. **Reconnaissance** — mapping the target audience's beliefs, vulnerabilities, and media environment
2. **Preparation** — crafting payloads that exploit the mapped vulnerabilities
3. **Distribution** — initial seeding through controlled channels
4. **Expansion** — dissemination to other individuals *who need not be the main target*
5. **Persistence** — maintaining the cognitive effect through repeated exposure and lock-in

The phase that matters for this post is **expansion**. Plaza's wording is explicit: the payload travels to individuals who are not the primary target. The primary target's role is to receive and forward. They are the dissemination layer.

That's the botnet step in technical terms. And that's where the spiritual brand enters.

## The Spiritual Brand Enters at Expansion

A spiritual creator is rarely the original target of a cognitive campaign. The primary target was upstream — the creator's source, the channel they trusted, the workshop they attended, the framework that crystallised their worldview. By the time the payload reaches the creator, it has been laundered through layers of plausible context and emotional resonance.

The creator's role, in the kill chain, is to **forward**. They re-encode the payload in their voice. They give it their audience's trust. They amplify.

The reason this stays invisible to the creator is the second piece of the framework. [Deppe and Schaal (2024)](https://doi.org/10.3389/fdata.2024.1452129), in their conceptual analysis of NATO Allied Command Transformation's cognitive-warfare doctrine, surface a definition with a specific load-bearing word: cognitive warfare is *designed to use information to activate the subconscious processes in our brains, making it difficult for our conscious minds to perceive the presence of a cognitive threat*.

That distinction is doing critical work. It's what separates cognitive warfare from disinformation, propaganda, or conventional persuasion. The other three want the target to consciously change its mind. Cognitive warfare wants the target to never notice the change.

The host's consciousness is bypassed by design. That's not a failure of the host's discernment. It's a property of the payload.

## Well-Meaning Amplification Is the Mechanism

The third paper makes the mechanism concrete. [Paziuk et al. (2025)](https://doi.org/10.3389/frai.2025.1566022), studying the Russia-Ukraine information environment with NLP-based linguistic-marker detection, document what they call *well-meaning followers amplifying a payload*. The amplification is genuinely well-meaning — the follower believes they are helping, warning, awakening. The structure of the amplification is identical to what an adversarial actor would design.

Their finding generalises beyond geopolitics. Wherever a community combines high trust, high engagement, and low structural fact-checking norms, well-meaning amplification becomes the dominant transport for cognitive payloads. The community does not need to be infiltrated. It just needs to have the right shape.

The spiritual creator's amplification is not insincere. That's the point. Sincere amplification is the most effective kind.

## Why the Spiritual Domain Is Ideal Terrain

The conditions Plaza and Deppe identify as enabling cognitive warfare are present in the spiritual market at unusually high concentration:

- **No institutional verification norm.** Information arrives via "channelled", "downloaded", "transmitted" — language that positions the source as unverifiable and the receiver as a conduit, not an editor. Plaza's *testimony* technique (borrowed authority that cannot be checked) is the default content shape.
- **Audience profile maps to the published vulnerability taxonomy.** Deppe's micro/meso/macro factors — emotional arousal, social-belonging needs, reduced critical-information literacy in the specific domain — describe a meaningful slice of the spiritual market's audience by design. The market sells to those needs; cognitive-warfare campaigns find the same audience profile already concentrated.
- **AI as amplifier, already deployed.** Generative AI is in production use across the market for content drafting, oracle interpretation, channelling assistance, and audience targeting. The infrastructure for fast payload propagation is in place, with no fact-check norm above it.
- **A predictable next attack vector.** We expect prompt-injection attacks specifically targeting spiritual-industry AI tools to follow. The industry has already accepted "what comes through is valid" as a content-acceptance norm; AI-generated misinformation crosses that gate without resistance.

The point of this list is not that the spiritual market is uniquely bad. The point is that it's structurally permeable in ways the security literature has already mapped for other domains. The defensive vocabulary is portable.

## The Recruit Does Not See Itself as Recruited

Now the structural angle, because the recruitment mechanism has a precise shape worth being concrete about.

A botnet operator does not just have victims — it has **command-and-control infrastructure**. The classical C2 server issues instructions, collects telemetry, and pushes updated payloads to the compromised hosts. The trick that makes C2 work is that its traffic looks ordinary: DNS tunnelling, HTTPS callbacks, signed binaries with hidden behaviour. The host keeps running its legitimate workloads while also serving the operator's purposes, and the operator stays invisible because the C2 traffic is indistinguishable from normal.

The structural equivalent in the spiritual market is what esoteric tradition calls the **egregore** and what we model in the [Consciousness Virtualisation Platform](https://spiritualintelligence.cc/the-virtualisation-model/) as a [stateful container](https://spiritualintelligence.cc/egregores/) — a self-sustaining collective that operates with emergent survival logic and no single point of control. This is **distributed C2 with no server to take down.** The instructions are not pushed by an external operator; they are aggregated from the hosts' own outputs and redistributed back as identity, status, belonging, and "what the moment needs." A host running this kind of C2 is not malicious. It is well-integrated into a system it cannot see from the inside.

Now the move that matters for invisibility: the C2 channel does not stay at the network layer. It also runs through the host's own cognitive pipeline.

Repeated conscious engagement with the C2's redistributed signals — the framings, the urgency cues, the in-group vocabulary — gets internalised over time. This is ordinary learning machinery: anything the conscious mind rehearses with emotional weight eventually commits into subconscious deep-pattern storage. In CVP terms, the host's own conscious processing performs the commit from the mental instance (Layer 5) into the deep-pattern repository (Layer 3). **The egregore does not write to the host's deep patterns directly.** The host writes them — using its own internalisation pathway, while believing it is simply recognising what is true.

Once that commit happens, the pattern surfaces back to the host as inherited knowing. Not as incoming information that conscious inspection could examine — as a feeling of remembering, of having always known, of receiving something from somewhere ancient. The host then produces content from this internalised knowing, in their own voice, with full sincerity. The C2 instruction has become the host's truth.

That is the recruitment mechanism. The host is not deceived. The host is using its own perfectly functional learning machinery to install patterns it did not author. And because the commit runs through the host's own pipeline, no external counterintelligence boundary can intercept it — the patterns appear to arrive from inside, because the host's own cognition is the channel they arrived through.

## Node-Hardening

A precondition before the hygiene: hardening requires permission to have been a host. You cannot audit a system you are still defending. The reframe at the top of this post is not a courtesy — it is the prerequisite for the work that follows.

Plaza's countermeasure recommendations rest on two pillars: **Resilience** and **Education**. Both are designed for the audience side of the campaign — the consumers of cognitive payloads. We endorse them, and we want to add two specifically for the node side — the creators at risk of becoming relay infrastructure.

**Pillar three — outbound metadata hygiene.** The CVP names this as the L5→L6 boundary: the outbound counterintelligence layer. Most threat-modelling has focused on what arrives at the boundary (the inbound firewall). The outbound boundary is less inspected, and it is where the host's amplification actually happens.

In practical terms, hardening the node looks like asking, before any piece of content moves outward:

- **Authority structure.** Is the content's authority claim verifiable, or does it rest on testimony from an unfalsifiable source? Borrowed authority is the single most reliable signature of payload material.
- **Binary framing.** Does the content sort the audience into a chosen and unchosen group, an aligned and unaligned tier, a high-vibration and low-vibration class? Sorting is one of the kill chain's central effects.
- **Urgency stack.** Does the content combine scarcity (limited spots, closing window) with commitment escalation (each step requires more belief than the last)? That stack is the textbook persuasion architecture.
- **Source of source.** When the content references its origin, can the origin be inspected? Or is it bounded by an unfalsifiability layer (channelled, downloaded, transmitted, intuited)?
- **Exit cost.** Does engaging with the content increase the difficulty of subsequently disengaging from the system that produced it? Lock-in is a structural property; you can detect it without judging the system's intent.

These questions are not accusations. They are an editorial gate the host applies to its own outbound stream — the same hygiene a responsible publisher applies before forwarding material to an audience that trusts them.

**Pillar four — creator self-audit.** Our [Quick-Check Skill](https://github.com/lemur47/si-protocols/blob/main/skills/si-quick-check/SKILL.md) is most often framed as a tool for analysing other people's content — the audience-side question, *"is this trying to manipulate me?"* The more useful application, the one this post is arguing for, is the creator running their own outbound stream through the same instrument before publication.

The priorities of counterintelligence are inverted from those of intelligence. Detecting someone else's payload is the easy half. *Preventing one's own emission* is the load-bearing half. The Quick-Check Skill scores text across seven dimensions that map cleanly to the five questions above. Pointing it at your own draft before you publish is the lowest-friction single hardening step we know of. It is local, transparent, and free. We do not think it is the only way to apply the questions, but it is the one we have found most consistent in practice.

## What We Are Not Saying

A pattern this post identifies is not a verdict. We've written about this principle before in [Beyond NLP: Detecting Deception Without LLMs](https://spiritualintelligence.dev/blog/beyond-nlp-detecting-deception-without-llms/), and it applies again here, with two specific additions:

- **Pattern presence is not adversarial intent.** Authority appeals, binary framing, and urgency are present in genuine spiritual content, in news media, in education, in advocacy. Their presence is a flag for examination, not a sentence.
- **Recruited does not mean culpable.** The botnet metaphor matters: the host's machine was not asked. Reframing creators as compromised hosts is a structural description, not a moral one. There is a small but load-bearing piece of market hygiene in this: a creator who can accept that they may have been a host can audit themselves cleanly; a creator who has to defend that they are not one cannot. The constructive move is hardening, not blame — and the prerequisite for hardening is the permission to look.

This post is published under the same constraint as the rest of our work: we analyse structure; we do not name people. Every pattern referenced here is at the trope level. Specific brands, channels, and teachers exist in the wild, but they are not what we examine. The patterns are what we examine. The patterns are the artefact.

## What's Next

Three things are in flight on this material.

- A Japanese-language briefing — **[Briefing #006: あなたのビジネスは他人を操る道具になっていないか？](https://note.com/ohoran/n/nea98458f14ae)** — that walks five field-observable signals through the same framework, in a more personal and provocative register for creators who want to audit their own stream this week. Now live on `note.com/ohoran`.
- The [Quick-Check Skill](https://github.com/lemur47/si-protocols/blob/main/skills/si-quick-check/SKILL.md), already deployable, that scores the structural questions above.
- A book section consolidating this material as part of the broader cognitive-warfare and manipulation analysis. We'll link to it from here when it lands.

If you build at the boundary between AI tooling and spiritual content — or if you create in that space and would like a structural second opinion on your outbound stream — we welcome the contact.

---

*si-protocols is MIT-licenced. We analyse structure, not people.*
