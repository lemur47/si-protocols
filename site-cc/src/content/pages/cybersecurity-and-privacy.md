---
title: Cybersecurity and Privacy
description: Why privacy-first design matters for tools that analyse personal spiritual content.
order: 5
---

## Why Privacy Matters Here

Spiritual content is deeply personal. The texts you might want to analyse — messages from a teacher, group communications, personal journal entries, content from online communities — reveal intimate details about your beliefs, vulnerabilities, and social connections.

Any tool that analyses this content must treat it with the same care as medical or financial data. This is not optional. It is foundational.

> "A tool that claims to protect you whilst sending your spiritual journal to a cloud server has missed the point entirely."

## Our Privacy Principles

The SI Protocols tool is designed around three core principles:

### Local-only processing

All analysis runs on your machine. Your text is never sent to external servers, never stored in cloud databases, never processed by third-party APIs. The NLP pipeline (spaCy) runs locally. The scoring algorithms run locally. Nothing leaves your device.

This is not a limitation — it is a deliberate design choice. We believe that tools for spiritual discernment must be private by architecture, not merely by policy.

### No data collection

The tool collects no usage data, no analytics, no telemetry. We do not know who uses it, how often, or what they analyse. This means we cannot optimise for engagement metrics — and that is exactly the point. Engagement optimisation is one of the patterns we are trying to help people recognise.

### Open-source transparency

Every line of code is available for inspection. The marker lists — the words and phrases the tool looks for — are published and documented. The scoring weights are fixed and visible. There is no proprietary algorithm making hidden judgements about your content.

If you disagree with a marker or a scoring weight, you can see exactly what it is, understand why it is there, and modify it for your own use. This level of transparency is only possible with open-source software.

## Digital Threats in Spiritual Spaces

Beyond the content analysis tool itself, spiritual seekers face specific digital threats:

### Data harvesting by spiritual platforms

Many online spiritual platforms — astrology apps, meditation services, channelling communities — collect extensive personal data. Birth dates, locations, emotional states, relationship details, and health information are routinely gathered through "personalisation" features. This data can be:

- Sold to data brokers
- Used for targeted advertising
- Exploited for more precise manipulation
- Exposed in data breaches

### Social engineering

Spiritual communities, especially online ones, can be vectors for social engineering. Members who share personal details in the context of spiritual growth may inadvertently provide information useful for:

- Financial fraud (life details shared during "readings")
- Identity theft (birth dates, full names, locations)
- Targeted phishing (knowing someone's spiritual interests enables highly convincing lures)

### Platform dependency

When spiritual communities exist solely on commercial platforms (social media, proprietary apps), they are subject to algorithm changes, data policies, and platform shutdowns beyond their control. Decentralised and self-hosted alternatives provide more resilience.

## Practical Recommendations

- **Run tools locally** whenever possible. If a spiritual tool requires cloud processing, understand exactly what data it sends and to whom.
- **Review permissions** on spiritual and wellness apps. Do they really need access to your contacts, location, or health data?
- **Use separate accounts** for spiritual communities if you want to maintain boundaries between your spiritual exploration and other aspects of your digital life.
- **Be cautious with personal details** shared in group settings, even in trusted communities. Information shared spiritually can be exploited mundanely.

The SI Protocols tool is one small part of this larger picture — a local, transparent, open-source tool that respects your privacy whilst helping you navigate complex spiritual content.

Beyond the threat score, the tool can also [map the claims and patterns](/mapping-claims-and-patterns/) within a text — showing you not just *how much* manipulation is present, but *where* it lives and how the pieces connect.

Visit the [developer site](https://spiritualintelligence.dev) to explore the technical documentation and contribute.
