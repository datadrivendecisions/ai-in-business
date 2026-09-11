"""The build plan's gates, one function each: python3 gates.py N

Every gate is a command with an exit code, run against fixtures that are not
student work. A gate that needs a person to interpret it is not a gate. Gates
1–4 build a throw-away intake root under a temporary directory; gate 0 looks at
the real one, because it checks the layout and nothing else.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_ROOT = pathlib.Path.home() / "Documents/HAN/M3DM/ai-in-business-intake"

# The tree in blueprint §5, as the entries the root must and must not have.
MUST = ["README.md", "roster.tsv", "log.tsv", "rubric", "inbox", "teams", "rubric/prd-scoresheet.md"]
MUST_NOT_MATCH = ("week-",)  # per-week folders at the root are the old layout


def say(ok, what):
    print(f"  {'ok  ' if ok else 'FAIL'} {what}")
    return ok


def gate_0(root=DEFAULT_ROOT):
    """Layout of the intake root, the roster's shape, the fixtures README."""
    print(f"gate 0 — ground, at {root}")
    ok = True
    for rel in MUST:
        ok &= say((root / rel).exists(), f"{rel} exists")
    stray = [p.name for p in root.iterdir() if p.name.startswith(MUST_NOT_MATCH)]
    ok &= say(not stray, f"no per-week folder at the root {stray or ''}")

    lines = [l.rstrip("\n") for l in (root / "roster.tsv").read_text(encoding="utf-8").splitlines()]
    rows = [l for l in lines if l.strip() and not l.startswith("#")]
    ok &= say(rows and rows[0].split("\t") == ["team", "names", "channel"], "roster header is team/names/channel")
    teams = [r.split("\t") for r in rows[1:]]
    bad = [r for r in teams if len(r) != 3 or not all(c.strip() for c in r)]
    ok &= say(not bad, f"every roster line has team, names and channel ({len(teams)} team(s); the owner fills these in)")

    readme = (REPO / "project-documentation/test-fixtures/README.md").read_text(encoding="utf-8")
    for needle in ("prd-socratic-gate.md", "blueprint-socratic-workflow.html", "pull only"):
        ok &= say(needle in readme, f"fixtures README names {needle}")
    ok &= say((REPO / "project-documentation/test-fixtures/pipeline-log.md").exists(), "pipeline-log.md exists")
    return ok


GATES = {0: gate_0}


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) not in GATES:
        print(f"usage: gates.py N   (N in {sorted(GATES)})", file=sys.stderr)
        return 2
    passed = GATES[int(sys.argv[1])]()
    print("PASSED" if passed else "FAILED")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
