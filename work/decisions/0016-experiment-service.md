# ADR-0016: How the week 3 experiment collects results — the browser, or a service we own

## Status

Superseded by ADR-0017

## Context

The week 3 experiment needs thirty-two students' results in one place, inside a
150-minute block, while the room is still interested. The tool is currently
specified as browser-only: every student's answers live in their own
`localStorage`, and aggregation is a person pasting thirty-two lines of text
into a box.

That was chosen deliberately and it buys something real. Nothing leaves the
laptop, so withdrawal is closing a tab, no data-protection question arises
because no data moves, and the consent sentence is the shortest one anybody will
ever write. It is also the only design that obeys the standing rule in
`CLAUDE.md`: a `tool-*.html` page may carry JavaScript **only** if it is
self-contained, with no build step, no framework and no network calls.

Three costs of that design are felt in the session rather than on paper. The
paste step spends the better part of ten minutes at the exact moment the room's
attention peaks. A line typed or copied wrong is a participant lost with no way
to recover them. And the dashboard cannot be live, so the thing the session is
building towards — watching a difference appear and then being asked what it
licenses — happens after a lull instead of during one.

[ADR-0014](0014-socratic-gate-architecture.md) rejected making the site a real
front end for the Socratic gate, and said so in terms that anticipate this
moment: *"Option B is not rejected for ever. If the pull model proves too coarse
… the answer is a narrow submission endpoint, decided in its own record, with the
site's static property given up deliberately rather than by drift."* This is that
record.

Two further facts bear on it. [ADR-0015](0015-gate-runtime.md) already stands up
Cloud Run, Firestore and Cloud Scheduler in an EU region for the gate, so the
infrastructure question is answered by what is on hand. And LRD §6.6 describes an
instructor dashboard that ADR-0014's consequences admit is not built by anything
yet.

What is undecided is whether student work may leave the browser at all, what a
service may hold if it does, who may see an interpretation of the result, and
what happens to the data when the session ends.

## Options considered

**A — Keep the browser-only design and paste thirty-two lines.** Free, no
operational owner, no data-protection surface, and withdrawal stays trivially
easy. It costs roughly ten minutes of the block, it is fragile to a mistyped
line, and it cannot produce a live view. It is the right answer if the dashboard
is a convenience; it is the wrong answer if the dashboard is the lesson.

**B — A shared spreadsheet.** Students paste their line into one sheet. Cheap,
familiar, nothing to build. It fails on two counts, and both are fatal rather
than inconvenient: every student can read every other student's line, which
contaminates the debrief that the whole session is aimed at, and it needs a
Google identity per student inside the owner's tenant — the same objection
ADR-0014 raised to its own option D, and a data-protection question nobody has
asked.

**C — A narrow submission endpoint and an instructor-only dashboard, in a service
of its own.** A Cloud Run service with two routes and a Firestore collection
behind it. It costs a container, a secret, a purge job and an operational owner,
and it makes the session depend on something that can be down. It buys the live
dashboard, removes the typing, and reuses infrastructure the gate already needs.

**D — Add an experiment route to the existing gate service.** Cheapest in
infrastructure and the most tempting. It couples a once-a-year teaching
experiment to the service that must run every week: a bad deploy on a Monday
afternoon takes the Socratic gate down with it, and the gate is the thing that
cannot fail.

## Decision

**The experiment collects results through a narrow submission endpoint on a
service of its own, with an instructor-only dashboard, and the site's static
property is given up for exactly one named page.**

Seven things are decided here rather than left to implementation.

1. **The exception is named, not general.** `site/tool-bias-experiment.html` may
   call one origin and two routes. Every other page in `site/`, including every
   other tool, keeps the no-network rule unchanged. `CLAUDE.md` gains the
   exception with the page named in it, so that the next tool cannot inherit it
   by analogy.
2. **The service takes numbers and never prose.** Counts, timings and scale
   scores go; the student's position sentences and whatever their assistant
   replied stay in the browser and are never transmitted. This keeps NFR-11 — the
   rule that interview material never passes through a model service — a
   property of the wiring rather than a promise, and it removes the only part of
   the payload anyone would care about reading.
3. **One collection, and no per-student route.** `submissions/` holds what the
   dashboard aggregates. There is no endpoint that returns one student's row to
   anyone, which is the same permission boundary ADR-0015 drew between
   `reports/` and `owner_reports/` and for the same reason.
4. **Pressing submit is the consent act**, and the button says so. A student who
   does not press it is not in the dataset, exactly as closing the tab was
   before. A student who changes their mind afterwards gives their self-chosen
   code and the row is deleted.
5. **The data is deleted at the end of the teaching day**, by a scheduled purge
   rather than by intention. Retention is the session because that is all the
   purpose requires.
6. **The dashboard is instructor-only, and its interpretation is chosen from a
   fixed set of sentences rather than written by a model.** Which sentence
   appears is determined by where the confidence interval sits relative to
   zero, and the sentence cannot render unless the interval and the smallest
   effect the sample could have detected are both on screen beside it. A
   region for an interval narrower than that effect is not offered, because
   none exists: a 95% interval is always about 1.4 times as wide. A
   generated narrative may be added on top of that; it may never replace it.
7. **It is a separate service from the gate.** A teaching experiment must not be
   able to take down the thing that runs every week.

The reason to prefer C over A is not convenience. The live dashboard **is** the
pedagogical payoff: thirty-two people watching a difference appear and then being
asked what it licenses is the session, and ten minutes of transcription at the
moment attention peaks is the wrong trade. The reason to prefer C over D is that
the gate is load-bearing and the experiment is not.

## Consequences

- **This repository now contains something that can be down while a class is
  waiting**, which nothing in it could be before. A fallback is therefore part of
  the decision rather than a nicety: the tool keeps writing its `localStorage`
  line and keeps its copy button, so an outage degrades to the manual paste of
  option A instead of losing the session.
- **The clean consent story is gone.** *"Nothing you type leaves this browser"*
  was a genuine asset and it is now false. What replaces it is weaker and has to
  be said plainly: it leaves your browser, we hold numbers and not sentences, for
  one day, and you can have them deleted.
- **Someone owns a deployment** — a container, a database and a purge job — with
  the same burden ADR-0015 already names, and now twice over.
- **The exception will be cited.** Naming one page stops it spreading by drift,
  but the next tool that wants a network call will point at this record. The
  answer is that this one was argued and written down, which is exactly what the
  next one must also do.
- **An instructor dashboard exists for the first time**, so LRD §6.6 is partly
  built. The gate's half of it still is not, and this record does not build it.
- **A fixed interpretation will sometimes be wrong**, because it states what the
  interval permits rather than what is true, and an underpowered study usually
  permits very little. It is a guard against a model writing something
  overconfident, not a substitute for the owners reading the numbers.
- **A self-chosen code can be submitted twice.** Last write wins for a code, and
  the dashboard shows how many submissions it holds, so a mismatch with the
  register is visible rather than silent.
- **Student data now exists outside the institution's tenant**, in the module
  owner's cloud project, for a day. That is a smaller exposure than the gate
  already carries, and it inherits the same unresolved question ADR-0015 names:
  the project belongs to one person, and the experiment leaves with whoever
  leaves.
