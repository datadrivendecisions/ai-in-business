# PRD — the course site for *AI in Business* (first draft)

*Written to the same prompt the teams get in AEL week 1 (`assignment-ael-prd.md`), on the same
1–3 page bar. The site is the one piece of the module the teaching team builds itself, so it is
worth writing its requirements the way we ask students to write theirs — and worth scoring
against them, the way `kickoff-scorecard.md` scores the session.*

---

## 1. Problem and users

**Primary user — a student in HAN's minor *Data Driven Decision Making in Business*** who has
just enrolled in *AI in Business* and has never met either module. They arrive with three
questions, in this order, and leave if the site answers none of them:

1. *Why should I care?* — what this gives me that the rest of the minor does not.
2. *How does it work, and how am I judged?* — the rhythm, the team, the mark.
3. *What do I actually do — overall, and this week?*

They read on a laptop between classes, or on a phone. They will come back weekly for exactly one
thing: what is due, and what happens in the next session.

That primary user is a composite, and a composite has no fears the page happens not to answer.
[`course-site-journeys.md`](course-site-journeys.md) splits them into four personas, maps each
one's journey through the site, and scores the site once per persona — a journey-level companion
to the page-level scoring in [`course-site-scorecard.md`](course-site-scorecard.md).

**Secondary users.** The two module owners, who publish one week at a time and must be able to do
it in minutes. Colleagues in the LRD's audience, who reach the site for the learning-requirements
document. Prospective students and the minor's coordination, who want to see what the module is.

**The problem.** The module runs adaptively — materials are decided week by week, one week ahead
(`course-outline.md`). That is a deliberate didactic choice, and it is also the thing most likely
to read to a student as *disorganised*. The site's job is to make the adaptive design legible:
what is **fixed for the whole run** is published up front and does not move; what is **decided as
we go** is named as such, and appears on a stated schedule.

## 2. What it must let a user do

| A user must be able to | Path |
|---|---|
| Decide, in under a minute, whether this module is worth their attention | Landing page opens on purpose, grounded outside the school |
| Understand the deal — team, rhythm, deliverable, mark — without asking a lecturer | One landing page, no click needed for anything structural |
| See the whole six-week arc, and know what is provisional in it | Week map on the landing page, marked provisional, with the publication rule stated |
| Find this week's work, complete | One page per teaching week, linked from the map; week 1 published before the kick-off |
| See what a finished deliverable looks like | Link to the handbook template |
| Reach the module owners' document | Link to the integrated LRD, under a heading that says who it is for |

## 3. Output qualities — what a good course-site page looks like

The **quality criteria** this site is built and scored against. Eighteen items, each scored 0–3
(3 = designed in and visible on the page; 2 = present but partial; 1 = asserted, nothing carries
it; 0 = absent). Maximum 54. **Target: ≥ 90 %, i.e. 49 or more.**

**A · Purpose — why this course matters to *this* student**

- **A1.** The page opens on the student's stake, not on administration: what they will be able to
  do afterwards that they cannot do now.
- **A2.** The "why now" is grounded in something outside the school — the Draghi diffusion
  argument — in one passage a student reads in under a minute.
- **A3.** The course is placed inside the minor: who it is for, what it assumes, where it sits,
  with a link to the minor's own module page.
- **A4.** Honest about the experiment: the adaptive week-by-week design is stated, with what it
  means for the student. No false precision about weeks we have not designed yet.

**B · Structure and assessment — legible without asking a lecturer**

- **B1.** The two modules and the one team are shown side by side, with what each produces — a
  student can tell which hat they wear when.
- **B2.** The rhythm is explicit: six teaching weeks then an assessment period, one joint session
  a week, one published page per team per week.
- **B3.** Assessment is complete and unambiguous: what carries the mark, what does not, whose mark
  it is, and what evidence it draws on.
- **B4.** Team composition and the four build roles are stated, with what each role owes the team.

**C · The work — global and week by week**

- **C1.** The end product is concrete: the handbook, its reader, and a link to the template the
  student can actually look at.
- **C2.** Fixed versus decided-as-we-go is visibly separated, not buried in prose.
- **C3.** All six weeks appear with theme and platform layer, marked provisional, and the
  publication rule ("detail lands one week ahead") is stated where the gaps are.
- **C4.** Week 1 is complete and actionable: pre-reading with a link, what happens in the session,
  both assignments in full with their bar, and what is handed in.

**D · Craft — the site as an artefact**

- **D1.** Publication gate: every relative link resolves inside `site/`; `check-links.sh` passes.
  Anything outside `site/` is linked by absolute URL.
- **D2.** Brand system: the inlined Business Data Solutions token block, used through tokens
  rather than hard-coded values, visually consistent with the other two pages.
- **D3.** No JavaScript. Anything interactive uses native HTML that degrades to visible content.
- **D4.** Accessible and responsive: semantic landmarks, one heading order, visible focus,
  sufficient contrast, wide content scrolls in its own box, readable at 360 px.
- **D5.** Repo conventions: AIBS/AEL only, British-leaning prose with em dashes, nothing published
  that only a Proposed decision record supports, no parallel Markdown copy of a page.
- **D6.** Maintainable at the weekly cadence: publishing week N is one new file plus one link,
  following an obvious pattern, with placeholders in the existing `.tpl` convention.

## 4. Known constraints

- Three hand-authored static HTML pages, inlined CSS, **no build step, no dependencies, no
  JavaScript**. A per-week page is authored, not generated.
- Only `site/` is published; a relative link that escapes it fails the build.
- The palette is inlined per file — a palette change means editing every page.
- The LRD is the *ideal*; `course-outline.md` is how the module actually runs. Where they differ,
  the student-facing site follows the outline.
- Every decision record is still **Proposed**. The site publishes only what `course-outline.md`
  states as fixed, and marks the rest provisional.
- The module owners publish each week by hand, under time pressure, the week before.

## 5. Out of scope (for now)

Team pages and per-team handbook contributions (they arrive with the cohort); submission
mechanics beyond naming where and when; the teaching team's decision log (internal); weeks 2–6
detail; any search, login, comment or analytics; the Socratic tutor and instructor dashboard,
which the LRD holds as design, not as things a student can use today.

## 6. Open questions and assumptions

- **Open — where drafts are handed in.** The session plan leaves it as `[where]`, `[when]`. The
  site says the hand-in is named in the session until that is settled.
- **Open — the weekly block's length after week 1.** Week 1 is ~4 hours; the LRD assumes 2.5.
  The site states week 1 only.
- **Open — field visit window.** Planned weeks 2–4, subject to the adaptive call.
- **Assumed** — the cohort is a single group taught by both owners together, teams of four.
- **Assumed** — students reach the site by link from the LMS; no navigation from elsewhere.
