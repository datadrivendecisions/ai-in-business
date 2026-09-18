# The week 3 experiment service

Two routes for the tool, two for its owners, and one collection that is
empty by the next morning. It exists because [ADR-0016](../work/decisions/0016-experiment-service.md)
decided that thirty-two students pasting result lines costs ten minutes at
the moment the room's attention peaks, and that the live dashboard *is* the
lesson rather than a convenience.

It is not published. Only `site/` is uploaded to GitHub Pages; this is a
container that runs somewhere else.

## What it holds, and for how long

Counts, timings, scale scores, which card ids were opened, a team number and
a self-chosen code. **Nothing a student wrote.** Their two position
sentences and whatever their assistant replied stay in the browser and are
never transmitted — not stripped on arrival, but never sent, because
[`schema.py`](schema.py) refuses a payload carrying any field it does not
name. The day someone adds a sentence to the tool's payload, the service
rejects the submission instead of storing it.

Retention is the teaching day, enforced three times over:

| Mechanism | Catches |
|---|---|
| `POST /purge`, on a 19:00 schedule | the ordinary case |
| a Firestore TTL policy on `expiresAt` | the night the scheduler does not fire |
| every read drops an expired row before returning it | the hours between the two |

A retention rule resting on one cron job is an intention. This is three
independent mechanisms, and the cheapest of them cannot be skipped.

## The routes

| | | |
|---|---|---|
| `POST /submit` | the tool, once, on a button press | anonymous |
| `GET /dashboard` | the tool's instructor view, polling | owners |
| `POST /delete` | a student changed their mind | owners |
| `POST /purge` | the end of the day | the scheduler, or owners |
| `GET /health` | Cloud Run wants one | anonymous |

There is **no route that takes a code and returns a row.** `/delete` takes a
code and returns a count, which is the one direction ADR-0016 allows. And
`/dashboard` never returns a code either: each row carries a salted hash of
it instead, so two submissions from one person are still visibly one person
while nobody reading the response learns who. That is narrower than the
record requires and costs one line.

**The service never interprets.** It cannot. The congeniality index is a
function of the codebook, and `SM-8` keeps the codebook out of anything
published, so the arithmetic lives in the page where the owner pastes it.
The blueprint's part table says the service "aggregates on request"; it
does not, and [blueprint §5](../project-documentation/build/information-seeking-experiment/blueprint.html)
now says why.

## Running it here

No package manager, no container, nothing installed:

```bash
OWNER_TOKEN=local-owner-token PURGE_TOKEN=local-purge-token \
ALLOWED_ORIGINS=http://localhost:8765 ID_SALT=local \
  python3 server.py                      # http://localhost:8080
```

With no `FIRESTORE_PROJECT` set it keeps submissions in memory, which is
what you want on a laptop and never what you want in a room.

Then serve the site beside it and point the tool at it — one line in
`site/tool-bias-experiment.html`:

```js
var SERVICE = { origin: "http://localhost:8080", ... };
```

The gate that proves the routes is `check-service.py`, beside the build
plan. It drives every route through WSGI, so it needs no port, no container
and no cloud project, and it injects the clock so the "nothing survives the
teaching day" check fast-forwards a day rather than waiting one.

```bash
python3 ../project-documentation/build/information-seeking-experiment/check-service.py
```

## Deploying it

```bash
PROJECT=your-course-project ./deploy.sh
```

Read it first. It enables APIs, creates a Firestore database, mints three
secrets, binds a service account to one collection, deploys a container,
creates a scheduler job and sets a TTL policy. All of that costs money and
holds student data.

**Nothing in this repository has run it.** The service is written and
tested; it has never been deployed, and `SERVICE.origin` in the tool ships
empty, so the published page makes no request at all until someone puts a
URL there.

### Why a bearer token and not IAM

Cloud Run's own IAM is stronger and cannot be used here: the dashboard is
read by a browser inside the tool page, and a plain browser cannot present
an identity token. IAP in front of a load balancer is the proper upgrade
and is a great deal of machinery for a service that holds one day of
pseudonymous numbers. The token is compared in constant time, lives in
Secret Manager, and is separate from the scheduler's.

If this outlives one afternoon, that is the thing to change first.

## Four secrets, and why four

| | |
|---|---|
| `experiment-owner-token` | the dashboard and the delete route |
| `experiment-purge-token` | the purge, and nothing else |
| `experiment-id-salt` | makes the dashboard's opaque ids unguessable |
| `experiment-codebook` | the answer key, handed to the owners' dashboard and nowhere else |

The purge has its own token so that a scheduler job configuration and a
person's credential are never the same string. The salt matters more than it
looks: without one, anyone who could read the dashboard could hash `kite`
and find that row, and the hash would have bought nothing.

The codebook is here so that the person running the room pastes nothing. It
may not be in the published page (SM-8), so it lives beside the owners'
credential and leaves the service only inside the owner-authenticated
`/dashboard` response (SV-13). `deploy.sh` builds it from
`work/drafts/week-03-codebook.md` — the 32 card-to-cell pairs, none of the
file's prose — and adds a new version only when the file has changed. The
service still computes nothing from it; the page does.

An earlier draft of `/purge` accepted the `X-CloudScheduler: true` header as
proof of who was calling. That header is not proof of anything — any caller
can send it — and the draft let a student wipe the room's data mid-session
with one `curl`. It is written down here because the mistake is an easy one
and the check that catches it is now in `check-service.py`.
