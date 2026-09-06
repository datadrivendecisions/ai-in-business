# ADR-0008: Module names — AIBS and AEL replace DIAIA and AEAIS

## Status

Proposed

## Context

The research module has been called DIAIA — Decision Intelligence and AI
Agents — since before the redesign, and the sister module was given the working
name AEAIS — Agentic Engineering & AI Systems — by the sketches. Neither name
survives the decisions above.

Under ADR-0001 and ADR-0003, DIAIA is the module that researches the business,
economic and societal side of AI for SMEs, and under ADR-0006 the sister module
is the one that builds the agents. So the module with "AI Agents" in its name
is the one that does not build them, and the module that does build them is the
one whose name a student cannot tell apart from the other: two five-letter
acronyms, both starting with A, both containing AI, both meaningless until
expanded. Students, SME partners and the examination board all have to be told
which is which every time.

A name is the first thing a student reads about a module, and the first thing an
SME owner sees on the handbook. If the name has to be explained, the split
between the modules has to be explained with it.

## Options considered

**Keep both names.** Nothing to update, no confusion with the course register,
and the existing course code still matches. But the mismatch is permanent, and
the handbook, the LRD and every teaching document keep paying for it with a
sentence of explanation.

**Rename only the sister module.** The research module keeps its registered
name, and the sister module gets a name that says what it builds. Cheaper, but
leaves the "AI Agents" in the research module's name, which is the misleading
half.

**Rename both, so that the names carry the split.** The research module is
named after its subject and the sister module after its activity: a reader
sees "business and society" on one side and "engineering lab" on the other and
needs no further explanation. Costs a pass through every document, a note
wherever the old name still appears in an official record, and a period in
which both names circulate.

## Decision

The research module is **AIBS — AI in Business & Society**, and the technical
sister module is **AEL — Agent Engineering Lab**.

Both are renamed because the misleading half of the problem is on the research
module's side. The two names are chosen to be plain rather than clever: the
research module's name states its subject in words an SME owner would use, and
the sister module's name states what happens there — building agents, in a lab
format — rather than what field it belongs to. Read together they show the
split: subject versus activity, society versus engineering.

Where an old name is part of a record this repository does not own — the
course code in the programme register, the research lecturer's original
proposal, the redesign sketches — the old name stays, and the documents that
cite it say which module it refers to.

## Consequences

- Every document the module owns is updated: the handbook, the LRD, the
  earlier decision records (all still Proposed, so they may change), the
  repository's own description of itself. The previous names appear in none of
  them; this record and a note at the top of the sketches hold the mapping.
- The proposal PDF and the redesign sketches keep the old names. They are
  source documents written before this decision, and rewriting them would
  falsify the sources the other records cite. A note at the top of the sketches
  maps the old names to the new ones.
- The repository slug and the published URL move to `ai-in-business`, the name
  the course carries for students. This record first held them at `diaia`, on
  the grounds that no shared link is worth breaking for a name; that was
  weighed before the site had a landing page addressed to students, and an
  address a student cannot connect to the course they enrolled in costs more
  than the handful of links shared so far. GitHub redirects the repository URL
  and the git remote, but not the Pages URL: `.../diaia/` stops resolving, and
  anything already pointing at it has to be reissued. The module keeps its
  registered course code until the programme changes it; Appendix A of the LRD
  records the module by that code.
- Two names will circulate for at least one cohort, and the published documents
  do not explain the old ones. Whoever introduces the modules to a group that
  knows the previous names has to make the connection in person.
