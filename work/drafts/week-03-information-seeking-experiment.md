# Does an AI devil's advocate reduce biased information seeking?

*An in-class experiment for week 3. Draft for the module owners; not for students in this form —
it states the hypothesis direction and the manipulation, and students must not read either before
they run it. Belongs with [issue #13](https://github.com/datadrivendecisions/ai-in-business/issues/13),
whose counter-case protocol this puts to the test on the students' own behaviour.*

## Why this experiment and not a demonstration

Week 3 teaches teams to build a counter-case against their own conclusion. The obvious next
question is whether it works, and the honest answer is that we do not know for this population.
So the session does not demonstrate the method — it **tests** it, on the students' own information
seeking, with the students as both experimenters and participants.

That doubles the teaching: they learn a reliability method, and they learn what it takes to find
out whether a method works. The second is the thing week 2 gestured at when it asked them to write
a search strategy another team could repeat.

## What is being measured

**Biased information seeking** is the tendency to seek out material that agrees with a position you
already hold. It is well established: a meta-analysis of selective-exposure studies found a
moderate preference for congenial over uncongenial information, **d = 0.36**
([Hart et al. 2009](https://doi.org/10.1037/a0015701), *Psychological Bulletin* 135(4): 555–588).

Two findings shape the design:

- Presenting information **sequentially** rather than all at once produces a *stronger* preference
  for supporting material, because it focuses attention on the prior decision
  ([Jonas et al. 2001](https://pubmed.ncbi.nlm.nih.gov/11316221/), *JPSP* 80(4): 557). Real
  searching is sequential, so the realistic condition is also the high-bias one. Good for us: it is
  where an effect is most likely to be visible.
- **Structure matters more than source.** Across six studies, whether information came from an AI or
  a human made no reliable difference to confirmation bias, but the presence of a **conclusive
  recommendation consistently amplified it**, and its absence mitigated it
  ([*Computers in Human Behavior: Artificial Humans*, 2026](https://www.sciencedirect.com/science/article/pii/S2451958826001211)).

That second finding is why this experiment is worth running here rather than anywhere else. The
whole course rests on a rule — **the gates ask questions and never give a verdict** (ADR-0011, and
the Socratic agent's instructions). If conclusive recommendations amplify bias and questions do not,
that rule is not a pedagogical preference, it is a debiasing mechanism. This experiment tests our
own foundation.

## Design

**The cohort is eight teams of four, so the unit of analysis is the student, not the team.**

That decision does the most work in this document, so here is the reasoning. Chiang et al. and
Lee et al. measured *group* decision making, so their unit had to be the group. Biased information
seeking is not a group phenomenon — Hart et al. and Jonas et al. both measured it in individuals,
because selecting what to read next is something a person does. Matching the unit to the
phenomenon takes the sample from **8 to 32** at no cost in session time.

For that to be honest, the manipulation has to reach the individual: **each student works their own
source menu with their own agent**, before the team discusses anything. If the agent argued with
the team instead, the treatment would be applied at team level, observations inside a team would
not be independent, and the effective sample would be 8 again whatever the spreadsheet said.

**Within-person, counterbalanced, two rounds.**

| | Round A | Round B |
|---|---|---|
| Half the students (by team, 4 teams) | no agent, claim 1 | questioning agent, claim 2 |
| Other half (4 teams) | questioning agent, claim 1 | no agent, claim 2 |

Order and claim are counterbalanced. Carryover is real and not removable — someone who has met the
devil's advocate cannot unmeet it — so order enters the analysis as a factor and is reported rather
than assumed away. Students are still clustered in teams by shared context, so report team means as
a robustness check alongside the individual-level result.

### The verdict-giving agent: demoted, not dropped

The original design had a second arm — an agent that states a verdict rather than asking — to test
the course's own *questions, never a verdict* rule. With eight teams that comparison would be four
against four, which is not a test of anything.

So it stays in the session and leaves the analysis: run the verdict variant **in the debrief**, live,
on a position the room has just taken, and let them see what it produces beside what the questioning
agent produced. It is a demonstration, labelled as one, and it earns its place because the 2026
finding about conclusive recommendations is the most interesting thing in the reading. Claiming it
as a measured result on n = 4 would be the exact error the session is teaching against.

### The task

Each team gets a claim in their own domain — AI for regional manufacturing SMEs — stated so that a
reasonable team could land either side. For example: *"A manufacturing SME of 50 staff should put an
AI assistant in front of its customers before it puts one behind its own processes."*

They state an initial position in one sentence, then build the evidence for it from a source menu,
then state a final position.

### The source menu, and why it is closed

Sixteen prepared sources, revealed **one at a time**, of which a team may open eight. Title and two
lines of abstract are visible; opening costs one of the eight.

The menu is crossed **2 × 2**: stance (supports the claim / opposes it) × quality (strong source /
weak source), four in each cell. The crossing is the instrument. If a team selects on quality they
end up near balance; if they select on agreement they do not. Nobody is told the menu is balanced
until the debrief.

This is the one part of the session that is real work to build, and it cannot be improvised — it is
the analogue of the deliberately biased `RiskComp` model in Chiang et al., where the experimenters
knew which cases the model got wrong before anyone sat down.

### The agent

Introduced **after the position is locked and before the first source is seen**. That placement is
forced by what is being measured: the outcome is which sources a student chooses to open, so an
agent arriving after the menu could not move it at all. What it objects to is therefore the
student's own stated position, quoted back at them. Chiang et al. found the interactive devil's advocate
aimed at the AI's recommendation produced the highest group decision accuracy
(β = 0.135, SE = 0.068, 95% CI [0.002, 0.269], p = 0.047), and that aiming at the AI beat aiming at
the group's majority opinion (F(1,92) = 3.500, p = 0.064). Aim ours at the position, not at the
people.

Two styles, and the contrast is the course's own rule:

- **Questioning** — asks about the position and the sources; states no view. This is the
  Socratic agent's register, and `project-documentation/socratic_agent/instructions.txt` already
  contains the prompt discipline to copy.
- **Verdict-giving** — states that the position is wrong and says why.

Prediction from the 2026 result: the questioning agent reduces bias more. Prediction from the
course's own assumption: the same. If the verdict agent wins, the course has something to revise.

Set the intervention frequency and record it. Lee et al. interjected after roughly every eight
messages and their participants reported diminishing utility over a session — *"the further it went
on, the more I felt like I kind of tended to ignore it"*. Too often is a failure mode, not a dose.

## Outcome measures

**Primary**

1. **Congeniality index** — (congenial opened − uncongenial opened) ÷ opened. Comparable in
   direction to Hart et al.'s d = 0.36.
2. **The crossed cell** — did the team open the *strong source that opposes them*? One binary per
   team per round, and the most legible number in the room.

**Secondary**

3. **Over-collection** — how many sources opened before committing. Schwenk & Thomas (1982), reported
   in [Schwenk 1984](https://www.jstor.org/stable/10.1111/j.1467-6486.1984.tb00230.x)
   (*Journal of Management Studies* 21(2): 153–168), found devil's advocacy **reduced the tendency
   to collect too much information**. A rare directional prediction from 1982 that we can test.
4. **Position movement** — did the final sentence differ from the first?

**Subjective, and do not skip these**

5. Perceived decision quality, perceived teamwork quality, and a short NASA-TLX.

Measure 5 exists because of the most useful result in the whole reading pile. In Chiang et al., the
groups with the interactive devil's advocate had the **highest actual decision accuracy and the
lowest self-perceived performance and perceived teamwork quality**. Lee et al. found satisfaction
rose but that the agent's effect was *indirect* — presence changed the climate more than content
changed minds. And Schweiger, Sandberg & Ragan found the same trade-off in 1986 with human devil's
advocates: better decisions, less satisfaction, less acceptance.

Forty years, three methods, one result: **structured dissent feels worse than it works.** If the
room reproduces that on its own data, no one will forget it.

## Rigour the students run themselves

- **Pre-registration.** Before the session, each team writes its hypothesis, its analysis plan and
  what result would falsify it. This is step 4 of the counter-case protocol applied to their own
  experiment, and it is what stops the analysis becoming a search for a pleasing number.
- **Two people code the sources, and then we check whether they agreed.** The central number in
  this experiment — did a student open sources that agree with them? — rests on somebody deciding,
  source by source, whether it agrees or disagrees with that student's stated position. That is a
  judgement, and judgements differ. So two people code independently, and we measure how well they
  matched.

  **There are two of these, and they do different jobs. Do not merge them.**

  **The instrument kappa — the owners, before the session.** Two of the teaching team code the whole
  16-card deck against the codebook rules, independently, and compute a kappa. This is the one the
  data rests on: if the two of them cannot agree what each card says, no student's score means
  anything. It is done in advance for a reason. If confirmation bias is strong — the thing we are
  looking for — then most *opened* sources are "agrees", the categories go lopsided, and kappa
  collapses precisely when the effect is largest. The deck is balanced eight against eight by
  construction, so coding the deck instead of the selections keeps the categories even and the
  number meaningful.

  **The teaching kappa — the students, in the debrief.** Hand each pair the same eight cards the
  owners coded, balanced four supporting and four opposing. They code independently, build the 2×2,
  and compute it. Then put their kappa beside the owners' and ask what a disagreement means: is the
  card ambiguous, or were the rules unclear? This makes them auditors of the instrument they were
  just measured with, rather than people who were measured by it. It touches no data and costs about
  fifteen minutes.

  The lesson only works in that order. A student who has watched a number they were proud of fall
  apart will ask the right question of an AI grading claim; a student shown someone else's kappa on
  a slide will not.

  **Not as a percentage, because a percentage flatters you.** If most opened sources really do agree
  with the student, both coders will write "agrees" most of the time, and two people who both write
  the same thing constantly will look like they agree even if neither read carefully. Say two coders
  matched on 85 of 100 sources — but one wrote "agrees" 90% of the time and the other 85%. Pure
  chance would already have produced about 78% matching. They beat luck by 7 points out of the 22
  that were available.

  **Cohen's kappa is that ratio**: (85 − 78) ÷ (100 − 78) = 0.32. So 85% agreement is really a kappa
  of 0.32, which the usual bands (Landis & Koch 1977 — 0.21–0.40 fair, 0.41–0.60 moderate,
  0.61–0.80 substantial, and these are conventions somebody proposed rather than laws) call *fair*.
  Not good enough to rest a finding on.

  **The same percentage can mean opposite things**, which is why the balanced menu above matters:

  | Two coders' matrix | Agreed | By chance | Kappa |
  |---|---|---|---|
  | `[[80,10],[5,5]]` | 85% | 78% | 0.32 |
  | `[[90,0],[5,5]]` | 95% | 86% | 0.64 |
  | `[[95,3],[2,0]]` | 95% | 95% | −0.02 |
  | `[[45,5],[5,45]]` | 90% | 50% | 0.80 |

  Rows two and three are both 95% agreement and land a full 0.66 apart; row four agrees *less* often
  and scores best of all. What separates them is how lopsided the categories are, not how often the
  coders matched. Named and worked through in
  [Feinstein & Cicchetti (1990)](https://pubmed.ncbi.nlm.nih.gov/2348207/), *Journal of Clinical
  Epidemiology* 43(6): 543–549.

  Worth also looking at **which way the disagreements run**. If one coder is consistently the more
  generous of the two, that is systematic bias rather than random noise, and kappa cannot tell them
  apart — but it shifts the measurement in one direction, which is the more damaging of the two.

  **Then make the connection, and only then.** An AI judge reported as reaching "over 80% agreement
  with humans" is quoting the flattering number. Converting to kappa typically costs 33–41
  percentage points, putting it around 0.4. Students who have just watched their own 85% collapse to
  0.32 will ask the right question of every AI grading claim they meet afterwards. The lesson works
  because they felt it on their own work first, so do not front-load it.
- **The control is the finding.** Plot every team's two rounds, take the paired difference, and put
  a confidence interval on it. Then ask what effect size eight teams could have detected at all.

## What this cannot show, and say so before it is run

- **It is underpowered, and now you can say by how much.** Work the numbers out before the session
  and put them on a slide, because this is the part students never see done. For a paired
  comparison at α = .05 two-tailed and 80% power, **8 paired observations can only detect an effect
  of about d_z ≈ 1.1** — enormous, and not a plausible size for a debiasing nudge. Thirty-two paired
  observations bring that to **about d_z ≈ 0.5**: still only a moderate-to-large effect, but inside
  the range where an intervention might actually live. Confirm both in G*Power or R rather than
  trusting these approximations, and have a student do it.
- **Do not compare d_z to Hart et al.'s d = 0.36.** They are different quantities — one is a
  within-person standardised difference, the other a between-condition effect — and converting
  between them needs the correlation between a person's two rounds, which nobody knows before the
  data exists. The temptation to line them up because both are called "d" is worth naming out loud.
- **A null result is evidence about the sample size and nothing else**, and a positive result on
  n = 32 in one room is not to be trusted either.
- **Demand characteristics are the biggest threat.** Students know the lecturer would like the agent
  to work. Do not state the hypothesis direction beforehand; have each team pre-register its own
  prediction; keep the menu's balance hidden until the debrief.
- **No blinding is possible.** Everyone knows which round had the agent.
- **Carryover between rounds** cannot be removed, only counterbalanced and reported.
- **Students inside a team share a context**, so the 32 observations are not fully independent even
  when the manipulation is individual. Eight clusters is too few to model properly; report it as a
  limitation rather than fitting something the data cannot support.
- **One session, one cohort, one task.** Nothing here generalises, and the write-up must say so.

Naming all five before the data exists is the difference between an experiment and a demonstration
dressed as one.

## Ethics

Students are participants, so the floor is not negotiable and it is the same floor the course
already applies to field research (ADR-0005, ADR-0013 route 4).

- Written consent, voluntary, and **no grade consequence either way** — consistent with ADR-0011,
  where neither weekly gate is scored.
- A team may withdraw its data after the debrief without explaining why.
- **Full debrief**, as Chiang et al. debriefed their participants about the biased model: the menu
  was balanced 50/50, here is what was manipulated, here is why you were not told.
- Nothing personal goes through an AI service. The agent sees the team's position and the sources
  they opened, and nothing else.
- This is teaching, not research. If it is ever written up for publication it needs institutional
  ethics approval first, and it falls under the Netherlands Code of Conduct for Research Integrity.

## What has to be built

| Thing | Where | Notes |
|---|---|---|
| The 16-source menu, crossed 2 × 2 | `work/drafts/` first | The real work. Cannot be improvised. |
| Agent prompts, two styles | `project-documentation/` | Off the site: the verdict variant only makes sense if students have not read it. Reuse the register from `../../project-documentation/socratic_agent/instructions.txt`. |
| Pre-registration sheet | `work/drafts/` | One page. |
| Codebook + the owners' coding sheet | `work/drafts/` | Two coders, full deck, kappa recorded with its matrix. |
| The debrief's eight-card coding set | `work/drafts/` | A balanced 4/4 subset of a deck the owners already coded, plus a blank 2×2 to fill in. |
| Session plan | `project-documentation/session-plan-week-03.md` | Does not exist yet; see issue #12 for the AIBS/AEL handovers it must name. |
| *Optional* `site/tool-source-menu.html` | `site/` | Presents the menu one item at a time, enforces the eight-item budget, timestamps choices, exports the data. Needs **no network calls**, so it sits inside the tool rules rather than straining them. |

## Reading behind this

- Chiang, C.-W., Lu, Z., Li, Z., & Yin, M. (2024). Enhancing AI-Assisted Group Decision Making
  through LLM-Powered Devil's Advocate. *IUI '24*, 103–119.
  [10.1145/3640543.3645199](https://doi.org/10.1145/3640543.3645199)
- Lee, S., Hwang, S., Kim, D., & Lee, K. (2025). Conversational Agents as Catalysts for Critical
  Thinking: Challenging Social Influence in Group Decision-making. *CHI EA '25*.
  [10.1145/3706599.3719792](https://doi.org/10.1145/3706599.3719792)
- Csaszar, F. A., Ketkar, H., & Kim, H. (2024). Artificial Intelligence and Strategic
  Decision-Making: Evidence from Entrepreneurs and Investors. *Strategy Science* 9(4): 322–345.
  [10.1287/stsc.2024.0190](https://doi.org/10.1287/stsc.2024.0190) — §2.3 makes the mechanism
  argument: an LLM devil's advocate is cheap where a human one costs days of skilled work, and it
  has no social inhibition about contradicting a senior person.
- Schwenk, C. R. (1984). Devil's Advocacy in Managerial Decision-Making. *Journal of Management
  Studies* 21(2): 153–168 — the review Csaszar et al. cite, and the source of the
  information-collection finding.
- Hart, W., et al. (2009). Feeling Validated Versus Being Correct. *Psychological Bulletin* 135(4):
  555–588. [10.1037/a0015701](https://doi.org/10.1037/a0015701)
- Jonas, E., Schulz-Hardt, S., Frey, D., & Thelen, N. (2001). *JPSP* 80(4): 557.
- Schweiger, D. M., Sandberg, W. R., & Ragan, J. W. (1986). *Academy of Management Journal* 29(1):
  51–71. [10.5465/255859](https://doi.org/10.5465/255859)

The four PDFs sit in `archive-local/`, which is git-ignored — they are not in the repository and
must not be committed.
