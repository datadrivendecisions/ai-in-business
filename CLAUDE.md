# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The course site for two HAN modules — AIBS and AEL — that share one team and one deliverable: a
living handbook teaching regional manufacturing SMEs to apply AI. Together the two modules are
published to students as one course, **AI in Business**. It is prose, not software: hand-authored
static HTML pages with inlined CSS, no build step, no dependencies, no package manager, no test
framework. Most "development" here is editing content, and the risk to manage is publishing
something that is not ready rather than shipping a bug.

## The publication boundary

`site/` is published to GitHub Pages. `work/` is not. That split is the organising principle
of the repo — see [`work/README.md`](work/README.md) for the working agreement.

- `site/` — everything here goes live at https://datadrivendecisions.github.io/ai-in-business/
- `work/` — drafts and exploration, staged before they reach the site
- `project-documentation/` — internal documents (the redesign sketches, the original proposal, the LRD logbook)

Only `site/` is published; the other two are in the repo but off the site. The repo is
**public**, so nothing here is hidden — anything that genuinely cannot be public should
not be committed at all.

Promote a draft by `git mv`-ing it from `work/` into `site/` and adding the link from the
handbook — both steps, or the link check fails.

## The decision record

`work/decisions/` holds the design decisions behind the module — why AIBS is shaped the way it
is — as numbered ADRs. Curriculum decisions, not software architecture, but the form fits: a
curriculum is revisited yearly, and the value is that next year's discussion starts from why last
year's choice was made.

The rule that makes them worth keeping: **an accepted record stops changing.** Change your mind by
writing a new record that supersedes the old one and setting the old status to
`Superseded by ADR-NNNN` — the only edit an accepted record may still receive.
`check-adrs.sh` enforces this against the base commit in CI, so it is a gate rather than an
honour system.

Records live under `work/`, so they are off the site but still in a public repo: they name
**roles**, never people, and carry no timetables or personal notes.

## Commands

```bash
./.github/scripts/check-links.sh   # publication gate: every relative link in site/ resolves inside site/
./.github/scripts/check-adrs.sh    # decision records: numbering, structure, status, cross-references
BASE_SHA=HEAD~1 ./.github/scripts/check-adrs.sh   # ...plus: no accepted record was edited
python3 -m http.server -d site     # preview the site locally at :8000
gh run list --workflow=pages.yml   # deploy status

python3 .claude/skills/strip-ai-language/scripts/aiprose.py site/   # prose check: AI language, reading level
```

`check-links.sh` enforces two separate rules. Inside `site/` it is the **publication gate**: every
relative link must resolve *inside* `site/`, and a link that escapes — `../` included — fails the
build, because nothing outside `site/` is uploaded and the link would 404 on Pages. That is exactly
what happens when you link to a draft still sitting in `work/`. Outside `site/` — `README.md`,
`CLAUDE.md`, `work/` — the rule is weaker: a relative link must point at something that exists, so
the repo's own description of itself cannot rot when a file moves. Run it before pushing.

## Deployment

[`.github/workflows/pages.yml`](.github/workflows/pages.yml) uploads `site/` and nothing else. Two
further workflows check things that are never published and therefore never deploy.

| Event | Result |
|---|---|
| Push to `main` touching `site/` | Link check → deploy |
| PR touching `site/` | Link check → downloadable `site-preview` artifact, no deploy |
| Push or PR touching `work/decisions/` | ADR check — [`decisions.yml`](.github/workflows/decisions.yml) — plus the doc link check. Never deploys |
| Push or PR touching `README.md`, `CLAUDE.md` or `work/` | Link check — [`links.yml`](.github/workflows/links.yml). Never deploys |
| Anything else | No run at all |

Pages is configured with `build_type: workflow`, not deploy-from-branch. Do not switch it back:
the legacy branch build serves the repo root, which no longer holds `index.html`, so it would
404 every handbook URL. `actions/configure-pages` does **not** set this by itself when Pages is
already enabled — it was set once via `gh api -X PUT repos/datadrivendecisions/ai-in-business/pages -f build_type=workflow`.

## Content architecture

**`site/index.html` is the course landing page, and its audience is students** of the minor
*Data Driven Decision Making in Business*. It answers, in that order, the three questions a student
arrives with: why this course is worth their attention, how it is structured and assessed, and what
they are working on — globally and week by week. It links the handbook template as the worked
example of the deliverable, and the LRD under a heading that says it is for the module owners.

What it may state as settled comes from [`project-documentation/course-outline.md`](project-documentation/course-outline.md),
which is how the module is *actually* run and whose "What is fixed" list is exactly that promise.
The LRD is the ideal, not the plan: design machinery that lives only in the LRD and rests on a
decision record still marked Proposed — gate-blocked progression, the instructor dashboard, the
seventh week — stays off the student-facing pages. Where the two documents differ, the site
follows the outline and says so.

**`site/week-NN.html` is one page per teaching week**, published about a week before its session,
because the module is run adaptively and later weeks genuinely do not exist yet. Each carries the
week's pre-reading, what happens in the session, the assignments in full, and the hand-in.
Publishing week N is two edits: the new file, and its link in the week map on the landing page
(plus the previous week's pager). Copy `week-01.html` — it is the pattern. Anything still unknown
uses the same `.tpl` placeholder convention as the handbook template, so an unfilled slot reads as
deliberate rather than forgotten.

**`site/handbook.html` is the handbook's template, not the handbook.** It holds the shell every
cohort fills — start here, the theme index, the chapter template, the tooling index, the regional
ecosystem section, and the quality bar with the disclaimer — with placeholders (class `tpl`) where
content goes. The programme design the page used to carry (mission, curriculum, seven themes with
readings, partners, roadmap) is **superseded by the LRD** and lives only in git history; the
handbook's own requirements will come from the PRD each team writes in AEL. Do not put programme
design back on this page — it belongs in the LRD — and do not name people on it.

The repo twice carried a second copy of the handbook page that had to be updated by hand alongside it —
`ai-for-smes-programme.html` (removed in 827f32a) and `ai-for-smes-programme.md` (removed once its
content was confirmed to be fully present in the HTML). Do not reintroduce a parallel Markdown or
HTML version; there is no generator to keep one in sync.

The page is organised as the sections a reader of the finished handbook would see, in reading order.

`site/integrated-lrd.html` is a separate document for the module owners (the
learning-requirements document covering AIBS and its AEL sister module). It is published at
`/integrated-lrd.html` so it can be shared with colleagues by link. The landing page links it from
its "For the module owners" section, which is **instructor-only** (`?instructor`); the handbook does
**not** link it — students are not its audience. The document itself is still open at its URL and
still carries material that should not be in front of students — the Socratic tutor's hidden rubric
above all — which is issue #3. Everything it refers to outside
`site/` (the sketches, the proposal PDF, the decision records) is linked by its GitHub URL, because
a relative link to `project-documentation/` or `work/` would fail the publication gate.

**Instructor material never sits in a student's path.** A page in `site/` is read by students by
default, so anything written for the teaching team is out of place on it. Two rules, and they are
not the same rule:

- **Some instructor material must not be in `site/` at all.** Anything whose worth depends on a
  student not having read it — the reveal at the end of an exercise, a manipulation that is
  deliberately withheld, the Socratic tutor's hidden rubric and scores, question banks, answer
  keys, the lecturer's *ask, never comment* prompts — stays in `project-documentation/` or `work/`.
  `site/` is uploaded to a public URL from a public repo. There is no such thing as a secret in it.
- **The rest may be published behind the instructor view**, marked
  `data-audience="instructor"` and revealed only when the URL carries `?instructor`: run sheets,
  prep checklists, the design in its ideal form — material that is merely *not for students* rather
  than damaging in their hands. The teaching team reaches it by link; a student never meets it
  walking through the page.

The query parameter is **signposting, not access control**. The content is in the HTML either way,
and view-source defeats it in one click — it keeps instructor material out of a student's way, not
out of their reach. The first rule is the one that protects anything.

**Brand system.** Every HTML file carries its own inlined copy of the Business Data Solutions
palette — identical `:root` custom-property blocks, ~24 tokens for colour, type scale, spacing,
shadows and radii. The `stylebook/shared.css` named in the source comment is not in this repo.
A palette change means editing every file; use the tokens rather than hard-coded values.
`index.html` and `week-01.html` share one longer stylesheet (the landing-page and weekly-page
components on top of the same tokens) and must be kept identical to each other.

One palette combination fails WCAG AA: `--text-muted` on `--bg-cream` is 4.26:1. Do not put muted
text on a cream ground — the `.handin` block overrides `.tpl` to `--text-secondary` for exactly
this reason.

**The masthead belongs to the course, not to the supplier.** Every page's `bds-wordmark` reads
*AI in Business* over the HAN minor, links to `index.html`, and carries the BDS lighthouse as a
small unlabelled mark. The company name appears in exactly two places: a one-line `bds-credit` in
every footer, and the colophon at `index.html#colophon` that every one of those lines points at.
The site's own footer says *educational, not consultancy*, and a commercial wordmark above that
sentence undercuts it — the credit is fair, the prominence was not, and prose does the job a logo
cannot. Do not put the company back in the masthead. The SVG keeps `aria-label="Business Data
Solutions"` because that is what the mark depicts; the link's own `aria-label` names the course,
so the accessible name is the course and not the company.

**`site/tool-*.html` are course tools**, listed in the *Course tools* section of the landing page —
things used in a session or needed for an assignment. They are the one deliberate exception to two
rules below, because a tool is not a page of prose:

- **They may carry JavaScript.** A self-assessment that cannot be taken is not a tool. Keep it
  self-contained and dependency-free: no build step, no framework, no network calls. State on the
  landing page's tool card where any answers are stored — the current one keeps them in the
  reader's own browser and sends nothing anywhere, and that is the bar.
- **They carry the brand system like every other page**, including the sticky `bds-nav` and the
  `bds-footer` — copy both from `index.html` rather than writing them again. A tool without the nav
  is a dead end, the same defect `handbook.html` used to have. Light only: the site has no dark
  mode, so a tool arriving with one loses it.

**Re-skinning a tool that encodes meaning in colour.** Where a tool's palette *is* data — an
ordinal ramp, a status scale — rebuild it in BDS terms rather than dropping it. The maturity
scale's six levels are `--l0`…`--l5` with matching `--l0-ink`…`--l5-ink`, a warm neutral ramp from
`--bg-cream-2` to `--supporting`: **monotonic in lightness, every step at or above 4.5:1 against
its own ink.** Keep the token *names* a tool's JavaScript builds colours from — that one does
`var(--l" + level + ")` at runtime, so renaming the tokens breaks it silently. Reserve `--primary`
for the accent that marks the reader's own position; it is never text on a light ground (lime on
white is 1.7:1).

A tool reproduced from elsewhere says so, and links to where it is maintained. Anything it linked
to that is not in `site/` becomes an absolute URL, or the publication gate fails. Drop external
font loads: the site is system-stack only.

No page of the course itself has any JavaScript — not `index.html`, not a week page, not the
handbook template, not the LRD. Keep it that way unless there is a reason not to. The **instructor
view** is the one agreed reason, and it lives at the foot of `index.html`: twenty lines that unhide
the sections marked `data-audience="instructor"` when the URL carries `?instructor`, remember the
choice in `sessionStorage` for the rest of the visit, and let `?student` turn it off again. Copy
that block verbatim into a page when it gains an instructor section, and add nothing to it.

## Conventions

The course, as students meet it, is **AI in Business**. Its two modules are **AIBS** (AI in
Business & Society, the research track) and **AEL** (Agent Engineering Lab, the technical track). The names the project started with survive only in
ADR-0008 and in the proposal PDF and the redesign sketches, which are source
documents — the repository slug and the Pages URL were moved to `ai-in-business` to match the
course. Do not reintroduce them anywhere else, and never in `site/`.

**The LRD does not track its own changes.** It carries a version number and a date, nothing
more. What changed in each version, and why, goes in `project-documentation/lrd-logbook.md`.
Bump the version and add a logbook entry together.

Prose is British-leaning English with em dashes. The handbook positions itself as *educational,
not consultancy* — a framing that recurs in the content and is worth preserving.

**Prose that reads as machine-written is a defect on a student-facing page.** The
[`strip-ai-language`](.claude/skills/strip-ai-language/SKILL.md) skill holds the method and
`scripts/aiprose.py` runs the check. The form to watch here is not vocabulary — a scan of the
five published pages for the usual AI words returns four hits in 24,000 words, all four fair —
it is the **antithesis**: *X, not Y* / *is not X — it is Y* / *rather than*, which appears 173
times, once every eight sentences on the landing page. Keep the ones where the contrast is the
content, as the two gates' *questions back, never a verdict* does; the rest are rhythm pretending
to be thought. The same measurement flags one repeated intensifier per page — *actually*,
*honest*, *quietly* — and the em-dash density, which is house style here and stays.

Commit messages here explain **why**, in full sentences, and reference the commits they respond
to (see 827f32a). Match that.
