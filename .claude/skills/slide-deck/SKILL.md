---
name: slide-deck
description: Use when writing or editing session slides — the site/week-NN-slides.html decks, or any deck a lecturer will present — and whenever a slide is asked to carry more than a listener can take in at one glance. Triggers include "make the slides", "add a slide", "this slide is too full", "make it briefer", "show, don't tell", or a card whose text a student would read instead of listening.
---

# Slides support the story; the speaker tells it

## The core rule

**A student reads or listens. Never both.** A slide full of sentences is read, and while it is
read the lecturer is not heard. So a slide carries only what the voice cannot carry: the one
sentence to remember, a number, a quote, a name, a structure, a link. Everything that can be
said is said, and stays off the slide. The full text lives on the week page, which is where a
student goes afterwards.

This is the assertion–evidence structure: the headline is the assertion, the body is the
evidence for it, and the argument belongs to the speaker.

## What a card carries

| Element | Rule |
|---|---|
| Headline | One sentence a student could repeat afterwards; twelve words at most. A topic label (*Your PRDs*) marks a section; a content slide states its point. |
| Body | At most 40 words. Fragments, not sentences. Three bullets at most, one line each. |
| A sentence, if there must be one | At most 20 words — D1 for projected text, because the reader gets one glance. |
| Evidence | One thing: a number, a quote, a name, a link, a diagram, a row of names. Never a paragraph that explains it. |
| Detail | Off the card, on the week page or the criteria page, and linked from the card. A link is something the voice cannot carry; use it. |
| Unknowns | `.tpl` for anything set on the day. An empty slot is honest; a filled one that asserts is not. |

## Two tests

**The ghost-deck test.** Read the headlines alone, top to bottom. If they tell the session's
story, the deck holds. A headline that is only a label means the slide does not know what it is
for.

**The listening test.** For each card, say aloud what you will say over it. Anything on the card
you just said aloud is a duplicate: delete it from the card. Anything on the card you would never
say aloud — the exact wording of a template, a figure, a link — is why the card exists.

## Method

1. **Write the talk track first.** One line per slide: what the speaker says.
2. **For each line, decide what the listener must see** to follow it. That is the card.
3. **Run the counter.** It reports words, bullets and the longest sentence per card and flags
   what is over the line; exit 1 means something is.

   ```bash
   python3 .claude/skills/slide-deck/scripts/slidewords.py site/week-02-slides.html
   python3 .claude/skills/slide-deck/scripts/slidewords.py deck.html --max-words 40 --max-bullets 3 --max-sentence 20
   ```

4. **Run the prose check** the way the skill documents it for decks, so that separate cards
   are not read as one long sentence:

   ```bash
   python3 .claude/skills/strip-ai-language/scripts/aiprose.py site/week-02-slides.html --block-tag li --codes A1,D1
   ```

5. **Render it and look.** A headless-browser screenshot of the page, read as an image. A card
   that reads as a wall of text is obvious on the screen and invisible in the source.
6. **Move what you cut, do not lose it.** If a cut sentence carries a fact the site does not
   hold elsewhere, it goes to the week page and the card links there.

## This repository's decks

`site/week-NN-slides.html` is one card per slide, in the brand system, "same content as on the
screen, readable on a phone". The card *is* the projected slide, so the rule applies to the card.

- A slide is a `.slide` section with a `.slide-head` (kicker and `N / M`), an `h2`, then the body.
  `.cols` gives two columns, `.roles` a row of names, `is-title` a section marker.
- Adding a slide means renumbering every `N / M` after it and adding it to the `deck-nav` list.
- No speaker notes on the page. Notes live in `project-documentation/slides/week-NN-notes.md`,
  one `## sN` block per card, and the lecturer's *ask, never comment* prompts stay out of even
  that file under the instructor-material rule.
- The week page carries the assignment in full; the card carries its name and a link.

## The presenter build

The card page is what students read; the lecturer presents from a build of it. One command
turns the cards plus the notes file into `site/week-NN-deck.html` (arrow keys, **F** full
screen, **P** print; `?instructor` reveals the notes and the **N** key), a PDF with the notes
under every slide, and a PPTX with the notes in the notes pane:

```bash
.venv/bin/python project-documentation/slides/build_deck.py 2
```

The build reads the cards, so the rule above is enforced by construction: what is on the card
is what is projected, and nothing else. When a cut sentence is something the lecturer should
still say, it goes into the notes file, not back onto the card. Rebuild after every edit to a
card page or a notes file; the outputs are never edited by hand.
[`project-documentation/slides/README.md`](../../../project-documentation/slides/README.md)
has the file list.

## Worked example — slide 5 of week 2

Before, 162 words on one card. A three-sentence opening paragraph; three bullets, each a
paragraph; a closing paragraph with two more findings. A student reading it has stopped listening
by the second bullet.

After, 40 words. The same three findings, each reduced to the phrase the lecturer will use, plus
the one thing the voice cannot carry: the exact wording of a hypothesis. The count of drafts and
the link to the criteria stay because they are evidence. The header and the page limit went to the
lecturer's mouth; both are already on the criteria page.

```html
<h2>Your PRDs — three things almost every draft missed</h2>
<p>Eight drafts, <a href="prd-criteria.html">twenty criteria</a>.</p>
<ul>
  <li><strong>How you will know it works.</strong> Measures, with a cadence.</li>
  <li><strong>A hypothesis you could be wrong about.</strong> <em>By bringing X to life, Y gets easier — seen in Z.</em></li>
  <li><strong>Pain points with evidence.</strong> Failure log. Problem analysis.</li>
</ul>
```

## Where this comes from, and where it differs

- **Michael Alley's assertion–evidence structure** (Penn State): a sentence headline that states
  the slide's message, supported by visual evidence; bulleted lists have no place in it. We keep
  bullets, three at most and fragments only, because our cards are also read on a phone afterwards.
- **Anthropic's `pptx` skill**: every slide needs a visual element, "text-only slides are
  forgettable", and speaker notes go in notes, never in a text box. Our decks have no image
  pipeline, so the evidence is text-shaped — a number, a quote, a name, a link — and there are no
  notes at all, because the page is public.
- **The `academic-pptx` skill** (Gabberflast): action titles as complete sentences, about 40 words
  of body per content slide, one insight per slide, and the ghost-deck test — "the presenter
  carries the argument; the slide carries the evidence." The 40-word line and the ghost-deck test
  are taken as they are.
- **The house `strip-ai-language` skill**: D1 at 20 words for projected text, and the
  `--block-tag` flag so a deck is measured card by card.
