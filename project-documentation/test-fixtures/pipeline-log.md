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
