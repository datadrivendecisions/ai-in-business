# ADR-0014: How the Socratic gate runs — the platform, and what carries the traffic

## Status

Proposed

## Context

The Socratic gate is specified in detail and built not at all. LRD §6.4 says what
it must do — one submission and one report per team per week, questions to the
team and a rubric score to the instructor, every report generated against the
team's full prior history so that no question repeats — and ADR-0009 says who
pays for it: a course-owned key with a hard spend cap, the single model-usage
line the programme funds. Nothing says where it runs or how a team reaches it.

Two facts now settle most of that. The module owner already has an account on
**Google's Gemini Enterprise Agent Platform**, so the platform question is
answered by what is on hand. And ADR-0013 has already
decided where gate traffic goes: the team's own Teams channel, deliberately
outside the marking system, because an unscored gate that arrives through the
graded channel stops being unscored in the only place that matters.

What is left is the part that looks obvious and is not: the course site is the
one address every student already has, so it is the natural front door for the
gate. But `site/` is hand-authored static HTML on GitHub Pages — no build step,
no backend, no dependencies, and by standing convention no JavaScript on any
page of the course itself. A page that accepts a submission and returns a report
needs all four. The site can be the gateway in one sense and cannot be in
another, and the difference has to be stated before week 2, when the first gate
runs and the week-2 draft still carries *exact location to be filled in here* as
a visible placeholder.

Three constraints bound every option below, and none of them is negotiable:

- **The graded party must not hold the controls.** LRD §6.4 and FR-10 put the
  agent's prompts, rubric and configuration beyond student write access. The
  hidden rubric and its scores are tier-1 instructor material under the
  publication rule — they may not sit in `site/` in any form, because `site/`
  is uploaded to a public URL from a public repository.
- **One report per team per week is the protocol, not a quota.** It is what
  removes the incentive to game the agent (LRD Part 12). Any architecture that
  hands a team an open chat window has already lost it.
- **Interview material may not pass through the platform.** NFR-11 and ADR-0013
  are absolute on this: public sources and the team's own writing may go through
  a model service, transcripts and consent go by the manual route inside the
  institution's tenant.

## Options considered

**A — Give every team a seat in the Gemini Enterprise app.** The agent is built
once in Workflow Builder and shared with the cohort; students open it in the
Gemini Enterprise web app and talk to it. It is the shortest path from an
existing account to a working gate, and it is the wrong shape twice over.
Sharing an agent requires a licensed seat per user, at roughly $21–30 per seat
per month; at eight to ten teams that is a four-figure line for a six-week run,
against ADR-0009's one capped line. And a chat window is an open-ended chat —
the team can re-ask, rephrase and probe until the questions soften, which is the
one thing §6.4's protocol exists to prevent. It also needs an identity for each
student inside the owner's tenant, which is a data-protection question nobody
has asked yet.

**B — Make the site a real front end.** A form on a course page posts to a Cloud
Run service holding the course-owned service account, which calls the
Interactions API, stores the report history, and writes the report back to the
page. This is the gateway as it is usually imagined, and it is the only option
that puts both the submission and the report on the site itself. It costs a
backend, a secret, a datastore, a per-team authentication scheme and an
operational owner — and it breaks the site's defining property. The tool
exception in the conventions allows JavaScript on a `tool-*.html` page only on
condition that it is self-contained and makes **no network calls**; a form
posting to Cloud Run is outside even that exception. It is a small application,
not a page, and it would be the first thing in this repository that can be down.

**C — The agent reads what the team has already published.** ADR-0013 decided
that the weekly handbook page is handed in *by being published*. Take that
literally: there is no separate submission at all. A scheduled Workflow Builder
run, once a week, walks the roster of team page URLs, generates one report per
team against that team's stored history, and delivers the questions to the
team's Teams channel and the report-plus-score to the instructor. The site's
role is to publish the roster and the protocol. No student authentication, no
backend, no JavaScript, no secret anywhere near the browser.

**D — A form as the letterbox.** A Google Form takes the week's submission and
triggers the agent; the report comes back by mail. Small and familiar, and it
adds a fifth hand-in route to a module that has just finished deciding it has
four. It also needs a Google identity per student for attribution, or an open
form that anyone can post to.

## Decision

**The gate runs as option C — the agent pulls the team's published page on a
weekly schedule — and the site is the gateway in the sense it can actually be:
it publishes the contract, not the traffic.**

Concretely:

1. **The agent is built on the Gemini Enterprise Agent Platform**, in a
   course-owned project, as a scheduled Workflow Builder workflow over a roster
   of team page URLs. Sessions carry each team's prior reports forward, which is
   what LRD §6.4's growth requirement needs and what a stateless call could not
   give. Billing is pay-as-you-go on the platform rather than per seat: at
   roughly sixty reports a run, the funded line stays a rounding error, and no
   student needs a licence, an account, or an identity in the owner's tenant.
2. **The schedule is the protocol.** One run a week produces exactly one report
   per team, by construction rather than by a rule someone has to enforce. There
   is no submit button to press twice and no chat window to reopen.
3. **The report goes to the team's Teams channel and the score goes to the
   instructor**, per ADR-0013 route 3. Two audiences, two destinations, and the
   rubric never enters the public repository.
4. **The site carries the gateway's other half**: on each week page, what the
   gate reads, when it runs, what comes back, where it arrives, and what the
   team is expected to do with it — the part of a gateway a static page is good
   at, and the part currently missing.

The reason to prefer this over B is not only that it is smaller. **It makes the
data boundary structural.** The agent's only input is a page that is already
public, so interview material cannot reach the model service by a student's
mistake — NFR-11 stops being a rule a student must remember at the moment they
are tired and becomes a property of the wiring. Option B, by opening a text box,
invites exactly the paste that rule forbids.

Option B is not rejected for ever. If the pull model proves too coarse — most
likely because teams want to submit reasoning that is not on the published page —
the answer is a narrow submission endpoint, decided in its own record, with the
site's static property given up deliberately rather than by drift.

## Consequences

- **The site never shows a team its report.** A student's mental model will be
  that the gate lives on the site, because that is where everything else lives,
  and the report will arrive somewhere else. The week page must say where, every
  week, in the same block that carries the hand-in routes — the same discipline
  ADR-0013 already demands, applied to one more artefact.
- **The gate can only see what was published.** Thinking a team did and did not
  write down is invisible to it. That is partly the point — the published page
  is the checkpoint — but it means a team that works well and publishes late
  gets a report about a page that no longer reflects them. The schedule must sit
  far enough after the publication deadline to make that rare, and the manual
  route (an instructor running the agent by hand on a late page) has to exist,
  consistent with the standing rule that every automated step keeps a manual one.
- **The roster of team page URLs becomes infrastructure.** It is the workflow's
  input, so a team that renames its page silently stops being graded. It belongs
  in one place, owned, and checked before each run.
- **A scheduled run has no one watching it.** NFR-04 asks for a report inside a
  session-usable window; a workflow that fails quietly on a Tuesday night meets
  that requirement on paper and not in fact. Someone must confirm each week that
  eight to ten reports actually landed, and that is a recurring task with a name
  on it, not a monitoring system.
- **Data residency is an open item with a deadline.** Gemini Enterprise supports
  EU data-residency zones on its Standard and Plus editions, while the Agent
  Platform's Interactions API is documented as `global`-region only. Student
  writing is not personal data of the kind ADR-0013 route 4 protects, but it is
  student work at a Dutch institution, and the question of which region processes
  it has to be answered before week 2. If the answer is
  unsatisfactory, the model call moves to a Vertex endpoint pinned to an EU
  region and the workflow calls it — a change of plumbing, not of this decision.
- **The account is the owner's, and that is a single point of failure.** The
  agent runs in one person's project on one person's billing. Before the second
  cohort, it needs to be a project the institution owns, or the gate leaves with
  whoever leaves.
- **The instructor dashboard (LRD §6.6) is not built by this decision.** What
  this gives the teaching team is a report and a score per team per week, in
  whatever the workflow writes them to. That is enough to run the gate and short
  of what §6.6 describes, and the difference should be admitted rather than
  planned around.
