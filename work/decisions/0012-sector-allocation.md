# ADR-0012: A sector per team, and what stays invariant when the sectors differ

## Status

Proposed

## Context

The cohort is larger than the design assumed. Eight to ten teams will run the
same six weeks, and under ADR-0001 every week is a research assignment ending in
one published handbook page per team. Nothing in the design distinguishes one
team's assignment from another's: every team researches the same theme, about the
same target — "regional manufacturing SMEs" — in the same week.

That produces eight to ten near-identical pages per theme, five times over. The
consolidation week (ADR-0002) then has to merge ten answers to one question into
one chapter, which is editing, not curation, and it is the teaching team that
inherits it. The peer gate has the same problem from the other side: a partner
team reviewing a page that duplicates its own has little to say that it did not
already know.

The obvious fix is to differentiate the *target* rather than the theme: give each
team a sector, keep the weekly theme shared. Five sectors across ten teams leaves
two teams per sector, and the handbook becomes a matrix — five themes by five
sectors — instead of a pile of variants.

The sector list under discussion is: manufacturing (e.g. machinery engineering),
industrial services (e.g. cleaning), business services (e.g. accountancy), local
government (municipalities), and local health care (e.g. hospitals).

That list quietly contains a second decision, which is the one this record is
really about. Three of those five are SMEs. A municipality is not an SME, and a
hospital is emphatically not: both are large organisations with procurement
departments, works councils and IT staff — the three things the course's framing
assumes the target does *not* have. So the question is not only *which sectors*
but **what stays invariant when the sectors differ: the scale, or the region?**

What breaks if this stays undecided: teams cannot be told what they are
researching, and the field-research obligation (ADR-0005) cannot start, because a
team cannot approach an organisation before it knows what kind of organisation it
is looking for.

## Options considered

**Leave it: every team on SMEs in general.** No new decision, no rewriting. It
keeps the duplication, hands the consolidation week ten versions of one chapter,
and weakens the peer gate exactly where it was supposed to be sharpest. It also
lets every team drift toward whichever SME was easiest to reach, so the "sector"
ends up assigned by accident rather than design.

**A sector per team, all of them SME-scale.** Manufacturing, industrial services,
business services, and further sectors chosen for regional density and
reachability — small care providers, construction, agri-food, retail, logistics.
Everything the site, the LRD, the outline and ADR-0005 already promise stays
true. The handbook gains a structure it does not currently have. The cost is that
the teaching team must now hold five sector framings in its head instead of one,
and the shared grounding per theme (ADR-0004) has to stay general enough to serve
all five.

**A sector per team, widened to public bodies and care.** The list as proposed,
municipalities and hospitals included. Two real arguments for it. First, access:
ten teams must each find an organisation willing to be interviewed within about
two weeks, and a municipality has a public contact point and an obligation to
answer, where a forty-person machine shop has neither. Second, regional
relevance: these are large local employers and their AI questions are live.

Against it: they are not SMEs, and the course says "SME" in four published
places. More importantly the questions genuinely differ. A municipality's first
AI question is lawfulness, transparency toward citizens, and the AI Act's
public-sector duties; an SME owner's is whether it pays for itself by next
quarter. A hospital's is patient data before anything else. A handbook that
answers both is two handbooks, and the thing that makes the deliverable useful —
that it is written for one recognisable reader — is what would be lost.

**Widen the scope explicitly, to "organisations of SME scale".** The honest
version of the previous option: keep the sectors, drop the word SME, and admit
small municipalities and GP practices and care homes while still excluding
hospitals. Preserves the "no procurement department, no IT staff" assumption that
the whole course rests on, and preserves it *by scale*, which is what actually
carries it. The cost is a framing change in `site/index.html`, the handbook
template, the LRD and `course-outline.md`, and the loss of a sharp, sayable
positioning: "regional manufacturing SMEs" is a reader you can picture.

## Decision

**Each team is assigned one sector for the whole run, and the invariant is
scale, not sector: every target organisation is SME-scale — small enough to have
no procurement department, no works council and no IT department.**

Under that rule the proposed list is admitted as follows. Manufacturing,
industrial services and business services enter unchanged. **Health care enters
at SME scale** — a group practice, a dental or physiotherapy chain, a care home —
**and not as hospitals.** **Local government does not enter as a target.** A
municipality appears in the handbook where it belongs: as the *customer, funder
or regulator* an SME deals with, which is a question several teams will have to
answer anyway.

The reason for holding the scale rather than the sector is that every promise the
course has already made rests on scale, not on sector. The claim that a
forty-person firm has nobody to run a pilot, that its owner decides on a quarter
horizon, that a vendor's terms change is an existential problem rather than a
procurement matter — none of that survives contact with a hospital, and all of it
survives contact with a care home or an accountancy practice. Sector is the axis
that makes the handbook *interesting*; scale is the axis that makes it *true*.

**Two teams per sector, and the two teams sharing a sector are each other's peer
gate partners.** The pairing that week 2 currently makes by position in the room
is made by sector instead. A partner that knows the domain gives a sharper review
than a partner that does not, which is the whole point of the gate; and the two
teams are told at the outset to split the sub-question, so that sharing a sector
produces comparison rather than convergence.

**Sectors are assigned by the teaching team, not chosen by teams.** Choice would
concentrate teams in whichever sector a student's family firm sits in, and would
leave the least-reachable sector unstaffed.

## Consequences

- **The consolidation week changes shape.** Five themes by five sectors is a
  table of contents; ten answers to one question is an editing job. The handbook
  gains the structure it currently lacks, and the week-7 work becomes curation.
- **The teaching team now carries five framings.** The per-theme grounding
  (ADR-0004) must stay sector-neutral, and the sector-specific work moves onto
  the teams — which is consistent with ADR-0001, and is more preparation for the
  lecturers in weeks where a theme lands unevenly across sectors.
- **Field research gets harder in exactly the sectors that were added for
  access.** Dropping municipalities removes the easiest door in the list. Teams
  in industrial services and small care will need help finding a first contact,
  and the regional network is the teaching team's to lend, not the students'.
- **The published framing needs a small correction, not a rewrite.** The site
  says "regional manufacturing SMEs" and "a real regional manufacturer" in
  several places; under this decision manufacturing is one sector of five. Those
  sentences become wrong the moment sectors are assigned, and the landing page,
  the handbook template and the outline must be corrected before the cohort is
  told anything.
- **Two teams per sector will produce comparable pages, and that is a feature
  only if the split is enforced.** If the two teams are not given distinct
  sub-questions at assignment time, this decision has bought duplication at a
  finer grain.
- **Sector-paired peer partners raise a collusion risk** that the design can
  absorb, because neither gate is scored (ADR-0011) and the interview tests the
  student rather than the page. If a gate ever became an instrument, this pairing
  would have to be reconsidered first.
- **A team whose sector turns out to be unreachable needs a fallback.** ADR-0005
  already allows a persona or archetype where field access fails; that fallback
  now has to be available per sector, and used without treating it as a failure.
