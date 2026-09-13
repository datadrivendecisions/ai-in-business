# Week 2 — instructor notes

Speaker notes for `site/week-02-slides.html`, one block per card, keyed by the card's id.
`build_deck.py` folds them into the presenter deck, the PDF and the PPTX. Drafted from the
slides, `session-plan-week-02.md` where it still applies, the criteria page and the six-documents
page; edit freely. The folder is public, so nothing that only works if a student has not read it
goes here.

## s1

Session of Monday 14 September, about four hours with one break, both lecturers.

Sequel to week 1's Draghi discussion: that was Europe's position; this week is what a single SME depends on, and what an AI tool gives you when you ask it who leads.

Goal: every team leaves paired with its peer-review partner, with both assignments understood and started, and with the way of working said out loud.

## s2

Five parts. Suggested split, to adjust on the day:

- Questions on the homework, 20 minutes
- Review of the proposals and the PRDs, 40 minutes
- Assignment 1 explained and started, 40 minutes; break
- Assignment 2 explained, 20 minutes; team work time
- Way of working and close, 20 minutes

Two minutes somewhere early on what week 1 showed and what we changed as a result. Keep it concrete; this is where the adaptive run earns its credibility.

## s3

Open the floor before anything else. Three prompts:

- The course website: anything unclear? The six-documents page and the week map are new since last week.
- The Draghi address: anything to revisit?
- The AI Maturity Ladder: ask them to have their own result at hand — they were told to keep a copy. Then: where does your target SME sit, and where do you?

## s4

What the proposals showed, as three review points:

- Sub-questions per theme: concrete questions that map onto internal and external analysis, not one broad theme.
- A logical structure: themes ordered so the whole reads as one research plan.
- The link forward: from structure to product — how this feeds the handbook, and the tool that will build it.

Restate, before the PRDs: neither gate is scored, and neither ever will be. Students will assume otherwise now that the portfolio carries 30 %.

## s5

Eight drafts, read against the twenty published criteria. The user journey, the users and the functional requirements were solid nearly everywhere. What was missing is one thing, seen at three points of the same argument: nothing in the draft could be proven wrong.

The three points are the criteria page's own order, and they are a chain:

- **Before** is the evidence for the pain point (A3): something observed, in the failure log or the problem analysis, that costs the team time or quality today.
- **Claim** is the hypothesis (A5): this feature will change that observed thing, by roughly this much, by this week.
- **After** is how you will know it works (C3): the measures, and the cadence, that would show the claim held or failed.

Take one away and the other two stop working. A hypothesis without a measured pain has nothing to improve on. A measure without a hypothesis is a number nobody acts on. Evidence without a claim is a complaint. The one team that came closest on all three is the same team each time, which is the point: it is one thread, not three items.

The three quotes are from one draft, shortened, with nothing that names the team or its firm. It is the draft that shows the chain best, because it has all three links on one theme, time, and still cannot be proven wrong:

- Before: the pain is named, and it is time. But it is asserted; nothing shows it. No failure-log entry, no finding from the problem analysis, no number for how long the manual route took last week.
- Claim: the goal says faster. A goal, with no size and no date; nothing in it could be proved wrong by a week of use. The template: by bringing X to life, Y becomes easier, faster or more reliable for us, and we will see it in Z.
- After: success is one reliable, reviewed page a week. That counts pages, and never time — so the one thing the claim promised is the one thing the measure cannot see. Nor does it say what reliable means, or who checks. Criterion C3: one measure that matters most, one about the product, one about the AI, one guardrail — each with a cadence.

Ask the room: if this team ships and produces one page a week, do we know the research got faster? No. That is the gap.

What the thread looks like when it holds, invented for the course's own platform, not taken from a draft. Say it aloud as one story, or write it on the board:

- **Before.** "In the week-1 spike the agent drafted a page with six sources; two links did not resolve and one quoted a figure the source does not contain (failure log, entries 3–5). The problem analysis found that three of the four of us cannot read the CBS and KvK material in Dutch, so one person did all the source work last week."
- **Claim.** "By giving the platform a source-appraisal step that scores publisher, date and relevance, checking a page's sources takes a researcher under an hour instead of an afternoon. We will see it in the logged review time by week 3."
- **After.** "North star: one published page a week that passes the peer gate without a factual correction. Product measure: hours from first source to published page, logged every week. AI measure: unconfirmable citations per page, counted at every review. Guardrail: pages published that nobody on the team read in full — zero, checked at every hand-in."

The same failure appears in the before, is named in the claim, and is counted in the after. That is what "could be proven wrong" means: by week 3 the review time either fell or it did not.

And the small one: a header. Name, version, date, who wrote it, where the related documents are. Three drafts also ran past three pages; a PRD that has not chosen what matters has not finished choosing.

Set the rest of the discussion from what the hand-ins showed.

## s6

The PRD is the first of six weekly AEL documents: PRD, technical blueprint, knowledge architecture, build plan, and two evaluations. One a week, posted in the team's Teams channel, one to three pages.

The site has one page for all six: the bar each must clear, its criteria, and what happens after posting. Say that part: a lecturer hands the document to the AI tutor; three to five questions come back in the channel; never a score. From this week the tutor also reads the new document beside the earlier ones and asks whether they still describe one platform.

This week's document is the technical blueprint. Its criteria go up before the deadline, like the PRD's — the deadline is on the week-2 page.

Say plainly: the PRD is allowed to change. When the blueprint shows it promised something it cannot deliver, revise it and say why.

## s7

What a part is, for a research platform: a step on the path from a source to a published page — add material, appraise it, translate it, draft, check, publish. Each step is a box; the blueprint names the boxes and what each one does. No code in this document. The developer holds the pen because they will build it, and the whole team reads it because the PRD's promises are theirs.

The architecture-styles wheel exists — microservices, event-driven, layered, CQRS and thirty more. Say plainly that almost all of it is for systems at scale. Their platform is a pipeline, and naming that is the whole style choice. The same for the "system design blueprint" ingredients lists on the web: seven ingredients, of which two apply here — the high-level architecture and the data flow. Scaling, load balancing, replication, dashboards: not this document.

The first part most teams will draw is the context file the platform always reads: target SME, quality criteria, out of scope. That is this week's context-layer block seen from the blueprint's side. One to three pages; a one-page blueprint that clears the bar beats three that do not.

## s8

What "passes between parts" means: a file with a fixed shape. That file is the contract, and it is what lets two people build two parts at once without talking every hour. Ask them to name the file and its shape for at least one seam.

The line nothing may cross, with our own example: interview material never reaches a model service. Their platform has an equivalent, and the blueprint says in one sentence where it runs and what keeps it there.

From this week the tutor reads the blueprint beside the PRD and looks for three things: a promise in the PRD that no part carries, a part that no promise asked for, and a departure — which is allowed, if the blueprint says so and the PRD is revised with a version, a date and one line of reason. A blueprint that quietly drops a promise is exactly what it finds.

Dates, for those who need them first: due before the week-3 session, posted in the team's Teams channel. Three to five questions come back. No mark.

## s9
We look at every assignment this way, and so should you. Make the split visible in your own work: what did you write, what did AI draft, and what did you check?

The rule underneath it, for the handbook pages: every claim needs an appraised source, and "the model said so" is not one.

## s10
Two assignments this week, and they are one lesson in two halves. Assignment 1 makes bias appear on purpose; assignment 2 makes the antidote — criteria and strategy — explicit.

Walk both briefly here; the next slides carry each in turn.

## s11
Three prompts, three separate conversations. Ask AI to argue that the US dominates AI. In a new conversation, that China does. Then Europe.

No cross-referencing: each article is written as if it were the only one being produced.

Then read the three back to back. Stop here and ask what they notice before showing the next slide; the takeaway lands harder if the room says it first.

## s12
AI gives you what you ask for, not what is true. Ask for the US case and you get a convincing US case; the same for China, the same for Europe.

Source diversity is the fix, and it is what actually teaches you who leads. A cleverer prompt does not.

It matters twice: for business judgement, informed and unbiased; and personally, knowing your own starting position.

Bridge to dependency, from the plan for this week: who builds these systems, who funds them, who could buy them? Open weights, closed weights, hosted API, on-premise — what does each mean for a forty-person firm with no IT department? What would your target SME lose if its tool changed price, terms or European availability?

## s13
The question: good-quality reports on the geopolitics of the AI race — US, China, Europe.

Two things made explicit and written down: what makes a source good quality here, and how you searched and why.

Then AI, carefully: a first analysis of your sources with AI, with your strategy made explicit too. The order matters — sources and criteria first, the model second.

## s14
Partner teams. Pair by wall position: 1 with 2, 3 with 4, 5 with 6. An odd count makes a ring of three. Say once: this pairing holds for the rest of the run. They read everything you publish; you read theirs.

The Socratic agent: an AI tutor, run by us, questions every team's thinking. It reads the page you publish and the document you post; questions come back in your Teams channel. Informational, not scored, and it never will be.

Where things go: the document in your team's Teams channel; the page handed in by being published.

Portfolio: the second entry is the first with the four standard questions, because there is now a page and both gates have run.

Field research opens. Nobody approaches a company before the consent text is signed off, and interview material never goes through a free tier or the tutor.

## s15
Every time we spot a habit worth keeping, we turn it into a rule. Rule 1: before taking a break, always set AI to work.

Rule 2 is added together in the session. Capture it on the board and put it in the deck afterwards.

After class: decision-log entry, and read the second portfolio entries — "what the gates asked and what I changed" is the evidence base for planning week 3.
