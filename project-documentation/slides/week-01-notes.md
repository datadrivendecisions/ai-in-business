# Week 1 — instructor notes

Speaker notes for `site/week-01-slides.html`, one block per card, keyed by the card's id.
`build_deck.py` folds them into the presenter deck, the PDF and the PPTX. They are the
lecturer's words, drafted from `session-plan.md` and the week 1 page; edit freely. Nothing
here is secret — the folder is in a public repository — so the *ask, never comment* prompts
and anything that only works if a student has not read it stay out of this file.

## s1

Session of Monday 7 September, about four hours with one break, both lecturers in the room.

Goal: everyone leaves in a team of four, with both first drafts started, and we leave with a read on where the group starts.

Pre-reading was Draghi's address to the European Parliament, eleven pages. Ask who read it; do not make a point of it yet.

## s2

Two modules, taught as one pipeline to the same teams.

- AEL, the technical track: builds the tool. Witek.
- AIBS, the research track: decides what the tool's output must achieve, and judges whether it does. Meike.
- One research problem holds both: what do European SMEs need in order to implement AI in their business?

Say once: you never work on one module at a time. Every week has both hats.

## s3

Keep this short: all of it is on the course page in writing, and they will read it again.

- The handbook is the end goal — what a regional SME owner needs to know and decide about AI.
- One new published page per team per week. New page, never an edit to an earlier one, so the trail of thinking stays visible.
- Teams of four; everyone researches; each holds one AEL build role.
- Six Mondays, then an assessment period: consolidated handbook and one joint interview, two marks.

## s4

We run this adaptively. We start with the first assignments, watch what the group can do, and decide week by week what comes next.

Be explicit about the consequence: some things you want to know in week 1 do not exist yet in week 1. Each week's page appears about a week before its session.

Left column is a promise — it will not move. Right column is decided as we go, and that is deliberate, so we pitch the work at the level in the room.

## s5

Timings, 240 minutes:

- 0:00–0:20 welcome and how the module runs
- 0:20–0:55 discussion 1, your experience with AI
- 0:55–1:35 discussion 2, the Draghi report
- 1:35–1:45 break
- 1:45–2:10 team formation
- 2:10–2:25 the two assignments
- 2:25–3:40 team work time, both lecturers circulating
- 3:40–4:00 share-out and close

## s6

Structured round; capture the answers on the board. Say that this is our diagnostic: it shapes the coming weeks, so understating what you can do does not help.

Confidence check by hands, 1 to 5, three times: using AI tools; building something with AI; judging whether an AI output is any good.

Keep a written record of three things: the confidence spread, the job-market and skills answers, and the "want to be able to do" answers. They go into the first decision-log entry after class.

## s7

Framing, about ten minutes, lecturer only.

- What it is: Draghi's report for the European Commission, September 2024, on why the EU falls behind the US and China on growth and productivity.
- Core diagnosis: largely a technology gap. Few large tech firms, and, the point that matters for us, slow to diffuse digital technology into the businesses Europe already has, especially SMEs.
- On AI: Europe will not win by building frontier models alone; it has to get AI adopted across its industrial base.
- Barriers for SMEs: fragmented single market, regulatory complexity, limited access to capital, skills shortages, limited scale.
- Why it is our starting point: the handbook is a small, concrete contribution to exactly that diffusion problem.

## s8

Guided discussion, about 25 minutes. The slide carries three questions; there is a fourth to ask between the second and the third:

The report's lens is competitiveness. What does that lens underweight — trust, dependency on foreign vendors, jobs, data?

Take the first question back to the board from discussion 1: the tools they named, and who makes them.

The last question is the bridge into the assignments. End on it.

## s9

Teams of four, formed now, together for the run. Each member takes one build role; everyone also researches.

Sanity check per team: four people, four roles, at least one willing to drive the command line, at least one who knows this region or can work in Dutch. If a team is missing one of the last two, say so now; it is far cheaper to fix in week 1 than in week 3.

Push for four people who are not already a group. A team that formed in the corridor tends to research the firm one of them already knew.

On roles: take the one you want to get better at. If you have never opened a terminal, developer is a legitimate choice.

## s10

Hand out the PRD prompt. The platform helps the team research and produce the handbook, one page a week. Its user is the team itself; the SME owner is the downstream reader.

Walk the six sections. On constraints, say the four out loud: you direct an agentic CLI rather than hand-code; you reuse the wiki and the site; a non-coder must be able to run it; every automated step keeps a manual fallback.

Add the point the slide does not carry: much of the source material is Dutch — CBS, the Chamber of Commerce, sector bodies, the regional press, probably the interview too. Crossing that gap is a requirement of the platform, not a favour someone does by hand. Say so in the PRD.

The bar: a reader can tell what you are building, for whom, and how you will know it works.

## s11

Hand out the research proposal prompt. Walk the five sections.

On target audience, give the shape of "specific enough": a sector, a size, a region and a decision the owner is actually facing. The week 1 page has the worked example — metal and machine-building firms in the Achterhoek, 20 to 100 staff, spending two days a week turning drawings into quotations. It is there to show the shape, not to be copied.

Research question: one main question, at least four sub-questions, two external and two internal.

Quality criteria: this list becomes the checklist the handbook is later judged against. Methodology: desk research plus one SME visit in weeks 2 to 4, and which questions each serves.

## s12

The two documents constrain each other. The proposal's quality criteria and the PRD's output qualities describe the same thing from two sides. If they disagree, one of them is wrong; find out now, not in week 4.

Team work time, 2:25 to 3:40. Both lecturers circulate: AEL on the PRD, AIBS on the proposal. Push every team, early and repeatedly, to name a concrete target SME: sector, size, region.

## s13

Share-out: each team, one sentence on who the handbook is for, and one open question they are stuck on.

Then the close, four points:

- Where the drafts go: post both in the team's Teams channel, due by the start of next session. The PRD is the first of six weekly AEL documents; the site lists them.
- The individual portfolio: one document per student, added to every week, 30 % of each mark; the interview carries the other 70 %. Say the four standard questions. Week 1's entry is shorter: what you contributed, what your role did first, and what you do not understand yet. Half a page.
- Two things the instrument lives or dies on: write it the same week, not at the end; and an honest small contribution scores better than an unsupportable large one, because the interview tests the claim.
- The two weekly gates are still not scored. Say it explicitly; students will assume otherwise now that something weekly carries a mark.

Next week is decided from what we saw today, partly from the "what I do not understand yet" answers.

After class: write the first decision-log entry, and read the portfolio entries.
