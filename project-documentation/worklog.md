# Worklog

What has been done to this repository, what has been *checked*, and how long it took.
Newest entry first.

`lrd-logbook.md` does this for one document. This file does it for the project, and it
exists because of something that happened on 15 September 2026: a prose check was run
across the whole site, and 125 of its 247 findings turned out to have been reviewed and
deliberately kept nine days earlier. The reasoning was written down both times — once in
the LRD logbook, once in a skill file — and an agent starting fresh found neither. Work
that has already been judged should be findable in one place before anyone repeats it.

**Read the checks register first.** If the thing you are about to inspect is already in
it, read the verdict before you start.

## How to add to it

1. **A substantive change** — a page published, a document rewritten, a decision taken —
   gets a row in the sessions ledger.
2. **Every check that runs** gets a row in the checks register, *including the ones that
   find nothing*. A clean result is the row that saves the next person an afternoon. A
   finding you looked at and decided to keep is worth more still: write down why, because
   the check will report it again next time.
3. **The hours come from the Claude Code transcripts**, never from memory:

   ```bash
   python3 .github/scripts/worklog.py hours    # what is not yet booked
   python3 .github/scripts/worklog.py verify   # the header still adds up
   ```

   `hours` reads the transcripts on your own laptop and reports the sessions missing from
   this file. Add a row per working day, then list the session ids in the `worklog:booked`
   comment at the foot of this file so they are not counted twice. `verify` runs anywhere,
   including CI, and fails when the total above no longer matches the rows below.

**How the hours are measured.** Active time: the gaps between consecutive messages in a
session, each gap capped at **15 minutes**. A session's first-to-last span was the obvious
measure and it is wrong — two September sessions span eighteen and twenty-two hours because
the window stayed open overnight, which booked 41 hours against a fortnight holding about
six. The cap moves the figure (5 minutes gives 4.4 h, 30 minutes gives 8.5 h over the same
transcripts), so it is fixed at 15 and named here.

**What is not counted.** Anything done away from Claude Code — reading, teaching, marking,
thinking on the train. Transcripts begin on **13 September 2026**; the repository begins on
**2 June 2026**, and the hours of those first three months were never measured. They are
absent rather than estimated.

---

Total recorded: **6.40 h** over 2 working days, from 13 September 2026.

## Checks register

What has been inspected, when, and what was concluded. A verdict here stands until someone
supersedes it with a new row.

| Target | Check | Date | Verdict |
|---|---|---|---|
| `site/integrated-lrd.html` | `strip-ai-language`, A-codes | 6 Sep 2026 | Eight uses of *actually* and two demonstrative echoes removed. **The 120 A1 antitheses are deliberate and stay** — ruling out a wrong reading is what a specification does, and *the team's tool, not the handbook's precondition* loses its meaning without the negated half. Three uses of *actually* stay for the same reason. Reasoning in `lrd-logbook.md` v1.8. |
| The five published pages, 24,034 words | AI vocabulary word list, 42 terms | 6 Sep 2026 | **Four hits, all four fair.** The word-list method finds nothing here; the antithesis is the form this site actually produces. Recorded in `.claude/skills/strip-ai-language/SKILL.md`. |
| `site/` | `strip-ai-language` A4, A5, A7 | 6 Sep 2026 | **Five findings, all five kept.** *Regional ecosystem* is the name of a real thing, *unlock* describes a gate that is literally locked, *either way* fell mid-sentence rather than at the end. |
| `site/tool-ai-worker-maturity.html` | all prose checks | standing | **Out of scope.** Reproduced from the AI Wiki and maintained there; its footer says so. Do not edit its prose here. |
| Em-dash density (A10) across `site/` | `strip-ai-language` A10 | standing | **House style.** Every page trips it and every page is meant to. `CLAUDE.md` settles this; it does not need deciding again. |
| Every relative link in the repo | `check-links.sh` | every push and PR | Green. Runs in CI, so it needs a row here only when it finds something. |
| `work/decisions/` | `check-adrs.sh` | every push and PR touching it | Green, 15 records. |

## Sessions ledger

| Date | Who | Hours | Branch | What happened |
|---|---|---|---|---|
| 2026-09-14 | Witek | 5.22 | `collaboration-guardrails`, `week-03-*` | Put the pull-request route behind a ruleset on `main` that refuses a direct push, and wrote the merge-conflict agreement into `CLAUDE.md` and `SAMENWERKEN.md`. Designed the week-3 experiment on biased information seeking and specified the browser tool that runs it, then moved its result collection to a service and costed it. |
| 2026-09-13 | Witek | 1.18 | `main` | Published the session slides as one page of cards per slide, generated the presenter decks from those cards, and rebuilt the week-2 page around the session as the deck now runs it. Gathered everything written to build the system into `project-documentation/build/`. Landed phase 6 of the hand-in pipeline. |

<!-- worklog:booked
8cea137b aef50e82 a470a9b9
75bf4d92 12e6427b 26636e49
-->
