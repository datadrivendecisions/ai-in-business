"""What a submission may contain, and nothing else.

SV-1 says the submission carries no free text. There are two ways to build
that. The weak one strips prose out of whatever arrives. The strong one
refuses a payload carrying any field this file does not name, so a field
nobody thought about cannot travel by being ignored -- and the day someone
adds the student's closing sentence to the tool, the service rejects it
rather than storing it.

Every value is a number, a boolean, or a member of a named set. The two
strings that survive are the student's self-chosen code and their card ids,
and both are held to a pattern narrow enough that neither can carry a
sentence: twenty characters of lowercase, and a card id out of thirty-two.
"""

import re

LINE_VERSION = 2            # 2 added `pick`, the seconds to choosing a side

CODE = re.compile(r"^[a-z0-9][a-z0-9-]{0,19}$")
CARD_ID = re.compile(r"^c[12]-(?:0[1-9]|1[0-6])$")

SIDES = ("a", "d")           # agreed with the claim, or disagreed
TEAMS = range(1, 9)
CLAIMS = (1, 2)
ROUNDS = (1, 2)

MAX_OPENED = 8               # the budget, SM-3
MAX_SECONDS = 60 * 60        # an hour in one round is not a session
TLX_RANGE = (0, 100)         # the workload total, rescaled
Q_RANGE = (2, 14)            # two 7-point items


class Rejected(Exception):
    """A payload that will not be stored, and the reason, in one sentence."""


def _require(condition, message):
    if not condition:
        raise Rejected(message)


def _only(mapping, allowed, where):
    extra = sorted(set(mapping) - set(allowed))
    _require(not extra, "%s carries %s, which this service does not accept"
             % (where, ", ".join(repr(k) for k in extra)))


def _int(value, low, high, where):
    _require(isinstance(value, int) and not isinstance(value, bool),
             "%s must be a whole number" % where)
    _require(low <= value <= high, "%s must be between %d and %d" % (where, low, high))
    return value


def _bool(value, where):
    _require(isinstance(value, bool), "%s must be true or false" % where)
    return value


def _member(value, allowed, where):
    _require(value in allowed, "%s must be one of %s"
             % (where, ", ".join(repr(a) for a in allowed)))
    return value


def clean_round(raw, expected_n):
    _require(isinstance(raw, dict), "each round must be an object")
    fields = ("n", "agent", "claim", "side", "pick", "opened", "seconds",
              "endSide", "moved", "tlx", "q")
    _only(raw, fields, "round %d" % expected_n)
    for field in fields:
        _require(field in raw, "round %d is missing %r" % (expected_n, field))

    where = "round %d" % expected_n
    opened = raw["opened"]
    _require(isinstance(opened, list), "%s: opened must be a list" % where)
    _require(len(opened) <= MAX_OPENED,
             "%s: opened %d cards, and the budget is %d" % (where, len(opened), MAX_OPENED))
    for card in opened:
        _require(isinstance(card, str) and CARD_ID.match(card),
                 "%s: %r is not a card id" % (where, card))
    _require(len(set(opened)) == len(opened), "%s: the same card twice" % where)

    claim = _member(raw["claim"], CLAIMS, "%s: claim" % where)
    for card in opened:
        _require(card.startswith("c%d-" % claim),
                 "%s: %s does not belong to claim %d" % (where, card, claim))

    return {
        "n": _member(raw["n"], (expected_n,), "%s: n" % where),
        "agent": _bool(raw["agent"], "%s: agent" % where),
        "claim": claim,
        "side": _member(raw["side"], SIDES, "%s: side" % where),
        "pick": _int(raw["pick"], 0, MAX_SECONDS, "%s: pick" % where),
        "opened": list(opened),
        "seconds": _int(raw["seconds"], 0, MAX_SECONDS, "%s: seconds" % where),
        "endSide": _member(raw["endSide"], SIDES, "%s: endSide" % where),
        "moved": _bool(raw["moved"], "%s: moved" % where),
        "tlx": _int(raw["tlx"], TLX_RANGE[0], TLX_RANGE[1], "%s: tlx" % where),
        "q": _int(raw["q"], Q_RANGE[0], Q_RANGE[1], "%s: q" % where),
    }


def clean_submission(raw):
    """A stored submission, or Rejected with the reason."""
    _require(isinstance(raw, dict), "the body must be a JSON object")
    _only(raw, ("v", "code", "team", "rounds"), "the submission")
    for field in ("v", "code", "team", "rounds"):
        _require(field in raw, "the submission is missing %r" % field)

    _require(raw["v"] == LINE_VERSION,
             "this service reads version %d and the line says %r"
             % (LINE_VERSION, raw["v"]))

    code = raw["code"]
    _require(isinstance(code, str) and CODE.match(code),
             "a code is up to 20 characters of lowercase letters, digits and hyphens")

    rounds = raw["rounds"]
    _require(isinstance(rounds, list) and len(rounds) == len(ROUNDS),
             "a submission carries %d rounds" % len(ROUNDS))

    cleaned = [clean_round(r, n) for r, n in zip(rounds, ROUNDS)]
    _require(cleaned[0]["claim"] != cleaned[1]["claim"],
             "the two rounds carry the same claim")
    _require(cleaned[0]["agent"] != cleaned[1]["agent"],
             "the assistant appears in exactly one of the two rounds")

    return {
        "v": LINE_VERSION,
        "code": code,
        "team": _int(raw["team"], TEAMS[0], TEAMS[-1], "team"),
        "rounds": cleaned,
    }
