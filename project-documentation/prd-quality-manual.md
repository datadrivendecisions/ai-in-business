# PRD quality manual — where the criteria come from

*The reading behind the AEL week-1 hand-in ([`assignment-ael-prd.md`](assignment-ael-prd.md)):
what Marily Nika, **Building AI-Powered Products** (O'Reilly, 2025) says about PRDs, and how
that was folded into the criteria a team's document is read against. Page numbers are those of
the print edition's index.*

**This document was split on 11 September 2026.** It carried three parts, and they had three
different audiences:

| Part | Now lives | Why there |
|---|---|---|
| 1 — What the book says | here | Course-design rationale. Internal, and it quotes the book at length. |
| 2 — The criteria | [`site/prd-criteria.html`](../site/prd-criteria.html) | Published for students. A team is entitled to know the bar its deliverable is read against, and `index.html` promises criteria are published before they judge anything. |
| 3 — Scoresheet, bands, agent prompt | `ai-in-business-intake/rubric/prd-scoresheet.md`, outside the repo | Its worth depends on a student not having read it. This repository is public, so "instructor-only" is not a property it can have. |

Where the book and the course brief pull in different directions, the brief wins, and the
reason is given. The one that matters most: Nika's template is written for a 0-to-1 commercial
AI product with a market; the team's PRD is for an internal research platform whose user is the
team itself ([ADR-0010](../work/decisions/0010-ael-arc.md)). Market analysis, positioning and
rollout are trimmed accordingly.

---

## Part 1 — What the book says about PRDs

The book never treats the PRD as a chapter of its own. It appears at four points of the AI
Product Development Lifecycle (AIPDL) and once in full, as a template in the appendix. Taken
together, the four appearances say what the document is *for*, and the template says what is
*in* it.

### 1.1 The PRD starts at ideation, before the brainstorm (ch. 2, "Step 3: Brainstorm with your team", p. 32)

The ideation phase is "the perfect time to kick off a product requirements document (PRD),
where you'll begin framing the problem and jotting down potential AI-powered feature ideas."
The order is deliberate: outline the initial concepts in the PRD *first*, then brainstorm with
the team to turn "vague ideas into feasible AI solutions". The document is the surface the
brainstorm works on, not the write-up afterwards.

Three things the book wants in that early PRD:

- **The problem, framed.** Every idea starts from a problem, "but is it the right one to
  leverage AI? You must validate whether users are bothered enough by that problem before
  jumping into solutions."
- **Feasibility talked through**, specifically "the data needed for model training or the
  potential impact of AI on user experience", because these conversations are "crucial to
  setting realistic goals".
- **The people.** Select four or five core members with diverse skills "and tag them in the
  PRD". The PRD is where the team is named.

Two *don'ts* from the same section are the sharpest quality tests in the book:

> Don't fall into the "shiny AI object" trap. Don't launch products just because the
> technology behind them is "cool." … make sure your product road map aligns with your
> business objectives.

> Don't talk about a "hunch." … Back your "hunches" with data: Have others done something
> similar? If so, what was the return on investment?

Step 4 adds the prioritisation instrument the template later assumes: **RICE** — reach,
impact, confidence, effort — with the note that "confidence is crucial in AI product
development because sometimes the data or algorithm feasibility may not be entirely clear at
the ideation phase", and an optional fifth factor, *AI investment*, for the cost of training or
integrating a model.

### 1.2 By project scoping, the PRD is finished and hands over to engineering (ch. 3, "Project Scoping", p. 78)

"By this point, you should have a finalized PRD … that defines the **objectives, user needs,
success metrics, and constraints** of your AI product." Scoping is then "the engineering team
translating the product requirements into technical boundaries", driven by three questions:
"What problems are you trying to solve? What outcomes are you aiming for? What data sources
will be involved?"

The worked example is a recommendation system: the PRD "would detail the types of data needed,
the integration points with the existing platform, and the key performance indicators (KPIs)
to measure success." And the one rule of scoping the book states outright: "It's a good
practice to explicitly call out what is **out of scope**, which will help you set the right
expectations."

The same chapter fixes the quality bar the PRD has to name. The lifecycle iterates "until the
project reaches a fair **minimum viable quality (MVQ)**, … the threshold at which the product
provides sufficient value to address users' needs effectively and can be released." Setting it
"is a critical decision, and there's no single 'right' or 'wrong' threshold. As the PM, you
determine this based on … user expectations, business goals, risk tolerance, and the specific
use case."

### 1.3 The PRD is the pre-read for a product review, and grows after it (ch. 5, "Product Reviews", p. 133)

The product-review checklist names the PRD twice. Before the review: "Have you shared the PRD
or slide deck with all attendees beforehand so that participants come prepared and informed?" After it: "Do
you have a plan to monitor progress on the agreed-upon actions (e.g., holding a follow-up
review, **adding specific sections to the PRD**, or gathering more data)?"

During the review the presenter must have "laid out the trade-offs, highlighting the risks,
costs, benefits, and potential impact of different decisions" — which is only possible if the
PRD carries them. The PRD is a living document that a review adds to; it is not frozen at
scoping.

### 1.4 Scoping an AI MVP is the hard part (ch. 4, interview with Mark Cramer, p. 115)

Mark Cramer's "biggest learning might be how difficult it is to scope an MVP for an AI
product … you cannot 'know,' a priori, how your application will perform. Its behavior will
depend on many factors, including the volume and quality of the training data." The advice:
"take great care when defining any MVP that's based on an ML model." A PRD that promises a
performance level it has no way to know yet has ignored this.

### 1.5 The template (Appendix, "AI Product Requirements Document Template", pp. 184–188)

The framing instruction: "clearly define the problem space, outline user needs, and demonstrate
how AI will uniquely solve these challenges." The header carries the product name, **author,
contributors** and **relevant documents**, and one question the whole document must answer:
*"How can we use AI to help our users?"* Then nine sections:

| # | Section | What it asks for |
|---|---|---|
| 1 | **About** | The high-level problem space; "the tl;dr of what you are trying to achieve". |
| 2 | **Market Insights** | Customer segments ("if you don't know, which users will you target as per the hypotheses"), a user persona ("a one-size-fits-all persona that you will be solving for"), market, competitor and technology analysis. |
| 3 | **The Problem** | *Use cases* — what users are trying to achieve, listed. *Pain points* — why they cannot, or what is wrong with how they do. A *problem statement* in the form "<Athletic John spends too much time trying to figure out the right fitness and nutrition routine … and he never achieves his performance goals>", with a note on **why AI is uniquely positioned** to solve it. *Hypotheses and mission*: "By bringing x to life, you will be making z easier/more efficient … for the user." |
| 4 | **The Solution** | *Ideation* (all candidate features). *Leveraging AI* — "why is AI appropriate or essential". *Feature prioritisation* by RICE. The *AI MVP* — "Will you be training a model? Will this be a hybrid solution?" at a high level. A *road map*. A *technical architecture* "on a very high level (client, server, where does data flow from/to?) — the software engineers/scientists will then create a design doc." *Assumptions and constraints*. *Risks* "along with strategies for mitigating those risks". |
| 5 | **Requirements** | *User journeys*. *Functional requirements* — "Don't talk about what kinds of algorithms the scientists will use; instead, talk about **why you need algorithms and what smart functionalities they will support**." *Non-functional* — security, scalability, performance, usability. *AI and data requirements* — data sources, types, collection and management. |
| 6 | **Challenges** | "Will you have enough data? How do you plan to acquire it? Do you have enough funds? Do you have enough user conviction that what you are bringing to life will indeed solve your users' problems?" |
| 7 | **Positioning** | A one-table snapshot: use case, pain point, possible solutions, impact. |
| 8 | **Measuring Success** | Generic product metrics (engagement, retention) *and* AI-specific ones: "What does quality mean to you? … **What quality is good enough to launch?** … What is your North Star metric?" |
| 9 | **Launching** | Stakeholders and communication; rollout strategy. |

Chapter 6 supplies what section 8 assumes: no single metric captures an AI product, so success
is a *blend* of **product health** (engagement, retention, satisfaction), **system health**
(uptime, latency, error rate) and **AI proxy** metrics (accuracy, precision, recall — the
model's integrity, as a stand-in for the product goal). The OKR framework there asks for one
North Star, at least one metric from each bucket, and a **guardrail metric** for "potential
adverse side effects or risks you want to monitor and minimize".

### 1.6 In one paragraph

A PRD, in this book, is opened at ideation to frame a problem worth solving with AI and to name
the people who will think about it; is finished at scoping, when it states objectives, user
needs, success metrics and constraints clearly enough for engineers to draw technical
boundaries from it, and says what is out; is the pre-read for every review; and gains sections
as decisions are taken. Its two recurring quality tests are *why AI, specifically* and *evidence
rather than a hunch*; its hardest section is the honest statement of what quality is good enough
to ship, because for an AI product that cannot be known in advance.

---

---

## Where the rest went

The twenty criteria this reading produced — A1–A5, B1–B4, C1–C3, D1–D2, E1–E2, F1–F2, G1–G2 —
are published at [`site/prd-criteria.html`](../site/prd-criteria.html), linked from the week 1
page beside the assignment itself.

The scale, the three invariants, the sheet, the bands and the prompt the assessing agent is
given are in `ai-in-business-intake/rubric/prd-scoresheet.md`, outside this repository. The
agent reads them at runtime, next to the normalised hand-ins.
