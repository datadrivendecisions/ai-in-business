# Samenwerken aan deze repo

*This repository is in English. This page is not: it is the one page you must understand
at the moment something goes wrong. The working agreement itself lives in `CLAUDE.md` and
[`work/README.md`](work/README.md).*

Witek en Meike werken allebei aan de cursus. Deze pagina zegt hoe dat gaat zonder dat
iemand per ongeluk iets publiceert.

## Eerst dit: main publiceert

Alles wat in `site/` op `main` terechtkomt, staat binnen een minuut live op
https://datadrivendecisions.github.io/ai-in-business/. Dat is openbaar, ook voor studenten
die nog niet zover zijn. Daarom kun je niet rechtstreeks naar `main` pushen. GitHub weigert
dat; je hebt altijd een pull request nodig.

Dat is geen wantrouwen, het is een pauzeknop. Tussen „ik ben klaar" en „het staat er
voor iedereen" zit één stap waarin je nog kunt kijken.

## Elke keer dat je begint

1. **Haal op wat de ander heeft gedaan.** In VSCode linksonder op het rondje met de
   pijltjes, of ⌃⇧P → „Git: Pull". Doe dit vóórdat je iets aanpast.
2. **Maak een eigen tak.** Linksonder staat de naam van de tak waar je in zit, meestal
   `main`. Klik erop, kies „Create new branch...", en geef hem een naam die zegt waar je
   aan werkt: `week-03-opdracht`.

Werk je met Claude Code, dan volstaat één zin: *„haal eerst op wat er is en zet me op een
eigen tak"*.

## Elke keer dat je klaar bent

Push je tak en open een pull request. GitHub zet daar zelf een knop voor neer zodra je
tak binnen is. Tegen Claude Code: *„push mijn tak en open een pull request"*.

Op die pull request draait automatisch een controle: **Check every link in de repo**.
Die kijkt of alle verwijzingen nog ergens naartoe wijzen. Staat er een groen vinkje, dan
kun je zelf op „Merge" drukken — je hoeft niet op Witek te wachten. Staat er een rood
kruisje, dan is er een link kapot; klik erop om te zien welke.

## Waar je wat zet

| Map | Wat het is |
|---|---|
| `site/` | De cursussite. Staat live zodra het op `main` staat. |
| `work/drafts/` | Waar je iets uitwerkt dat nog niet af is. Komt niet op de site. |
| `work/decisions/` | Waarom de cursus is zoals hij is. Blijft staan, wordt nooit gepubliceerd. |

Werk je aan iets nieuws, begin dan in `work/drafts/`. Als het af is verhuist het naar
`site/`. Die route staat in [`work/README.md`](work/README.md).

Let op: de repo is **openbaar**. `work/` houdt drafts van de site af; op GitHub zelf kan
iedereen ze gewoon lezen. Wat echt niet openbaar mag, hoort hier helemaal niet.

## Als er iets misgaat

| Wat je ziet | Wat het betekent | Wat je doet |
|---|---|---|
| `GH013: Repository rule violations found` en „Changes must be made through a pull request" | Je stond nog op `main` | Maak een tak en push opnieuw. Je werk is niet weg. |
| „Required status check … is expected" in diezelfde melding | Hetzelfde: zonder pull request draait die controle nooit | Idem — een tak en een pull request, dan draait hij vanzelf |
| Rood kruisje op je pull request | Er is een link kapot | Klik op het kruisje; er staat welke. Repareer hem en push opnieuw. |
| VSCode meldt „merge conflict" | Jullie hebben allebei dezelfde plek aangepast | Zeg tegen Claude: *„los dit conflict op en laat me kiezen"*. Zie hieronder. |
| `<<<<<<<` en `>>>>>>>` in een bestand | Hetzelfde, maar dan al zichtbaar in de tekst | Niets weghalen. Zelfde zin tegen Claude; die ruimt de tekens op. |

Bij twijfel: niets forceren. Er gaat in git bijna nooit iets echt verloren, behalve als
iemand met veel overtuiging iets forceert.

## Tegelijk in hetzelfde document

Jullie werken elke week aan dezelfde documenten. Conflicten hóren daarbij; ze betekenen
niet dat er iets stuk is. Ze betekenen dat jullie allebei dezelfde alinea hebben aangeraakt
en dat git niet kan weten wie gelijk heeft.

**De techniek is niet aan jou; de inhoudelijke keuze wel.** Zeg tegen Claude Code:
*„los dit conflict op en laat me kiezen"*. Je krijgt dan een vraag terug, geen git:

> Op deze plek staan twee versies van dezelfde zin.
> Witek schreef: „…"
> Jij schreef: „…"
> Welke houden we — of zetten we ze achter elkaar?

Die vraag kun jij beantwoorden en Claude niet; met de tekens en de commit eromheen is het
andersom. Soms kun je niet overzien wat goed is: twee tabellen die elkaar tegenspreken,
of iets in `.github/`. Stuur dat door naar Witek.

## Wat conflicten klein houdt

Afspreken wie welk bestand bezit heeft hier geen zin; jullie zitten overal samen aan. Wat
wel helpt is de tijd verkorten dat jullie tegelijk in dezelfde tekst zitten.

- **Zeg even waar je bezig bent** voordat je begint. Eén berichtje.
- **Houd een tak kort.** Liefst samengevoegd in dezelfde zitting. De kans op een conflict
  groeit met de tijd dat je tak los staat, niet met de hoeveelheid werk erin.
- **Gebruik de knop „Update branch"** op je pull request zodra hij verschijnt. Die haalt het
  werk van de ander in jouw tak. Zo krijg je drie kleine conflicten verspreid over de week
  in plaats van één grote op vrijdag.
- **Zet „Auto-merge" aan** als je klaar bent maar de controle nog draait. Dan gaat hij vanzelf
  samen zodra het vinkje groen is, en staat je werk niet onnodig open.
