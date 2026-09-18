# Phases 6–8: what I decided on your behalf, and what is still yours

Written for the two module owners. Phases 6, 7 and 8 of
`project-documentation/build/information-seeking-experiment/buildplan.html` are built, checked
and pushed on `week-03-decks-and-position-controls`. Six things needed a decision that the
blueprint, the build plan and ADR-0016 did not settle. I made each one, built on it, and wrote
it down here rather than stopping. **Every one of them is reversible**, and the cost of
reversing is noted.

> **Confirmed, 18 September 2026.** The owners confirmed all six decisions below as they stand.
> On the same day they accepted ADR-0016 and made a seventh decision, recorded at the end:
> the first session is the pilot.

---

## 1. The service lives in this repository, not its own

The build plan said *"the service repository"*. It is `experiment_service/` here instead — a
top-level directory, outside `site/`, so nothing about it is published.

SV-11 asks for **two deployments and no shared container**, and that is satisfied: it is its own
image and its own Cloud Run service, and a bad deploy of it cannot touch the Socratic gate.
Keeping it here keeps the code beside the ADR, the blueprint and the build plan that govern it,
which is the same reasoning `CLAUDE.md` gives for `socratic_agent/`.

*To reverse:* `git mv` the directory into a new repo. Nothing in `site/` references it by path.

## 2. The dashboard is a panel in the tool's instructor view

Not a page of its own. `GET /dashboard` returns the stored rows; the panel polls it and hands
them to the arithmetic that was already there.

This was worth more than tidiness. It makes the gate's *"dashboard arithmetic matches phase 5's"*
true **by construction** — there is one implementation, not two that agree. A separate dashboard
would have had to reimplement the interval, the detectable effect and the pairing, and then be
checked against the first one for ever.

*To reverse:* costly. The second implementation is the expensive part, not the page.

## 3. Owner authentication is a bearer token, not IAM

Cloud Run's own IAM is stronger and cannot be used: the dashboard is read by a browser inside the
tool page, and a plain browser cannot present an identity token. IAP in front of a load balancer
is the proper answer and is a great deal of machinery for a service that holds one day of
pseudonymous numbers.

The token is compared in constant time and lives in Secret Manager. There are **three** secrets,
not one: the owners' token, a separate token for the scheduler's purge (so a job configuration
and a person's credential are never the same string), and a salt.

**If this outlives one afternoon, IAP is the first thing to change.** It is written down in
`experiment_service/README.md` so the next person does not have to rediscover it.

## 4. The service does not aggregate — and the blueprint was wrong about this

The blueprint had the service *"aggregate on request"*. It cannot. Every figure rests on the
congeniality index, the index rests on the codebook, and SM-8 keeps the codebook out of anything
published. A service that aggregated would hold the answer key in the cloud, for the one page
whose whole design is that the answer key is not in it.

**I changed the blueprint to 0.3** rather than leaving the two documents disagreeing, with an
aside in §5 in the same style as the existing one about the result line. If you would rather the
blueprint had stayed as it was and the code carried the exception, say so and I will revert the
document — but then the two disagree, and the build plan says the blueprint is the intent.

## 5. `SERVICE.origin` ships empty, and that is the switch

The published page makes **no network request at all** until someone puts a URL in one line of
`site/tool-bias-experiment.html`. With it empty the consent screen says nothing leaves the
browser, the finish is the one phase 5 shipped, and a student meets exactly what they met before.

This means **the service can be deployed well before the session** without changing anything a
student sees, and the decision to switch it on is one edit you make when you are ready. It also
means that if you never deploy it, nothing on the site is a lie.

The consent screen has two statements and picks between them on that switch. Both are under
DA-5's sixty words.

## 6. Three interpretation sentences, not four

I wrote four and deleted one. The fourth was for an interval *narrower* than the smallest
difference the sample could detect, and **that cannot happen at any sample size**: a 95% interval
runs about 1.4 times the width of an 80%-power detectable effect — 1.52 at n = 3, 1.41 at 32,
1.40 at 2000 — because both are fixed multiples of the same standard error.

This is worth ten minutes of the debrief. When the room sees an interval wider than the effect
the session could have caught, the natural reading is *we did this badly*. It is arithmetic. The
spanning sentence now says so, and a check sweeps sixteen sample sizes to insist every stored
sentence is reachable by some real summary.

---

## What I did not do, and why

**I did not deploy anything.** `experiment_service/deploy.sh` is one command
(`PROJECT=… ./deploy.sh`) and it enables APIs, creates a Firestore database, mints three secrets,
binds a service account, deploys a container, creates a scheduler job and sets a TTL policy. All
of that costs money on a project this build does not own. Read it before you run it.

**I did not tick any gate a human has to perform.** Left open across the three phases:

| Phase | Open, and it needs a person |
|---|---|
| 6 | The phone. `PR-2` and `PR-4` are verified by demonstration; I measured a 400 px viewport in Chrome and screened the markup for trap patterns, which is not a phone in a hand or a finger on Tab. |
| 7 | The tester walk, and `SV-5` against a real deployment rather than a laptop. `SV-11` cannot be ticked at all: only one of the two services exists, and neither is deployed. |
| 8 | The walk from two machines. |
| 5 | Still open from before: `AN-3`, that nothing on the results screen states a finding, **inspected by someone who did not write it**. There is more on that screen now than there was, so this one is worth more than it was. |

**Phase 0 was untouched and it was the risk.** *(Answered on 18 September 2026 by decision 7 below.)* The pilot (0.2–0.4), the two-coder kappa (0.8–0.9)
and the eight-card debrief set (0.11) are all still open, and none of them can be done from a
desk. Everything above assumes two claims that divide a room, and **nobody has yet checked that
either of them does**. The tool's own notice on the page now says *Not piloted* rather than *Not
finished*, because that is the honest summary.

## One bug of mine worth knowing about

The first draft of `POST /purge` accepted the header `X-CloudScheduler: true` as proof of who was
calling. That header is not proof of anything — any caller can send it — and the draft let a
student wipe the room's data mid-session with one `curl`. The scheduler has its own bearer token
now, and the spoof is a check in `check-service.py`. It is in the README too, because it is an
easy mistake and the next person deserves the warning rather than the silence.

---

## 7. The first session is the pilot — decided by the owners, 18 September 2026

There is no separate hands-up pilot before the session. The sides students lock before reading
anything are the pilot's split (`CL-1`, `CL-7`), and the tool now records how many seconds each
student took to choose a side (`CL-10`). The lecturer view has a **pilot audit** that reports each of
these, and the two coders' agreement (`CL-5`), as *met*, *not met* or *not yet measurable*, with a
tally. Phase 0 closes on what that audit says after the session.

What this changed in the build:

- **The result line is version 2.** It gained `pick`, the seconds to a side, and the submission
  gained the same field. The service refuses a version 1 payload. Nothing had been run with version 1.
- **The blueprint is version 0.4.** It gained `MS-7` (the timing) and `AN-8` (the audit), and says
  that the pilot the CL rules name is the first session.
- **Build plan subtask 0.4 is dropped.** It picked the two closest claims from a set of pilot
  survivors. The claims are fixed, so there is nothing to pick from.

**The cost:** a claim that fails is found out after the session, not before. That claim is replaced
for the next run, and this run's comparison is reported with the miss written beside it.

**Still yours, and none of it can be measured:** `CL-8` and `CL-9` before the session (build plan 0.2),
two people coding all 32 cards on their own (0.8), and the eight-card debrief set (0.11).

---

## 8. The owners open the dashboard with one link — decided by the owners, 18 September 2026

The owners asked that the person running the room see the results without pasting a codebook or
typing a credential. Two changes do that:

- **The codebook moves into Secret Manager**, beside the owners' credential. The service returns it
  inside the owner-authenticated dashboard response and in no other response (`SV-13`). This
  reverses the narrowing in decision 4: the codebook now *does* reach a server. It is still not in
  anything published, which is what `SM-8` protects, and the service still computes nothing.
- **The credential travels in a personal link**, after the `#`. That part never leaves the browser,
  so GitHub never sees it. The page removes it from the address bar before the first request and
  keeps it for that tab only (`SV-12`).

**The cost:** the link is the key. Anyone who has it sees the live results, so it is bookmarked,
not shared. Revoking it means adding a new version of `experiment-owner-token` and deploying again.

