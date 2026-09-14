# Build — everything written to build the system

The documents behind the things this repository builds, kept in one place so that a PRD, its
blueprint, its build plan and the log of building it are never more than one folder apart. Course
content — the pages, the assignments, the criteria — lives elsewhere; this folder is about the
machinery.

| Folder | What it builds | Files |
|---|---|---|
| [`socratic-workflow/`](socratic-workflow/) | The Socratic gate and the document hand-in pipeline | [`prd.md`](socratic-workflow/prd.md) · [`design-note.md`](socratic-workflow/design-note.md) · [`blueprint.html`](socratic-workflow/blueprint.html) · [`buildplan.html`](socratic-workflow/buildplan.html) · [`agent-config.md`](socratic-workflow/agent-config.md) · [`pipeline-log.md`](socratic-workflow/pipeline-log.md) |
| [`course-site/`](course-site/) | The course website | [`prd.md`](course-site/prd.md) · [`journeys.md`](course-site/journeys.md) · [`scorecard.md`](course-site/scorecard.md) |
| [`information-seeking-experiment/`](information-seeking-experiment/) | The browser tool that runs the week 3 experiment on biased information seeking | [`prd.html`](information-seeking-experiment/prd.html) · [`blueprint.html`](information-seeking-experiment/blueprint.html) · [`buildplan.html`](information-seeking-experiment/buildplan.html) |

The code these describe stays beside the fixtures it is tested against:
[`../socratic_agent/`](../socratic_agent/) and [`../test-fixtures/`](../test-fixtures/).

**Not for `site/`.** The Socratic workflow's PRD carries the design of a rubric, and its agent
config carries the rubric itself, which is tier-1 instructor material under the publication rule
in `CLAUDE.md`. The blueprint and the build plan are written as worked examples of the documents
teams hand in and may one day be promoted to the site; until then they are read from here, and
their links to the site are absolute so they work from any folder.
