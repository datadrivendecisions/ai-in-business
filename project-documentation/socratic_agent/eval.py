"""Run the gate against the fixtures and check the answer keys as assertions.

    python eval.py            # all cases
    python eval.py team_03    # one case

Checks split the way the PRD does. The invariants are pass/fail on every report,
because a single verdict or score reaching a team is a defect whatever else the
report got right. The expectations are per fixture, from the answer keys in
../test-fixtures/README.md, and they are what tells calibration from noise.

The growth checks are string heuristics over the questions, not judgements. They
can say a topic was raised or was not; they cannot say a return was asked well.
Read them as a screen, and read the report itself before believing them.
"""

import asyncio
import re
import sys
from pathlib import Path

from google.adk.runners import InMemoryRunner
from google.genai import types

from agent import root_agent

RAW = ("https://raw.githubusercontent.com/datadrivendecisions/ai-in-business/"
       "now-board-landing/project-documentation/test-fixtures/")
FIXTURES = Path(__file__).parent.parent / "test-fixtures"

VERDICT_WORDS = r"\b(good|bad|strong|weak|thorough|promising|excellent|poor|impressive|well done|great job|solid)\b"
ADVICE_WORDS = r"\b(you might|you should|consider |try to|it would help|we recommend|I suggest)\b"
LEDGER_WORDS = ("CONFIRMED", "MISMATCHED", "NOT-FOUND", "UNCHECKED")

CASES = {
    "team_03": {
        "page": RAW + "week-02-team-03.html",
        "history": None,
        "expect": {"sourcing": (0, 1), "vetting": (0, 1), "movement": None},
        "ledger": {"Van der Meer": ("NOT-FOUND",)},
    },
    "team_07_wk2": {
        "page": RAW + "week-02-team-07.html",
        "history": None,
        "expect": {"sourcing": (2, 3), "vetting": (2, 3), "reasoning": (2, 3), "movement": None},
        "ledger": {"Draghi": ("CONFIRMED",), "Article 6": ("CONFIRMED",),
                   "Microsoft": ("CONFIRMED",), "Stanford": ("CONFIRMED",)},
    },
    "team_07_wk3": {
        "page": RAW + "week-03-team-07.html",
        "history": FIXTURES / "week-02-team-07-report.txt",
        "expect": {"sourcing": (2, 3), "vetting": (2, 3), "reasoning": (2, 3), "movement": (2, 3)},
        "growth": {
            "must_return_to": ["switching cost", "vendor nationality"],
            "must_not_repeat": ["house rule", "specialist quotation tool"],
            "should_name_return": ["return", "again", "last week", "previous"],
        },
    },
}


def split(text):
    """The two halves. Everything the team sees is above the second heading."""
    m = re.search(r"##\s*FOR THE OWNERS", text, re.I)
    t = re.search(r"##\s*FOR THE TEAM", text, re.I)
    if not t or not m or m.start() < t.start():
        return None, None
    return text[t.end():m.start()], text[m.end():]


def questions(team_half):
    return [q.strip() for q in re.findall(r"[^?]*\?", team_half) if len(q.strip()) > 25]


def score(owner_half, name):
    m = re.search(rf"{name}\s*[:\-]?\s*(n/a|[0-3])", owner_half, re.I)
    if not m:
        return None
    v = m.group(1).lower()
    return "n/a" if v == "n/a" else int(v)


def check(case_name, case, text):
    team, owner = split(text)
    results = []

    def add(ok, label, detail=""):
        results.append((ok, label, detail))

    if team is None:
        add(False, "structure: both headings, in order", "missing or reversed")
        return results, None
    add(True, "structure: both headings, in order")

    qs = questions(team)
    add(3 <= len(qs) <= 5, "B3: three to five questions", f"{len(qs)}")

    v = re.findall(VERDICT_WORDS, team, re.I)
    add(not v, "I1: no verdict to the team", ", ".join(sorted(set(v))))
    a = re.findall(ADVICE_WORDS, team, re.I)
    add(not a, "I1: no advice to the team", ", ".join(sorted(set(a))))
    # Quoting the team's own words back is not rubric language, so scan only
    # outside quotations, and only flag a dimension name used as a score.
    unquoted = re.sub(r'"[^"]*"', " ", team)
    s = re.findall(r"\b(Sourcing|Vetting|Reasoning|Movement)\s*[:=]\s*[0-3]|\b(rubric|gate A)\b",
                   unquoted, re.I)
    s = [x for pair in s for x in pair if x]
    add(not s, "I2: no score or rubric language to the team", ", ".join(sorted(set(s))))
    o = re.findall(r"\b(another team|other team|team \d)\b", team, re.I)
    add(not o, "I4: no other team named", ", ".join(sorted(set(o))))

    scores = {k: score(owner, k) for k in ("Sourcing", "Vetting", "Reasoning", "Movement")}
    for dim, rng in case["expect"].items():
        got = scores[dim.capitalize()]
        if rng is None:
            add(got in (None, "n/a"), f"{dim} is n/a (cold start)", str(got))
        else:
            lo, hi = rng
            add(isinstance(got, int) and lo <= got <= hi,
                f"{dim} in {lo}-{hi}", str(got))

    for source, allowed in case.get("ledger", {}).items():
        # The ledger is a block per source, not a line: fix 16 added a "cited at"
        # line, so the verdict sits below the name. Read from the name to the
        # next name.
        m = re.search(rf"{re.escape(source)}(.{{0,600}}?)(?=\n\s*[*-]\s+\S|\Z)",
                      owner, re.I | re.S)
        entry = m.group(0) if m else ""
        found = [w for w in LEDGER_WORDS if w in entry]
        add(bool(found) and found[0] in allowed,
            f"ledger: {source} -> {'/'.join(allowed)}", found[0] if found else "not in ledger")

    g = case.get("growth")
    if g:
        low = team.lower()
        add(any(k in low for k in g["must_return_to"]),
            "growth: returns to the ducked claim",
            "found" if any(k in low for k in g["must_return_to"]) else "absent")
        # A topic reappearing is not a repeat: building on an answer is what the
        # growth requirement asks for. String matching cannot tell the two apart,
        # so this reports rather than judges — read the question before believing
        # it either way.
        ack = ("last week", "in response", "previously", "clarifies", "you now")
        for k in g["must_not_repeat"]:
            if k in low:
                sent = next((q for q in qs if k in q.lower()), "")
                built_on = any(w in sent.lower() for w in ack)
                add(built_on, f"growth: '{k}' built on rather than repeated",
                    "acknowledged" if built_on else "REVIEW BY HAND — no marker of the prior answer")
        add(any(k in low for k in g["should_name_return"]),
            "growth: names the return as a return")

    return results, scores


async def run_case(name, case):
    runner = InMemoryRunner(agent=root_agent, app_name="eval")
    session = await runner.session_service.create_session(app_name="eval", user_id="eval")
    prompt = case["page"]
    if case["history"]:
        prompt = (f"{case['page']}\n\nThis team's earlier reports:\n\n"
                  f"{Path(case['history']).read_text(encoding='utf-8')}")
    out = []
    async for event in runner.run_async(
        user_id="eval", session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
    ):
        if event.content and event.content.parts:
            for p in event.content.parts:
                if p.text:
                    out.append(p.text)
    return "".join(out)


async def main():
    wanted = sys.argv[1:] or list(CASES)
    reports, failures, total = {}, 0, 0
    for name in wanted:
        print(f"\n{'='*70}\n{name}\n{'='*70}")
        try:
            text = await run_case(name, CASES[name])
        except Exception as exc:                                   # noqa: BLE001
            print(f"  RUN FAILED: {type(exc).__name__}: {exc}")
            failures += 1
            continue
        reports[name] = text
        results, scores = check(name, CASES[name], text)
        for ok, label, detail in results:
            total += 1
            failures += 0 if ok else 1
            print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"   [{detail}]" if detail else ""))
        if scores:
            print(f"  scores: {scores}")
    out = Path(__file__).parent / "eval-output.txt"
    out.write_text("\n\n".join(f"{'='*70}\n{k}\n{'='*70}\n{v}" for k, v in reports.items()))
    print(f"\n{total - failures}/{total} checks passed. Reports written to {out.name}.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
