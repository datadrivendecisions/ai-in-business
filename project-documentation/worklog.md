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

Total recorded: **13.60 h** over 3 working days, from 13 September 2026.

## Checks register

What has been inspected, when, and what was concluded. A verdict here stands until someone
supersedes it with a new row.

| Target | Check | Date | Verdict |
|---|---|---|---|
| `site/tool-bias-experiment.html` | `check-measures.py` (new) | 15 Sep 2026 | **Green.** Ten measurement sessions, five classes of result lines, four kappa matrices. Every figure recomputed in Python from `work/drafts/week-03-codebook.md` and compared with the same figure produced by the shipped page's own code, which `runpage.mjs` evaluates outside a browser. The two implementations disagree in method where they can: scipy's `t.ppf` against a t quantile from the incomplete beta, and scipy's non-central t against the page's own Simpson integration of it. All matched to 3 dp. The power figure was checked a third way, against a 200,000-run simulation, which returned .8012 against a nominal .80. |
| `site/tool-bias-experiment.html` | `check-session.mjs` (new) | 15 Sep 2026 | **Green.** Whole sessions driven through the page's own code in a `node:vm` stub DOM. 20 fresh sessions gave 20 distinct orders, all 20 stored (`SM-2`, `SM-9`); the 9th open was refused 800 times out of 800 across 100 sessions (`SM-3`); the card index never fell (`SM-4`); one storage key, nothing written before consent, nothing left after erase (`DA-1`); all 8 teams met the assistant in the right round and before card 1, and none got past an empty paste box (`AG-3`); 5 cards timed to within 0 ms of the wall clock (`MS-5`). |
| `site/tool-bias-experiment.html` | `SM-8`, answer key in the shipped file | 15 Sep 2026 | **Two leaks found and fixed.** The check looks for cell codes, for card ids within 160 characters of a stance or quality word, and for a seventh field on any card record. It caught two pieces of *my own* interface text — a worked example reading `c1-01 NAS3` in a hint and in an error message, which is that card's real cell. Both replaced with a description of the format. This is the check most worth keeping: the leak was introduced by someone who knew the rule, while writing help text about the rule. |
| `site/tool-bias-experiment.html` | `check-prompt.py` (new) | 15 Sep 2026 | **Green.** The assistant prompt is built through the page's own `agentPrompt()` and run against a 48-phrase verdict list. It asks for four questions, names the claim and the locked sentence, carries none of the 48 phrases, and speaks of the position in the third person while addressing the student as *you*. The claim and the student's sentence are stripped before the list is applied: a claim contains *should* by construction. The prompt deliberately carries no list of banned words, which would put them in the prompt. |
| `site/tool-bias-experiment.html` | Real browser, full session and lecturer view | 15 Sep 2026 | **Green.** Two rounds end to end: 32 distinct cards, 8 question groups of 7 per round, unanswered questions and an empty paste box both refused, one storage key, a line that parses. **One network request across the whole session: the page itself** (`AG-1`). The lecturer view took a 15.8 KB paste of the codebook markdown and read 32 cards from it, accepted 32 lines, listed 3 malformed ones with reasons and skipped a blank without counting it, and rendered the question with both its governing numbers. `?instructor` reveals it, `?student` hides it again. |
| `site/tool-bias-experiment.html` | `strip-ai-language`, A-codes and D-codes | 15 Sep 2026 | **7 findings, 2 rewritten, 5 A1 kept.** The five kept are the contrast-is-content case this register already settled on 15 Sep: *about the round you have just finished, not about the claim* stops a student answering about the claim, *listed back rather than dropped* names the failure `AN-6` exists to prevent. Rewritten: one sentence carrying two antitheses at once, and a lecturer hint that ran to 30 words. 0 D-code findings afterwards. |
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
| 2026-09-15 | Witek | 7.20 | `worktree-prose-pass-and-worklog`, `week-03-decks-and-position-controls` | Built this worklog: the checks register, the sessions ledger, `worklog.py` and the CI job that refuses a total which stops matching its rows. Then ran the prose pass that prompted it across every page of `site/`, rewriting six constructions and recording the verdict on the rest. Rebuilt the week-2 presenter deck, PDF and PPTX from the edited card page. The pull request could not be opened: GitHub returned 502s and empty bodies from both the GraphQL and REST create paths while its reads stayed up. Then took the bias experiment tool from phase 1 to phase 5: the second round, the assistant step, the closing questions, the timings, the result line and the lecturer view that turns thirty-two of them into one paired comparison. Wrote the three checks that hold it — one of which caught an answer key I had put in my own help text. |
| 2026-09-14 | Witek | 5.22 | `collaboration-guardrails`, `week-03-*` | Put the pull-request route behind a ruleset on `main` that refuses a direct push, and wrote the merge-conflict agreement into `CLAUDE.md` and `SAMENWERKEN.md`. Designed the week-3 experiment on biased information seeking and specified the browser tool that runs it, then moved its result collection to a service and costed it. |
| 2026-09-13 | Witek | 1.18 | `main` | Published the session slides as one page of cards per slide, generated the presenter decks from those cards, and rebuilt the week-2 page around the session as the deck now runs it. Gathered everything written to build the system into `project-documentation/build/`. Landed phase 6 of the hand-in pipeline. |

<!-- worklog:booked
8cea137b:69.9
aef50e82:0.6
a470a9b9:0.8
75bf4d92:0.7
12e6427b:1.3
26636e49:311.5
37c8f1e5:45.8
6578e10f:167.8
8a19ba30:22.5
cfe0144c:1.2
277f19c6:135.3
22cf3541:1.1
9bd6a79e:1.1
680da1a9:0.9
32e9dcd6:0.9
c6b21fc3:1.2
b6650ce9:1.2
7bba867f:0.6
fc94e9a2:1.5
2bbec1a2:0.9
1f93dbcc:0.9
fd1e54ec:0.7
57e8a8d2:0.5
bc957735:47.5
-->
