# The patterns, with English examples

Reference alongside `SKILL.md`. Per code: what the form looks like, why it arises,
and what replaces it. The examples are from real course material.

This list quotes the mistakes it describes. Run `aiprose.py` over this file and it
reports those quotations. That is correct behaviour.

---

## A1 · The antithesis

**Form.** "Not X, but Y." "X, not Y." "It is not X — it is Y." "This isn't about X."
"Less X, more Y." "Without X there is no Y." "X rather than Y."

**Why it arises.** The construction promises an insight: something is taken away
first, then the reveal arrives. That rhythm feels like depth and costs no facts at
all. Models produce it at every opportunity.

**What is wrong with it.** Half the sentence is about what is not the case. For a
reader who does not yet know the subject, that is the half that sticks.

**Replacement.** See the recipe in SKILL.md. In short: delete the negated half; if
the sentence is then incomplete, give the misconception an owner and a sentence.

> You recognise a good team not by what it knows, but by how much has become impossible.

becomes

> You recognise a good team by how much has become impossible. Knowledge sits in
> people's heads; a blocked path sits in the software.

**The functional antithesis.** The same form is sometimes the right tool. The
difference is not in the sentence but in what surrounds it:

| | Hollow | Functional |
|---|---|---|
| The negated side | a straw man nobody defends | on the same page, or the reader just wrote it down |
| Deletion test | the sentence is just as good | the meaning changes |
| What it does | builds tension | rejects a misconception that is present |

*"This is a design question about an organisation, not about software"* is hollow on
an empty slide, and functional on a slide where the room's three technical answers sit
next to it in boxes. There the negation rejects them one by one.

Rule of thumb: **a negation may stay if you can point at who thought the negated thing.**

**English-specific note.** *"rather than"* is the quietest member of this family and
the easiest to overuse, because it reads as ordinary prose. It is the same
construction: *"it measures a person rather than a company"* spends half its words on
the company. Where the contrast is not the point, use the plain sentence — *"it
measures a person"*.

---

## A2 · The strong word without evidence

**Form.** crucial, essential, fundamental, groundbreaking, revolutionary, powerful,
invaluable, vital, pivotal, robust, seamless, cutting-edge, transformative, game-changer.

**What is wrong with it.** The word tells the reader how important something is
instead of why. Delete it and the meaning does not change — that is the test.

**Replacement.** The mechanism, a number, or a consequence.
*"A crucial step"* → *"Without this step the rest waits two weeks."*

---

## A3 · The warm-up

**Form.** "In today's fast-paced world…", "In the current era…", "It is important to
note that…", "Let's take a look at…", "In this chapter we will examine…", "What makes
this so special is…", "Before we go further, it is worth…".

**What is wrong with it.** The sentence is a run-up. It announces that something is
coming instead of saying it.

**Replacement.** Delete. The next sentence was your opening.

---

## A4 · The container noun

**Form.** the landscape, the ecosystem, the playing field, the world of, the realm of,
the domain of, in the space of, in the context of.

**What is wrong with it.** The word replaces the party that acts with an area in which
it happens. Whoever is doing something disappears.

**Replacement.** Name the organisation, the people or the place.
*"The healthcare landscape is changing"* → *"Hospitals get less money per patient."*

**Watch out.** In biology, IT and regional innovation policy, *ecosystem* is a term of
art. Then it stays.

---

## A5 · The buzzword

**Form.** dive into, delve into, unlock, seamless, effortless, empower, leverage,
navigate the, harness the, tap into, reap the benefits, at its core.

**Replacement.** An ordinary verb. *"We dive into the figures"* → *"We look at the
figures."* *"Unlock value"* → *"save four hours a week."*

**Watch out.** *unlock* is literal when something is actually locked — a gate, a level,
a door.

---

## A6 · The detour around "is"

**Form.** serves as, acts as, functions as, forms the basis for, stands for,
represents, constitutes, marks a, plays a key role in.

**Why it arises.** Models avoid repeating the verb *to be*, including where repetition
would not have bothered anyone.

**Replacement.** *is*, *is called*, or the verb that names the action.
*"The budget forms the basis for the plan"* → *"The plan starts from the budget."*

**Watch out.** *"Four characteristics constitute an organisation"* is ordinary English.
Moderate precision: read before you cut.

---

## A7 · The ending that decides nothing

**Form.** "Time will tell." "It remains to be seen." "There is room for improvement."
"One thing is certain." "Either way."

**What is wrong with it.** After a text with a direction, the writer ends without
making a choice. The reader does not know what to do.

**Replacement.** A choice, a limit or a next step. *"Time will tell"* → *"In March we
find out whether the wait stays under two weeks."*

---

## A8 · The future promise

**Form.** "revolutionises", "changes the way we work", "brings us closer to", "the
future of X is Y", "will never be the same", "is set to transform".

**Replacement.** Name the condition and the measuring point. *"AI changes the way we
work"* → *"If the permit comes through, one person will do the work of three."*

---

## A9 · The politeness formula

**Form.** "Great question!", "You're absolutely right", "Absolutely!", "Good catch".

**Replacement.** Delete. In interview transcripts and chat logs it may stay as a quotation.

---

## A10 · The em dash

**Form.** More than roughly one dash per hundred words.

**What is wrong with it.** The dash suggests an aside with weight. At high density
every sentence acquires a subordinate clause claiming that weight, and the text reads
breathless.

**Replacement.** A full stop, a comma or a colon. Keep the dash for the one or two
places where the interruption genuinely counts.

**Watch out.** Em dashes are house style in some projects, this repository included.
A10 will then fire on every page. Decide once whether the norm applies, write the
decision down, and stop re-opening it — but do read the finding, because house style
is a licence for the dash, not for the breathless clause it usually carries.

---

## A11 · The metronome rhythm

**Form.** Eight or more sentences of nearly identical length.

**What is wrong with it.** Human prose varies: a three-word sentence next to a
thirty-word one. Evenness reads as generated, even with no suspect word in sight.

**Replacement.** Cut one sentence down to two words. Join two others. It is the spread
that matters, not the average.

---

## A12 · The rule of three

**Form.** "speed, efficiency and innovation" — three items where two would do, or where
the third was added to round out the rhythm.

**Test.** Delete the third item. Do you miss information? Then it stays.

---

## A16 · The repeated intensifier

**Form.** actually, genuinely, truly, really, quietly, honest, simply, literally,
notably — the same one, over and over.

**Why it arises.** The word is doing the work the sentence should do. It signals that
the writer means it, instead of giving the reader a reason to believe it.

**What is wrong with it.** One is invisible. Seven in a page is a verbal tic, and it is
what a reader with an ear notices first. Measured on this repository's landing page:
*actually* seven times, *honest* six, *quietly* four, in 4,060 words.

**Replacement.** Cut it, or put in the fact that made you reach for it.
*"what a manufacturer actually needs"* → *"what a manufacturer asked for"*.
*"where it quietly fails"* → *"where it fails without saying so"*.

---

## A17 · The demonstrative echo

**Form.** A closing sentence that begins *"That is what…"*, *"That is the…"*, *"That is
why…"* and restates the sentence before it in slightly grander terms.

**What is wrong with it.** It reads as a conclusion but adds nothing. The reader has
just been told; the echo asks them to be impressed by it.

**Replacement.** Delete it, or make it carry new information. *"…the quality bar each
chapter is measured against. That is what a finished page has to look like."* → *"…the
quality bar each chapter is measured against."*

**Watch out.** Sometimes it is the plainest sentence available and the pointing is
genuinely needed. Moderate precision.

---

## D1 to D3 · The reader

**D1 · Sentence length.** Above twenty-five words a reader working in a second language
loses the thread. For projected text, twenty: the reader gets one glance.

**D2 · Abstraction density.** Nouns of action (implementation, effectiveness,
coordination) stack up in administrative prose. Each is a verb in hiding: *"after the
implementation of the system"* → *"once the system runs"*.

**D3 · Jargon.** The question is not whether the word is allowed, but whether it was
explained before it was needed. Rule of thumb: a term used once can go; a term used
more often gets a description in the same sentence at first mention.

---

# The three forms no rule finds

## A13 · Elegant variation

The same concept gets a different name in every sentence: *the team* → *the unit* →
*the group* → *the crew*. Intended as variety, read as four subjects. A reader still
learning the subject goes looking for the difference.

**Recognising it.** Count how often the core term appears literally. Four sentences,
four different words: this is the fault.

**Fixing it.** Pick one term and hold it. In teaching material, repetition is a virtue.

## A14 · False concreteness

An example shaped like an example that adds nothing: *"Think of an organisation that
wants to improve its processes."* That is the definition in other words, not a case.

**Recognising it.** Can you put the example on a map, in a year or in an amount of
money? No → false.

**Fixing it.** One real case, with a name and a number, or delete it.

## A15 · The inflated list

Four bullets that together hold one thought, each starting with a verb in the same
form. The list suggests four steps; the reader finds one.

**Recognising it.** Can you merge two bullets with no loss? Then the list was form and
not content.

**Fixing it.** Running prose, or a list that really does hold separate items.
