# ADR-0015: What the Socratic gate runs on — the no-code canvas or a service we own

## Status

Proposed

## Context

[ADR-0014](0014-socratic-gate-architecture.md) decided the architecture: the gate
pulls the page a team has already published, on a weekly schedule, and there is
no submission mechanism at all. That record settled *what* happens. It named a
mechanism in passing — "a scheduled Workflow Builder workflow over a roster of
team page URLs" — and left the rest of the runtime unstated, because at the time
nobody had built one.

A pilot has now built one, twelve times, and the log of it is in
`project-documentation/test-fixtures/pilot-log.md`. Four things it found bear on
this decision, and none of them was visible from the outside:

- **The no-code canvas cannot read a page.** Its URL Context tool is a
  summarising sub-agent, not a fetch. The summary it returns dropped the source
  list entirely, so the gate scored a page it had never seen and quoted sentences
  the team had not written. There is no setting that changes this.
- **The knobs that matter are not exposed.** The thinking budget is managed by
  the runtime and cannot be set on the node. The agent had no planning budget for
  four runs, which is part of why it never once called the search tool it had
  been given.
- **The runtime routes nothing.** It returns one response to its caller. The two
  audiences — questions to the team, rubric to the owners — have to be separated
  by whatever calls it, or not at all.
- **There is no per-agent spend cap.** Cloud Billing budgets alert; they do not
  stop. ADR-0009 promises a hard cap, and no part of the platform provides one.

What breaks if this stays undecided: the gate runs on one person's browser
session, on a canvas that cannot reliably read the thing it is grading, with the
rubric one careless forward away from the students it grades.

## Options considered

**Stay on the no-code canvas.** Nothing to build, nothing to host, and the
teaching team edits the agent in a browser without a Python environment — which
matters, because the people maintaining this are lecturers rather than engineers.
It fails on the first finding above and that is enough: an agent that scores a
summary is not a gate, it is a plausible-looking report generator, and the fault
is invisible in the output. It also leaves the two audiences in one response with
nothing but discipline between them.

**The agent as code, run by hand each week.** The pilot's `run_week.py`. Honest,
cheap, no infrastructure, and the schedule becomes a person remembering. That
person is one of two module owners in a week that already contains teaching, and
the protocol's whole force comes from the run being a clock. A deadline enforced
by someone's calendar is a deadline that gets extended, which is the thing the
PRD's hard-deadline section exists to prevent.

**A workflow orchestrator** — Workflows, Composer, or similar — driving the same
container. More machinery to reason about for a job that is one HTTP call a week
against ten pages, and every part of it is another thing to hold a permission.

**The agent as code, on a service that runs itself.** Cloud Run holding the agent,
Firestore holding the roster and the reports, Cloud Scheduler as the clock. Costs
a container, a database, a service account, and a deployment the teaching team
cannot do from a browser. Buys a fetch that returns the page, model settings that
are parameters, and — the part that is not merely convenience — the ability to
put the two halves somewhere different.

## Decision

**The gate runs as an ADK agent in a Cloud Run service, with Firestore holding
the roster and the reports, triggered weekly by Cloud Scheduler in an EU region.**

This does not supersede ADR-0014. That record's architecture is unchanged and its
central argument is untouched: the agent's only input is a page that is already
public, so NFR-11 remains a property of the wiring rather than a rule a tired
student has to remember. What changes is the one mechanism ADR-0014 named in
passing — Workflow Builder — which the pilot established cannot read a page.

Four things are decided here rather than left to implementation:

1. **The two halves go to two collections.** `reports/` holds what a team may
   see; `owner_reports/` holds the scores, the ledger and the gate signal.
   Whatever delivers reports to a channel is granted the first and refused the
   second. The single unrecoverable failure in this design is the rubric reaching
   a student, and a permission boundary holds where an instruction does not.
2. **History comes from `reports/` and only from there.** Prior weeks'
   team-facing reports are read back as context, which is what makes ADR-0014's
   growth requirement work without anyone assembling it by hand. Because the
   owners' collection is not read, a score cannot travel into next week's
   questions.
3. **A partial run is a failed run.** The service returns 500 if any team got no
   report, so a week that quietly produced eight of ten appears as a failure in
   the scheduler's history. One run in twelve returned nothing at all during the
   pilot, with no error.
4. **There is no endpoint that re-runs a team on request.** A single-team route
   exists for a broken run, not for a late page. The schedule is the deadline,
   and a route that can be asked for will be asked for.

The manual route stays. Every automated step in this module keeps one, and a
page published late still has to be gradeable by hand.

## Consequences

- **The teaching team can no longer edit the gate in a browser.** Changing a
  prompt now means a repository, a commit and a deploy — a real cost, paid by two
  lecturers. It is worth paying because the prompt is the rubric, and a version
  of the rubric that only one person's console holds is neither reviewable nor
  recoverable.
- **Someone must own a deployment.** A container, a database and a scheduler job
  are three more things that can be misconfigured, and none of them announces
  itself when it is. The 500 covers a failed run; nothing covers a scheduler job
  that was never created for week 4.
- **The ownership problem is now concrete rather than theoretical.** ADR-0014
  noted that the gate runs on one person's account. It will now also run on one
  person's project, database and billing. Before a second cohort this has to be
  an institution's project, or the gate leaves when they do.
- **ADR-0009's hard spend cap does not exist and cannot be built cheaply.** Cloud
  Billing alerts; stopping requires wiring a budget alert through Pub/Sub to a
  function that disables billing. Either that gets built, or ADR-0009 is amended
  to promise a monitored ceiling, which is what it would actually be. Leaving the
  record claiming a cap nobody implemented is the worse option.
- **Firestore's location cannot be changed after creation.** Choosing the region
  answers the residency question ADR-0014 left open, and answers it once.
- **The roster is now a database nobody looks at.** A team that renames its page
  stops being read, silently, and the failure looks like a team that published
  nothing. This was already true in ADR-0014 and is now easier to ignore, because
  the roster has moved out of sight.
- **Delivery is not built and is deliberately separate.** Until something reads
  `reports/` and puts it in front of a team, the gate produces reports nobody
  receives. The permission split makes that job safe to build; it does not build
  it.
- **The score is a signal and not a measurement.** The pilot ran the same three
  pages four times: direction was right every time, and the numbers moved by up
  to two points, with one ledger verdict taking three different values. The gate
  threshold does arithmetic on those numbers. It held here only because the gap
  between a good page and a weak one is far wider than the noise, and a page near
  the boundary will be decided by the noise — which is what the instructor
  override in LRD §6.6 is for, and a reason not to remove it.
