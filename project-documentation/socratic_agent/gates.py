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


def scratch_root():
    """A throw-away intake root with the phase-0 layout, under a temp dir."""
    import tempfile
    root = pathlib.Path(tempfile.mkdtemp(prefix="intake-gate-"))
    for d in ("rubric", "inbox", "teams"):
        (root / d).mkdir()
    (root / "README.md").write_text("scratch root for a gate\n")
    (root / "roster.tsv").write_text("team\tnames\tchannel\n")
    (root / "log.tsv").write_text("")
    (root / "rubric/prd-scoresheet.md").write_text("# scratch sheet\n")
    return root


def mini_pdf(lines):
    """A one-page PDF with the given lines, valid enough for pdftotext."""
    content = "BT /F1 12 Tf 50 750 Td 14 TL " + " ".join(
        "(" + l.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") + ") Tj T*" for l in lines) + " ET"
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        f"<< /Length {len(content)} >>\nstream\n{content}\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = "%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{o}\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n" + "".join(f"{o:010d} 00000 n \n" for o in offsets)
    out += f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    return out.encode("latin-1")


def run(root, week, *extra):
    import subprocess
    r = subprocess.run([sys.executable, str(pathlib.Path(__file__).with_name("run_documents.py")),
                        "--week", str(week), "--root", str(root), *extra],
                       capture_output=True, text=True)
    print("    " + r.stdout.strip().replace("\n", "\n    "))
    return r.returncode


def gate_1():
    """Intake: five awkward files, three runs, and the exact state after each."""
    import subprocess
    root = scratch_root()
    print(f"gate 1 — intake, scratch root {root}")
    inbox = root / "inbox"
    (inbox / "Team 3 PRD.pdf").write_bytes(mini_pdf(["Team three PRD", "Problem: owners cannot find vetted guidance."]))
    src = inbox / "t05.txt"
    src.write_text("Team five PRD.\nUsers: the four of us as researchers.\n")
    subprocess.run(["textutil", "-convert", "docx", "-output", str(inbox / "t05_prd.docx"), str(src)], check=True)
    src.unlink()
    (inbox / "prd-final.pdf").write_bytes(mini_pdf(["A PRD with no team in its name."]))
    (inbox / "team-03-prd-v2.md").write_text("# Team 3 PRD, second try\n\nSharper problem statement.\n")
    (inbox / "team-04-prd.pdf").write_text("this is not a PDF at all\n")

    ok = True
    print("  run 1")
    code = run(root, 1, "--step", "intake")
    t3, t4, t5 = (root / "teams" / t / "week-01" for t in ("team-03", "team-04", "team-05"))
    ok &= say(code == 1, f"exit 1 (got {code})")
    ok &= say((t3 / "team-03-week-01-prd-original.pdf").exists() and (t3 / "team-03-week-01-prd.txt").exists(), "Team 3 PRD.pdf filed and converted")
    ok &= say((t3 / "team-03-week-01-prd-v2.md").exists() and (t3 / "team-03-week-01-prd-v2.txt").exists(), "team-03-prd-v2.md filed as -v2 and converted")
    ok &= say((t5 / "team-05-week-01-prd-original.docx").exists() and "Team five" in (t5 / "team-05-week-01-prd.txt").read_text(), "t05_prd.docx filed and converted")
    ok &= say((t4 / "team-04-week-01-prd-original.pdf").exists() and not (t4 / "team-04-week-01-prd.txt").exists(), "the non-PDF is filed but not converted")
    ok &= say((inbox / "prd-final.pdf").exists(), "prd-final.pdf stays in the inbox")
    man = (inbox / "manifest.tsv").read_text() if (inbox / "manifest.tsv").exists() else ""
    ok &= say("\t\tprd\tprd-final.pdf" in man or "\tprd\tprd-final.pdf" in man, "manifest has prd-final.pdf with an empty team cell")
    docs3 = (root / "teams/team-03/documents.tsv").read_text()
    ok &= say("\t2\t" in docs3 and docs3.count("\nprd\t") == 1, "team-03 documents.tsv holds one prd line, at version 2")
    log_lines = (root / "log.tsv").read_text().count("\n")
    ok &= say(log_lines == 5, f"log.tsv has header + 4 moves ({log_lines} lines)")

    print("  run 2 — manifest corrected")
    (inbox / "manifest.tsv").write_text("team\tdeliverable\tfile\tnote\nteam-06\tprd\tprd-final.pdf\t\n")
    code = run(root, 1, "--step", "intake")
    ok &= say(code == 0, f"exit 0 (got {code})")
    ok &= say((root / "teams/team-06/week-01/team-06-week-01-prd.txt").exists(), "prd-final.pdf filed as team-06 and converted")
    ok &= say((root / "log.tsv").read_text().count("\n") == 6, "log.tsv gained exactly one line")
    ok &= say((root / "teams/team-06/documents.tsv").read_text().count("\nprd\t") == 1, "team-06 documents.tsv has one line")
    ok &= say(not (inbox / "manifest.tsv").exists() or (inbox / "manifest.tsv").read_text().count("\n") <= 2, "manifest is empty")

    print("  run 3 — nothing to do")
    snapshot = {p: p.stat().st_mtime_ns for p in root.rglob("*") if p.is_file()}
    code = run(root, 1, "--step", "intake")
    ok &= say(code == 2, f"exit 2 (got {code})")
    ok &= say(snapshot == {p: p.stat().st_mtime_ns for p in root.rglob("*") if p.is_file()}, "no file changed")
    return ok


def gate_2():
    """Scorer: the gate's own PRD scored; a document without a sheet named, not scored."""
    import hashlib
    real_sheet = DEFAULT_ROOT / "rubric/prd-scoresheet.md"
    if not real_sheet.exists():
        print(f"gate 2 needs the real sheet at {real_sheet}; it is outside the repository")
        return False
    root = scratch_root()
    (root / "rubric/prd-scoresheet.md").write_bytes(real_sheet.read_bytes())
    print(f"gate 2 — scorer, scratch root {root}")
    (root / "inbox/team-03-prd.md").write_bytes((REPO / "project-documentation/prd-socratic-gate.md").read_bytes())
    (root / "inbox/team-03-blueprint.html").write_bytes(
        (REPO / "work/drafts/blueprint-socratic-workflow.html").read_bytes())
    ok = True
    print("  intake")
    ok &= say(run(root, 1, "--step", "intake") == 0, "both fixtures filed and converted")

    print("  run 1 — score")
    code = run(root, 1, "--step", "score")
    score = root / "teams/team-03/week-01/owners/score-prd.md"
    ok &= say(code == 1, f"exit 1, because the blueprint has no sheet (got {code})")
    ok &= say(score.exists(), "owners/score-prd.md written")
    text = score.read_text() if score.exists() else ""
    head = text.split("---\n\n", 1)[0]
    ok &= say(text.startswith("---\n") and all(k in head for k in ("criteria: site/prd-criteria.html @", "sheet: rubric/prd-scoresheet.md sha256", "version: 1")),
              "provenance header carries criteria commit, sheet hash and version")
    ok &= say("## RETURNED" in text or ("## SCORESHEET" in text and "## BEFORE V1" in text), "required headings present")
    ok &= say(not (root / "teams/team-03/week-01/owners/score-blueprint.md").exists(), "nothing written for the blueprint")
    print("    headings found:", ", ".join(h for h in ("## RETURNED", "## SCORESHEET", "## BEFORE V1") if h in text))
    print("    header:\n      " + head.strip().replace("\n", "\n      "))

    print("  run 2 — skip")
    before = hashlib.sha256(score.read_bytes()).hexdigest() if score.exists() else ""
    code = run(root, 1, "--step", "score")
    ok &= say(code == 1, f"exit 1 again: the blueprint is still unscored (got {code})")
    ok &= say(score.exists() and hashlib.sha256(score.read_bytes()).hexdigest() == before, "score-prd.md unchanged")
    return ok


GATES = {0: gate_0, 1: gate_1, 2: gate_2}


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) not in GATES:
        print(f"usage: gates.py N   (N in {sorted(GATES)})", file=sys.stderr)
        return 2
    passed = GATES[int(sys.argv[1])]()
    print("PASSED" if passed else "FAILED")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
