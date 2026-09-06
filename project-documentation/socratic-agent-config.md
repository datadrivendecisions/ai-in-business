# The Socratic agent — registered configuration

The three fields as they are entered in the Gemini Enterprise Agent Platform console, kept here so
the agent's configuration is in the repository rather than only in one person's console. Requirements
are in [`prd-socratic-gate.md`](prd-socratic-gate.md); architecture is
[ADR-0014](../work/decisions/0014-socratic-gate-architecture.md).

**This file may not enter `site/`.** The Instructions field below contains the hidden rubric and its
thresholds — tier-1 instructor material under the publication rule in `CLAUDE.md`. A student who reads
it can write to the rubric instead of to the work, which is the one failure the gate has no defence
against. `project-documentation/` is off the site; this is a public repository, so this file is the
outer limit of where the rubric may live, and it should not be quoted into anything student-facing.

Edit here and paste into the console, not the other way round. Under FR-10 no student holds write
access to any of it.

---

## Name

```
Socratic Gate (pilot)
```

The console currently holds `Socratic Reviewe` — a truncation of *Socratic Reviewer*, missing its
last character. Worth changing for a second reason: the agent's own name sits in its context, and a
model called *Reviewer* drifts towards reviewing. Passing a verdict is what the four invariants
forbid, so the name should not spend the instructions' budget arguing against itself. *Pilot* stays
in the name until the output has been checked by hand against the owners' own reading (LRD Part 12),
so that a test report cannot be mistaken for a live one.

## Description

Purpose and capabilities — what routing and agent discovery read. Deliberately short; behaviour
belongs in Instructions.

```
Asks a student team Socratic questions about the thinking behind the handbook page
they published this week. Takes one published page URL plus that team's earlier
reports; returns questions to the team, and a process-rubric score with an
open/closed gate signal to the two module owners. One run per team per teaching
week, weeks 2–6. Never given transcripts or personal data. Pilot instance.
```

## Instructions

The system prompt lives in [`socratic_agent/instructions.txt`](socratic_agent/instructions.txt),
which is the single copy: [`socratic_agent/agent.py`](socratic_agent/agent.py) reads it at import,
and the console field is pasted from it. Do not keep a second copy here — there is no generator to
hold two in step, and a prompt that has drifted from what runs is worse than no record of it.

## Running it as code

Agent Designer's *Get code* produces an ADK project, and moving to it settles three of the four
platform limits in one step: the thinking budget becomes a parameter, output routing becomes
ordinary Python, and — the one that matters — the page can be fetched properly.

The console version wrapped `url_context` in an `LlmAgent` and passed it as a tool. That is a second
language model, so it read the page and wrote its own account of it; the summary that came back had
dropped the source list, and the gate scored a page it had never seen (run 4). `fetch_page` in
`agent.py` is a plain function: it returns the team's own words and their own source list, with
every link kept inline.

Search stays wrapped as an agent tool, because a summarised search result is fine — all that is
asked of it is whether a work exists.

```
adk web        # from project-documentation/, then open the printed URL
```

## Running a week

[`socratic_agent/run_week.py`](socratic_agent/run_week.py) takes a roster of teams and writes two
files each — see [`socratic_agent/roster-example.tsv`](socratic_agent/roster-example.tsv) for the
format, which is `team<TAB>url<TAB>[prior report]`.

```
cd socratic_agent
set -a && . ./.env && set +a
python run_week.py roster.tsv --week 2 --out ../gate-reports
```

It prints a table — scores, gate signal, ledger flags, one line per team — and writes
`<team>-for-the-team.md` and `<team>-for-the-owners.md`. **Only the first may be forwarded.**
Nothing is sent anywhere by the script: forwarding is a person's job, because the one unrecoverable
mistake in this system is the owners' half reaching a student, and it should take a deliberate act.

It retries a team twice on an empty response, in a fresh session each time — one run in twelve came
back empty during the pilot with no error — and exits non-zero naming any team it could not produce
a report for. That exit code is the weekly confirmation the PRD asks for.

**Why this is a script and not a page on the site.** A tool that calls the agent needs a key and a
network call. `site/` is a public URL from a public repository; its tool exception allows JavaScript
only for pages that are self-contained and make no network calls; and the instructor view is
signposting rather than access control, so "instructor-only" is not a property a page there can
have. The rubric is tier-1 material and may not enter `site/` in any form. ADR-0014 weighed this as
option B and declined it; a front end would need a record that supersedes or extends it, not a page
that quietly contradicts it.

---

## Notes on the choices above

**The two audiences are split structurally, not by trust.** One model call produces both parts, so
the only thing standing between a student and the rubric is the workflow that forwards Part 1 and
withholds Part 2. That split is the single most likely place a pilot leaks, and it is worth testing
before anything else: run it once, and confirm that what reaches the channel starts at
`## FOR THE TEAM` and ends where Part 2 begins.

**The thresholds are a first guess.** Movement ≥ 2 and total ≥ 6 out of 12 have no evidence behind
them yet. LRD Part 12 asks for a hand-graded pilot precisely so that the threshold is calibrated
against real pages rather than assumed; expect to move it after week 2.

**"Never helps" is in the first line on purpose.** Helpfulness is the strongest default an
assistant model has, and every invariant here is a refusal of it. Stating the refusal once at the
top does more work than the individual prohibitions that follow.

**What is not configured here.** The schedule, the roster of team page URLs, the destinations for
each part, and the spend cap are workflow and project settings rather than agent fields. They are
open items in the PRD's §6 and need answering before week 2.
