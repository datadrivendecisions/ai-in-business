#!/usr/bin/env python3
"""Phase 7 and 8, the server half. Every route driven end to end.

SV-1   the submission carries no free text
SV-3   no route returns one student's row
SV-4   nothing survives the teaching day
SV-5   a student's row goes on request, by their code
SV-8   the dashboard refuses an anonymous read
SV-11  its own deployment, nothing shared with the gate
AG-1   the service answers one origin

The routes are called through WSGI rather than over a socket, so this needs
no port, no container and no cloud project -- and it still exercises the
real request path, the real validation and the real store. The clock is
injected, which is what lets the SV-4 check fast-forward a day instead of
waiting one.

No package manager, same as the other checks here.
"""

import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SERVICE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "experiment_service"))
sys.path.insert(0, SERVICE)

from app import App                      # noqa: E402
from store import MemoryStore            # noqa: E402

ORIGIN = "https://datadrivendecisions.github.io"
TOKEN = "an-owner-token-for-the-gate"
PURGE_TOKEN = "a-separate-token-for-the-scheduler"

PASSES = []
FAILURES = []


def check(name, condition, detail=""):
    (PASSES if condition else FAILURES).append((name, detail))
    print(("  PASS  " if condition else "  FAIL  ") + name)
    if detail and not condition:
        print("        " + detail)


class Clock:
    def __init__(self, t=1_800_000_000.0):
        self.t = t

    def __call__(self):
        return self.t

    def advance(self, seconds):
        self.t += seconds


def call(app, method, path, body=None, token=None, origin=ORIGIN, headers=None):
    raw = json.dumps(body).encode("utf-8") if body is not None else b""
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "CONTENT_LENGTH": str(len(raw)),
        "wsgi.input": io.BytesIO(raw),
        "REMOTE_ADDR": "198.51.100.7",
    }
    if origin:
        environ["HTTP_ORIGIN"] = origin
    if token:
        environ["HTTP_AUTHORIZATION"] = "Bearer " + token
    environ.update(headers or {})

    captured = {}

    def start_response(status, response_headers):
        captured["status"] = int(status.split()[0])
        captured["headers"] = dict(response_headers)

    chunks = app(environ, start_response)
    raw_body = b"".join(chunks)
    captured["raw"] = raw_body
    try:
        captured["json"] = json.loads(raw_body) if raw_body else {}
    except ValueError:
        captured["json"] = {}
    return captured


def submission(code="kite", team=3, agent_round=1, claims=(1, 2)):
    def one(n, agent, claim, opened):
        return {"n": n, "agent": agent, "claim": claim, "side": "a", "pick": 24,
                "opened": ["c%d-%02d" % (claim, i) for i in opened],
                "seconds": 180, "endSide": "a", "moved": True, "tlx": 47, "q": 11}
    return {"v": 2, "code": code, "team": team, "rounds": [
        one(1, agent_round == 1, claims[0], [3, 7, 11, 2]),
        one(2, agent_round == 2, claims[1], [4, 9, 1, 12, 5, 16]),
    ]}


def fresh(clock=None):
    clock = clock or Clock()
    return App(store=MemoryStore(salt="gate"), owner_token=TOKEN,
               purge_token=PURGE_TOKEN, origins=(ORIGIN,), clock=clock), clock


# ------------------------------------------------------------------ SV-1 ---

def sv1():
    print("\nSV-1  the submission carries no free text")
    app, _ = fresh()

    ok = call(app, "POST", "/submit", submission())
    check("a well-formed submission is accepted", ok["status"] == 200,
          json.dumps(ok["json"])[:200])

    # Every shape a sentence could arrive in.
    prose = "I think the small-model people are right, and here is why."
    attempts = [
        ("an extra top-level field", dict(submission(), note=prose)),
        ("an extra field inside a round", None),
        ("the student's position sentence", None),
        ("the assistant's reply", None),
        ("a code that is a sentence", dict(submission(), code=prose)),
        ("a code with a space in it", dict(submission(), code="two words")),
        ("a card id that is prose", None),
        ("a team that is a string", dict(submission(), team="three")),
        ("a workload score out of range", None),
        ("nine opened cards", None),
        ("the same card twice", None),
        ("a card from the other claim", None),
        ("an unknown line version", dict(submission(), v=3)),
        ("the assistant in both rounds", None),
        ("the assistant in neither round", None),
        ("the same claim twice", None),
        ("a raw result line as the body", "v1|kite|t3|r1:ask:c1"),
        ("three rounds", None),
        # Appended, not inserted: the overrides below address this list by position.
        ("a version 1 payload, from before the seconds to a side",
         dict(submission(), v=1, rounds=[{k: v for k, v in r.items() if k != "pick"}
                                         for r in submission()["rounds"]])),
    ]

    s = submission(); s["rounds"][0]["reply"] = prose
    attempts[1] = (attempts[1][0], s)
    s = submission(); s["rounds"][0]["position"] = prose
    attempts[2] = (attempts[2][0], s)
    s = submission(); s["assistantReply"] = prose
    attempts[3] = (attempts[3][0], s)
    s = submission(); s["rounds"][0]["opened"] = [prose]
    attempts[6] = (attempts[6][0], s)
    s = submission(); s["rounds"][0]["tlx"] = 400
    attempts[8] = (attempts[8][0], s)
    s = submission(); s["rounds"][0]["opened"] = ["c1-%02d" % i for i in range(1, 10)]
    attempts[9] = (attempts[9][0], s)
    s = submission(); s["rounds"][0]["opened"] = ["c1-03", "c1-03"]
    attempts[10] = (attempts[10][0], s)
    s = submission(); s["rounds"][0]["opened"] = ["c2-03"]
    attempts[11] = (attempts[11][0], s)
    s = submission(); s["rounds"][1]["agent"] = True
    attempts[13] = (attempts[13][0], s)
    s = submission(); s["rounds"][0]["agent"] = False
    attempts[14] = (attempts[14][0], s)
    s = submission(); s["rounds"][1]["claim"] = 1; s["rounds"][1]["opened"] = ["c1-05"]
    attempts[15] = (attempts[15][0], s)
    s = submission(); s["rounds"].append(s["rounds"][0])
    attempts[17] = (attempts[17][0], s)

    rejected = []
    for label, payload in attempts:
        r = call(app, "POST", "/submit", payload)
        rejected.append((label, r["status"], r["json"].get("error", "")))
    bad = [(l, st) for l, st, _ in rejected if st != 400]
    check("%d payloads carrying something they should not, %d rejected"
          % (len(attempts), len(attempts) - len(bad)), not bad,
          "accepted: " + ", ".join("%s (%d)" % b for b in bad))

    stored = json.dumps(app.store.rows())
    check("0 occurrences of the prose in anything stored", prose not in stored)
    check("still 1 row after %d refusals" % len(attempts),
          call(app, "GET", "/dashboard", token=TOKEN)["json"]["count"] == 1)


# ------------------------------------------------------------ SV-3, SV-8 ---

def sv3_sv8():
    print("\nSV-3  no route returns one student's row; SV-8  the dashboard is owners-only")
    app, _ = fresh()
    for code in ("kite", "anvil", "reed"):
        call(app, "POST", "/submit", submission(code=code))

    anonymous = [
        call(app, "GET", "/dashboard"),
        call(app, "GET", "/dashboard", token="wrong"),
        call(app, "GET", "/dashboard", token=""),
        call(app, "POST", "/delete", {"code": "kite"}),
        call(app, "POST", "/purge"),
    ]
    check("5 anonymous or wrongly-credentialled reads, 0 accepted",
          all(r["status"] == 401 for r in anonymous),
          str([r["status"] for r in anonymous]))

    # Every route the service answers, asked for one student by every means.
    probes = [
        ("GET", "/dashboard?code=kite"),
        ("GET", "/submissions/kite"),
        ("GET", "/submission?code=kite"),
        ("GET", "/row/kite"),
        ("GET", "/kite"),
    ]
    found = []
    for method, path in probes:
        r = call(app, method, path, token=TOKEN)
        if r["status"] == 200 and r["json"].get("count") == 1:
            found.append(path)
    check("5 attempts to fetch one student's row, 0 returned one", not found,
          str(found))

    rows = call(app, "GET", "/dashboard", token=TOKEN)["json"]["rows"]
    check("the dashboard returns every row or none: 3 of 3", len(rows) == 3)
    codes_in_response = json.dumps(rows)
    check("0 student codes anywhere in the response",
          not any(c in codes_in_response for c in ("kite", "anvil", "reed")),
          codes_in_response[:200])
    check("3 distinct opaque ids, so a repeat submission is still visible",
          len({r["id"] for r in rows}) == 3)


# ------------------------------------------------------- the codebook ---

def codebook():
    print("\nSM-8 beside the service  the answer key reaches the owners and nobody else")
    key = "c1-01 NAS3\nc1-02 AS3\nc2-01 AW1"
    app = App(store=MemoryStore(salt="gate"), owner_token=TOKEN, purge_token=PURGE_TOKEN,
              origins=(ORIGIN,), clock=Clock(), codebook=key)
    ok = call(app, "POST", "/submit", submission())
    owner = call(app, "GET", "/dashboard", token=TOKEN)
    check("the owners' dashboard carries the codebook", owner["json"].get("codebook") == key,
          repr(owner["json"].get("codebook")))
    others = [
        ("the submit response", ok),
        ("an anonymous dashboard read", call(app, "GET", "/dashboard")),
        ("a wrong token", call(app, "GET", "/dashboard", token="wrong")),
        ("the health route", call(app, "GET", "/health")),
        ("an unknown route, with the owners' token", call(app, "GET", "/codebook", token=TOKEN)),
        ("the preflight", call(app, "OPTIONS", "/dashboard")),
    ]
    leaked = [label for label, r in others if b"NAS3" in r["raw"] or b"c1-01" in r["raw"]]
    check("%d other responses, 0 carrying any of it" % len(others), not leaked, ", ".join(leaked))
    bare, _ = fresh()
    check("with no codebook configured the dashboard says so rather than inventing one",
          call(bare, "GET", "/dashboard", token=TOKEN)["json"].get("codebook") is None)


# ------------------------------------------------------------------ SV-5 ---

def sv5():
    print("\nSV-5  a row goes on request, by the code the student gives")
    app, _ = fresh()
    for code in ("kite", "anvil"):
        call(app, "POST", "/submit", submission(code=code))
    before = call(app, "GET", "/dashboard", token=TOKEN)["json"]["count"]
    gone = call(app, "POST", "/delete", {"code": "kite"}, token=TOKEN)
    after = call(app, "GET", "/dashboard", token=TOKEN)["json"]["count"]
    check("2 rows, delete by code, 1 row",
          before == 2 and gone["json"]["removed"] == 1 and after == 1,
          "before=%s removed=%s after=%s" % (before, gone["json"], after))
    again = call(app, "POST", "/delete", {"code": "kite"}, token=TOKEN)
    check("deleting it twice removes 0 the second time",
          again["json"]["removed"] == 0)

    app2, _ = fresh()
    call(app2, "POST", "/submit", submission(code="kite", team=3))
    call(app2, "POST", "/submit", submission(code="kite", team=4))
    rows = call(app2, "GET", "/dashboard", token=TOKEN)["json"]["rows"]
    check("the same code twice is 1 row, and the last write won",
          len(rows) == 1 and rows[0]["team"] == 4, str(rows))


# ------------------------------------------------------------------ SV-4 ---

def sv4():
    print("\nSV-4  nothing survives the teaching day")
    app, clock = fresh()
    for code in ("kite", "anvil", "reed"):
        call(app, "POST", "/submit", submission(code=code))
    check("3 rows during the session",
          call(app, "GET", "/dashboard", token=TOKEN)["json"]["count"] == 3)

    purged = call(app, "POST", "/purge", token=TOKEN)
    check("the purge removes 3 and leaves 0",
          purged["json"]["removed"] == 3
          and call(app, "GET", "/dashboard", token=TOKEN)["json"]["count"] == 0)

    # And now the case the purge exists to survive: the scheduler does not fire.
    app2, clock2 = fresh()
    for code in ("kite", "anvil", "reed"):
        call(app2, "POST", "/submit", submission(code=code))
    clock2.advance(24 * 60 * 60 + 1)
    morning = call(app2, "GET", "/dashboard", token=TOKEN)["json"]
    check("the scheduler never fires; the morning after, 0 rows remain",
          morning["count"] == 0, str(morning))

    app3, clock3 = fresh()
    call(app3, "POST", "/submit", submission())
    clock3.advance(23 * 60 * 60)
    check("23 hours in, the row is still there for the owners",
          call(app3, "GET", "/dashboard", token=TOKEN)["json"]["count"] == 1)

    scheduled = call(app3, "POST", "/purge", token=PURGE_TOKEN)
    check("the scheduler's own token purges, without being an owner",
          scheduled["status"] == 200)

    # The header Cloud Scheduler sets is not a credential, and an earlier
    # draft of the route treated it as one.
    spoofed = call(app3, "POST", "/purge", token=None,
                   headers={"HTTP_X_CLOUDSCHEDULER": "true"})
    check("a caller claiming to be the scheduler by header alone is refused",
          spoofed["status"] == 401, str(spoofed["status"]))


# ------------------------------------------------------------------ AG-1 ---

def ag1():
    print("\nAG-1  the service answers one origin, and the tool uses two routes")
    app, _ = fresh()

    allowed = call(app, "POST", "/submit", submission(), origin=ORIGIN)
    check("the pinned origin is answered with its own name",
          allowed["headers"].get("Access-Control-Allow-Origin") == ORIGIN,
          str(allowed["headers"]))

    for other in ("https://evil.example", "http://localhost:8765",
                  "https://datadrivendecisions.github.io.evil.example", "null"):
        r = call(app, "POST", "/submit", submission(code="anvil"), origin=other)
        if "Access-Control-Allow-Origin" in r["headers"]:
            check("origin %s is refused a CORS header" % other, False,
                  r["headers"]["Access-Control-Allow-Origin"])
            return
    check("4 other origins, 0 given a CORS header", True)

    pre = call(app, "OPTIONS", "/submit", origin=ORIGIN)
    check("the preflight is answered 204 for the pinned origin",
          pre["status"] == 204
          and pre["headers"].get("Access-Control-Allow-Origin") == ORIGIN)
    # HTTP gives a 204 no body. The local server let "204 with {}" through;
    # Cloud Run's front end turned it into a 502, so every student's submit
    # died at the preflight. A check that calls the app directly could only
    # see it if it asks this question outright.
    check("the 204 carries no body and no content headers",
          pre["raw"] == b"" and "Content-Length" not in pre["headers"]
          and "Content-Type" not in pre["headers"],
          "body %r, headers %s" % (pre["raw"], sorted(pre["headers"])))

    routes = [p for p in ("/submit", "/dashboard", "/delete", "/purge", "/health")]
    tool_routes = ("/submit", "/dashboard")
    check("the service answers %d routes; the tool uses %d of them"
          % (len(routes), len(tool_routes)), len(tool_routes) <= 2)

    unknown = call(app, "GET", "/anything-else", token=TOKEN)
    check("an unknown route is 404, not a redirect anywhere", unknown["status"] == 404)


# ------------------------------------------------------------ rate limit ---

def flood():
    print("\nA classroom, not a botnet")
    app, _ = fresh()
    statuses = [call(app, "POST", "/submit", submission(code="c%d" % i))["status"]
                for i in range(60)]
    check("60 submissions from one address: some refused",
          429 in statuses, "statuses seen: %s" % sorted(set(statuses)))
    check("the first 30 got through", statuses[:30].count(200) == 30)


def main():
    print("Phases 7 and 8, the server half — experiment_service/")
    print("Routes driven through WSGI; no port, no container, no cloud project.")
    sv1()
    sv3_sv8()
    sv5()
    sv4()
    ag1()
    codebook()
    flood()
    print("\n%d passed, %d failed." % (len(PASSES), len(FAILURES)))
    if FAILURES:
        for name, detail in FAILURES:
            print("  FAILED: " + name + ("  " + detail if detail else ""))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
