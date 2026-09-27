# ADR-0018: What the weekly reading weighs — the quality of the document, or the evidence of learning

## Status

Proposed

## Context

Every instrument the owners use to read a team's week scores a document. The PRD,
blueprint and coherence sheets each hold twenty items or so, each 0–3, and each asks
whether the page in front of it is specific, carried by evidence and good enough to
build on. That was a fair question in week 1. By week 3 it has stopped separating
teams.

The reason is the tool the course asks students to use. A team with an agentic CLI
and a template produces a complete, well-structured, plausibly sourced document in
an evening, whether or not anyone in the team understood what it says. Content and
result are now the cheap part of the work. What is still hard, and what the course
exists to teach, is the part around the content: deciding what to test, noticing
that an output is wrong, rejecting it for a reason, checking quality before it
ships, and doing better next week because of what went wrong this week. The
scoresheets see almost none of it. The PRD sheet admits as much in its own last
section: it rewards a PRD that *points at* a failure log, and only a person can
check that the failures happened.

Two things already in the design lean the same way and have no instrument behind
them. ADR-0011 made the revision trail — what the gates asked and what the student
changed — a quarter of the portfolio. The week 3 page started the decision log, one
entry per choice, recording what failed and what changed. And the week 4 mini-CBI
asks every team, among five questions, what did not work that week and what they
did about it.

What breaks if this stays undecided: the owners' weekly reading keeps rewarding the
part AI does well, the teams learn from the scores what is rewarded, and the
interview at the end has to find learning that nothing measured along the way.

## Options considered

**Keep scoring documents and read learning informally.** No new sheet, no new work.
It leaves the weekly reading pointing at the wrong thing, and it is the position the
course is in now.

**Add learning items to each document sheet.** One sheet per document, as now, with
three or four extra rows. It spreads the evidence of learning over six sheets that
each see one document, when learning shows up *between* documents and between weeks,
and it lets forty document items outvote four learning items by arithmetic.

**Replace the document sheets with a learning sheet.** It makes the point sharply
and throws away the only instrument that tells a team whether its PRD is good
enough to build on. A team that learns a great deal and ships a document nobody can
build against has still not done the job.

**A separate learning sheet per team per week, weighted above the document total.**
The document sheets stay as they are. A second sheet reads the week as a whole
against a handful of items, each with the written evidence that counts for it and
the part only a conversation can judge. The two totals are combined with the
learning total weighted twice the document total. It costs a second sheet per team
per week and a place in the week where the conversation happens.

## Decision

**Each team's week is read on a learning sheet as well as on its document sheets,
and in the combined reading the learning total weighs twice the document total.**

The learning sheet holds five items, each scored 0–3:

1. **An assumption tested** — which one, how, and what came out.
2. **What went wrong, and what changed** — the failure, and the change it caused.
3. **AI output rejected or adjusted, and why** — the judgement a team exercises over
   what its tools produce: taste.
4. **How quality was assured** — what was checked before the work was handed in, by
   whom, against what.
5. **Growth against last week** — what the team does now that it did not do before.

For each item the sheet names the written evidence that counts — the failure log,
the decision log, the difference between versions, the question register — and the
part that only a conversation can judge. The written part can be read in advance;
the score is settled after the conversation, and the conversation can move it
either way.

The weighting sits above the total because it is the point of the decision. Both
totals are turned into a percentage and combined as two parts learning to one part
document. A team with a polished document and nothing on the learning sheet reads
lower than a team with a rougher document and a clear record of what it tried,
what failed and what it changed. The ratio is a first setting, to be calibrated
against the first cohort as the document sheets' bands are.

The sheet itself is kept outside this repository, with the document sheets, for the
same reason: its worth depends on a team not having written to it.

## Consequences

- **A reason to stage failure.** Rewarding what went wrong invites teams to report
  failures they did not have, or to fail on purpose. The written evidence alone
  cannot tell. That is why no item is settled on paper, and why the sheet rewards the
  change a failure caused rather than the failure itself.
- **The weekly reading needs a conversation.** Half of every item is judged in the
  room. The week 4 mini-CBI is the first place this happens; if the course has no
  such moment in a later week, the learning sheet is only half filled in, and the
  sheet should say so rather than guess.
- **A second sheet per team per week** for the owners to read and complete, on top
  of the document sheets. The intake dashboard reads twenty-item sheets and does not
  yet show this one.
- **The document sheets lose their standing as the weekly verdict.** They still say
  whether a document is good enough to build on. They no longer say how the team is
  doing.
- **The criteria still owed under ADR-0011 have a direction.** The interview and
  portfolio criteria are not written yet. This record does not decide them, but a
  set that weighs the result above the learning would now contradict the weekly
  reading, and should have to say why.
- **The gates stay informational.** Nothing here scores a gate. What a team did with
  a gate's questions is evidence for items 2 and 5, as ADR-0011 already allows.

## Related

- [ADR-0011](0011-continuous-assessment.md) — continuous assessment; the revision
  trail in the portfolio is the same evidence read from the student's side.
- [ADR-0010](0010-ael-arc.md) — the AEL arc, whose failure log and decision log are
  the main written evidence for this sheet.
