"""The weekly gate as a Cloud Run service, triggered by Cloud Scheduler.

The schedule is the deadline. One run a week reads the roster, fetches each
team's published page, and writes one report per team — which is the
one-submission-one-report protocol of LRD 6.4 enforced by the clock rather than
by a rule anyone has to apply. A team that publishes after the run is unread,
and there is no endpoint here that lets anyone ask again.

This is ADR-0014's scheduled pull with the parts named: Firestore is the roster
that record calls infrastructure, Cloud Scheduler is the clock, and the agent's
only input is still a page that is already public.

    POST /run?week=3          run every active team
    POST /run?week=3&team=t04 run one team, for a page that was late or a run that broke

Data model — the split is enforced by IAM, not by discipline:

    teams/{team}                        url, name, active
    reports/{team}_w{NN}                the team's half. Readable by whatever
                                        delivers it to the team.
    owner_reports/{team}_w{NN}          scores, ledger, gate signal. Readable
                                        only by the module owners.

Nothing here delivers anything. A delivery job reads `reports` and must never be
granted `owner_reports`: the one unrecoverable mistake in this system is the
owners' half reaching a student, and a permission boundary is a better guard than
a careful person.
"""

import asyncio
import os
import re
import sys
from datetime import datetime, timezone

from flask import Flask, request
from google.cloud import firestore

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import root_agent                                       # noqa: E402
from google.adk.runners import InMemoryRunner                      # noqa: E402
from google.genai import types                                     # noqa: E402

app = Flask(__name__)
db = firestore.Client(database=os.environ.get("FIRESTORE_DATABASE", "(default)"))
RETRIES = 2


def split(text):
    t = re.search(r"##\s*FOR THE TEAM", text, re.I)
    o = re.search(r"##\s*FOR THE OWNERS", text, re.I)
    if not t or not o or o.start() < t.start():
        return None, None
    return text[t.end():o.start()].strip(), text[o.end():].strip()


def summarise(owner_half):
    scores = {}
    for dim in ("Sourcing", "Vetting", "Reasoning", "Movement"):
        m = re.search(rf"{dim}\W{{0,4}}\s*(n/a|[0-3])\b", owner_half, re.I)
        scores[dim.lower()] = m.group(1) if m else None
    gate = ("open" if re.search(r"gate a (?:is )?opens?", owner_half, re.I)
            else "closed" if re.search(r"gate a .{0,12}closed", owner_half, re.I)
            else "unknown")
    flags = [w for w in ("NOT-FOUND", "MISMATCHED", "UNCHECKED") if w in owner_half]
    return scores, gate, flags


def history(team, week):
    """Every earlier team-facing report, oldest first.

    The team's half only. A history carrying last week's score into this week's
    questions would put the rubric in the student-facing channel by another
    route, which is why the owners' half lives in a different collection and is
    not read here.
    """
    earlier = []
    for w in range(2, int(week)):
        doc = db.collection("reports").document(f"{team}_w{w:02d}").get()
        if doc.exists:
            earlier.append(f"--- week {w} ---\n{doc.to_dict().get('text','')}")
    return "\n\n".join(earlier)


async def run_team(url, prior):
    prompt = url
    if prior:
        prompt += f"\n\nThis team's earlier reports:\n\n{prior}"
    for attempt in range(1, RETRIES + 2):
        runner = InMemoryRunner(agent=root_agent, app_name="gate")
        session = await runner.session_service.create_session(app_name="gate", user_id="gate")
        out = []
        async for event in runner.run_async(
            user_id="gate", session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
        ):
            if event.content and event.content.parts:
                out.extend(p.text for p in event.content.parts if p.text)
        text = "".join(out).strip()
        if text and split(text)[0]:
            return text, attempt
    return "", RETRIES + 1


@app.post("/run")
def run():
    week = request.args.get("week")
    if not week or not week.isdigit():
        return {"error": "week is required, as a number"}, 400
    wk = f"w{int(week):02d}"

    query = db.collection("teams").where(filter=firestore.FieldFilter("active", "==", True))
    teams = [(d.id, d.to_dict()) for d in query.stream()]
    if one := request.args.get("team"):
        teams = [t for t in teams if t[0] == one]
        if not teams:
            return {"error": f"no active team {one!r}"}, 404

    done, failed = [], []
    for team, data in teams:
        url = data.get("url")
        if not url:
            failed.append({"team": team, "reason": "no url in roster"})
            continue
        try:
            text, attempts = asyncio.run(run_team(url, history(team, week)))
        except Exception as exc:                                   # noqa: BLE001
            failed.append({"team": team, "reason": f"{type(exc).__name__}: {exc}"})
            continue
        if not text:
            failed.append({"team": team, "reason": f"empty response after {attempts} attempts"})
            continue

        team_half, owner_half = split(text)
        scores, gate, flags = summarise(owner_half)
        now = datetime.now(timezone.utc)
        db.collection("reports").document(f"{team}_{wk}").set({
            "team": team, "week": int(week), "url": url,
            "text": team_half, "created": now,
        })
        db.collection("owner_reports").document(f"{team}_{wk}").set({
            "team": team, "week": int(week), "url": url,
            "text": owner_half, "scores": scores, "gate_a": gate,
            "ledger_flags": flags, "attempts": attempts, "created": now,
        })
        done.append({"team": team, "gate_a": gate, "scores": scores, "attempts": attempts})

    # 500 on any failure so the scheduler records it and someone is told. A week
    # in which two teams silently got nothing is the failure this exists to make
    # impossible to miss.
    return {"week": int(week), "reported": done, "failed": failed}, (500 if failed else 200)


@app.get("/health")
def health():
    return {"ok": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
