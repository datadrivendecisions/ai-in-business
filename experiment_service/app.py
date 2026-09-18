"""The experiment service: two routes for the tool, two for its owners.

ADR-0016 gave up the site's static property for exactly one page, and every
choice here exists to keep that exception as narrow as it was argued to be.

    POST /submit      the tool, once, on a button press        anonymous
    GET  /dashboard   the tool's instructor view, polling      owners
    POST /delete      a student changed their mind             owners
    POST /purge       the end of the teaching day              owners, or the scheduler
    GET  /health      Cloud Run wants one                      anonymous

There is no route that takes a code and returns a row. /delete takes a code
and returns a count, which is the one direction ADR-0016 allows.

The service never interprets. It cannot: the congeniality index is a
function of the codebook, and SM-8 keeps the codebook out of anything that
ships. So /dashboard returns the numbers a session produced and the page
that already holds the arithmetic does the rest. That is narrower than the
blueprint's part table imagined, and it is not a shortcut -- a service that
aggregated would need the answer key, which is the one thing nothing in this
build is allowed to hold in public.

WSGI, standard library only. The one dependency in the container is the
Firestore client, and store.py imports it lazily so every route here can be
driven with python3 and nothing installed.
"""

import hmac
import json
import os
import time

from schema import Rejected, clean_submission
from store import MemoryStore

# The tool calls one host. The service answers one origin.
DEFAULT_ORIGINS = ("https://datadrivendecisions.github.io",)

# A student's laptop should manage one submission and a handful of retries.
RATE_LIMIT = 30          # requests
RATE_WINDOW = 60.0       # seconds


def _json(status, payload, origin=None, extra=None):
    # A 204 carries no body, and says nothing about one. The local server
    # passed "204 with {}" through; Cloud Run's front end answers it with a
    # 502 -- which, on the CORS preflight, failed every student's submit
    # before it was sent.
    if status == 204:
        body = b""
        headers = [("Cache-Control", "no-store"), ("X-Content-Type-Options", "nosniff")]
    else:
        body = json.dumps(payload).encode("utf-8")
        headers = [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-store"),
            ("X-Content-Type-Options", "nosniff"),
        ]
    if origin:
        headers += [
            ("Access-Control-Allow-Origin", origin),
            ("Vary", "Origin"),
            ("Access-Control-Allow-Headers", "Content-Type, Authorization"),
            ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
            ("Access-Control-Max-Age", "600"),
        ]
    return status, headers + list(extra or []), body


class App:
    def __init__(self, store=None, owner_token=None, origins=None, clock=time.time,
                 purge_token=None, codebook=None):
        self.store = store if store is not None else MemoryStore()
        # The answer key: which card sits in which cell. It may not be in the
        # published page (SM-8), and pasting it into the instructor view at the
        # start of a session was one step too many for the person running the
        # room. So it lives beside the owners' token, in Secret Manager, and
        # leaves this service only inside an owner-authenticated dashboard
        # response -- never to a student, never from any other route.
        self.codebook = codebook if codebook is not None else os.environ.get("CODEBOOK", "")
        self.owner_token = owner_token if owner_token is not None else os.environ.get("OWNER_TOKEN", "")
        self.purge_token = purge_token if purge_token is not None else os.environ.get("PURGE_TOKEN", "")
        env_origins = os.environ.get("ALLOWED_ORIGINS", "")
        self.origins = tuple(origins if origins is not None else
                             ([o.strip() for o in env_origins.split(",") if o.strip()]
                              or DEFAULT_ORIGINS))
        self.clock = clock
        self._hits = {}

    # ---------------------------------------------------------------- auth --

    def _is_owner(self, environ):
        """A bearer token, compared in constant time.

        Cloud Run's own IAM would be stronger and cannot be used: the
        dashboard is read by a browser inside the tool page, and a plain
        browser cannot present an identity token. IAP in front of a load
        balancer is the upgrade if this outlives one afternoon; it is a lot
        of machinery for a service that holds one day of pseudonymous
        numbers. Written down in the README rather than left implied.
        """
        if not self.owner_token:
            return False
        header = environ.get("HTTP_AUTHORIZATION", "")
        if not header.startswith("Bearer "):
            return False
        return hmac.compare_digest(header[7:], self.owner_token)

    def _is_scheduler(self, environ):
        if not self.purge_token:
            return False
        header = environ.get("HTTP_AUTHORIZATION", "")
        if not header.startswith("Bearer "):
            return False
        return hmac.compare_digest(header[7:], self.purge_token)

    def _origin(self, environ):
        sent = environ.get("HTTP_ORIGIN")
        return sent if sent in self.origins else None

    def _rate_limited(self, environ):
        now = self.clock()
        who = environ.get("HTTP_X_FORWARDED_FOR", environ.get("REMOTE_ADDR", "?")).split(",")[0].strip()
        hits = [t for t in self._hits.get(who, ()) if now - t < RATE_WINDOW]
        hits.append(now)
        self._hits[who] = hits
        if len(self._hits) > 5000:            # a teaching room, not a botnet
            self._hits = {who: hits}
        return len(hits) > RATE_LIMIT

    # -------------------------------------------------------------- routes --

    def submit(self, environ, body, origin):
        if self._rate_limited(environ):
            return _json(429, {"error": "too many requests"}, origin)
        try:
            payload = json.loads(body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return _json(400, {"error": "the body is not JSON"}, origin)
        try:
            submission = clean_submission(payload)
        except Rejected as why:
            return _json(400, {"error": str(why)}, origin)
        doc = self.store.put(submission, now=self.clock())
        return _json(200, {"stored": True, "at": doc["at"],
                           "count": len(self.store.rows(now=self.clock()))}, origin)

    def dashboard(self, environ, origin):
        if not self._is_owner(environ):
            return _json(401, {"error": "this route is for the module owners"}, origin,
                         [("WWW-Authenticate", "Bearer")])
        rows = self.store.rows(now=self.clock())
        return _json(200, {"count": len(rows), "rows": rows,
                           "codebook": self.codebook or None,
                           "servedAt": self.clock()}, origin)

    def delete(self, environ, body, origin):
        if not self._is_owner(environ):
            return _json(401, {"error": "this route is for the module owners"}, origin,
                         [("WWW-Authenticate", "Bearer")])
        try:
            code = json.loads(body.decode("utf-8")).get("code")
        except (ValueError, UnicodeDecodeError, AttributeError):
            return _json(400, {"error": "the body is not JSON"}, origin)
        if not isinstance(code, str) or not code:
            return _json(400, {"error": "give a code to delete"}, origin)
        removed = self.store.delete(code)
        return _json(200, {"removed": removed,
                           "count": len(self.store.rows(now=self.clock()))}, origin)

    def purge(self, environ, origin):
        """The end of the teaching day, by the scheduler or by an owner.

        Cloud Scheduler sets X-CloudScheduler: true on its requests, and an
        earlier draft of this route accepted that as proof of who was calling.
        It is not proof of anything -- it is a header, and any caller can send
        it, so that draft let a student wipe the room's data mid-session with
        one curl. The scheduler carries its own bearer token in a custom
        header instead, kept apart from the owners' so that a job
        configuration and a person's credential are not the same secret.
        """
        if not (self._is_owner(environ) or self._is_scheduler(environ)):
            return _json(401, {"error": "this route is for the module owners"}, origin,
                         [("WWW-Authenticate", "Bearer")])
        return _json(200, {"removed": self.store.purge()}, origin)

    # ----------------------------------------------------------------- wsgi --

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "/").rstrip("/") or "/"
        method = environ.get("REQUEST_METHOD", "GET").upper()
        origin = self._origin(environ)

        if method == "OPTIONS":
            status, headers, body = _json(204, {}, origin)
        elif path == "/health" and method == "GET":
            status, headers, body = _json(200, {"ok": True}, origin)
        elif path == "/submit" and method == "POST":
            status, headers, body = self.submit(environ, _read(environ), origin)
        elif path == "/dashboard" and method == "GET":
            status, headers, body = self.dashboard(environ, origin)
        elif path == "/delete" and method == "POST":
            status, headers, body = self.delete(environ, _read(environ), origin)
        elif path == "/purge" and method == "POST":
            status, headers, body = self.purge(environ, origin)
        else:
            status, headers, body = _json(404, {"error": "no such route"}, origin)

        start_response("%d %s" % (status, _REASON.get(status, "Status")), headers)
        return [body]


_REASON = {200: "OK", 204: "No Content", 400: "Bad Request", 401: "Unauthorized",
           404: "Not Found", 413: "Payload Too Large", 429: "Too Many Requests"}

MAX_BODY = 16 * 1024


def _read(environ):
    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        return b""
    return environ["wsgi.input"].read(min(length, MAX_BODY)) if length > 0 else b""


def build():
    """The application Cloud Run runs."""
    salt = os.environ.get("ID_SALT", "")
    if os.environ.get("FIRESTORE_PROJECT"):
        from store import FirestoreStore
        return App(store=FirestoreStore(salt=salt))
    return App(store=MemoryStore(salt=salt or "local"))
