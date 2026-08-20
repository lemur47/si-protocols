# Security Policy

Thank you for taking the time to look at this project's security. This document
says how to report something, and — just as importantly — what this project
actually is, so you can judge whether a finding belongs here.

## Reporting a vulnerability

**Please report privately, through GitHub:**

➡️ **[Open a private security advisory](https://github.com/lemur47/si-protocols/security/advisories/new)**

Private vulnerability reporting is enabled on this repository. That channel is
the only one we use — it keeps the report visible to the maintainers and to you,
and nowhere else, until there is something to publish.

**Please do not** open a public issue, a pull request, or a discussion for a
security problem. A public report is a disclosure, and it is not one you can
take back.

A useful report usually includes what you did, what happened, what you expected
instead, and the version or commit you were on. A proof of concept helps, but do
not feel you need one to tell us something looks wrong.

## Supported versions

**`main` only.**

There is no version table here, because a table would imply a support commitment
that does not exist. The project is at `0.1.0`, has no tagged releases, and is
not published on PyPI. Fixes land on `main`; there are no backports, because
there is nothing to backport to.

## What this project is — and what that means for scope

This matters more than usual here, because the shape of the project rules out
most of what a security report normally targets.

**The toolkit is local-only.** It runs on your machine, against text you give
it. It does not host anything, does not collect anything, and never sends your
text anywhere — with one deliberate exception, noted under *Data flow* below.

**Nothing is deployed.** The FastAPI application in `app/` binds to loopback and
is intended to be run by you, locally. There is no hosted instance, no
production environment, and no service operated by this project that could be
attacked.

**The former websites are gone.** `spiritualintelligence.dev` and
`spiritualintelligence.cc` are retired. Their content moved to `ohoran.org`, a
separate project, and the old domains are redirect shells that this repository
neither runs nor controls. **Findings against those domains are not in scope
here**, and neither are findings against `ohoran.org` itself.

**The skills are prompt files.** Everything under `skills/` is plain text
designed to be copied into your own Claude project. When you use them, they run
on Anthropic's infrastructure, under your account — not on ours.

### In scope

- The Python package under `src/`, and the `si-threat-filter` and `si-topology`
  entry points.
- The FastAPI application under `app/`, as shipped — for example, a request that
  crashes it, hangs it, or reads something it should not.
- Packaging and build metadata, including anything that would cause an install
  to fetch or execute something unexpected.
- The workflows and gate scripts in this repository, particularly anything that
  would let untrusted input influence what CI executes.
- The skill and ontology files published here, if their content could cause harm
  to someone who copies them as instructed.

### Out of scope

- Anything that requires us to be hosting a service. We are not.
- The retired domains above, and the separate website that replaced them.
- Third-party platforms the project merely names or interoperates with.
- Known vulnerabilities in dependencies that already carry an upstream advisory
  — please report those upstream. **Do** tell us if our pinning, our lockfile, or
  a suppression we have written is the reason you are exposed; that part is ours.
- Findings that depend on an attacker already having local access to the machine
  running the tool. At that point the tool is not the weakest link.

## Data flow, stated plainly

By default, no analysed text leaves your machine.

The one exception is opt-in and explicit: the topology analyser's Anthropic
engine (`--engine anthropic`) sends the text you are analysing to the Anthropic
API, authenticated with **your** API key, which you supply. It is not the
default, it does nothing unless you select it, and the maintainers receive
nothing. If you would rather nothing left the machine at all, use the default
local engine.

## What to expect

This is a small project without a dedicated security team, so please read the
following as honesty rather than indifference: **we do not offer a response-time
guarantee, and there is no bug bounty.** Reports are triaged on a best-effort
basis. We would still much rather hear from you than not.

If a report is valid, we will fix it on `main`, publish an advisory through
GitHub, and credit you — unless you would prefer we did not, which is entirely
your call.

## Good-faith research

We will not pursue or support action against anyone who reports a finding in
good faith through the channel above, who stays within the scope described here,
and who avoids privacy violations and data destruction while investigating.

Since there is no hosted service, almost all legitimate testing of this project
happens on your own machine, against your own copy. Please keep it that way.
