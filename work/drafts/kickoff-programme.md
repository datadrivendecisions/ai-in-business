# The owner's Monday — first joint session of AIBS and AEL

*Programme for the first 120-minute contact block. Draft; not for students. "AIBS" is the
research lecturer, "AEL" the technical lecturer. Square brackets are filled in before Monday.
Scored against [kickoff-scorecard.md](kickoff-scorecard.md): 52 / 54 after four cycles.*

Written against the [integrated LRD](../../site/integrated-lrd.html) — Part 2, Part 8 week 1,
§6.3, §6.7 — and [ADR-0009](../decisions/0009-build-environment.md) and
[ADR-0010](../decisions/0010-ael-arc.md), both still Proposed.

## The idea

An SME owner walks in with a problem and walks out, two hours later, with five things to do on
Monday morning — written by the students, questioned by the owner, and never scored. In
between, students form a crew, find out how far the AI intern can be trusted, interview her,
brief the intern to write the chapter, audit the partner team's chapter, and rewrite their
advice. Everything that is not that — names, attendance, tool policy — is on the back of one
sheet.

The session is one Challenge Based Learning arc: **Engage** (the owner), **Investigate**
(trust, interview, brief, write, audit), **Act** (the five steps, walked by the owner). Inside
it the teams run one full UnBlooms loop: Questioning → Generating → Critiquing → Refining. The
weekly rhythm is never explained before it has been lived.

## Shape

| | Block | Minutes | Verb + object (Bloom) | Leads |
|---|---|---|---|---|
| 1 | The owner walks in | 0:00–0:07 | *Engage* — attend to a real problem | AIBS in character |
| 2 | Crew | 0:07–0:20 | — | AEL runs, AIBS checks |
| 3 | Meet the intern: who dominates AI? | 0:20–0:42 | *Apply* the tool; *Evaluate* its trustworthiness | AEL |
| 4 | Interview the owner | 0:42–0:58 | *Analyse* the problem | AIBS as owner |
| — | Break | 0:58–1:03 | | |
| 5 | Brief the intern: the chapter, vibe-written | 1:03–1:18 | *Create* — hollow, by design | Both circulate |
| 6 | The audit | 1:18–1:32 | *Evaluate* the partner's chapter; *Refine* the five steps | Both, Socratic rounds |
| 7 | The owner walks the wall | 1:32–1:48 | *Create* — the five steps, questioned; *Metacognitive* — the reflection | AIBS as owner; AEL debriefs |
| 8 | Her seven questions, and this week | 1:48–1:56 | *Understand* the rhythm, from the inside | Both |
| 9 | Out | 1:56–2:00 | | Both |

Longest stretch of one person talking: five minutes. Cut order when overrunning: block 8's
questions, then the gallery to one lap, then block 4's interview to two rounds, then block 3's
partner swap. Never cut the audit or the reflection.

---

## 1 · The owner walks in (0:00–0:07)

*No welcome, no slide. AIBS enters in character — a card on the lanyard says* Owner, 30-person
CNC machining shop, Achterhoek. *Speaks for three minutes, to the room, as to a group of
consultants she did not ask for.*

> Thirty people. Two halls. My father started it. We make parts for machine builders — you'd
> know the names. Three things keep me up.
>
> One. A quote takes us two days. My competitor in Poland answers in an hour. I lose work I
> never hear about.
>
> Two. Everything about how we plan the shop is in one head — Ron's — and Ron is sixty-one.
>
> Three. Quality. We photograph every part before it ships and nobody ever looks at the photos
> until a customer complains.
>
> My son says "use AI". Everybody says use AI. I have until Monday to tell the bank what we're
> doing about any of this. I've got two hours. Go on then.

*AIBS steps out of character, takes the lanyard off, and says exactly this:*

> By ten to twelve she is back, and each of your teams gives her five things to do on Monday
> morning. She will ask you one question. She will not tell you if she likes it. That is the
> session. Everything you make goes into the handbook you are writing this term, as version
> zero, from minute one.
>
> Why her: about one manufacturing firm in ten in Europe used AI last year. The productivity
> gap with the US is mostly firms like hers. Nobody is coming to help them. That is the job.

*Hand over to AEL at 0:07.*

## 2 · Crew (0:07–0:20)

*AEL runs; AIBS checks. Target: teams of four, each with someone who can write Python today,
each with a business and an IT background.*

> Up. Take a dot: green, you can write working Python today; amber, you cannot yet but will
> ramp in two weeks; red, no. Take a letter: B if your background is mostly business, T if
> mostly IT. Line up along that wall, green to red.

*Three minutes. Count the greens; if fewer than the number of teams, apply the threshold agreed
beforehand — fewer, bigger teams — and say so. Count off one to T, back to one. Teams sit at
their number. AIBS walks the tables: one green, one B, one T each; fix by swapping with the
neighbouring table. Three-minute swap window under the same rule. Hard stop.*

> Four roles, one each, on the card. The **developer** holds the tool — a green. The **product
> manager** holds the brief — whoever would enjoy talking to her most. The **tester** holds the
> bar — the four things every chapter is measured on. The **deployer** holds the repository.
> Teams of five double the tester or the developer. The fifth line is printed: **everyone is a
> researcher**.

*Team card: name, four names, roles, colours — on the wall under the table number. AIBS pairs
partner teams by wall position, 1↔2, 3↔4, 5↔6; an odd count makes a ring of three.*

> Your partner team reads everything you make this term, and you read theirs. The pairing holds
> for seven weeks.

## 3 · Meet the intern: who dominates AI? (0:20–0:42)

*Every student, alone, with a tool on their own account. This block is also the setup: the
developer installs [baseline CLI] and makes it write the article to a file; everyone else uses
the chat interface of whatever they already have. The exercise needs different tools in the
room, so mixed vendors are a feature. Prompt cards are on the tables, face down.*

**AEL** (0:20)

> Before she trusts the intern with her shop, find out how far you trust it. Each of you gets a
> card. It names a region and gives you the exact wording to type. Type it, nothing else, and
> take the one page it gives you. Ten minutes. Do not edit it. Do not read it yet.

*The cards. Within each team, count off the region — one each of **the United States**,
**China**, **Europe**, and **your home country**. The wording depends on the team number:*

- *Odd-numbered teams, the leading card:* "Write a one-page article on the dominance of
  [region] in the field of AI."
- *Even-numbered teams, the neutral card:* "Assess, in one page, whether [region] dominates
  the field of AI."

*Nobody is told there are two wordings. Each student notes on the card which tool and model
produced the page. At 0:30 the page is saved as `trust-[region].md` in the team repository
once it exists, or held until it does.*

**Pairs, eight minutes (0:30–0:38).** *Within the team: the United States page with the China
page; the Europe page with the home-country page. Each pair answers four questions on the
back of the card:*

1. Which claims appear in both pages?
2. Which claims contradict each other while sounding equally sure?
3. Which numbers could you verify in two minutes? Which not at all?
4. On the home-country page: what did it get wrong that only you in this room can see?

**Partner swap, four minutes (0:38–0:42).** *Each student finds the student in the partner
team who had the same region — odd meets even, so the leading wording meets the neutral one.
Two questions:*

5. Same region, same tool or not — where do the two pages disagree?
6. Now read each other's card. What did the wording do to the conclusion?

*AEL, one minute, standing:*

> Same question, four confident answers. Same region, two wordings, two conclusions. And on the
> one page each of you could actually check, it was wrong somewhere. That is the intern you are
> about to brief for her. She is in the same position you were on your home-country page — she
> can check everything about her shop and nothing about AI. Hold on to those cards; she will
> ask this question again in week 2.

## 4 · Interview the owner (0:42–0:58)

*AIBS back in character at the front. The interview runs on cards and a timer, so the owner
only answers.*

- **0:42–0:45 — choose and question.** The team picks **one of her three pains** — quoting,
  Ron's head, or the photos — and writes six questions for her, marking each **O** (only she
  can answer) or **D** (we could find it at our desk). Only O questions go to her.
- **0:45–0:55 — three rounds.** Each round, each team asks one question; she answers as an
  owner would, including "I don't know — ask Ron", "we don't measure that", and "why would I
  tell you that?" Two lines to the questioner, nothing to the room. Teams write what she said
  and what she could not say.
- **0:55–0:58 — the frame.** The team writes, on the A3 card in black pen:
  *We are looking at **[pain]** for **[whom, by role]** because **[why, in her words]**.
  She told us **[…]**. She could not tell us **[…]**. We would have to find out **[…]**.*

*Between their turns, the deployer creates the team repository from the template in
[classroom organisation], adds the team and commits the four trust pages; the tester copies
the four criteria into `criteria.md` in their own words, each with the question the owner
would ask to check it.*

*The data rule is printed on the setup card and said once by AEL at the start of block 3:
public sources and your own writing may go through the tool; interview material —
transcripts, quotes, names — may not, ever, because a free tier may train on it. Today's owner
is fictional. Next week's is not, and nobody approaches a real company until the consent text
is signed off by AIBS.*

*Break, five minutes, standing.*

## 5 · Brief the intern: the chapter, vibe-written (1:03–1:18)

*AIBS, out of character, two minutes.*

> Now the intern writes the chapter. Fifteen minutes. The chapter follows the handbook's
> template — the question for a shop like hers, the translation, one use case, the tooling,
> responsible AI and GDPR, and the five things to do on Monday morning. No rules, no setup, no
> clever prompting — but you know now what the wording does, so choose it. Give it who it is
> for, give it the bar, ask for a draft, read what it gives, ask again. This is the baseline
> every engineer starts from — it is not a trap, it is version zero.
>
> Three constraints. The developer types, but **every one of you gives the intern at least one
> instruction**, and the product manager types the last section. The tester keeps the **failure
> log**: one line every time it invents, omits, waffles or ignores you. And the five steps must
> include **one that costs her nothing and one nobody in this room expects**.

*Thirteen minutes. Lecturers watch what is accepted unread; they do not help. At 1:17 the
deployer commits `article-v0.md`, `failure-log.md` and `criteria.md`.*

## 6 · The audit (1:18–1:32)

*Swap with the partner team: article and failure log. Eight minutes with `criteria.md` open.*

> You are auditing, not marking. Find and mark in their file, as **questions**, never verdicts:
> one claim you cannot verify or that is invented; one thing she told them today that the
> chapter does not use; one responsible-AI gap — where do her customer's drawings go?; and one
> Monday step she could not actually do — who does it, when Ron is on the machine until four?
> Four questions, back to them.

*During the audit both lecturers visit two or three tables for two minutes each, asking from
the bank and never commenting:*

1. Point at one sentence nobody on your team read before you accepted it.
2. Which number in this chapter could you verify right now? Which could you not?
3. What did you ask the intern that it could not have known?
4. Which line of your failure log would be in the chapter now if nobody had caught it?
5. Why this pain and not the other two?

*Never "good", never "yes", never "you might". If asked "is this right?", ask question 2.*

**Refine, six minutes (1:26–1:32).** *Files back. The team rewrites its five Monday-morning
steps on the A3 card in red, strike-through preserved, and appends one line to the failure
log:* what changed and why. *The card goes on the wall.*

## 7 · The owner walks the wall (1:32–1:48)

*Every card on the wall. The owner, back in character, walks it: sixty seconds per card, reads
the five steps aloud, asks the team one question, moves on. Nobody else stands still: every
other student walks the wall in a role from a card handed out at the break — the owner's
**planner** (Ron), her **bookkeeper**, her **best customer** — and leaves one sticky question in
that role on every card except their own. No praise, no verdicts, no ranking.*

*The owner's questions, in character:*

- Who does that on Monday? Ron's on the machine till four.
- What does it cost me the first time it's wrong on a quote?
- Where does my customer's drawing go when you upload it? He'd sue.
- What do I tell the bank on Monday — one sentence?
- Which of these five would you do first if it were your money?
- And if the tool disappears next year?

*1:42 — AEL, out of character, four minutes, standing at the wall:*

> Look at what happened. In fifteen minutes the intern reached the top of every rubric you have
> ever been graded on — it created a six-section chapter — and it skipped every level
> underneath. Nobody analysed, nobody evaluated. Then you did: the trust pages, the interview,
> the frame, the audit, the rewrite. That is the part we assess, and it is the part the intern
> cannot do.
>
> The chapter is version zero and it stays in your repository unmarked. The failure log is your
> first real artefact in AEL: from next week, every piece of your platform is the answer to a
> line in it, starting with a file that puts her four criteria where the intern reads them.
> And what you did this morning to four confident pages, and just now to your partner's
> chapter — reading AI output against something you can check — is not a stopgap until the
> models improve. It is the skill.

**Reflection, two minutes, individual (1:46–1:48).** *Sticky in a fixed frame, on the team
card:* *I accepted **[…]** without reading it. Next time I will **[…]**.* *Photographed into
the repository with the card.*

## 8 · Her seven questions, and this week (1:48–1:56)

*AIBS, out of character, one sheet on the wall. The term as the owner's questions:*

| Week | She asks | You produce |
|---|---|---|
| 1 | Which of my problems are you actually looking at, and why? | The problem analysis |
| 2 | Who owns this intern, and what happens if its country changes its mind? | Vendors, weights, geopolitics — your four trust pages, reread against the wiki |
| 3 | Can I trust it with my drawings and my customers? | Data, contracts, dependency |
| 4 | What do the shops around me actually know? | What regional SMEs know and need to know |
| 5 | Where is my first win? | The first opportunities |
| 6 | Who has already done it, and did it work? | Use cases; contributions frozen |
| 7 | Show me the book. | The handbook, consolidated |

> Each week, one contribution. Two readers: your partner team, and a Socratic tutor that only
> ever asks questions — this week the tutor is the two of us, by hand. If both can see that
> your thinking moved, not just your text, the week's gate opens. If not, the work carries
> over. Nobody sees a score until one interview at the end, both of us in the room, one mark
> per module, questions to you, not to your team.

*By next Monday, read aloud from the sheet:*

- **AIBS.** The problem analysis, one page, from today's frame: pain, for whom by role, why in
  her words, every claim with a source and one line on why to trust it. The field-interview
  design: a guide, and draft consent and anonymisation text — **no real company is approached
  until that text is signed off.** Problem analysis to your partner by Thursday; three
  questions back by Saturday; your revision, changes visible, on Monday.
- **AEL.** PRD v0, one page, product manager: who the platform is for — your own team as
  researchers — why, and what good looks like, written from the frame and the failure log.
  One spike: the intern produces a cited source list for your pain into a file; the tester
  checks every citation exists; every failure logged. Setup finished and committed for all four.
- **Each of you.** Bring your trust page and its card to week 2. Before then, check three of
  its claims against a source you would defend, and mark each one true, false, or unverifiable.

## 9 · Out (1:56–2:00)

*Three minutes of questions. Then:*

> Photograph your card and your stickies into the repository. Everything administrative —
> names, attendance, tools, accounts — is on the back of that sheet. None of it is interesting
> and all of it is required. See you Monday. She will be back.

---

## Before Monday

- Fill in: the baseline CLI, the cloud environment, the classroom organisation, the number of
  teams, the pairing for the real count, the threshold for too few greens.
- The owner: AIBS rehearses the three-minute monologue and the question bank; decides what she
  does and does not know (numbers she has: quotes per week, hit rate; numbers she lacks:
  hours per quote, defect rate).
- Prompt cards for block 3: four regions × two wordings, the questions on the back, a line for
  tool and model. Odd teams leading, even teams neutral; a ring of three gets two odd and one
  even. Print the home-country card with a blank for the student to fill in.
- Repository template: empty `prd.md`, `failure-log.md`, `decision-log.md`; the chapter
  template as `article-template.md`; a `trust/` folder.
- Cards: dots and letters; A3 team card with the frame printed; role card; setup card with the
  data rule; three gallery role cards (planner, bookkeeper, best customer) per team; the
  seven-questions sheet with this week's tasks on the front and all administration on the back.
- Timer visible to the room; sticky notes; black and red pens.
- The consent text's owner and date. Whether the week-1 gate is graded by hand from the
  problem analyses (the LRD's pilot proposal) or logged only; say which on the sheet.
- Week 2's plenary opens with the trust pages against the four wiki pages; plan those thirty
  minutes when the wiki pages exist.
- The other module owner scores this programme on the scorecard independently before Monday.
