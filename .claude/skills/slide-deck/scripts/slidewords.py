#!/usr/bin/env python3
"""Words, bullets and longest sentence per slide card in a week-NN-slides.html deck.

A slide is read or listened to, never both. This counts what a card asks a
student to read, and flags the cards that ask too much:

  body  > 40 words       the card is telling the story instead of supporting it
  bullets > 3            more than one glance
  sentence > 20 words    D1 for projected text (strip-ai-language)
  headline > 12 words    an assertion, not a paragraph

Usage:
  python3 slidewords.py site/week-02-slides.html [more decks...]
  python3 slidewords.py deck.html --max-words 40 --max-bullets 3 --max-sentence 20
Exit 1 when any card is flagged, 0 otherwise.
"""
import argparse
import html
import re
import sys

SLIDE = re.compile(r'<section class="slide[^"]*" id="(s\d+)">(.*?)</section>', re.S)
KICKER = re.compile(r'<div class="slide-kicker">.*?</div>', re.S)
SLIDENO = re.compile(r'<span class="slide-no">.*?</span>', re.S)
H2 = re.compile(r"<h2>(.*?)</h2>", re.S)
TAG = re.compile(r"<[^>]+>")


def text(fragment):
    return html.unescape(TAG.sub(" ", fragment))


def words(t):
    # A separator such as · or — on its own is not a word
    return sum(1 for w in t.split() if re.search(r"[A-Za-z0-9]", w))


def sentences(t):
    # A bullet, a heading and a line break each end a sentence; so do . ! ? ; :
    parts = re.split(r"[.!?;:\n]+|·", t)
    return [p.strip() for p in parts if p.strip()]


def measure(body):
    body = SLIDENO.sub("", KICKER.sub("", body, count=1), count=1)
    m = H2.search(body)
    headline = text(m.group(1)).strip() if m else ""
    rest = H2.sub("", body, count=1)
    # Keep list items and paragraphs as separate lines so a card is never one long sentence
    rest = re.sub(r"</(li|p|h3|div)>", "\n", rest)
    body_text = text(rest)
    bullets = len(re.findall(r"<li\b", rest))
    longest = max((words(s) for s in sentences(body_text)), default=0)
    return {
        "headline": headline,
        "headline_words": words(headline),
        "body_words": words(body_text),
        "bullets": bullets,
        "longest_sentence": longest,
    }


def check(path, limits):
    src = open(path, encoding="utf-8").read()
    flagged = 0
    print(f"{path}")
    print(f"  {'slide':>5} {'words':>5} {'bul':>3} {'sent':>4} {'head':>4}  headline")
    for sid, body in SLIDE.findall(src):
        m = measure(body)
        flags = []
        if m["body_words"] > limits.max_words:
            flags.append(f"body {m['body_words']} > {limits.max_words}")
        if m["bullets"] > limits.max_bullets:
            flags.append(f"bullets {m['bullets']} > {limits.max_bullets}")
        if m["longest_sentence"] > limits.max_sentence:
            flags.append(f"sentence {m['longest_sentence']} > {limits.max_sentence}")
        if m["headline_words"] > limits.max_headline:
            flags.append(f"headline {m['headline_words']} > {limits.max_headline}")
        mark = "!" if flags else " "
        print(f"{mark} {sid:>5} {m['body_words']:>5} {m['bullets']:>3} {m['longest_sentence']:>4} "
              f"{m['headline_words']:>4}  {m['headline'][:56]}")
        for f in flags:
            print(f"        → {f}")
        flagged += bool(flags)
    return flagged


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("decks", nargs="+")
    ap.add_argument("--max-words", type=int, default=40)
    ap.add_argument("--max-bullets", type=int, default=3)
    ap.add_argument("--max-sentence", type=int, default=20)
    ap.add_argument("--max-headline", type=int, default=12)
    a = ap.parse_args(argv)
    total = sum(check(d, a) for d in a.decks)
    print(f"\n{total} card(s) flagged")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
