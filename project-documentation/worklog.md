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
   python3 .github/scripts/worklog.py book     # record what has been counted
   python3 .github/scripts/worklog.py verify   # the header still adds up
   ```

   `hours` reads the transcripts on your own laptop and reports what is missing from this
   file. Add a row per working day and update the total, then run `book`, which writes the
   figures into the `worklog:booked` comment at the foot of this file so nothing is counted
   twice. `book` stores minutes against each session id rather than the id alone, so a
   session booked while the conversation is still open gets topped up next time instead of
   losing its tail. `verify` runs anywhere, including CI, and fails when the total above no
   longer matches the rows below.

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

Total recorded: **8.65 h** over 3 working days, from 13 September 2026.

## Checks register

What has been inspected, when, and what was concluded. A verdict here stands until someone
supersedes it with a new row.

| Target | Check | Date | Verdict |
|---|---|---|---|
| All of `site/` | `strip-ai-language`, A-codes | 15 Sep 2026 | 247 findings, of which **125 were already closed** by the rows below and 11 are the em-dash norm. Of the 111 left, **six were rewritten** and the rest keep their contrast, which on these pages is usually the content: *informational, not scored* and *questions, not feedback* stop meaning anything without the negated half. Rewritten: the Draghi paragraph on `index.html` (it corrected a misreading nobody on the page had voiced, so it now states the positive fact), *not one after the other* and a demonstrative *That is why* on `week-01.html`, two hollow uses of *actually* on `week-02.html`, the *founding the company again* image on the blueprint tool (the sentence before it already gave the mechanism), and a restating closer on card 12 of the week-2 slides. |
| Student pages | `strip-ai-language`, D1 and D3 | 15 Sep 2026 | **Measured and left open: 68 sentences over 25 words** (26 on `index.html`, 16 on `week-01.html`, 13 on `prd-criteria.html`, 7 on `handbook.html`, 6 on `week-02.html`) and one unexplained term, *framework* in a `prd-criteria.html` list of implementation detail the reader is told to leave out. These are reader-fit rather than machine-written prose, and rewriting 68 sentences changes the course's voice, which is the module owner's call. |
| `project-documentation/slides/week-0*-notes.md` | `strip-ai-language`, A-codes | 15 Sep 2026 | **12 findings, all left.** A lecturer's spoken script for an audience of one who wrote it; every contrast mirrors a distinction taught on the page, and a demonstrative closer is ordinary emphasis in speech. |
| `site/week-02-slides.html` | `slidewords.py` | 15 Sep 2026 | **Open: 7 of 15 cards over the 40-word body limit**, card 13 also over the three-bullet limit. Pre-existing and untouched by the prose pass, which took card 12 from 55 words to 53. |
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
| 2026-09-15 | Witek | 2.25 | `worktree-prose-pass-and-worklog` | Built this worklog: the checks register, the sessions ledger, `worklog.py` and the CI job that refuses a total which stops matching its rows. Then ran the prose pass that prompted it across every page of `site/`, rewriting six constructions and recording the verdict on the rest. Rebuilt the week-2 presenter deck, PDF and PPTX from the edited card page. The pull request could not be opened: GitHub returned 502s and empty bodies from both the GraphQL and REST create paths while its reads stayed up. |
| 2026-09-14 | Witek | 5.22 | `collaboration-guardrails`, `week-03-*` | Put the pull-request route behind a ruleset on `main` that refuses a direct push, and wrote the merge-conflict agreement into `CLAUDE.md` and `SAMENWERKEN.md`. Designed the week-3 experiment on biased information seeking and specified the browser tool that runs it, then moved its result collection to a service and costed it. |
| 2026-09-13 | Witek | 1.18 | `main` | Published the session slides as one page of cards per slide, generated the presenter decks from those cards, and rebuilt the week-2 page around the session as the deck now runs it. Gathered everything written to build the system into `project-documentation/build/`. Landed phase 6 of the hand-in pipeline. |

<!-- worklog:booked
8cea137b:69.9
aef50e82:0.6
a470a9b9:0.8
75bf4d92:0.7
12e6427b:1.3
26636e49:311.5
37c8f1e5:44.7
6578e10f:21.6
8a19ba30:22.5
cfe0144c:1.2
277f19c6:39.3
22cf3541:1.1
9bd6a79e:1.1
680da1a9:0.9
32e9dcd6:0.9
c6b21fc3:1.2
-->
