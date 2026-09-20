#!/usr/bin/env python3
"""Phases 2 and 5: check the tool's arithmetic against an independent reference.

The tool computes the congeniality index, the paired difference, its interval,
the smallest detectable effect and Cohen's kappa. This script computes all of
them again from the codebook and the fixture inputs, in Python, without reading
the tool's code -- and then runs the tool's own code (via runpage.mjs, which
evaluates the shipped page) over the same fixtures and compares.

An agreement between two implementations of the same wrong formula would prove
nothing, so the two disagree in method where they can: the interval uses
scipy's t quantile rather than a series of its own, and the detectable effect
is solved exactly from the non-central t rather than approximated.

    python3 check-measures.py          run everything
    python3 check-measures.py -v       ...and print every figure

Exit status is 0 when every fixture matches to 3 decimal places.
"""

import json
import math
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
CODEBOOK = ROOT / "work" / "drafts" / "week-03-codebook.md"
PAGE = ROOT / "site" / "tool-bias-experiment.html"

DP = 3
TOL = 10 ** -DP / 2

try:
    from scipy import optimize, stats
except ImportError:  # pragma: no cover
    sys.exit("this check needs scipy: python3 -m pip install scipy")


# ---------------------------------------------------------------- the codebook

def read_codebook():
    """id -> (stance, quality), read straight out of the markdown table."""
    book = {}
    for line in CODEBOOK.read_text(encoding="utf-8").splitlines():
        m = re.search(r"\|\s*`(c[12]-\d{2})`\s*\|\s*(NA|A)(S|W)\d*\s*\|", line)
        if m:
            book[m.group(1)] = (m.group(2), m.group(3))
    return book


BOOK = read_codebook()


def congenial(card, side):
    stance, _ = BOOK[card]
    return (side == "agree" and stance == "A") or (side == "disagree" and stance == "NA")


def strong_opposing(card, side):
    stance, quality = BOOK[card]
    return quality == "S" and not congenial(card, side)


def measure(ids, side):
    opened = len(ids)
    cong = sum(1 for c in ids if congenial(c, side))
    return {
        "opened": opened,
        "congenial": cong,
        "uncongenial": opened - cong,
        "strongOpposing": sum(1 for c in ids if strong_opposing(c, side)),
        "index": None if opened == 0 else (cong - (opened - cong)) / opened,
    }


# ------------------------------------------------------------- the two totals

TLX_IDS = ["mental", "physical", "temporal", "perform", "effort", "frustr"]
FLIPPED = {"perform"}
PERCEPTION_IDS = ["satisf", "confid"]


def tlx_total(a):
    raw = sum((8 - a[k]) if k in FLIPPED else a[k] for k in TLX_IDS)
    return round((raw - 6) / 36 * 100)


def perception_total(a):
    return sum(a[k] for k in PERCEPTION_IDS)


# --------------------------------------------------------------- the statistics

ALPHA = 0.05
POWER = 0.80


def paired(diffs):
    n = len(diffs)
    m = sum(diffs) / n
    sd = math.sqrt(sum((d - m) ** 2 for d in diffs) / (n - 1))
    se = sd / math.sqrt(n)
    t = stats.t.ppf(1 - ALPHA / 2, n - 1)
    return {"n": n, "diff": m, "sdDiff": sd, "tcrit": t, "lo": m - t * se, "hi": m + t * se}


def exact_mde(n):
    """The standardised difference a paired design of n pairs catches 80% of the
    time at alpha = .05 two-tailed, solved from the non-central t rather than
    approximated. This is what the tool's figure is checked against."""
    df = n - 1
    crit = stats.t.ppf(1 - ALPHA / 2, df)

    def power(d):
        nc = d * math.sqrt(n)
        # The wrong-tail term underflows to NaN in scipy once nc is large, and
        # at that point it is below 1e-12 anyway, so it is dropped rather than
        # allowed to poison the solve.
        far = stats.nct.cdf(-crit, df, nc)
        if not math.isfinite(far):
            far = 0.0
        return stats.nct.sf(crit, df, nc) + far - POWER

    return optimize.brentq(power, 1e-6, 3.0)


def kappa(a, b, c, d):
    n = a + b + c + d
    po = (a + d) / n
    pe = ((a + b) * (a + c) + (c + d) * (b + d)) / (n * n)
    return {"n": n, "po": po, "pe": pe, "kappa": (po - pe) / (1 - pe)}


# ------------------------------------------------------------------- fixtures

def ids_of(deck):
    return [f"c{deck}-{i:02d}" for i in range(1, 17)]


def cell(deck, code):
    """Every card in one cell of one deck, in id order."""
    return [i for i in ids_of(deck) if BOOK[i][0] + BOOK[i][1] == code]


AS1, AW1, NAS1, NAW1 = cell(1, "AS"), cell(1, "AW"), cell(1, "NAS"), cell(1, "NAW")
AS2, AW2, NAS2, NAW2 = cell(2, "AS"), cell(2, "AW"), cell(2, "NAS"), cell(2, "NAW")

# Ten sessions whose numbers can be read off the description rather than
# computed: each names how many cards it takes from each cell, so the expected
# index is arithmetic anyone can do in their head before running anything.
MEASURES = [
    dict(name="all congenial, agreeing", side="agree", ids=AS1[:4] + AW1[:4]),
    dict(name="all uncongenial, agreeing", side="agree", ids=NAS1[:4] + NAW1[:4]),
    dict(name="even split, agreeing", side="agree", ids=AS1[:2] + AW1[:2] + NAS1[:2] + NAW1[:2]),
    dict(name="even split, disagreeing", side="disagree", ids=AS1[:2] + AW1[:2] + NAS1[:2] + NAW1[:2]),
    dict(name="six to two, agreeing", side="agree", ids=AS1[:3] + AW1[:3] + NAS1[:2]),
    dict(name="five to three, disagreeing", side="disagree", ids=NAS1[:3] + NAW1[:2] + AS1[:3]),
    dict(name="three opens only", side="agree", ids=AS1[:2] + NAW1[:1]),
    dict(name="one open", side="disagree", ids=[AW1[0]]),
    dict(name="deck two, all strong", side="agree", ids=AS2[:4] + NAS2[:4]),
    dict(name="deck two, seven opens", side="disagree", ids=NAW2[:4] + AS2[:3]),
]

TOTALS = [
    dict(name="floor", answers=dict(mental=1, physical=1, temporal=1, perform=7, effort=1, frustr=1, satisf=1, confid=1)),
    dict(name="ceiling", answers=dict(mental=7, physical=7, temporal=7, perform=1, effort=7, frustr=7, satisf=7, confid=7)),
    dict(name="midpoint", answers=dict(mental=4, physical=4, temporal=4, perform=4, effort=4, frustr=4, satisf=4, confid=4)),
    dict(name="mixed a", answers=dict(mental=6, physical=2, temporal=5, perform=3, effort=6, frustr=4, satisf=3, confid=5)),
    dict(name="mixed b", answers=dict(mental=2, physical=1, temporal=3, perform=6, effort=3, frustr=2, satisf=6, confid=6)),
    dict(name="performance high", answers=dict(mental=4, physical=1, temporal=2, perform=7, effort=3, frustr=1, satisf=7, confid=7)),
    dict(name="performance low", answers=dict(mental=4, physical=1, temporal=2, perform=1, effort=3, frustr=1, satisf=2, confid=2)),
    dict(name="mixed c", answers=dict(mental=5, physical=3, temporal=6, perform=2, effort=7, frustr=6, satisf=2, confid=3)),
    dict(name="mixed d", answers=dict(mental=3, physical=2, temporal=2, perform=5, effort=4, frustr=3, satisf=5, confid=4)),
    dict(name="mixed e", answers=dict(mental=7, physical=4, temporal=7, perform=6, effort=5, frustr=2, satisf=4, confid=6)),
]

KAPPAS = [
    dict(name="perfect agreement", a=8, b=0, c=0, d=8),
    dict(name="one card apart", a=7, b=1, c=0, d=8),
    dict(name="chance only", a=4, b=4, c=4, d=4),
    dict(name="lopsided margins", a=14, b=1, c=2, d=3),
]


def line(code, team, rounds):
    return "|".join([f"v2", code, f"t{team}"] + rounds)


def block(n, agent, claim, side, pick, ids, secs, end, moved, tlx, q):
    return ":".join([
        f"r{n}", "ask" if agent else "none", claim,
        "pos" + ("a" if side == "agree" else "d"), f"pick{pick}",
        f"op{len(ids)}", "ids=" + ",".join(ids), f"s{secs}",
        "end" + ("a" if end == "agree" else "d"),
        f"moved{1 if moved else 0}", f"tlx{tlx}", f"q{q}",
    ])


def make_dataset(name, n, seed, malformed=(), lean=None, pick_span=64):
    """A class of n students. Every choice comes from a plain linear
    congruential generator so the same fixture is produced on any machine and
    the reference and the tool are fed exactly the same room.

    `lean` is the chance in ten of agreeing, for a room that does not divide;
    left out, a side is a coin toss exactly as before. The seconds to a side
    are a sweep over `pick_span` rather than a draw, so adding them left every
    other number in the older rooms where it was."""
    state = seed
    ask, none = [], []
    sides = {"c1": [], "c2": []}
    picks = {"c1": [], "c2": []}

    def rnd(k):
        nonlocal state
        state = (1103515245 * state + 12345) % (2 ** 31)
        return state % k

    lines, expected = [], []
    for i in range(n):
        team = (i % 8) + 1
        agent_round = 2 if team <= 4 else 1
        blocks, per = [], {}
        for r in (1, 2):
            if lean is None:
                side = "agree" if rnd(2) == 0 else "disagree"
            else:
                side = "agree" if rnd(10) < lean else "disagree"
            pick_s = (7 * i + 13 * r + seed) % pick_span
            sides[f"c{r}"].append(side)
            picks[f"c{r}"].append(pick_s)
            pool = ids_of(r)
            opened = []
            for _ in range(6 + rnd(3)):
                pick = pool[rnd(len(pool))]
                if pick not in opened:
                    opened.append(pick)
            end = side if rnd(10) else ("disagree" if side == "agree" else "agree")
            secs, tlx, q = 90 + rnd(200), 25 + rnd(45), 4 + rnd(9)
            blocks.append(block(r, agent_round == r, f"c{r}", side, pick_s, opened, secs, end, rnd(2) == 0, tlx, q))
            per["ask" if agent_round == r else "none"] = measure(opened, side)
        lines.append(line(f"s{i:02d}", team, blocks))
        expected.append(per["ask"]["index"] - per["none"]["index"])
        ask.append(per["ask"]["index"])
        none.append(per["none"]["index"])
    lines.extend(malformed)
    return dict(name=name, n=n, lines=lines, diffs=expected,
                ask=ask, none=none, bad=len(malformed), sides=sides, picks=picks)


DATASETS = [
    make_dataset("a full room of 32", 32, 7),
    make_dataset("32 plus two that will not parse", 32, 11, malformed=[
        "v2|broken|t3|r1:ask:c1:posa:pick20:op3:ids=c1-01,c1-02:s100:enda:moved0:tlx40:q8|r2:none:c2:posd:pick20:op8:ids=c2-01,c2-02,c2-03,c2-04,c2-05,c2-06,c2-07,c2-08:s100:endd:moved0:tlx40:q8",
        "v3|future|t1|r1:ask:c1:posa:pick20:op1:ids=c1-01:s10:enda:moved0:tlx1:q2|r2:none:c2:posd:pick20:op1:ids=c2-01:s10:endd:moved0:tlx1:q2",
    ]),
    make_dataset("an afternoon half-group of 14", 14, 23, pick_span=80),
    make_dataset("the smallest run worth reading, 6", 6, 41),
    make_dataset("two cohorts together, 61", 61, 97, pick_span=75),
    make_dataset("a room that leans, 20", 20, 53, lean=9),
]


# ------------------------------------------------------------ the pilot audit
# Phase 0's data criteria, computed from the fixture rooms' own sides and
# seconds rather than from the page's parse of them. Thresholds are the
# blueprint's CL-1, CL-7, CL-10 and CL-5, written out again here on purpose.

def pilot_reference(sides, picks):
    rows = []
    larger = {}
    for claim in ("c1", "c2"):
        n = len(sides[claim])
        agree = sum(1 for s in sides[claim] if s == "agree")
        larger[claim] = max(agree, n - agree) / n if n else None
        if n < 10:
            rows.append(("CL-1", "open"))
        else:
            rows.append(("CL-1", "met" if larger[claim] <= 0.70 else "missed"))
    if len(sides["c1"]) < 10 or len(sides["c2"]) < 10:
        rows.append(("CL-7", "open"))
    else:
        gap = abs(larger["c1"] - larger["c2"]) * 100
        rows.append(("CL-7", "met" if gap <= 15 else "missed"))
    for claim in ("c1", "c2"):
        n = len(picks[claim])
        quick = sum(1 for p in picks[claim] if p <= 60)
        if n < 10:
            rows.append(("CL-10", "open"))
        else:
            rows.append(("CL-10", "met" if quick / n >= 0.9 else "missed"))
    rows.extend([("CL-5", "open"), ("CL-5", "open")])
    return rows, larger


def codebook_text(book):
    return "\n".join(f"| `{cid}` | {st}{q} |" for cid, (st, q) in sorted(book.items()))


def flipped(book, ids):
    out = dict(book)
    for cid in ids:
        st, q = out[cid]
        out[cid] = ("NA" if st == "A" else "A", q)
    return out


CODERS = [
    dict(name="two coders who agree on every card", two=dict(BOOK)),
    dict(name="one stance apart in each deck", two=flipped(BOOK, ["c1-03", "c2-11"])),
    dict(name="two apart in deck 1, none in deck 2", two=flipped(BOOK, ["c1-02", "c1-09"])),
    dict(name="a card coder 2 left out", two={k: v for k, v in BOOK.items() if k != "c2-05"}),
]


def coder_reference(one, two):
    out = []
    for claim in ("c1", "c2"):
        ids = [f"{claim}-{i:02d}" for i in range(1, 17)]
        missing = [c for c in ids if c not in one or c not in two]
        if missing:
            out.append(dict(verdict="open", missing=len(missing)))
            continue
        a = sum(1 for c in ids if one[c][0] == "A" and two[c][0] == "A")
        b = sum(1 for c in ids if one[c][0] == "A" and two[c][0] == "NA")
        cc = sum(1 for c in ids if one[c][0] == "NA" and two[c][0] == "A")
        d = sum(1 for c in ids if one[c][0] == "NA" and two[c][0] == "NA")
        k = kappa(a, b, cc, d)
        out.append(dict(verdict="met" if a + d >= 15 else "missed", agreed=a + d,
                        matrix=(a, b, cc, d), kappa=k["kappa"], po=k["po"], pe=k["pe"], missing=0))
    return out


# ---------------------------------------------------------------------- driver

def close(a, b):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return abs(a - b) < TOL


def main():
    verbose = "-v" in sys.argv
    if not PAGE.exists():
        sys.exit(f"no page at {PAGE}")
    if len(BOOK) != 32:
        sys.exit(f"the codebook holds {len(BOOK)} cards, not 32")

    fixtures = {
        "codebookText": CODEBOOK.read_text(encoding="utf-8"),
        "measures": [{"name": m["name"], "side": m["side"], "ids": m["ids"]} for m in MEASURES],
        "totals": TOTALS,
        "datasets": [{"name": d["name"], "lines": d["lines"]} for d in DATASETS],
        "kappas": KAPPAS,
        "coders": [{"name": c["name"], "one": codebook_text(BOOK), "two": codebook_text(c["two"])}
                   for c in CODERS],
        "promptClaim": "An SME should run its AI on small models it controls rather than on frontier models it rents.",
        "promptSide": "agree",
        "promptLocked": "Renting means the price and the model can both change under you.",
    }
    tmp = HERE / ".fixtures.json"
    tmp.write_text(json.dumps(fixtures), encoding="utf-8")
    try:
        got = json.loads(subprocess.run(
            ["node", str(HERE / "runpage.mjs"), str(tmp)],
            capture_output=True, text=True, check=True).stdout)
    except subprocess.CalledProcessError as e:
        sys.exit("the page would not run:\n" + e.stderr)
    finally:
        tmp.unlink(missing_ok=True)

    fails = []

    def check(label, want, have, dp=DP):
        ok = close(want, have) if isinstance(want, float) or isinstance(have, float) else want == have
        if not ok:
            fails.append(f"{label}: reference {want}, page {have}")
        if verbose:
            mark = "  " if ok else "!!"
            shown = f"{have:.{dp}f}" if isinstance(have, float) else have
            print(f"{mark} {label}: {shown}")

    check("codebook cards read by the page", 32, got["codebookCards"])

    print(f"\nMS-1, MS-2, MS-3 — ten sessions with known choices")
    for want, have in zip(MEASURES, got["measures"]):
        ref = measure(want["ids"], want["side"])
        n = want["name"]
        check(f"  {n}: opened", ref["opened"], have["opened"])
        check(f"  {n}: congenial", ref["congenial"], have["congenial"])
        check(f"  {n}: uncongenial", ref["uncongenial"], have["uncongenial"])
        check(f"  {n}: strong opposing", ref["strongOpposing"], have["strongOpposing"])
        check(f"  {n}: index", ref["index"], have["index"])
        if have["congenial"] + have["uncongenial"] != have["opened"]:
            fails.append(f"  {n}: opened is not congenial + uncongenial")

    print(f"\nMS-6 — the two closing totals")
    for want, have in zip(TOTALS, got["totals"]):
        check(f"  {want['name']}: workload 0-100", tlx_total(want["answers"]), have["tlx"])
        check(f"  {want['name']}: perception 2-14", perception_total(want["answers"]), have["q"])
        if not 0 <= have["tlx"] <= 100:
            fails.append(f"  {want['name']}: workload {have['tlx']} outside 0-100")
        if not 2 <= have["q"] <= 14:
            fails.append(f"  {want['name']}: perception {have['q']} outside 2-14")

    print(f"\nAN-1, AN-2, AN-4, AN-6 — {len(DATASETS)} classes")
    for ds, have in zip(DATASETS, got["datasets"]):
        n = ds["name"]
        check(f"  {n}: lines accepted", ds["n"], have["accepted"])
        check(f"  {n}: lines rejected", ds["bad"], have["rejected"])
        check(f"  {n}: pairs", ds["n"], have["pairs"])
        ref = paired(ds["diffs"])
        check(f"  {n}: mean with the assistant", sum(ds["ask"]) / ds["n"], have["meanAsk"])
        check(f"  {n}: mean without it", sum(ds["none"]) / ds["n"], have["meanNone"])
        check(f"  {n}: paired difference", ref["diff"], have["diff"])
        check(f"  {n}: sd of the differences", ref["sdDiff"], have["sdDiff"])
        check(f"  {n}: t at 95%", ref["tcrit"], have["tcrit"])
        check(f"  {n}: interval low", ref["lo"], have["lo"])
        check(f"  {n}: interval high", ref["hi"], have["hi"])
        # AN-4 allows 0.02 against a reference. The page solves the same
        # non-central t scipy does, so it is held to 3 decimal places instead,
        # and the 0.02 is checked as well in case that ever stops being true.
        exact = exact_mde(ds["n"])
        check(f"  {n}: smallest detectable effect", exact, have["dz"])
        gap = abs(exact - have["dz"])
        if gap > 0.02:
            fails.append(f"  {n}: detectable effect is {gap:.4f} from the exact {exact:.4f}, over AN-4's 0.02")

    print(f"\nAN-6 — a line that will not parse is listed back")
    bad = got["datasets"][1]
    if bad["rejected"] != 2:
        fails.append(f"  expected 2 rejections, got {bad['rejected']}")
    for r in bad["rejectReasons"]:
        if not r["why"]:
            fails.append("  a rejection carries no reason")
        if verbose:
            print(f"   line {r['n']}: {r['why']}")

    print(f"\nAN-5, AN-7 — four 2x2 matrices")
    for want, have in zip(KAPPAS, got["kappas"]):
        ref = kappa(want["a"], want["b"], want["c"], want["d"])
        check(f"  {want['name']}: pairs", ref["n"], have["n"])
        check(f"  {want['name']}: observed agreement", ref["po"], have["po"])
        check(f"  {want['name']}: chance agreement", ref["pe"], have["pe"])
        check(f"  {want['name']}: kappa", ref["kappa"], have["kappa"])

    print(f"\nPhase 0 — the pilot audit over six rooms")
    for ds, have in zip(DATASETS, got["datasets"]):
        n = ds["name"]
        ref_rows, larger = pilot_reference(ds["sides"], ds["picks"])
        have_rows = [(r["rule"], r["verdict"]) for r in have["audit"]["rows"]]
        check(f"  {n}: seven criteria, in order, each with its verdict", ref_rows, have_rows)
        for claim in ("c1", "c2"):
            check(f"  {n}: larger side, {claim}", larger[claim], have["audit"]["split"][claim]["larger"])
    verdicts = {v for ds in DATASETS for _, v in pilot_reference(ds["sides"], ds["picks"])[0][:5]}
    if verdicts != {"met", "missed", "open"}:
        fails.append(f"  the rooms only ever produce {sorted(verdicts)}; each of met, missed and open must appear")

    print(f"\nPhase 0 — CL-5, two coders over {len(CODERS)} pairs of codebooks")
    for want, have in zip(CODERS, got["coders"]):
        n = want["name"]
        ref = coder_reference(BOOK, want["two"])
        for i, (r, h) in enumerate(zip(ref, have["decks"])):
            check(f"  {n}: deck {i + 1} verdict", r["verdict"], h["verdict"])
            check(f"  {n}: deck {i + 1} cards missing", r["missing"], h["missing"])
            if r["verdict"] != "open":
                check(f"  {n}: deck {i + 1} stances agreed", r["agreed"], h["agreed"])
                check(f"  {n}: deck {i + 1} matrix", list(r["matrix"]), h["matrix"])
                check(f"  {n}: deck {i + 1} observed agreement", r["po"], h["po"])
                check(f"  {n}: deck {i + 1} chance agreement", r["pe"], h["pe"])
                check(f"  {n}: deck {i + 1} kappa", r["kappa"], h["kappa"])

    print()
    if fails:
        print(f"{len(fails)} disagreement(s):")
        for f in fails:
            print("  " + f)
        return 1
    print("Every fixture matches the reference to 3 decimal places.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
