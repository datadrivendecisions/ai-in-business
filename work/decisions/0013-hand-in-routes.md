# ADR-0013: Where work is handed in — HANDIN, Teams, or one route per kind of artefact

## Status

Proposed

## Context

The module produces four different kinds of artefact every week and has never
said where any of them goes. The week-2 page carries the gap as a visible
placeholder — *exact location to be filled in here*, twice — and the placeholder
cannot survive publication, because a hand-in with no address is not an
assignment.

The four kinds are genuinely different, and that is the whole difficulty:

- **The team's weekly handbook page.** Public by design. It is published to the
  shared site, and under ADR-0006 the team's own platform is what publishes it.
- **The individual portfolio.** Carries 30 % of each module's mark (ADR-0011),
  is written by one student about their own contribution, and is read by both
  lecturers at the end of the run.
- **Gate traffic.** One Socratic submission per team per week, and the partner
  team's peer review. Neither is scored, both must reach a specific reader
  quickly, and what matters is that the exchange happened and was answered.
- **Field research material.** Interview recordings, transcripts, quotes, names,
  signed consent. Personal data, under GDPR, belonging to people who agreed to
  talk to a student — and the one category here that must never become public.

Two candidate homes are available: **HANDIN**, the institution's submission
system, and **Teams**, where the cohort already talks. The temptation is to pick
one and put everything in it. Everything in HANDIN turns weekly informal feedback
into a formal submission, which is exactly what the gate design says not to do.
Everything in Teams leaves the one marked artefact in a chat tool, where it is
not archived as an examination record, and puts personal data one careless
channel invite away from the wrong audience.

What breaks if this stays undecided: the week-2 page cannot be published,
students hand in nowhere, and the first field interviews — which open in the same
week — happen before anyone has said where the transcript may live.

## Options considered

**Everything through HANDIN.** One address, unambiguous, and every artefact
archived as an examination record. It makes each weekly gate a formal submission,
which the design deliberately refuses: feedback that arrives through the marking
channel is read as a verdict no matter how often it is called informational. It
also cannot host the published page, whose whole point is to be public.

**Everything through Teams.** Matches how the cohort already works, fast, and
threads keep the exchange next to the work. But the portfolio carries 30 % of a
mark, and a marked artefact in a chat tool has no reliable timestamp, no archive
the examination board can be pointed at, and no route for the checks an
institution expects of a graded submission. Personal data in a channel is
retained and shared according to the channel's membership, which changes.

**A mix decided artefact by artefact, as it comes up.** What is happening now.
It produces exactly the placeholders the week pages are carrying, and the answer
comes out different each week depending on who was asked.

**A mix decided by one rule, stated once.** Route each artefact by what it *is*
rather than by which system is nearest: what is marked, what is published, what
is conversation, what is personal data. Costs students two systems to learn, and
costs the teaching team the discipline of saying the rule every time a new
artefact appears.

## Decision

**Four routes, one rule: an artefact is handed in where its own nature requires,
and the rule is stated on every week page rather than remembered.**

1. **The individual portfolio goes to HANDIN**, once, at the end of the run. It
   is the only marked hand-in in the module, and it goes where marked work is
   archived, timestamped and attributable to one student. A student's mark for
   30 % of the module should never rest on a file in a chat thread.
2. **The team's weekly handbook page is handed in by being published.**
   Publication *is* the submission: the page on the shared site, produced by the
   team's own platform, with the repository's history as its timestamp. There is
   no second upload anywhere, and asking for one would say that publishing is
   not really the deliverable.
3. **Gate traffic runs in Teams**, in the team's own channel: the Socratic
   submission and the report that comes back, the partner team's review and the
   answer to it. It stays out of the marking system on purpose — an unscored gate
   that arrives through the graded channel stops being unscored in the only place
   that matters, which is how a student reads it.
4. **Field research material stays inside the institution's tenant** — Teams and
   the storage behind it — and goes nowhere else. Never the public repository,
   never the published site, never a consumer AI tool on a free tier. Signed
   consent is stored with the material it covers. This is the one route that is
   a rule about *where data may not go* rather than about where work is sent.

The consolidated handbook at the end of the run is published like every other
page, and **one archival copy per team goes to HANDIN** alongside the
portfolios, because it is the evidence base the interview is conducted against
and the examination record should not depend on a site that will be rebuilt next
year.

The rule that generates all five lines, and that should be said to students in
one sentence: **marked work goes where marks are kept; published work is handed
in by being published; conversation stays where conversation happens; and
personal data does not leave the institution.**

## Consequences

- **Students learn two systems, and will get it wrong at least once.** The week
  page must carry the routes explicitly, every week, in the hand-in block — not
  once in week 1 on the assumption that it was read.
- **The portfolio's weekly rhythm has no weekly submission.** ADR-0011 makes it
  continuous by construction, but under this decision nothing checks in weekly.
  Either the teaching team asks to see portfolios in the session, or the
  "continuous" claim rests entirely on the student's own discipline and is tested
  for the first time when it is marked.
- **Publication as hand-in has no grace period.** A page that is late is publicly
  late, and a team whose platform breaks cannot hand in at all. A manual fallback
  route for publishing must exist and be known before it is needed — which is
  consistent with the standing rule that every automated step keeps a manual one.
- **HANDIN assignments must exist before the cohort needs them**, configured for
  an individual submission per student plus one team archival copy. This is
  administrative work with a deadline earlier than it looks.
- **The public repository becomes a place students must think about.** Everything
  in it is world-readable; the field-research rule above is what stands between a
  student's convenience and an interviewee's name in a public commit. It has to
  be said out loud in the session where field visits open, not only written here.
- **Consent and retention now have an owner-shaped hole.** This record says where
  interview material lives; it does not say who deletes it, or when. That is a
  further decision, and it is due before the first interview rather than after
  the run.
- **Two systems means two places to look when something is missing**, and at
  eight to ten teams the teaching team will spend real time reconciling them. A
  single index — which team published what, and where — is worth keeping from
  week 1.
