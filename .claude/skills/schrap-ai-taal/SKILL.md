---
name: schrap-ai-taal
description: Use when Dutch text may read as machine-written and must sound human before it reaches readers — slides, course material, reports, web copy, mail. Triggers include "klinkt als ChatGPT", "dit is AI-speak", "haal de AI-taal eruit", "te glad geschreven", a "niet X, maar Y" construction, or text aimed at a specific audience such as first-year students.
---

# AI-taal herkennen en wegschrijven

*Voor Engelse tekst: [`strip-ai-language`](../strip-ai-language/SKILL.md). De codes A1 t/m A15 zijn in beide
dezelfde; A16 en A17 bestaan alleen daar, omdat ze Engelse vormen zijn.*

## De kernregel

**Een gladde zin die je niets nieuws vertelt, is een lege zin.** AI-taal valt niet op door fouten maar door vorm: tegenstellingen die diepgang nabootsen, sterke woorden zonder bewijs, en een ritme waarin elke zin even lang is. De lezer voelt vaart en houdt niets over.

## Waarom een gewone redactieronde dit mist

Gemeten op een hoorcollegedeck: een redacteur zonder deze skill vond 40 punten — spelfouten, jargon, inconsistenties — en liet de AI-taal staan. De aangewezen zin *"valt er één weg, dan is het er geen"* werd herschreven tot *"valt er één weg, dan is er geen organisatie meer"*: nettere grammatica, dezelfde constructie. In hetzelfde voorstel kwamen er twee nieuwe bij (*"investeren niet alleen in technologie, maar ook in mensen"*).

Dat is de valkuil van deze faalvorm: **wie hem niet als vorm herkent, herschrijft hem in zichzelf.** Vandaar het recept hieronder, en niet alleen een verbod.

## Werkwijze

1. **Draai het script.** Het wijst aan wat een regel kan aanwijzen.

   ```bash
   python3 scripts/aitaal.py tekst.md
   python3 scripts/aitaal.py deck.html --negeer-html-klasse notes --blok-tag span
   # notes = spreektekst overslaan; blok-tag = losse kaartjes niet als één lange zin tellen
   python3 scripts/aitaal.py map/ --recursief --codes A1,A2 --json bevindingen.json
   ```

2. **Weeg elke melding.** Een melding is een aanwijzing, geen vonnis — zie de precisiekolom.
3. **Herschrijf met het recept**, niet op gevoel. Anders komt de constructie terug.
4. **Lees `patronen.md`** voor de vormen die geen regel kan vinden (A13 t/m A15).
5. **Herdraai het script.** Een herschrijving die een nieuwe melding oplevert is geen herschrijving.

## Het recept voor de tegenstelling (A1)

De vaakst gevonden vorm, en de enige met een vaste oplossing:

1. **Schrap de ontkende helft.** Blijft er een zin over die klopt? Klaar.
2. **Klopt hij niet meer?** Dan droeg de ontkenning informatie. Zet die in een eigen zin, met de partij erbij die het denkt: *"Veel mensen denken X. In werkelijkheid Y, want Z."*
3. **Gaat het om een grens?** Vervang de negatie door een voorbeeld dat de grens laat zien.

| Voor | Na | Wat er gebeurde |
|---|---|---|
| Een organisatie rust op vier kenmerken — valt er één weg, dan is het er geen | Elke organisatie heeft deze vier kenmerken. Een volle wachtkamer heeft er maar één: mensen | negatie vervangen door een voorbeeld |
| Succes gaat niet alleen over geld, maar ook over mensen en kennis | Succes gaat over geld, mensen en kennis | ontkende helft geschrapt |
| Het is geen technologievraag, maar een organisatievraag | De directie vraagt naar techniek. Het antwoord gaat over wie wat mag beslissen | misverstand met eigenaar, dan het antwoord |

## Wanneer hij blijft staan

Niet elke tegenstelling is hol. Hij is functioneel als hij alle drie deze vragen doorstaat:

1. **Staat de ontkende kant ergens op de pagina?** Heeft de lezer hem net zelf opgeschreven, gezegd of gelezen, dan wijst de ontkenning iets af dat er werkelijk ligt.
2. **Kost schrappen informatie?** Haal de ontkende helft weg. Verandert de betekenis, dan droeg hij iets.
3. **Is het een tegenstelling of een uitbreiding?** *"Niet alleen X, maar ook Y"* betekent gewoon X én Y — een opsomming in vermomming, en die gaat weg.

Het gemeten voorbeeld: op een dia waar studenten net drie technische antwoorden gaven — *"koop een AI-tool"*, *"huur een data scientist"*, *"bouw een chatbot"* — sluit de dia af met **"dit is een ontwerpvraag over een organisatie, niet over software"**. Die ontkenning heeft een eigenaar in beeld, verdwijnt niet zonder betekenisverlies, en is geen verkapte opsomming. Hij blijft staan.

Het verschil met de holle vorm zit dus niet in de woorden maar in wat eromheen staat. Dezelfde zin op een dia zonder die drie kaarten bestrijdt een stroman.

**Vierde vraag, voor de slotzin met een beeld erin.** Staat er op de plek van *Y* een metafoor — *"dan heb je geen cultuur maar een dashboard"* — dan moet de lezer twee sprongen maken: eerst het beeld ontcijferen, dan de conclusie trekken. Zelfs een schrijver die zijn eigen zin terugleest, moet er soms even over nadenken; een eerstejaars doet dat niet en leest eroverheen. Vervang het beeld door het mechanisme dat het beeld bedoelde: *"…ziet elke overtreding gebeuren en voorkomt er geen enkele."*

## Wat het script vindt

| Code | Faalvorm | Precisie |
|---|---|---|
| A1 | Tegenstelling: "niet X, maar Y", "zonder X geen Y", "minder X, meer Y" | hoog |
| A2 | Sterk woord zonder bewijs: cruciaal, baanbrekend, krachtig | goed — soms terecht in een citaat |
| A3 | Opwarmer: "in de snel veranderende wereld van", "het is belangrijk om te beseffen" | hoog |
| A4 | Containerbegrip: landschap, ecosysteem, speelveld, de wereld van | matig — *ecosysteem* is in biologie en IT een vakterm |
| A5 | Modewoord: duiken in, naadloos, handvatten, ontgrendelen | goed |
| A6 | Omweg om "is" te vermijden: vormt de basis, fungeert als, staat voor | matig — *vormt* is soms gewoon het juiste werkwoord |
| A7 | Slot dat niets besluit: "de tijd zal het leren", "hoe dan ook" | hoog |
| A8 | Toekomstbelofte: "verandert de manier waarop", "brengt ons dichter bij" | hoog |
| A9 | Beleefdheidsformule: "goede vraag", "je hebt helemaal gelijk" | hoog |
| A10 | Gedachtestreepdichtheid boven 1,2 per 100 woorden | goed, maar het is een norm en geen fout |
| A11 | Metronoomritme: alle zinnen even lang (spreiding onder 0,38) | goed vanaf acht zinnen |
| A12 | Drieslagdichtheid: "X, Y en Z" boven 1,5 per 100 woorden | matig — een opsomming van drie is vaak gewoon waar |
| D1 | Zin boven 20 woorden | hoog; drempel hangt aan de lezer |
| D2 | Abstractiedichtheid: naamwoorden op -ing, -heid, -iteit, -isatie | matig |
| D3 | Onuitgelegd jargon uit een vaste lijst | goed — uitleg tussen haakjes, na een dubbele punt of in een eigennaam telt als uitgelegd |

Gemeten op een deck van 32 dia's: 18 meldingen op de dia-tekst. Na de redactie bleven er
zeven staan, alle zeven bewuste keuzes: twee directiecitaten, een parafrase van Deming,
twee vaktermen die de dia zelf invoert, en de gedachtestreepdichtheid als huisstijl.
Op een schoon geschreven controletekst: nul meldingen.

## Wat het script niet vindt

**Een tegenstelling zonder signaalwoord.** *"Techniek verandert. Organiseren blijft."* Zelfde vorm, geen "maar".

**Een sterk woord dat wél bewijs heeft.** A2 meldt *cruciaal* ook als er twee regels lager een cijfer staat. Lezen blijft nodig.

**Holle inhoud in correcte zinnen.** Een alinea die drie keer hetzelfde zegt in wisselende bewoordingen haalt geen enkele code. Daarvoor is `redigeer-nederlandse-tekst` er, faalvorm F2.

Drie vormen die alleen een lezer ziet, staan in `patronen.md`: elegante variatie (A13), valse concreetheid (A14) en het opgeblazen lijstje (A15).

## Taal op maat van de lezer

De D-codes stellen zich in op wie het leest. Voor eerstejaars die een vak voor het eerst zien:

- **D1 op 20 woorden.** Voor professionals mag 25.
- **Elk vakwoord krijgt zijn uitleg in dezelfde zin**, niet in een voetnoot: *"poka-yoke — Japans voor: fouten onmogelijk maken"*.
- **Een Engelse afkorting die één keer valt, mag weg.** Valt hij vaker, dan hoort er een Nederlandse omschrijving bij de eerste vermelding.
- **Praat tegen de lezer, niet over hem.** *"Drie begrippen die studenten door elkaar halen"* wordt *"drie begrippen die je makkelijk door elkaar haalt"*.

Pas de drempels aan in de kop van `scripts/aitaal.py` (`ZIN_MAX_WOORDEN`, `ABSTRACT_PER_100`) en vul `JARGON` aan met de termen van het vakgebied.

## Veelgemaakte fouten

| Fout | Waarom het misgaat |
|---|---|
| De tegenstelling gladstrijken in plaats van schrappen | de constructie overleeft de herschrijving — dit is de gemeten baseline |
| Élke tegenstelling schrappen | een ontkenning die een misverstand afwijst dat op dezelfde pagina staat, is informatie — zie *Wanneer hij blijft staan* |
| Alle meldingen wegwerken | A4, A6 en A12 hebben matige precisie; een vakterm hoeft niet weg |
| Citaten meeredigeren | een uitspraak van Deming of een directie houdt zijn eigen woorden |
| Alleen het script draaien | de drie ernstigste vormen staan in `patronen.md` en vragen dat je leest |
| Elke lange zin knippen | afwisseling is het doel; alleen korte zinnen levert A11 op |
| De drempels laten staan | 20 woorden is voor eerstejaars; stel ze in op je lezer |
| Vergeten wat de redactie elders raakt | een kop die korter wordt, levert minder grote letters op — controleer normen voor lettergrootte of dianorm ná de redactie |
