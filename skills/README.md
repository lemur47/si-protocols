# SI Protocols — Skills

Zero-install [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
that encode the SI Protocols detection methodology as standalone prompts. They
let anyone run an analysis in Claude — claude.ai, Claude Code, or the API —
without installing the Python toolkit.

Each skill follows Anthropic's official folder layout: a directory containing a
`SKILL.md` with YAML frontmatter (`name`, `description`) and the instructions in
the body.

## Available skills

| Skill | What it does |
|-------|--------------|
| [`quick-check/`](quick-check/SKILL.md) | Detects manipulation patterns in spiritual, metaphysical, and self-help text across seven dimensions plus a CVP consciousness-topology assessment. Auto-detects English or Japanese. Returns an approximate 0–100 threat score, a per-dimension table, quoted signals, and a structural assessment. **v0.3** (CVP-enhanced). |

> The skills are a lightweight companion to the full
> [SI Protocols toolkit](https://spiritualintelligence.dev) — an open-source NLP
> pipeline for detecting manipulation patterns in spiritual content. They run on
> Anthropic's infrastructure; SI Protocols never receives, stores, or has access
> to text you analyse. For fully local analysis, use the
> [CLI toolkit](https://github.com/lemur47/si-protocols).

## How to install

### claude.ai — upload as a project file (recommended)

1. Open [claude.ai](https://claude.ai) and create a new **Project**.
2. Click **Add content** and upload the skill's `SKILL.md` (e.g.
   `quick-check/SKILL.md`).
3. Paste any text into the chat to analyse it.

### claude.ai — paste into custom instructions

1. Create a new **Project** and open its **Custom Instructions** (the pencil
   icon).
2. Copy the body of `SKILL.md` (everything below the `---` frontmatter block)
   into the custom instructions and save.
3. Paste any text into the chat to analyse it.

### Claude Code

Copy the skill folder into `.claude/skills/` (project) or `~/.claude/skills/`
(personal):

```bash
cp -r skills/quick-check ~/.claude/skills/
```

Claude Code discovers it automatically; the frontmatter `description` decides
when it triggers.

### API

Upload the skill folder via the Skills API and reference it in your request.
See the [Skills guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide).

## Notes

- These are **distribution artefacts**, not the skills loaded into this repo's
  own Claude Code session (those live under `.claude/skills/`).
- Skills are approximate heuristics for human judgement, not verdicts on truth
  or harm. See each `SKILL.md` for guardrails.
