"""The Socratic gate, as code rather than as console fields.

Agent Designer generated a version of this that wrapped url_context in an
LlmAgent and passed it as a tool. That is a second language model, so it read the
page and wrote its own account of it: the summary it returned had dropped the
source list entirely, and the gate scored a page it had never seen (run 4 in
../test-fixtures/pilot-log.md). fetch_page below is a plain function, so what
reaches the model is what the team published.

Search stays wrapped, because a summarised search result is fine — the only thing
asked of it is whether a work exists.

Run locally with `adk web` from the parent directory.
"""

import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.genai import types

# The model's knowledge ends long before the course runs, so without being told
# the date it reads a 2026 source as dated in the future and reports real work as
# fabricated — run 5 did exactly that to the fixture's control source.
INSTRUCTIONS = (Path(__file__).parent / "instructions.txt").read_text(
    encoding="utf-8"
).replace("{{TODAY}}", date.today().strftime("%-d %B %Y"))

MAX_BYTES = 2_000_000
BLOCK_TAGS = {"p", "li", "tr", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6",
              "section", "article", "blockquote", "dt", "dd"}
# Only tags that wrap text we do not want. Void elements such as <meta> and
# <link> must never appear here: they have no end tag, so a depth counter that
# they increment is never decremented and the rest of the page is discarded.
DROP_TAGS = {"script", "style", "noscript"}


class _Extract(HTMLParser):
    """HTML to text, keeping every href — the source list is the point."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self._dropping = 0

    def handle_starttag(self, tag, attrs):
        if tag in DROP_TAGS:
            self._dropping += 1
        elif tag in BLOCK_TAGS:
            self.out.append("\n")
        elif tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.out.append(f" [{href}] ")

    def handle_endtag(self, tag):
        if tag in DROP_TAGS and self._dropping:
            self._dropping -= 1
        elif tag in BLOCK_TAGS:
            self.out.append("\n")

    def handle_data(self, data):
        if not self._dropping:
            self.out.append(data)

    def text(self):
        lines = [" ".join(line.split()) for line in "".join(self.out).splitlines()]
        return "\n".join(line for line in lines if line)


def fetch_page(url: str) -> dict:
    """Fetch a published handbook page and return its text exactly as written.

    Returns the page's own words and its own source list, with every link kept
    inline in square brackets. Does not summarise, shorten or rewrite anything.

    Args:
        url: The http(s) address of the team's published page.

    Returns:
        A dict with status 'ok' and the page under 'text', or status 'error'
        and the reason under 'error'.
    """
    if not url.startswith(("http://", "https://")):
        return {"status": "error", "error": f"not an http(s) url: {url}"}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "socratic-gate/pilot"})
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read(MAX_BYTES)
        parser = _Extract()
        parser.feed(raw.decode("utf-8", errors="replace"))
        text = parser.text()
    except Exception as exc:                                  # noqa: BLE001
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}
    if not text.strip():
        return {"status": "error", "error": "page fetched but contained no text"}
    return {"status": "ok", "text": text}


search_agent = LlmAgent(
    name="Socratic_Gate__pilot__google_search_agent",
    model="gemini-2.5-flash",
    description="Agent specialized in performing Google searches.",
    instruction="Use the GoogleSearchTool to find information on the web.",
    tools=[GoogleSearchTool()],
)

root_agent = LlmAgent(
    name="Socratic_Gate__pilot_",
    model="gemini-2.5-flash",
    description=(
        "Asks a student team Socratic questions about the thinking behind the "
        "handbook page they published this week. Takes one published page URL "
        "plus that team's earlier reports; returns questions to the team, and a "
        "process-rubric score with an open/closed gate signal to the two module "
        "owners. One run per team per teaching week, weeks 2-6. Never given "
        "transcripts or personal data. Pilot instance."
    ),
    instruction=INSTRUCTIONS,
    generate_content_config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
    ),
    tools=[
        fetch_page,
        agent_tool.AgentTool(agent=search_agent),
    ],
)
