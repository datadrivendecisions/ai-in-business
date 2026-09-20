"""Where submissions sit for a day.

Two implementations behind one interface, for a reason that is not tidiness:
the phase 7 and 8 gates have to drive the real routes, and a gate that needs
a cloud project is a gate nobody runs. MemoryStore lets every route be
exercised end to end with python3 and nothing installed. FirestoreStore is
the same interface against the collection ADR-0016 named.

Retention (SV-4) is enforced three times over, which is deliberate. The
scheduled purge is the mechanism the record names; a Firestore TTL policy on
expiresAt is the one that still runs when the scheduler does not; and every
read here drops anything past its expiry before returning, so a missed purge
cannot leak past the deadline even for the minutes before the TTL sweep
notices. A retention rule that depends on one cron job firing is an
intention, and the record was explicit that this is not one.

Since ADR-0017 the window is the exercise rather than the teaching day: the
experiment is homework, so rows arrive across a week and all die together on
the evening of the debrief they were collected for. RETENTION_UNTIL holds that
instant, and every row gets it as its expiry, so the three mechanisms and the
sentence the student read before pressing the button all name one moment. With
no deadline set -- a local run, a gate -- it falls back to a day from the write,
which is what a store with no course calendar can honestly promise.
"""

import os
import threading
import time

RETENTION_SECONDS = 24 * 60 * 60


def _retention_until():
    """The instant every row expires, from RETENTION_UNTIL, or None.

    An ISO 8601 date-time with an offset: "2026-09-28T19:00:00+02:00". A value
    that cannot be read is refused at import rather than silently ignored,
    because the failure mode of a mistyped deadline is data that outlives the
    promise made to the student who sent it.
    """
    raw = os.environ.get("RETENTION_UNTIL", "").strip()
    if not raw:
        return None
    from datetime import datetime
    try:
        when = datetime.fromisoformat(raw)
    except ValueError:
        raise SystemExit(f"RETENTION_UNTIL is not an ISO 8601 date-time: {raw!r}")
    if when.tzinfo is None:
        raise SystemExit(f"RETENTION_UNTIL needs a timezone offset: {raw!r}")
    return when.timestamp()


RETENTION_UNTIL = _retention_until()


def expiry(now):
    """When a row written at `now` dies: the fixed deadline, or a day."""
    if RETENTION_UNTIL is not None:
        return RETENTION_UNTIL
    return now + RETENTION_SECONDS


def _hash_code(code, salt):
    """A stable, opaque stand-in for the student's code.

    The dashboard needs to know that two submissions are the same person --
    last write wins, and a mismatch with the register should be visible --
    and it needs nothing else. So the code is the key here and never leaves
    in a response. This is narrower than ADR-0016 requires, and it costs one
    line: the owner deletes by the code a student gives them, and never has
    to read a list of codes to do it.
    """
    import hashlib
    return hashlib.sha256((salt + "\0" + code).encode("utf-8")).hexdigest()[:16]


class Store:
    def put(self, submission, now=None):
        raise NotImplementedError

    def rows(self, now=None):
        """Every live submission, with the code replaced by its opaque id."""
        raise NotImplementedError

    def delete(self, code):
        """-> how many rows went. The one route that takes a code (SV-5)."""
        raise NotImplementedError

    def purge(self):
        """-> how many rows went. Everything, whatever its age (SV-4)."""
        raise NotImplementedError


def public_row(doc, salt):
    """What a dashboard is allowed to see: numbers, and an opaque id."""
    return {
        "id": _hash_code(doc["code"], salt),
        "team": doc["team"],
        "at": doc["at"],
        "rounds": doc["rounds"],
    }


class MemoryStore(Store):
    """One process, one dictionary. For the gates, and for a local run."""

    def __init__(self, salt="local"):
        self._lock = threading.Lock()
        self._docs = {}
        self.salt = salt

    def put(self, submission, now=None):
        now = time.time() if now is None else now
        doc = dict(submission)
        doc["at"] = now
        doc["expiresAt"] = expiry(now)
        with self._lock:
            self._docs[submission["code"]] = doc      # last write wins
        return doc

    def _live(self, now):
        stale = [k for k, d in self._docs.items() if d["expiresAt"] <= now]
        for k in stale:
            del self._docs[k]
        return list(self._docs.values())

    def rows(self, now=None):
        now = time.time() if now is None else now
        with self._lock:
            live = self._live(now)
        return [public_row(d, self.salt) for d in sorted(live, key=lambda d: d["at"])]

    def delete(self, code):
        with self._lock:
            return 1 if self._docs.pop(code, None) is not None else 0

    def purge(self):
        with self._lock:
            n = len(self._docs)
            self._docs.clear()
            return n


def _as_time(seconds):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(seconds, tz=timezone.utc)


def _seconds(value):
    """An expiry as epoch seconds, whether it was stored as a timestamp or,
    by an older version of this file, as a number. Missing means expired."""
    if value is None:
        return 0
    if hasattr(value, "timestamp"):
        return value.timestamp()
    return float(value)


class FirestoreStore(Store):
    """submissions/, keyed by code. The import is here rather than at the top
    so the gates, and anyone reading this on a laptop, need nothing installed."""

    COLLECTION = "submissions"

    def __init__(self, salt, client=None):
        if client is None:
            from google.cloud import firestore      # noqa: F401
            # A database of its own, not the project's default. The default
            # holds the Socratic gate's owner_reports/, and ADR-0015 keeps
            # those from anything a student can reach. This service is open
            # to every browser, so its account is granted this database and
            # nothing else -- deploy.sh binds the role with that condition.
            client = firestore.Client(
                project=os.environ.get("FIRESTORE_PROJECT") or None,
                database=os.environ.get("FIRESTORE_DATABASE", "experiment"))
        self._db = client
        self.salt = salt

    def _col(self):
        return self._db.collection(self.COLLECTION)

    def put(self, submission, now=None):
        now = time.time() if now is None else now
        doc = dict(submission)
        doc["at"] = now
        # A timestamp, not a number of seconds: Firestore's TTL policy only
        # acts on a date-and-time field and silently ignores anything else,
        # so a float here would leave the second of the three retention
        # mechanisms switched on and doing nothing.
        doc["expiresAt"] = _as_time(expiry(now))
        self._col().document(submission["code"]).set(doc)
        return doc

    def rows(self, now=None):
        now = time.time() if now is None else now
        out = []
        for snap in self._col().stream():
            d = snap.to_dict()
            if _seconds(d.get("expiresAt")) <= now:
                snap.reference.delete()
                continue
            out.append(public_row(d, self.salt))
        return sorted(out, key=lambda r: r["at"])

    def delete(self, code):
        ref = self._col().document(code)
        if ref.get().exists:
            ref.delete()
            return 1
        return 0

    def purge(self):
        n = 0
        for snap in self._col().stream():
            snap.reference.delete()
            n += 1
        return n
