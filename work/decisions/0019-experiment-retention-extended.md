# ADR-0019: How long the week 3 experiment's data is kept, once the debrief leaves week 4

## Status

Accepted

## Context

[ADR-0017](0017-experiment-as-homework.md) made the week 3 experiment individual
homework and set its retention to the exercise: submissions are deleted on the
evening of the week 4 debrief, 28 September 2026 at 19:00. The page says so to
every student before they press the button, and three mechanisms enforce it — a
scheduled purge, a Firestore TTL on each row's `expiresAt`, and a read that drops
anything past its expiry.

The week 4 session has since become a mini-CBI, and the debrief is no longer in
it. The module owners have decided to hold the debrief later, without fixing its
date yet. Left alone, the purge would run on the evening of 28 September and
delete the data before it is ever shown, which would make the exercise pointless
for everyone who did it.

ADR-0017 foresaw this and said what it requires: *nothing here licenses keeping
data beyond the debrief it was collected for*, and a longer window is a new
record, not an extension of that one. This is that record.

When it was taken, four rows had been sent.

## Options considered

**Let the purge run on 28 September.** Keeps the promise to the letter and
destroys the data the promise was made about. The debrief would have nothing to
show.

**Postpone with no end date, and delete when the debrief has happened.** What
the owners first asked for. The service cannot express it: an empty
`RETENTION_UNTIL` falls back to one day per row, which is shorter, not longer.
And a student who agreed to one date would now be holding data open against no
date at all.

**Postpone to a fixed latest date, with the debrief free to fall before it.**
The owners choose the debrief date when they are ready; the data goes after the
debrief and never later than the stated day. The student sees one date again,
later than the one they agreed to, and can still withdraw by code.

## Decision

**The week 3 experiment's data is kept until after the debrief, and deleted by
19:00 on Saturday 31 October 2026 at the latest.** A reminder at the end of
October prompts the owners to hold the debrief, or to let the purge run.

1. **All three mechanisms move together.** The scheduled purge fires at 19:00 on
   31 October (Amsterdam time, `+01:00` after the clocks change), the service's
   `RETENTION_UNTIL` is `2026-10-31T19:00:00+01:00`, and every row already sent
   has its `expiresAt` moved to the same instant. Moving one without the others
   would leave the TTL to delete the rows on the old date.
2. **The pages say the new date.** The tool, the week 3 page and the landing page
   say "after the debrief, and by 31 October 2026 at the latest". The week 4 page
   says the debrief has moved and that its date will be announced.
3. **Withdrawal stays as it was.** A student gives their code to a lecturer and
   their row goes, at any point before the purge.
4. **The debrief can come sooner and the data goes with it.** If the debrief is
   held before 31 October, the owners run the purge that evening by hand rather
   than wait for the deadline.

Everything else in ADR-0017 stands: the run is individual and asynchronous, the
four held-back topics move with the run, and the collection keeps the shape
ADR-0016 gave it.

## Consequences

- **A promise was changed after students relied on it.** The four students who
  had submitted agreed to 28 September. The changed pages tell anyone who comes
  back, but only a message tells them for certain; the owners should say it in
  the course channel, with the reminder that a code removes a row.
- **The window is five weeks instead of eight days.** Withdrawal is easier to
  honour in that time and harder to bound; a student who forgets their code has
  longer to live with a row they cannot find.
- **The priming ADR-0017 warned about gets worse.** Students who run the exercise
  after week 4 have met the mini-CBI and more of the course. The debrief should
  name the date each row arrived, or at least the split before and after
  28 September.
- **The debrief is now an obligation with a deadline.** If it has not been held
  by 31 October, the data is deleted anyway, and the exercise ends without its
  debrief.
- **The deploy script's default is this cohort's date.** The next cohort sets
  its own, as the script already asks.

## Related

- [ADR-0017](0017-experiment-as-homework.md) — superseded by this record for
  retention only; everything else in it stands.
- [ADR-0016](0016-experiment-service.md) — the collection's shape, unchanged.
