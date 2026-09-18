#!/usr/bin/env python3
"""Phase 3: check the agent prompt the tool hands the student.

AG-2  it asks for at least three questions about the locked position
AG-4  it states no view of that position
AG-5  it speaks about the position in the third person, and asks its
      questions in the second

The prompt is read out of the shipped page by building it, not by reading the
source, so a prompt reworded in place is re-checked without touching this file.

Only the fixed wording is examined. The claim and the student's own sentence
are stripped first: the claim contains "should" by construction and the
student is free to write "I am right about this", and neither is the tool
stating a view.

    python3 check-prompt.py [-v]
"""

import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent

# Words and phrases that would put a view of the position into the prompt.
# Asking a model not to use them would itself put them in, so the prompt is
# written without them and this list is how that is kept true.
VERDICT = [
    "right", "wrong", "correct", "incorrect", "mistaken", "flawed",
    "sound", "unsound", "valid", "invalid", "true", "false",
    "strong", "weak", "robust", "shaky", "compelling", "convincing",
    "unconvincing", "persuasive", "plausible", "implausible",
    "good", "bad", "better", "worse", "best", "worst",
    "accurate", "inaccurate", "naive", "simplistic", "overstated",
    "understated", "agree", "disagree", "clearly", "obviously",
    "in fact", "the truth", "i think", "in my view", "you are ",
    "rebut", "refute", "debunk", "challenge the", "push back",
]

# First-person possessives attached to the position. "your position" is second
# person and would be a different fault; it is caught by its own check.
FIRST_PERSON = [r"\bmy\s+position\b", r"\bour\s+position\b", r"\bmy\s+view\b", r"\bour\s+view\b"]

NUMBER = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
          "seven": 7, "eight": 8, "nine": 9, "ten": 10}

CLAIM = "An SME should run its AI on small models it controls rather than on frontier models it rents."
LOCKED = "Renting means the price and the model can both change under you."


def build_prompt():
    fixtures = {
        "codebookText": "", "measures": [], "totals": [], "datasets": [], "kappas": [],
        "promptClaim": CLAIM, "promptSide": "agree", "promptLocked": LOCKED,
    }
    tmp = HERE / ".prompt-fixture.json"
    tmp.write_text(json.dumps(fixtures), encoding="utf-8")
    try:
        out = subprocess.run(["node", str(HERE / "runpage.mjs"), str(tmp)],
                             capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit("the page would not run:\n" + e.stderr)
    finally:
        tmp.unlink(missing_ok=True)
    return json.loads(out.stdout)["prompt"]


def template_of(prompt):
    """The prompt minus the parts the student supplied."""
    keep = []
    for line in prompt.splitlines():
        if line.startswith(("CLAIM:", "THE POSITION TAKEN:", "REASON GIVEN:")):
            continue
        keep.append(line)
    return "\n".join(keep)


def main():
    verbose = "-v" in sys.argv
    prompt = build_prompt()
    tpl = template_of(prompt)
    low = tpl.lower()
    fails = []

    if verbose:
        print(prompt)
        print("\n" + "-" * 60 + "\n")

    # AG-2 — it asks for questions, and for at least three of them.
    counts = []
    for m in re.finditer(r"\b(\d+|" + "|".join(NUMBER) + r")\s+questions\b", low):
        tok = m.group(1)
        counts.append(int(tok) if tok.isdigit() else NUMBER[tok])
    asked = max(counts) if counts else 0
    if asked < 3:
        fails.append(f"AG-2: the prompt asks for {asked} questions, and the rule is at least 3")
    elif verbose:
        print(f"AG-2  asks for {asked} questions")

    # AG-2 — and they are about the position the student locked.
    if LOCKED not in prompt:
        fails.append("AG-2: the locked sentence is not in the prompt")
    if CLAIM not in prompt:
        fails.append("AG-2: the claim is not in the prompt")
    if "position" not in low:
        fails.append("AG-2: the prompt never names the position")

    # AG-4 — no view of the position.
    hits = [w for w in VERDICT if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low)]
    if hits:
        fails.append("AG-4: verdict wording in the prompt: " + ", ".join(hits))
    elif verbose:
        print(f"AG-4  0 of {len(VERDICT)} verdict phrases present")

    # AG-5 — third person about the position.
    fp = [p for p in FIRST_PERSON if re.search(p, low)]
    if fp:
        fails.append("AG-5: first-person possessive attached to the position: " + ", ".join(fp))
    elif verbose:
        print("AG-5  0 first-person possessives attached to the position")

    # AG-5 — second person in what it asks for.
    if not re.search(r'\byou\b|\byour\b', low):
        fails.append("AG-5: the prompt never addresses the student as \"you\"")
    elif verbose:
        print("AG-5  addresses the student as \"you\"")

    # A prompt that asked for prose as well as questions would let the model
    # deliver its view inside the prose.
    for banned in ["summary", "summarise", "explain why", "assessment of whether", "verdict"]:
        if banned in low:
            fails.append(f"AG-4: the prompt asks for “{banned}”, which is room for a view")

    print()
    if fails:
        for f in fails:
            print("  " + f)
        return 1
    print("The prompt asks for questions, states no view, and speaks of the position in the third person.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
