#!/usr/bin/env python3
"""Finds constructions in English text that give away a language model, and
language pitched above the reader's level.

Works on .md, .txt and .html. In HTML, tags and entities are replaced by runs of
spaces of the same length, so line numbers and quotations still point at the
place in the source file.

    python3 aiprose.py page.html
    python3 aiprose.py dir/ --recursive --codes A1,A2 --json findings.json
    python3 aiprose.py deck.html --ignore-html-class notes   # skip speaker notes
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass, asdict
from html import unescape
from pathlib import Path

# --------------------------------------------------------------------------
# thresholds — starting values, adjusted after measuring real material
# --------------------------------------------------------------------------
DASHES_PER_100 = 1.2       # A10: em dashes per 100 words
RHYTHM_MIN_SENTENCES = 8   # A11: fewer sentences than this says nothing about rhythm
RHYTHM_SPREAD = 0.38       # A11: coefficient of variation of sentence length
TRIAD_PER_100 = 1.5        # A12: "X, Y and Z" lists per 100 words
INTENSIFIER_MIN = 4        # A16: same intensifier repeated this often is a tic
INTENSIFIER_PER_1000 = 0.5 # A16: …and at least this dense, so long documents are not punished
SENTENCE_MAX_WORDS = 25    # D1: upper bound for a student reading in a second language
ABSTRACT_PER_100 = 3.5     # D2: nouns of action per 100 words


@dataclass
class Finding:
    code: str
    file: str
    line: int
    context: str
    quote: str
    note: str


# --------------------------------------------------------------------------
# getting the text in
# --------------------------------------------------------------------------
# A block element ends a sentence: two paragraphs side by side must not be
# counted as one forty-word sentence. The boundary gets its own character rather
# than a newline, so line numbers keep pointing at the right place.
BOUNDARY = "\x1e"
BLOCKTAG = re.compile(
    r"</?(?:p|div|li|ul|ol|h[1-6]|t[dhr]|table|section|article|figure|figcaption|"
    r"blockquote|br|dd|dt|dl|caption|main|header|footer|nav)\b[^>]*>", re.I)


def _blank(m: re.Match) -> str:
    """Replaces a run of markup with as many spaces, keeping newlines."""
    return re.sub(r"[^\n]", " ", m.group(0))


def _block(m: re.Match) -> str:
    """The same, but leaves a sentence boundary where the tag was."""
    return BOUNDARY + re.sub(r"[^\n]", " ", m.group(0))[1:]


def strip_html(text: str, ignore_classes: tuple[str, ...] = (),
               block_extra: tuple[str, ...] = ()) -> str:
    """Removes the markup but keeps every position where it was.

    Entities become their character plus padding, so that &mdash; counts as an
    em dash without shifting the rest of the line."""
    for cls in ignore_classes:
        pattern = re.compile(
            r'<(\w+)[^>]*class="[^"]*\b' + re.escape(cls) + r'\b[^"]*"[^>]*>.*?</\1>', re.S)
        text = pattern.sub(_blank, text)
    text = re.sub(r"<(script|style)\b.*?</\1>", _blank, text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", _blank, text, flags=re.S)
    text = re.sub(r"<svg\b.*?</svg>", _blank, text, flags=re.S | re.I)
    text = BLOCKTAG.sub(_block, text)
    if block_extra:
        extra = re.compile(r"</?(?:" + "|".join(re.escape(e) for e in block_extra) + r")\b[^>]*>", re.I)
        text = extra.sub(_block, text)
    text = re.sub(r"<[^>]+>", _blank, text)

    def _entity(m: re.Match) -> str:
        char = unescape(m.group(0))
        if len(char) != 1:                       # unknown: leave as spaces
            return " " * len(m.group(0))
        return char + " " * (len(m.group(0)) - 1)

    return re.sub(r"&[#\w]+;", _entity, text)


def read(path: Path, ignore_classes: tuple[str, ...] = (),
         block_extra: tuple[str, ...] = ()) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in (".html", ".htm", ".xhtml"):
        return strip_html(raw, ignore_classes, block_extra)
    return raw


# --------------------------------------------------------------------------
# structure: line number, and the heading a place falls under
# --------------------------------------------------------------------------
def line_of(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def build_context(raw: str) -> list[tuple[int, str]]:
    """Anchors a finding sits under: data-title in HTML, or a markdown heading."""
    anchors: list[tuple[int, str]] = []
    for m in re.finditer(r'data-title="([^"]*)"', raw):
        anchors.append((m.start(), m.group(1)))
    for m in re.finditer(r"<h[1-6][^>]*>(.*?)</h[1-6]>", raw, re.S | re.I):
        anchors.append((m.start(), re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()))
    for m in re.finditer(r"^#{1,6}\s+(.+)$", raw, re.M):
        anchors.append((m.start(), m.group(1).strip()))
    anchors.sort()
    return anchors


def context_of(anchors: list[tuple[int, str]], position: int) -> str:
    name = ""
    for start, title in anchors:
        if start > position:
            break
        name = title
    return name


# --------------------------------------------------------------------------
# sentences
# --------------------------------------------------------------------------
_ABBREVIATION = re.compile(r"\b(e\.g|i\.e|etc|cf|vs|Dr|Mr|Mrs|Ms|Prof|St|Fig|No|approx|ca)\.$", re.I)


def sentences(text: str) -> list[tuple[int, str]]:
    """Splits on sentence end and returns (start position, sentence)."""
    out: list[tuple[int, str]] = []
    start = 0
    for m in re.finditer(r"[.!?…](?=[\s\"')\]]|$)|\n{2,}|" + BOUNDARY + "+", text):
        chunk = text[start:m.end()]
        if _ABBREVIATION.search(chunk.strip()):
            continue
        if chunk.strip():
            out.append((start + len(chunk) - len(chunk.lstrip()), chunk.strip()))
        start = m.end()
    rest = text[start:]
    if rest.strip():
        out.append((start + len(rest) - len(rest.lstrip()), rest.strip()))
    return out


def words(s: str) -> list[str]:
    return re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'’-]*", s)


# --------------------------------------------------------------------------
# A1 to A9 — forms a rule can point at
# --------------------------------------------------------------------------
def _p(*variants: str) -> re.Pattern:
    return re.compile("|".join(variants), re.I)


PATTERNS: list[tuple[str, re.Pattern, str]] = [
    ("A1", _p(
        r"\bnot\s+(?:just|only|merely|simply|about\s+)?[\w’'-]+(?:\s+[\w’'-]+){0,4},?\s+but\b",
        r"\b(?:is|are|was|were|it'?s|that'?s|they'?re)\s+not\s+[\w’'-]+(?:\s+[\w’'-]+){0,6}\s*[—–]\s*(?:it|they|that)\b",
        r",\s+not\s+(?!\w+ing\b)[\w’'-]+",
        r"\bis\s+not\s+[\w’'-]+(?:\s+[\w’'-]+){0,6}\.\s+It\s+is\b",
        r"\bit'?s\s+not\s+about\b",
        r"\bwithout\s+[\w’'-]+(?:\s+[\w’'-]+){0,3}\s+there\s+(?:is|are)\s+no\b",
        r"\bless\s+[\w’'-]+,\s*more\b",
        r"\brather\s+than\b",
    ), "antithesis that mimics insight; say what it is and drop the half it isn't"),

    ("A2", _p(
        r"\b(?:crucial|essential|fundamental|indispensable|groundbreaking|revolutionary|"
        r"unprecedented|remarkable|powerful|invaluable|vital|pivotal|robust|seamless|"
        r"cutting[- ]edge|state[- ]of[- ]the[- ]art|transformative|game[- ]?changer|"
        r"of\s+critical\s+importance|of\s+paramount\s+importance|key\s+(?:driver|enabler|pillar))\b",
    ), "strong word with no mechanism, number or example behind it"),

    ("A3", _p(
        r"\bin\s+(?:today'?s|the\s+(?:current|modern|rapidly\s+changing|ever[- ]changing|fast[- ]paced))\b",
        r"\bin\s+a\s+world\s+(?:where|that)\b",
        r"\bit(?:'?s|\s+is)\s+(?:important|worth|useful|good)\s+to\s+(?:note|remember|realise|realize|understand)\b",
        r"\blet'?s\s+(?:take\s+a\s+look\s+at|dive\s+in|explore)\b",
        r"\bin\s+this\s+(?:chapter|section|part),?\s+we(?:'?ll|\s+will)?\s+(?:discuss|examine|explore|look)\b",
        r"\bwhat\s+makes\s+this\s+(?:so\s+)?(?:special|unique|interesting)\b",
        r"\bbefore\s+we\s+(?:go\s+further|begin|continue),?\s+(?:it|we)\b",
    ), "warm-up carrying no information; start at the point"),

    ("A4", _p(
        r"\b(?:\w+\s+)?landscape\b", r"\becosystem\b", r"\bplaying\s+field\b",
        r"\bthe\s+world\s+of\s+\w+", r"\bthe\s+realm\s+of\b", r"\bin\s+the\s+space\s+of\b",
        r"\bin\s+the\s+context\s+of\b", r"\bthe\s+domain\s+of\b", r"\bthe\s+arena\s+of\b",
    ), "container noun; name the organisation, the people or the place"),

    ("A5", _p(
        r"\b(?:dive|diving|delve|delving)\s+into\b", r"\bunlock(?:s|ing|ed)?\b",
        r"\bseamless(?:ly)?\b", r"\beffortless(?:ly)?\b", r"\bempower(?:s|ing|ed|ment)?\b",
        r"\bleverag(?:e|es|ing|ed)\b", r"\bharness(?:es|ing|ed)?\s+the\b",
        r"\bnavigat(?:e|ing)\s+(?:the|this)\b", r"\breap\s+the\s+benefits\b",
        r"\btap\s+into\b", r"\bat\s+its\s+core\b", r"\band\s+that'?s\s+precisely\b",
    ), "buzzword; use an ordinary verb"),

    ("A6", _p(
        r"\bserves?\s+as\b", r"\bacts?\s+as\b", r"\bfunctions?\s+as\b",
        r"\bforms?\s+the\s+(?:basis|foundation)\s+for\b", r"\bstands?\s+for\b",
        r"\brepresents?\b", r"\bconstitutes?\b", r"\bmarks?\s+(?:a|an|the)\b",
        r"\bplays?\s+an?\s+(?:\w+\s+)?role\b", r"\bhas\s+its\s+origins\s+in\b",
    ), "detour around 'is'"),

    ("A7", _p(
        r"\b(?:only\s+)?time\s+will\s+tell\b", r"\bit\s+remains\s+to\s+be\s+seen\b",
        r"\bthere\s+is\s+(?:still\s+)?room\s+for\s+improvement\b",
        r"\bone\s+thing\s+is\s+(?:certain|clear)\b", r"\beither\s+way\b",
        r"\bthe\s+future\s+will\s+(?:tell|show)\b",
    ), "ending that decides nothing; name a choice, a limit or a next step"),

    ("A8", _p(
        r"\brevolutionis(?:e|es|ing|ed)\b", r"\brevolutioniz(?:e|es|ing|ed)\b",
        r"\bchang(?:es|ing)\s+the\s+way\s+we\b",
        r"\bbrings?\s+us\s+(?:one\s+step\s+)?closer\s+to\b",
        r"\bthe\s+future\s+of\s+\w+\s+is\b",
        r"\bwill\s+never\s+be\s+the\s+same\b", r"\bis\s+set\s+to\s+transform\b",
    ), "future promise with no condition and no measuring point"),

    ("A9", _p(
        r"^\s*(?:great|good|excellent|sharp)\s+question\b",
        r"\byou'?re\s+(?:absolutely\s+)?right\b",
        r"^\s*(?:absolutely|certainly|of\s+course)[!.]",
        r"\bgood\s+(?:catch|point)\b",
    ), "politeness formula; cut it"),

    ("A17", _p(
        r"(?:^|[.!?]\s+|[—–]\s*)That\s+is\s+(?:what|the|why|where|how|exactly|not|a|an)\b",
        r"(?:^|[.!?]\s+)That'?s\s+(?:what|the|why|where|how|exactly|not)\b",
    ), "demonstrative echo: a closer that restates the sentence before it"),
]


def find_patterns(text: str, codes: set[str] | None) -> list[tuple[str, int, str, str]]:
    """Returns (code, position, quote, note) for every hit."""
    out = []
    for code, pattern, note in PATTERNS:
        if codes and code not in codes:
            continue
        for m in pattern.finditer(text):
            begin, end = max(0, m.start() - 45), min(len(text), m.end() + 45)
            quote = re.sub(r"\s+", " ", text[begin:end].replace(BOUNDARY, " ")).strip()
            out.append((code, m.start(), quote, note))
    return out


# --------------------------------------------------------------------------
# A10 to A12, A16 and D1 to D3 — densities and rhythm
# --------------------------------------------------------------------------
JARGON = {
    "stakeholder", "stakeholders", "governance", "compliance", "alignment", "mindset",
    "scope creep", "deliverable", "deliverables", "benchmark", "kpi", "kpis", "roadmap",
    "framework", "onboarding", "agile", "lean", "scrum", "sprint", "backlog",
    "value proposition", "business case", "best practice", "best practices",
    "disruption", "disruptive", "scalable", "scalability", "esg", "csrd", "iot",
    "cybersecurity", "circularity", "raci", "synergy", "actionable", "low-hanging fruit",
}

INTENSIFIERS = re.compile(
    r"\b(?:actually|genuinely|truly|really|quietly|honest|honestly|simply|literally|"
    r"fundamentally|arguably|notably|precisely|indeed)\b", re.I)

ABSTRACT = re.compile(
    r"\b\w{5,}(?:tion|sion|ment|ness|ity|ance|ence|ism|isation|ization)\b", re.I)


def is_explained(sentence: str, term: str) -> bool:
    """True when the term carries its explanation in the same sentence.

    Three forms count: a gloss in brackets ('smart devices (IoT)'), a colon or
    equals sign in the sentence ('Agile: working in short rounds'), and the term
    as part of a proper name ('Integrated Reporting Framework')."""
    m = re.search(r"\b" + re.escape(term) + r"\b", sentence, re.I)
    if not m:
        return False
    around = sentence[max(0, m.start() - 3):m.end() + 3]
    if "(" in around or ")" in around:
        return True
    if re.search(r"[:=]", sentence):
        return True
    before = sentence[:m.start()].rstrip().split(" ")[-1:]
    after = sentence[m.end():].lstrip().split(" ")[:1]
    neighbours = [w for w in before + after if w]
    return bool(sentence[m.start():m.start() + 1].isupper()
                and neighbours and any(w[:1].isupper() for w in neighbours))


def measure_densities(text: str, codes: set[str] | None) -> list[tuple[str, int, str, str]]:
    out: list[tuple[str, int, str, str]] = []
    all_words = words(text)
    n = len(all_words) or 1

    if not codes or "A10" in codes:
        dashes = [m.start() for m in re.finditer(r"—|–|--", text)]
        per100 = 100 * len(dashes) / n
        if per100 > DASHES_PER_100 and len(dashes) >= 5:
            out.append(("A10", dashes[0],
                        f"{len(dashes)} em dashes in {n} words ({per100:.1f} per 100)",
                        f"above {DASHES_PER_100} per 100; make some of them full stops or commas"))

    sents = [s for _, s in sentences(text)]
    lengths = [len(words(s)) for s in sents if len(words(s)) >= 3]
    if (not codes or "A11" in codes) and len(lengths) >= RHYTHM_MIN_SENTENCES:
        mean = statistics.mean(lengths)
        spread = statistics.pstdev(lengths) / mean if mean else 1
        if spread < RHYTHM_SPREAD:
            out.append(("A11", 0,
                        f"{len(lengths)} sentences, {mean:.0f} words on average, spread {spread:.2f}",
                        f"below {RHYTHM_SPREAD}: every sentence the same length; mix short and long"))

    if not codes or "A12" in codes:
        triads = [m.start() for m in re.finditer(
            r"\b[\w’'-]+,\s+[\w’'-]+\s+and\s+[\w’'-]+\b", text)]
        per100 = 100 * len(triads) / n
        if per100 > TRIAD_PER_100 and len(triads) >= 4:
            out.append(("A12", triads[0],
                        f"{len(triads)} three-part lists in {n} words ({per100:.1f} per 100)",
                        "the rule of three as filler; two items is allowed"))

    if not codes or "A16" in codes:
        # The signal is one word used over and over, not intensifiers in general:
        # "actually" seven times in a page is a tic, seven different ones are not.
        seen: dict[str, list[int]] = {}
        for m in INTENSIFIERS.finditer(text):
            seen.setdefault(m.group(0).lower(), []).append(m.start())
        for word, spots in sorted(seen.items()):
            per1000 = 1000 * len(spots) / n
            if len(spots) >= INTENSIFIER_MIN and per1000 >= INTENSIFIER_PER_1000:
                out.append(("A16", spots[0],
                            f"'{word}' {len(spots)} times in {n} words ({per1000:.1f} per 1000)",
                            "an intensifier claims emphasis the sentence has not earned; "
                            "cut it, or replace it with the fact that made you reach for it"))

    if not codes or "D2" in codes:
        abstracts = ABSTRACT.findall(text)
        per100 = 100 * len(abstracts) / n
        if per100 > ABSTRACT_PER_100:
            top = ", ".join(sorted({a.lower() for a in abstracts})[:6])
            out.append(("D2", 0, f"{per100:.1f} nouns of action per 100 words ({top}…)",
                        f"above {ABSTRACT_PER_100}; turn them back into verbs"))

    return out


def measure_sentences(text: str, codes: set[str] | None) -> list[tuple[str, int, str, str]]:
    out: list[tuple[str, int, str, str]] = []
    for pos, sentence in sentences(text):
        w = words(sentence)
        if (not codes or "D1" in codes) and len(w) > SENTENCE_MAX_WORDS:
            out.append(("D1", pos, re.sub(r"\s+", " ", sentence)[:120],
                        f"{len(w)} words; above {SENTENCE_MAX_WORDS} a second-language reader loses the thread"))
        if not codes or "D3" in codes:
            for term in sorted(JARGON):
                if re.search(r"\b" + re.escape(term) + r"\b", sentence, re.I):
                    if is_explained(sentence, term):
                        continue
                    out.append(("D3", pos, re.sub(r"\s+", " ", sentence)[:120],
                                f"'{term}' — explain it on first use, or replace it"))
                    break
    return out


# --------------------------------------------------------------------------
# running it
# --------------------------------------------------------------------------
def check(path: Path, codes: set[str] | None, ignore_classes: tuple[str, ...],
          block_extra: tuple[str, ...] = ()) -> list[Finding]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = read(path, ignore_classes, block_extra)
    anchors = build_context(raw)
    hits = (find_patterns(text, codes) + measure_densities(text, codes)
            + measure_sentences(text, codes))
    findings = [Finding(code, str(path), line_of(text, pos), context_of(anchors, pos), quote, note)
                for code, pos, quote, note in hits]
    findings.sort(key=lambda f: (f.line, f.code))
    return findings


def collect(paths: list[str], recursive: bool) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            pattern = "**/*" if recursive else "*"
            out += [q for q in sorted(path.glob(pattern))
                    if q.suffix.lower() in (".md", ".txt", ".html", ".htm", ".xhtml")]
        else:
            out.append(path)
    return out


def main(argv: list[str] | None = None) -> int:
    a = argparse.ArgumentParser(description="Checks English text for AI language and reading level.")
    a.add_argument("paths", nargs="+")
    a.add_argument("--recursive", action="store_true")
    a.add_argument("--codes", help="only these codes, comma separated (A1,D1,…)")
    a.add_argument("--ignore-html-class", action="append", default=[],
                   help="skip HTML elements with this class, e.g. notes")
    a.add_argument("--block-tag", action="append", default=[],
                   help="also treat this tag as a sentence boundary, e.g. span")
    a.add_argument("--json", help="also write the findings to this file")
    n = a.parse_args(argv)

    codes = {c.strip().upper() for c in n.codes.split(",")} if n.codes else None
    everything: list[Finding] = []
    for path in collect(n.paths, n.recursive):
        if not path.exists():
            print(f"not found: {path}", file=sys.stderr)
            continue
        everything += check(path, codes, tuple(n.ignore_html_class), tuple(n.block_tag))

    for f in everything:
        where = f"{f.file}:{f.line}"
        head = f" [{f.context}]" if f.context else ""
        print(f"{f.code}  {where}{head}\n     {f.quote}\n     → {f.note}")

    tally: dict[str, int] = {}
    for f in everything:
        tally[f.code] = tally.get(f.code, 0) + 1
    summary = " · ".join(f"{c}: {tally[c]}" for c in sorted(tally)) or "nothing found"
    print(f"\n{len(everything)} findings — {summary}")

    if n.json:
        Path(n.json).write_text(json.dumps([asdict(f) for f in everything], ensure_ascii=False, indent=2),
                                encoding="utf-8")
        print(f"written: {n.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
