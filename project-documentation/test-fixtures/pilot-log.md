# Pilot log — the Socratic gate

One entry per test run against a fixture. LRD Part 12 asks for a hand-checked pilot before the gate
runs unattended; this is where that checking is recorded, so that a later run can be read against an
earlier one instead of against memory.

Tier-1 material — it quotes the rubric output. Never in `site/`.

---

## Run 1 — 6 September 2026

**Fixture:** `week-02-team-03.html` · **Model:** `gemini-2.5-flash` · **Prompt tokens:** 1979 ·
**Output:** 357 · **History given:** none (cold start)

### What held

The structural split worked on the first attempt: both headings, correct order, and no score,
grade or judgement above `## FOR THE OWNERS`. That was the leak this run existed to test, and it
did not leak.

All four invariants held. Five questions, inside the three-to-five bound, every one of them
quoting a specific sentence from the page — quality A1 clean, which is the failure mode most
reports of this kind have. No praise, no advice, no other team. The control worked too: the
properly appraised Stanford HAI source was not attacked, so the agent was reading rather than
carpet-bombing.

### What failed

**One of five tier-1 defects caught.** Only the Draghi-via-NOS citation, which also carried the
Sourcing score. Missed: the fabricated Van der Meer & Kowalski reference, the false EU AI Act
claim, the Microsoft white paper used as neutral evidence. The unsourced 70% figure was noticed
but probed for its definition — *what does "primary process" mean* — rather than for where the
number came from.

**No question about vetting at all** (quality A4). This is the one the gate exists for.

**Two rubric dimensions were conflated.** Vetting was scored 1 on the strength of the team's
source-bias reasoning, which is Sourcing. Reasoning was scored 1 because the page contrasts two
vendor models, which is the content describing alternatives rather than the team weighing them.
Both justifications quoted the best sentence on a page that also contains an invented citation.

**`Movement: 0` was emitted alongside "cannot be scored".** Contradictory, and a workflow parsing
the number would close a gate the next sentence opens.

### Diagnosis

Two causes, and the larger is the prompt. The instructions named verification as a *subject* for
questions without ever instructing the agent to verify anything. A model that has not checked the
source list cannot ask a pointed question about the source that does not exist — the omission was
in the configuration, not the model.

The second is model choice. Flash is the small fast model, and the specific work that failed —
recognising a fabricated citation, holding a legal claim against knowledge — is where it is
weakest. At roughly 2,300 tokens a run and fifty runs a cohort, the cost of Pro is not a
consideration.

### Changes made

In `../socratic-agent-config.md`:

1. A **check-the-page step** before the questions: every number and legal claim against its
   support, every source for existence, independence and whether it is the work or a summary,
   every recommendation against the firm's own stated capability, and any two statements that
   cannot both be true. Explicitly: find it, never correct it, ask the question that makes them
   look.
2. **Operational definitions** for the four dimensions, with Vetting rewritten to judge what the
   team verified rather than what they cited, and Reasoning to judge the team's own choices rather
   than the content's coverage.
3. **Quote the weakest evidence, not the strongest**, with 0 and a statement of what was looked
   for when a dimension has no support.
4. **`Movement: n/a`** on a first report, never a number, with the gate opening stated as the
   first-report rule rather than as a score.

### Next run

Same fixture, same cold start, `gemini-2.5-pro`. Changing the prompt and the model together means
a better result will not say which fixed it — accept that for run 2, and if it passes, run the
old prompt on Pro once to find out whether the model alone was enough. Target: three of five
tier-1 defects, at least one vetting question, Vetting scored 0 with the fabricated citation as
its evidence.

---

## Run 2 — 6 September 2026

**Fixture:** `week-02-team-03.html` · **Model:** `gemini-2.5-flash` (unchanged) ·
**Prompt tokens:** 2472 · **Output:** 644 · **History given:** none (cold start)

The model was not changed, so this run isolates the four prompt fixes from run 1. That was not the
plan and it is the better experiment.

### Result against the run-1 target

Target was three of five tier-1 defects, at least one vetting question, and Vetting scored 0 with
the fabricated citation as its evidence. The first two were met; the third was met on the score and
missed on the evidence.

**Caught: three of five.** The unsourced 70% figure, the false EU AI Act claim, and Draghi cited
through a summary. Question 3 is the one worth keeping as a reference — *which article specifies
this requirement for all SMEs, regardless of the risk level of the AI system?* — because it points
at the exact wrongness without correcting it, which is the behaviour the whole configuration is
trying to buy.

**Still missed:** the Microsoft white paper used as neutral evidence, untouched for a second run.

**Three of the four fixes worked.** The rubric definitions held — Vetting scored 0 on the AI Act
claim rather than on source-bias reasoning, and Reasoning judged the team's own choices rather than
the content's coverage. `Movement: n/a — first report for this team` came back with no number and
the gate opening stated as the first-report rule.

### Two errors that matter more than the score

**The agent affirmed the fabricated source.** Its Sourcing justification calls Van der Meer &
Kowalski "a published academic paper". It did not merely miss the invented reference; it lent it
credibility it cannot check. On a real gate that is worse than silence.

**It attributed a citation the team never made.** The page reads "Research shows that around 70% of
Dutch SMEs…" with nothing cited at that sentence. The agent's first question says "citing Van der
Meer & Kowalski (2025)" — it filled the gap with the only plausible entry in the source list. A
team reading a question about a citation they never wrote learns that the report did not read them
carefully, and every later report pays for it.

### Diagnosis

Not model size. The instruction asked whether a source "plausibly exists", and a fabricated
citation carrying authors, a journal, a volume and a page range is precisely plausible — the
question was wrong, not the answer. Without retrieval no model can settle this, and Pro would fail
the same way.

### Changes made

In `../socratic-agent-config.md`:

5. **Source existence reframed.** A source that cannot be confirmed is unconfirmed, never genuine;
   never call one published, peer-reviewed or credible without checking; a citation's apparatus is
   not evidence, because that is the shape a fabrication takes. Plus a conditional instruction to
   verify with a search tool where one is available.
6. **A claim with no citation at the point it is made is uncited**, whatever the source list holds,
   and the agent may not assign it to a source itself.
7. **Quote exactly; never describe the page as saying something it does not say.**

### Open — the real fix is a tool, not a prompt

Fixes 5 and 6 stop the agent asserting what it cannot know. They do not let it catch a fabricated
reference, because that needs retrieval. Gemini Enterprise offers Google Search grounding; turning
it on is a platform setting rather than a prompt change, and it is the next thing to try. Note what
it changes about the gate: an agent that can search can also check claims the team made, which
moves it closer to fact-checking than the design intends. The questions must stay questions.

### Next run

Same fixture, same cold start, Flash, with search grounding enabled. Target: four of five, with the
fabricated citation caught and named as unconfirmed rather than as published. Only after that,
compare Flash against Pro on the same prompt — on this evidence the model has not yet been the
binding constraint.

---

## Before run 3 — the two tools, and a fixture defect they exposed

The agent has **Google Search** and **URL Context** enabled. Both change something.

**Google Search closes the gap run 2 could not.** Source existence is a retrieval problem, so the
conditional instruction from fix 5 becomes an instruction: search every source, confirm the work
exists, is by those authors, and says what they are said to say.

**URL Context is the pull mechanism itself.** ADR-0014 has the agent read the team's published page
by URL and nothing else; this is the tool that does it, in the agent rather than in the workflow.
Worth recording in the PRD's §4 as the mechanism behind the constraint, because the constraint was
written before it was known which layer would satisfy it.

### The fixture had to be fixed first

Every source link in `week-02-team-03.html` pointed at `example.org` and resolved to nothing. With
URL Context enabled the agent would have found all four unreachable and could have marked the whole
source list unconfirmed — including the Stanford HAI entry, which is the control that proves it is
reading rather than carpet-bombing. The run would have tested dead links, not fabricated sources.

The sources are now shaped the way the defects need them:

- **Microsoft** → `learn.microsoft.com/en-us/privacy/eudb/eu-data-boundary-learn`, real and
  verified. This sharpens defect 3 rather than softening it: the agent can now open it and see for
  itself that the team's evidence for a sovereignty claim is the vendor's own documentation.
- **Stanford HAI** → `hai.stanford.edu/ai-index`, real and verified. The control survives.
- **Draghi, TechRadar** → citation text with no link, as a student who did not keep the URL would
  leave them.
- **Van der Meer & Kowalski** → still no link, which is exactly how a fabricated journal reference
  presents itself. Search should now fail to find it.

### The risk the tools introduce

An agent that can search can correct, and correcting is what the whole configuration exists to
prevent. Added to the instructions: the tools are for checking, never for teaching — no quoting
what it found, no supplying the right figure, the right article, the better source. The most it may
say is that it could not confirm something, and even that is better asked.

Also added, because search sends text outward: follow only links on their page or reached through
their own sources. Their page is public, so everything reaching a search engine is already public,
and NFR-11 holds. It holds because of that sentence, not by accident.

### Run 3 target

Same fixture, same cold start, Flash, both tools on. Four of five tier-1 defects, with **Van der
Meer & Kowalski named as unconfirmed** rather than as published. Then check the new failure mode
first: does any question hand the team a fact, a figure or a source? A run that catches five of five
by telling them the answers is a worse outcome than run 2.

---

## Run 3 — 6 September 2026

**Fixture:** `week-02-team-03.html` (real source URLs) · **Model:** `gemini-2.5-flash` ·
**Tools:** Google Search, URL Context · **Prompt tokens:** 4038 · **Output:** 566 ·
**History given:** none (cold start)

### The failure mode the tools introduced did not appear

This was the run's first question, ahead of the score. Every one of the five questions is a
question, and not one supplies a figure, an article number, a source or a fact. The tools were used
for checking and not for teaching, which is the behaviour the guardrail was written for.

Run 2's attribution error is also gone. Where it invented "citing Van der Meer & Kowalski", it now
asks *where on the page is it cited* — it saw that the claim carries no citation. Fix 7 held.

### Result

**Three of five again, better grounded.** The 70% claim, the AI Act error and Draghi-through-a-
summary, each sharper than in run 2: the Draghi question now asks them to separate what came from
the report from what came from the summary.

**The fabricated citation is half-fixed.** It is no longer affirmed as "a published academic
paper" — the damage is undone — but it is still not caught. The Sourcing note observes that the
year does not match the claim, which is a confused reading rather than the finding that the work
does not exist.

**The vendor white paper has now been missed three times.** The rule asking whether a source is
independent or is the vendor being discussed has never once fired.

**The rubric improved where the definitions were sharpened.** Sourcing 1 → 0 and Reasoning 1 → 0,
both with correct justifications; Reasoning now judges whether the team justified its own choices
rather than whether the content covers alternatives. `Movement: n/a` came back in the exact form
required.

**Unplanned find:** the questions caught a real internal contradiction nobody planted — Copilot
described as "no setup" beside a use case whose data preparation is "the step most likely to fail".
The two-statements check works.

### Did it search?

The response carries no grounding metadata. With Google Search enabled a grounded answer normally
reports one. If the tool never fired, run 3 tested the new instructions without the retrieval they
depend on, and the Van der Meer result means nothing yet. **Check the trace before drawing any
conclusion from this run about source verification.**

### Change made

8. **The vendor-source rule made concrete.** Name any source written by a company whose product the
   page recommends; a vendor's own documentation cannot settle a question about that vendor's
   product. Stated with why it is easy to miss: the document is usually accurate, and the defect is
   who chose it rather than what it says.

### The gap that now matters more than the remaining defects

Every score in run 3 is 0. On this fixture that is defensible — the page was built to be weak — but
**the rubric has only ever seen a bad page**. Nothing tells us whether it can tell a competent page
from this one, or whether it returns zeros for everything. A gate that cannot discriminate is worse
than no gate, because it looks like it is working.

The next artefact is therefore a second fixture: a page a good team would actually publish, with
appraised sources, a justified choice of angle, and visible evidence of checking what the platform
produced. Expected scores 2–3 across Sourcing, Vetting and Reasoning. If it scores like this one,
the rubric is broken and nothing above matters.

### Next run

Two runs, not one. First, confirm search actually fires and re-run this fixture — target four of
five with Van der Meer named unconfirmed and the Microsoft white paper questioned. Then the good-page
fixture, on the same configuration, to test discrimination.

---

## Testing whether Google Search actually fires

The toggle being on means the tool is available, not that the model called it. Three checks, in
increasing cost.

**0 — Grounding metadata.** The platform attaches `grounding_metadata` / `groundingChunks` /
`webSearchQueries` to a response that really searched. This is the only hard evidence, it costs
nothing, and it was absent from run 3. Look for it before doing anything else.

**1 — A throwaway probe agent.** Same two tools, instructions that do nothing but search, and three
questions: does the *Journal of European Industrial Policy* exist; find the 2025 Van der Meer &
Kowalski paper; what is the top story on nos.nl right now. The third cannot be answered from
parameters and is checkable in seconds, so it cannot be bluffed. The first two probe the exact
capability the gate needs, and both should come back not found, because the journal and the paper
were invented for the fixture. This isolates the platform from the Socratic prompt: a failure here
is not a prompt problem.

**2 — The source ledger, added to the configuration.** Part 2 now opens with a line per source
marked CONFIRMED, MISMATCHED, NOT-FOUND or UNCHECKED, with an explicit instruction never to write
CONFIRMED for a source it did not look up. UNCHECKED is offered as a truthful answer precisely so
the model has somewhere honest to go instead of confabulating a check.

The ledger is worth keeping beyond this test: it turns the owners' half into something auditable,
and four UNCHECKED lines tell an instructor to distrust everything under them. It is not proof,
though — a model can claim a check it did not run. Test 0 is the proof; the ledger is the daily
signal.

### If search turns out never to fire

Then the fabricated-citation defect cannot be caught by this agent at all, and the honest options
are to accept that the gate does not verify sources — questioning them is still useful — or to move
source-checking into the workflow, where a step resolves each citation before the model sees the
page. That is an architecture change and would need its own record.

---

## Probe result — question 1 only

Asked directly whether a *Journal of European Industrial Policy* exists, the model said correctly
that it does not, and named real alternatives (the Oxford Handbook of Industrial Policy, the Oxford
Review of Economic Policy, an Edward Elgar volume).

**Inconclusive on search.** Every work it named is something a model knows without searching, and a
negative can be produced from absence of knowledge. Against search: the probe asked for the URL used
and it returned none, and it ignored the `NOT FOUND` format it was given. Question 3 — the top story
on nos.nl — is the one that cannot be answered from parameters, and it has not been run yet.

**Conclusive on something better.** The model can reject a fabricated journal name. In run 3, under
the full prompt, it never questioned Van der Meer & Kowalski at all. So the capability is present and
the prompt is not calling on it: the source check is one bullet among many, and the model spends its
attention producing five good questions instead.

That is the strongest argument yet for the source ledger. A step you must report on line by line is
a step you cannot quietly skip, so the next run of the fixture — with the ledger in place — is the
one that matters most so far.

### A hazard this exposed, now covered

A model willing to say "does not exist" will say it about sources that do. Obscure Dutch-language,
industry and unpublished work is real and hard to find, and telling a team they invented a source
they honestly used is a worse failure than missing one they did invent — worse for the student, and
worse for the gate's standing the first time it happens in front of a cohort. Added to the
configuration: a source you cannot find is not a fabricated source, never say or imply to a team
that a source is fake, ask them where they found it and what it says.

---

## Run 4 — 6 September 2026 — the agent never saw the page

**Fixture:** the raw GitHub URL · **Model:** `gemini-2.5-flash`, `thinking_budget: 0` ·
**Tools declared:** `UrlContextAgent`, `GoogleSearchAgent` · **Prompt tokens:** 2966 ·
**Output:** 576

The full trace, rather than the reply alone, is what made this run worth more than the three
before it.

### URL Context is a summariser, not a fetch

`UrlContextAgent` is a sub-agent, and what it returned is a prose summary of the page. **The
summary contains no source list at all** — Van der Meer, Stanford HAI, the Microsoft link, Draghi
and TechRadar are all absent, because the summariser dropped the section. The agent then scored a
page it had never read.

Everything wrong with the report follows from that one fact:

- **The ledger is confabulated.** Its three entries are claims from the body, not sources, all
  marked NOT-FOUND. The page's four actual sources appear nowhere, because the agent never saw
  them. NOT-FOUND asserts a search that did not happen.
- **The quotations are not the team's words.** The report quotes "This is increasingly relevant in
  2026, as approximately 70%…", which appears nowhere on the page; the team wrote "Research shows
  that around 70% of Dutch SMEs will be using AI tools in their primary process by 2027". Run 2's
  attribution failure is back, caused this time by the architecture rather than the model, and no
  prompt rule can catch it — the agent is quoting faithfully from what it was given.
- **A question about a choice the team did not make.** It asks why CRISP-DM rather than another
  project-management approach. CRISP-DM is prescribed by the handbook template.

### Google Search has never fired

`GoogleSearchAgent` is declared and was not called, in this run or any earlier one. That closes the
question left open after run 3: the tool is available and the model does not reach for it. With
`thinking_budget: 0` there is no planning step in which it would decide to.

### Also learned from the trace

The platform appends the Description field to the system instruction — "You are an agent. Your
internal name is… The description about you is…". The description is therefore live context, not
routing metadata, which is a reason to keep it short and accurate rather than promotional.

### Changes made

9. **The page must arrive as full text.** If the agent has only a URL or only a summary it replies
   with the single line CANNOT READ THE PAGE. Failing loudly is worth more than a plausible report
   built on a summary, which is what this run produced and what nobody would have caught without
   the trace.
10. **The ledger lists sources, never claims** — one line per entry in the page's own source list,
    named as the page names it, or "no source list on the page". CONFIRMED and NOT-FOUND now
    explicitly require that a search was run; UNCHECKED is the honest word otherwise.

### What this changes about the design

ADR-0014 has the agent read the published page. On this platform the fetch has to sit in the
workflow instead: it retrieves the page and passes the text, and the agent never holds a URL. The
architecture is unaffected — the input is still a page that is already public, so NFR-11 holds
exactly as before — but the layer that fetches is now decided, and decided against the tool that
looked purpose-built for it.

### Next run

Workflow fetches, agent gets full text, URL Context off. Then look at the ledger first: it should
carry five lines naming the page's own sources, and if they are all UNCHECKED the search problem is
confirmed as the remaining one. Raise `thinking_budget` above 0 before concluding anything about
Google Search — a model with no planning budget was never going to call a tool it was not forced to.

---

## Platform answers — 6 September 2026

Five configuration questions put to the console's own assistant. Four of the answers change
something, and two of them change the design rather than the settings.

**Thinking budget is not exposed in Agent Designer.** Low-level generation parameters are managed
by the runtime. So `thinking_budget: 0` stands unless the agent moves off the low-code canvas to
the SDK. Accept it for the pilot.

**URL Context always summarises**, with no toggle for raw retrieval. Run 4's diagnosis is now a
vendor-confirmed property rather than an inference, and the workflow-fetches constraint is settled.

**Tool invocation is a model heuristic.** Whether Google Search fires is the model's decision every
run; instructions improve the odds and guarantee nothing, and the one setting that would give it
room to plan is the one Agent Designer does not expose. **Source verification cannot be made
reliable at the agent level.** It moves to the workflow — a step that resolves each citation before
the model sees the page — or it leaves the design. What the agent can still do, and should, is ask
where a claim came from.

**The runtime returns one response and routes nothing.** Two supported ways to reach two audiences:
parse the headings in the caller, or split into two agents.

**There is no per-agent spend cap.** Cloud Billing budgets alert; they do not stop. Hard-stopping
needs budget alerts wired through Pub/Sub to a function that disables billing. ADR-0009 promises "a
hard spend cap with a course-owned key", and today that promise is an alert. Either the record
softens to a monitored cap, or someone builds the shut-off — and it is worth deciding which before
a runaway loop rather than after one.

### The recommendation this produces: two agents, not one

The parsing route keeps the rubric inside a payload that must never be forwarded whole. One
misconfigured step and a team reads its own scores, and that leak cannot be taken back.

Splitting the work removes the possibility instead of guarding against it. A questioner agent whose
instructions contain no rubric, no thresholds and no scoring language **cannot** emit a score, and
nothing in its context could leak because the confidential material was never there. A separate
rubric agent, called with the same page, writes only for the owners and is never addressed to a
student.

The second gain is the one run 3 diagnosed. The source check has been failing partly because it is
one bullet competing with everything else in a 2,000-word instruction; each half of a split agent
carries roughly half the load, and the checking has somewhere to be the main task rather than a
preliminary.

The costs are real and worth stating: two calls instead of one, two configurations to keep in step,
the rubric agent reading the page a second time, and the possibility that the questions and the
score drift apart because nothing guarantees they were formed from the same reading.

This is a design decision rather than a setting, so it belongs in a record before it belongs in the
console.

---

## Run 5 — 6 September 2026 — verification finally happens

**Model:** `gemini-2.5-flash` on Vertex, `thinking_budget: -1` · **Fetch:** `fetch_page`, a plain
function · **Input:** the fixture's live raw URL

### What the real fetch bought

The ledger came back with five lines carrying the page's own source names, which is the first time
the agent has demonstrably read what the team wrote. And the words are real verdicts rather than a
formality: Microsoft CONFIRMED (it opened the link), **Van der Meer NOT-FOUND**. Google Search
fired. Four runs of asking whether it would, answered by moving the fetch out of an LlmAgent.

**Both long-standing misses fell in the same run.** The vendor-source rule, missed three times,
produced question 3 — the team cites Microsoft's own documentation for a claim about Microsoft's
guarantees, and the question asks what independent source they consulted. The fabricated citation,
missed three times, is NOT-FOUND in the ledger and is the evidence behind Vetting: 0. Question 4
also caught the persona mismatch: one office manager who handles all IT, against a recommendation
needing "someone technical for a weekend".

Three of five tier-1 defects, and a different three than before — the 70% claim and Draghi both
dropped out this run. With three to five questions and eight defects, coverage varies run to run.
That is the design working as specified rather than a fault, but it means no single report should be
read as a complete account of a page.

### The defect this run introduced is worse than the two it fixed

The agent told the team their sources "appear to be dated in the future", marked Stanford HAI
MISMATCHED and TechRadar NOT-FOUND on that basis, and told the owners that neither "exists at the
current date". The Stanford HAI AI Index is real; its URL was verified by hand before it went into
the fixture. It is the control source — the one that proves the agent reads rather than
carpet-bombs — and the agent shot at it.

The cause is that the model's knowledge ends well before the course runs, so it reads 2026 as the
future. On real student pages, which will cite current material constantly, this would fire almost
every week, and a gate that routinely implies teams invented their sources loses the cohort the
first time it is wrong. The never-accuse guard held in the wording of the question and not in the
reasoning underneath it.

### Changes made

11. **The agent is told the date.** `agent.py` substitutes `{{TODAY}}` at import, so the
    instruction now opens by saying what day it is, that the model's knowledge ends before it, and
    that on what exists the search result decides and memory does not. Being in code rather than in
    a console field is what makes this possible at all.
12. **Recency is never grounds for doubt.** A work dated after the model's knowledge ends is a fact
    about the model. Never tell a team a source is dated in the future; never mark one down for
    being unfamiliar.
13. **NOT-FOUND and MISMATCHED are claims about a search that was run**, never about what the model
    recognises. Not knowing a work is not finding it absent.

### Next run

Same fixture. The ledger should now read Stanford HAI CONFIRMED and TechRadar CONFIRMED or
UNCHECKED, with Van der Meer still NOT-FOUND — that combination is the one that shows it can tell a
real recent source from an invented one, which is the discrimination the whole ledger exists for.
Then, at last, the good-page fixture: every score so far has been 0 or 1, and the rubric has still
never seen competent work.
