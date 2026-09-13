# Session slides — presenter builds

The student version of every deck is the card page on the site, `site/week-NN-slides.html`:
one card per slide, no JavaScript, readable on a phone. That page is the source of truth for
what is projected. This folder adds what a lecturer needs to present it:

| File | What it is |
|---|---|
| `week-NN-notes.md` | Instructor notes, one `## sN` block per card. The lecturer's words; edit freely. |
| `build_deck.py` | Reads the card page and the notes, writes the three files below. |
| `site/week-NN-deck.html` | Presenter deck, published beside the card page and linked from it. Arrow keys, **F** full screen, **P** print, `#s5` deep links. Add `?instructor` to the address for the notes panel and the **N** key; `?student` turns it off again. |
| `week-NN-deck.pdf` | The deck printed, notes under every slide. |
| `week-NN-deck.pptx` | The same slides in PowerPoint, notes in the notes pane. |

```bash
.venv/bin/python project-documentation/slides/build_deck.py        # both weeks
.venv/bin/python project-documentation/slides/build_deck.py 2      # one week
```

The PDF needs Google Chrome on the machine; the PPTX needs `python-pptx` (installed in the
repository's `.venv`). Rebuild after any change to a card page or a notes file; the outputs
are generated and are never edited by hand.

The deck is on the site and the notes are in it, behind the instructor view — signposting, not access control. Notes here are run-sheet material — what
to say, timings, what to ask — and never the material whose worth depends on a student not
having read it. That stays where the instructor-material rule in `CLAUDE.md` puts it.
