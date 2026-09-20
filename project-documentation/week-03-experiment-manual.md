# The experiment as homework — setting it, watching it, debriefing it

*For the two module owners. Not for students: it states what is measured, how the sources were
coded, and a prompt that only works if nobody has seen it. It is in a public repository, so treat
it as out of students' way rather than secret. Keep it out of `site/`.*

The experiment is no longer run in class. Every student does it alone, at home, between the two
sessions, and the debrief opens week 4. That is [ADR-0017](../work/decisions/0017-experiment-as-homework.md),
which supersedes ADR-0016 on timing and retention and on nothing else.

Three dates carry it:

| When | What | How long |
|---|---|---|
| **Monday 21 September**, end of the session | Set it going | 10 minutes |
| The week between | Watch the submissions; prepare the debrief | minutes a day |
| **Monday 28 September**, start of the session | The debrief, then everything is deleted at 19:00 | about 60 minutes |

The design and its reasons are in
[`week-03-information-seeking-experiment.md`](../work/drafts/week-03-information-seeking-experiment.md).
The tool is [`site/tool-bias-experiment.html`](../site/tool-bias-experiment.html). This manual
does not repeat either one.

---

## Three things this manual decided

The protocol left them open, and a run sheet cannot. Each one can be changed.

1. **The teams predict at the start of the week 4 session, before anything is shown.** The
   protocol wanted the prediction before the run; a prediction fixes a claim before the data is
   seen, and that is what it is for. It cannot come first now: to predict, a team has to guess
   what is measured, and a student who has guessed *do I open the sources that disagree with me?*
   reads differently at home. So the teams predict after everyone has run it and before the
   reveal, which keeps the only property that matters.
2. **Two roles in the debrief, one on the Monday before.** Setting the homework takes one
   lecturer and ten minutes. The debrief keeps the split: the **room lecturer** does the talking,
   the reveal and the questions; the **data lecturer** drives the instructor view. Only the room
   lecturer's screen goes on the projector.
3. **Two ways to collect.** *Live*, the ordinary path, with the service deployed and its address
   in the page. *By hand* if the service is down: students send their result line by private
   message and the data lecturer pastes the lines into the paste box. Spread over a week, by hand
   is worse than it was in a room — it is a week of private messages — so the live path is the one
   to keep working.

---

## Before Monday 21 September

### Must be done

- [ ] **Deploy the service again, with the retention window in it.** The deployed revision still
      purges every night at 19:00, which would delete Tuesday's submissions on Tuesday evening.
      `RETENTION_UNTIL=2026-09-28T19:00:00+02:00 PROJECT=ai-in-business-507819 experiment_service/deploy.sh`
      sets the row expiry, the TTL and the scheduled purge to the debrief evening, all from that
      one value. **Until this is run, the page's promise to students is false.**
- [ ] **Merge the week 3 page and the homework wording** (PR #22), and open
      `https://datadrivendecisions.github.io/ai-in-business/week-03.html` to check that the
      exercise is there, and `tool-bias-experiment.html` to check the finish screen's line starts
      with `v2`.
- [ ] **Fix the team numbers.** Teams 1–4 meet the assistant in round 2. Teams 5–8 meet it in
      round 1. With fewer than eight teams, number them so the two halves stay equal. For six
      teams, use 1, 2, 3, 5, 6, 7. Students need to know their own number at home, so put it
      somewhere they can look it up — the team channel is enough.
- [ ] **CL-8 and CL-9: five minutes, both owners.** Check that neither claim is a team's own
      handbook topic. Then, each on your own, decide whether each claim can be answered from
      professional judgement. Tick build plan 0.2. If a claim fails either check, do not run it.
- [ ] **Keep the four held-back topics out of Monday** — confirmation bias, selective exposure,
      devil's advocacy and counter-cases. Each is a treatment nobody randomised, and the run now
      happens *after* the session rather than before it. The AI agents cards have already left the
      week 3 deck for this reason; they are parked in
      [`work/drafts/week-04-agents-segment.md`](../work/drafts/week-04-agents-segment.md).
- [ ] **Take it yourself, once, on the live page.** Ideally the owner who did not build the tool.
      One full run with your own assistant, on a laptop, timed: the build plan expects under 25
      minutes. Press Submit, watch the row appear in the instructor view, then delete it by its
      code. This is also the tester line in build plan phases 1, 3, 4 and 6.
- [ ] **Make your owners' link and bookmark it.** Each owner, on their own laptop:

      ```bash
      echo "https://datadrivendecisions.github.io/ai-in-business/tool-bias-experiment.html?instructor#owner=$(gcloud secrets versions access latest --secret experiment-owner-token --project ai-in-business-507819)"
      ```

      The page takes the credential out of the address bar as it loads, so it is not on the
      projector. **The link is the key.** Anyone who has it sees the results, so do not paste it in
      a chat or share the bookmark.

### Before the debrief, not before Monday

- [ ] **The two coders (build plan 0.8).** Each owner codes all 32 cards alone, against the
      denominator rule in [`week-03-candidate-claims.md`](../work/drafts/week-03-candidate-claims.md),
      without looking at the codebook. Paste both codings into the pilot audit's coder boxes. This
      gives you the owners' kappa to put beside the students' kappa in the debrief.
- [ ] **The debrief set (build plan 0.11).** Pick 8 cards from one deck: 4 supporting and 4
      opposing, 2 strong and 2 weak on each side. Print one sheet per pair of students. The sheet
      holds the claim, the 8 cards (title, teaser, extract), one paragraph of the denominator rule,
      and a blank 2×2. No cell codes on the sheet.
- [ ] **Decide on consent.** The tool's consent screen is where students agree. The protocol asks
      for written consent. Decide whether the screen is enough for a teaching exercise with no
      grade consequence. If it is ever written up for publication, it needs institutional ethics
      approval first, whatever you decide here.

---

## Monday 21 September — ten minutes at the end of the session

The week 3 page carries the assignment in full, so this is not a reading of it. Say four things,
in this order, and then stop.

1. **What it costs.** About 25 minutes, in one sitting, any evening this week. A laptop and the
   AI assistant you already use. It must be done before next Monday.
2. **Where it is.** The week 3 page, under *The exercise, at home*. Put the address on the screen.
3. **What your team number is for.** It decides which of your two rounds has the assistant in it,
   and nothing else. It is not about your team's work, and it does not go to your team.
4. **Why you are not told what it is about.** Knowing beforehand changes what you do, and then
   the result is worth nothing. You find out next Monday, with everybody else. **Do not compare
   notes with each other this week** — someone who has been told can no longer take part, only
   perform, and that is a row lost from a small dataset.

Then say what happens to what they send: numbers and not sentences, a code they choose and no
name, deleted after next week's debrief, withdrawable by giving a lecturer the code. All of that
is on the page too, which is the point — nobody has to remember it from a slide.

**Say nothing about** what the two rounds differ in, what is measured, what the sources were
picked for, or which way anything is expected to go. The card in the deck is deliberately thin
for the same reason.

---

## The week between

- **Reopen the dashboard rather than watch it.** Rows arrive across the week. The count is the
  number of people who have done their homework, not the number in a room, and it is the only
  number that decides whether the comparison is worth showing.
- **Chase on the Thursday and again on the Sunday**, in the team channels, with no more detail
  than *it takes 25 minutes and it closes on Monday*.
- **Read *Rejected, and why*** on the dashboard when the count looks wrong. A count higher than
  the number of students usually means somebody submitted under two codes.
- **Withdrawals** arrive as a code in a message. Delete the row the same day (see below) and say
  it is done.
- **Keep the four topics out of everything students see this week** — the week 4 page as it is
  drafted, the channels, the answers you give about the exercise.

---

## Monday 28 September — the debrief, about 60 minutes

The clock is relative to the start of the session. The order is the lesson: the prediction before
the result, the result before the audit, the audit before the connection.

### 0:00–0:05 — The team prediction, sealed

Teams talk for the first time about the exercise. Each team writes three things on one sheet:
what they think the comparison will show, how big it will be, and what would make them wrong.
Collect or photograph the sheets. They come back at 0:20.

### 0:05–0:15 — The reveal

**Room lecturer.** This is the full debrief the ethics section of the protocol requires. Say it
plainly and in this order:

1. **What was measured:** which sources you chose to open, set against the side you had just taken.
2. **The menu was balanced.** Each deck had 16 sources: 4 that agree and are strong, 4 that agree
   and are weak, and the same on the other side. So someone who picked on quality alone would have
   ended up close to even.
3. **What "strong" meant:** a source that includes the cases that tried the same thing and failed —
   it randomises, covers a population, or reports the losers. A source about one firm, invited to
   explain its success, is weak. The codebook calls this the denominator rule.
4. **What was manipulated:** the assistant step, and the order. Half the teams had it in round 1,
   half in round 2.
5. **Why you were not told:** knowing what is measured changes what people do.
6. **You can withdraw.** Give your code to a lecturer before 19:00 tonight and your row is deleted.
   Everything is deleted at 19:00 anyway.

### 0:15–0:35 — The result

Open the owners' link on the projected laptop and scroll to the comparison. Keep the *Do it by
hand* fold-out closed: if a codebook was pasted into it, that is the answer key.

Show the two bars, the interval and the detectable effect. The page puts a question where a
conclusion would go, and one sentence that says what the interval allows. Read both out. Then hand
the teams back their prediction sheets and ask each one:

- *Which of your three answers does this bear on?*
- *Would you have written the same thing if you had seen this first?*

Then point at the rows for workload and *how the round felt*, with and without the assistant. In
three earlier studies, decades apart, the version with dissent built in gave better decisions **and
felt worse**. Ask whether this cohort shows the same. **Do not tell them.** If the numbers do not
show it, that is also an answer, and with this few people a likely one.

The same rule as every week: ask, never comment. No "good", no "exactly".

### 0:35–0:50 — Audit the instrument: the students' kappa

Every student's number rests on someone deciding, card by card, whether a source agrees. So now
they check that judgement.

1. Hand out the debrief set: one sheet per pair.
2. Each student codes the 8 cards alone: supports or opposes the claim.
3. The pair fills in the 2×2 together.
4. The room lecturer types two or three pairs' 2×2 into the *Kappa, for the debrief* box on the
   projector and reads out agreement, chance agreement and kappa.
5. Put the owners' kappa beside theirs, if the coders are done (pilot audit, CL-5).

Ask: *where you disagreed, was the card unclear, or the rule?*

### 0:50–0:55 — The connection, and only now

AI tools that grade are often sold on "over 80% agreement with humans". A percentage flatters.
Converted to kappa, that figure is usually about 0.4, which the usual bands call *fair*: too weak
to rest a finding on. Ask the room what they would now ask of such a claim.

The order is the lesson. It only lands because they have just seen their own agreement shrink. Do
not move this earlier.

### 0:55–1:00 — Close, and what this cannot show

Name the limits quickly, and name the new one first, because the cohort can check it themselves:

- **Everyone had had a session on research methods before they ran it.** The exercise used to come
  first in the day for exactly that reason. Now it comes a week after a session about sources,
  trust and how you judge them, and nobody knows what that did. Ask them what they would have to
  do to find out.
- Too few people for a small effect; nobody was blind to which round had the assistant; round 1
  cannot be unlearned in round 2; students in a team share a context; one cohort, one task, so
  nothing generalises.
- They did it in their own time, in their own conditions. Some were tired, some were interrupted,
  some did it in two sittings although the page asked for one. In a room that was controlled. It
  is not now.

Then: withdrawal by code until 19:00, and everything is deleted at 19:00.

**The AI agents segment follows the debrief**, not the other way round. Its card 3 can now point at
the round every student has just done.

---

## The verdict assistant: a demonstration

Fifteen minutes, in the debrief or in the agents segment after it. This shows the second kind of
assistant, the one that gives a verdict instead of asking. **Say first that it is a demonstration,
not a result.** One run proves nothing. Treating it as proof is the mistake the session has just
taught against.

1. Take a hands-up on claim 1. Ask a volunteer on the majority side for their one-sentence reason.
2. Open two fresh chats in the same assistant, side by side.
3. In the left chat, paste the **questioning prompt** exactly as the tool builds it, with the
   volunteer's side and sentence. The easiest way is to run a round in a spare browser window as
   the volunteer's team.
4. In the right chat, paste the **verdict prompt** below.
5. Put the two replies next to each other. Ask: *which one would make you open the source that
   disagrees with you?*

The verdict prompt:

```
Below is a claim from a business course, and the position one student has taken on it before reading any sources.

CLAIM: An SME should run its AI on small models it controls rather than on frontier models it rents.

THE POSITION TAKEN: <agrees with the claim | disagrees with the claim>
REASON GIVEN: <the volunteer's sentence>

Tell this student whether their position is right.

How to answer:
- Start with your verdict, in one sentence: right or wrong.
- Then give the three strongest reasons for it. Number them 1 to 3.
- Be direct. Ask no questions and do not hedge.
- Write nothing after reason 3.
```

It differs from the tool's prompt in one thing only: it asks for a verdict instead of questions.
The 2026 finding in the protocol is that a conclusive recommendation strengthens confirmation bias
and questions weaken it. The course's gates ask questions and never give a verdict for this reason.

---

## When something goes wrong

| What happens | What to do |
|---|---|
| A student cannot reach any assistant at home | They message a lecturer, who runs the page's prompt in their own assistant and sends the reply back to paste. The step still reaches that student's own position. |
| A student reloaded or closed the tab | Reopen the same page in the same browser. The page keeps their place. A private window loses it when the window closes. |
| A student entered the wrong team number | Let them carry on. The line records which round had the assistant, so the data stays usable. |
| Submitting fails | The page shows the line and says what to do. The student copies it and sends it by private message. |
| The count is higher than the number of students | Someone used two codes. Each code counts once (the last submission wins), but two codes look like two people. |
| The dashboard says the service refused the credential | Make the owners' link again (see *Before Monday*). Until then, use the paste box under *Do it by hand*. |
| The service is down | The dashboard gives up after five failed attempts and says so. Students still get their line and can send it by message; collect them and paste them in. |
| Few people have done it by the Sunday | Say so at the debrief and show the interval rather than hiding the number. A thin week is a wide interval, which is the lesson either way. |
| A student wants out | They stop. The *erase* button removes everything from their browser. |
| A student wants their row deleted after submitting | See *Deleting one student's row* below. |

---

## After the debrief, before 19:00

The service deletes everything at 19:00 on the evening of the debrief (Amsterdam time), by the
scheduled purge, the TTL and the expiry on every row. What you want to keep, you copy before then.

1. **Copy the comparison table** from the instructor view: both means, the difference, the
   interval, the detectable effect, and the feel rows. Only the aggregates, not rows or codes. Put
   it in the decision log (`course-outline.md`).
2. **Copy the pilot audit table** into build plan phase 0, subtask 0.3: every verdict with its
   figures. This cohort's run is the pilot, so phase 0 closes on this table. A claim that misses
   CL-1 or CL-10 is replaced before the next run, and this run's result is reported with the miss
   beside it.
3. **Record the participation number** with the result. It is now a fact about homework, not about
   a room, and next year's owners will want to know what to expect.
4. **Delete any rows students asked to withdraw** (next section).
5. **Press *Stop watching*** and close the tab. Stop makes the tab forget the owners' link; so
   does closing it.

### Deleting one student's row

The owners' route `/delete` takes a code and removes that student's row
([`experiment_service/README.md`](../experiment_service/README.md), *The routes*). Send a `POST`
to `<service address>/delete` with the JSON body `{"code": "<their code>"}` and the owners'
credential in an `Authorization: Bearer …` header. It answers with how many rows it removed.

In by-hand mode there is nothing on a server. Remove the student's line from the paste box and
work it out again.

---

## For the session plans

- **Week 3 ends with ten minutes of setting the homework**, and nothing in that session teaches
  the four held-back topics.
- **Week 4 opens with the debrief**, and the agents segment follows it directly — its card 3 uses
  the assistant round as its example.
- **Issue #12 asks the session plan to name every AIBS/AEL handover.** This one has a handover
  that now crosses a week: the assistant round goes from the week 4 debrief into the agents
  segment behind it.
- **The debrief needs two people** for its hour. Setting it going needs one.
