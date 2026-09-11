# The hand-in pipeline — from inbox to a message the team can be sent

*Design note, 11 September 2026. Companion to [`prd-socratic-gate.md`](prd-socratic-gate.md),
which says what the gate must do, and to [`socratic_agent/intake.py`](socratic_agent/intake.py),
which already does the first step of what is described here. Nothing below is built yet beyond
that script.*

**Not for `site/`.** The pipeline handles student work and carries the scoresheets from the
quality manuals, which are instructor material under the publication rule in `CLAUDE.md`. The
files it produces live outside the repository altogether — see §2.

---

## 1. What this is for, and what it is not for

Two kinds of hand-in reach the teaching team, and they arrive by different doors.

- **The weekly handbook page, weeks 2–6**, is handed in by being published (ADR-0013 route 2).
  The gate pulls it from its URL on a schedule (ADR-0014, ADR-0015) and there is no submission
  step. `run_week.py` is that path, and this note does not change it.
- **Documents** — the AEL process artefacts, a different one each week — cannot be pulled,
  because there is nothing to pull. They arrive in the team's Teams channel (route 3) and a
  lecturer moves them into an inbox. This note is the path from that inbox onwards, **and it
  runs every week of the module.**

The inbox is therefore not a fifth hand-in route and gives the student nothing new to do. The
student's action is still "post it in the channel". If the inbox is ever wanted for the weekly
pages as well, that partly supersedes ADR-0014 and needs a record of its own; it is not decided
here.

### 1.1 What comes in, week by week

One document a week, six weeks, each scored against its own manual and checked against
everything handed in before it:

| Week | Hand-in | Deliverable id | Scored against | Checked against |
|---|---|---|---|---|
| 1 | PRD v0 | `prd` | `prd-quality-manual.md` | — |
| 2 | Technical blueprint | `blueprint` | `blueprint-quality-manual.md` | PRD |
| 3 | Knowledge architecture — where sources, drafts and pages live | `knowledge` | `knowledge-quality-manual.md` | blueprint (the components it serves), PRD B4 (sources and data) |
| 4 | Build plan — phases, tasks, test gates | `buildplan` | `buildplan-quality-manual.md` | blueprint (every component built), knowledge (built where the sources are), PRD C1–C3 (every gate tests a named quality) |
| 5 | Evaluation of the first artefact the platform produced, **with the decision log** | `eval`, `decisions` | `eval-quality-manual.md`, `decisions-quality-manual.md` | eval: PRD C1–C3 and the build plan's gates — measured against the bar the team set itself; decisions: every entry answers a failure, a gate, or a change to an earlier document, and every change to an earlier document has an entry |
| 6 | Evaluation of the second artefact | `eval` (v2) | `eval-quality-manual.md` | eval v1 (same criteria, and what moved), PRD, and the decision log for what changed between the two |

Only the PRD manual exists. The other five are written one week ahead of the hand-in they
score, in the shape of the PRD manual (§3, step 2).

This is ADR-0010's spine with its harness column folded into the hand-ins: the knowledge
architecture is that record's week-3 element and the first entry of its decision log, the two
evaluations are its eval config put to work on real output, and the decision log arrives as a
document in week 5 rather than being opened in week 3. The run is adaptive (course outline);
if a week moves, this table and the record move together.

Two properties of the documents shape the pipeline:

- **They are living.** ADR-0010: one page each, version-bumped weekly. A team may hand in a
  revised PRD in week 2 beside its blueprint, and often should, because the blueprint changes
  what the PRD can promise. The pipeline therefore scores *the latest version of every
  document*, not only this week's new one.
- **They must agree with each other.** A blueprint that builds what the PRD does not ask for,
  or a build plan whose test gates test nothing the PRD calls quality, is the failure the
  document spine exists to catch. From week 2 on, coherence is a check of its own (§3, step
  2b), over whichever documents exist by then. By week 6 that is the whole set.

## 2. Where the files live

Outside the repository, as a sibling of it — `intake.py`'s default already:

```
~/Documents/HAN/M3DM/ai-in-business-intake/
  roster.tsv                      team-NN → first names, Teams channel; the only file that links the two
  inbox/                          the lecturer drops files here
  teams/
    team-03/
      register.tsv                the question ledger, one line per question ever asked
      documents.tsv               which version of each deliverable is current, and where it is
      week-01/
        team-03-week-01-prd-original.pdf     as received, never edited
        team-03-week-01-prd.txt              plain text, derived from the original
        owners/score-prd.md                  the scoresheet — never forwarded
        team/questions.md                    the questions, as the agent wrote them
        team/message.md                      the message to the team, ready to send
      week-02/
        team-03-week-02-blueprint-original.docx
        team-03-week-02-blueprint.txt
        team-03-week-02-prd-original.pdf     a revised PRD, if one came in
        team-03-week-02-prd.txt
        owners/score-blueprint.md
        owners/score-prd.md                  only if a revision came in
        owners/coherence.md                  the cross-document check
        team/questions.md
        team/message.md
  log.tsv                         what moved where, when, from which inbox name
```

Four rules carried by the layout rather than by memory:

- **Teams are numbered, not named.** `team-NN` is the identifier everywhere: folders, file
  names, prompts, reports. First names live in `roster.tsv` and nowhere else. The agent is never
  given personal data (`agent.py`'s own description), and a folder named after four students
  puts their names into every path that reaches a prompt. Teams also change composition;
  numbers do not.
- **Every file names its deliverable.** `prd`, `blueprint`, `knowledge`, `buildplan`, `eval`,
  `decisions` — the same ids as `intake.py --deliverable`. A week can hold several, and the coherence check
  finds them by id, not by week.
- **Two audiences, two folders.** `owners/` holds what only the module owners see; `team/`
  holds what may be forwarded. The same split as `run_week.py`'s `-for-the-owners` and
  `-for-the-team`, and for the same reason: the one unrecoverable mistake is the rubric
  reaching a student, and a folder boundary is harder to cross by accident than a file suffix.
- **The original is never overwritten.** A second hand-in of the same deliverable in the same
  week is `-v2`, `-v3`; the later steps take the highest version. `-original` means *as
  received*, not *the only one*.

`documents.tsv` is the team's table of contents: one line per deliverable id with the week and
file of its current version. Step 1 updates it; steps 2b and 3 read it to find "the latest
PRD" without guessing from folder names.

## 3. The steps

One script, four steps, each of which skips work whose output already exists. That makes the
whole run restartable: a step that fails is re-run, and nothing before it is repeated. The
"signal" from one step to the next is the existence of the file the previous step writes —
there is no queue and no status to keep anywhere else.

The week is given explicitly (`--week 2`). Deriving it from the date against the module
calendar would save an argument and cost a wrong week now and then, which is worse.

### Step 1 — intake: inbox → the team's week folder

For each file in `inbox/`:

1. Work out the team **and the deliverable**. `intake.py`'s `guess_team()` reads the team from
   the file name; the deliverable is guessed the same way (`blueprint`, `bouwplan`, `build
   plan`…) and both are corrected by the lecturer in the manifest where the guess is empty or
   wrong. A file with no team or no deliverable **stays in the inbox** and goes no further
   until someone fills them in. The agent never guesses either from the document's content.
2. Move the file to `teams/team-NN/week-NN/team-NN-week-NN-<deliverable>-original.<ext>`, or
   `-vN` if one already exists. A move on one filesystem is atomic, so the move is its own
   test; a hash before and after is the belt to that pair of braces, and cheap. Append a line
   to `log.tsv` and update `documents.tsv`.
3. Convert the moved file to `.txt` **from the team folder**, not from the inbox. `intake.py`
   currently regenerates `text/` from `inbox/`, which stops working the moment the inbox is
   emptied; that is the one change the script needs.

Anything the converter cannot read is named in the output, as `intake.py` already does. A
hand-in that vanishes between inbox and run is the failure nobody notices.

### Step 2 — score: one scoresheet per document, against that document's manual

Runs for every `<deliverable>.txt` in the week folder that has no `owners/score-<deliverable>.md`.

**The agent reads the manual for that deliverable at the start of every run, from its path in
the repository, before it reads the document.** For the PRD that is
[`prd-quality-manual.md`](prd-quality-manual.md): Part 2 (the criteria), §3.1–3.4 (scale,
invariants, sheet, bands) and the instruction block in §3.5, applied as read. The blueprint
and build plan manuals follow the same shape — what the book says, the criteria mapped to the
assignment, the sheet and the agent's instructions — so the pipeline treats them alike.
Nothing from a manual is copied into the skill, the prompt or the script: the manuals are
edited as insight accumulates, and a copy is a second version that drifts the first time the
original changes. The skill's own text is one line long on this point — *read the manual
first, in full, every time* — and the criteria are wherever the manual says they are.

**No manual, no score.** A deliverable whose manual does not exist in the repository is
reported as *unscored: no manual for `blueprint`* and the step moves on. The agent does not
improvise criteria, because an improvised sheet cannot be compared with next week's, and a
score the manual did not define is a number nobody can defend to a student.

Two consequences of manuals that change:

- **Every scoresheet records which manual scored it.** The first lines carry the manual's git
  commit (the short hash of the last commit that touched the file) and the date, or
  *uncommitted* plus a content hash while it has not been committed. Without this, a score of
  38 in week 1 and 41 in week 3 cannot be told apart from a manual that moved by three points
  in between. The PRD manual is currently untracked; committing it is what makes the hash mean
  something.
- **A previous scoresheet is an input, as §3.5 already says.** Where the same deliverable comes
  in again — a revised PRD in week 2 — the previous `score-prd.md` is passed along, and the
  agent says per changed item what on the page changed it. If the manual changed between the
  two, the agent is told so, and says which movements are the page and which are the ruler.

The output is what §3.5 specifies: `## RETURNED` with the invariant and the sentence, or
`## SCORESHEET` with the table, total and band, and `## BEFORE V1` with the three items to
revise first. These files are the owners' half. They are never forwarded and never given to a
student, in any week.

### Step 2b — coherence: do the documents describe one platform?

Runs from week 2, after step 2, wherever the team has at least two deliverables in
`documents.tsv` and this week's `owners/coherence.md` does not exist. The rows below are
exercised as the documents arrive: PRD ↔ blueprint in week 2, the knowledge rows in week 3,
the build-plan rows in week 4, the evaluation and decision-log rows in weeks 5 and 6. The
"Checked against" column of §1.1 says which rows a given week runs. Inputs: the **latest**
text of every deliverable the team has handed in so far — from `documents.tsv`, not from this
week's folder — and a coherence manual, `coherence-quality-manual.md`, read fresh like the
others. That manual is *to be written*; what follows is what it has to contain.

The check is traceability in both directions plus contradiction, and it is a check of the
set, not of any one document:

| Direction | Question | Finding |
|---|---|---|
| PRD → blueprint | Does every functional requirement (B2) and every constraint (D1) land somewhere in the blueprint? | **Orphan requirement**: promised, not designed |
| Blueprint → PRD | Does every component in the blueprint answer to something the PRD asks for? | **Unasked-for component**: designed, not promised — scope creep, or a PRD that is out of date |
| Blueprint → knowledge | Does every component that reads or writes sources, drafts or pages have a place in the knowledge architecture to read from or write to? | **Homeless component** |
| Knowledge → PRD | Does the architecture hold the sources and data the PRD names (B4), and nothing the PRD rules out (D1, E1 — interview material above all, per NFR-11)? | **Unhoused source**, **forbidden store** |
| Blueprint → build plan | Is every component built in some phase? | **Unbuilt component** |
| Build plan → PRD | Does every test gate test a quality the PRD names (C1–C3)? Does any phase build what the PRD excludes (E1)? | **Untethered gate**, **excluded scope built** |
| Eval → PRD, build plan | Is the artefact judged against the PRD's own quality criteria and threshold (C1–C2), by the gates the build plan promised? Or against a bar invented for the occasion? | **Moved goalposts** |
| Eval v2 → eval v1 | Same criteria, same measure, and a stated reason for every difference? | **Incomparable evaluations** |
| Decisions → everything | Does every entry name the failure, gate or earlier document it answers? Does every change to an earlier document since its scored version have an entry? | **Unmotivated decision**, **unrecorded change** |
| Across all three | Do the numbers, names, users and thresholds agree? Same target SME, same threshold for "good enough to publish", same source set? | **Contradiction**, each with the two quotes that disagree |
| Open questions (F2) | Has each PRD open question been answered by the blueprint, carried forward, or silently dropped? | **Dropped question** |

Output, under `## TRACE`, the matrix — one row per PRD requirement, with the blueprint element
and build-plan phase that carry it, or NONE — and under `## FINDINGS` the orphans,
contradictions and dropped questions, each with quotes from the documents concerned, in the
team's own words. Scored 0–3 per direction on the same scale as the manuals, so the owners see
at a glance whether the set is one platform or three documents. Like the other scoresheets,
this one stays in `owners/`.

Because the documents are living, an orphan is not always a defect in the newer document: a
blueprint that drops a PRD requirement may be right, and the PRD wrong. The finding says what
disagrees and quotes both sides; which side moves is the team's decision, and a question for
step 3.

### Step 3 — question: the Socratic agent writes the register and the message

Runs where every scoresheet due this week exists (including `coherence.md` from week 2) and
`team/questions.md` does not. Four inputs, in this order:

1. **The register**, `register.tsv`, filtered to this team's questions with status *open*,
   *partly* or *ducked*.
2. **This week's documents**, as text — every deliverable handed in this week, and for the
   coherence questions the latest versions the check ran on.
3. **The qualitative columns only** of every scoresheet written this week — *weakest evidence*
   and *what would raise it by one* from each `score-*.md`, and the `## FINDINGS` section of
   `coherence.md` — and **not** the scores, totals or bands of any of them. This is the one
   design choice in the note that matters most. The Socratic agent's questions are shaped by
   the rubrics, which is the design; but if it never sees a number, it cannot leak one.
   `run_week.py`'s docstring names exactly this route — a history carrying last week's score
   into this week's questions — as the way the rubric ends up in the student channel by the
   back door. Keep the numbers out of its context rather than asking it to keep them out of
   its mouth.
4. The instructions in `socratic_agent/instructions.txt`, which already say: never ask a
   question they have answered, and ask a ducked one again, harder.

Coherence findings make the best Socratic questions the pipeline has, because they need no
rubric to be fair: *the PRD promises the reader a source list on every page; where in the
blueprint does the source list come from?* is a question the team can answer from its own
documents, and cannot answer by polishing one of them.

Four outputs:

- **The register, updated.** Each open question is checked against this week's documents and
  its status set, with the quote that carries the decision. Then the new questions are
  appended, each tagged with the deliverable it is about, or `coherence`.
- **`team/questions.md`** — three to five questions, nothing else, as the instructions require.
  Across all of this week's documents, not three to five per document.
- **`team/message.md`** — the questions wrapped in the fixed opening and closing the team
  always gets, ready to paste into the channel.
- A one-line summary to the terminal per team: status changes in the register, and the count
  of new questions.

A small check runs over `team/message.md` before the step reports success: no item codes
(`A1`…`G2`, and their equivalents in the other manuals), no `/60`, no band names, no *score*.
It fails the step rather than warns, because the file it guards is the one that gets sent.

## 4. The register

One file per team, one line per question ever asked. This is what `instructions.txt` currently
does by reading prior reports as prose, made checkable — and it is what AC-06 needs at the
interview, where a student is asked to name a question that changed their work.

| column | holds |
|---|---|
| `id` | `team-03-w02-q2` |
| `asked` | week number |
| `about` | `prd` · `blueprint` · `knowledge` · `buildplan` · `eval` · `decisions` · `coherence` |
| `question` | the text as sent |
| `status` | `open` · `answered` · `partly` · `ducked` · `withdrawn` |
| `resolved` | week number, or empty |
| `evidence` | the quote from the document that carries the status |

Two rules, or the register is fifteen open questions long by week 4:

- **At most five open questions per team.** More than that and the team cannot tell which ones
  matter, and the agent cannot either.
- **Every older open question is either re-asked or withdrawn** when a new set is written. A
  re-asked question keeps its `id` and gets a harder wording; a withdrawn one gets the reason
  in `evidence`. Nothing stays open by default.

A question about a living document is answered in whichever version comes next. A week-1
question about the PRD's threshold (C2) may be answered by the week-2 blueprint rather than by
a revised PRD; the `evidence` column names the document the answer was found in.

Quotes from student work go into the register, so the register is student material and stays
outside the repository with everything else here.

## 5. Decided for now, and open

Two things were decided on 11 September 2026 as *for now*, and both are reversible:

- **The lecturer sends the message.** Step 3 writes `team/message.md`; a person pastes it into
  the team's Teams channel. Automating that post is a separate decision, and `run_week.py`'s
  argument for keeping it a deliberate act still stands: forwarding the wrong file should take
  effort.
- **The register stays local**, in the intake folder on the lecturer's machine. The interview
  is months away and ADR-0013 says where archival copies of examination evidence go (HANDIN,
  route 1; Teams storage, route 4). Where the register goes at the end of the run, and whether
  a team ever sees its own register, are both open.

**Manuals, one week ahead of the hand-in they score**, or the pipeline reports *unscored*:

| Before week | Write |
|---|---|
| 2 | `blueprint-quality-manual.md`; `coherence-quality-manual.md` with at least the PRD ↔ blueprint rows of step 2b |
| 3 | `knowledge-quality-manual.md`; the knowledge rows of the coherence manual |
| 4 | `buildplan-quality-manual.md`; the build-plan rows |
| 5 | `eval-quality-manual.md` and `decisions-quality-manual.md`; the evaluation and decision rows |
| 6 | nothing new — the eval manual gains a section on comparing v2 with v1, if it does not already have one |

Each in the shape of the PRD manual: what the source says, the criteria mapped to the
assignment, the sheet, the instruction block. The assignment text for each week has to exist
before its manual can map criteria to it.

Still open, and not decided here:

- Whether the inbox path is ever used for the weekly pages (see §1).
- What the scoring agent does with a document that fails an invariant — return it to the team
  with the reason, which the manual says, or hold it for the lecturer first.
- How the second module owner runs this, given the intake root is a path on one machine.
- Whether a revised PRD in week 2 is *required* when the blueprint changes what it promises, or
  merely allowed. ADR-0010 says the decision log is where PRD changes are recorded; that log
  opens in week 3, one week after the first reason to change the PRD.
