"""Collect a week's hand-ins and turn them into plain text the gate can read.

The deployed gate fetches a public page (ADR-0014, "pull only"). This does the
other thing: it takes files a team handed in — PDF, Word, Markdown, HTML — and
normalises them, so the agent receives full text rather than a URL.

The files live outside the repository, and that is deliberate. ai-in-business is
public, and student work is not; a .gitignore inside the repo is one `git add -A`
away from failing. Default root is ../ai-in-business-intake, a sibling.

No dependencies: pdftotext (poppler) for PDF, textutil (macOS) for Word and RTF,
the standard library for the rest. Anything it cannot convert it names rather
than skips silently, because a hand-in that vanishes between the inbox and the
run is the one failure nobody notices.

    python3 intake.py --week 1
    python3 intake.py --week 1 --root /some/other/place
"""

import argparse
import pathlib
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser

DEFAULT_ROOT = pathlib.Path.home() / "Documents/HAN/M3DM/ai-in-business-intake"

# Word and RTF go through textutil, which ships with macOS. PDF needs poppler.
CONVERTERS = {
    ".pdf": "pdftotext",
    ".docx": "textutil", ".doc": "textutil", ".rtf": "textutil", ".odt": "textutil",
    ".md": "copy", ".markdown": "copy", ".txt": "copy",
    ".html": "html", ".htm": "html",
}

SKIP_TAGS = {"script", "style", "head"}


class Text(HTMLParser):
    """Tag-stripper. Mirrors the one in agent.py rather than adding bs4."""

    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
        elif tag in ("p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data)

    def text(self):
        return re.sub(r"\n{3,}", "\n\n", "".join(self.parts)).strip()


def convert(src: pathlib.Path, dst: pathlib.Path) -> str:
    """Write src as plain text at dst. Returns "" on success, else the reason."""
    how = CONVERTERS.get(src.suffix.lower())
    if how is None:
        return f"geen converter voor {src.suffix or '(geen extensie)'}"
    try:
        if how == "pdftotext":
            # -layout keeps tables and headings readable rather than reflowing
            # them into one column, which matters for a PRD full of lists.
            r = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(src), str(dst)],
                               capture_output=True, text=True, timeout=120)
            if r.returncode:
                return (r.stderr or "pdftotext faalde").strip().splitlines()[-1]
        elif how == "textutil":
            r = subprocess.run(["textutil", "-convert", "txt", "-encoding", "UTF-8",
                                "-output", str(dst), str(src)],
                               capture_output=True, text=True, timeout=120)
            if r.returncode:
                return (r.stderr or "textutil faalde").strip().splitlines()[-1]
        elif how == "copy":
            shutil.copyfile(src, dst)
        elif how == "html":
            p = Text()
            p.feed(src.read_text(encoding="utf-8", errors="replace"))
            dst.write_text(p.text(), encoding="utf-8")
    except FileNotFoundError:
        return f"{how} niet geïnstalleerd"
    except subprocess.TimeoutExpired:
        return "conversie liep vast (120s)"
    except Exception as e:  # noqa: BLE001 — one bad file must not stop the batch
        return f"{type(e).__name__}: {e}"

    if not dst.exists() or not dst.stat().st_size:
        return "conversie gaf lege tekst"
    return ""


def guess_team(name: str) -> str:
    """Pull a team number out of a filename. Students name files anything, so
    this is a first guess the manifest lets you correct, never an answer."""
    # \b after the digits fails on "t05_prd": underscore is a word character, so
    # there is no boundary between "5" and "_". Look ahead for a non-digit instead.
    m = (re.search(r"team[\s_-]*0*(\d{1,2})(?!\d)", name, re.I)
         or re.search(r"(?:^|[^a-z0-9])t0*(\d{1,2})(?!\d)", name, re.I))
    return f"team-{int(m.group(1)):02d}" if m else ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT)
    ap.add_argument("--deliverable", default="prd", help="prd, proposal, … (naamdeel)")
    a = ap.parse_args()

    week = a.root / f"week-{a.week:02d}"
    inbox, out = week / "inbox", week / "text"
    if not inbox.is_dir():
        print(f"Geen inbox: {inbox}\nMaak hem aan en zet de bestanden erin.", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in inbox.iterdir() if p.is_file() and not p.name.startswith("."))
    if not files:
        print(f"Inbox is leeg: {inbox}")
        return 1

    # text/ is derived from inbox/, so regenerate it rather than adding to it.
    # Without this a second run appends -2, -3 copies of documents that have not
    # changed, and the run silently doubles.
    for stale in out.glob("*.txt"):
        stale.unlink()

    rows, failed = [], []
    for src in files:
        team = guess_team(src.name)
        stem = f"week-{a.week:02d}-{team or 'ONBEKEND'}-{a.deliverable}"
        dst = out / f"{stem}.txt"
        n = 2
        while dst.exists():  # two hand-ins from one team must not overwrite
            dst, n = out / f"{stem}-{n}.txt", n + 1
        reason = convert(src, dst)
        if reason:
            failed.append((src.name, reason))
        else:
            words = len(dst.read_text(encoding="utf-8", errors="replace").split())
            rows.append((team, src.name, dst.name, words))
            print(f"  {'?' if not team else team:8s} {src.name}  →  {dst.name}  ({words} woorden)")

    man = week / "manifest.tsv"
    with man.open("w", encoding="utf-8") as f:
        f.write("# corrigeer de teamkolom waar hij leeg of fout is; regels met een leeg team worden niet gedraaid\n")
        f.write("team\tbron\ttekst\twoorden\n")
        for team, src, dst, words in rows:
            f.write(f"{team}\t{src}\t{dst}\t{words}\n")

    print(f"\n{len(rows)} van {len(files)} omgezet → {out}")
    if failed:
        print("\nNiet omgezet:")
        for name, reason in failed:
            print(f"  {name}: {reason}")
    unknown = [r for r in rows if not r[0]]
    if unknown:
        print(f"\n{len(unknown)} bestand(en) zonder herkenbaar team. Vul de teamkolom in:\n  {man}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
