# What a word list catches, and what it walks past

Measurement of 6 September 2026 on the five published pages of this repository —
`site/index.html`, `site/week-01.html`, `site/handbook.html`,
`site/integrated-lrd.html` and `site/tool-ai-worker-maturity.html`. 24,034 words of
hand-written English prose.

This file quotes the word list and the constructions it describes, so running
`aiprose.py` over it reports them. That is correct behaviour.

## The instrument that fails

A scan for the forty-two words that every "how to spot AI writing" list contains:
*delve, leverage, robust, seamless, unlock, harness the power, fast-paced, tapestry,
testament to, pivotal, cutting-edge, game-changer, elevate, empower, dive in, unpack,
realm, foster, underscore, moreover, furthermore, it's worth noting, in conclusion,
navigate the, landscape of, embark, holistic, synergy, paradigm, myriad, plethora,
vibrant, crucial, comprehensive, meticulous, profound, transformative, revolutionize,
at the end of the day, when it comes to, in the realm of, groundbreaking, unprecedented.*

**Four hits in 24,034 words. All four in one document, and all four defensible:**

| Hit | Why it survives |
|---|---|
| "the review itself is naturally **holistic** rather than split by lens" | the word means what it says; the sentence is about not splitting by lens |
| "a single binary next week **unlocked** signal" | a gate that is literally locked |
| "teams game the Socratic agent with shallow answers to **unlock** faster" | the same literal gate |
| "Synthesis of Motivation and Flow in Educational **Paradigms**" | the title of a cited source |

Four pages score zero. On that instrument the site is clean.

## What was actually in the text

Run `aiprose.py` over the same 24,034 words:

| Code | Findings |
|---|---|
| A1 antithesis | **173** |
| D1 sentence over 25 words | 304 |
| D3 unexplained jargon | 39 |
| A17 demonstrative echo | 8 |
| A10 em-dash density | 5 pages, all above the norm |
| A16 repeated intensifier | 5 |
| A4, A5, A7 vocabulary | 5, all five deliberate on review |

The landing page alone carries 26 instances of A1 in 4,060 words — roughly one
sentence in eight. Three consecutive paragraphs end on it:

> The scarce skill is **not** producing text with a model — **it is** verification.
> It is **not** a report that ends in a folder — **it is** a chapter of a handbook…
> The platform is your tool, **not** the handbook's precondition.

And the intensifiers, on that one page: *actually* seven times, *honest* six,
*quietly* four.

## The conclusion the skill rests on

**The vocabulary was never the tell.** A writer who has been told to avoid *delve* and
*leverage* will avoid them, and go on producing the construction — because the
construction does not feel like a word choice, it feels like a thought. It survives
every edit pass aimed at word choice, including an edit pass by another model.

That is why `SKILL.md` carries a three-step recipe and a before-and-after table rather
than a list of banned words, and why the *When it stays* test is part of it: the goal
is not zero antitheses. On this same site, *"you get questions back, never a verdict
and never a score"* is one of the 173 and should stay — the distinction between a
question and a verdict is the design being described. It is the other hundred-odd,
where the negated half fights nobody, that make a page read as generated.
