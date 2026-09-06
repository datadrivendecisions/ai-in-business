"""Run the gate over a roster of teams and write one report per team.

    python run_week.py roster.tsv --week 2 --out ../gate-reports

The roster is tab-separated, one team per line, blank lines and # comments
ignored:

    team-01<TAB>https://.../team-01/week-02.html<TAB>[path to prior report]

The third column is optional and is the team's own half of last week's report —
its history. Never give it the owners' half: a history carrying last week's score
into this week's questions puts the rubric in the student-facing channel by
another route.

Two files per team, and the split is the point:

    <out>/week-NN/<team>-for-the-team.md      forward this, and nothing else
    <out>/week-NN/<team>-for-the-owners.md    scores, ledger, gate signal

Nothing is sent anywhere. Forwarding is a person's job, because the one
unrecoverable mistake in this system is the owners' half reaching a student, and
it should take a deliberate act.

Written for the teaching team rather than for the site: the tool needs a key, and
`site/` is a public URL from a public repository (ADR-0014, and the tool rules in
CLAUDE.md).
"""

import argparse
import asyncio
import re
import sys
from pathlib import Path

from google.adk.runners import InMemoryRunner
from google.genai import types

from agent import root_agent

RETRIES = 2


def read_roster(path):
    teams = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("\t") if p.strip()]
        if len(parts) < 2:
            sys.exit(f"{path}:{n}: expected 'team<TAB>url', got: {line!r}")
        teams.append({"team": parts[0], "url": parts[1],
                      "history": Path(parts[2]) if len(parts) > 2 else None})
    if not teams:
        sys.exit(f"{path}: no teams found")
    return teams


def split(text):
    t = re.search(r"##\s*FOR THE TEAM", text, re.I)
    o = re.search(r"##\s*FOR THE OWNERS", text, re.I)
    if not t or not o or o.start() < t.start():
        return None, None
    return text[t.end():o.start()].strip(), text[o.end():].strip()


def summarise(owner_half):
    """The one line an instructor reads first."""
    scores = {}
    for dim in ("Sourcing", "Vetting", "Reasoning", "Movement"):
        m = re.search(rf"{dim}\W{{0,4}}\s*(n/a|[0-3])\b", owner_half, re.I)
        scores[dim[0]] = m.group(1) if m else "?"
    flags = [w for w in ("NOT-FOUND", "MISMATCHED", "UNCHECKED") if w in owner_half]
    gate = "open" if re.search(r"gate a (?:is )?opens?", owner_half, re.I) else \
           "CLOSED" if re.search(r"gate a (?:is )?(?:stays )?closed", owner_half, re.I) else "?"
    return scores, flags, gate


async def run_team(entry):
    prompt = entry["url"]
    if entry["history"]:
        prompt += ("\n\nThis team's earlier reports:\n\n"
                   + entry["history"].read_text(encoding="utf-8"))
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
        # One run in twelve came back empty during the pilot, with no error.
        # A fresh session per attempt, because a session that produced nothing
        # is not a session to ask again.
        if text and split(text)[0]:
            return text, attempt
    return "", RETRIES + 1


async def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("roster")
    ap.add_argument("--week", required=True)
    ap.add_argument("--out", default="gate-reports")
    args = ap.parse_args()

    teams = read_roster(args.roster)
    outdir = Path(args.out) / f"week-{int(args.week):02d}"
    outdir.mkdir(parents=True, exist_ok=True)

    rows, failed = [], []
    for entry in teams:
        team = entry["team"]
        print(f"  {team} … ", end="", flush=True)
        try:
            text, attempts = await run_team(entry)
        except Exception as exc:                                   # noqa: BLE001
            print(f"FAILED — {type(exc).__name__}: {exc}")
            failed.append(team)
            continue
        if not text:
            print(f"NO REPORT after {attempts} attempts")
            failed.append(team)
            continue
        team_half, owner_half = split(text)
        (outdir / f"{team}-for-the-team.md").write_text(team_half + "\n", encoding="utf-8")
        (outdir / f"{team}-for-the-owners.md").write_text(owner_half + "\n", encoding="utf-8")
        scores, flags, gate = summarise(owner_half)
        rows.append((team, scores, flags, gate, attempts))
        print(f"ok{'' if attempts == 1 else f' (attempt {attempts})'}")

    print(f"\n{'team':<12} {'S':>2} {'V':>2} {'R':>2} {'M':>3}  gate     sources")
    print("-" * 62)
    for team, s, flags, gate, _ in rows:
        print(f"{team:<12} {s['S']:>2} {s['V']:>2} {s['R']:>2} {s['M']:>3}  "
              f"{gate:<8} {', '.join(flags) or '-'}")

    print(f"\n{len(rows)} of {len(teams)} reports written to {outdir}")
    if failed:
        print(f"NO REPORT for: {', '.join(failed)} — run these again before the session.")
    print("The -for-the-team files are the only ones that may be forwarded.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
