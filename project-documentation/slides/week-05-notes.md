# Week 5 — instructor notes

Speaker notes for `site/week-05-slides.html`, one block per card, keyed by the card's id.
`build_deck.py` folds them into the presenter deck. The page holds a placeholder for the AIBS
segment (s2), the AEL segment on the LLM wiki with its live demo (s3–s10), and the homework
card (s11). The folder is public: run-sheet material only.

The template the demo starts from is `datadrivendecisions/llm-wiki-template`. It is a lean,
assistant-neutral version of the schema behind the AI Wiki (`businessdatasolutions/ai-wiki`):
the same three layers, page types and ingest discipline, without Quartz, qmd, retention decay
or quality scoring.

## s1

Session of Monday 5 October. AIBS theme: AI use cases at SMEs. AEL: one way to keep knowledge, built live from an empty folder.

## s2

AIBS segment. To be filled in by the AIBS lecturer before Monday.

## s3

Most of what the teams built in week 4 looks things up at the moment a question is asked: files uploaded to a chat, a folder the assistant searches, a vector store. That works, and it forgets. Ask the same question twice and it does the work twice; a contradiction between two sources is found only if a question happens to touch both. Karpathy's point is that nothing accumulates. The week 3 visualisation is the reminder that this is one of four options, not the new default.

## s4

Three folders, three owners. raw/ is the evidence and is never edited, the assistant included. wiki/ belongs to the assistant: the team reads it and asks for changes. AGENTS.md is the contract, and the team changes it when it does not fit. All six assistants the students use read AGENTS.md; CLAUDE.md and GEMINI.md in the template point to it.

## s5

Demo, part 1 (acquire). One command per format, each lands a markdown file in raw/:

- Article: `python3 tools/fetch_article.py https://oecdcogito.blog/2025/09/16/agentic-ai-for-small-business-growth/` — about 1,800 words, verbatim.
- Video: `python3 tools/fetch_youtube.py https://www.youtube.com/watch?v=51lXx4wBuHE` — captions only, the video is not downloaded; 64 minutes, about 7,600 words of automatic captions.
- Report: save the PDF in raw/reports/, then `markitdown raw/reports/oecd-empowering-smes-in-the-age-of-ai.pdf > raw/reports/oecd-empowering-smes-in-the-age-of-ai.md` — 36 pages, about 13,000 words, four seconds.

Point out that the PDF itself is not committed (.gitignore): the text is, and the source page says where the original lives.

## s6

Demo, part 2 (process). In Claude Code: `/ingest raw/articles/agentic-ai-for-small-business-growth.md — added by Witek`. Let the pause happen and read the takeaways out loud before saying go. On the source page, show the byline: a PayPal author on the OECD's blog, and the two business owners in it are invented examples. Then open wiki/index.md and wiki/log.md.

Dry run on 30 September, headless, no pause: the article took just under five minutes and wrote twelve pages. With the pause and talking, budget eight. Ingest the article live; if time is short, run the video and the report while talking over s7.

## s7

The disagreement the wiki should surface once both are in: the article describes an assistant that runs inventory and negotiates with suppliers; the OECD's own survey finds most SME users are novices using off-the-shelf tools. Show where it lands — the Debates section of the concept page, and the confidence number that went down. Also worth a sentence: the OECD calls its own sample non-representative, and the source page should say so.

## s8

Demo, part 3 (query and lint). Ask: *Which AI uses pay off first for a small manufacturer, according to the wiki?* Show the citations, then the query entry in the log with the pages it read. Then `/lint`. The quote check is the one to dwell on: it compares every quotation on a wiki page with the raw file, so an invented quotation fails. These are the two habits the knowledge architecture criteria said would come back in week 5.

## s9

Teams make their copy now, if they did not before the session. The README has the steps. Walk the room: the usual problems are Python not on the PATH on Windows (`python` instead of `python3`) and the venv not activated. Each team ingests one published source of its own and reads the source page back.

## s10

Nobody has to switch. A folder with a naming rule, traced end to end, is still a good answer. What the wiki costs: every source is read when it arrives whether anyone asks or not; a misreading lands on several pages at once; past a few hundred pages the index is not enough. A team that adopts it writes a decision-log entry and versions its knowledge architecture.

## s11

The first evaluation is held against the PRD's own criteria. The decision log travels with it. The lookup record and the quotation check are what let a team explain a wrong sentence on its page instead of guessing.
