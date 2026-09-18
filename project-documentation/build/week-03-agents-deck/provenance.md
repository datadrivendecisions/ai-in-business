# Provenance — the AI agents segment

Every factual claim on the three cards (s8–s10 of `site/week-03-slides.html`) and in their note
blocks (`project-documentation/slides/week-03-notes.md`), mapped to the one AI Wiki page it rests
on. The slug is the path under `ai-wiki/wiki/` without `.md`; `check-agents-deck.py --deck` opens
each one (CT-7). Card 1 is s8, card 2 is s9, card 3 is s10 — renumbered twice as the AIBS research
methodology segment ahead of them grew, first to s3–s6 and now to s3–s7; the cards and their
sourcing are unchanged. Drawn from the query trace
`ai-wiki/inspiration/2026-09-18-ai-agents-intro-deck-outline-query-trace.json` and re-read
against each page on 18 September 2026.

| card | claim, in eight words or fewer | wiki slug | section heading |
|---|---|---|---|
| 1 | Agent: LLM, tools, loop, goal | `concepts/ai-agents` | The four-clause definition, now shared across competing vendors (August 2026) |
| 1 | Google and Anthropic material share the definition | `concepts/ai-agents` | The four-clause definition, now shared across competing vendors (August 2026) |
| 1 | Wooldridge's definition leaves the LLM out | `sources/2009-01-01-wooldridge-introduction-to-multiagent-systems-ch1-2` | TL;DR |
| 1 | Wooldridge's definition admits a thermostat | `concepts/ai-agents` | Debates and supersession |
| 1 | Workflow: code picks path; agent: model does | `sources/2024-12-19-anthropic-building-effective-agents` | TL;DR |
| 1 | Workflows can also use tools and loop | `concepts/ai-agents` | The four-clause definition, now shared across competing vendors (August 2026) |
| 1 | The loop: reason, act, observe (ReAct) | `concepts/react-reasoning-acting` | The core mechanism |
| 1 | Intern analogy is the week 1 anchor | LRD | Part 8, week 1 ("the intern analogy as the shared vocabulary"; the PRD's "Appendix A.1" is the module-identity table) |
| 1 | Karpathy: agents are "intern entities" needing oversight | `concepts/ai-agents` | Working definition |
| 2 | Harness: the software around the model | `concepts/agent-harness` | Working definition |
| 2 | Model is CPU, harness is operating system | `concepts/agent-harness` | The operating-system analogy |
| 2 | Context window is the RAM | `concepts/agent-harness` | The operating-system analogy |
| 2 | Model rented, overtaken within the year | `concepts/agent-harness` | The model is rented; the harness is owned |
| 2 | Harness is what a company owns | `concepts/agent-harness` | The model is rented; the harness is owned |
| 2 | RAG retrieves, LLM Wiki compiles, Fat Skills act | `syntheses/knowledge-architectures-for-llm-agents` | The three-architecture comparison matrix |
| 2 | The choice follows from the agent's job | `syntheses/knowledge-architectures-for-llm-agents` | The decision tree — "what is your agent's job?" |
| 2 | Contracts, Constraints, Compounding are harness layers | `concepts/agent-harness` | Working definition |
| 2 | Those layers are debrief reading, weeks 4–6 | LRD | Part 8, AEL concept column |
| 3 | Trust brief: data, output, people | LRD | Part 8, week 3 AIBS row |
| 3 | SLM defined by the device it fits | `concepts/small-language-models` | The definition is device-indexed, so it moves |
| 3 | Users regret agents acting beyond authorisation | `concepts/agent-oversight-and-delegation` | The failure mode that is not about accuracy |
| 3 | Regret persists even when output was right | `concepts/agent-oversight-and-delegation` | The failure mode that is not about accuracy |
| 3 | Trigger: irreversible and externally visible, e.g. email | `concepts/agent-oversight-and-delegation` | Three findings that tell you where to put the gate |
| 3 | 604 daily users: 14 % versus 47 % hide | `concepts/ai-knowledge-hiding` | The empirical claim: trust, not governance |
