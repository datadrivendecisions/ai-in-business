# PRD — the bias experiment tool (first draft)

|                    |                                                                                                                                                                  |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Document** | Product requirements — the tool that runs the week 3 in-class experiment                                                                                        |
| **Version**  | 0.1, 14 September 2026                                                                                                                                           |
| **Owner**    | The two module owners; the AIBS owner runs the session                                                                                                           |
| **Serves**   | The experiment protocol in[`work/drafts/week-03-information-seeking-experiment.md`](../../../work/drafts/week-03-information-seeking-experiment.md)             |
| **Rests on** | [ADR-0011](../../../work/decisions/0011-continuous-assessment.md) (gates are informational and unscored) and the tool rules in [`CLAUDE.md`](../../../CLAUDE.md) |
| **Status**   | Nothing built. This is the first statement of what it has to do.                                                                                                 |

---

## 1. Problem and users

Week 3 runs an experiment on the students themselves: does an AI devil's advocate reduce **biased
information seeking** — the habit of reading the things that agree with you? The design is
within-person and counterbalanced, so every student does the task twice, once with the agent and
once without.

Run on paper, the session collapses. Someone has to shuffle sixteen cards differently for each of
thirty-two students, enforce a budget of eight, time each choice, collect two rounds of answers,
and get thirty-two results into one place before the room loses interest. None of that is
interesting work and all of it is error-prone.

**Three users, and they want different things.**

- **The student** wants to get through it without being confused about what they are allowed to do,
  and to leave understanding what happened to them.
- **The lecturer** wants thirty-two results in one place, a paired comparison on screen, and no
  laptop admin during a 240-minute block.
- **The module owners** want data that survives being questioned: randomisation recorded, a fixed
  codebook, nothing invented after the fact.

A fourth party matters and is not a user: **the student as participant**. They consent, they may
withdraw, and nothing they type may leave their own browser.

---

## 2. What it must let a user do

Five screens for the student, one for the lecturer. Drawn below as they would appear.

### 2.1 Before anything — consent, and what happens to your typing

Consent comes before the first question, not buried in a footer. The honest selling point is that
the tool has nowhere to send anything.

```
┌────────────────────────────────────────────────────────────────┐
│  AI in Business · Week 3                                       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  You are about to take part in a small experiment about how    │
│  people choose what to read.                                   │
│                                                                │
│  · It takes about 50 minutes, in two rounds.                   │
│  · Nothing you type leaves this browser. There is no server.   │
│  · Nothing here is marked, and it cannot affect your grade.    │
│  · At the end you get one line of text. Handing it in is how   │
│    you take part. If you would rather not, close the tab and   │
│    nothing is recorded anywhere.                               │
│  · We will tell you at the end what we were actually testing.  │
│                                                                │
│  Pick a code only you know (not your name):  [ ______ ]        │
│  Team:  [ 1 ▾ ]                                                │
│                                                                │
│                        [ I understand — begin ]                │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 Your position, before you read anything

The claim, and one sentence committing to a side. This is the anchor everything is measured
against, so it is written before a single source is seen.

```
┌────────────────────────────────────────────────────────────────┐
│  Round 1 of 2 · Step 1 of 5                                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  THE CLAIM                                                     │
│  "A manufacturing SME of 50 staff should put an AI assistant   │
│   in front of its customers before it puts one behind its own  │
│   processes."                                                  │
│                                                                │
│  Where do you stand, right now, before reading anything?       │
│                                                                │
│     ( ) I agree      ( ) I disagree                            │
│                                                                │
│  In one sentence, why?                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│                                        [ Lock it in ]          │
└────────────────────────────────────────────────────────────────┘
```

### 2.3 The source menu — the screen that is the experiment

Sixteen cards, one at a time, in an order shuffled for this student alone. Eight opens. No going
back. The position stays on screen, because the measurement is about *this* position.

```
┌────────────────────────────────────────────────────────────────┐
│  Round 1 of 2 · Step 2 of 5                   opened  3 of 8   │
├────────────────────────────────────────────────────────────────┤
│  You said: "Customer-facing first — that is where the money    │
│  is." (agree)                                                  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Card 7 of 16                                                  │
│                                                                │
│    Journal of Business Research · 2021                         │
│    Too small to do it all? A meta-analysis of exploration,     │
│    exploitation and ambidexterity across 5,488 SMEs            │
│                                                                │
│                                                                │
│         [  Open this one  ]        [  Skip  ]                  │
│                                                                │
│    Opening costs one of your eight. A card you skip does not   │
│    come back.                                                  │
└────────────────────────────────────────────────────────────────┘
```

Opening it spends one of the eight and reveals an extract plus the link to the real document:

```
┌────────────────────────────────────────────────────────────────┐
│  Card 7 of 16 — opened                        opened  4 of 8   │
├────────────────────────────────────────────────────────────────┤
│    Journal of Business Research · 2021                         │
│    Too small to do it all? ...                                 │
│                                                                │
│    "Meta-analytical evidence from 5,488 SMEs across 34         │
│     studies suggests that ambidexterity has a less positive    │
│     relationship with SME performance than both exploration    │
│     and exploitation."                                         │
│                                                                │
│    Read the original ↗                                         │
│                                                                │
│                                        [ Next card ]           │
└────────────────────────────────────────────────────────────────┘
```

### 2.4 The agent — in one round only

The tool cannot call a model, so it hands over the prompt and takes back what the student's own
assistant said. That seam is deliberate: the student sees the questions arrive, which is the point.

```
┌────────────────────────────────────────────────────────────────┐
│  Round 2 of 2 · Step 3 of 5                                    │
├────────────────────────────────────────────────────────────────┤
│  Before you settle on an answer, one more voice.               │
│                                                                │
│  1 · Copy this into your own AI assistant.                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Here is a position I hold: "..."                         │  │
│  │ Here are the four sources I read: ...                    │  │
│  │ Ask me three questions about this position and these     │  │
│  │ sources. Quote my own words back at me. Do not tell me   │  │
│  │ whether I am right, and do not suggest what to do.       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                            [ Copy prompt ]     │
│                                                                │
│  2 · Paste what it asked you.                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│                                        [ Continue ]            │
└────────────────────────────────────────────────────────────────┘
```

### 2.5 The end — one line, handed over by choice

```
┌────────────────────────────────────────────────────────────────┐
│  Done. Nothing you typed has left this browser.                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Your result line:                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ v1|kite|t3|r1:none:c1:op8:cong6:sopp1:s142                │ │
│  │ |r2:ask:c2:op8:cong4:sopp3:s188|moved:yes|tlx:41          │ │
│  └──────────────────────────────────────────────────────────┘  │
│                                     [ Copy my line ]           │
│                                                                │
│  Hand this line in and you are in the dataset. Prefer not to?  │
│  Close the tab — there is no copy anywhere else.               │
└────────────────────────────────────────────────────────────────┘
```

### 2.6 The lecturer's screen

Same page, a different door. Thirty-two lines in, the paired comparison out — **and a question
rather than a verdict**, because the conclusion is the thing the students came to write.

```
┌────────────────────────────────────────────────────────────────┐
│  Lecturer view          32 lines pasted · 32 read · 0 rejected │
├────────────────────────────────────────────────────────────────┤
│  Congeniality index — higher means more one-sided reading      │
│                                                                │
│    no agent   ████████████████████░░░░░░  0.52                 │
│    with agent ███████████████░░░░░░░░░░░  0.38                 │
│                                                                │
│    paired difference          −0.14                            │
│    95% interval        −0.31  to  +0.03                        │
│    n = 32 students in 8 teams                                  │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  The interval crosses zero.                              │  │
│  │  What would you have to believe to call this an effect?  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │                                                    │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  Smallest effect 32 paired observations could have detected    │
│  at 80% power:  d ≈ 0.51                       [ show working ]│
└────────────────────────────────────────────────────────────────┘
```

---

## 3. Output qualities — what good data looks like

**Invariants. Every student, every round, pass/fail.**

- The card order shown is recorded, not just the choices. Without it, position effects and stance
  effects cannot be told apart.
- The position sentence is locked before the first card appears, and cannot be edited afterwards.
- Exactly eight opens, or fewer if the student runs out of cards; never nine.
- The result line identifies a self-chosen code and a team, and contains no name.
- The four counts in a line reconcile: opened = congenial + uncongenial.

**Qualities. Judged on the class as a whole.**

- **Comparability.** Every student met the same sixteen cards. Any difference between them is about
  them, not about what they were handed.
- **Reconstructability.** From the thirty-two lines alone, a second person can recompute every
  number the lecturer screen displayed.
- **Legibility under doubt.** A student who asks "how do you know I was biased?" can be shown their
  own line and the codebook, and follow the arithmetic.

---

## 4. Known constraints

- **No network calls.** The tool rules in `CLAUDE.md` allow JavaScript on a `tool-*.html` page only
  if it is self-contained: no build step, no framework, no requests. That rules out hosting the
  model, and it rules out a server collecting results.
- **`localStorage` is per-browser.** Thirty-two laptops means thirty-two islands. Aggregation is a
  deliberate manual step — copy a line, paste thirty-two — not an oversight.
- **The site is public.** Anything in `site/` can be read by anyone, students included. The sixteen
  cards and the codebook are in the page source. The stance and quality labels therefore **cannot**
  be in the published page, or the experiment is readable before it is run.
- **One 240-minute block**, shared with the rest of week 3. The tool gets perhaps 150 minutes.
- **Light only, brand system, sticky nav and footer**, copied from `index.html` like every other
  tool.
- **`--text-muted` on `--bg-cream` is 4.26:1** and fails AA. Not that pair, anywhere.

---

## 5. Out of scope (for now)

- **Calling a model.** The agent runs in the student's own assistant, from a prompt the tool
  supplies.
- **Writing the conclusion.** The tool displays numbers and asks about them. Stating a finding
  would deploy, inside the measuring instrument, the verdict-giving behaviour the experiment is
  testing — and would take from students the one thing the session exists to give them.
- **Scoring anyone.** ADR-0011 keeps the week's gates informational and unscored; this is not a
  back door.
- **Cross-device or cross-session sync.** A student who closes the tab has withdrawn.
- **A general-purpose survey builder.** Two claims, sixteen cards each, hard-coded.
- **Keeping the data.** Nothing persists past the session by design.

---

## 6. Open questions and assumptions

- **Where do the stance and quality labels live?** They cannot sit in the published page. Either the
  lecturer view holds the codebook and is pasted in at analysis time, or the labels are kept out of
  `site/` entirely and applied to the lines afterwards in a spreadsheet. *Owner: the module owners,
  before the menu is built.*
- **What happens if a student skips more than eight cards?** They reach the end with a budget
  unspent. Assumed acceptable: the index is a proportion of what was opened. Worth confirming that
  a student with three opens is not silently compared with one who opened eight.
- **Two claims are needed and neither is chosen.** Both must be arguable either way with real
  literature on both sides. *Owner: the AIBS owner.*
- **Is the extract enough, or must they open the original?** Assumed the extract is enough for the
  clock; the link is there for anyone who wants it. If reading the original matters, the session
  does not fit.
