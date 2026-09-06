# Work — not published

Nothing in this folder reaches https://datadrivendecisions.github.io/ai-in-business/.
The publish workflow uploads `site/` and only `site/`.

Note: this repo is **public**, so `work/` is separated from the handbook but still
readable by anyone who browses the repo. It keeps drafts off the site, not out of
sight — anything that genuinely cannot be public should not be committed at all.

## What lives here

Two kinds of thing, with opposite lifecycles.

**`drafts/`** — ideas being worked out that are not yet fit for students. Transient:
each draft is either promoted to `site/` or abandoned, and the folder is empty
whenever nothing is in flight.

**`decisions/`** — the design decisions behind the module, recorded as they are
taken. Permanent, and never promoted: they explain why `site/` looks the way it
does, which is not something the handbook itself should say. An accepted record
stops changing — you supersede it rather than edit it, and
[`check-adrs.sh`](../.github/scripts/check-adrs.sh) enforces that in CI. See
[`decisions/README.md`](decisions/README.md).

## Promoting work to the site

1. Draft here.
2. When it is ready, `git mv` it into `site/` (or fold it into `site/index.html`)
   and add the link from the handbook.
3. Run `./.github/scripts/check-links.sh`, then open a PR. CI re-checks the links
   and attaches a downloadable preview of the site.
4. Merge to `main` → it deploys.

Step 3 is the staging gate: if a page in `site/` still links to something left
behind here, the build fails rather than shipping a dead link.

Decision records are not part of this flow. They stay here for good.
