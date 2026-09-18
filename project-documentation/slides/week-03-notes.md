# Week 3 — instructor notes

Speaker notes for `site/week-03-slides.html`, one block per card, keyed by the card's id.
`build_deck.py` folds them into the presenter deck. So far the page holds the AI agents
segment (s3–s5) and two placeholders around it; the rest of the session's cards and notes
are added with the rest of the deck. The folder is public, so nothing that only works if a
student has not read it goes here — no hypothesis direction for the experiment, no codebook,
no agent prompt. That material stays in `work/drafts/week-03-information-seeking-experiment.md`.

The segment's spec is in `project-documentation/build/week-03-agents-deck/`; every claim
below has a row in its `provenance.md`.

## s1

Session of Monday 21 September. AIBS theme: trust and AI safety. AEL decision: where the team's knowledge lives.

## s2

Placeholder for the experiment debrief, which the rest of the deck supplies. The AI agents segment comes straight after it and never before: an agents segment ahead of the experiment would be a treatment nobody randomised.

## s3

About five minutes. Connects to AEL week 1 (the spike) and AEL week 2 (the debrief that named ReAct).

Every team has used an agent for two weeks: the agentic command line of the week 1 spike. This card gives that a name. The definition is the one Google and Anthropic developer material both use by mid-2026: an LLM with tools, running in a loop, towards a goal. Wooldridge's textbook definition from 2009 leaves the LLM out. A thermostat passes his test.

The line between a workflow and an agent is who picks the next step. In a workflow, your code sets the path. In an agent, the model decides. Both can use tools and loop.

The loop is the one they watched in the spike: reason, act, observe, and again. If the week 2 debrief did not name ReAct, introduce it here rather than recall it.

The intern from week 1 still holds: capable, and still needs someone in charge of judgement and oversight — Karpathy's phrase for it is "intern entities".

## s4

About five minutes. Connects to AEL week 3, this week's knowledge-architecture decision, and back to AIBS week 2 on vendor dependency.

The harness is everything around the model: what it sees, which tools it may call, what happens after each step. Open the *Harness is the OS* visualisation: the model is the CPU, "powerful but inert" in the source's words; the context window is the RAM; the harness is the operating system that decides what the CPU sees and when.

Why it matters to an SME: the model is rented from a vendor who will be overtaken within the year. The harness is what a company builds, owns and improves.

This week's AEL decision is one part of that harness — where the team's knowledge lives. RAG retrieves passages from documents at the moment of the question. An LLM Wiki compiles sources into pages ahead of time. Fat Skills act on what is known without being asked. Open *one question, four ways* and let the room see the same question answered each way. The choice follows from what the agent's job is.

Name Contracts, Constraints and Compounding and move on. They come in weeks 4 to 6, each after the failure it answers.

## s5

About five minutes. Connects to AIBS week 3: the brief asks whether the SME can trust AI, and splits the answer three ways.

Data. The model is rented and the harness owned, so the question is what leaves the building. A small language model is defined by the device it fits on, which turns "can we run it ourselves?" into a question with an answer.

Output. People regret an agent that acted beyond what they would have authorised, even when the result was correct. The trigger is an action that cannot be recalled and that someone outside sees — sending an email is the example. Tie it to the room: in one of the two rounds everyone put their position to an assistant. By the definition on the first agents card that was not an agent — no tools, no loop, it could only reply. Nothing it did could be recalled or seen outside the room, which is the safe end of that scale. Where should an SME's first real agent sit?

People. Whether employees admit to using AI follows trust. In a survey of 604 daily users, 14 % in the most-trusting quartile hid their AI use, against 47 % in the least-trusting.
