from slidewords import measure, main

CARD = '''
    <div class="slide-head"><div class="slide-kicker">Kicker words</div><span class="slide-no">1 / 2</span></div>
    <h2>Your PRD is the first of six</h2>
    <p>Eight drafts, read against the <a href="x.html">twenty criteria</a>.</p>
    <ul><li><strong>One.</strong> Short.</li><li>Two</li></ul>
'''


def test_head_is_not_counted():
    m = measure(CARD)
    assert m["headline"] == "Your PRD is the first of six"
    assert m["headline_words"] == 7
    assert m["body_words"] == 10  # kicker and slide number excluded
    assert m["bullets"] == 2


def test_bullets_are_separate_sentences():
    assert measure(CARD)["longest_sentence"] == 7


def test_exit_code(tmp_path):
    deck = tmp_path / "deck.html"
    deck.write_text('<section class="slide" id="s1">' + CARD + "</section>")
    assert main([str(deck)]) == 0
    assert main([str(deck), "--max-words", "5"]) == 1
