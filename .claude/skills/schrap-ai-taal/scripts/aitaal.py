#!/usr/bin/env python3
"""Zoekt in Nederlandse tekst naar constructies die verraden dat een taalmodel
meeschreef, en naar taal die boven het niveau van de lezer gaat.

Werkt op .md, .txt en .html. Bij HTML worden tags en entiteiten vervangen door
even lange stukken spatie, zodat regelnummers en citaten van de gevonden plek
naar het bronbestand blijven wijzen.

    python3 aitaal.py college.html
    python3 aitaal.py map/ --recursief --codes A1,A2 --json bevindingen.json
    python3 aitaal.py deck.html --negeer-html-klasse notes   # notities overslaan
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
# drempels — startwaarden, bijgesteld na meting op echt materiaal
# --------------------------------------------------------------------------
STREEP_PER_100 = 1.2      # A10: gedachtestrepen per 100 woorden
RITME_MIN_ZINNEN = 8      # A11: minder zinnen dan dit zegt niets over ritme
RITME_SPREIDING = 0.38    # A11: variatiecoëfficiënt van de zinslengte
DRIESLAG_PER_100 = 1.5    # A12: "X, Y en Z"-opsommingen per 100 woorden
ZIN_MAX_WOORDEN = 20      # D1: bovengrens voor een eerstejaarslezer
ABSTRACT_PER_100 = 6.0    # D2: naamwoorden van handeling per 100 woorden


@dataclass
class Melding:
    code: str
    bestand: str
    regel: int
    context: str
    citaat: str
    uitleg: str


# --------------------------------------------------------------------------
# tekst binnenhalen
# --------------------------------------------------------------------------
# Een blokelement beëindigt een zin: twee alinea's naast elkaar op een dia horen
# niet als één zin van veertig woorden geteld te worden. De grens krijgt een eigen
# teken in plaats van een regeleinde, zodat regelnummers blijven kloppen.
GRENS = "\x1e"
BLOKTAG = re.compile(
    r"</?(?:p|div|li|ul|ol|h[1-6]|t[dhr]|table|section|article|figure|figcaption|"
    r"blockquote|br|dd|dt|dl|caption)\b[^>]*>", re.I)


def _blank(m: re.Match) -> str:
    """Vervangt een stuk opmaak door even veel spaties, met behoud van regeleinden."""
    return re.sub(r"[^\n]", " ", m.group(0))


def _blok(m: re.Match) -> str:
    """Zelfde, maar laat een zinsgrens achter op de plek van de tag."""
    return GRENS + re.sub(r"[^\n]", " ", m.group(0))[1:]


def ontdoe_html(tekst: str, negeer_klassen: tuple[str, ...] = (),
                blok_extra: tuple[str, ...] = ()) -> str:
    """Haalt de opmaak weg maar houdt elke positie op zijn plek.

    Entiteiten worden vervangen door hun teken plus opvulling, zodat &mdash;
    als — meetelt zonder dat de rest van de regel verschuift."""
    for klasse in negeer_klassen:
        patroon = re.compile(
            r'<(\w+)[^>]*class="[^"]*\b' + re.escape(klasse) + r'\b[^"]*"[^>]*>.*?</\1>', re.S)
        tekst = patroon.sub(_blank, tekst)
    tekst = re.sub(r"<(script|style)\b.*?</\1>", _blank, tekst, flags=re.S | re.I)
    tekst = re.sub(r"<!--.*?-->", _blank, tekst, flags=re.S)
    tekst = re.sub(r"<svg\b.*?</svg>", _blank, tekst, flags=re.S | re.I)
    tekst = BLOKTAG.sub(_blok, tekst)
    if blok_extra:
        extra = re.compile(r"</?(?:" + "|".join(re.escape(e) for e in blok_extra) + r")\b[^>]*>", re.I)
        tekst = extra.sub(_blok, tekst)
    tekst = re.sub(r"<[^>]+>", _blank, tekst)

    def _entiteit(m: re.Match) -> str:
        teken = unescape(m.group(0))
        if len(teken) != 1:                      # onbekend: laat staan als spaties
            return " " * len(m.group(0))
        return teken + " " * (len(m.group(0)) - 1)

    return re.sub(r"&[#\w]+;", _entiteit, tekst)


def lees(pad: Path, negeer_klassen: tuple[str, ...] = (),
         blok_extra: tuple[str, ...] = ()) -> str:
    rauw = pad.read_text(encoding="utf-8", errors="replace")
    if pad.suffix.lower() in (".html", ".htm", ".xhtml"):
        return ontdoe_html(rauw, negeer_klassen, blok_extra)
    return rauw


# --------------------------------------------------------------------------
# structuur: regelnummer en de kop waar een plek onder valt
# --------------------------------------------------------------------------
def regel_van(tekst: str, positie: int) -> int:
    return tekst.count("\n", 0, positie) + 1


def bouw_context(rauw: str) -> list[tuple[int, str]]:
    """Ankers waaronder een melding valt: data-title uit HTML of een markdown-kop."""
    ankers: list[tuple[int, str]] = []
    for m in re.finditer(r'data-title="([^"]*)"', rauw):
        ankers.append((m.start(), m.group(1)))
    for m in re.finditer(r"^#{1,6}\s+(.+)$", rauw, re.M):
        ankers.append((m.start(), m.group(1).strip()))
    ankers.sort()
    return ankers


def context_van(ankers: list[tuple[int, str]], positie: int) -> str:
    naam = ""
    for start, titel in ankers:
        if start > positie:
            break
        naam = titel
    return naam


# --------------------------------------------------------------------------
# zinnen
# --------------------------------------------------------------------------
_AFKORTING = re.compile(r"\b(bijv|nl|o\.a|d\.w\.z|etc|dr|ir|drs|prof|nr|blz|fig|vs|ca)\.$", re.I)


def zinnen(tekst: str) -> list[tuple[int, str]]:
    """Splitst op zinseinde en geeft (startpositie, zin). Afkortingen breken niet."""
    uit: list[tuple[int, str]] = []
    start = 0
    for m in re.finditer(r"[.!?…](?=\s|$)|\n{2,}|" + GRENS + "+", tekst):
        stuk = tekst[start:m.end()]
        if _AFKORTING.search(stuk.strip()):
            continue
        if stuk.strip():
            uit.append((start + len(stuk) - len(stuk.lstrip()), stuk.strip()))
        start = m.end()
    rest = tekst[start:]
    if rest.strip():
        uit.append((start + len(rest) - len(rest.lstrip()), rest.strip()))
    return uit


def woorden(s: str) -> list[str]:
    return re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'’-]*", s)


# --------------------------------------------------------------------------
# A1 t/m A9 — patronen die een regel kan aanwijzen
# --------------------------------------------------------------------------
def _p(*varianten: str) -> re.Pattern:
    return re.compile("|".join(varianten), re.I)


PATRONEN: list[tuple[str, re.Pattern, str]] = [
    ("A1", _p(
        r"\bniet\s+(?:om\s+|over\s+|alleen\s+)?[\w’'-]+(?:\s+[\w’'-]+){0,4},?\s+maar\b",
        r"\bgeen\s+[\w’'-]+(?:\s+[\w’'-]+){0,4},?\s+(?:maar|wel)\b",
        r"\bzonder\s+[\w’'-]+(?:\s+[\w’'-]+){0,3}\s+(?:is|zijn|bestaat|heb\s+je|kun\s+je)\s+(?:er\s+)?geen\b",
        r"\bdan\s+is\s+het\s+er\s+geen\b",
        r"\bminder\s+[\w’'-]+,\s*meer\b",
        r"\bhet\s+gaat\s+niet\s+om\b",
        r"\bdit\s+is\s+geen\s+[\w’'-]+[.,]\s*(?:dit|het)\s+is\b",
    ), "tegenstelling die diepgang nabootst; zeg gewoon wat het wél is"),

    ("A2", _p(
        r"\b(?:cruciaal|cruciale|essentieel|essentiële|fundamenteel|fundamentele|onmisba(?:ar|re)|"
        r"baanbrekende?|revolutionaire?|ongekende?|indrukwekkende?|krachtige?|waardevolle?|"
        r"game[- ]?changer|sleutelrol|spilfunctie|van\s+onschatbare\s+waarde|"
        r"niet\s+weg\s+te\s+denken|van\s+cruciaal\s+belang|van\s+groot\s+belang)\b",
    ), "sterk woord zonder mechanisme, cijfer of voorbeeld erachter"),

    ("A3", _p(
        r"\bin\s+(?:de|het)\s+(?:snel\s+veranderende|steeds\s+veranderende|huidige|hedendaagse)\b",
        r"\bin\s+een\s+wereld\s+(?:waarin|die)\b",
        r"\bhet\s+is\s+(?:belangrijk|goed|nuttig)\s+om\s+(?:te\s+)?(?:beseffen|weten|onthouden|vermelden)\b",
        r"\blaten\s+we\s+(?:eens\s+)?kijken\s+naar\b",
        r"\bin\s+dit\s+(?:hoofdstuk|onderdeel|deel)\s+(?:bespreken|behandelen|bekijken)\s+we\b",
        r"\bwat\s+dit\s+(?:zo\s+)?(?:bijzonder|uniek|interessant)\s+maakt\b",
        r"\bvoordat\s+we\s+(?:verder\s+gaan|beginnen),?\s+(?:is\s+het|moeten\s+we)\b",
    ), "opwarmer zonder informatie; begin bij je kernpunt"),

    ("A4", _p(
        r"\b(?:het\s+)?(?:\w+)?landschap\b",
        r"\becosysteem\b",
        r"\bspeelveld\b",
        r"\bde\s+wereld\s+van\s+(?:de\s+|het\s+)?\w+",
        r"\bop\s+het\s+gebied\s+van\b",
        r"\bin\s+de\s+context\s+van\b",
        r"\bhet\s+domein\s+van\b",
    ), "containerbegrip; benoem de organisatie, de mensen of de plek zelf"),

    ("A5", _p(
        r"\bduik(?:en|t)?\s+(?:we\s+|je\s+|ik\s+)?in\b", r"\bontgrendel(?:en|t|d)?\b",
        r"\bnaadloos\b", r"\bmoeiteloos\b", r"\bempower\w*\b", r"\bleverage\w*\b",
        r"\bhandvatten\b", r"\bmeenemen\s+in\b", r"\bmeegenomen\s+in\b",
        r"\bnavigeren\s+(?:door|in)\b", r"\bde\s+vruchten\s+plukken\b",
        r"\bbij\s+uitstek\b", r"\ben\s+dat\s+is\s+precies\b",
    ), "modewoord; kies een gewoon werkwoord"),

    ("A6", _p(
        r"\bvormt\s+(?:de|het|een)\b", r"\bvormen\s+(?:de|het|een)\b",
        r"\bfungeer(?:t|en)\s+als\b", r"\bdien(?:t|en)\s+als\b",
        r"\bstaat\s+voor\b", r"\bmarkeer(?:t|en)\s+(?:een|het|de)\b",
        r"\brepresenteer(?:t|en)\b", r"\bspeelt\s+een\s+(?:\w+\s+)?rol\b",
        r"\bkent\s+zijn\s+oorsprong\b",
    ), "omweg om 'is' te vermijden"),

    ("A7", _p(
        r"\bde\s+tijd\s+zal\s+(?:het\s+)?(?:leren|uitwijzen)\b",
        r"\bhet\s+blijft\s+afwachten\b", r"\bdat\s+valt\s+nog\s+te\s+bezien\b",
        r"\bde\s+toekomst\s+zal\s+uitwijzen\b",
        r"\ber\s+is\s+nog\s+(?:veel\s+)?ruimte\s+voor\s+verbetering\b",
        r"\béén\s+ding\s+is\s+zeker\b", r"\bhoe\s+dan\s+ook\b",
    ), "slot dat niets besluit; noem een keuze, grens of vervolgstap"),

    ("A8", _p(
        r"\brevolutionee?r(?:t|en|de)\b",
        r"\bverander(?:t|en|de)\s+de\s+manier\s+waarop\b",
        r"\bbrengt\s+ons\s+(?:een\s+stap\s+)?dichter\s+bij\b",
        r"\bde\s+toekomst\s+van\s+\w+\s+is\b",
        r"\bzal\s+alles\s+verander(?:en|d)\b",
        r"\bnooit\s+meer\s+hetzelfde\b",
    ), "toekomstbelofte zonder voorwaarde of meetpunt"),

    ("A9", _p(
        r"^\s*(?:goede|uitstekende|scherpe)\s+vraag\b",
        r"\bje\s+hebt\s+(?:helemaal\s+)?gelijk\b",
        r"^\s*(?:absoluut|zeker|natuurlijk)[!.]",
        r"\bgoed\s+dat\s+je\s+dit\s+(?:vraagt|opmerkt)\b",
    ), "beleefdheidsformule; laat weg"),
]


def zoek_patronen(tekst: str, codes: set[str] | None) -> list[tuple[str, int, str, str]]:
    """Geeft (code, positie, citaat, uitleg) voor elke treffer."""
    uit = []
    for code, patroon, uitleg in PATRONEN:
        if codes and code not in codes:
            continue
        for m in patroon.finditer(tekst):
            begin, eind = max(0, m.start() - 45), min(len(tekst), m.end() + 45)
            citaat = re.sub(r"\s+", " ", tekst[begin:eind].replace(GRENS, " ")).strip()
            uit.append((code, m.start(), citaat, uitleg))
    return uit


# --------------------------------------------------------------------------
# A10 t/m A12 en D1 t/m D2 — dichtheden en ritme
# --------------------------------------------------------------------------
JARGON = {
    "stakeholder", "stakeholders", "governance", "compliance", "alignment", "mindset",
    "scope", "deliverable", "deliverables", "benchmark", "kpi", "kpi's", "roadmap",
    "framework", "asset", "assets", "onboarding", "agile", "lean", "scrum", "sprint",
    "value proposition", "business case", "best practice", "best practices",
    "stakeholdermanagement", "disruptie", "disruptief", "schaalbaar", "schaalbaarheid",
    "esg", "csrd", "iot", "cybersecurity", "circulariteit", "faciliteren", "raci",
}


def is_uitgelegd(zin: str, term: str) -> bool:
    """Waar als de vakterm zijn uitleg in dezelfde zin bij zich draagt.

    Drie vormen tellen: een omschrijving tussen haakjes ('slimme apparaten (IoT)'),
    een dubbele punt of isgelijkteken in de zin ('Agile: werken in korte rondes'),
    en de term als deel van een eigennaam ('Integrated Reporting Framework')."""
    m = re.search(r"\b" + re.escape(term) + r"\b", zin, re.I)
    if not m:
        return False
    rond = zin[max(0, m.start() - 3):m.end() + 3]
    if "(" in rond or ")" in rond:
        return True
    if re.search(r"[:=]", zin):
        return True
    voor = zin[:m.start()].rstrip().split(" ")[-1:]
    na = zin[m.end():].lstrip().split(" ")[:1]
    buren = [w for w in voor + na if w]
    return bool(zin[m.start():m.start() + 1].isupper()
                and buren and any(w[:1].isupper() for w in buren))
ABSTRACT = re.compile(r"\b\w{5,}(?:ing|heid|iteit|isatie|atie|isme)\b", re.I)


def meet_dichtheden(tekst: str, codes: set[str] | None) -> list[tuple[str, int, str, str]]:
    uit: list[tuple[str, int, str, str]] = []
    alle = woorden(tekst)
    n = len(alle) or 1

    if not codes or "A10" in codes:
        strepen = [m.start() for m in re.finditer(r"—|--", tekst)]
        per100 = 100 * len(strepen) / n
        if per100 > STREEP_PER_100 and len(strepen) >= 5:
            uit.append(("A10", strepen[0],
                        f"{len(strepen)} gedachtestrepen op {n} woorden ({per100:.1f} per 100)",
                        f"boven {STREEP_PER_100} per 100; maak er punten of komma's van"))

    zn = [z for _, z in zinnen(tekst)]
    lengtes = [len(woorden(z)) for z in zn if len(woorden(z)) >= 3]
    if (not codes or "A11" in codes) and len(lengtes) >= RITME_MIN_ZINNEN:
        gem = statistics.mean(lengtes)
        spreiding = statistics.pstdev(lengtes) / gem if gem else 1
        if spreiding < RITME_SPREIDING:
            uit.append(("A11", 0,
                        f"{len(lengtes)} zinnen, gemiddeld {gem:.0f} woorden, spreiding {spreiding:.2f}",
                        f"onder {RITME_SPREIDING}: elke zin even lang; wissel kort en lang af"))

    if not codes or "A12" in codes:
        drie = [m.start() for m in re.finditer(
            r"\b[\w’'-]+,\s+[\w’'-]+\s+en\s+[\w’'-]+\b", tekst)]
        per100 = 100 * len(drie) / n
        if per100 > DRIESLAG_PER_100 and len(drie) >= 4:
            uit.append(("A12", drie[0],
                        f"{len(drie)} drieledige opsommingen op {n} woorden ({per100:.1f} per 100)",
                        "de drieslag als vulling; twee items mag ook"))

    if not codes or "D2" in codes:
        abstracten = ABSTRACT.findall(tekst)
        per100 = 100 * len(abstracten) / n
        if per100 > ABSTRACT_PER_100:
            top = ", ".join(sorted({a.lower() for a in abstracten})[:6])
            uit.append(("D2", 0, f"{per100:.1f} naamwoorden van handeling per 100 woorden ({top}…)",
                        f"boven {ABSTRACT_PER_100}; maak er werkwoorden van"))

    return uit


def meet_zinnen(tekst: str, codes: set[str] | None) -> list[tuple[str, int, str, str]]:
    uit: list[tuple[str, int, str, str]] = []
    for pos, zin in zinnen(tekst):
        w = woorden(zin)
        if (not codes or "D1" in codes) and len(w) > ZIN_MAX_WOORDEN:
            uit.append(("D1", pos, re.sub(r"\s+", " ", zin)[:120],
                        f"{len(w)} woorden; boven {ZIN_MAX_WOORDEN} raakt een eerstejaars de draad kwijt"))
        if not codes or "D3" in codes:
            for term in sorted(JARGON):
                if re.search(r"\b" + re.escape(term) + r"\b", zin, re.I):
                    if is_uitgelegd(zin, term):
                        continue
                    uit.append(("D3", pos, re.sub(r"\s+", " ", zin)[:120],
                                f"'{term}' — leg uit bij eerste gebruik of vervang"))
                    break
    return uit


# --------------------------------------------------------------------------
# uitvoeren
# --------------------------------------------------------------------------
def controleer(pad: Path, codes: set[str] | None, negeer_klassen: tuple[str, ...],
               blok_extra: tuple[str, ...] = ()) -> list[Melding]:
    rauw = pad.read_text(encoding="utf-8", errors="replace")
    tekst = lees(pad, negeer_klassen, blok_extra)
    ankers = bouw_context(rauw)
    treffers = zoek_patronen(tekst, codes) + meet_dichtheden(tekst, codes) + meet_zinnen(tekst, codes)
    meldingen = [Melding(code, str(pad), regel_van(tekst, pos), context_van(ankers, pos), citaat, uitleg)
                 for code, pos, citaat, uitleg in treffers]
    meldingen.sort(key=lambda m: (m.regel, m.code))
    return meldingen


def verzamel(paden: list[str], recursief: bool) -> list[Path]:
    uit: list[Path] = []
    for p in paden:
        pad = Path(p)
        if pad.is_dir():
            patroon = "**/*" if recursief else "*"
            uit += [q for q in sorted(pad.glob(patroon))
                    if q.suffix.lower() in (".md", ".txt", ".html", ".htm", ".xhtml")]
        else:
            uit.append(pad)
    return uit


def main(argv: list[str] | None = None) -> int:
    a = argparse.ArgumentParser(description="Controleert Nederlandse tekst op AI-taal en leesniveau.")
    a.add_argument("paden", nargs="+")
    a.add_argument("--recursief", action="store_true")
    a.add_argument("--codes", help="alleen deze codes, komma-gescheiden (A1,D1,…)")
    a.add_argument("--negeer-html-klasse", action="append", default=[],
                   help="HTML-element met deze klasse overslaan, bijv. notes")
    a.add_argument("--blok-tag", action="append", default=[],
                   help="deze tag ook als zinsgrens tellen, bijv. span in een dia met losse kaartjes")
    a.add_argument("--json", help="schrijf de bevindingen ook naar dit bestand")
    n = a.parse_args(argv)

    codes = {c.strip().upper() for c in n.codes.split(",")} if n.codes else None
    alles: list[Melding] = []
    for pad in verzamel(n.paden, n.recursief):
        if not pad.exists():
            print(f"niet gevonden: {pad}", file=sys.stderr)
            continue
        alles += controleer(pad, codes, tuple(n.negeer_html_klasse), tuple(n.blok_tag))

    for m in alles:
        plek = f"{m.bestand}:{m.regel}"
        kop = f" [{m.context}]" if m.context else ""
        print(f"{m.code}  {plek}{kop}\n     {m.citaat}\n     → {m.uitleg}")

    tel: dict[str, int] = {}
    for m in alles:
        tel[m.code] = tel.get(m.code, 0) + 1
    samenvatting = " · ".join(f"{c}: {tel[c]}" for c in sorted(tel)) or "niets gevonden"
    print(f"\n{len(alles)} meldingen — {samenvatting}")

    if n.json:
        Path(n.json).write_text(json.dumps([asdict(m) for m in alles], ensure_ascii=False, indent=2),
                                encoding="utf-8")
        print(f"geschreven: {n.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
