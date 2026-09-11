"""One command a week: take a team's hand-ins from the inbox to a message the team can be sent.

    python3 run_documents.py --week 2
    python3 run_documents.py --week 2 --step intake
    python3 run_documents.py --week 2 --team team-03 --root /some/other/place

Four steps, in order: intake → score → coherence (from week 2) → question, then a
lint on the message. Each step runs where its input exists and its output does
not, so a run that stops can be started again and picks up where it broke — the
presence of a file is the signal from one step to the next. There is no queue,
no status and no clock kept anywhere else.

Everything this writes goes to the intake root, a sibling of the repository and
never inside it: the repository is public and student work is not. The design is
in project-documentation/hand-in-pipeline.md and the two drafts beside it; this
file is its step 1, with the later steps arriving one phase at a time.

Exit codes: 0 every team done · 1 something unscored, unconverted or failed lint,
named in the output · 2 nothing to do.
"""

import argparse
import datetime as dt
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser

DEFAULT_ROOT = pathlib.Path.home() / "Documents/HAN/M3DM/ai-in-business-intake"

# The six documents of ADR-0010's spine, and the names students actually give
# their files. Order matters where one alias contains another: 'plan' alone is
# not listed, because a build plan and a knowledge plan would both match it.
DELIVERABLES = {
    "prd": ["prd", "product requirements", "requirements"],
    "blueprint": ["blueprint", "blauwdruk", "technical design", "technisch ontwerp"],
    "knowledge": ["knowledge", "kennis", "knowledge architecture", "kennisarchitectuur"],
    "buildplan": ["buildplan", "build plan", "build-plan", "bouwplan"],
    "eval": ["eval", "evaluation", "evaluatie"],
    "decisions": ["decisions", "decision log", "decision-log", "besluiten", "beslissingen", "decisionlog"],
}

# Word and RTF go through textutil, which ships with macOS. PDF needs poppler.
CONVERTERS = {
    ".pdf": "pdftotext",
    ".docx": "textutil", ".doc": "textutil", ".rtf": "textutil", ".odt": "textutil",
    ".md": "copy", ".markdown": "copy", ".txt": "copy",
    ".html": "html", ".htm": "html",
}

MANIFEST_HEADER = ["team", "deliverable", "file", "note"]
DOCUMENTS_HEADER = ["deliverable", "week", "version", "original", "text"]
LOG_HEADER = ["when", "team", "week", "deliverable", "from", "to", "sha256"]


# ----------------------------------------------------------------------------
# small shared helpers
# ----------------------------------------------------------------------------

def read_tsv(path, header):
    """Rows of a TSV as dicts, skipping blanks and # comments. Missing file → []."""
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        cells = line.rstrip("\n").split("\t")
        if cells == header:
            continue
        cells += [""] * (len(header) - len(cells))
        rows.append(dict(zip(header, cells)))
    return rows


def write_tsv(path, header, rows, comment=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        if comment:
            f.write(f"# {comment}\n")
        f.write("\t".join(header) + "\n")
        for r in rows:
            f.write("\t".join(str(r.get(k, "")) for k in header) + "\n")


def append_tsv(path, header, row):
    new = not path.exists() or not path.stat().st_size
    with path.open("a", encoding="utf-8") as f:
        if new:
            f.write("\t".join(header) + "\n")
        f.write("\t".join(str(row.get(k, "")) for k in header) + "\n")


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


# ----------------------------------------------------------------------------
# step 1 — intake
# ----------------------------------------------------------------------------

class _Text(HTMLParser):
    """Tag-stripper for HTML hand-ins. Mirrors agent.py rather than adding bs4."""

    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "head"):
            self.skip += 1
        elif tag in ("p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data)

    def text(self):
        return re.sub(r"\n{3,}", "\n\n", "".join(self.parts)).strip()


def guess_team(name):
    """A team number from a file name. Students name files anything, so this is
    a first guess the manifest lets the lecturer correct, never an answer."""
    m = (re.search(r"team[\s_-]*0*(\d{1,2})(?!\d)", name, re.I)
         or re.search(r"(?:^|[^a-z0-9])t0*(\d{1,2})(?!\d)", name, re.I))
    return f"team-{int(m.group(1)):02d}" if m else ""


def guess_deliverable(name):
    low = name.lower()
    hits = [(len(alias), did) for did, aliases in DELIVERABLES.items()
            for alias in aliases if alias in low]
    return max(hits)[1] if hits else ""  # the longest alias wins


def convert(src, dst):
    """Write src as plain text at dst. Returns "" on success, else the reason."""
    how = CONVERTERS.get(src.suffix.lower())
    if how is None:
        return f"no converter for {src.suffix or '(no extension)'}"
    try:
        if how == "pdftotext":
            r = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(src), str(dst)],
                               capture_output=True, text=True, timeout=120)
            if r.returncode:
                return (r.stderr or "pdftotext failed").strip().splitlines()[-1]
        elif how == "textutil":
            r = subprocess.run(["textutil", "-convert", "txt", "-encoding", "UTF-8",
                                "-output", str(dst), str(src)],
                               capture_output=True, text=True, timeout=120)
            if r.returncode:
                return (r.stderr or "textutil failed").strip().splitlines()[-1]
        elif how == "copy":
            shutil.copyfile(src, dst)
        elif how == "html":
            p = _Text()
            p.feed(src.read_text(encoding="utf-8", errors="replace"))
            dst.write_text(p.text(), encoding="utf-8")
    except FileNotFoundError:
        return f"{how} is not installed"
    except subprocess.TimeoutExpired:
        return "conversion hung (120s)"
    except Exception as e:  # noqa: BLE001 — one bad file must not stop the batch
        return f"{type(e).__name__}: {e}"
    if not dst.exists() or not dst.stat().st_size:
        return "conversion produced no text"
    return ""


def next_original(week_dir, stem, ext):
    """`<stem>-original<ext>`, or `-v2`, `-v3`… when a version already exists.
    Versions are counted across extensions: a PDF followed by a Markdown file of
    the same deliverable is v1 and v2, not two originals. Returns (path, version)."""
    if not list(week_dir.glob(f"{stem}-original.*")) and not list(week_dir.glob(f"{stem}-v*.*")):
        return week_dir / f"{stem}-original{ext}", 1
    n = 2
    while list(week_dir.glob(f"{stem}-v{n}.*")):
        n += 1
    return week_dir / f"{stem}-v{n}{ext}", n


def step_intake(root, week, only_team=None):
    """inbox/ → teams/<team>/week-NN/, converted. Returns (done, problems)."""
    inbox = root / "inbox"
    manifest_path = inbox / "manifest.tsv"
    if not inbox.is_dir():
        return [], [f"no inbox at {inbox}"]

    known = {r["file"]: r for r in read_tsv(manifest_path, MANIFEST_HEADER)}
    files = sorted(p for p in inbox.iterdir()
                   if p.is_file() and not p.name.startswith(".") and p.name != manifest_path.name)
    done, problems, still = [], [], []

    for src in files:
        row = known.get(src.name, {"team": "", "deliverable": "", "file": src.name, "note": ""})
        team = row["team"].strip() or guess_team(src.name)
        deliv = row["deliverable"].strip() or guess_deliverable(src.name)
        if deliv and deliv not in DELIVERABLES:
            row["note"] = f"unknown deliverable '{deliv}'; one of {', '.join(DELIVERABLES)}"
            deliv = ""
        if only_team and team != only_team:
            still.append({**row, "team": team, "deliverable": deliv})
            continue
        if not team or not deliv:
            row.update(team=team, deliverable=deliv)
            row["note"] = row["note"] or ("fill in " + " and ".join(
                k for k, v in (("team", team), ("deliverable", deliv)) if not v))
            still.append(row)
            problems.append(f"{src.name}: {row['note']} (stays in inbox)")
            continue

        # move, with the hash as the test that the bytes arrived
        week_dir = root / "teams" / team / f"week-{week:02d}"
        week_dir.mkdir(parents=True, exist_ok=True)
        stem = f"{team}-week-{week:02d}-{deliv}"
        dst, version = next_original(week_dir, stem, src.suffix.lower())
        before = sha256(src)
        shutil.move(str(src), str(dst))
        if sha256(dst) != before:
            problems.append(f"{src.name}: hash changed in the move to {dst} — check it by hand")
            continue
        append_tsv(root / "log.tsv", LOG_HEADER, {
            "when": now(), "team": team, "week": week, "deliverable": deliv,
            "from": src.name, "to": str(dst.relative_to(root)), "sha256": before})

        # convert from the team folder, never from the inbox
        txt = week_dir / (f"{stem}.txt" if version == 1 else f"{stem}-v{version}.txt")
        reason = convert(dst, txt)
        docs_path = root / "teams" / team / "documents.tsv"
        docs = [r for r in read_tsv(docs_path, DOCUMENTS_HEADER) if r["deliverable"] != deliv]
        docs.append({"deliverable": deliv, "week": week, "version": version,
                     "original": str(dst.relative_to(root)),
                     "text": "" if reason else str(txt.relative_to(root))})
        write_tsv(docs_path, DOCUMENTS_HEADER, sorted(docs, key=lambda r: r["deliverable"]),
                  comment="the current version of each deliverable; rewritten by intake, read by the later steps")
        if reason:
            problems.append(f"{src.name} → {dst.name}: filed but not converted: {reason}")
        else:
            words = len(txt.read_text(encoding="utf-8", errors="replace").split())
            done.append(f"{team} {deliv} v{version}: {src.name} → {txt.name} ({words} words)")

    # Rewrite the manifest only when it would change: a run that did nothing
    # must leave nothing touched, or "no file changed" stops meaning anything.
    if still:
        wanted = manifest_text(still)
        if not manifest_path.exists() or manifest_path.read_text(encoding="utf-8") != wanted:
            manifest_path.write_text(wanted, encoding="utf-8")
    elif manifest_path.exists():
        manifest_path.unlink()
    return done, problems


def manifest_text(rows):
    lines = ["# files still in the inbox; fill in an empty team or deliverable cell and run again",
             "\t".join(MANIFEST_HEADER)]
    lines += ["\t".join(str(r.get(k, "")) for k in MANIFEST_HEADER) for r in rows]
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------
# later steps — arriving one phase at a time
# ----------------------------------------------------------------------------

def step_not_built(name):
    def run(root, week, only_team=None):
        print(f"  step {name}: not built yet")
        return [], []
    return run


STEPS = [
    ("intake", step_intake),
    ("score", step_not_built("score")),
    ("coherence", step_not_built("coherence")),
    ("question", step_not_built("question")),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT)
    ap.add_argument("--team", help="only this team, e.g. team-03")
    ap.add_argument("--step", choices=[n for n, _ in STEPS] + ["all"], default="all")
    a = ap.parse_args()

    if not a.root.is_dir():
        print(f"no intake root at {a.root}", file=sys.stderr)
        return 2

    all_done, all_problems = [], []
    for name, fn in STEPS:
        if a.step not in ("all", name):
            continue
        print(f"step {name}")
        done, problems = fn(a.root, a.week, a.team)
        for line in done:
            print(f"  {line}")
        for line in problems:
            print(f"  ! {line}")
        all_done += done
        all_problems += problems

    print()
    if all_problems:
        print(f"{len(all_done)} done, {len(all_problems)} problem(s) named above.")
        return 1
    if not all_done:
        print("Nothing to do.")
        return 2
    print(f"{len(all_done)} done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
