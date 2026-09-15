# Week 3 codebook — the two decks

**This file is the answer key and must never move into `site/`.** It maps each card id in
`site/tool-bias-experiment.html` to the cell it was coded into. The published page carries no
stance or quality label (SM-8), so this mapping is what Phase 2 needs to compute the result line,
and it is the only place the coding exists in machine-readable form.

The coding rule is the **denominator rule** set out in
[`week-03-candidate-claims.md`](week-03-candidate-claims.md): a source is *denominator-bearing*
(**S**) if it includes the cases that did the same thing and failed — it randomises, covers a
population, or reports the losers; it is *selected on outcome* (**W**) if it is one firm, one
founder, one vendor's customer, invited to explain what they did right. Direction (**A** / **NA**)
is coded against the claim as worded.

File order in the page is built in two steps. A hash of each source decides which card comes
first out of each cell, so the ordering is unrelated to the coding; the walk then never takes two
cards from the same cell in a row. The second step was added after the first, left alone, put all
four of deck 1's weak-opposing cards next to each other: an order can be independent of the cells
and still cluster them, and a cluster is a pattern a reader of the page source could work with.

## Deck 1 — round 1

> *An SME should run its AI on small models it controls rather than on frontier models it rents.*

## Deck 2 — round 2

> *An SME's first AI project should make its existing staff faster rather than remove steps from a
> process.*



### DECK1 — id to cell

| id | cell | meaning | source |
|---|---|---|---|
| `c1-01` | NAS3 | disagree, denominator-bearing | [`2026-09-01-cfa-institute-agentic-ai-finance-workflows-governance`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-09-01-cfa-institute-agentic-ai-finance-workflows-governance) |
| `c1-02` | AS3 | agree, denominator-bearing | [`2025-06-02-belcak-nvidia-small-language-models-future-agentic-ai`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-06-02-belcak-nvidia-small-language-models-future-agentic-ai) |
| `c1-03` | NAS1 | disagree, denominator-bearing | [`2026-03-11-allen-mcdonald-how-well-can-ai-do-strategy-simulation-benchmark`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-03-11-allen-mcdonald-how-well-can-ai-do-strategy-simulation-benchmark) |
| `c1-04` | AW1 | agree, selected on outcome | [`2026-08-11-huang-sequoia-own-your-intelligence-sovereign-ai`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-11-huang-sequoia-own-your-intelligence-sovereign-ai) |
| `c1-05` | NAS2 | disagree, denominator-bearing | [`2025-06-12-spracklen-package-hallucinations-code-generating-llms`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-06-12-spracklen-package-hallucinations-code-generating-llms) |
| `c1-06` | AS2 | agree, denominator-bearing | [`2025-04-04-prabhakar-salesforce-apigen-mt-xlam-2`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-04-04-prabhakar-salesforce-apigen-mt-xlam-2) |
| `c1-07` | AW4 | agree, selected on outcome | [`2026-08-06-garry-tan-own-your-intelligence`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-06-garry-tan-own-your-intelligence) |
| `c1-08` | NAS4 | disagree, denominator-bearing | [`2026-04-28-ai-index-report-2025`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-04-28-ai-index-report-2025) |
| `c1-09` | NAW2 | disagree, selected on outcome | [`2026-05-21-allen-aws-london-exec-forum-agentic-team-structures`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-05-21-allen-aws-london-exec-forum-agentic-team-structures) |
| `c1-10` | AW2 | agree, selected on outcome | [`2026-07-10-hugging-face-ceo-companies-done-renting-their-ai`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-07-10-hugging-face-ceo-companies-done-renting-their-ai) |
| `c1-11` | NAW1 | disagree, selected on outcome | [`2026-06-12-aws-leaders-guide-advanced-team-structures-agentic-world`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-12-aws-leaders-guide-advanced-team-structures-agentic-world) |
| `c1-12` | AS1 | agree, denominator-bearing | [`2025-07-13-patil-berkeley-function-calling-leaderboard`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-07-13-patil-berkeley-function-calling-leaderboard) |
| `c1-13` | NAW3 | disagree, selected on outcome | [`2026-09-14-google-cloud-agent-factory-agent-harnesses-explained`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-09-14-google-cloud-agent-factory-agent-harnesses-explained) |
| `c1-14` | AS4 | agree, denominator-bearing | [`2026-09-07-yc-paper-club-why-the-harness-matters-more-than-the-model`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-09-07-yc-paper-club-why-the-harness-matters-more-than-the-model) |
| `c1-15` | NAW4 | disagree, selected on outcome | [`2025-05-06-jassy-amazon-agility-ai-strategy-changing-role-of-managers`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-05-06-jassy-amazon-agility-ai-strategy-changing-role-of-managers) |
| `c1-16` | AW3 | agree, selected on outcome | [`2026-07-08-jensen-huang-why-companies-need-open-agent-systems`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-07-08-jensen-huang-why-companies-need-open-agent-systems) |

Cell counts: **AS 4**, **AW 4**, **NAS 4**, **NAW 4** — total 16.


### DECK2 — id to cell

| id | cell | meaning | source |
|---|---|---|---|
| `c2-01` | NAS1 | disagree, denominator-bearing | [`2025-07-10-becker-metr-early-2025-ai-experienced-developer-productivity`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-07-10-becker-metr-early-2025-ai-experienced-developer-productivity) |
| `c2-02` | AW2 | agree, selected on outcome | [`2026-02-18-lyft-customer-support-with-claude`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-02-18-lyft-customer-support-with-claude) |
| `c2-03` | NAS4 | disagree, denominator-bearing | [`2026-06-25-raboresearch-ai-it-zakelijke-dienstverlening`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-25-raboresearch-ai-it-zakelijke-dienstverlening) |
| `c2-04` | AS1 | agree, denominator-bearing | [`2026-04-28-brynjolfsson-li-raymond-generative-ai-at-work`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-04-28-brynjolfsson-li-raymond-generative-ai-at-work) |
| `c2-05` | NAS2 | disagree, denominator-bearing | [`2026-04-28-dellacqua-jagged-technological-frontier`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-04-28-dellacqua-jagged-technological-frontier) |
| `c2-06` | AS3 | agree, denominator-bearing | [`2025-06-09-krakowski-human-centered-ai-field-experiment`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-06-09-krakowski-human-centered-ai-field-experiment) |
| `c2-07` | NAW2 | disagree, selected on outcome | [`2026-04-25-masad-replit-ceo-only-two-jobs-left`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-04-25-masad-replit-ceo-only-two-jobs-left) |
| `c2-08` | AS4 | agree, denominator-bearing | [`2026-05-07-anthropic-economic-index-5-learning-curves`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-05-07-anthropic-economic-index-5-learning-curves) |
| `c2-09` | AW3 | agree, selected on outcome | [`2026-02-09-hubspot-customer-success-with-claude`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-02-09-hubspot-customer-success-with-claude) |
| `c2-10` | NAS3 | disagree, denominator-bearing | [`2025-06-01-autor-thompson-expertise`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-06-01-autor-thompson-expertise) |
| `c2-11` | NAW1 | disagree, selected on outcome | [`2026-08-14-blomfield-yc-building-structuring-ai-native-company`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-08-14-blomfield-yc-building-structuring-ai-native-company) |
| `c2-12` | AS2 | agree, denominator-bearing | [`2025-10-05-patwardhan-et-al-openai-gdpval`](https://businessdatasolutions.github.io/ai-wiki/sources/2025-10-05-patwardhan-et-al-openai-gdpval) |
| `c2-13` | NAW4 | disagree, selected on outcome | [`2026-06-19-lopopolo-ai-native-devcon-harness-engineering`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-19-lopopolo-ai-native-devcon-harness-engineering) |
| `c2-14` | AW4 | agree, selected on outcome | [`2026-06-18-ramaswamy-mckinsey-every-company-software-company`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-06-18-ramaswamy-mckinsey-every-company-software-company) |
| `c2-15` | NAW3 | disagree, selected on outcome | [`2026-05-27-scheffer-de-ondernemer-helloprint-ai-rebuild-from-day-zero`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-05-27-scheffer-de-ondernemer-helloprint-ai-rebuild-from-day-zero) |
| `c2-16` | AW1 | agree, selected on outcome | [`2026-07-14-khan-academy-ceo-the-real-ai-opportunity-is-in-boring-industries-sal-khan`](https://businessdatasolutions.github.io/ai-wiki/sources/2026-07-14-khan-academy-ceo-the-real-ai-opportunity-is-in-boring-industries-sal-khan) |

Cell counts: **AS 4**, **AW 4**, **NAS 4**, **NAW 4** — total 16.
## How the extracts were made

Every extract is quoted from the wiki's own capture of the source — `raw/papers`, `raw/videos`,
`raw/articles`, `raw/reports` in the [AI Wiki](https://github.com/businessdatasolutions/ai-wiki)
repository — and is checked back against that capture by
[`check-deck.py`](../../project-documentation/build/information-seeking-experiment/check-deck.py),
which fails if a quotation is not found. The check normalises both the quotation and the source
the same way, so nothing passes that the source does not say. What it normalises, and why each
one is needed:

| Normalisation | Why the captures need it |
|---|---|
| Whitespace and hyphens ignored | A PDF breaks words across lines, so `crowd-sourced` is captured as `crowdsourced`. |
| Two-column pages de-interleaved | `pdftotext` reads a two-column page across both columns, so a sentence is interrupted by whatever sits beside it. Both a document-wide gutter and a per-line gutter are tried, because column width changes from page to page. |
| Timestamps, speaker labels, chapter headings removed | Video captures are auto-transcripts: `[38:43]`, `**ANDY JASSY**:`, `## [26:40] …`. |
| Fillers removed — *um*, *uh*, *erm*, *like* | Auto-transcripts are full of them, and the transcripts use *like* as a filler (*"as like Claude 4.6 Opus"*). |
| Repeated words collapsed | The transcripts stutter: *"lower lower"*, *"local local"*. |
| Known transcription errors treated as equal | `LMS`/`LM` for *LLMs*, `Quen` for *Qwen*, `costum` for *cost um*, `aentic` for *agentic*. |
| Reference numbers, inline citations and footnote markers removed | `[70, 68, 36]`, `(Touvron et al., 2023)`, `augmentation.⁴`. |
| Combining accents dropped | So `dag één` is not read as `dag en`. |

Where a passage in the source is interrupted by something the card leaves out, the card marks the
omission with `[...]`. An unmarked cut fails the check — that is the difference between quoting
and paraphrasing. The paper's own internal apparatus (*see item CA4*, *see figure 4*) is elided
this way; anything substantive is kept.

## Three cards that were rebuilt, and why

The source cells in [`week-03-candidate-claims.md`](week-03-candidate-claims.md) recorded, for
each card, "the unambiguous bit". Checking each of those against the source turned up three that
were not in the document credited with them. The cells still hold four cards each; the card
*content* changed.

1. **Deck 1, AS1 — BFCL (Patil et al.).** The figures recorded against it (xLAM-2-70b 75.12 on
   multi-turn, against `o1` 36 and `gpt-4o` 41) are in **Prabhakar et al.**, the next card in the
   same cell — `75.12` occurs in exactly one file in the corpus. As written the two cards were one
   finding counted twice, which CL-2 forbids. BFCL's own open-model passage cuts the other way
   (xLAM-7B degrades on the crowd-sourced stress test), so the card is now built on the finding
   BFCL does carry with a denominator: most open models scored the same or better on 2,251 novel
   crowd-sourced tasks than on the static benchmark, which the authors read as evidence their
   scores are *"genuine capability rather than exposure to test solutions"*.
2. **Deck 2, AW3 — HubSpot.** "The redeployment-of-ten worked example" appears neither in the
   two-minute transcript nor on the wiki page. Rebuilt on what the video does say:
   *"it has helped amplify my expertise. We've seen a 40% increase in productivity."* Still a
   vendor-selected augmentation story, so the cell is unaffected.
3. **Deck 2, NAS4 — RaboResearch.** The ~44% whole-economy figure is not in the article. The
   86% (IT) and 64% (business services) figures are verbatim and are the stronger part.

## Access: what was checked, so it is not re-litigated

Subtask 0.6 asks that every source be openable and free. All 32 links were opened on
15 September 2026. Twenty-seven answer an ordinary request. **Five refuse an automated fetch with
HTTP 403 and open normally in a browser** — a bot challenge, not a wall — and each is open access
under a stated licence:

| Card | Source | Licence, per the wiki's own Source section |
|---|---|---|
| `c1-03` | Allen & McDonald, *Strategy Science* | open access, CC BY |
| `c2-03` | RaboResearch | a bank's public research page, no subscription |
| `c2-05` | Dell'Acqua et al., *Organization Science* | CC BY |
| `c2-04` | Brynjolfsson, Li & Raymond, *QJE* | CC BY-NC 4.0, open access via Oxford University Press |
| `c2-06` | Krakowski et al., *Management Science* | CC BY-NC-ND, open access |

A 403 from these publishers therefore means nothing about a student's ability to read them. Do not
treat it as a broken link, and do not repoint these cards at the wiki to route around it: a wiki
source page opens by naming the source *peer-reviewed* and *open access*, carries a **My take**
section and confidence scores, and all five of these cards are **strong** ones. Sending only the
strong cards to an appraisal, while the weak cards go to a raw vendor talk, would make the two
halves of the deck differ in what clicking through reveals — which is the one asymmetry this
instrument cannot afford, and the reason SM-8 keeps quality labels off a student's path at all.

## Two things to brief

- **`c2-15` — HelloPrint, De Ondernemer.** The article is free, but DPG Media puts a **cookie
  consent dialogue** in front of it: two buttons, *Akkoord* or *Instellen*, over text naming 4
  media partners and 101 advertising partners. No payment and no subscription, so 0.6 is satisfied
  — but this is the only card of the thirty-two that asks a student for a tracking decision, on a
  tool whose own promise is that nothing they do leaves their browser. Say so before the session
  rather than let someone meet it mid-exercise. The *~100 to 18* figure is the wiki's tag rather
  than the article's text, and is not quoted on the card.
- **`c1-08` — AI Index 2025.** The report is 457 pages of graphics and only its summary page yields
  text, so the quotation comes from there. The sentence *after* the one quoted reads *"Open-weight
  models are closing the gap with closed models, reducing the performance difference from 8% to
  just 1.7% on some benchmarks in a single year"* — which leans the other way. The card is coded on
  cost, where the source is unambiguous, but anyone who opens the link meets both.
- **`c1-09`, `c1-11`, `c1-13`, `c1-15` — the weak-opposing cell of deck 1.** Three of its four cards are Amazon, as
  the candidate-claims document already records. The rent-side case in this corpus is made almost
  entirely by one cloud vendor.
