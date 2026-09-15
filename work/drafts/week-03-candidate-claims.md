# Four candidate claims for the week 3 experiment

*Input to phase 0 of the [build plan](../../project-documentation/build/information-seeking-experiment/buildplan.html).
Three of these four will probably die in the pilot, which is what the pilot is for. Drafted from the
AI Wiki on 14 September 2026 using its own retriever (`scripts/wiki-retrieve.mjs`), then by reading
the concept pages.*

## How they were judged

Against the [CL rules](../../project-documentation/build/information-seeking-experiment/blueprint.html#cl-1),
plus one rule those do not yet contain.

**The denominator rule.** A source is *strong* if it includes the cases that did the same thing and
failed — by randomising, by covering a population, or by reporting the losers. It is *weak* if it is
selected on the outcome: one firm, one founder, invited to explain what they did right. This is a
better cut than peer-reviewed against vendor blog, because it is codeable by two people who will
agree, and because it puts a magazine founder profile in the same cell as a whitepaper, which is
where it belongs.

It rests on **Denrell (2003)**, *Organization Science* 14(2): 227–243,
[10.1287/orsc.14.2.227.15164](https://pubsonline.informs.org/doi/10.1287/orsc.14.2.227.15164):
risky practices unrelated to performance across a full population appear *positively* related to it
in a sample of survivors. Systematically misleading, in a predictable direction.

**Why this bit first.** A genre count over the wiki's 265 source pages — crude keyword matching, so
indicative only — returned roughly 77 podcast, keynote or interview pages and 72 vendor-channel
pages, against 60 peer-reviewed, arXiv or RCT pages and 26 surveys or benchmarks. The testimony
layer is the larger one. That does not disqualify the wiki; it means *which page* a claim rests on
matters more than the fact that the wiki carries it.

## The four

### 1 — Trusting your team's sense that AI is helping · **strongest**

> *A firm should trust its own people's judgement that AI is speeding them up, rather than wait to
> measure it.*

Wiki page: [`ai-coding-productivity-evidence`](https://businessdatasolutions.github.io/ai-wiki/concepts/ai-coding-productivity-evidence)
(confidence 0.8), which opens by stating the corpus holds **two RCTs with opposite signs**.

| | For trusting judgement | Against |
|---|---|---|
| Randomised | Cui et al. 2026 — 3 pre-registered field experiments, n = 4,867, **+26.08% tasks** (SE 10.3%) | METR 2025 — RCT, 16 developers, 246 tasks, **+19% time, i.e. slower** |
| Population | DORA 2025 — **over 80%** of ~5,000 respondents believe AI raised their productivity; throughput turned positive in 2025 | DORA 2025 — delivery **stability still negative**; 30% do not trust the tool they use |
| The killer | | METR's participants forecast −24%, estimated −20% afterwards, measured **+19%** — wrong by about 39 points, consistently |

Both sides carry denominators, which no other candidate manages. The claim is also *about* whether
to trust perception over measurement, so the deck and the lesson point the same way.

**Weakness:** the evidence is about developers and knowledge workers, not shop floors. A
manufacturing SME team may fairly ask what it has to do with them.

### 2 — Own the model or rent it

> *An SME should run its AI on small models it controls rather than on frontier models it rents.*

Wiki pages: [`open-source-ai`](https://businessdatasolutions.github.io/ai-wiki/concepts/open-source-ai)
(0.9), which names "the own-vs-rent thesis", and
[`small-language-models`](https://businessdatasolutions.github.io/ai-wiki/concepts/small-language-models)
(0.75), which carries a section headed **"The counter-arguments worth keeping"**.

That section is unusually honest and does half the work: it concedes the economic case is
unresolved — *"the jury is still out"* — and names roughly **$57bn committed to centralised
inference** as a barrier with a balance sheet behind it. On the other side, xLAM-2-70b scores 75.12
on multi-turn function calling against 41–47 for GPT-4o, while losing on τ-bench overall (56.2
against 60.1, 63.9 and 69.8).

**Scores best on CL-3**, the criterion most easily missed: frontier labs and open-weight vendors are
both selling, so the weak cells fill on both sides. Benchmarks give the strong cells a denominator
of a kind; the cost arguments have none.

### 3 — Augment people or automate the task

> *An SME's first AI project should make its existing staff faster rather than remove steps from a
> process.*

Wiki page: [`automation-vs-augmentation`](https://businessdatasolutions.github.io/ai-wiki/concepts/automation-vs-augmentation)
— the largest in the wiki, 11,541 words at confidence 0.95.

**Two problems.** Its evidence is largely the testimony layer: section headings include *"The
Claude-channel customer-story cluster"* and *"Nadella / Possible, June 2026"*. And "automate" sits
close to job loss, so it risks **CL-9** — a claim that becomes about employment measures values
rather than reading habits. The pilot decides that; nothing else can.

### 4 — Data model before agent · **best domain fit, thinnest evidence**

> *A manufacturing SME should get its process and data model in order before it puts an AI agent
> near the shop floor.*

Wiki pages: [`industrial-ai-agents`](https://businessdatasolutions.github.io/ai-wiki/concepts/industrial-ai-agents)
(0.75), which carries "Ontology vs. relational data model", and
[`lean-4-0`](https://businessdatasolutions.github.io/ai-wiki/concepts/lean-4-0) (0.70) with the
Lean ↔ Industry 4.0 mapping.

This is the only candidate about the course's actual population, which makes it the one everybody
will want. It is also the one most likely to fail **CL-2**: there is probably no denominator-bearing
source on either side, and both pages are thin.

## Where they stand

| | 1 Trust judgement | 2 Own or rent | 3 Augment or automate | 4 Data model first |
|---|---|---|---|---|
| CL-2 strong sources, both sides | **yes, with denominators** | partly | testimony-heavy | doubtful |
| CL-3 commercial advocates, both sides | likely | **yes, clearly** | likely | likely |
| CL-4 comparison form | yes | yes | yes | yes |
| CL-9 professional, not moral | yes | yes | **at risk** | yes |
| In the course's domain | weak | fair | fair | **strong** |
| CL-1 splits the room | pilot | pilot | pilot | pilot |
| CL-7 matched splits | pilot | pilot | pilot | pilot |
| CL-8 not a team's topic | owners | owners | owners | owners |

Nothing in the bottom three rows can be settled from a desk. **No cell has been filled with an
actual source yet** — what is established is that the wiki carries two-sided material on claims 1
and 2, and that it probably does not on claim 4.

## What to do next

1. Take claims **1 and 2** into the pilot first. They are the two most likely to survive.
2. Pilot claim **3** as well, specifically to find out whether it reads as a question about work or
   about jobs. If the room hears jobs, drop it.
3. Before spending anything on claim **4**, go looking for one denominator-bearing source on either
   side. If there is none, it cannot carry the strong cells however well it fits the course, and
   forcing it would break the instrument to keep the topic.
4. Remember the split the wiki cannot help with: it supplies the **strong** cells, because its
   sources are appraised and linkable. The **weak** cells are exactly what a curated wiki excludes,
   so they have to be hunted in the open — and that is the half that decides whether a claim is
   buildable at all.

---

# Source cells for claims 1–3

*Filled 15 September 2026 from the AI Wiki via `/wqa` (the `traceable-wiki-answer` skill:
`scripts/wiki-retrieve.mjs`, three retrievals, 238 candidates triaged). Full audit trail:
`inspiration/2026-09-15-week03-claim-source-cells-query-trace.{md,json}` in the wiki repo.*

## How S and W were coded

**By the denominator rule above, not by genre** — that is this document's own operational
definition, and it is the one applied here. **S** = the source includes the cases that did the same
thing and failed: it randomises, covers a population, or reports the losers. **W** = the source is
selected on the outcome: one firm, one founder, one vendor's customer, invited to explain what they
did right.

Two consequences worth stating before the tables, because they will look like coding errors
otherwise:

- **A peer-reviewed venue does not by itself earn S.** Yuan, Aseri & Ramasubbu is a working paper
  building an analytical model; it has no empirical denominator. It is marked S only because it
  reports its losers explicitly (which employee classes lose), and that judgement is contestable.
- **An HBR article can earn S.** Anicich & Brouwers reports a 604-respondent survey plus a
  48,000-person KPMG study. Under the denominator rule that is stronger than a keynote, whatever the
  masthead suggests. A `genre` column is given in each table so you can recode to the
  peer-reviewed/vendor cut if you prefer — the two codings disagree on exactly four rows, all flagged **⚠**.

**Direction (A / NA)** is coded against the claim *as worded*, and only unambiguous cases were
admitted. For claim 1 that means: **A = the source finds AI does speed people up, so the team's
sense of it is borne out**; **NA = the source finds self-report and measured effect come apart.**

## Result up front

| | AS | NAS | AW | NAW | total |
|---|:-:|:-:|:-:|:-:|:-:|
| **1 Trust judgement** | **4** | **4** | **4** | **4** | **16 ✅** |
| **2 Own or rent** | **4** | **4** | **4** | **4** | **16 ✅** |
| **3 Augment or automate** | **4** | **4** | **4** | **4** | **16 ✅** |

*All three fill. Reached over three passes: broad semantic retrieval (238 candidates) → five
cell-shaped queries (~200 more) → a **structural sweep** that enumerated all 44 corpus sources
tagged for model choice, benchmarks or openness and checked the ones the semantic queries never
surfaced. Claim 3 went 13 → 16; claim 2 went 12 → 14 → **16**. The last two sources came from the
structural sweep, not from search — see the method note at the end.*

**All three fill, 48 sources in total.** Two caveats that matter more than the count:

- **Claim 2 fills, but its NAW cell is three-quarters Amazon.** The rent-side case in this corpus is
  made almost entirely by one cloud vendor at three events, plus Google once — because every
  non-vendor candidate turned out to argue the *other* way (Nadella, Jensen Huang and the BBC's
  adviser are all A-leaning). The cell is usable; it would be materially stronger with one non-vendor
  voice from the open web. Details under that table.
- **Claim 3's NAS cell fills, but read what fills it.** All four disagree by showing **augmentation
  failing**, not automation succeeding. The corpus still has **no head-to-head study where
  automating a step beat assisting the worker on the same task**, and the
  `automation-vs-augmentation` page explains why: automation removes the worker, so per-worker
  productivity stops being a coherent outcome. Sufficient for the instrument — the cell needs
  sources that clearly *disagree*, and these do — but brief it deliberately rather than be ambushed.

One structural limit stands behind claim 2 regardless of cell counts, and the
`small-language-models` page states it: **no source measures an SLM agent against an LLM agent on
the same task, under the same harness, with the same evaluation.** Until someone runs that, both
strong cells rest on benchmark transfer.

## Claim 1 — *trust your people's judgement that AI is speeding them up* ✅ 16/16

### AS — agree, denominator-bearing

| # | Source | Denominator | The unambiguous bit | Genre |
|---|---|---|---|---|
| 1 | Cui, Demirer, Jaffe, Musolff, Peng & Salz 2026, *Management Science* — [`2026-02-27-cui-demirer-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-02-27-cui-demirer-generative-ai-high-skilled-work-three-field-experiments) | 3 pre-registered field experiments, **n = 4,867** | **+26.08% completed tasks** (SE 10.3%) — the belief is right at scale | peer-reviewed |
| 2 | Harvey & DeBellis, **DORA 2025** — [`2025-09-23-dora-2025-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-09-23-dora-2025-state-of-ai-assisted-software-development) | population survey, **~5,000** respondents | **>80% believe AI raised their productivity** *and* delivery **throughput turned positive** in 2025 — belief vindicated behaviourally | industry report |
| 3 | Brynjolfsson, Li & Raymond 2026, *QJE* — [`2026-04-28-brynjolfsson-li-raymond-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-04-28-brynjolfsson-li-raymond-generative-ai-at-work) | **5,172 agents**, 3,006,395 chats, staggered rollout ≈ individual random assignment | **+15% resolutions/hour**, low-skill **+30%** | peer-reviewed |
| 4 | Patwardhan et al. 2025, **GDPval** — [`2025-10-05-patwardhan-et-al-openai-gdpval`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-10-05-patwardhan-et-al-openai-gdpval) | **1,320 tasks, 44 occupations**, blind pairwise expert grading; non-saturating | model **+ expert oversight saved both time and money** vs unaided experts | arXiv (OpenAI) |

### NAS — disagree, denominator-bearing

| # | Source | Denominator | The unambiguous bit | Genre |
|---|---|---|---|---|
| 1 | Becker, Rush, Barnes & Rein 2025, **METR** — [`2025-07-10-becker-metr-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-07-10-becker-metr-early-2025-ai-experienced-developer-productivity) | RCT, task-level randomisation, 16 devs / **246 tasks** | forecast **−24%**, post-hoc estimate **−20%**, measured **+19% slower** — wrong by ~39 points *after doing the work* | arXiv |
| 2 | Dell'Acqua et al. 2026, *Organization Science* 37(4) — [`2026-06-12-dellacqua-cybernetic-teammate-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-12-dellacqua-cybernetic-teammate-field-experiment-genai-teamwork) | preregistered, **N = 791** at Procter & Gamble | **+0.37 SD performance** (p<0.01) while **9.2 pp *less* likely** to expect a top-10% placement (p<0.05) — decoupling, opposite sign to METR | peer-reviewed |
| 3 | Anicich & Brouwers 2026, *HBR* — [`2026-06-10-anicich-brouwers-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-10-anicich-brouwers-why-employees-arent-transparent-ai-usage) ⚠ | KPMG/Melbourne **n > 48,000**; own survey **n = 604** | **57% admit hiding their AI use**; **30.3%** withheld knowledge; lowest-trust quartile **~4×** more likely to hide (47% vs 14%) — self-report is structurally incomplete | practitioner article |
| 4 | Liu et al. 2026, SMU, arXiv:2603.28592 — [`2026-03-30-liu-debt-behind-the-ai-boom`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-03-30-liu-debt-behind-the-ai-boom) | **484,366 issues** mined across assistants | **22.7% of AI-introduced issues never fixed**; **>15%** of commits introduce ≥1 issue — the felt speed-up has an unbilled ledger | arXiv |

*Bench (all denominator-bearing, same direction, if you want substitutes):* Veracode 2025 — **45%**
of AI-generated samples carry OWASP Top-10 flaws, flat across model size; Abujadallah et al. 2026
(MSR) — **46.41%** of agent-proposed PRs rejected across 306 PRs; Gloaguen et al. (ETH) — context
files raise inference cost **>20%** for no measured success gain.

### AW — agree, selected on outcome

| # | Source | Why weak | The unambiguous bit |
|---|---|---|---|
| 1 | Tan, *Own Your Intelligence*, YC Startup School — [`2026-08-06-garry-tan-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-06-garry-tan-own-your-intelligence) | accelerator CEO, n=1, metric he disowns on stage | **~400×** his 2013 output, *"still 8x at the absolute floor"* |
| 2 | Darroman, *Profitable Founder* — [`2026-07-25-darroman-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-07-25-darroman-profitable-founder-managing-ai-agents-25-prs-a-day) | one solo founder, invited to explain the method | **22–25 PRs/day, sometimes 40**, from 5–10 concurrent agents |
| 3 | Blum, *How I AI* — [`2026-08-31-blum-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-31-blum-how-i-ai-claude-cowork-pm-system) | one PM, self-reported, unaudited | *"I'm really able to do in a day now what used to take me a week"* |
| 4 | Ramaswamy (Snowflake CEO) / McKinsey — [`2026-06-18-ramaswamy-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-18-ramaswamy-mckinsey-every-company-software-company) | one firm, CEO on a podcast | whole company **AI-literate in six weeks** via viral adoption, no mandate, no training programme |

### NAW — disagree, selected on outcome

| # | Source | Why weak | The unambiguous bit |
|---|---|---|---|
| 1 | Frey / Bloomberg *Trumponomics* — [`2026-08-05-frey-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-05-frey-bloomberg-trumponomics-why-ai-isnt-boosting-productivity) | expert interview; no denominator of its own | AI is **not** showing up in aggregate productivity; the verification tax is why |
| 2 | BBC *AI Decoded* — [`2026-08-01-bbc-ai-decoded-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-01-bbc-ai-decoded-why-isnt-ai-working-for-your-company) | broadcast panel, chosen for the argument | the premise is the title; firms feel gains they cannot show, **3:1** tool-access-to-training ratio |
| 3 | Carson / *How I AI* — [`2026-08-24-carson-vo-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-24-carson-vo-how-i-ai-manage-15-ai-agents-solo-founder) | one founder; the anti-thesis inside a success story | *"I don't think I get multiples of quality off of multiples of output"* |
| 4 | Forsgren & Macvean, DORA 2026 — [`2026-04-21-forsgren-macvean-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-04-21-forsgren-macvean-build-core-skills-thrive-ai-era-developer) | leadership guidance, no measurement attached | **productive struggle** — deliberately work *through* complexity rather than offload it; treats felt ease as a thing to resist |

**Note on #4:** the least direct row in claim 1. It argues against acting on the feeling of speed
rather than against the feeling's accuracy. If a coder rejects it, the wiki has no clean fourth NAW
and claim 1 lands at 15/16.

## Claim 2 — *run small models you control rather than frontier models you rent* ✅ 16/16

### AS — agree, denominator-bearing ✅ 4/4

| # | Source | Denominator | The unambiguous bit |
|---|---|---|---|
| 1 | Patil et al. 2025, **BFCL** (UC Berkeley, ICML) — [`2025-07-13-patil-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-07-13-patil-berkeley-function-calling-leaderboard) | **>67,000** community datapoints → 2,251 curated; ~110 models ranked | multi-turn: **xLAM-2-70b 75.12 vs GPT-4o 41–47, `o1` 36**; even the **1B** model beats `o1` and `gpt-4o` on multi-turn |
| 2 | Prabhakar et al. 2025, **xLAM-2 / APIGen-MT** (Salesforce AI Research) — [`2025-04-04-prabhakar-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-04-04-prabhakar-salesforce-apigen-mt-xlam-2) | full benchmark suite; models + data open-sourced (CC BY) | an open-weight family you can host tops multi-turn function calling |
| 3 | Belcak et al. 2025 (NVIDIA Research + Georgia Tech) — [`2025-06-02-belcak-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-06-02-belcak-nvidia-small-language-models-future-agentic-ai) | benchmark roster (**4 of 8 from their own lab** — discount accordingly) | serving 7B is **10–30× cheaper** in latency/energy/FLOPs; an SLM of size *x* ≈ a generalist **10×** its size on the four agentic capabilities |
| 4 | Saad-Falcon et al., **OpenJarvis** (Stanford / Hazy Research), presented at YC Paper Club — [`2026-09-07-yc-paper-club-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-09-07-yc-paper-club-why-the-harness-matters-more-than-the-model) ⚠ | tested across multiple cloud optimisers × multiple local models; **states its own limit** (*"many tasks for which local-size LLMs are not enough"*) | local models are *"only 6 to 12 months behind"* frontier; a cloud model optimises the local stack **once**, then it runs locally at **~800× lower inference cost**, beating out-of-the-box local on cost, latency *and* quality |

**⚠ on row 4:** the wiki holds this **second-hand** — a conference talk about the project, not the
paper. The numbers are unverified here. It is the only remaining pro-small source with any
denominator at all; every other one is a practitioner or vendor talk without one (Sokolenko at
PyCon DE; Google Cloud's *Agent Factory* loop-count argument, which the wiki flags as *"a vendor
recommending its own cheaper tier, with no measurements attached"*).

### NAS — disagree, denominator-bearing ✅ 4/4

| # | Source | Denominator | The unambiguous bit |
|---|---|---|---|
| 1 | Allen & McDonald 2026, *Strategy Science* 11(1):93–117 — [`2026-03-11-allen-mcdonald-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-03-11-allen-mcdonald-how-well-can-ai-do-strategy-simulation-benchmark) | **21 proprietary + 13 open-source** models, identical conditions | open models score **substantially below** proprietary and *"plateaued at a markedly lower level"* |
| 2 | Spracklen et al. 2025, **USENIX Security '25** — [`2025-06-12-spracklen-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-06-12-spracklen-package-hallucinations-code-generating-llms) | **16 models, 2.23 million** generated samples | package-hallucination rate **≥5.2% commercial vs 21.7% open-source** — a **four-fold** gap, and a *class* difference rather than a capability gradient |
| 3 | CFA Institute roundtable — [`2026-09-01-cfa-institute-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-09-01-cfa-institute-agentic-ai-finance-workflows-governance) ⚠ | Tate ran open alternatives through an **identical pipeline** against a proprietary baseline | the open model **matched on the task and failed on throughput** (proprietary batch API: 50,000 requests back in 24h); Pisaneschi: open lags ~3 months, the **harness** is the moat, *"a winner take all scenario"* |
| 4 | **AI Index 2025** (Stanford HAI), 8th annual — [`2026-04-28-ai-index-report-2025`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-04-28-ai-index-report-2025) | industry-wide price and benchmark series, tracked across vendors and time by an independent academic body | it attacks the own-side case on **its own chosen ground, cost**: inference cost **cratered 280-fold in 18 months** at fixed quality (Nov 2022 **$20/M tokens** → Oct 2024 **$0.07/M tokens**), with hardware costs falling **30%/yr** and energy efficiency improving **40%/yr**. Renting got two orders of magnitude cheaper while you were deciding whether to self-host |

**A note on row 3 and the cell that nearly stayed short.** The CFA roundtable is the one source that
could sit equally in NAW below (podcast genre ⇒ W; controlled pipeline comparison ⇒ S). It is placed
here, in NAS, on method. That left NAW short until the structural sweep found Jassy — see below.
**GDPval was considered and dropped**: it never *tested* a small or open model, so "no open model is
in contention" is an argument from silence rather than a clear disagreement.

The first pass also had BFCL in this cell for its τ-bench result (xLAM-2-70b **56.2** vs Claude 3.5
Sonnet 60.1, `o1` 63.9, Claude 3.7 **69.8**). **That has been removed**: it is the same paper as
AS#1, and using one source on both sides of a claim is exactly what CL-2 forbids. The τ-bench number
is still worth knowing — it is why the pro-small case is narrow rather than general — but it cannot
be a cell.

### AW — agree, selected on outcome ✅ 4/4

| # | Source | Why weak | The unambiguous bit |
|---|---|---|---|
| 1 | Huang / Sequoia, *Own Your Intelligence* — [`2026-08-11-huang-sequoia-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-11-huang-sequoia-own-your-intelligence-sovereign-ai) | investor addressing her own portfolio at an event designed to change its behaviour | **"not your weights, not your product"** |
| 2 | Delangue / Hugging Face (TechCrunch *Equity*) — [`2026-07-10-hugging-face-ceo-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-07-10-hugging-face-ceo-companies-done-renting-their-ai) | sells open-model infrastructure | companies *"need to own AI and own models instead of renting them"* |
| 3 | Jensen Huang / NVIDIA (via LangChain) — [`2026-07-08-jensen-huang-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-07-08-jensen-huang-why-companies-need-open-agent-systems) | sells the silicon and the open weights beneath the argument | build proprietary specialised agents on an **open** substrate |
| 4 | Tan / YC, *Own Your Intelligence* — [`2026-08-06-garry-tan-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-06-garry-tan-own-your-intelligence) | accelerator CEO, open-sourcing his own stack | *"model quality is rented but your brain is owned"* |

This is the cell CL-3 predicted: **all four are selling something that gets more valuable if you
stop renting.** The wiki flags the shared blind spot itself — none of them measures the outcome.

### NAW — disagree, selected on outcome ✅ 4/4

| # | Source | Why weak | The unambiguous bit |
|---|---|---|---|
| 1 | AWS Leaders' Guide, Summit Sydney Exec Forum — [`2026-06-12-aws-leaders-guide-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-12-aws-leaders-guide-advanced-team-structures-agentic-world) | cloud vendor whose business is renting inference | the **pricing scissors** — training costs **+2.4×/yr**, inference **−10×/yr**, gap opening **12–24×/yr**; frontier creation costs billions while *using* one *"collapses toward zero"*. Hence **USE / COMPOSE** before BUILD |
| 2 | Allen / AWS London Exec Forum — [`2026-05-21-allen-aws-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-05-21-allen-aws-london-exec-forum-agentic-team-structures) | same vendor, different event; base rate is **his own customer book** | **~80% of his customers land on COMPOSE** — frontier-model APIs — and *"they don't want to train those models. They just want to hit the frontier model."* BUILD is justified *only* when *"a frontier model can actually give you an inference cost which is cheaper than you maintaining that model"* |
| 3 | Google Cloud, *Agent Factory* — [`2026-09-14-google-cloud-agent-factory-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-09-14-google-cloud-agent-factory-agent-harnesses-explained) | vendor recommending its own tier; wiki notes **no measurements attached** | the answer to loop-count cost is a **cheap rented frontier tier** (Gemini 3.8 Flash as daily driver), not a self-hosted model |
| 4 | Jassy (Amazon CEO), *Agility* — [`2025-05-06-jassy-amazon-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-05-06-jassy-amazon-agility-ai-strategy-changing-role-of-managers) | the CEO of the company selling the middle layer; the wiki flags the passage as *"a directed marketing message — Amazon-as-stack-vendor"* | his three-layer stack is built around a middle tier explicitly for **"teams that don't want to train models"** — served by *"the largest selection of leading third-party frontier models"* (Bedrock) plus your own data, guardrails, RAG and agents. Self-hosting is the *bottom* layer, for model builders, not for firms like the reader |

**Three of the four are Amazon.** That is a genuine CL-3 weakness in this cell and you should know it
before using it: **the rent-side case in this corpus is made almost entirely by one cloud vendor**,
at three different events, plus Google once. It is not that the argument is weak — the pricing
scissors and the 280-fold cost collapse are serious — it is that **nobody outside the hyperscalers
makes it out loud.** Two consequences: the cell is fillable but monotone, and swapping any row for a
non-vendor voice found on the open web would strengthen the claim materially.

**Why that is, and it is the most interesting thing this pass found.** Every non-vendor candidate
turned out **A**-leaning. Nadella: *"don't use frontier models for non-frontier problems."* Jensen
Huang: *"start with the frontier… as soon as it gets good enough, specialize."* The BBC's enterprise
adviser predicts a **return to on-prem**, self-hosting an open model behind a firewall and routing
by sensitivity. Chamath and Snowflake's CEO both host open models *alongside* frontier — ambiguous,
so excluded. **Hyperscalers sell renting rather than arguing for it**, so the case against ownership
is mostly made by people with a price list rather than by people with a finding.

*Substitute worth noting for **AW**:* the BBC's Grant ([`2026-08-01-bbc-ai-decoded-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-01-bbc-ai-decoded-why-isnt-ai-working-for-your-company))
makes the own-side case while selling **advisory rather than models** — a less conflicted voice than
the four vendors and investors currently in that cell, if CL-3 monotony bothers you.

## Claim 3 — *augment existing staff rather than remove process steps* ✅ 16/16

### AS — agree, denominator-bearing ✅ 4/4

| # | Source | Denominator | The unambiguous bit |
|---|---|---|---|
| 1 | Brynjolfsson, Li & Raymond 2026, *QJE* — [`2026-04-28-brynjolfsson-li-raymond-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-04-28-brynjolfsson-li-raymond-generative-ai-at-work) | 5,172 agents, 3.0M chats | the system was **"designed to augment (rather than replace) human agents"** — suggestions to the agent only, full discretion to ignore — and returned **+15%**, low-skill **+30%** |
| 2 | Patwardhan et al. 2025, **GDPval** — [`2025-10-05-patwardhan-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-10-05-patwardhan-et-al-openai-gdpval) | 1,320 tasks, 44 occupations, blind expert grading | **model + expert oversight beat either alone**, cheaper *and* faster — the augmentation case measured rather than argued |
| 3 | Krakowski, Rizzo et al. 2025, *Management Science* — [`2025-06-09-krakowski-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-06-09-krakowski-human-centered-ai-field-experiment) | 3-arm field experiment, **N = 72**, DiD; **reports its losing arm** | tailored augmentation (D3) raises performance and utilisation; **untailored AI (D2) saw utilisation and performance *decline* as staff withdrew from the system** |
| 4 | **Anthropic Economic Index**, 4th → 5th reports — [`2026-05-07-anthropic-economic-index-5-learning-curves`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-05-07-anthropic-economic-index-5-learning-curves) | millions of Claude conversations, classified per conversation | augmentation leads in **4 of 5 samples**; latest sample **53% augmentation (+1 pp) / 44% automation (−1 pp)** — the split is **stable, not drifting toward automation** |

*Bench:* Boussioux et al. 2024 — 300 evaluators, 3,900 evaluator-solution pairs; differentiated
human-AI search scores highest on quality, viability and value.

### NAS — disagree, denominator-bearing ✅ 4/4

*This cell was empty after the first pass and is the main thing the second pass fixed. Read the
caveat under the table — **what fills it matters as much as that it fills**.*

| # | Source | Denominator | The unambiguous bit |
|---|---|---|---|
| 1 | Becker, Rush, Barnes & Rein 2025, **METR** — [`2025-07-10-becker-metr-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-07-10-becker-metr-early-2025-ai-experienced-developer-productivity) | RCT, task-level randomisation, 246 tasks | the claim's own recommendation, measured: assisting experienced staff made them **+19% slower**. Doing exactly what claim 3 advises produced a negative result |
| 2 | Dell'Acqua et al. 2026, *Organization Science* — [`2026-04-28-dellacqua-jagged-technological-frontier`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-04-28-dellacqua-jagged-technological-frontier) | RCT, random assignment within task arms, **758 BCG consultants** | **outside the frontier, AI users are 19 pp *less* likely to be correct** (84.5% control → 60.0% / 70.6%) — and *"subjective coherence quality is higher with AI even when answers are wrong"* |
| 3 | Autor & Thompson 2025, **NBER** — [`2025-06-01-autor-thompson-expertise`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-06-01-autor-thompson-expertise) | occupation-level panel across the US economy; historical automation record | **removing** tasks is not uniformly bad and assisting is not uniformly good: *removing inexpert tasks* and *adding expert tasks* both predict **wage gains**; removing expert tasks predicts declines. Which steps you remove decides the outcome — the blanket "augment rather than remove" is the wrong instruction |
| 4 | RaboResearch (Rabobank) 2026 — [`2026-06-25-raboresearch-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-25-raboresearch-ai-it-zakelijke-dienstverlening) | sector-wide coverage of the Dutch economy, occupation-task classification | automation is broadly feasible, not marginal: **(high) potential 86% in IT, 64% in business services, ~44% across the whole economy** — which contradicts the premise that removing steps is the harder or later option |

*Bench:* Yuan, Aseri & Ramasubbu 2026 (SSRN 6103949) — [`2026-01-20-yuan-aseri-ramasubbu-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-01-20-yuan-aseri-ramasubbu-backfiring-ai-deployment-workplace)
⚠ — analytical model, no empirical denominator, but it **reports its losers** explicitly: AI that
transfers hard skill **backfires**, the firm gains (**+**) and the augmented employees do not
(**0/−**). Use it if you want a fifth, code it W if you follow the peer-reviewed/vendor cut.

**The honest caveat, and it is important for how you brief this claim.** All four disagree by
showing **augmentation failing**, not by showing **automation succeeding**. The structural point from
the first pass survives in narrower form: the corpus still contains **no head-to-head study where
automating a step beat assisting the worker on the same task**, and the
`automation-vs-augmentation` page explains why —

> *"We do **not** have equivalent rigorous studies of pure-automation productivity gains in the wiki
> — because pure automation replaces the worker entirely, so 'productivity per worker' is no longer
> a coherent measurement."*

For the instrument this is **fine**: the cell needs four strong sources that clearly disagree with
the claim, and these four do, unambiguously and with real denominators. But if a participant asks
*"where is the evidence that automating works better?"*, the honest answer is that it is not here
and probably cannot be, because the outcome measure dissolves. That is a good discussion to have on
purpose rather than to be ambushed by.

### AW — agree, selected on outcome ✅ 4/4

| # | Source | Why weak | The unambiguous bit |
|---|---|---|---|
| 1 | Khan / Khan Academy — [`2026-07-14-khan-academy-ceo-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-07-14-khan-academy-ceo-the-real-ai-opportunity-is-in-boring-industries-sal-khan) | one organisation, CEO stating a policy | *"if we could do 3x more with the same resources, we will do 3x more; that would never be the catalyst for layoffs"* — the catalyst is revenue, *"not AI"* |
| 2 | Lyft customer support with Claude — [`2026-02-18-lyft-customer-support-with-claude`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-02-18-lyft-customer-support-with-claude) | vendor-published customer story, chosen because it worked | agents assisted, not removed |
| 3 | HubSpot customer success with Claude — [`2026-02-09-hubspot-customer-success-with-claude`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-02-09-hubspot-customer-success-with-claude) | same channel, same selection | the **redeployment-of-ten** worked example |
| 4 | Ramaswamy / Snowflake — [`2026-06-18-ramaswamy-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-18-ramaswamy-mckinsey-every-company-software-company) | one firm, CEO on a podcast | **redeploy, don't cut** — the demo team moved into other roles |

### NAW — disagree, selected on outcome ✅ 4/4

| # | Source | Why weak | The unambiguous bit |
|---|---|---|---|
| 1 | Blomfield / YC — [`2026-08-14-blomfield-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-14-blomfield-yc-building-structuring-ai-native-company) | early-stage greenfield startups advised by his own firm; the wiki notes **no failure modes are described anywhere in the talk**, and he says *"no one knows how to do this"* | rejects the multiplier framing outright: *"previously AI is like make each person 20% more productive… **what happens if we reimagine the company as a series of AI loops?**"* — and therefore **no middle management** |
| 2 | Masad / Replit — [`2026-04-25-masad-replit-ceo-only-two-jobs-left`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-04-25-masad-replit-ceo-only-two-jobs-left) | founder narrating his own product's history | successive **removal of whole layers** — environment, deployment, then writing code itself |
| 3 | **Scheffer / HelloPrint**, *De Ondernemer* — [`2026-05-27-scheffer-de-ondernemer-...`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-05-27-scheffer-de-ondernemer-helloprint-ai-rebuild-from-day-zero) | one founder, interviewed about a rebuild he chose himself; no firm that attempted the same and failed appears anywhere in the piece | the **day-zero rebuild** — *"wat nou als ik mijn huidige bedrijf op dag één opnieuw zou moeten bouwen, wat zou ik dan doen?"* — dissolves the functional departments and takes customer service from **~100 people to 18** |
| 4 | Lopopolo / AI Native DevCon — [`2026-06-19-lopopolo-ai-native-devcon-harness-engineering`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-19-lopopolo-ai-native-devcon-harness-engineering) | practitioner talk from inside a success case | **humans steer, agents execute** → the explicit glide toward *"more headless"* |

*Bench:* Nishar & Nohria 2026 — [`2026-05-05-nishar-nohria-end-of-one-size-fits-all`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-05-05-nishar-nohria-end-of-one-size-fits-all)
— framework article, no denominator; **Buy Outcomes** is the most automative of its four models, the
vendor taking the whole job rather than discrete tasks. Held here after the swap below.

**Why HelloPrint displaced it: domain.** The other three cards in this cell are software-sector
voices — a YC partner, a dev-tools founder, a DevCon talk — and Nishar & Nohria was a framework with
no firm inside it at all. HelloPrint is Dutch, turns over €80M and prints physical things, which is
as near the course's population as this cell is likely to get. Claim 3's domain fit was rated *fair*
in the table above; this is the card that moves it.

**And it takes CL-9 to its worst case, deliberately.** The headline is *"Elke kantoorbaan voor een
scherm verdwijnt"*, and Scheffer says *"Heel veel banen die wij kennen, gaan gewoon echt
verdwijnen."* A student who opens this card is reading about redundancy. So the card belongs in the
**0.3 pilot**: if the room hears jobs when shown the sharpest card in the deck, claim 3 fails CL-9
for the price of one source rather than sixteen.

**Two things to settle before it counts as a card.** First, the extract at subtask 0.7 has to be
quoted from the original — `deondernemer.nl/innovatie/ondanks-80-miljoen-omzet-gooit-hans-scheffer-zijn-bedrijf-volledig-om-met-ai-elke-kantoorbaan-voor-een-scherm-verdwijnt`
— because the wiki page is a summary of it, and SM-7 wants the quotation found verbatim in the
source while SM-11 wants the link to point at it. The *~100 to 18* figure is the wiki's so far,
carried in its `customer-service-100-to-18` tag, and is unverified here. Second, the article would
not open from this machine, so someone has to confirm it is readable without a DPG subscription
(0.6). If it is metered, the card fails however well it fits, and Nishar & Nohria comes back off the
bench.

## What this changes in the plan above

*Revised twice. The first pass recommended dropping claim 3 and called claim 2 short; **both
judgements are withdrawn.** All three claims fill.*

1. **Claim 1 remains the lead.** Every cell filled, and it gained the thing the earlier draft could
   not know: the perception gap **runs both ways** as of the wiki's 2026-09-15 revision. Dell'Acqua
   et al. found people *underestimating* themselves while outperforming — the mirror image of METR.
   The transferable claim narrowed to *"self-assessment decouples from performance under AI, in a
   direction that is not predictable from the technology alone."* **This makes claim 1 better**: the
   lesson is no longer "people overrate AI", which a room can dismiss as scolding, but "the
   instrument is broken in both directions", which nobody can.
2. **Claim 2 is buildable, with one repair.** 16/16, but hunt one non-vendor rent-side voice on the
   open web to break the Amazon monotony in NAW — any "why we moved off self-hosting" post. Note also
   that its strong cells rest on benchmark transfer, which is the honest limit to state if a
   participant presses.
3. **Claim 3 is back in contention, and the plan's original instruction stands.** Pilot it to find
   out whether the room hears "work" or "jobs" (CL-9). That was always a pilot question; the
   evidence base is no longer the reason to drop it. Its NAW cell has since been swapped: the
   HelloPrint interview replaces Nishar & Nohria, which buys the cell a Dutch physical-product firm
   and makes the CL-9 question as sharp as this corpus can make it. **Show that card in the pilot.**
4. **Claim 4 is untested by this pass** (not requested). The item-3 instruction in the original plan
   still stands.

## Method note — three passes, and what actually worked

| Pass | Method | Candidates | Yield |
|---|---|---:|---|
| 1 | Three broad semantic queries via `wiki-retrieve.mjs` (qmd ∪ graph, RRF) | 238 | found the claims; filled claim 1 only |
| 2 | Five **cell-shaped** queries naming the *evidence shape* wanted | ~200 | +7 sources; claim 3 → 16, claim 2 → 14 |
| 3 | **Structural sweep** — enumerated all 44 corpus sources tagged for model choice / benchmarks / openness, then read the ones search never surfaced | 44 | +2 sources; claim 2 → 16 |

**Three lessons worth keeping for the next claim.**

1. **Broad semantic retrieval finds topics, not cells.** Pass 1 returned 238 candidates and filled
   one claim of three. The queries that worked in pass 2 named the *shape of evidence* — "RCT where
   AI assistance made workers worse", "measured comparison open-weight versus proprietary" — not the
   subject.
2. **Search saturates before the corpus is exhausted.** By pass 2 repeated queries returned the same
   pool, which looked like exhaustion and was not. The last two sources — **AI Index 2025**'s
   280-fold inference-cost collapse and **Jassy**'s three-layer stack — were both sitting in the
   corpus, tagged, and never surfaced by any of eight semantic queries. A `grep` over frontmatter
   tags found them in one command.
3. **The same source reads differently against different claims.** METR was a claim-1 source in pass
   1 and turned out to be one of the strongest claim-3 NAS sources in pass 2 — the same RCT, read
   against a different proposition. Worth re-reading the shortlist against each claim rather than
   assigning each source once.
