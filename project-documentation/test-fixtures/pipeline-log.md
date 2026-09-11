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
