# PRD — the Socratic gate (first draft)

*Written to the same prompt the teams get in AEL week 1 ([`assignment-ael-prd.md`](assignment-ael-prd.md)),
on the same 1–3 page bar. The gate is the one piece of the platform the teaching team builds
itself (LRD §6.4, ADR-0009), so it is worth writing its requirements the way we ask students to
write theirs — and worth judging against them.*

**Not for students, and not a draft on its way to the site.** It lives in
`project-documentation/` rather than `work/drafts/` because §3 below is the hidden rubric's
design, which is tier-1 instructor material: it may not enter `site/` in any form.

Architecture is settled in [ADR-0014](../work/decisions/0014-socratic-gate-architecture.md); this
document says what the thing has to do. Where the two disagree, the record wins. The agent's three
registered fields — name, description and the instructions carrying the rubric — are in
[`socratic-agent-config.md`](socratic-agent-config.md), which is the same tier-1 material and under
the same rule.

---

## 1. Problem and users

**Primary user — a team of four**, in weeks 2 to 6, who have just published that week's handbook
page. They do not operate the gate. They publish, and on a fixed morning a set of questions about
their thinking is waiting in their channel. What they owe in return is a revision, visible in next
week's page and in each member's portfolio.

**Secondary user — the two module owners.** They receive the same report the team received, plus
the score behind it and the gate-A signal, and they are the only people who can open a gate by
hand. They also carry the weekly confirmation that the run happened at all.

**Tertiary — the examiner at the criterion-based interview**, which is the same two people in a
different role. The run's accumulated reports are evidence: AC-06 asks each student to name a
question that changed their work, and that is only answerable if the history exists and is legible
months later.

**The problem.** The gate is specified (LRD §6.4), funded (ADR-0009), routed (ADR-0013) and
architected (ADR-0014), and built not at all. Week 2 is the first automated run, and the week-2
page still carries *exact location to be filled in here* where the answer belongs. Meanwhile the
mechanism it replaces — two lecturers walking between tables asking three questions and walking
away — does not scale past the kick-off and was never meant to.

**Why a machine does this and a lecturer does not.** Not cost. Consistency, memory, and the
absence of a face: eight to ten teams each get the same discipline, every week, from something
that has read every previous report and cannot be talked round.

## 2. What it must let a user do

The team's only action is to publish on time — the whole interface, by design.

| Someone must be able to | Path |
|---|---|
| Have their week's thinking questioned, without asking for it | Scheduled run reads the team's published page; no submission, no button |
| Know exactly what will be read, and when | Week page states the URL that is read and the hour the run happens |
| Receive questions they can act on before the next session | Report lands in the team's Teams channel, ahead of the weekly block (ADR-0013 route 3) |
| Show what a question changed | Report is quotable into the portfolio; the history is retrievable at the interview |
| See a team's report *and* its score | Instructor destination carries both, plus the gate-A signal (§6.4) |
| Open a gate that should not have closed | Manual override by an owner, logged with a reason (LRD §6.6, AC-07) |
| Confirm the week actually ran | One weekly check: N teams, N reports, or a named exception |

**The hard deadline is a feature, and it is this document's sharpest claim.** The run is a clock,
not a queue. A team that publishes after the run gets no report that week — the schedule *is* the
one-report-per-week limit from §6.4, and a re-run on request would quietly turn it back into the
resubmit-until-it-passes loop the protocol exists to prevent. So:

- **Published late is unread.** The gate does not wait, and there is no extension to ask for.
- **Unread is not unassessed.** The week's unanswered questions carry forward, exactly as
  unaddressed feedback does under §6.4; a missed week is visible in the history at the interview.
- **The manual re-run exists for our failure, not for theirs.** If the workflow breaks, the region
  is down, or the roster was wrong, an owner runs it by hand — consistent with the standing rule
  that every automated step keeps a manual one. Lateness is not one of those cases, and saying so
  once, in week 1, is cheaper than saying no eight times in week 4.

## 3. Output qualities — what a good report looks like

Two separate bars, because they are audited differently.

### 3a. Invariants — every report, every week, pass/fail

A report violating any of these is a defect in the shared system, not an unlucky week. Spot-audited
each cohort (AC-03).

- **I1. No verdict.** Never "this is good", "well done", "this is weak", "you should". Praise and
  advice are both barred; the kick-off card's rule — *never "good", never "yes", never "you
  might"* — is the same rule.
- **I2. No score, no grade, no level, no progress bar** in anything the team sees. Nothing numeric.
- **I3. Questions only.** Every sentence to the team is a question or the material a question needs
  in order to be asked.
- **I4. Nothing from another team.** A report names only its own team's work.

### 3b. Qualities — scored 0–3 on a sample

Same scale as the course-site PRD: 3 = clearly present; 2 = partial; 1 = asserted, nothing carries
it; 0 = absent. Twelve items, maximum 36. **Target: ≥ 30, and no item below 2.** Audited on a
sample of reports per cohort, and this is also the seed for the eval config AEL week 4 asks teams
to write against §6.2 — the gate is judged the way we teach them to judge.

**A · Grounded in this page, this week**

- **A1.** At least one question quotes or points at a specific sentence, claim or number on the
  team's page. A report that would fit any team is worth nothing.
- **A2.** Questions target the week's own capability (§3.2, Part 8) rather than generic research
  hygiene.
- **A3.** At least one question probes a source: who says this, and why are they worth believing.
- **A4.** At least one question probes critical vetting of what the team's platform generated —
  the failure mode §6.4 names, now that the page is machine-produced.

**B · Socratic in form, not only in label**

- **B1.** Questions are answerable inside one week by this team, with what they have.
- **B2.** Questions open a line of thinking rather than closing it: no question whose only honest
  answer is yes or no.
- **B3.** The set is bounded — three to five questions. A list of twelve is a checklist wearing a
  costume.
- **B4.** Order is deliberate: the question the team most needs to sit with comes first.

**C · It grows, or it isn't doing its job**

- **C1.** The report demonstrably reads last week's: it builds on, sharpens, or drops a prior
  question, and says which. AC-05 sets the bar at 90 % of reports in weeks 3–6.
- **C2.** No question already answered is asked again.
- **C3.** A prior question the team ducked is asked again, harder, and named as a return.

**D · The instructor's half**

- **D1.** The score is a rubric judgement on *process*, not polish, with the dimension named and
  one line of evidence per dimension — enough that an owner can disagree with it specifically.
  It flags shallow-pattern answers (Part 12) and emits gate-A open or closed.

## 4. Known constraints

- **Pull only.** The single input is the team's published page. No text box, no upload, no
  student authentication, nothing student-supplied beyond what is already public.
- **The workflow fetches, not the agent.** Gemini Enterprise's URL Context tool returns a summary
  rather than the page, with no toggle for raw retrieval — confirmed by the platform's own
  assistant — and a summary drops the source list and rewrites the team's sentences (run 4). The
  agent must receive full text, or the questions quote words no student wrote.
- **Tool invocation cannot be guaranteed.** Whether the agent calls Google Search is a model
  heuristic; instructions raise the odds and settle nothing, and Agent Designer does not expose the
  thinking budget that would give the model room to plan. Source verification is therefore not
  something this agent can be relied on to do — it belongs in the workflow, or it is not in the
  design.
- **The runtime returns one response and routes nothing.** Splitting the two audiences is the
  caller's job, by parsing the headings or by using two agents. Nothing in the platform keeps the
  rubric away from a student; only the surrounding design does.
- **There is no per-agent spend cap**, and Cloud Billing budgets alert rather than stop. ADR-0009
  promises a hard cap, and a billing alert is not one. Either the promise softens to a monitored
  cap, or someone builds the budget-alert-to-Cloud-Function path that actually disables billing.
- **That boundary is what keeps NFR-11.** Interview material cannot reach the model service
  through this gate, because the gate cannot be handed anything. Do not add an input that breaks it.
- **One scheduled run a week**, weeks 2–6. The schedule is the protocol (§6.4).
- **Course-owned project, pay-as-you-go, hard spend cap** (ADR-0009). No student holds a seat, an
  account, or an identity in the owner's tenant.
- **No student write access** to prompts, rubric or configuration (FR-10). The graded party does
  not hold the controls.
- **The rubric and its scores never enter `site/` or any student-readable path.** The repository is
  public; there is no such thing as a secret in `site/`.
- **Report in the channel before the weekly block** (NFR-04), so a team can act on it in the
  session.
- **Every automated step keeps a manual one** — here, an owner running the agent by hand.
- **Eight to ten teams, five runs**: roughly fifty reports a run. Small enough that cost is a
  rounding error and large enough that nobody reads them all by hand.

## 5. Out of scope (for now)

The instructor dashboard as one screen (LRD §6.6) — this delivers a report and a score per team
per week into whatever the workflow writes to, which is enough to run the gate and short of §6.6.
The difference is admitted rather than designed around. Also out: the peer gate, which is human and needs
no system; any interactive or conversational mode; resubmission, appeal, or a second consult;
publishing reports to the site or to other teams; any automatic consequence of a closed gate
beyond the signal itself; and anything that touches interview material, ever.

## 6. Open questions and assumptions

- **Open — the clock.** Publication deadline `[day, time]`, run at `[day, time]`, at least `[N]`
  hours before the weekly block. Nothing else in this document works until these three are numbers,
  and they must be on the week page before week 2, not announced in the session.
- **Open — region and residency.** Gemini Enterprise supports EU data-residency zones on Standard
  and Plus; the Agent Platform's Interactions API is documented as `global`-only. Student writing
  is not the personal data ADR-0013 route 4 protects, but the question needs an answer before week
  2. Fallback: pin the model call to an EU Vertex endpoint and have the workflow call that.
- **Open — cold start.** Week 2's report has no prior history, so criteria C1–C3 cannot apply to
  it. Either week 1's by-hand Socratic round is written up as the first entry, or week 2 is
  audited against A and B only. The first is better and costs someone an hour after the kick-off.
- **Open — who owns the project.** It runs on one person's account and billing. Before a second
  cohort, either the institution owns it or the gate leaves when they do.
- **Open — the roster.** The workflow's input is a list of team page URLs. Where it lives, who
  updates it, and who notices when a renamed page silently stops being read.
- **Assumed — the automated gate runs weeks 2–6, five times.** Week 1 has no handbook page to
  read; its checkpoint is the research proposal and the PRD, and the kick-off design already has
  the two lecturers running that round by hand.
- **Assumed — a team that publishes nothing gets no report**, and gate A does not open. This
  follows from the hard deadline and should be said out loud in week 1.
- **Assumed — the report goes to the team and the owners only**, not to the peer team and not to
  the cohort. Publishing reports across teams is a separate decision with its own consequences.
