# Pipeline log — the document hand-in pipeline

One entry per gate run and per live run of `run_documents.py`. The build plan
(`work/drafts/buildplan-socratic-workflow.html`) puts a gate's transcript here rather than in a
pull request, because there are no pull requests: each phase is one commit on `main`, pushed when
its gate passed, and the next phase starts when the push has landed.

Scores of fixtures are not pasted here — a score carries the sheet's bands, and this file is in a
public repository. The provenance line and the headings found are enough to show a gate passed.

---

## Gate 0 — 11 September 2026 — ground

```
$ python3 project-documentation/socratic_agent/gates.py 0
gate 0 — ground, at /Users/witoldtenhove/Documents/HAN/M3DM/ai-in-business-intake
  ok   README.md exists
  ok   roster.tsv exists
  ok   log.tsv exists
  ok   rubric exists
  ok   inbox exists
  ok   teams exists
  ok   rubric/prd-scoresheet.md exists
  ok   no per-week folder at the root 
  ok   roster header is team/names/channel
  ok   every roster line has team, names and channel (0 team(s); the owner fills these in)
  ok   fixtures README names prd-socratic-gate.md
  ok   fixtures README names blueprint-socratic-workflow.html
  ok   fixtures README names pull only
  ok   pipeline-log.md exists
PASSED
exit 0
```

The roster has zero teams: the file has its header and its comment, and the names are the owner's to fill in before the week-1 run. Gate 0 checks the roster's shape and reports the count; it does not require a team, because the run that needs one is phase 3's, not this one.

## Gate 1 — 11 September 2026 — intake

Two defects found on the first run, both fixed before this transcript: a second hand-in of the same deliverable with a different extension was filed as a first version and its text overwrote the first; and the manifest was rewritten on a run that did nothing, so "no file changed" could not be checked.

```
$ python3 project-documentation/socratic_agent/gates.py 1
gate 1 — intake, scratch root /var/folders/tl/27n5mfs173zf3987pbbpmpcw0000gn/T/intake-gate-zjrdi6o3
  run 1
  ok   exit 1 (got 1)
  ok   Team 3 PRD.pdf filed and converted
  ok   team-03-prd-v2.md filed as -v2 and converted
  ok   t05_prd.docx filed and converted
  ok   the non-PDF is filed but not converted
  ok   prd-final.pdf stays in the inbox
  ok   manifest has prd-final.pdf with an empty team cell
  ok   team-03 documents.tsv holds one prd line, at version 2
  ok   log.tsv has header + 4 moves (5 lines)
  run 2 — manifest corrected
  ok   exit 0 (got 0)
  ok   prd-final.pdf filed as team-06 and converted
  ok   log.tsv gained exactly one line
  ok   team-06 documents.tsv has one line
  ok   manifest is empty
  run 3 — nothing to do
  ok   exit 2 (got 2)
  ok   no file changed
PASSED
exit 
```

## Gate 2 — 11 September 2026 — scorer

```
$ .venv/bin/python project-documentation/socratic_agent/gates.py 2
gate 2 — scorer, scratch root /var/folders/…/intake-gate-rqt7nh1d
  intake
      team-03 blueprint v1: team-03-blueprint.html → team-03-week-01-blueprint.txt (3374 words)
      team-03 prd v1: team-03-prd.md → team-03-week-01-prd.txt (2203 words)
  ok   both fixtures filed and converted
  run 1 — score
      team-03 prd v1: SCORESHEET → teams/team-03/week-01/owners/score-prd.md
      ! team-03 blueprint: unscored: no sheet for blueprint
  ok   exit 1, because the blueprint has no sheet (got 1)
  ok   owners/score-prd.md written
  ok   provenance header carries criteria commit, sheet hash and version
  ok   required headings present
  ok   nothing written for the blueprint
    headings found: ## SCORESHEET, ## BEFORE V1
    header:
      criteria: site/prd-criteria.html @ e5f12af
      sheet: rubric/prd-scoresheet.md sha256 8edcc7d4ec1c
      previous: none
  run 2 — skip
  ok   exit 1 again: the blueprint is still unscored (got 1)
  ok   score-prd.md unchanged
PASSED
exit 0
```

About 30 seconds of model time per document.

**Read, not gated.** The fixture was scored three times in three fresh scratch roots. One run
*returned* it on invariant V2 — the primary user is a student team, not "the team as
researchers" building a platform — which is arguably right: the gate's own PRD is not the kind of
document the sheet was written for, and the fixture is a stand-in. The other two runs scored it,
six points apart, and disagreed by two or more on three items (A5, C1, B3). Two readings for the
sheet's author: the invariants are applied softly two times in three, and the items that moved
are the ones whose criterion asks for something the document could carry implicitly. Neither is
a defect in the step; both are calibration, and the sheet is the place to tighten them. A team's
real PRD, written to the brief, will not trip V2 the way this fixture does.

## Gate 3 — 11 September 2026 — questioner, register, lint

The first run failed on the lint, and the lint was wrong: it rejected a question for the word
*assessment*, which is the fixture's own subject, and another for a section code the team had
written itself. The lint now exempts quoted spans, no longer flags ordinary words, and treats a
code as a leak only when it does not occur in the team's own text. What it still catches is what
the sheet would leak: a code the team never wrote, a total, a fraction, a band name, and the
words score, scoresheet, band and rubric.

```
$ .venv/bin/python project-documentation/socratic_agent/gates.py 3
gate 3 — questioner
  scenario 1 — first week, PRD fixture
      team-03 prd v1: RETURNED → teams/team-03/week-01/owners/score-prd.md
      team-03: 4 questions → teams/team-03/week-01/team/message.md; register: no earlier questions
  ok   questions.md has three to five lines (4)
  ok   every question ends in a question mark
  ok   message.md written and passes lint
  ok   register has 4 lines, all open
  ok   no roster name in the assembled input
  ok   no roster name in the message
  ok   no score column in the assembled input
  scenario 2 — planted lint failure
  ok   lint catches the planted lines (3 hits: criterion code, a total, the word band)
  ok   lint passes a question quoting the team's own code and words
  scenario 3 — week 2, one register question answered in a doctored document
      team-03 prd v1: RETURNED → teams/team-03/week-02/owners/score-prd.md
      team-03: 4 questions → teams/team-03/week-02/team/message.md; register: team-03-w01-q1→answered, team-03-w01-q2→ducked
  ok   q1 (the clock) is answered with a quote
  ok   the answered question is not asked again
  ok   q2 has a valid status (open)
  ok   at most five questions open
PASSED
exit 0
```

About a minute of model time for two scores and two question sets.

**The fixture's message, in full** (scenario 1) — the one output that is meant to be read:

> 1. The document states, "Primary user — a team of four, in weeks 2 to 6, who have just published that week's handbook page." Given that "The problem" is described as the gate being "built not at all" and the mechanism it replaces "does not scale past the kick-off," what problem, from the perspective of this primary user, does the Socratic gate solve?
> 2. The document states, "The hard deadline is a feature, and it is this document's sharpest claim." How does the document demonstrate that this hard deadline serves as a beneficial "feature" for the "Primary user — a team of four"?
> 3. The document states, "The team's only action is to publish on time — the whole interface, by design." However, it also states that someone "must be able to... Show what a question changed" and that "What they owe in return is a revision." In what ways are these actions of showing changes and making revisions consistent with the team's "only action"?
> 4. The "Secondary user — the two module owners" receive "the same report the team received, plus the score behind it and the gate-A signal." What specific action would a module owner take, or what decision would they make differently, on Monday morning, given this information and the criteria described in section 3.D1?

**Read, not gated.** Every question is anchored in a quoted sentence, and the third finds a real
tension in the document. The fourth asks about "the criteria described in section 3.D1" — a
section of the fixture, so allowed, and a reminder that the questioner will refer to a team's own
codes when the team uses them. Across gates 2 and 3 the scorer has now *returned* this fixture on
invariant V2 four times in seven; the questioner worked from the returned reason each time and
still produced grounded questions, which is the behaviour the design wanted for a document that
fails an invariant.

## Gate 4 — 11 September 2026 — coherence

Two things changed on the way to this transcript. The gate's own trace counter only knew tables
and dashes, and the model writes the trace as a nested list, one top-level item per PRD line;
the counter now counts top-level items. And the lint rejected a good question for the word
*scoring* — the blueprint fixture is a document about a scorer — so the exemption that already
held for codes now holds for words: a term the team's own text contains is not a leak. The
lecturer reading every message before it is sent is the rule; the lint is the net under it.

```
$ .venv/bin/python project-documentation/socratic_agent/gates.py 4
gate 4 — coherence
  the pair — week 2
      team-03: coherence over 2 documents, 22 finding(s) → teams/team-03/week-02/owners/coherence.md
  ok   exit 0 (got 0)
  ok   the three headings are present
  ok   TRACE has at least seven rows, one per line of the PRD's table (57)
  ok   FINDINGS names the planted departure: the inbox door against pull-only
  ok   provenance header carries the sheet hash
  the questioner, after it
      team-03: 5 questions → teams/team-03/week-02/team/message.md; register: no earlier questions
  ok   exit 0 (got 0)
  ok   at least one register line is tagged coherence (5)
  ok   no direction code in the message
  one document alone
      team-03: coherence skipped — 1 document(s) so far, needs two
  ok   skipped with a reason, nothing written, exit 2 (got 2)
PASSED
exit 0
```

About a minute and a quarter: one coherence call over both fixtures, one questioner call.

**The findings, in part** — our own documents, so publishable. Besides the planted departure,
which the report classified as a *recorded change* rather than a contradiction because the
blueprint states and justifies it, the first run found two open questions of the PRD that the
blueprint's own list of open questions drops — region and residency, and who owns the project —
and a PRD requirement the blueprint carries only generally: the manual override of a gate,
"logged with a reason". All three are true, and they are the blueprint's to answer. The count of
findings varied between runs (6, 12, 22) as the model split or merged items; the substance of
the top findings did not.

**The questions it led to** (one of five):

> The blueprint states that the questioner "never sees a number" and that this "is a property of
> the wiring rather than a rule the model has to remember". What specific aspect of the wiring, as
> described in the blueprint, ensures that the questioner model call definitively does not receive
> any numerical data from the scoring process?
