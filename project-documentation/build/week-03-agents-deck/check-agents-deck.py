#!/usr/bin/env python3
"""Acceptance checks for the week 3 AI agents segment.

    python3 check-agents-deck.py --spec          # the blueprint's own structure
    python3 check-agents-deck.py --deck          # every Test rule against the cards
    python3 check-agents-deck.py --deck --online # ... and request every external card link
    python3 check-agents-deck.py                 # both

--spec checks blueprint.html beside this file: the ten sections in order, an anchor
per rule, a level, a criterion with a number and a unit, one of four methods, one
"shall" per rule, no vague terms or escape clauses, no build-order vocabulary, and
not every rule a Must.

--deck checks the rules whose method is Test against site/week-03-slides.html, the
notes file and provenance.md. SL-2..SL-5 use slidewords.measure() and PR-2..PR-4
run aiprose.py, so the two skills are the check rather than a copy of it.

Every path can be overridden, which is how each check is sabotage-tested:
    --blueprint --slides --notes --provenance --wiki
The AI Wiki is expected at ~/Projects/ai-wiki; set AI_WIKI or pass --wiki.

Exit 0 when everything checked passes, 1 otherwise.
"""
import argparse, html, json, os, pathlib, re, subprocess, sys, tempfile, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
REPO = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                                   text=True, cwd=HERE).stdout.strip() or HERE.parents[2])
SKILLS = REPO / ".claude" / "skills"
sys.path.insert(0, str(SKILLS / "slide-deck" / "scripts"))
import slidewords  # noqa: E402  (the slide-deck skill's counter)
AIPROSE = SKILLS / "strip-ai-language" / "scripts" / "aiprose.py"

KICKER = "AI agents"
DEBRIEF_KICKER = "Debrief"
SECTIONS = ["Header and provenance", "The goal", "The parts", "Where the segment sits in the session",
            "Contracts", "Rules", "What the checks enforce", "Trace to the goal",
            "Deliberate exclusions", "Open questions"]
LEVELS = {"Must", "Should", "Could"}
METHODS = {"Test", "Demonstration", "Inspection", "Analysis"}
UNITS = r"(word|card|bullet|minute|finding|term|link|file|sentence|match|block|page|item|row|%|pixel|statement|occurrence|mention|exit|claim|layer|headline|second)"
VAGUE = ["reliable", "user-friendly", "where possible", "if possible", "as appropriate", "as needed",
         "robust", "seamless", "sufficient", "adequate"]
STATUS = [r"\bphases?\b", r"\bcurrently\b", r"\bnot yet\b", r"\btoday\b", r"\btodo\b", r"\bin progress\b",
          r"\bso far\b", r"\bfor now\b", r"\bpreviously\b", r"\bwill be added\b"]
# SE-2: phrasings that would tell a student which way the experiment's hypothesis points
DIRECTION = [r"(questioning|socratic)\s+agents?\s+(reduce|lower|cut|decrease|weaken)s?",
             r"verdict(-giving)?\s+agents?\s+(increase|amplif|strengthen|worsen)",
             r"agents?\s+(reduce|amplif\w*|increase)s?\s+(confirmation\s+)?bias",
             r"(expect|predict|hypothesi[sz]e)\w*\s+(that\s+)?(the\s+)?agent"]

# PR-3: the segment's own technical vocabulary, checked on first use
AGENT_TERMS = ["harness", "LLM", "RAG", "SLM", "MCP", "LLM Wiki", "Fat Skills", "agentic", "context window", "ReAct"]

results = []


def report(rule, ok, detail=""):
    results.append(ok)
    print(f"  {'PASS' if ok else 'FAIL'}  {rule:<6} {detail}")


def plain(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


# ------------------------------------------------------------------ the spec

def check_spec(path):
    print(f"spec: {path}")
    src = path.read_text(encoding="utf-8")
    main = src[src.index('<section id="provenance">'):src.rindex("</main>")]
    h2 = [re.sub(r"^\d+\s*·\s*", "", plain(h)) for h in re.findall(r'<h2 class="bds-part">(.*?)</h2>', main, re.S)]
    report("S-1", h2 == [f"{t}" for t in SECTIONS] and all(
        re.search(rf'<h2 class="bds-part">{i + 1} &middot; ', main) for i in range(len(SECTIONS))),
        f"sections {'in order' if h2 == SECTIONS else h2}")
    rows = re.findall(r'<tr id="([a-z]{2}-\d+)"><th>([A-Z]{2}-\d+)</th>(.*?)</tr>', main, re.S)
    report("S-2", len(rows) > 0 and all(a == i.lower() for a, i, _ in rows),
           f"{len(rows)} rules, every anchor matches its id")
    ids = {i for _, i, _ in rows}
    cited = set(re.findall(r"\b([A-Z]{2}-\d+)\b", plain(main)))
    plan = HERE / "buildplan.html"
    if plan.exists():
        cited |= set(re.findall(r"\b([A-Z]{2}-\d+)\b", plain(plan.read_text(encoding="utf-8"))))
    missing = sorted(c for c in cited if c[:2] in {i[:2] for i in ids} and c not in ids)
    report("S-3", not missing, "every cited rule id has an anchor" if not missing else f"no anchor: {missing}")
    bad, levels = [], []
    for _, rid, body in rows:
        cells = [plain(c) for c in re.findall(r"<td>(.*?)</td>", body, re.S)]
        if len(cells) != 4:
            bad.append(f"{rid}: {len(cells)} cells"); continue
        rule, level, crit, method = cells
        levels.append(level)
        if level not in LEVELS: bad.append(f"{rid}: level {level!r}")
        if method not in METHODS: bad.append(f"{rid}: method {method!r}")
        if not (re.search(r"\d", crit) and re.search(UNITS, crit, re.I)): bad.append(f"{rid}: criterion lacks number+unit")
        if len(re.findall(r"\bshall\b", rule)) > 1: bad.append(f"{rid}: two 'shall'")
        low = (rule + " " + crit).lower()
        bad += [f"{rid}: vague '{v}'" for v in VAGUE if v in low]
    report("S-4", not bad, "every rule has level, number+unit, method, one shall, no vague term" if not bad else "; ".join(bad))
    report("S-5", levels and set(levels) != {"Must"}, f"levels {dict((l, levels.count(l)) for l in LEVELS)}")
    leaks = [p for p in STATUS if re.search(p, plain(main), re.I)]
    report("S-6", not leaks, "no build-order or status vocabulary" if not leaks else f"found {leaks}")
    ext = re.findall(r'<(?:script|link)[^>]*(?:src|href)="https?://', src)
    report("S-7", not ext, "self-contained: no external script or stylesheet")


# ------------------------------------------------------------------ the deck

def segment(slides):
    src = slides.read_text(encoding="utf-8")
    cards = []
    for n, (classes, sid, body) in enumerate(re.findall(r'<section class="slide([^"]*)" id="(s\d+)">(.*?)</section>', src, re.S)):
        k = re.search(r'<div class="slide-kicker">(.*?)</div>', body, re.S)
        cards.append({"n": n, "id": sid, "kicker": plain(k.group(1)) if k else "", "body": body})
    return src, cards


def aiprose(fragment_html, codes, block_li=True):
    # aiprose marks a block boundary with \x1e, and Python's \s matches \x1e, so a pattern such
    # as A5's "harness\s+the" still runs from a headline into the bullet below it. A full stop
    # at the end of each block is what actually stops it.
    fragment_html = re.sub(r"</(h2|li|p)>", r".</\1>", fragment_html)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(f"<html><body>{fragment_html}</body></html>"); page = f.name
    out = page + ".json"
    args = [sys.executable, str(AIPROSE), page, "--codes", codes, "--json", out]
    # A headline, a bullet and a paragraph each end a sentence. Without h2 here a headline
    # ending "...the harness" runs into a bullet starting "The harness" and A5 reads "harness the".
    if block_li: args += ["--block-tag", "li", "--block-tag", "h2", "--block-tag", "p"]
    subprocess.run(args, capture_output=True, text=True)
    found = json.loads(pathlib.Path(out).read_text()) if pathlib.Path(out).exists() else []
    os.unlink(page); pathlib.Path(out).unlink(missing_ok=True)
    return found


def unexplained_agent_terms(seg):
    """D3 for this segment's own vocabulary, which aiprose's JARGON list does not carry.

    The skill says to extend JARGON with the field's terms; doing that here rather than in
    the shared script keeps the skill unchanged for every other page. A term counts as
    explained if, on the card where it first appears, aiprose.is_explained() accepts at least
    one line that uses it (a gloss in brackets, after a colon, or inside a proper name). The
    card is the unit because a headline has no room for a gloss and the line below it does.
    Later cards may use the term freely.
    """
    sys.path.insert(0, str(AIPROSE.parent))
    import aiprose as ap
    seen, out = set(), []
    for c in seg:
        lines = [plain(b) for b in re.split(r"</(?:h2|li|p)>", c["body"])]
        for term in AGENT_TERMS:
            uses = [s for s in lines if re.search(rf"\b{re.escape(term)}\b", s, re.I)]
            if term in seen or not uses:
                continue
            seen.add(term)
            if not any(ap.is_explained(s, term) for s in uses):
                out.append(f"{term}: {uses[0]}")
    return out


def note_blocks(notes, ids):
    if not notes.exists():
        return {}
    text = notes.read_text(encoding="utf-8")
    return {m.group(1): m.group(2) for m in re.finditer(r"^## (s\d+)\s*$(.*?)(?=^## s\d+\s*$|\Z)", text, re.S | re.M)
            if m.group(1) in ids}


def check_deck(slides, notes, provenance, wiki, online):
    print(f"deck: {slides}")
    if not slides.exists():
        report("SL-1", False, f"{slides.name} is absent"); return
    src, cards = segment(slides)
    seg = [c for c in cards if c["kicker"] == KICKER]
    consecutive = seg and [c["n"] for c in seg] == list(range(seg[0]["n"], seg[0]["n"] + len(seg)))
    report("SL-1", len(seg) == 3 and bool(consecutive), f"{len(seg)} '{KICKER}' cards, consecutive={bool(consecutive)}")
    if not seg: return
    deb = [c["n"] for c in cards if c["kicker"] == DEBRIEF_KICKER]
    report("SE-1", bool(deb) and all(c["n"] > deb[0] for c in seg),
           f"debrief card at #{deb[0] + 1}, segment from #{seg[0]['n'] + 1}" if deb else f"no card with kicker '{DEBRIEF_KICKER}'")

    lim = {"headline_words": 12, "body_words": 40, "bullets": 3, "longest_sentence": 20}
    m = [slidewords.measure(c["body"]) for c in seg]
    for rule, key in [("SL-2", "headline_words"), ("SL-3", "body_words"), ("SL-4", "bullets"), ("SL-5", "longest_sentence")]:
        vals = [x[key] for x in m]
        report(rule, all(v <= lim[key] for v in vals), f"{key} {vals} (max {lim[key]})")

    texts = [plain(c["body"]).lower() for c in seg]
    c1, c2, c3 = (texts + ["", "", ""])[:3]
    report("CT-1", all(re.search(p, c1) for p in [r"\b(model|llm)\b", r"\btools?\b", r"\bloop\b", r"\bgoal\b"]),
           "card 1: model/LLM, tools, loop, goal")
    b2 = seg[1]["body"] if len(seg) > 1 else ""
    report("CT-3", "harness-is-os-en.html" in b2, "card 2 links Harness is the OS")
    report("CT-4", "architecture-of-scale-en.html" in b2, "card 2 links Four ways")
    report("CT-6", all(re.search(rf"\b{w}\b", c3) for w in ["data", "output", "people"]), "card 3: data, output, people")
    report("CT-9", "intern" in c1, "card 1 mentions the intern")

    blocks = note_blocks(notes, {c["id"] for c in seg})
    alltext = " ".join(texts) + " " + " ".join(blocks.values()).lower()
    hits = [p for p in DIRECTION if re.search(p, alltext)]
    report("SE-2", not hits, "no hypothesis direction on cards or notes" if not hits else f"matched {hits}")

    fragment = "".join(f"<section>{c['body']}</section>" for c in seg)
    f2 = aiprose(fragment, "A2,A3,A5,A7,A8,A9")
    report("PR-2", not f2, f"{len(f2)} empty-emphasis findings on the cards" + "".join(f"\n           {x['code']}: {x['quote']}" for x in f2))
    f3 = [f"{x['quote']}" for x in aiprose(fragment, "D3")] + unexplained_agent_terms(seg)
    report("PR-3", not f3, f"{len(f3)} unexplained terms on the cards" + "".join(f"\n           {q}" for q in f3))
    a1 = aiprose(fragment, "A1")
    print(f"  INFO  PR-1   {len(a1)} A1 findings — each needs a rewrite or a register row (inspection)")

    report("BD-2", len(blocks) == 3, f"{len(blocks)} of 3 segment ids have a ## sN block in {notes.name}")
    report("CT-8", len(blocks) == 3 and all(re.search(r"\bweek\s*\d", b, re.I) for b in blocks.values()),
           "every note names a module week")
    fn = aiprose("".join(f"<p>{html.escape(b)}</p>" for b in blocks.values()), "A3,A7,A8,A9", block_li=False) if blocks else []
    report("PR-4", bool(blocks) and not fn, f"{len(fn)} empty-emphasis findings in the notes")

    rows = []
    if provenance.exists():
        for line in provenance.read_text(encoding="utf-8").splitlines():
            cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
            if len(cells) == 4 and cells[0].isdigit():
                rows.append(cells)
    wiki_rows = [r for r in rows if r[2] != "LRD"]
    gone = [r[2] for r in wiki_rows if not (wiki / "wiki" / f"{r[2]}.md").exists()]
    report("CT-7", bool(rows) and {r[0] for r in rows} >= {"1", "2", "3"} and not gone,
           f"{len(rows)} provenance rows, {len(wiki_rows)} to the wiki, missing slugs {gone}")

    links = [h for c in seg for h in re.findall(r'href="([^"]+)"', c["body"])]
    rel_out = [h for h in links if not re.match(r"https?://|#|mailto:", h) and
               not (slides.parent / h.split("#")[0]).resolve().is_relative_to(slides.parent.resolve())]
    report("ST-2", not rel_out, f"{len(links)} card links, {len(rel_out)} relative links leaving site/")
    if online:
        bad = []
        for h in (h for h in links if h.startswith("http")):
            try:
                code = urllib.request.urlopen(urllib.request.Request(h, method="GET", headers={"User-Agent": "check-agents-deck"}), timeout=15).status
            except Exception as e:  # noqa: BLE001
                code = getattr(e, "code", str(e))
            if not (isinstance(code, int) and 200 <= code < 300): bad.append(f"{h} → {code}")
        report("ST-1", not bad, "every external card link answers 2xx" if not bad else "; ".join(bad))

    deck = REPO / "site" / "week-03-deck.html"
    outs = [deck, REPO / "project-documentation" / "slides" / "week-03-deck.pdf",
            REPO / "project-documentation" / "slides" / "week-03-deck.pptx"]
    fresh = [o for o in outs if o.exists() and o.stat().st_mtime >= slides.stat().st_mtime]
    report("BD-1", len(fresh) == 3, f"{len(fresh)} of 3 build outputs present and newer than the card page")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", action="store_true"); ap.add_argument("--deck", action="store_true")
    ap.add_argument("--online", action="store_true")
    ap.add_argument("--blueprint", type=pathlib.Path, default=HERE / "blueprint.html")
    ap.add_argument("--slides", type=pathlib.Path, default=REPO / "site" / "week-03-slides.html")
    ap.add_argument("--notes", type=pathlib.Path, default=REPO / "project-documentation" / "slides" / "week-03-notes.md")
    ap.add_argument("--provenance", type=pathlib.Path, default=HERE / "provenance.md")
    ap.add_argument("--wiki", type=pathlib.Path, default=pathlib.Path(os.environ.get("AI_WIKI", pathlib.Path.home() / "Projects" / "ai-wiki")))
    a = ap.parse_args(argv)
    both = not (a.spec or a.deck)
    if a.spec or both: check_spec(a.blueprint)
    if a.deck or both: check_deck(a.slides, a.notes, a.provenance, a.wiki, a.online)
    failed = results.count(False)
    print(f"\n{len(results) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
