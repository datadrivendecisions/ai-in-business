#!/usr/bin/env python3
"""Keep project-documentation/worklog.md honest about how much time this took.

Two jobs, and only one of them can run in CI.

  worklog.py hours     # local only: read the Claude Code transcripts and
                       # report the active time not yet booked
  worklog.py book      # local only: record what has been counted, so a session
                       # booked while still running is topped up next time
  worklog.py verify    # anywhere: the stated total equals the table's sum

The split is forced by where the evidence lives. Session transcripts sit in
~/.claude/projects/ on whoever's laptop ran them; they are not in the
repository and never will be, so a CI runner cannot recompute an hour. What CI
*can* do is refuse a total that no longer matches the rows beneath it, which is
the failure that actually happens: someone adds a session and forgets the
header.

ACTIVE TIME, NOT WALL CLOCK. A session's first and last timestamps are useless
here — two of the early ones span eighteen and twenty-two hours because the
window was left open overnight, which would have booked 41 hours against a
fortnight that held about six. So the measure is the sum of the gaps between
consecutive messages with each gap capped at GAP_CAP_MINUTES: a pause longer
than the cap is someone doing something else, and is counted as the cap rather
than in full. The cap is a judgement and it moves the number (5 min gave 4.4 h,
30 min gave 8.5 h over the same transcripts), so it is named here, stated in
worklog.md, and left alone unless there is a reason.
"""

import json
import pathlib
import re
import subprocess
import sys
from datetime import datetime

GAP_CAP_MINUTES = 15
WORKLOG = "project-documentation/worklog.md"

# The visible header line the table must agree with.
TOTAL_RE = re.compile(r"Total recorded:\s*\*\*([0-9]+(?:\.[0-9]+)?)\s*h\*\*")
# Sessions already booked, kept in an HTML comment so a reader never meets it.
BOOKED_RE = re.compile(r"<!--\s*worklog:booked(.*?)-->", re.S)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          check=True).stdout.strip()


def main_checkout():
    """The main checkout, even when called from a linked worktree.

    Transcripts are keyed on the main checkout's path plus a suffix per
    worktree, so this is the right root for finding them.
    """
    common = _git("rev-parse", "--path-format=absolute", "--git-common-dir")
    return pathlib.Path(common).parent


def worklog_path():
    """The worklog in the tree we are standing in, not the main checkout.

    These two roots differ inside a worktree, and conflating them was a real
    bug: the booked-sessions list was read from a file the worktree had not
    got, so every session reported as new and would have been booked twice.
    """
    return pathlib.Path(_git("rev-parse", "--show-toplevel")) / WORKLOG


def transcript_files(root):
    """Every transcript for this repository, worktrees included.

    Claude Code keys transcripts on the working directory, not the repository,
    so a session run inside .claude/worktrees/<name> lands in its own project
    folder: <repo slug>--claude-worktrees-<name>. Globbing the prefix rather
    than opening one directory is the whole point — the first version of this
    read only the main checkout and booked zero hours for worktree sessions,
    which is a total that is quietly too low and therefore worse than none.
    """
    slug = str(root).replace("/", "-").replace(".", "-")
    projects = pathlib.Path.home() / ".claude" / "projects"
    if not projects.is_dir():
        return []
    files = []
    for d in projects.iterdir():
        if d.is_dir() and (d.name == slug or d.name.startswith(slug + "-")):
            files.extend(d.glob("*.jsonl"))
    return files


def active_minutes(path):
    """Sum the inter-message gaps, each capped. Returns (start, minutes)."""
    stamps = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            ts = rec.get("timestamp")
            if ts:
                stamps.append(datetime.fromisoformat(ts.replace("Z", "+00:00")))
    if len(stamps) < 2:
        return None, 0.0
    stamps.sort()
    total = sum(min((b - a).total_seconds() / 60, GAP_CAP_MINUTES)
                for a, b in zip(stamps, stamps[1:]))
    return stamps[0], total


def booked_minutes(text):
    """id -> minutes already booked, from the worklog:booked comment.

    Minutes rather than a bare list of ids, because a session can be booked
    while it is still running: the row goes in, the conversation continues, and
    everything after the commit would be lost for good if the id alone marked
    it done. Storing the figure lets a later run book only the difference.
    """
    m = BOOKED_RE.search(text)
    if not m:
        return {}
    out = {}
    for token in m.group(1).split():
        sid, _, mins = token.partition(":")
        out[sid] = float(mins) if mins else 0.0
    return out


def measure(files):
    """(start, minutes) per session id, skipping windows that only opened."""
    seen = {}
    for f in sorted(files):
        start, mins = active_minutes(f)
        if start is not None and mins >= 0.5:
            seen[f.stem[:8]] = (start, mins)
    return seen


def table_hours(text):
    """Every Hours cell in the sessions ledger.

    A session row is recognised by shape rather than by position in the file:
    a date in the first cell and a number in the third. The checks register
    above it is also a table, and keying off "the third table column" alone
    would eventually read a row of it as an hour.
    """
    hours = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not DATE_RE.match(cells[0]):
            continue
        try:
            hours.append(float(cells[2]))
        except ValueError:
            continue
    return hours


def cmd_hours():
    files = transcript_files(main_checkout())
    if not files:
        sys.exit("No Claude Code transcripts for this repository on this machine.")
    log = worklog_path()
    booked = booked_minutes(log.read_text()) if log.exists() else {}

    fresh = 0.0
    print(f"Active time, gaps capped at {GAP_CAP_MINUTES} min:\n")
    for sid, (start, mins) in sorted(measure(files).items(), key=lambda kv: kv[1][0]):
        owed = mins - booked.get(sid, 0.0)
        fresh += max(owed, 0.0)
        mark = "NEW   " if sid not in booked else ("+more " if owed > 0.5 else "booked")
        extra = f"  (+{owed / 60:.2f} h since booking)" if 0.5 < owed < mins else ""
        print(f"  {mark}  {sid}  {start:%Y-%m-%d %H:%M}  {mins / 60:5.2f} h{extra}")
    print(f"\n  {fresh / 60:.2f} h not yet in {WORKLOG}")
    if fresh:
        print("  Add or adjust the rows, then run:  worklog.py book")


def cmd_book():
    """Rewrite the worklog:booked comment with what the transcripts now say.

    Transcribing eight figures by hand is how a ledger picks up its first wrong
    number, so the machine writes them. The visible rows and the total are
    still yours to edit; `verify` is what checks you got them to agree.
    """
    log = worklog_path()
    text = log.read_text()
    seen = measure(transcript_files(main_checkout()))
    lines = [f"{sid}:{mins:.1f}"
             for sid, (_, mins) in sorted(seen.items(), key=lambda kv: kv[1][0])]
    block = "<!-- worklog:booked\n" + "\n".join(lines) + "\n-->"
    if not BOOKED_RE.search(text):
        sys.exit(f"::error file={WORKLOG}::no worklog:booked comment to update")
    log.write_text(BOOKED_RE.sub(lambda _: block, text, count=1))
    total = sum(m for _, m in seen.values())
    print(f"Booked {len(seen)} sessions, {total / 60:.2f} h in total.")
    print(f"The ledger's rows must now add up to that; run verify.")


def cmd_verify():
    path = worklog_path()
    if not path.exists():
        sys.exit(f"::error file={WORKLOG}::the worklog is missing")
    text = path.read_text()

    m = TOTAL_RE.search(text)
    if not m:
        sys.exit(f"::error file={WORKLOG}::no 'Total recorded: **N h**' line to check")
    stated = float(m.group(1))
    hours = table_hours(text)
    summed = round(sum(hours), 2)

    # Each row is rounded to two places, so the sum drifts by at most half a
    # cent per row. Anything larger is a row someone forgot to add up.
    if abs(stated - summed) > 0.05 + 0.005 * len(hours):
        sys.exit(f"::error file={WORKLOG}::header says {stated} h, "
                 f"the {len(hours)} session rows add up to {summed} h")
    print(f"Worklog adds up: {len(hours)} sessions, {summed} h, header agrees.")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    if action == "hours":
        cmd_hours()
    elif action == "book":
        cmd_book()
    elif action == "verify":
        cmd_verify()
    else:
        sys.exit(__doc__)
