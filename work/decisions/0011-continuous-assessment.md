# ADR-0011: Continuous assessment — an individual portfolio alongside the final interview

## Status

Proposed

## Context

ADR-0007 put the whole mark on the final criterion-based interview, with the
team's frozen contribution as its evidence base. That record named the problem it
was not solving: a student who contributed little to a good contribution can
still be marked down *only if the interview surfaces it*, and the interview is a
single conversation at the end of the run.

Three pressures have since made that single point of measurement look thin.

The first is timing. Every instrument in the design fires after the work is over.
A student who is drifting in week 2 receives nothing that changes their behaviour
until the mark arrives, by which time the six weeks that produced it are spent.
The two weekly gates were built to carry that load, but they are deliberately
informational — under the motivation design in the LRD's Part 2 they produce
questions, never verdicts — so they cannot, and should not, tell a student where
they stand.

The second is attribution. ADR-0005 makes field research a team obligation, and
ADR-0007 observes that a student can therefore hold a mark for research skills
without having conducted an interview. The same holds across the technical track:
four build roles produce four different weekly outputs, and nothing in the design
records which student produced which.

The third is that the run is adaptive. `course-outline.md` decides each week from
what the previous week showed, and the evidence it decides on is currently
informal — what the teaching team happened to notice in the room.

What breaks if this stays undecided: the module reaches its assessment period
with one instrument, no individual record of who did what across six weeks, and
no artefact a student can point at to contest a mark.

## Options considered

**Leave the mark entirely on the interview (ADR-0007 as it stands).** Cheapest,
and defensible — a criterion-based interview genuinely can distinguish two
members of the same team. It leaves every problem above in place, and it makes
the mark rest on forty minutes of talking about six weeks of work.

**Weight the weekly published pages.** The pages already exist, so this costs
students nothing new. But the page is a *team* artefact, so it re-imports the
attribution problem the interview was meant to solve; and scoring the weekly
output puts a grade next to the two gates, which students will then read as
rehearsal for a mark rather than as an invitation to revise. That is the specific
failure the informational-feedback rule exists to prevent.

**Marked milestones in weeks 3 and 6.** A real mid-course signal, and cheap. Two
snapshots of a team artefact still say nothing about who did what, and a
milestone in week 3 of an adaptive run marks students against a specification
that was written the week before.

**An individual portfolio, built weekly, marked once.** Each student keeps a
running record of what they contributed, what their build role produced, what the
gates asked of them and what they changed as a result. Strong attribution,
continuous by construction, and it produces exactly the individual evidence the
interview currently has to manufacture in the room. It costs every student a
weekly writing habit and both markers a second pile of documents — the reason
ADR-0007 set it aside.

## Decision

**Each student keeps an individual portfolio, built weekly and submitted once at
the end of the run. It carries 30 % of each module's mark; the joint
criterion-based interview carries the remaining 70 %. The two weekly gates remain
informational and unscored.**

The portfolio is one document per student, added to each week, drawing on four
things the course already produces:

1. **The team's published page** for that week — what the team put out.
2. **The student's own contribution to it** — named, specific, and honest about
   size.
3. **The revision trail** — what the Socratic and peer gates asked, and what the
   student changed as a result. Not whether the gate was satisfied; what moved.
4. **The build role's weekly output** — the PRD revision, the failure log, the
   test results, the deployment: whatever that student's AEL role produced.

Each lecturer reads the same portfolio from their own side and marks it against
their own module's criteria, exactly as they do the interview. There is one
portfolio, not two.

This is the option ADR-0007 rejected, and the reason for reversing it is that
ADR-0007 weighed the portfolio's cost against a *hypothetical* attribution
problem. The intervening decisions made the problem concrete: ADR-0005 made
fieldwork collective, ADR-0010 gave each build role a distinct weekly output, and
`course-outline.md` committed the run to deciding each week from evidence the
design does not otherwise capture. The portfolio is now doing three jobs, not
one, and at three jobs it earns its cost.

The 70/30 split keeps the interview dominant, because the interview remains the
only instrument that can test whether a student can *use* what the portfolio
claims they did. A portfolio that carried half the mark would reward diligent
recording over understanding.

The gates stay unscored for the reason the LRD's Part 2 gives: feedback that
carries a mark stops being information and becomes a verdict, and students
optimise against verdicts. The portfolio records *what the student did with* the
gate's questions, which is assessable without making the gate itself an
instrument.

This record supersedes ADR-0007. Two of that record's decisions carry forward
unchanged and are restated here so that nothing is lost: **teams still submit
their own contribution separately before the editorial merge**, and **the
role-relevance reflection remains a standard part of the interview** — the
student is asked which of the four build roles needs which of the handbook's
findings, and why.

## Consequences

- **The published promise changes.** `site/index.html` states, inside a box
  headed *settled before week 1, will not move*, that "nothing you hand in during
  the six weeks carries a mark". That is now false, and the site, the outline and
  the LRD must all be corrected before the cohort is told anything. Doing this
  after week 1 would be substantially worse than doing it before.
- **Students gain a weekly obligation.** Roughly a page a week, every week, on
  top of the team page. For a student carrying paid work alongside the minor this
  is the most expensive thing the module has added, and the weekly bar must stay
  genuinely small or it will be met by padding.
- **Both markers gain a second pile.** Four portfolios per team, read twice, once
  from each side. At six teams that is twenty-four documents per lecturer. The
  format must be short and fixed, or marking will not happen.
- **Honest self-report is being assessed, which creates a reason to overstate.**
  The portfolio claims a contribution; the interview is where the claim is
  tested. The criteria must say that an unsupportable claim costs more than a
  small honest one, or the instrument rewards the wrong thing.
- **A student who does little now leaves a record of doing little**, weekly and
  in their own words. That is the point, and it will be uncomfortable in a way
  the interview alone was not.
- **The portfolio becomes the adaptive run's evidence base.** What the teaching
  team decides for week N+1 can now rest on what students wrote about week N
  rather than on what was noticed in the room. This is a benefit that only
  materialises if the portfolios are actually read weekly, which nothing in the
  design yet requires.
- **The criteria are now due twice over.** Both criterion sets already had to
  cover the interview; they must now also say how the portfolio is judged. Until
  they are published, 30 % of each mark rests on an unstated standard — a worse
  position than the one ADR-0007 left, and the reason the criteria are now the
  most urgent piece of writing in the module.
