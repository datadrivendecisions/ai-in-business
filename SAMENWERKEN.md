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
| VSCode meldt „merge conflict" | Jullie zaten in hetzelfde bestand | Stop, en laat het Witek weten. Niet zelf uitproberen. |
| `<<<<<<<` en `>>>>>>>` in een bestand | Hetzelfde, maar dan al in het bestand | Sla niets op, en stuur een berichtje. |

Bij twijfel: niets forceren. Er gaat in git bijna nooit iets echt verloren, behalve als
iemand met veel overtuiging iets forceert.

## Uit elkaar blijven

Het conflictrisico is hier klein, want elke week heeft zijn eigen bestand
(`site/week-01.html`, `site/week-02.html`, …). Spreek af wie welke week doet, dan komen
jullie elkaar bijna nooit tegen. Twee pagina's deelt iedereen: `site/index.html` en `CLAUDE.md`.
Meld het even voordat je daarin gaat zitten.

En houd een tak kort. Liefst dezelfde dag samengevoegd. Hoe langer je tak los staat, hoe
verder de cursus onder je vandaan schuift.
