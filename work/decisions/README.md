# Decision records

Design decisions for the AIBS redesign and its technical sister module AEL, recorded
as they are taken. These are curriculum decisions, not software architecture, but
the form fits: a curriculum is revisited every year, and the value of a record is
that next year's discussion can start from why last year's choice was made rather
than from scratch.

Not published. `site/` goes live; this folder does not, and these records are
never promoted to it. They are, however, in a **public repository** — so they
refer to roles ("the research lecturer", "the technical lecturer"), never to
names, and carry no timetables or personal notes.

## The rule

**An accepted record stops changing.** If a decision turns out to be wrong, write
a new record that supersedes it and set the old record's status to `Superseded by
ADR-NNNN`. That status line is the only edit an accepted record may still
receive, and [`check-adrs.sh`](../../.github/scripts/check-adrs.sh) enforces it in
CI. Silently rewriting the reasoning is what turns a decision record back into an
ordinary document.

Status is one of `Proposed`, `Accepted`, `Rejected`, or `Superseded by ADR-NNNN`.

## Writing a new one

Copy [`template.md`](template.md), take the next free number, fill in the five
sections, and add a row below. A record in `Proposed` status still states a
decision — the point is to force a yes or a no, not to host an open question.

## The records

| # | Decision | Status |
|---|---|---|
| 0001 | [Teaching mode — taught curriculum or student-led research](0001-teaching-mode.md) | Proposed |
| 0002 | [Module calendar — six teaching weeks plus consolidation, or seven](0002-module-calendar.md) | Proposed |
| 0003 | [Module structure — two separate modules or one co-taught module](0003-module-structure.md) | Proposed |
| 0004 | [Whether every theme must be grounded in the AI Wiki](0004-grounding-requirement.md) | Proposed |
| 0005 | [Whether field research at companies is mandatory or optional](0005-field-research.md) | Proposed |
| 0006 | [What the sister module builds — a client prototype or the research platform](0006-what-the-sister-module-builds.md) | Proposed |
| 0007 | [Assessing individuals when the deliverable is one collective handbook](0007-individual-assessment.md) | Superseded by ADR-0011 |
| 0008 | [Module names — AIBS and AEL replace DIAIA and AEAIS](0008-module-names.md) | Proposed |
| 0009 | [The AEL build environment — students bring their own agentic CLI](0009-build-environment.md) | Proposed |
| 0010 | [The AEL arc — two spines, one element a week, from vibe coding to agentic engineering](0010-ael-arc.md) | Proposed |
| 0011 | [Continuous assessment — an individual portfolio alongside the final interview](0011-continuous-assessment.md) | Proposed |
| 0012 | [A sector per team, and what stays invariant when the sectors differ](0012-sector-allocation.md) | Proposed |
| 0013 | [Where work is handed in — HANDIN, Teams, or one route per artefact](0013-hand-in-routes.md) | Proposed |
| 0014 | [How the Socratic gate runs — the platform, and what carries the traffic](0014-socratic-gate-architecture.md) | Proposed |

ADR-0001 is the keystone. ADR-0002, ADR-0003 and ADR-0006 follow from it and
should not be accepted before it is.

## Where these came from

All seven are the open tensions from a comparison between two design documents:
the three paired redesign sketches for AIBS and its sister module, and a
colleague's proposal for the handbook module. Both live outside this folder and
outside the site — the sketches vary the *technical ambition* of the sister
module, the proposal varies the *pedagogy* of AIBS, and neither had noticed that
they disagree about what kind of course AIBS is. Each record names one tension
and puts a decision on the table.

Neither source is linked from here. They sit in `project-documentation/`, off the
site, and the integrated LRD in `site/` is the document that reads them together.
