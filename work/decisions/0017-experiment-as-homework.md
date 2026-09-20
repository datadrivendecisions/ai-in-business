# ADR-0017: When the week 3 experiment runs — in the session, or alone at home before week 4

## Status

Accepted

## Context

[ADR-0016](0016-experiment-service.md) decided how the week 3 experiment collects
results, and every line of its reasoning rests on one assumption: that thirty-two
students run it at the same time, in one room, inside a 150-minute block. That
assumption is what made a live dashboard worth a service, what made ten minutes
of pasting the wrong trade, and what set retention at a single teaching day.

The module owners have decided the experiment is not run in class. Everybody does
it alone, at home, in the week between the third and fourth sessions, and week 4
opens on what the cohort produced. The reasons are the owners': a 150-minute
block spent on one exercise is over half the contact time of the week, and the
same exercise costs twenty-five minutes when nobody has to wait for anybody.

That is a teaching decision and not this record's business. What is this record's
business is that ADR-0016 cannot stand as written once it is taken. Three things
in it are now false or unsafe:

- **Retention.** A purge at 19:00 on the day of the session deletes submissions
  that arrive on the Tuesday, the Wednesday and the Thursday. Point 5 of ADR-0016
  would quietly destroy most of the data the exercise exists to produce.
- **The rationale.** "Thirty-two people watching a difference appear and then
  being asked what it licenses is the session" is the stated reason to prefer a
  service over a paste box. Nobody watches anything appear now.
- **The ordering constraint.** The experiment's design holds four topics back
  until after the run — confirmation bias, selective exposure, devil's advocacy
  and counter-cases — and the agents segment was built to sit after the debrief
  for the same reason. With the run moved to the week *after* the session, any
  of that taught on the Monday is a treatment nobody randomised.

What does not change is everything ADR-0016 decided about the shape of the
collection: one named page, one origin, two routes, numbers and never prose, no
per-student route, submit as the consent act, an instructor-only dashboard whose
interpretation comes from a fixed set of sentences, and a service separate from
the Socratic gate. Those were argued on grounds that have nothing to do with when
the students press the button.

## Options considered

**A. Keep ADR-0016 as it stands and run the homework inside one evening.** One
named evening before 19:00, and the purge never has to move. It keeps the record
true at the cost of making the assignment a deadline students will miss for
reasons that have nothing to do with the course — a shift, a train, a flat
battery — and each miss is a lost row that cannot be recovered.

**B. Keep the nightly purge and copy the aggregate out each evening.** No code
changes; an owner opens the dashboard before 19:00 every day and keeps the
numbers. It turns a scheduled job into a human obligation on five consecutive
evenings, and a missed evening is silent.

**C. Move the deletion to the end of the week 4 debrief.** Retention becomes the
exercise rather than the day: submissions live from the Monday they are set to
the Monday they are shown, and the purge runs that evening. The consent sentence
on the page changes from one day to eight, and a student who withdraws does so
against a window they can see written down.

**D. Turn the collection off and let the tool stay in the browser.** Honest, and
it returns the site to the no-network rule. It also throws away the cohort
result, which is the only thing that turns twenty-five minutes of private
clicking into a lesson about what a comparison licenses.

## Decision

**The experiment is individual homework done between the week 3 and week 4
sessions, its data is deleted on the evening of the week 4 debrief rather than
the evening of the week 3 session, and nothing that the experiment manipulates is
taught before the cohort has run it.**

Four things are decided here.

1. **The run is individual and asynchronous.** One student, one laptop, one
   sitting of about twenty-five minutes, any time before the week 4 session. The
   team number keeps its only job — deciding which of the two rounds carries the
   assistant — and stops being a card on a table.
2. **Retention is the exercise, not the teaching day.** The purge moves to the
   evening of the week 4 session. This is a change to point 5 of ADR-0016 and to
   nothing else in it: the TTL, the scheduled job and the sentence on the page
   all say the same date, and the page says it to the student before they press
   the button.
3. **The four held-back topics move with the run.** The AI agents segment leaves
   the week 3 deck for week 4, where it can point at a round every student has
   just done. Nothing on a published page, a card or a note may say what the two
   rounds differ in until the debrief.
4. **The live dashboard stays, and stops being live in the sense that mattered.**
   It is the same page and the same two routes; it is now something the owners
   reopen across a week rather than watch for twenty minutes. That is a weaker
   justification than ADR-0016 gave, and it is not retracted here, because the
   service exists and the alternative — thirty-two students mailing lines to a
   lecturer over eight days — is worse than the paste box ever was in a room.

ADR-0016 is superseded by this record rather than amended, because its status is
Accepted and its reasoning has to stay readable: it is the record of what was
decided when the experiment was still a thing the room did together.

## Consequences

- **The pedagogical payoff is weaker, and the record should say so plainly.** A
  result read off a screen a week later is not the same as watching it arrive.
  What the debrief keeps is the part that was always the lesson — what the
  numbers license and what they do not — and it loses the moment that made the
  room care about the answer.
- **The experiment is now primed by its own course.** Students meet research
  methods on the Monday and run the exercise on the Wednesday. The week 4 debrief
  gains a limitation the cohort can see for itself, which is teachable and is
  also a genuine weakness in the data. It is named in the manual so that nobody
  discovers it as a surprise while reading the interval.
- **Participation becomes a number nobody controls.** In a room, the count rises
  to the number of people present. Spread over a week it rises to however many
  people did their homework, and the comparison gets whatever that is. The design
  already reports the smallest effect its sample could detect, so a thin week
  shows up as a wide interval rather than as a false result.
- **Withdrawal gets easier to honour and harder to bound.** A student can ask for
  their row to go at any point in eight days instead of before 19:00 on one, and
  the window is written on the page they submit from.
- **A second week would need a second decision.** Nothing here licenses keeping
  data beyond the debrief it was collected for. If a later cohort's results are
  ever wanted for comparison, that is a new record, not an extension of this one.

## Related

- [ADR-0016](0016-experiment-service.md) — superseded by this record; the shape of
  the collection is unchanged and its reasoning still stands for everything but
  timing and retention.
- [ADR-0014](0014-socratic-gate-architecture.md) — the record that licensed a
  narrow endpoint at all.
- [ADR-0015](0015-gate-runtime.md) — the runtime this service borrows.
