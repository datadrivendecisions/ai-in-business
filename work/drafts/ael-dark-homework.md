# Dark research — three homework tasks for AEL, week 1

*Draft for the module owners. Three options, each scored above 90 % on the homework variant of
[kickoff-scorecard.md](kickoff-scorecard.md). Choose one, or combine as noted at the end.
"The intern" is the agentic CLI of [ADR-0009](../decisions/0009-build-environment.md); the
process artefacts are those of [ADR-0010](../decisions/0010-ael-arc.md).*

## The source

A news report on China's dark factories, built around **ZEEKR**, a luxury EV maker founded in
2021 whose flagship plant in north-eastern China makes up to 300,000 cars a year, over 800 a
day — a volume Tesla took more than a decade to reach. Its definition of the term is the one to
give students: *a part of the plant so automated, and with so little human presence, that in
theory the lights could be shut off.*

Four things in it are worth more than the robots:

1. **The two jobs that stayed human.** Cable assembly, because it needs a human touch, and going
   into the plant to maintain the robots. Nothing else is named. Those two exceptions are the
   whole design question.
2. **Automation was a response to rising wages**, not to cheap labour. China's costs rose faster
   than the West expected, and automation was the obvious way to blunt it.
3. **Regulation is described as a brake.** Fewer labour rules and no unions in the same form mean
   "fewer impediments to automating". A brake is a choice somebody made.
4. **The sting in the tail: who buys all these cars?** Chinese firms already build more EVs than
   every other maker combined, Western markets are largely closed to them, and even friendly
   markets in Brazil, the Middle East, Africa and South-East Asia fear the flood. Most of the
   cars are sold at home, and overcapacity is the industry's real problem.

Context worth having in the room: the International Federation of Robotics found that in 2023,
every second industrial robot installed anywhere in the world went to China, and Chinese
robotisation has grown sevenfold since Made in China 2025 launched in 2015. Elsewhere, Xiaomi's
Changping plant claims 81 % automation and markets itself as "a phone every second", though ten
million phones a year is one every 3.15 seconds. FANUC has run lights-out since 2001, up to
thirty days unsupervised. Against them, Tesla's 2018 reversal, when Musk called excessive
automation a mistake and said humans are underrated.

## Why this lands on AEL

AEL's platform is a publishing pipeline: question → sources → draft → review → published
chapter. "Dark" is a real target for parts of it, and an impossible target for others, because
this module has already written its own brakes:

- **Nothing reaches an SME unreviewed.** The handbook is public and published under the
  programme's name, so there is an editorial gate before anything ships (ADR-0001).
- **The gate is the point.** A team advances only when a Socratic tutor and a partner team can
  see the thinking moved. A dark pipeline that clears its own gate has removed the assessment.
- **Interview material never runs through a free tier**, and nobody is approached before the
  consent text is signed (NFR-09, ADR-0009). The most valuable input to the pipeline is the one
  input that may not be automated.
- **A manual route is kept at every step** (FR-12).

So the question a team answers is not *can we go dark* but *which lights do we switch off, which
do we leave on, and who decided*. That is scope and non-goals — the product manager's half of
week 1, and exactly what PRD v0 is for.

## Scoring note

The session scorecard has eighteen items. Fifteen transfer to homework unchanged. Four items
are read differently, since there is no room to pace and no lecturer present:

| Item | In the session | For homework |
|---|---|---|
| B5 | No lecture over ten minutes; movement; a break | Fits the stated time budget; alternates reading with producing; is not a reading marathon |
| E1 | Administrative talk under five minutes | The brief fits on one card; the work is thinking, not admin |
| E2 | Students are inside a question within three minutes | The first line is a question a student wants the answer to |
| E3 | Two lecturers can run it, under a minute per team | Doable with the tools students have, feeds a gate, readable in under a minute per team |

Target is 49 of 54. Scores below are self-assessed by the same author who designed the tasks, so
they are a design check and not evidence; the other module owner should score independently.

---

## Option A — The automation ledger

**What it teaches.** Systems mapping and verification. Where the lights can go off, and what
would go unnoticed when they do.

**The brief, as students receive it.**

> ZEEKR's plant runs in the dark except for two jobs: assembling the cables, because they need a
> human touch, and going in to maintain the robots. Everything else is off.
>
> **Alone, 45 minutes.** Take one claim about a dark factory — Xiaomi's 81 %, "a phone every
> second", FANUC's thirty unsupervised days, ZEEKR's 800 cars a day, or one you find — and
> verify it. Write four lines: the claim, who made it, what you found, and whether it is true,
> false, or unverifiable. A source that does not resolve does not count. Then write one line on
> what you had assumed before you checked.
>
> **As a team, 45 minutes.** List every step your publishing pipeline will take, from a question
> to a published chapter. Against each step mark **dark** (no human, ever), **dim** (a human
> looks only when something trips), or **lit** (a human every time). For each dark and dim step,
> name in one line the failure that would go unnoticed and who would eventually notice it.
> Finish with two lines: the one step you would make dark that nobody else in the cohort would,
> and what you accept losing when you do; and the step you first marked dark because it sounded
> modern, and what changed your mind.

**Produces.** The scope and non-goals section of PRD v0, and four individually authored
verification notes.

**Read in.** One page, one table. The lecturer reads the dark rows only.

**Costs.** 90 minutes per student. PRD v0 shrinks to half a page because this is its content.

| Weak item | Why |
|---|---|
| D2 creativity — 2 | An audit converges by nature; the "nobody else would" line lifts it but does not make it open-ended |
| E3 feasible — 2 | Every student must find a source that resolves in 45 minutes; some will arrive with a fabricated citation, which is useful but costs reading time |

**Score 52 / 54 = 96 %.** Strengthened during scoring: the "what changed my mind" line was added
to reach A3, which was otherwise a system audit with no reflection on the student's own thinking.

---

## Option B — Who reads chapter 300?

**What it teaches.** Demand before throughput. The trap the video ends on, transplanted.

**The brief, as students receive it.**

> The report ends on a question the robots cannot answer. China builds more electric cars than
> every other maker in the world combined, Western markets are largely shut to them, and even
> friendly markets fear the flood. Most of the cars are sold at home. So: who buys them?
>
> **Alone, 45 minutes.** Find out what happens to output nobody wants. One documented case of
> overcapacity — in Chinese EVs, or in any industry, or in your own country, where the numbers
> are ones you can actually check. Four lines: what was built, how much of it was absorbed, what
> it cost when it was not, and your source.
>
> **As a team, 45 minutes.** Your platform will be able to produce a chapter in fifteen minutes.
> That is roughly 300 chapters in the term if you let it run. Answer three questions in one page.
> How many people are actually going to read your team's contribution this year — a number, and
> how you got to it. What does a chapter cost the reader when it is wrong, and who pays.
> And what throughput are you deliberately not building, and why. End with the sentence you
> would say to the owner if she asked why you are not simply giving her fifty chapters.

**Produces.** The non-goals of PRD v0 and its "who is this for" section, plus a demand figure the
AIBS problem analysis can also use for "why it matters".

**Read in.** One page. The lecturer reads the number and the last sentence.

**Costs.** 90 minutes per student. Overlaps the AIBS "why it matters" evidence, so it partly pays
for itself.

| Weak item | Why |
|---|---|
| D1 collaboration — 2 | The research half is individual and the synthesis is short; the partner team has no role unless one is added |
| E3 feasible — 2 | A readership number is contestable and slow to defend; expect some teams to guess and call it research |

**Score 51 / 54 = 94 %.** Strengthened during scoring: "how you got to it" was added to the
readership number, otherwise the task rewarded a confident guess — the exact failure the trust
exercise teaches students to catch.

---

## Option C — Three positions on a dark publishing company

**What it teaches.** That a position is cheap and a prediction is not. Every viewpoint on
automated publishing implies something testable about the team's own pipeline.

**The three positions.** One student takes each; the fourth is the editor. In a team of five,
double position 3, which is the hardest.

| | Position | It rests on |
|---|---|---|
| 1 | **Not feasible, and not desirable.** People only want to read what a person wrote. | Readers can tell, and care that they can |
| 2 | **Not fully dark.** Machines may write, but a human reviews before anything is published. | Review catches what nothing else catches |
| 3 | **Fully dark is feasible.** Readers need only say whether they liked it; the agents learn and optimise towards that. | A like or dislike is a good enough signal to improve on |

**The brief, as students receive it.**

> A car plant can run with the lights off because a finished car either fits the tolerance or it
> does not. A chapter is not like that. Three people can look at the same page and disagree about
> whether it is any good. So can a dark publishing company exist at all?
>
> **Alone, 45 minutes.** You have been given one of the three positions. You do not have to
> believe it. Have the intern write the strongest one-page case for it. Then do two things it
> cannot: find the one claim in its case that does not survive checking, and strike it with a
> line saying why. Then write the sentence that starts *"This is true only if …"* — the single
> condition your whole position rests on.
>
> **Bring to the team.** One paragraph on her quoting problem that you wrote yourself, and one
> the intern wrote on the same thing. Do not mark which is which.
>
> **As a team, 45 minutes.**
>
> *The blind test.* Send your eight paragraphs to your partner team, shuffled. They guess which
> four are human. You do the same for theirs. Write the score down. Then write one line on what
> a score out of eight can and cannot tell you — you are researchers, and eight is a very small
> number.
>
> *The prediction.* Each position turns its condition into something your own platform could
> prove or disprove before week 6. Position 1 predicts something about readers. Position 2
> predicts that review catches a class of error nothing else catches. Position 3 predicts that a
> like-or-dislike signal is enough to make the next chapter better. Write all three as
> predictions with a date.
>
> *The editor decides.* One paragraph, signed by the whole team: which position your platform is
> built on, which lights that switches off, and what you will do when the prediction fails.
>
> *The signal.* Position 3 is the interesting one, so answer its question whoever wins. If your
> pipeline optimises for what readers say they like, what exactly is it optimising for — and is
> that the same thing as being useful to a 30-person machining shop? She can tell you in five
> seconds whether she liked a chapter. She cannot tell you whether it was true until she has
> acted on it, months later, if ever. Name the signal you will actually measure, and why it is
> not "did they like it".

**Produces.** Three dated predictions, a signed position, and the first specification of a reward
signal — which is what the evaluation configuration in week 4 has to encode. It also gives the
decision log its first real record.

**Read in.** One paragraph and three dated predictions. The blind-test score is a number.

**Costs.** 90 minutes per student, plus a five-minute exchange with the partner team.

| Weak item | Why |
|---|---|
| E1 brief on a card — 2 | Three positions, a blind test and a prediction is a lot of instruction for one card; it needs the card plus a worked example |
| E3 feasible — 2 | The blind test depends on the partner team turning up; a team left without a partner has to test on the lecturers |

**Score 52 / 54 = 96 %.** Strengthened during scoring: the first draft ended at the signed
paragraph, which is a debate. The dated predictions and the reward-signal question were added,
because a position that cannot fail teaches nothing and leaves week 4 with nothing to encode.

**Why position 3 is worth the room.** It is the one that sounds most modern and breaks in the
most instructive way. Optimising on what readers say they like optimises the proxy, not the goal:
a confident, flattering, tidy chapter is more likeable than an accurate one that says the tooling
will take three months and might not work. For a handbook that is explicitly educational and not
consultancy, a pipeline tuned to approval is a pipeline tuned away from the disclaimer. Students
reach that on their own if the reward-signal question is asked plainly.

---

## Option D — The brake list *(kept in reserve)*

**What it teaches.** That a brake is a decision, and someone benefits either way.

**The brief, as students receive it.**

> The report gives one reason Chinese plants automate faster: fewer labour rules, and no unions
> in the same form, so there are "fewer impediments to automating". An impediment is somebody's
> protection. Your platform has four of its own: nothing reaches an SME unreviewed; the gate you
> have to pass every week; interview material may not go through a free tier; and a manual route
> at every step.
>
> **Alone, 45 minutes.** Take one brake on automation that exists outside this course — a labour
> law, a safety certification, a liability rule, a data-protection rule, in your own country if
> you can. Four lines: what it stops, who it protects, what it costs, and who has argued for
> removing it. Sources that resolve.
>
> **As a team, 45 minutes.** Split two against two. One pair uses the intern to build the
> strongest case for removing one of your platform's four brakes; the other pair builds the case
> for keeping it. Then both pairs find one claim in the intern's own case that does not survive
> checking, and strike it. Come back together and write two things: the one sentence about that
> brake that all four of you will sign, and the one sentence you could not agree on, with both
> versions.

**Produces.** The first entry in the team's decision log, in the shape the log will keep all
term, and a position the joint interview can walk back through.

**Read in.** Two sentences. The disagreement is the interesting one.

**Costs.** 90 minutes per student. Adds the decision log two weeks earlier than ADR-0010 places
it, which is a change to that record's table, not a change to make quietly.

| Weak item | Why |
|---|---|
| E3 feasible — 2 | Needs all four students to do their half; one no-show leaves a pair arguing with itself |
| B2 flow — 2 | A student assigned the side they do not hold can stall; the brief must say they are not being asked to believe it |

**Score 50 / 54 = 93 %.** Option C now covers this ground with a sharper structure, so this is
kept for a later week — the brakes question suits week 3, where the theme is data, contracts and
dependency.

**Original scoring note.** Strengthened during scoring: "find one claim in the intern's own case
that does not survive checking" was added, without which the AI does the arguing and the
students only pick a side.

---

## Choosing, and combining

- **If you want the platform specified**, take **A**. Most directly useful to the requirements
  document, and the easiest to read.
- **If you want the term's best question in their heads**, take **B**. It is the one that stops a
  team building a chapter cannon, and it feeds the research track as well.
- **If you want the viewpoints argued out**, take **C**. It is the strongest on collaboration and
  creativity, it produces the first reward-signal specification, and its blind test gives the
  cohort a fact about itself in the first week.

**The pairing that costs least.** **A's individual half with C's team half**: every student
verifies one dark-factory claim, then the team runs the blind test, writes the three predictions
and names its signal. Ninety minutes, keeps the verification practice, ends on the question
week 4 has to answer. Scores 52.

**If you want one only, take C.** It contains a version of the other two: the predictions do A's
work of deciding which lights go off, and position 3 forces B's question about what the output is
for. B's overcapacity framing then becomes a five-minute plenary opener in week 2 rather than
homework.

**Do not run three.** Week 1 already carries the problem analysis, the interview design, the
partner exchange, the requirements document, the spike and the setup.

## Before it goes out

- Decide whether the video is watched in the session or before it. If in the session, it costs
  six minutes and block 3 has to give them up.
- Options C and D move the decision log from week 3 to week 1. That contradicts ADR-0010's table,
  so either amend the record or note the deviation in the logbook.
- Option C's blind test needs the partner pairing to hold over the weekend. Say in the room that
  the exchange is by Thursday, so a silent partner surfaces while there is time to reassign.
- Option C ends where the week-4 evaluation configuration begins. If you run it, keep the teams'
  signal paragraphs — they are the input to that week, and rewriting them from memory in week 4
  loses the point.
- All three ask for sources that resolve. Say once, in writing, that a citation the intern
  invented is a failure-log line and not a moral failing — otherwise the first instinct is to
  hide it.
- The cohort is international. Options B and C invite a student's own country deliberately; that
  is the same seam as the home-country trust card, and the two should be introduced as a pair.

## Sources

- [Lights out (manufacturing)](https://en.wikipedia.org/wiki/Lights_out_(manufacturing)) —
  definition, FANUC since 2001, Philips, Siemens Amberg
- [Xiaomi's dark factory](https://www.slashgear.com/2144548/xiaomi-smartphone-robot-dark-factory-how-works-makes-phones-fast/)
  and [BGR](https://www.bgr.com/2087200/xiaomi-dark-robot-smart-phone-factory/) — 81 %
  automation, ten million phones a year, the "one per second" claim
- [Tesla's problem: overestimating automation, underestimating humans](https://theconversation.com/teslas-problem-overestimating-automation-underestimating-humans-95388)
  and [Musk admits automation at Tesla was a bad idea](https://futurism.com/musk-automation-bad-idea)
- [Shining a light on the lack of fully automated dark factories](https://www.gray.com/insights/shining-a-light-on-the-lack-of-fully-automated-dark-factories/)
  — why hybrid is the norm
