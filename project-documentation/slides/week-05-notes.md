# Week 5 — instructor notes

Speaker notes for `site/week-05-slides.html`, one block per card, keyed by the card's id.
`build_deck.py` folds them into the presenter deck. The page holds a placeholder for the AIBS
segment (s2), the AEL segment on the LLM wiki (s3–s5), and the homework card (s6). The wiki
segment has three cards on purpose: the demo on screen is the evidence, the cards only carry
what the voice cannot (the shape, the three sources, the template's address). The folder is public: run-sheet material only.

The template the demo starts from is `datadrivendecisions/llm-wiki-template`. It is a lean,
assistant-neutral version of the schema behind the AI Wiki (`businessdatasolutions/ai-wiki`):
the same three layers, page types and ingest discipline, without Quartz, qmd, retention decay
or quality scoring.

## s1

Session of Monday 5 October. AIBS theme: AI use cases at SMEs. AEL: one way to keep knowledge, built live from an empty folder.

## s2

AIBS segment. To be filled in by the AIBS lecturer before Monday.

## s3

The diagram fills the slide; tell it left to right, then bottom.

- **Start at the bottom row, the comparison.** Query-time RAG: question, search raw, synthesise on the spot, and only the answer remains. That is what most teams built in week 4: it works, and it forgets. Karpathy: the LLM "is rediscovering knowledge from scratch on every question". The wiki row ends differently: artifacts remain, and are reused and improved.
- **Raw sources, top left.** The source of truth. The model reads them and never modifies them.
- **Ingest, the orange box.** Two stages: analysis (entities, concepts, links to what is already in the wiki, contradictions and open questions), then generation (the source summary, entity and concept pages, index and log). This is the step the demo shows.
- **The red boxes are the honest part.** The same source ingested twice will not give identical pages. A summary drops details. A wrong summary stays as markdown and gets built on: error cementing. This is why the template pauses before writing, checks every quotation against the raw file, and keeps a log.
- **LLM wiki, top right.** Plain markdown files a person can read. The review queue (contradictions, duplicates, missing pages) is what the lint reports.
- **Query loop, the purple row.** A question searches the wiki pages and, where needed, the raw sources, fills the context window, and a good answer is saved back to the wiki. Retrieval does not disappear; it gets a better index.

Where the template differs from the diagram: `syntheses/` instead of `queries/`, `AGENTS.md` instead of `schema.md`, no `overview.md`. And "meeting notes" as a raw source is fine for a company, never for our field research: no interview material in the wiki.

All six assistants the students use read `AGENTS.md`; `CLAUDE.md` and `GEMINI.md` in the template point to it. Week 3's visualisation (one question, four ways) is the reminder that this is one of four options.

## s4

The demo. Leave this card up and switch to the terminal and Obsidian.

**Before class (the day before).** Create the demo repository from the template, install the helpers, and acquire and ingest the video and the report. They are too long to run live: in the dry run on 30 September (headless, no pause) the video took 10½ minutes and the report 17. Commit after each. The article stays in `raw/` un-ingested, or is fetched live.

Acquire, one command per format (show at least the article live; the other two take seconds):

- Article: `python3 tools/fetch_article.py https://oecdcogito.blog/2025/09/16/agentic-ai-for-small-business-growth/` — about 1,800 words, word for word.
- Video: `python3 tools/fetch_youtube.py https://www.youtube.com/watch?v=51lXx4wBuHE` — captions only; 64 minutes, about 7,600 words of automatic captions.
- Report: save the PDF in raw/reports/, then `markitdown raw/reports/oecd-empowering-smes-in-the-age-of-ai.pdf > raw/reports/oecd-empowering-smes-in-the-age-of-ai.md` — 36 pages, about 13,000 words, four seconds. The PDF itself is not committed (.gitignore).

**Live: the article.** `/ingest raw/articles/agentic-ai-for-small-business-growth.md — added by Witek`. Let the pause happen and read the takeaways aloud before saying go. On an empty wiki it took just under five minutes; on top of the report and the video expect longer, so budget ten with the pause and talk. Because the survey is already in, the disagreement appears live.

Four things to show:

1. The pause: the place to catch a misreading before it lands on ten pages.
2. The source page's caveats. In the dry run it found that the author heads PayPal's government relations, that PayPal is a partner of the survey the article cites, that the "72%" figure links back to the article itself, and that the two business owners are invented examples.
3. The disagreement. In the dry run it landed on the `agentic-ai` concept page under Debates: the article writes in the present tense about agents that reorder stock and negotiate with suppliers; the OECD survey counts 3.6% of AI users running agentic AI, in a sample it says is not representative and skews to the digitally mature. The page says what the disagreement turns on (partly tense, partly being found by other people's agents versus running your own) and the page's confidence dropped to 0.65.
4. Query and lint. Ask: *Which AI uses pay off first for a small manufacturer, according to the wiki?* Show the citations, then the query entry in the log with the pages it read. Then `/lint`, and dwell on the quote check: every quotation on a wiki page is compared with the raw file, so an invented quotation fails. These are the two habits the knowledge architecture criteria said would come back in week 5.

**Fallback.** The dry-run wiki, all three sources ingested and lint clean (52 pages), is on the lecturer's laptop outside the repositories. Open it in Obsidian if the network or the model fails.

## s5

Teams make their copy now if they did not before the session; the README has the steps. Walk the room: the usual problems are Python on Windows (`python`, not `python3`) and a venv that is not activated. Each team ingests one published source of its own and reads the source page back. Never interview material, private repository or not: what the assistant reads goes to a model service.

Nobody has to switch. A folder with a naming rule, traced end to end, is still a good answer. What the wiki costs: every source is read when it arrives, whether anyone asks or not; a misreading lands on several pages at once; past a few hundred pages the index is not enough and you need search. A team that adopts it writes a decision-log entry and versions its knowledge architecture.

## s6

The first evaluation is held against the PRD's own criteria, and the decision log travels with it. The lookup record and the quotation check are what let a team explain a wrong sentence on its page instead of guessing.
