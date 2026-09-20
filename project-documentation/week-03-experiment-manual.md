# Week 3 — running the experiment

*For the two module owners. Not for students: it states what is measured, how the sources were
coded, and a prompt that only works if nobody has seen it. It is in a public repository, so treat
it as out of students' way rather than secret. Keep it out of `site/`.*

The session is **Monday 21 September 2026**. This manual covers the experiment block only: what
to prepare, the 150 minutes, what can go wrong, and what to do before the data is deleted that
evening.

The design and its reasons are in
[`week-03-information-seeking-experiment.md`](../work/drafts/week-03-information-seeking-experiment.md).
The tool is [`site/tool-bias-experiment.html`](../site/tool-bias-experiment.html). This manual
does not repeat either one.

---

## Three things this manual decided

The protocol left them open, and a run sheet cannot. Each one can be changed.

1. **The teams make their prediction *after* the two rounds, not before.** They still predict
   before they see any result. The protocol put it before the session. But to predict, a team
   has to guess what is measured. A student who has guessed "do I open the sources that disagree
   with me?" then reads differently. The protocol itself names that as the biggest threat.
   A prediction written after the rounds but before the reveal still fixes the claim before the
   data is seen.
2. **Two roles.** Either owner can take either one. The **room lecturer** runs the room: the
   talking, the reveal and the debrief. The blueprint gives this to the AIBS owner. The **data lecturer** runs the
   instructor view on their own laptop, watches submissions come in, and solves problems with
   laptops. Only the room lecturer's screen goes on the projector.
3. **Two ways to collect the results.** *Live* when the service is deployed and its address is
   in the page. *By hand* when it is not. Then students send their result line to the data
   lecturer in a private chat message, and the data lecturer pastes the lines into the paste box. The
   block works either way. By hand costs about ten minutes.

---

## Before Monday

The session is on Monday, so this list is short on time. The first group decides whether the
block can run at all.

### Must be done

- [ ] **Merge the branch `week-03-experiment-live` and check the live page.** PR #19 was merged
      on 18 September without this work. The version students will use exists only on that branch;
      the live page is an older version with no Submit button and without the timing the pilot needs. After merging, open
      `https://datadrivendecisions.github.io/ai-in-business/tool-bias-experiment.html` and check that the finish
      screen's line starts with `v2`.
- [x] **The "Not piloted" notice is removed** from the top of the tool page (18 September). It
      told students the claims were meant to divide a room, which is part of the design.
- [ ] **CL-8 and CL-9: five minutes, both owners.** Check that neither claim is a team's own
      handbook topic. Then, each on your own, decide whether each claim can be answered
      from professional judgement. Tick build plan 0.2. If a claim fails
      either check, do not run it.
- [ ] **Fix the team numbers.** Teams 1–4 meet the assistant in round 2. Teams 5–8 meet it in
      round 1. With fewer than eight teams, number them so the two halves stay equal. For six
      teams, use 1, 2, 3, 5, 6, 7. Put the number on each team's card or table.
- [ ] **Tell students to bring a laptop, and to be able to reach an AI assistant they normally
      use.** Say nothing else about the session.
- [ ] **Keep the week-3 page and its pre-reading free of** confirmation bias, selective exposure,
      devil's advocacy and counter-cases until after the session. Each of those is a treatment
      nobody randomised.
- [ ] **Do a dry run.** Ideally the owner who did not build the tool does it. Take the whole
      session once on a laptop and once on a phone, with your own assistant, and time it. The
      build plan expects under 25 minutes. This also closes the tester lines in build plan
      phases 1, 3, 4 and 6.
- [ ] **Rehearse the instructor view.** Open your owners' link (below). Then open *No link, or
      the service is down? Do it by hand*, load each fixture, and watch the comparison and the
      sentence under it change. The fixtures use the codebook the live feed received, so there is
      nothing to paste.

### Should be done

- [ ] **The two coders (build plan 0.8).** Each owner codes all 32 cards on their own, against
      the denominator rule in
      [`week-03-candidate-claims.md`](../work/drafts/week-03-candidate-claims.md), without looking
      at the codebook. Paste both codings into the pilot audit's coder boxes. Doing it before
      Monday gives you the owners' kappa to put beside the students' kappa in the debrief. If it
      is done later, the pilot audit still closes CL-5.
- [ ] **The debrief set (build plan 0.11).** Pick 8 cards from one deck: 4 supporting and 4
      opposing, 2 strong and 2 weak on each side. Print one sheet per pair of students. The sheet
      holds the claim, the 8 cards (title, teaser, extract), one paragraph of the denominator rule,
      and a blank 2×2. No cell codes on the sheet.
- [ ] **Decide on consent.** The tool's consent screen is where students agree. The protocol asks
      for written consent. Decide whether the screen is enough for a teaching exercise with no
      grade consequence. If it is ever written up for publication, it needs institutional ethics
      approval first, whatever you decide here.

### Only for live collection

- [x] **The service is deployed** (18 September 2026): `experiment-service` in
      `ai-in-business-507819`, `europe-west4`, with a Firestore database of its own called
      `experiment`. Its account can reach that database and no other, so it cannot read the
      gate's `owner_reports/`. The 19:00 purge job and the TTL policy are set.
- [x] **The address is in the page**: `SERVICE.origin` in `site/tool-bias-experiment.html`. It
      goes live with the merge of `week-03-experiment-live`.
- [x] **Redeployed with the preflight fix** (revision `experiment-service-00002`). A full session
      in a real browser, served under the Pages address, submitted to the live service and appeared
      on the owners' dashboard. The test row was deleted.
- [ ] **Redeploy once more, so the service holds the codebook.** Run
      `PROJECT=ai-in-business-507819 experiment_service/deploy.sh`. It stores the 32 card-to-cell
      pairs from `work/drafts/week-03-codebook.md` in Secret Manager and gives them to the service,
      which hands them only to the owners' dashboard. Until then the live view stops and asks for a
      pasted codebook.
- [ ] **Test the Submit button on the published page**, not a local copy. The service answers
      `https://datadrivendecisions.github.io` and nothing else, so a page opened from your own
      laptop falls back to "copy your line". Take one session on the live page, press Submit, and
      watch it appear in the instructor view. Then delete it by its code.
- [ ] **Make your owners' link and bookmark it.** Each owner, on their own laptop, runs this once
      and bookmarks the address it prints:

      ```bash
      echo "https://datadrivendecisions.github.io/ai-in-business/tool-bias-experiment.html?instructor#owner=$(gcloud secrets versions access latest --secret experiment-owner-token --project ai-in-business-507819)"
      ```

      Opening the bookmark is all it takes on Monday: the results appear and refresh every five
      seconds, with nothing to paste or type. The page removes the credential from the address bar
      as soon as it loads, so it is not on the projector. **The link is the key.** Anyone who has it
      sees the live results, so do not paste it in a chat or share the bookmark.

---

## The block — 150 minutes

The clock is relative to the start of the block. The week-3 session plan places it in the day
(see *For the session plan* at the end).

### 0:00–0:10 — Opening

**Room lecturer.** Say:

- This is a class exercise about how people look for evidence. You will each work alone.
- It has no grade consequence, either way.
- You can stop at any point. The page has a button that erases everything.
- Choose a code word, not your name, and **write it down**. It is the only way to have your
  data removed later.
- Enter your team number. It decides the order of two things; nothing else.
- Work in silence. Do not talk about the sources with anyone until we debrief. Your neighbour
  may be seeing the same cards in a different order.

**Do not say** what is measured, that the sources were chosen with care, what the assistant step
is for, or what anyone expects to happen. If asked, say: *"I'll explain all of it afterwards. I
promise."*

Put the page address on the projector. Nothing else.

### 0:10–0:45 — Two rounds, alone

Each student:

1. Reads a claim, picks a side, and writes one sentence on why. That sentence is then locked.
2. In one of the two rounds, puts that position to their own assistant with the prompt the page
   gives, and pastes back the reply.
3. Sees 16 sources one at a time and may open 8. A source they skip does not come back.
4. Writes a final position, then answers eight short questions about how the round felt.

After round 1 the page waits on a bridge screen: *"Wait here if your lecturer has asked you
to."* You do not need to hold anyone there. The rounds are individual.

**Both lecturers walk the room.** Help with the page only. If a student asks what a source means,
or whether their position is right, say *"Whatever you think it means"* and move on. The gates work
the same way.

**Data lecturer.** In live mode, open your owners' link. The results start filling in by
themselves. Keep your screen to yourself.

### 0:45–0:50 — Hand in

- **Live:** students press *Submit my numbers*. The data lecturer watches the count rise to the
  number of people in the room.
- **By hand:** students copy their result line and send it **in a private chat message to the data
  lecturer**, never in the team channel. Every student would then see every line, and the debrief
  depends on them not having compared.

A student who sees an error on the submit screen copies the line and sends it by hand. The page is
built for that; nothing is lost.

### 0:50–1:00 — The team prediction, sealed

Teams now talk for the first time. Each team writes, on one sheet:

1. What do you think the assistant step changed, if anything?
2. Which number would show it?
3. What result would show you were wrong?

**Room lecturer.** Before they write, put one number on the projector: **with 32 people, this
comparison can only detect a difference of about half a standard deviation** (d_z ≈ 0.51 at 80%
power; with 8 it would be 1.16). Say that a smaller real effect could be there and not show.
Naming the limits before the result is seen is what separates an experiment from a demonstration
dressed as one.

Collect or photograph the sheets. They come back at 1:25.

### 1:00–1:10 — Break

**Data lecturer.** In live mode, the count should match the number of people present. A higher
count usually means someone submitted twice under two codes. In by-hand mode, paste the lines and
press *Work it out*. Either way: read the *Rejected, and why* list and chase anyone missing. Do not
project yet.

### 1:10–1:25 — The reveal

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

### 1:25–1:50 — The result

Open the owners' link on the projected laptop and scroll to the comparison. Keep the *Do it by
hand* fold-out closed: if a codebook was pasted into it, that is the answer key.

Show the two bars, the interval and the detectable effect. The page puts a question where a
conclusion would go, and one sentence that says what the interval allows. Read both out. Then hand
the teams back their prediction sheets and ask each one:

- *Which of your three answers does this bear on?*
- *Would you have written the same thing if you had seen this first?*

Then point at the rows for workload and *how the round felt*, with and without the assistant. In
three earlier studies, decades apart, the version with dissent built in gave better decisions **and
felt worse**. Ask whether this room shows the same. **Do not tell them.** If the numbers do not
show it, that is also an answer, and with 32 people a likely one.

The same rule as every week: ask, never comment. No "good", no "exactly".

### 1:50–2:05 — Audit the instrument: the students' kappa

Every student's number rests on someone deciding, card by card, whether a source agrees. So now
they check that judgement.

1. Hand out the debrief set: one sheet per pair.
2. Each student codes the 8 cards alone: supports or opposes the claim.
3. The pair fills in the 2×2 together.
4. The room lecturer types two or three pairs' 2×2 into the *Kappa, for the debrief* box on the
   projector and reads out agreement, chance agreement and kappa.
5. Put the owners' kappa beside theirs, if the coders are done (pilot audit, CL-5).

Ask: *where you disagreed, was the card unclear, or the rule?*

### 2:05–2:10 — The connection, and only now

AI tools that grade are often sold on "over 80% agreement with humans". A percentage flatters.
Converted to kappa, that figure is usually about 0.4, which the usual bands call *fair*: too weak
to rest a finding on. Ask the room what they would now ask of such a claim.

The order is the lesson. It only lands because they have just seen their own agreement shrink. Do
not move this earlier.

### 2:10–2:25 — The verdict assistant: a demonstration

This shows the second kind of assistant, the one that gives a verdict instead of asking. **Say
first that it is a demonstration, not a result.** One run proves nothing. Treating it as proof is the
mistake the session has just taught against.

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

### 2:25–2:30 — Close

- **What this cannot show.** Name them quickly: too few people for a small effect; nobody was
  blind to which round had the assistant; round 1 cannot be unlearned in round 2; students in a
  team share a context; one room, one task, so nothing generalises.
- Withdrawal by code until 19:00. Then everything is deleted.
- Hand over to the next part of the session. The agents segment follows directly: its card s5
  uses the assistant round as its example.

---

## When something goes wrong

| What happens | What to do |
|---|---|
| A student cannot reach any assistant | The data lecturer runs the page's prompt in their own assistant and gives the student the reply to paste. The step still reaches that student's own position. |
| A student reloaded or closed the tab | Reopen the same page in the same browser. The page keeps their place. A private window loses it when the window closes. |
| A student entered the wrong team number | Let them carry on. The line records which round had the assistant, so the data stays usable. |
| Submitting fails | The page shows the line and says what to do. The student copies it and sends it by private message. |
| The count on the dashboard is higher than the room | Someone used two codes. Each code counts once (the last submission wins), but two codes look like two people. Ask the room. |
| The dashboard says the service refused the credential | Make the owners' link again (see *Before Monday*). Until then, use the paste box under *Do it by hand*. |
| The service is down | The dashboard gives up after five failed attempts and says so. Switch to by hand. This is the ten minutes ADR-0016 accepted as the fallback. |
| A student wants out mid-session | They stop. The *erase* button removes everything from their browser. |
| A student wants their row deleted after submitting | See *Deleting one student's row* below. |

---

## After the session, before 19:00

The service deletes everything at 19:00 (Amsterdam time). What you want to keep, you copy before then.

1. **Copy the comparison table** from the instructor view: both means, the difference, the
   interval, the detectable effect, and the feel rows. Only the aggregates, not rows or codes. Put
   it in the decision log (`course-outline.md`).
2. **Copy the pilot audit table** into build plan phase 0, subtask 0.3: every verdict with its
   figures. This session was the pilot, so phase 0 closes on this table. A claim that misses CL-1
   or CL-10 is replaced before the next run, and this run's result is reported with the miss
   beside it.
3. **Delete any rows students asked to withdraw** (next section).
4. **Press *Stop watching*** and close the tab. Stop makes the tab forget the owners' link; so
   does closing it.

### Deleting one student's row

The owners' route `/delete` takes a code and removes that student's row
([`experiment_service/README.md`](../experiment_service/README.md), *The routes*). Send a `POST`
to `<service address>/delete` with the JSON body `{"code": "<their code>"}` and the owners'
credential in an `Authorization: Bearer …` header. It answers with how many rows it removed.

In by-hand mode there is nothing on a server. Remove the student's line from the paste box and
work it out again.

---

## For the session plan

`session-plan-week-03.md` does not exist yet. Whoever writes it places this block, and needs four
things from it:

- **The block comes first in the day.** Nothing that teaches counter-cases, devil's advocacy or
  agents can run before the two rounds are finished. Each one is a treatment.
- **The agents segment follows the debrief directly** (week-3 instructor notes, card s2).
- **Issue #12 asks the session plan to name every AIBS/AEL handover.** This block has one: the
  assistant round goes from the debrief into the agents segment's card s5. It happens at 2:30.
- **The two roles** above need two people for the whole 150 minutes.
