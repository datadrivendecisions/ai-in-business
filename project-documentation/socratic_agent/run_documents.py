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

# The six documents of ADR-0010's spine, and the names students give their
# files. Students write in English, so only English aliases are listed. Order
# matters where one alias contains another: 'plan' alone is not listed, because
# a build plan and a knowledge plan would both match it.
DELIVERABLES = {
    "prd": ["prd", "product requirements", "requirements"],
    "blueprint": ["blueprint", "technical design"],
    "knowledge": ["knowledge", "knowledge architecture"],
    "buildplan": ["buildplan", "build plan", "build-plan"],
    "eval": ["eval", "evaluation"],
    "decisions": ["decisions", "decision log", "decision-log", "decisionlog"],
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
# the model, shared by every step that reads and judges
# ----------------------------------------------------------------------------

REPO = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
MODEL = "gemini-2.5-flash"
RETRIES = 2


def call_model(name, instruction, message, shapes):
    """One fresh session per attempt, as run_week.py does. Returns the text, or
    "" when no attempt produced output in one of the `shapes` (lists of headings)."""
    import asyncio
    from dotenv import load_dotenv
    load_dotenv(HERE / ".env")  # the course-owned project; never a personal key
    from google.adk.agents import LlmAgent
    from google.adk.runners import InMemoryRunner
    from google.genai import types

    agent = LlmAgent(
        name=name, model=MODEL, instruction=instruction,
        generate_content_config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=-1)),
    )

    async def once():
        runner = InMemoryRunner(agent=agent, app_name="documents")
        session = await runner.session_service.create_session(app_name="documents", user_id="owner")
        out = []
        async for event in runner.run_async(
                user_id="owner", session_id=session.id,
                new_message=types.Content(role="user", parts=[types.Part(text=message)])):
            if event.content and event.content.parts:
                out.extend(p.text for p in event.content.parts if p.text)
        return "".join(out).strip()

    for _ in range(RETRIES + 1):
        text = asyncio.run(once())
        if text and has_shape(text, shapes):
            return text
    return ""


def has_shape(text, alternatives):
    """True when the text carries every heading of at least one alternative."""
    return any(all(h in text for h in alt) for alt in alternatives)


def page_text(path):
    """A site page as text with its links kept, through agent.py's extractor."""
    from agent import _Extract
    p = _Extract()
    p.feed(path.read_text(encoding="utf-8", errors="replace"))
    return p.text()


def git_short_hash(rel):
    r = subprocess.run(["git", "-C", str(REPO), "log", "-1", "--format=%h", "--", rel],
                       capture_output=True, text=True)
    return r.stdout.strip() or "uncommitted"


def parse_header(path):
    """The key: value lines between the two --- markers at the top of a report."""
    out = {}
    if not path.exists():
        return out
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return out
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def header(fields):
    return "---\n" + "".join(f"{k}: {v}\n" for k, v in fields.items()) + "---\n\n"


def latest_texts(week_dir, team, week):
    """{deliverable: (version, text path)} for the highest version in this week's folder."""
    found = {}
    for txt in week_dir.glob(f"{team}-week-{week:02d}-*.txt"):
        rest = txt.stem[len(f"{team}-week-{week:02d}-"):]
        m = re.fullmatch(r"([a-z]+)(?:-v(\d+))?", rest)
        if not m:
            continue
        deliv, version = m.group(1), int(m.group(2) or 1)
        if deliv in DELIVERABLES and version >= found.get(deliv, (0, None))[0]:
            found[deliv] = (version, txt)
    return found


def teams_in(root, only_team=None):
    teams_dir = root / "teams"
    if not teams_dir.is_dir():
        return []
    return sorted(p.name for p in teams_dir.iterdir()
                  if p.is_dir() and p.name.startswith("team-") and (not only_team or p.name == only_team))


# ----------------------------------------------------------------------------
# step 2 — score: one scoresheet per document, against its criteria and sheet
# ----------------------------------------------------------------------------

SCORE_SHAPES = [["## RETURNED"], ["## SCORESHEET", "## BEFORE V1"]]


def previous_score(root, team, deliv, week):
    """The most recent earlier score of the same deliverable for this team."""
    cands = []
    for p in (root / "teams" / team).glob(f"week-*/owners/score-{deliv}.md"):
        m = re.search(r"week-(\d+)", p.parent.parent.name)
        if m and int(m.group(1)) < week:
            cands.append((int(m.group(1)), p))
    return max(cands)[1] if cands else None


def step_score(root, week, only_team=None):
    done, problems = [], []
    for team in teams_in(root, only_team):
        week_dir = root / "teams" / team / f"week-{week:02d}"
        if not week_dir.is_dir():
            continue
        for deliv, (version, txt) in sorted(latest_texts(week_dir, team, week).items()):
            out = week_dir / "owners" / f"score-{deliv}.md"
            if out.exists() and parse_header(out).get("version") == str(version):
                continue  # scored already, at this version
            sheet = root / "rubric" / f"{deliv}-scoresheet.md"
            criteria = REPO / "site" / f"{deliv}-criteria.html"
            missing = [str(p.relative_to(root)) for p in (sheet,) if not p.exists()]
            missing += [f"site/{criteria.name}" for p in (criteria,) if not p.exists()]
            if missing:
                problems.append(f"{team} {deliv}: unscored: no sheet for {deliv}"
                                if not sheet.exists() else f"{team} {deliv}: unscored: no criteria page {missing[0]}")
                continue

            prev = previous_score(root, team, deliv, week)
            fields = {
                "team": team, "deliverable": deliv, "week": week, "version": version,
                "document": txt.name,
                "criteria": f"site/{criteria.name} @ {git_short_hash(f'site/{criteria.name}')}",
                "sheet": f"rubric/{sheet.name} sha256 {sha256(sheet)[:12]}",
                "previous": str(prev.relative_to(root)) if prev else "none",
                "scored": now(),
            }
            message = (f"# THE CRITERIA — {criteria.name}, as published to the team\n\n{page_text(criteria)}\n\n"
                       f"# THE DOCUMENT — {team}, week {week}, version {version}\n\n"
                       f"{txt.read_text(encoding='utf-8', errors='replace')}\n")
            if prev:
                body = prev.read_text(encoding="utf-8").split("---\n\n", 1)[-1]
                message += f"\n# THE PREVIOUS SCORESHEET — {fields['previous']}\n\n{body}\n"
            text = call_model("scorer", sheet.read_text(encoding="utf-8"), message, SCORE_SHAPES)
            if not text:
                problems.append(f"{team} {deliv}: no scoresheet after {RETRIES + 1} attempts")
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(header(fields) + text.strip() + "\n", encoding="utf-8")
            verdict = "RETURNED" if "## RETURNED" in text else "SCORESHEET"
            done.append(f"{team} {deliv} v{version}: {verdict} → {out.relative_to(root)}")
    return done, problems


# ----------------------------------------------------------------------------
# step 3 — question: the register, the questions, the message, the lint
# ----------------------------------------------------------------------------

REGISTER_HEADER = ["id", "asked", "about", "question", "status", "resolved", "evidence"]
STATUSES = ("open", "answered", "partly", "ducked", "withdrawn")
STILL_OPEN = ("open", "partly", "ducked")   # fed back next week
MAX_OPEN = 5
QUESTION_SHAPES = [["## REGISTER", "## QUESTIONS"]]


def score_columns(path):
    """The two qualitative columns of a scoresheet, and nothing numeric: for each
    row, the criterion, the weakest evidence quoted and what would raise it. Item
    codes, scores, totals and bands never leave this function. A RETURNED sheet
    yields its reason, minus the invariant's code."""
    text = path.read_text(encoding="utf-8").split("---\n\n", 1)[-1]
    if "## RETURNED" in text:
        body = text.split("## RETURNED", 1)[1].strip()
        body = re.sub(r"^V\d\s*[—-]\s*", "", body)
        return "The document was not read against the criteria, for this reason:\n" + body.strip()
    lines = []
    for row in re.findall(r"^\|\s*[A-G]\d\s*\|(.*)$", text, re.M):
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        criterion, evidence, raise_ = cells[0], cells[2], cells[3]
        if evidence.upper().startswith("NONE"):
            evidence = "nothing found — " + evidence[4:].strip(" :—-") if len(evidence) > 4 else "nothing found"
        line = f"- {criterion}. Weakest sentence: {evidence}"
        if raise_ and raise_.upper() not in ("N/A", "NA", "—", "-"):
            line += f" What is missing: {raise_}"
        lines.append(line)
    return "\n".join(lines)


def band_words(root):
    """Band names from every sheet's bands table, learnt at run time so the lint
    knows them without the repository carrying them."""
    words = set()
    for sheet in (root / "rubric").glob("*-scoresheet.md"):
        text = sheet.read_text(encoding="utf-8")
        m = re.search(r"^###\s*3\.4.*?(?=^###|\Z)", text, re.S | re.M)
        if not m:
            continue
        for b in re.findall(r"\*\*([^*]+?)\.?\*\*", m.group(0)):
            if not re.fullmatch(r"[\d–\-\s]+", b):
                words.add(b.strip().lower())
    return words


LINT_PATTERNS = [
    (r"\b[A-G]\d\b", "criterion code"),
    (r"\bV[1-3]\b", "invariant code"),
    (r"\bX\d\b", "direction code"),
    (r"/\s*\d{2,3}\b", "a total"),
    (r"\b\d+\s*(?:out of|/)\s*\d+\b", "a fraction"),
    (r"\bscor(?:e|es|ed|ing)\b", "the word score"),
    (r"\bscoresheet\b", "the word scoresheet"),
    (r"\bband\b", "the word band"),
    (r"\brubric\b", "the word rubric"),
]

QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”|‘[^’\n]*’')


def lint_message(text, root, own_texts=()):
    """Every line of the message that carries rubric language. Empty = clean.

    What the team wrote is theirs to be asked about, so a quoted span is exempt,
    and a code or a word that appears in the team's own text is not a leak.
    Everything else that looks like the sheet — a code, a total, a band name,
    the words score, band or rubric — fails the line. The lecturer reads every
    message before it is sent; this is the net under that, not a replacement."""
    own = " ".join(own_texts).lower()
    hits = []
    pats = list(LINT_PATTERNS) + [(re.escape(w), f"band name '{w}'") for w in band_words(root)]
    for line in text.splitlines():
        bare = QUOTED.sub('""', line)
        for pat, why in pats:
            m = re.search(pat, bare, re.I)
            if not m:
                continue
            if m.group(0).lower() in own:
                continue  # a word or code the team wrote is theirs to be asked about
            hits.append((why, line.strip()))
            break
    return hits


def message_frame():
    raw = (HERE / "message-frame.md").read_text(encoding="utf-8")
    parts = raw.split("\n---\n")
    if len(parts) < 3:
        raise SystemExit("message-frame.md needs two --- lines: opening between them, closing after")
    return parts[1].strip(), parts[2].strip()


def compose_message(team, week, documents, questions):
    opening, closing = message_frame()
    names = ", ".join(documents)
    opening = opening.format(team=team, week=week, documents=names)
    body = "\n".join(f"{i}. {q}" for i, q in enumerate(questions, 1))
    return f"{opening}\n\n{body}\n\n{closing}\n"


def parse_question_output(text):
    """(register lines as (id, status, note), questions as (return_id or None, text))."""
    reg_part, q_part = text.split("## QUESTIONS", 1)
    reg_part = reg_part.split("## REGISTER", 1)[1]
    reg = []
    for line in reg_part.splitlines():
        line = line.strip().strip("-* ")
        if not line or line.lower() == "none":
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) >= 2:
            reg.append((cells[0], cells[1].lower(), cells[2] if len(cells) > 2 else ""))
    qs = []
    for line in q_part.splitlines():
        m = re.match(r"^\s*(?:\d+[.)]|-|\*)\s+(.*\S)\s*$", line)
        if not m:
            continue
        q = m.group(1)
        r = re.match(r"^\[return\s+([^\]]+)\]\s*(.*)$", q, re.I)
        qs.append((r.group(1).strip(), r.group(2).strip()) if r else (None, q))
    return reg, qs


def step_question(root, week, only_team=None):
    done, problems = [], []
    instructions = (HERE / "instructions-documents.txt").read_text(encoding="utf-8") \
        .replace("{{TODAY}}", dt.date.today().strftime("%-d %B %Y"))
    for team in teams_in(root, only_team):
        week_dir = root / "teams" / team / f"week-{week:02d}"
        if not week_dir.is_dir():
            continue
        out_q, out_m = week_dir / "team" / "questions.md", week_dir / "team" / "message.md"
        if out_q.exists():
            continue
        texts = latest_texts(week_dir, team, week)
        if not texts:
            continue

        # every score that is due must exist; a deliverable with no sheet is due nothing
        readings, waiting = [], []
        for deliv in sorted(texts):
            score = week_dir / "owners" / f"score-{deliv}.md"
            if score.exists():
                readings.append(f"## Reading of the {deliv}\n\n{score_columns(score)}")
            elif (root / "rubric" / f"{deliv}-scoresheet.md").exists():
                waiting.append(deliv)
        if waiting:
            problems.append(f"{team}: questions not written, waiting for score of {', '.join(waiting)}")
            continue
        coherence = week_dir / "owners" / "coherence.md"
        if coherence.exists() and "## FINDINGS" in coherence.read_text(encoding="utf-8"):
            findings = coherence.read_text(encoding="utf-8").split("## FINDINGS", 1)[1].split("## DIRECTIONS", 1)[0].strip()
            findings = re.sub(r"\bX\d\b", "", findings)
            readings.append(f"## Reading of how this week's document agrees with the earlier ones\n\n{findings}")

        reg_path = root / "teams" / team / "register.tsv"
        register = read_tsv(reg_path, REGISTER_HEADER)
        open_rows = [r for r in register if r["status"] in STILL_OPEN]
        reg_text = "\n".join(f"{r['id']} | asked in week {r['asked']} about the {r['about']} | {r['status']} | {r['question']}"
                             for r in open_rows) or "none — this is the team's first week; the rules on history do not apply."
        docs_text = "\n\n".join(f"## The {d} (version {v})\n\n{p.read_text(encoding='utf-8', errors='replace')}"
                                for d, (v, p) in sorted(texts.items()))
        message = (f"# THE REGISTER\n\n{reg_text}\n\n# THE DOCUMENTS — {team}, week {week}\n\n{docs_text}\n\n"
                   f"# THE READING\n\n" + ("\n\n".join(readings) or "none"))
        (week_dir / "owners").mkdir(parents=True, exist_ok=True)
        (week_dir / "owners" / "question-input.md").write_text(message, encoding="utf-8")

        text = call_model("questioner", instructions, message, QUESTION_SHAPES)
        if not text:
            problems.append(f"{team}: no questions after {RETRIES + 1} attempts")
            continue
        reg_updates, qs = parse_question_output(text)
        if not 3 <= len(qs) <= 5:
            problems.append(f"{team}: {len(qs)} questions, not three to five; nothing written")
            continue

        # apply the register updates, then add the new questions
        by_id = {r["id"]: r for r in register}
        for rid, status, note in reg_updates:
            if rid not in by_id or status not in STATUSES:
                problems.append(f"{team}: register line ignored: {rid} | {status}")
                continue
            by_id[rid]["status"] = status
            by_id[rid]["evidence"] = note
            if status in ("answered", "withdrawn"):
                by_id[rid]["resolved"] = str(week)
        n = 1
        final_questions = []
        for return_id, q in qs:
            if return_id and return_id in by_id:
                by_id[return_id]["status"] = "open"
                by_id[return_id]["evidence"] = f"returned in week {week}: " + by_id[return_id]["evidence"]
                by_id[return_id]["question"] = q or by_id[return_id]["question"]
                final_questions.append(q or by_id[return_id]["question"])
                continue
            while f"{team}-w{week:02d}-q{n}" in by_id:
                n += 1
            rid = f"{team}-w{week:02d}-q{n}"
            named = [d for d in current_documents(root, team) if re.search(rf"\b{d}\b", q, re.I)]
            about = "coherence" if coherence.exists() and len(named) >= 2 else "+".join(sorted(texts))
            by_id[rid] = {"id": rid, "asked": str(week), "about": about, "question": q,
                          "status": "open", "resolved": "", "evidence": ""}
            final_questions.append(q)
        still_open = [r for r in by_id.values() if r["status"] in STILL_OPEN]
        if len(still_open) > MAX_OPEN:
            problems.append(f"{team}: {len(still_open)} questions open after this week, more than {MAX_OPEN}; nothing written")
            continue

        # the lint stands between the questions and the door
        composed = compose_message(team, week, sorted(texts), final_questions)
        hits = lint_message(composed, root, [p.read_text(encoding='utf-8', errors='replace') for _, p in texts.values()])
        if hits:
            for why, line in hits:
                problems.append(f"{team}: message failed lint ({why}): {line[:120]}")
            (week_dir / "owners" / "message-rejected.md").write_text(composed, encoding="utf-8")
            continue

        write_tsv(reg_path, REGISTER_HEADER, [by_id[k] for k in by_id],
                  comment="every question ever asked; status open/partly/ducked come back next week")
        out_q.parent.mkdir(parents=True, exist_ok=True)
        out_q.write_text("\n".join(f"{i}. {q}" for i, q in enumerate(final_questions, 1)) + "\n", encoding="utf-8")
        out_m.write_text(composed, encoding="utf-8")
        changed = ", ".join(f"{rid}→{st}" for rid, st, _ in reg_updates) or "no earlier questions"
        done.append(f"{team}: {len(final_questions)} questions → {out_m.relative_to(root)}; register: {changed}")
    return done, problems


# ----------------------------------------------------------------------------
# step 2b — coherence: do the team's documents describe one platform?
# ----------------------------------------------------------------------------

COHERENCE_SHAPES = [["## TRACE", "## FINDINGS", "## DIRECTIONS"]]


def current_documents(root, team):
    """{deliverable: (week, version, text path)} from documents.tsv, text present."""
    out = {}
    for r in read_tsv(root / "teams" / team / "documents.tsv", DOCUMENTS_HEADER):
        if r["text"] and (root / r["text"]).exists():
            out[r["deliverable"]] = (int(r["week"]), int(r["version"]), root / r["text"])
    return out


def step_coherence(root, week, only_team=None):
    done, problems = [], []
    sheet = root / "rubric" / "coherence-scoresheet.md"
    for team in teams_in(root, only_team):
        week_dir = root / "teams" / team / f"week-{week:02d}"
        if not week_dir.is_dir():
            continue
        out = week_dir / "owners" / "coherence.md"
        if out.exists():
            continue
        docs = current_documents(root, team)
        if len(docs) < 2:
            print(f"  {team}: coherence skipped — {len(docs)} document(s) so far, needs two")
            continue
        if not sheet.exists():
            problems.append(f"{team}: coherence unchecked: no sheet rubric/{sheet.name}")
            continue
        listing = ", ".join(f"{d} (week {w}, v{v})" for d, (w, v, _) in sorted(docs.items()))
        fields = {"team": team, "week": week, "documents": listing,
                  "sheet": f"rubric/{sheet.name} sha256 {sha256(sheet)[:12]}", "checked": now()}
        message = f"# THE DOCUMENTS — {team}, latest version of each, as of week {week}\n\n" + "\n\n".join(
            f"## The {d} — handed in week {w}, version {v}\n\n{path.read_text(encoding='utf-8', errors='replace')}"
            for d, (w, v, path) in sorted(docs.items()))
        text = call_model("coherence", sheet.read_text(encoding="utf-8"), message, COHERENCE_SHAPES)
        if not text:
            problems.append(f"{team}: no coherence report after {RETRIES + 1} attempts")
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(header(fields) + text.strip() + "\n", encoding="utf-8")
        n = len(re.findall(r"^\s*(?:\d+[.)]|-|\*|#{3,})\s*\S", text.split("## FINDINGS", 1)[1].split("## DIRECTIONS", 1)[0], re.M))
        done.append(f"{team}: coherence over {len(docs)} documents, {n} finding(s) → {out.relative_to(root)}")
    return done, problems


STEPS = [
    ("intake", step_intake),
    ("score", step_score),
    ("coherence", step_coherence),
    ("question", step_question),
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
