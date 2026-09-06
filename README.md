# AI for SMEs — Handbook

The course site for two HAN modules that share one team and one deliverable: a living handbook
helping regional manufacturing SMEs put AI to work.

**Site:** https://datadrivendecisions.github.io/ai-in-business/ · **Handbook template:** https://datadrivendecisions.github.io/ai-in-business/handbook.html

The course is published to students as **AI in Business**.

The modules are **AIBS** (AI in Business & Society, the research track) and **AEL** (Agent
Engineering Lab, the technical track). The repository and its URL were moved off the `diaia` slug
the project started with, so that the address says what the course is; links to the old
`.../diaia/` URL no longer resolve.

## Repo layout

| | |
|---|---|
| [`site/`](site/) | **Published.** Everything here goes live on GitHub Pages. |
| [`work/`](work/) | **Not published.** Drafts on their way to the site, and the decisions behind the module. |
| [`project-documentation/`](project-documentation/) | **Not published.** Internal project documents, tracked in git. |

### `site/` — the course site
- [`site/index.html`](site/index.html) — the landing page for **AI in Business**, the combined AIBS / AEL course, written for students: why the course matters, how it is structured and assessed, what is fixed versus decided week by week, and the provisional week map
- [`site/week-01.html`](site/week-01.html) — week 1: the pre-reading, the first joint session, and both week-1 assignments in full. One page per teaching week, published about a week before its session; copy this file for the next one and add its link to the week map
- [`site/handbook.html`](site/handbook.html) — the handbook's **template**: the shell every cohort fills (start here, the theme index, the chapter anatomy, tooling, ecosystem, quality bar and disclaimer). The programme design the handbook page used to carry — mission, curriculum, seven themes with readings, partners, roadmap — is superseded by the LRD and lives only in git history; the handbook's own requirements come from the PRD each team writes in AEL
- [`site/integrated-lrd.html`](site/integrated-lrd.html) — the integrated learning-requirements document for AIBS and AEL, published at https://datadrivendecisions.github.io/ai-in-business/integrated-lrd.html so it can be shared by link; its Appendix A records the module as it runs today. Written for the module owners, not for students; the landing page links it under that heading, and the handbook does not link it at all.

### `project-documentation/` — internal
- `module-redesign-sketches.md` — three paired sketches for splitting the current module into a business/society module and a technical sister module
- `Voorstel Handbook DIAIA .pdf` — the original proposal
- [`project-documentation/lrd-logbook.md`](project-documentation/lrd-logbook.md) — what changed in the LRD and why, per version. The LRD itself carries only a version number and date.

These are in the repo but not on the site. The LRD refers to them, and to the decision
records, by their GitHub URLs, so those links work from the published page.

### `work/` — where we think
- [`work/drafts/`](work/drafts/) — ideas being worked out, not yet fit for students. Transient: each draft is promoted to `site/` or abandoned.
- [`work/decisions/`](work/decisions/) — the design decisions behind the module, as numbered ADRs. Permanent, and never promoted. An accepted record stops changing: you supersede it rather than edit it.

See [`work/README.md`](work/README.md) for the working agreement.

## Publishing

Publishing is automated — see [`.github/workflows/pages.yml`](.github/workflows/pages.yml).

- **Push to `main`** touching `site/` → links are checked, then the site deploys.
- **Open a PR** touching `site/` → links are checked and the built site is attached to the run as a `site-preview` artifact you can download and open locally. Nothing goes live.

Nothing outside `site/` is ever uploaded to Pages.

## Checks

Three workflows, none of which needs a build step or a dependency. Run any of them yourself.

| | |
|---|---|
| [`pages.yml`](.github/workflows/pages.yml) | `site/` changed → link check, then deploy |
| [`links.yml`](.github/workflows/links.yml) | `README.md`, `CLAUDE.md` or `work/` changed → link check, no deploy |
| [`decisions.yml`](.github/workflows/decisions.yml) | `work/decisions/` changed → decision records checked, no deploy |

```bash
./.github/scripts/check-links.sh   # links
./.github/scripts/check-adrs.sh    # decision records
```

[`check-links.sh`](.github/scripts/check-links.sh) enforces two rules. Inside `site/`, every
relative link must resolve **inside `site/`** — a link that escapes, `../` included, fails the
build, because nothing outside `site/` is uploaded and the link would 404. That is what stops a
half-finished draft from being linked into the public handbook. Everywhere else — this file,
`CLAUDE.md`, `work/` — a relative link must simply point at something that exists, so the repo's
own description of itself cannot quietly rot.

Both `pages.yml` and `links.yml` run the whole script, so either can fail on either rule — a
broken link in `site/` will fail the `links.yml` run too. That is deliberate: one script that
always checks everything is harder to slip past than two that each check half.

[`check-adrs.sh`](.github/scripts/check-adrs.sh) checks that the decision records are numbered,
structured and cross-referenced, and refuses a change to a record that was already accepted.

*Educational, not consultancy.*
