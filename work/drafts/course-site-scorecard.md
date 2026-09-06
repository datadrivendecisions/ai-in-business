# Course-site scorecard — *AI in Business*

*Scores `site/index.html` and `site/week-01.html` against the eighteen quality criteria formulated
in [`prd-course-site.md`](prd-course-site.md) §3. Same instrument as
[`kickoff-scorecard.md`](kickoff-scorecard.md), same scale, same target — and the same caveat:
self-assessed and therefore optimistic. The number is a design check, not evidence.*

## Scale

Each item scores 0–3.

- **3** — designed in: the page carries it, and you can point at where.
- **2** — present but partial: it is there for some readers or in some places.
- **1** — asserted: the page says it, nothing on the page carries it.
- **0** — absent.

Eighteen items, maximum 54. **Target: above 90 %, i.e. 49 or more.**

## Items

The criteria are stated in full in the PRD; abbreviated here.

| | |
|---|---|
| **A · Purpose** | A1 opens on the student's stake · A2 grounded outside the school, readable in a minute · A3 placed inside the minor, assumptions stated · A4 honest about the adaptive design |
| **B · Structure & assessment** | B1 two modules side by side · B2 the rhythm explicit · B3 assessment complete and unambiguous · B4 team and roles, with what each owes |
| **C · The work** | C1 the end product concrete and linked · C2 fixed vs decided visibly separated · C3 all six weeks, provisional, publication rule stated · C4 week 1 complete and actionable |
| **D · Craft** | D1 publication gate · D2 brand system · D3 no JavaScript · D4 accessible and responsive · D5 repo conventions · D6 maintainable at the weekly cadence |

---

## Scoring log

### Cycle 1 — baseline: the first assembled build

Two pages built from `course-outline.md`, `session-plan.md` and the two week-1 assignment prompts.

| Item | Score | Evidence |
|---|---|---|
| A1 | 2 | The stake is in the pull-quote, but the first body paragraph is about the site — "This is the course site. It holds…" |
| A2 | 3 | Draghi's diffusion argument in three paragraphs, with the Commission's one-pager linked |
| A3 | 3 | "Where it sits, and what it assumes" — links the minor, states the prior knowledge, states that programming is not assumed |
| A4 | 3 | "Fixed, and decided as we go" states the adaptive design and its consequence for the reader |
| B1 | 3 | Five-row comparison table, plus each module's week-1 deliverable |
| B2 | 3 | "How a week runs" — four numbered steps; six weeks then an assessment period |
| B3 | 3 | Assessment table: instrument, marks, evidence, what is *not* evidence, end deliverables |
| B4 | 3 | Role table with what each role owes the team; "none of the four roles is a spectator" |
| C1 | 3 | The handbook callout, its reader, and a link to the template as the worked example |
| C2 | 3 | Two cards, badged **Fixed** / **Decided as we go**, contents taken from the outline's own split |
| C3 | 3 | Six weeks plus the assessment period, marked provisional, publication rule stated above the table |
| C4 | 2 | Pre-reading, agenda, both assignments in full — but the page never says **when or where** the session is, not even as a placeholder |
| D1 | 3 | `check-links.sh` passes; the Draghi summary and the minor's page are absolute URLs |
| D2 | 2 | Tokens throughout, but the page opened on two stacked rules (header border + part border) and nested lists in the agenda lost their markers |
| D3 | 3 | Zero `<script>` in `site/`; the one disclosure is a native `<details>` |
| D4 | 2 | `--text-muted` on `--bg-cream` measures **4.26:1** — below AA — in the hand-in block; the skip link scrolled but did not move focus |
| D5 | 2 | Three claims rested only on the LRD and a still-Proposed record: score-recorded-before-comparison, "decision log, build plan" as deliverables, and a *joint* session every week |
| D6 | 2 | The weekly-page pattern existed but was documented nowhere; `CLAUDE.md` still described a three-page site |
| **Total** | **48 / 54 = 89 %** | |

Below target. The content was in place; the defects were craft and over-claim.

### Cycle 2 — craft and framing pass

Changes: the opening paragraph now leads with the student's six weeks and the manufacturer's
question, and the site-meta sentence moves to second position (A1); the page header's rule is
dropped so the first part heading supplies the only divider (D2); nested agenda lists get a disc
marker back (D2); `.handin .tpl` steps up to `--text-secondary`, 6.7:1 (D4); `<main>` takes
`tabindex="-1"` so the skip link moves focus (D4); `CLAUDE.md` and `README.md` gain the
weekly-page pattern, the audience of the landing page, the outline-over-LRD rule and the
muted-on-cream warning (D6).

| Item | Change | Score |
|---|---|---|
| A1 | Opens on "You will spend six weeks on one question a real regional manufacturer is actually asking" | 3 |
| D2 | One divider, markers restored | 3 |
| D4 | Contrast fixed; focus moves; verified no horizontal overflow at 360 px | 3 |
| D6 | Pattern documented in both `CLAUDE.md` and `README.md`; `week-01.html` named as the file to copy | 3 |
| **Total** | | **52 / 54 = 96 %** |

Residual 2s: C4 and D5.

### Cycle 3 — accuracy and completeness pass

Changes: the three over-claims are trimmed to what `course-outline.md` actually fixes — the marks
row loses the score-before-comparison procedure, the deliverables row loses "decision log, build
plan" for "the documents that specify it — starting with the PRD you draft in week 1", and the
weekly session is "shared by both modules" rather than asserted joint every week (D5); week 1
gains a **When and where** row, marked as a placeholder rather than silently absent (C4); the
"How the two fit together" disclosure opens by default, because a student who misses it drafts two
documents that disagree; two pieces of teaching-team jargon leave the student-facing map —
"vibe-coded spike" becomes "a quick throwaway build", and the assessment period's detail cell no
longer promises to appear "a week ahead".

| Item | Change | Score |
|---|---|---|
| C4 | The two genuinely unknown values — session room/time, hand-in location — are now on the page as marked placeholders, so a reader can see they are pending rather than missing | 2 |
| D5 | Nothing on the student-facing pages now rests on a Proposed record alone; `CLAUDE.md` records the outline-over-LRD rule that keeps it that way | 3 |
| D6 | Unchanged | 2 |
| **Total** | | **52 / 54 = 96 %** |

---

## Final score

**52 / 54 = 96 %.** Above the 90 % target.

Per-cluster: **A 12/12 · B 12/12 · C 11/12 · D 17/18.**

### The two residual 2s, and why they stay

**C4 — week 1 cannot be fully actionable yet.** Two values are unresolved in the source documents
themselves: `session-plan.md` ends its hand-in line with `[where]`, `[when]`, and no timetable in
this repository gives the room or the start time. Inventing either would be worse than a marked
placeholder, and both are one edit away once a module owner supplies them. This is the one item
that should move to 3 before the cohort arrives.

**D6 — two stylesheets have to be kept identical by hand.** `index.html` and `week-01.html` carry
the same 330-line inlined stylesheet, and a component change means editing both. That is the
repository's own constraint — inlined CSS, no build step — not a slip, and the alternatives
(a shared `.css` file, a generator) each break a rule the repo holds on purpose. The mitigation is
documentation, not machinery: `CLAUDE.md` now says the two must stay identical, and
`diff <(sed -n '/^<style>/,/^<\/style>/p' site/index.html) <(sed -n '/^<style>/,/^<\/style>/p' site/week-01.html)`
checks it in one line. A third weekly page makes this worse, not better, and is the point at which
the trade-off is worth revisiting.

### What was measured rather than asserted

- `check-links.sh` — passes (D1).
- Contrast ratios computed for all thirteen foreground/background pairs in the palette as used;
  one failure found at 4.26:1 and fixed by scoping, not by moving a shared token (D4).
- HTML parsed for unclosed tags, heading-level skips and dead fragment links, including
  cross-page ones — all clean (D4).
- `document.scrollWidth == clientWidth == 360` on both pages: no horizontal overflow at phone
  width (D4).
- `grep -c '<script'` = 0 across `site/` (D3).
- Both stylesheets byte-identical (D6).

### Caveat

Same author, same scorer — the criteria in the PRD were written by the same hand that then built
against them, which is exactly the failure mode `kickoff-scorecard.md` warns about. The score that
counts is the one a student gives in week 1 when they cannot find something.
