"""Tests bij aitaal.py — elke code moet zijn eigen faalvorm vinden, en een
schoon geschreven tekst mag niets opleveren."""

from pathlib import Path

import pytest

import aitaal


def codes(tekst: str, **kw) -> list[str]:
    """Draait de controle op een stuk tekst in een tijdelijk .md-bestand."""
    pad = kw.pop("pad")
    pad.write_text(tekst, encoding="utf-8")
    return [m.code for m in aitaal.controleer(pad, None, ())]


@pytest.fixture
def md(tmp_path) -> Path:
    return tmp_path / "tekst.md"


# --------------------------------------------------------------------------
# de patronen
# --------------------------------------------------------------------------
@pytest.mark.parametrize("code,zin", [
    ("A1", "Dit is geen kostenvraag, maar een organisatievraag."),
    ("A1", "Zonder vertrouwen is er geen samenwerking."),
    ("A1", "Het gaat niet om de techniek."),
    ("A1", "Een organisatie rust op vier kenmerken; valt er één weg, dan is het er geen."),
    ("A2", "Dit is een cruciale stap in het proces."),
    ("A2", "Een baanbrekende aanpak van het probleem."),
    ("A3", "In de snel veranderende wereld van vandaag telt snelheid."),
    ("A3", "Het is belangrijk om te beseffen dat cijfers liegen."),
    ("A4", "Het landschap van de zorg verandert."),
    ("A4", "Binnen dit ecosysteem werken partijen samen."),
    ("A5", "We duiken in de cijfers van vorig jaar."),
    ("A5", "Dat verloopt naadloos."),
    ("A6", "De begroting vormt de basis voor het plan."),
    ("A6", "De manager fungeert als schakel."),
    ("A7", "De tijd zal het leren."),
    ("A7", "Er is nog ruimte voor verbetering."),
    ("A8", "Deze aanpak verandert de manier waarop we werken."),
    ("A8", "Dat brengt ons dichter bij een oplossing."),
    ("A9", "Goede vraag! Het antwoord staat hieronder."),
])
def test_patroon_wordt_gevonden(code, zin, md):
    assert code in codes(zin, pad=md), f"{code} niet gevonden in: {zin}"


def test_schone_tekst_blijft_stil(md):
    """Vakinhoudelijke, concrete tekst mag geen enkele melding opleveren."""
    tekst = (
        "De directie vroeg om een team van agents dat zelf diensten bedenkt.\n"
        "Wij bouwden er vier. Na drie weken stond de eerste dienst online.\n"
        "Twee mensen keken elke dag mee. Zij tekenden voor elke publicatie.\n"
        "De kosten bleven onder het budget van 40.000 euro. Dat was afgesproken.\n"
    )
    assert codes(tekst, pad=md) == []


# --------------------------------------------------------------------------
# dichtheden en ritme
# --------------------------------------------------------------------------
def test_gedachtestreepdichtheid(md):
    zin = "De keuze — en dat is het punt — ligt bij de directie. "
    assert "A10" in codes(zin * 6, pad=md)


def test_metronoomritme(md):
    """Tien zinnen van vrijwel gelijke lengte."""
    tekst = " ".join(f"De manager van afdeling {i} besloot het plan volgende week te bespreken."
                     for i in range(10))
    assert "A11" in codes(tekst, pad=md)


def test_wisselend_ritme_blijft_stil(md):
    tekst = ("Dat kon niet. De directie had drie weken eerder al besloten dat het team "
             "van vier mensen de nieuwe dienst zelf zou bouwen, met een budget dat door "
             "de raad was goedgekeurd. Toch ging het mis. Waarom? Niemand had de "
             "leverancier gebeld. Dat kostte acht dagen.")
    assert "A11" not in codes(tekst, pad=md)


def test_lange_zin(md):
    zin = "De manager " + "van de afdeling die het plan schreef " * 4 + "besloot iets."
    assert "D1" in codes(zin, pad=md)


def test_jargon_zonder_uitleg(md):
    assert "D3" in codes("De stakeholders zijn het eens.", pad=md)


# --------------------------------------------------------------------------
# HTML: opmaak weg, posities heel
# --------------------------------------------------------------------------
def test_html_behoudt_lengte_en_regels():
    bron = '<p class="lead">Zonder <b>plan</b> is er geen&nbsp;richting.</p>\n<p>Tweede regel.</p>'
    plat = aitaal.ontdoe_html(bron)
    assert len(plat) == len(bron)
    assert plat.count("\n") == bron.count("\n")
    assert "Zonder plan is er geen" in " ".join(plat.split())


def test_html_melding_wijst_naar_de_juiste_regel(tmp_path):
    pad = tmp_path / "deck.html"
    pad.write_text('<html>\n<body>\n<h2>Zonder plan is er geen richting</h2>\n</body>\n</html>',
                   encoding="utf-8")
    meldingen = aitaal.controleer(pad, {"A1"}, ())
    assert [m.regel for m in meldingen] == [3]


def test_negeer_html_klasse(tmp_path):
    pad = tmp_path / "deck.html"
    pad.write_text('<section data-title="Dia">\n<p>Alles goed hier.</p>\n'
                   '<div class="notes"><p>Zonder plan is er geen richting.</p></div>\n</section>',
                   encoding="utf-8")
    assert aitaal.controleer(pad, {"A1"}, ()) != []
    assert aitaal.controleer(pad, {"A1"}, ("notes",)) == []


def test_context_komt_uit_data_title(tmp_path):
    pad = tmp_path / "deck.html"
    pad.write_text('<section data-title="Wat is een organisatie">\n'
                   '<h2>Zonder plan is er geen richting</h2>\n</section>', encoding="utf-8")
    assert aitaal.controleer(pad, {"A1"}, ())[0].context == "Wat is een organisatie"


# --------------------------------------------------------------------------
# zinssplitsing
# --------------------------------------------------------------------------
def test_afkorting_breekt_de_zin_niet():
    zn = aitaal.zinnen("De cijfers, bijv. de omzet, staan in bijlage A. Daarna volgt de toelichting.")
    assert len(zn) == 2


def test_codefilter_werkt(md):
    md.write_text("Dit is geen vraag, maar een cruciale keuze.", encoding="utf-8")
    assert {m.code for m in aitaal.controleer(md, {"A1"}, ())} == {"A1"}


def test_blokelementen_scheiden_zinnen():
    """Twee alinea's zonder punt zijn twee zinnen, geen zin van tien woorden."""
    plat = aitaal.ontdoe_html("<p>Structuur wie mag wat</p><p>Systemen waar zit de rem</p>")
    assert len(plat) == len("<p>Structuur wie mag wat</p><p>Systemen waar zit de rem</p>")
    assert len(aitaal.zinnen(plat)) == 2


def test_lange_dia_zonder_punten_geeft_geen_valse_melding(tmp_path):
    pad = tmp_path / "deck.html"
    pad.write_text("<section data-title=\"Dia\">" + "".join(
        f"<p>Kaartje {i} met vier woorden</p>" for i in range(8)) + "</section>", encoding="utf-8")
    assert [m for m in aitaal.controleer(pad, {"D1"}, ())] == []


def test_extra_bloktag_scheidt_zinnen(tmp_path):
    """Losse keuzeknoppen in <span> zijn geen zin van dertig woorden."""
    pad = tmp_path / "deck.html"
    pad.write_text("<p>" + "".join(
        f"<span>Antwoord {i} met een stuk of zeven woorden erin</span>" for i in range(4)) + "</p>",
        encoding="utf-8")
    assert aitaal.controleer(pad, {"D1"}, ()) != []
    assert aitaal.controleer(pad, {"D1"}, (), ("span",)) == []


@pytest.mark.parametrize("zin", [
    "Dashboards en prestatiecijfers (KPI's).",
    "Agile: werken in korte rondes.",
    "Die keuze ís jouw governance: wie waarover beslist.",
    "Het Integrated Reporting Framework noemt zes soorten kapitaal.",
])
def test_uitgelegd_jargon_blijft_stil(zin, md):
    assert "D3" not in codes(zin, pad=md), zin


@pytest.mark.parametrize("zin", [
    "De stakeholders zijn het eens.",
    "We werken agile.",
    "Dat staat in de roadmap.",
])
def test_kaal_jargon_wordt_gemeld(zin, md):
    assert "D3" in codes(zin, pad=md), zin


def test_functionele_tegenstelling_zonder_signaalwoord(md):
    """Een ontkenning zonder 'maar' vindt het script niet — bewust: of hij hol is,
    hangt af van wat er omheen staat. Zie 'Wanneer hij blijft staan' in SKILL.md."""
    zin = "Dit is een ontwerpvraag over een organisatie, niet over software."
    assert "A1" not in codes(zin, pad=md)


@pytest.mark.parametrize("zin", [
    "Die organisatie heeft geen cultuur maar een dashboard.",
    "Die organisatie heeft geen cultuur, maar een dashboard.",
    "Cultuur is hier geen postertekst maar een ontwerpkeuze per norm.",
])
def test_geen_maar_ook_zonder_komma(zin, md):
    """De komma is optioneel; zonder komma ontsnapte de constructie eerder."""
    assert "A1" in codes(zin, pad=md), zin
