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
