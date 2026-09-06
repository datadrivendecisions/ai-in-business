# Test fixtures for the Socratic gate

Fake student work, written to be fed to the agent before a real cohort meets it. Each fixture is a
handbook page as a team might actually publish it, with **known defects planted in it**, plus an
answer key saying what a competent report should catch.

**Answer keys are tier-1 instructor material.** They may not enter `site/`, and a fixture must never
be shown to students — a cohort that has read the key knows what the gate looks for, which is the one
failure the gate has no defence against. Configuration is in
[`../socratic-agent-config.md`](../socratic-agent-config.md); requirements in
[`../prd-socratic-gate.md`](../prd-socratic-gate.md).

## How to run the test

1. Give the agent [`week-02-team-03.html`](week-02-team-03.html). **Prefer a URL**; if you paste,
   paste the HTML source and not the rendered text. Rendered text loses every `<a href>`, which
   silently removes the vendor-source defect and leaves the link-checking instruction with nothing
   to act on. A URL also exercises the fetch, which is where a real run breaks.
2. Give it **no prior reports**. This is week 2 of the course, which is the first report for this
   team, so it exercises the cold-start branch: Movement cannot be scored, and the agent should say
   so and open gate A rather than penalise a history that does not exist.
3. Score the output against the key below, then against the twelve qualities in the PRD §3b.

**Check the split before anything else.** Confirm that the reply carries both `## FOR THE TEAM` and
`## FOR THE OWNERS`, in that order, and that nothing above the second heading contains a score, a
grade, or a judgement. A leak here is unrecoverable in a real run.

## Why this page reads a little like a machine wrote it

That is deliberate, and it is the point of the exercise. Under LRD §6.1 the page *is* produced by
the team's own agentic platform, and §6.4 has the gate probe whether the team vetted what it
generated or waved it through. A fixture polished into good human prose would test the wrong thing.
Do not run the `strip-ai-language` skill over it.

---

# Answer key — `week-02-team-03.html`

Eight defects are planted. A report that catches three or four of the first five is working; one
that catches none of them is asking generic questions and fails quality A1.

### Tier 1 — should be caught

1. **The 70% figure is unsourced and unverifiable.** "Research shows that around 70% of Dutch SMEs
   will be using AI tools in their primary process by 2027" cites nothing in the text. The nearest
   source in the list is fabricated (see 4). A good question asks which number on this page they
   could verify right now.
2. **A factual error carried straight through from the model.** "The EU AI Act came into force in
   2024 and requires all SMEs deploying AI systems to complete a conformity assessment before
   deployment" is wrong on the date, wrong on the scope, and wrong on who must do what. It is stated
   with more confidence than anything else on the page. This is the vetting failure the gate exists
   to find.
3. **A vendor's marketing document used as neutral evidence.** The Microsoft EU Data Boundary white
   paper is linked without appraisal, and the tooling section repeats its framing. The team's own
   source list shows they know how to appraise (see the Stanford entry), so the question is why this
   one was not.
4. **A source that does not exist.** "Van der Meer, J. & Kowalski, T. (2025), *Journal of European
   Industrial Policy*" is invented — a plausible-looking citation with authors, volume and page
   range, which is the classic shape of a fabricated reference. Nothing in the body cites it.
5. **Draghi is cited through a news summary, not read.** The source line says "Summarised in NOS
   coverage". The whole geopolitical argument of the chapter rests on it.

### Tier 2 — a strong report reaches these

6. **No alternative was considered.** The chapter picks the open-versus-closed-weights framing and
   never says what else it could have asked about this theme, or why this angle serves this persona.
   Quality A2 and the Reasoning dimension.
7. **The five steps are generic.** Nothing in them is specific to a 30-person metalworking shop with
   one office manager; they would fit any firm of any size in any sector. The chapter's own persona
   makes the gap visible.
8. **The metadata is incomplete and internally inconsistent.** "Sources last appraised:" is empty.
   The tooling section recommends Azure OpenAI enterprise contracting to a firm the same page
   describes as having one office manager who handles all IT.

### The control — the agent should not flag this

The **Stanford HAI entry is properly appraised**: it says who they are and why they are worth
believing, and gives a reason for preferring them over a vendor benchmark. An agent that criticises
this source too is carpet-bombing rather than reading, and that is a defect worth catching early.

### What a good report looks like on this page

Three to five questions, at least one quoting a specific sentence, at least one about a source and
at least one about what the team checked versus what their system produced. No praise, no advice, no
score, no mention of another team. If the agent tells them the AI Act sentence is wrong, it has
failed — the question is what they did to check it, not the correction.

### Scoring, for calibration

Provisionally this page should land around Sourcing 1, Vetting 0–1, Reasoning 1, Movement n/a. Under
the thresholds in the config that is a total of 2–3 out of 9 available, which would close gate A —
except that Movement is unscorable in a team's first week, so gate A opens regardless. Whether that
is the right behaviour for a page this weak is exactly the calibration question the pilot exists to
answer, and it is the first thing to reconsider after week 2.

---

# Answer key — `week-02-team-07.html`

**The discrimination test.** Same week, same theme, same persona as `week-02-team-03.html`, so the
only variable is the quality of the work. Team 03 was built to fail; team 07 is built to pass, and
until both have been run the rubric has no scale — every score so far has been 0 or 1 on a page
designed to earn it.

## How to run it

Exactly as team 03: full text, cold start, no prior reports. **Start a new session first.** Run 7
was given this page and reported on team 03, because the earlier page was still in the conversation
history and the model answered from it rather than fetching. Then compare the two reports side by
side. The single question this fixture answers is whether the gate can tell competent work from
weak work, and that is visible in the scores rather than in the questions.

## Expected scores

**Sourcing 3, Vetting 3, Reasoning 3.** If any of these lands at 0 or 1, the rubric is not reading
the page — it is producing a number. The ledger should read CONFIRMED on all four sources, which are
real and were verified by hand before the page was written.

If team 07 scores the same as team 03, nothing learned in six runs of tuning is worth keeping, and
the rubric needs rebuilding rather than adjusting.

## What earns each score

**Sourcing.** Four sources, each appraised in the team's own words with a reason for trusting it
*and* a stated limit: Draghi is authoritative on the EU economy and openly political, so it is used
for the diffusion argument and not for prescriptions; the AI Act article is used instead of a
summary because the summaries disagreed; Microsoft is the vendor and is used only for where its own
servers are; Stanford HAI is preferred to a vendor benchmark for a stated reason, with its data
described as directional rather than about Dutch SMEs. The Draghi entry says explicitly that the
report was read rather than the coverage of it.

**Vetting.** The *What we checked, and what changed* block is the evidence, and it mirrors team 03's
planted defects one by one: the AI Act claim was wrong and was corrected against Article 6, the
unsourced 70% figure was cut because it could not be traced, and a source was dropped because the
journal could not be found. Three hedges elsewhere do the same work — the Draghi link is named as
the team's inference rather than Draghi's, the legal reading is flagged as not a lawyer's, and the
number of scanned quotations is admitted as unknown.

**Reasoning.** *Why we chose this question* names two angles considered and rejected with reasons
that turn on this persona: sovereignty-as-principle is not decidable for an owner, and the
open-versus-closed comparison is not live for a firm where nobody will run a model. The tooling
section justifies its three entries against one office manager with no technical support, and
includes the local model explicitly to say why it is not recommended.

## The honest gaps — legitimate targets

A flawless page would be a bad test, because the agent must produce three to five questions whatever
it reads. Three real weaknesses are left in, and a good report asks about these rather than
manufacturing something:

1. **No field research yet.** The page says so: the visit is in week 3, and the renewal-date argument
   has never been put to an owner who has made that decision.
2. **One claim rests on reasoning, not evidence.** That switching cost matters more than vendor
   nationality is the team's reading of Draghi plus inference, and the page admits nobody has
   measured it for firms this size.
3. **A whole category is named without appraisal.** Sector-specific quotation tools are recommended
   as a category because the team found only vendor pages; naming a category you cannot appraise is
   defensible, and worth being asked about.
4. **A legal obligation described as a house rule.** The transparency obligation is called "a house
   rule, not a compliance project". Found by the agent in run 8, not planted: it is a real weakness,
   and softening an obligation into an internal practice is exactly the move a chapter for owners
   should not make. Recorded here because a key that only lists what its author intended stops being
   a check on the author.

## What would show the gate is failing

- Any score of 0 or 1 on Sourcing, Vetting or Reasoning.
- A ledger entry other than CONFIRMED on the four sources, all of which resolve.
- Questions that manufacture faults — treating the admitted gaps as concealment, or asking for
  sources the page already appraises.
- Praise. A page this much better than team 03 is where the no-verdict rule is under the most
  pressure, and "this is well sourced" is a verdict however kindly meant.

---

# Answer key — `week-03-team-07.html` (the growth test)

**What this pair tests.** Movement, and the growth requirement at the centre of LRD §6.4 — that a
report is generated against the team's full prior history, never repeats a question already
answered, and never lets a team coast on one that has not been. Eight runs have all been cold
starts, so this dimension has never once been exercised.

## How to run it

**Fresh session.** Supply two things and nothing else:

1. The week 3 page: `week-03-team-07.html`.
2. The team's prior history: [`week-02-team-07-report.txt`](week-02-team-07-report.txt) — the
   questions the team received in week 2.

Give only the team-facing half as history. The owners' half, with its scores, is never part of a
team's record: a report that carries last week's score into this week's questions has smuggled the
rubric into the student-facing channel by another route.

Note that week 3 is a **new page on a new theme**, not a revision of week 2 — the course publishes
one page per team per week and never edits an earlier one. So movement has to be visible in how the
team works, not in a rewritten page, which is exactly what the gate must be able to see.

## What the page does with each of last week's three questions

| Week 2 question | What the page does | What the report must do |
|---|---|---|
| The transparency obligation called "a house rule" | **Answered, and then some.** They looked up Article 50, found it is law and in force since 2 August 2026, separated the provider's obligation from the shop's own staff rule, and rebuilt a section around the correction. | Must not ask it again. Movement evidence. |
| Specialist tools they could not appraise | **Answered.** They went back, established that no independent evaluation exists, and turned that into buying advice an owner can use without one. | Must not ask it again. Movement evidence. |
| The single-source claim about switching cost | **Ducked, and dressed as an answer:** "We still think this is right and it holds up in the reading we have done since." No source, no evidence, no reading named. | **Must return to it, harder, and say that it is a return.** |

The third row is the test. Ducking that looks like ducking is easy to catch; this is the form a
capable team actually uses, and a gate that accepts it will be gamed by exactly the teams the
mechanism exists for.

## Expected

**Movement 3.** Two questions genuinely answered, one of them by correcting a substantive error
against the legislative text. **Sourcing 3, Vetting 3, Reasoning 2–3** — the page carries the same
appraisal discipline, hedges its legal reading, and admits what it has not tested. **Gate A opens**
on the score this time rather than on the first-report rule, which is itself worth checking: the
threshold is Movement ≥ 2 and total ≥ 6, and this is the first run where those numbers do any work.

**The ledger:** four entries, all CONFIRMED, all four cited in the body.

## What would show the growth requirement is not working

- **Any question that repeats one of last week's three**, particularly the transparency obligation,
  which the page addresses at length.
- **Silence on the ducked claim.** If the switching-cost question is not returned to, the gate
  rewards the sentence "we still think this is right", and AC-05's 90% bar is unreachable.
- **A return that is not named as one.** §6.4 requires the team to see that it is being asked again;
  an unmarked repeat reads as the agent having forgotten.
- **Movement scored from the page's tone** rather than from what changed — a report that praises the
  block for existing without checking whether the three questions were actually addressed.
- **Movement n/a**, which would mean the history was not read at all.

## Fresh material, so the report is not only about last week

Two genuine gaps are new this week, and a good report has room for one of them: the people question
is deferred to week 5 by choice, and the buying advice is reasoning from an absence of evidence
rather than from evidence — the page says so, and says it is weaker for it.
