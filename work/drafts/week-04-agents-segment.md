# The AI agents segment, held back to week 4

These three cards were cards 8 to 10 of the week 3 deck. They came out when the information-seeking
experiment became homework done after the week 3 session: a segment on agents shown before students
run the experiment is a treatment nobody randomised, which is the ordering constraint in
`project-documentation/build/week-03-agents-deck/` and in ADR-0017. They belong in the week 4 deck,
after the debrief of the experiment, where card 3 can point at the round every student has just done.

Their notes are in the week 3 notes file's history; their provenance is unchanged, in
`project-documentation/build/week-03-agents-deck/provenance.md`.

```html
<section class="slide" id="s8">
    <div class="slide-head"><div class="slide-kicker">AI agents</div><span class="slide-no">8 / 11</span></div>
    <h2>You have used an agent since week&nbsp;1</h2>
    <p><strong><a href="https://businessdatasolutions.github.io/ai-wiki/concepts/ai-agents" target="_blank" rel="noopener">Agent</a>:</strong> an LLM (large language model) using tools in a loop, towards a goal.</p><ul><li><strong>Workflow or agent?</strong> Code or model: who picks the next step?</li><li><strong>The loop:</strong> reason, act, observe (ReAct).</li><li><strong>The week 1 intern:</strong> capable, needs oversight.</li></ul>
  </section>
```

```html
<section class="slide" id="s9">
    <div class="slide-head"><div class="slide-kicker">AI agents</div><span class="slide-no">9 / 11</span></div>
    <h2>The model is rented; the harness is the part you own</h2>
    <ul><li><strong>Harness:</strong> the software around the model. Model as CPU, harness as <a href="https://businessdatasolutions.github.io/architecture-of-scale/harness-is-os-en.html" target="_blank" rel="noopener">operating system</a>.</li><li><strong>This week&rsquo;s choice:</strong> where knowledge lives. RAG retrieves, LLM Wiki compiles, Fat Skills act &mdash; <a href="https://businessdatasolutions.github.io/architecture-of-scale/architecture-of-scale-en.html" target="_blank" rel="noopener">one question, four ways</a>.</li><li><strong>Still ahead:</strong> Contracts, Constraints, Compounding.</li></ul>
  </section>
```

```html
<section class="slide" id="s10">
    <div class="slide-head"><div class="slide-kicker">AI agents</div><span class="slide-no">10 / 11</span></div>
    <h2>Trusting an agent splits three ways: data, output, people</h2>
    <ul><li><strong>Data.</strong> Rent the model, or run a small one in-house.</li><li><strong>Output.</strong> Users regret an agent that <a href="https://businessdatasolutions.github.io/ai-wiki/concepts/agent-oversight-and-delegation" target="_blank" rel="noopener">acted beyond what they authorised</a> &mdash; even when it was right.</li><li><strong>People.</strong> Hiding AI use: <a href="https://businessdatasolutions.github.io/ai-wiki/concepts/ai-knowledge-hiding" target="_blank" rel="noopener">14&nbsp;% where trust is highest, 47&nbsp;% where lowest</a>.</li></ul>
  </section>
```
