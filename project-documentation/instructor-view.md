# The instructor view

The course site has one audience by default — students — and one narrow way to publish something
for the teaching team instead: a section marked as instructor material, hidden unless the address
carries `?instructor`.

## Using it

**<https://datadrivendecisions.github.io/ai-in-business/index.html?instructor>**

That reveals every instructor section on the landing page. The choice is remembered in
`sessionStorage` for the rest of the visit, so you can move around the site normally and it stays
on. It goes off when you close the tab, or immediately if you add `?student` to any address that
carries the toggle.

A revealed section says so at the top, in a line that also offers the way back out. That line
matters when you are presenting to the room: it is the difference between knowing you are in the
instructor view and finding out from a student.

**Pages that carry the toggle today:**

| Page | Instructor sections |
|---|---|
| `site/index.html` | *For the module owners* — the link to the LRD |

A page gains the toggle when it gains something to hide, not before. Everything else on the site
ignores `?instructor` entirely.

## What it is not

It is **signposting, not access control.** The section is in the HTML whether or not the parameter
is there; the page is served from a public URL, built from a public repository, and view-source
defeats the whole mechanism in one click. It keeps instructor material out of a student's *way*. It
does not keep it out of their *reach*, and it never will.

So the site runs on a two-tier rule, and only the first tier protects anything:

1. **Some instructor material is not in `site/` at all.** Anything whose worth depends on a student
   not having read it — the reveal at the end of an exercise, a manipulation that is deliberately
   withheld, the Socratic tutor's hidden rubric and scores, question banks, answer keys, the
   *ask, never comment* prompts a lecturer works from — lives in `project-documentation/` or
   `work/`. Those are off the site. (They are still in a public repo: off the site is not secret.
   Anything that genuinely cannot be public is not committed anywhere.)
2. **The rest may be published behind the instructor view.** Run sheets, prep checklists, the design
   in its ideal form, the pointers a lecturer needs and a student does not — material that is merely
   *not for students* rather than damaging in their hands.

Building the view was not a licence to publish tier 1. When in doubt about which tier something is
in, ask what the teaching loses if a student reads it the week before the session. If the answer is
"the session", it is tier 1.

## Adding an instructor section to a page

1. Mark the section: `<section id="…" data-audience="instructor" hidden>`. Use the `hidden`
   attribute rather than a CSS rule, so the content stays out of the accessibility tree, out of
   in-page search and out of print.
2. Open it with a line that says the view is on and links back to `?student` — copy the one in
   `site/index.html`, which uses the existing `.aside` component and needs no new CSS.
3. If the page does not already have it, copy the toggle script verbatim from the foot of
   `site/index.html`. It is the site's one agreed exception to *no JavaScript on a course page*;
   add nothing to it.
4. Check that nothing outside the section still points into it — a nav link or a table-of-contents
   entry to a hidden section is a dead link for every student who clicks it.
5. Run `./.github/scripts/check-links.sh`. Query strings are stripped before the check, so
   `index.html?student` resolves as `index.html`.

## Known gaps

- **`site/integrated-lrd.html` is not behind the view.** The path to it from the landing page is
  gated; the document itself is open at its own URL to anyone with the link, and it carries at least
  one tier-1 item — the Socratic tutor's hidden rubric, which FR-03 and §6.4 describe in full while
  specifying that teams never see it. It also names both module owners, which the decision records
  deliberately never do. See [issue #3](https://github.com/datadrivendecisions/ai-in-business/issues/3).
- **Week 2's lecturer material has no home yet.** The trust-cards exercise turns on a withheld
  manipulation and ends in a scripted reveal — tier 1 throughout, so it stays in
  `project-documentation/`. See [issue #2](https://github.com/datadrivendecisions/ai-in-business/issues/2).
