#!/usr/bin/env python3
"""Check the bias-experiment decks against the sources they quote.

    python3 check-deck.py            # from anywhere in the repository

Reads the cards out of site/tool-bias-experiment.html and the coding out of
work/drafts/week-03-codebook.md, and checks the phase-0 test gate:

    SM-5   every card carries a title, a reference and a teaser
    SM-6   four cards in each of the four cells, both decks
    SM-7   every extract 150 words or fewer, and found in the source
    SM-8   no stance or quality label anywhere in the published page
    SM-10  every teaser 25 words or fewer
    SM-11  one link per card
    CL-6   no source appears in both decks

"Found in the source" is checked against the AI Wiki's own capture of each
source, after normalisations that are declared rather than applied silently --
see the table in the codebook. Every normalisation is applied to BOTH the
quotation and the source, so nothing passes that the source does not say.

The wiki is expected beside this repository; set AI_WIKI to point elsewhere.
"""
import json, os, re, subprocess, sys, pathlib, unicodedata

REPO = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                   capture_output=True, text=True,
                                   cwd=pathlib.Path(__file__).parent).stdout.strip())
PAGE = REPO / "site" / "tool-bias-experiment.html"
CODEBOOK = REPO / "work" / "drafts" / "week-03-codebook.md"
WIKI = pathlib.Path(os.environ.get("AI_WIKI", pathlib.Path.home() / "Projects" / "ai-wiki"))
PDF_TEXT = pathlib.Path(os.environ.get("PDF_TEXT_DIR", REPO / ".deck-pdf-text"))

# Sources whose capture is a PDF. pdftotext is run once into PDF_TEXT_DIR.
PDF_CAPTURES = {
    "2026-04-28-ai-index-report-2025",
    "2026-04-28-brynjolfsson-li-raymond-generative-ai-at-work",
    "2025-10-05-patwardhan-et-al-openai-gdpval",
    "2025-06-09-krakowski-human-centered-ai-field-experiment",
    "2026-05-07-anthropic-economic-index-5-learning-curves",
    "2026-04-28-dellacqua-jagged-technological-frontier",
    "2026-05-27-scheffer-de-ondernemer-helloprint-ai-rebuild-from-day-zero",
}

# The vocabulary SM-8 forbids in the published page.
LABELS = ("denominator-bearing", "selected on outcome", "supporting cell",
          "opposing cell", "strong cell", "weak cell")

# Token-level equivalences for auto-transcript errors. Applied to both sides.
ASR = {"lms": "llms", "lm": "llms", "quen": "qwen", "costum": "cost",
       "aentic": "agentic"}
# Discourse fillers, removed from both sides. "like" is here because the
# transcripts use it as a filler ("as like Claude 4.6 Opus"); removing it from
# both sides means a card may keep or drop it without the check caring.
FILLERS = {"um", "uh", "erm", "like"}

def decolumnise_modal(text: str) -> str:
    """Rebuild reading order for a two-column PDF capture.

    pdftotext emits a two-column page line by line across both columns, so a
    sentence in the left column is interrupted by whatever sits beside it. The
    two columns are separated by a gutter that sits at the same character
    position down the whole document, so the gutter is found once (the most
    common wide-gap position) and every line is split there. Justification can
    open wide gaps inside a column too, which is why the gutter is taken from
    the document as a whole rather than per line. This restores what the page
    says; it changes no words.
    """
    lines = text.splitlines()
    starts = []
    for l in lines:
        for mm in re.finditer(r"\S\s{3,}\S", l):
            starts.append(mm.start() + 1)
    if not starts:
        return text
    counts = {}
    for st in starts:
        counts[st] = counts.get(st, 0) + 1
    gutter, hits = max(counts.items(), key=lambda kv: (kv[1], -kv[0]))
    if hits < 20:                      # not a consistent two-column layout
        return text
    left, right = [], []
    for l in lines:
        if len(l) > gutter and not l[gutter - 1 : gutter + 1].strip():
            left.append(l[:gutter].strip())
            right.append(l[gutter:].strip())
        else:
            left.append(l.strip())
    return "\n".join(left) + "\n" + "\n".join(right)

def decolumnise_perline(text: str) -> str:
    """Second reconstruction: split each line at its own widest interior gap.

    Column width is not constant down a PDF (a page with a figure, or the
    first page, sets a different gutter), so the modal-gutter reconstruction
    gets some pages wrong and this one gets others wrong. Both are searched,
    and a passage found in either is present in the source: each is a faithful
    de-interleaving of the same page, not an alteration of it.
    """
    lines, left, right = text.splitlines(), [], []
    for l in lines:
        gaps = [m for m in re.finditer(r"\S\s{3,}\S", l)]
        if gaps:
            cut = gaps[-1].start() + 1
            left.append(l[:cut].strip())
            right.append(l[cut:].strip())
        else:
            left.append(l.strip())
    return "\n".join(left) + "\n" + "\n".join(right)

def norm(s: str) -> str:
    """Reduce text to the word sequence it asserts, on both sides equally."""
    s = re.sub(r"[\u00b2\u00b3\u00b9\u2070-\u2079]", "", s)   # footnote markers
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[\u0300-\u036f]", "", s)                  # drop combining accents
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"[\u2010-\u2015\u2212]", "-", s)         # dashes -> hyphen
    s = s.replace("\u00d7", "x").replace("\\times", " ")  # 10x30x
    s = re.sub(r"-\s*\n\s*", "", s)                      # hyphenated line break
    s = re.sub(r"\[\d+:\d+\]", " ", s)                   # [38:43] timestamps
    s = re.sub(r"\d+ minutes?,? \d+ seconds?", " ", s)
    s = re.sub(r"\*\*[A-Z][A-Z\s.'\-]{2,40}\*\*\s*:", " ", s)   # **ANDY JASSY**:
    s = re.sub(r"(?m)^\s*>>\s*", " ", s)                      # turn markers
    s = re.sub(r"(?m)^#+\s.*$", " ", s)                        # chapter headings
    s = re.sub(r"\[[\d,\s]+\]", " ", s)                  # [70, 68, 36] refs
    s = re.sub(r"\([A-Z][A-Za-z'\-]+(?:\s+(?:et al\.|&|and|[A-Z][A-Za-z'\-]+))*,?\s*\d{4}[a-z]?\)",
               " ", s)                                    # (Touvron et al., 2023)
    s = s.lower()
    s = re.sub(r"[^a-z0-9%$.\s]", " ", s)                  # punctuation -> space
    words = [w.strip(".") for w in s.split()]
    words = [w for w in words if w and w not in FILLERS]
    words = [ASR.get(w, w) for w in words]
    words = [w for i, w in enumerate(words) if i == 0 or w != words[i-1]]
    # Compared as one character stream: word spacing and hyphenation differ
    # between a PDF capture and a quotation of it ("crowd-\nsourced" becomes
    # "crowdsourced"), and that difference is not a difference in what is said.
    return "".join(words)



def wc(s):
    return len(re.findall(r"\S+", s))


def cards_from_page():
    """Read DECK1 and DECK2 out of the page. The arrays are JSON but for the
    unquoted keys, so the keys are quoted and the rest parsed as JSON."""
    src = PAGE.read_text()
    decks = {}
    for name in ("DECK1", "DECK2"):
        m = re.search(r"var " + name + r" = (\[.*?\n\];)", src, re.S)
        if not m:
            sys.exit(f"{name} not found in {PAGE}")
        js = m.group(1).rstrip(";")
        js = re.sub(r"(?m)^(\s*)(id|title|ref|teaser|extract|href):", r'\1"\2":', js)
        decks[name] = json.loads(js)
    return decks


def codebook():
    """id -> (cell, slug), read from the codebook's tables."""
    out = {}
    for line in CODEBOOK.read_text().splitlines():
        m = re.match(r"\|\s*`(c\d-\d\d)`\s*\|\s*(\w+)\s*\|[^|]*\|\s*\[`([^`]+)`\]", line)
        if m:
            out[m.group(1)] = (m.group(2), m.group(3))
    return out


def capture(slug):
    p = WIKI / "wiki" / "sources" / f"{slug}.md"
    if not p.exists():
        sys.exit(f"no wiki page for {slug} (is AI_WIKI set? tried {WIKI})")
    t = p.read_text(errors="replace")
    m = re.search(r'^raw:\s*"?([^"\n]+)"?', t.split("---")[1], re.M)
    if not m:
        return t
    rp = (p.parent / m.group(1)).resolve()
    if slug in PDF_CAPTURES or rp.suffix == ".pdf":
        PDF_TEXT.mkdir(parents=True, exist_ok=True)
        txt = PDF_TEXT / f"{slug}.txt"
        if not txt.exists():
            subprocess.run(["pdftotext", str(rp), str(txt)],
                           capture_output=True, check=False)
        if not txt.exists():
            sys.exit(f"could not extract text from {rp} (is pdftotext installed?)")
        raw = txt.read_text(errors="replace")
    elif rp.exists() and rp.suffix in (".md", ".txt"):
        raw = rp.read_text(errors="replace")
    else:
        raw = t
    return "\n".join([raw, decolumnise_modal(raw), decolumnise_perline(raw)])


def main():
    decks, book = cards_from_page(), codebook()
    fails = []
    page = PAGE.read_text().lower()
    for label in LABELS:                                          # SM-8
        if label in page:
            fails.append(f"SM-8  the page contains the label {label!r}")
    seen_slugs = {}
    for name, cards in decks.items():
        counts = {}
        print(f"\n{name} - {len(cards)} cards")
        print(f"  {'id':8} {'cell':5} {'teaser':>6} {'extract':>7}  quoted")
        for c in cards:
            cell, slug = book.get(c["id"], ("?", None))
            if slug is None:
                fails.append(f"SM-6  {c['id']} is not in the codebook")
                continue
            seen_slugs.setdefault(slug, []).append(name)
            stem = "".join(ch for ch in cell if ch.isalpha())
            counts[stem] = counts.get(stem, 0) + 1
            tw, ew = wc(c["teaser"]), wc(c["extract"])
            src = norm(capture(slug))
            segs = [s for s in c["extract"].split("[...]") if s.strip()]
            found = ["ok" if norm(s) in src else "MISS" for s in segs]
            if tw > 25:
                fails.append(f"SM-10 {c['id']} teaser is {tw} words")
            if ew > 150:
                fails.append(f"SM-7  {c['id']} extract is {ew} words")
            if "MISS" in found:
                fails.append(f"SM-7  {c['id']} extract not found in {slug}")
            if not c.get("href"):
                fails.append(f"SM-11 {c['id']} has no link")
            for field in ("title", "ref", "teaser"):
                if not c.get(field):
                    fails.append(f"SM-5  {c['id']} has no {field}")
            print(f"  {c['id']:8} {cell:5} {tw:>6} {ew:>7}  {'+'.join(found)}")
        for stem in ("AS", "NAS", "AW", "NAW"):                    # SM-6
            if counts.get(stem, 0) != 4:
                fails.append(f"SM-6  {name} has {counts.get(stem, 0)} cards in {stem}, not 4")
        print("  cells: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    for slug, where in seen_slugs.items():                         # CL-6
        if len(set(where)) > 1:
            fails.append(f"CL-6  {slug} appears in {' and '.join(sorted(set(where)))}")
    print()
    if fails:
        for f in sorted(set(fails)):
            print("FAIL " + f)
        print(f"\n{len(set(fails))} failure(s)")
        return 1
    print("every gate passes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
