"""Tests for aiprose.py — every code must find its own failure form, and text
written cleanly must produce nothing at all."""

from pathlib import Path

import pytest

import aiprose


def codes(text: str, **kw) -> list[str]:
    """Runs the check over a piece of text in a temporary .md file."""
    path = kw.pop("path")
    path.write_text(text, encoding="utf-8")
    return [f.code for f in aiprose.check(path, None, ())]


@pytest.fixture
def md(tmp_path) -> Path:
    return tmp_path / "text.md"


# --------------------------------------------------------------------------
# the patterns
# --------------------------------------------------------------------------
@pytest.mark.parametrize("code,sentence", [
    ("A1", "This is not a cost question, but a question about the organisation."),
    ("A1", "The scarce skill is not producing text — it is verification."),
    ("A1", "They are instruments, not homework."),
    ("A1", "It is not a report. It is a chapter of a handbook."),
    ("A1", "It measures a person rather than a company."),
    ("A1", "Without trust there is no collaboration."),
    ("A2", "This is a crucial step in the process."),
    ("A2", "A groundbreaking approach to the problem."),
    ("A3", "In today's fast-paced world, speed is what counts."),
    ("A3", "It is important to note that numbers can mislead."),
    ("A4", "The healthcare landscape is changing."),
    ("A4", "Partners work together within this ecosystem."),
    ("A5", "Let us dive into last year's figures."),
    ("A5", "The handover was seamless."),
    ("A6", "The budget forms the basis for the plan."),
    ("A6", "The manager acts as the link between the two teams."),
    ("A7", "Time will tell."),
    ("A7", "There is still room for improvement."),
    ("A8", "This approach changes the way we work."),
    ("A8", "That brings us closer to a solution."),
    ("A9", "Great question! The answer is below."),
    ("A17", "The bar is published before it is used. That is what a finished page looks like."),
])
def test_pattern_is_found(code, sentence, md):
    assert code in codes(sentence, path=md), f"{code} not found in: {sentence}"


def test_clean_text_stays_quiet(md):
    """Concrete, specific prose must produce no finding at all."""
    text = (
        "The board asked for a team of agents that would design services itself.\n"
        "We built four. The first service went live after three weeks.\n"
        "Two people watched it every day. They signed off each publication.\n"
        "Costs stayed under the agreed budget of 40,000 euro.\n"
    )
    assert codes(text, path=md) == []


# --------------------------------------------------------------------------
# densities and rhythm
# --------------------------------------------------------------------------
def test_em_dash_density(md):
    sentence = "The choice — and this is the point — rests with the board. "
    assert "A10" in codes(sentence * 6, path=md)


def test_metronome_rhythm(md):
    """Ten sentences of near-identical length."""
    text = " ".join(f"The manager of department {i} decided to discuss the plan next week."
                    for i in range(10))
    assert "A11" in codes(text, path=md)


def test_varied_rhythm_stays_quiet(md):
    text = ("It could not be done. The board had decided three weeks earlier that the team "
            "of four would build the new service themselves, on a budget the council had "
            "approved. Still it went wrong. Why? Nobody had called the supplier. "
            "That cost eight days.")
    assert "A11" not in codes(text, path=md)


def test_repeated_intensifier(md):
    """The signal is one word used over and over, not intensifiers in general."""
    text = " ".join(f"What the team actually built in week {i} was a small thing."
                    for i in range(6))
    assert "A16" in codes(text, path=md)


def test_varied_intensifiers_stay_quiet(md):
    """Six different intensifiers, each used once, is not a tic."""
    text = ("The team actually shipped it. The result was genuinely small. "
            "Nobody really minded. The board simply agreed. "
            "It was literally one page. Notably, it worked.")
    assert "A16" not in codes(text, path=md)


def test_abstraction_density(md):
    text = ("The implementation of the transformation required the coordination of the "
            "organisation, the participation of the population and the documentation of "
            "the situation before the evaluation of the operation could begin.")
    assert "D2" in codes(text, path=md)


def test_long_sentence(md):
    sentence = "The manager " + "of the department that wrote the plan " * 5 + "decided something."
    assert "D1" in codes(sentence, path=md)


def test_jargon_without_explanation(md):
    assert "D3" in codes("The stakeholders agree.", path=md)


# --------------------------------------------------------------------------
# HTML: markup gone, positions intact
# --------------------------------------------------------------------------
def test_html_keeps_length_and_lines():
    source = '<p class="lead">This is not&nbsp;a plan, but a wish.</p>\n<p>Second line.</p>'
    flat = aiprose.strip_html(source)
    assert len(flat) == len(source)
    assert flat.count("\n") == source.count("\n")
    assert "This is not a plan, but a wish" in " ".join(flat.split())


def test_html_finding_points_at_the_right_line(tmp_path):
    path = tmp_path / "page.html"
    path.write_text('<html>\n<body>\n<h2>This is not a plan, but a wish</h2>\n</body>\n</html>',
                    encoding="utf-8")
    findings = aiprose.check(path, {"A1"}, ())
    assert [f.line for f in findings] == [3]


def test_ignore_html_class(tmp_path):
    path = tmp_path / "page.html"
    path.write_text('<section data-title="Slide">\n<p>All fine here.</p>\n'
                    '<div class="notes"><p>This is not a plan, but a wish.</p></div>\n</section>',
                    encoding="utf-8")
    assert aiprose.check(path, {"A1"}, ()) != []
    assert aiprose.check(path, {"A1"}, ("notes",)) == []


def test_context_comes_from_data_title(tmp_path):
    path = tmp_path / "page.html"
    path.write_text('<section data-title="What an organisation is">\n'
                    '<p>This is not a plan, but a wish.</p>\n</section>', encoding="utf-8")
    assert aiprose.check(path, {"A1"}, ())[0].context == "What an organisation is"


def test_context_comes_from_an_html_heading(tmp_path):
    """Prose pages have <h2>, not data-title; a finding must still say where it is."""
    path = tmp_path / "page.html"
    path.write_text('<h2>How a week runs</h2>\n<p>This is not a plan, but a wish.</p>',
                    encoding="utf-8")
    assert aiprose.check(path, {"A1"}, ())[0].context == "How a week runs"


# --------------------------------------------------------------------------
# sentence splitting
# --------------------------------------------------------------------------
def test_abbreviation_does_not_break_the_sentence():
    s = aiprose.sentences("The figures, e.g. turnover, are in annex A. The notes follow.")
    assert len(s) == 2


def test_code_filter_works(md):
    md.write_text("This is not a question, but a crucial choice.", encoding="utf-8")
    assert {f.code for f in aiprose.check(md, {"A1"}, ())} == {"A1"}


def test_block_elements_separate_sentences():
    flat = aiprose.strip_html("<p>Structure who may do what</p><p>Systems where the brake sits</p>")
    assert len(flat) == len("<p>Structure who may do what</p><p>Systems where the brake sits</p>")
    assert len(aiprose.sentences(flat)) == 2


def test_long_slide_without_full_stops_gives_no_false_finding(tmp_path):
    path = tmp_path / "deck.html"
    path.write_text('<section data-title="Slide">' + "".join(
        f"<p>Card {i} holding four words</p>" for i in range(8)) + "</section>", encoding="utf-8")
    assert aiprose.check(path, {"D1"}, ()) == []


def test_extra_block_tag_separates_sentences(tmp_path):
    """Separate answer buttons in <span> are not one thirty-word sentence."""
    path = tmp_path / "deck.html"
    path.write_text("<p>" + "".join(
        f"<span>Answer {i} running to about eight words in total here</span>"
        for i in range(4)) + "</p>", encoding="utf-8")
    assert aiprose.check(path, {"D1"}, ()) != []
    assert aiprose.check(path, {"D1"}, (), ("span",)) == []


@pytest.mark.parametrize("sentence", [
    "Dashboards and performance figures (KPIs).",
    "Agile: working in short rounds.",
    "That choice is your governance: who decides what.",
    "The Integrated Reporting Framework names six kinds of capital.",
])
def test_explained_jargon_stays_quiet(sentence, md):
    assert "D3" not in codes(sentence, path=md), sentence


@pytest.mark.parametrize("sentence", [
    "The stakeholders agree.",
    "We work agile.",
    "That is on the roadmap.",
])
def test_bare_jargon_is_reported(sentence, md):
    assert "D3" in codes(sentence, path=md), sentence


def test_antithesis_without_a_signal_word(md):
    """A negation with no 'but' is not found — deliberately: whether it is hollow
    depends on what surrounds it. See 'When it stays' in SKILL.md."""
    assert "A1" not in codes("Technology changes. Organising stays.", path=md)
