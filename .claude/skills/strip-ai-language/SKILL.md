---
name: strip-ai-language
description: Use when English text may read as machine-written and has to sound human before a reader sees it — course pages, slides, reports, web copy, mail. Triggers include "this reads like ChatGPT", "check for AI speak", "take the AI language out", "too smooth", "sounds generated", a "not X, but Y" construction, or text aimed at a named audience such as first-year students.
---

# Recognising English AI language and writing it out

## The core rule

**A smooth sentence that tells you nothing new is an empty sentence.** AI language
does not announce itself with errors. It announces itself with form: antitheses
that imitate insight, strong words with no evidence behind them, and a rhythm in
which every sentence is the same length. The reader feels momentum and keeps nothing.

## Why an ordinary edit pass misses this

Measured on this repository's own site — 24,034 words across five pages. A scan for
the forty-two words everyone lists as AI vocabulary (*delve, leverage, robust,
seamless, unlock, crucial, comprehensive, foster, moreover, landscape, tapestry,
embark, holistic, transformative*…) returned **four hits**, all four in one document.
On the same text the antithesis (A1) appears **173 times** — 26 of them on the
landing page, roughly one sentence in eight.

A word list would have declared that site clean. See
[`example/wordlist-baseline.md`](example/wordlist-baseline.md).

That is the trap in this failure form: **whoever does not recognise it as a form
rewrites it into their own prose.** Hence a recipe below, and not only a prohibition.

## Method

1. **Run the script.** It points at what a rule can point at.

   ```bash
   python3 scripts/aiprose.py page.md
   python3 scripts/aiprose.py deck.html --ignore-html-class notes --block-tag span
   # notes = skip speaker text; block-tag = don't count separate cards as one long sentence
   python3 scripts/aiprose.py dir/ --recursive --codes A1,A2 --json findings.json
   ```

2. **Weigh every finding.** A finding is an indication, not a verdict — see the
   precision column.
3. **Rewrite with the recipe**, not by feel. Otherwise the construction comes back.
4. **Read [`patterns.md`](patterns.md)** for the forms no rule can find (A13 to A15).
5. **Re-run the script.** A rewrite that produces a new finding is not a rewrite.

## The recipe for the antithesis (A1)

The most common form by a wide margin, and the only one with a fixed solution:

1. **Delete the negated half.** Does a sentence remain that is true? Done.
2. **Does it no longer hold?** Then the negation carried information. Give it its own
   sentence, with the party who thinks it: *"Many people assume X. In fact Y, because Z."*
3. **Is it about a boundary?** Replace the negation with an example that shows the boundary.

| Before | After | What happened |
|---|---|---|
| They are instruments, not homework | Nothing here is marked. Use them or don't | negated half deleted |
| Success is not only about money, but also about people and knowledge | Success is about money, people and knowledge | a list in disguise, unpacked |
| It is not a technology question, but an organisational one | The board asks about technology. The answer is about who may decide what | misconception given an owner, then the answer |

## When it stays

Not every antithesis is hollow. It is doing work if it survives all three questions:

1. **Is the negated side on the page?** If the reader has just written, said or read
   it, the negation rejects something that is genuinely there.
2. **Does deleting it cost information?** Remove the negated half. If the meaning
   changes, it carried something.
3. **Is it a contrast or an addition?** *"Not only X, but also Y"* means X and Y — a
   list in disguise, and it goes.

A measured example from this repository: *"you get questions back, never a verdict
and never a score"* survives all three. The gate design is exactly the distinction
between a question and a verdict; delete the negated half and the sentence stops
saying what a gate is. It stays. On the same page, *"They are instruments, not
homework"* fails all three — nothing on the page claims they are homework — and goes.

The difference is not in the words but in what surrounds them. The same sentence with
no page around it fights a straw man.

**A fourth question, for a closing sentence with an image in it.** If a metaphor sits
where *Y* should be — *"then you don't have a culture, you have a dashboard"* — the
reader has to make two jumps: decode the image, then draw the conclusion. Even the
writer rereading their own sentence sometimes has to stop and think; a first-year does
not, and reads straight past. Replace the image with the mechanism it stood for:
*"…it sees every breach happen and prevents none of them."*

## What the script finds

| Code | Failure form | Precision |
|---|---|---|
| A1 | Antithesis: "not X, but Y", "X, not Y", "is not X — it is Y", "rather than", "without X there is no Y" | good — *rather than* is ordinary English, so weigh it |
| A2 | Strong word with no evidence: crucial, groundbreaking, robust, seamless, pivotal | good — sometimes fair inside a quotation |
| A3 | Warm-up: "in today's fast-paced world", "it is important to note that" | high |
| A4 | Container noun: landscape, ecosystem, playing field, the realm of | moderate — *ecosystem* is a domain term in biology, IT and regional innovation policy |
| A5 | Buzzword: dive into, unlock, seamless, empower, leverage, tap into | good — *unlock* is literal when something is actually locked |
| A6 | Detour around "is": serves as, acts as, forms the basis for, represents | moderate — *represents* is sometimes the right verb |
| A7 | Ending that decides nothing: "time will tell", "either way" | high |
| A8 | Future promise: "changes the way we work", "brings us closer to" | high |
| A9 | Politeness formula: "great question", "you're absolutely right" | high |
| A10 | Em-dash density above 1.2 per 100 words | good, but it is a norm and not an error |
| A11 | Metronome rhythm: every sentence the same length (spread under 0.38) | good from eight sentences on |
| A12 | Rule-of-three density: "X, Y and Z" above 1.5 per 100 words | moderate — three things are often simply three things |
| A16 | The same intensifier four times or more: actually, genuinely, quietly, honest, simply | good — repetition is the signal, not the word |
| A17 | Demonstrative echo: "That is what…", "That is the…" restating the sentence before | moderate — sometimes it is the plainest available sentence |
| D1 | Sentence above 25 words | high; the threshold hangs on the reader |
| D2 | Abstraction density: nouns in -tion, -ment, -ity, -ance, -ism | moderate |
| D3 | Unexplained jargon from a fixed list | good — a gloss in brackets, after a colon, or inside a proper name counts as explained |

Measured on this repository's five published pages: 540 findings, of which 304 are D1
on one long instructor document. Of the five vocabulary findings (A4, A5, A7) all five
survived review as deliberate: *regional ecosystem* is the name of a real thing, *unlock*
describes a gate that is literally locked, and *either way* fell mid-sentence rather
than at the end. On a cleanly written control text: no findings at all.

## What the script does not find

**An antithesis with no signal word.** *"Technology changes. Organising stays."* Same
form, no "but".

**A strong word that does have evidence.** A2 reports *crucial* even when a number sits
two lines below it. Reading is still required.

**Empty content in correct sentences.** A paragraph that says the same thing three
times in different words trips no code at all.

Three forms only a reader can see are in [`patterns.md`](patterns.md): elegant
variation (A13), false concreteness (A14) and the inflated list (A15).

## Language fitted to the reader

The D-codes adjust to who is reading. For students meeting a subject for the first
time, many of them in a second language:

- **D1 at 25 words.** For projected slide text, 20 — the reader gets one glance.
- **Every technical term is explained in the same sentence**, not in a footnote:
  *"poka-yoke — Japanese for: making mistakes impossible"*.
- **An abbreviation used once can go.** Used more often, it gets a full description at
  first mention.
- **A word in another language gets its gloss on the spot.** In English course material
  for a Dutch programme, *bedrijfskunde* or *stageplaats* needs its English equivalent
  in the same sentence, once.
- **Talk to the reader, not about them.** *"Three concepts students confuse"* becomes
  *"three concepts you will easily confuse"*.

Adjust the thresholds at the top of [`scripts/aiprose.py`](scripts/aiprose.py)
(`SENTENCE_MAX_WORDS`, `ABSTRACT_PER_100`, `DASHES_PER_100`) and extend `JARGON` with
the field's own terms.

## Common mistakes

| Mistake | Why it goes wrong |
|---|---|
| Smoothing the antithesis instead of deleting it | the construction survives the rewrite — this is the measured baseline |
| Deleting every antithesis | a negation that rejects a misconception present on the same page is information — see *When it stays* |
| Clearing every finding | A4, A6, A12 and A17 have moderate precision; a domain term does not have to go |
| Editing quotations | a line from a board member or a cited author keeps its own words |
| Only running the script | the three worst forms are in `patterns.md` and require reading |
| Cutting every long sentence | variety is the goal; all-short prose earns you A11 |
| Leaving the thresholds alone | 25 words is for a page; set them for your reader |
| Treating A10 as a defect | em dashes may be house style — decide once, write it down, then stop re-litigating it |
