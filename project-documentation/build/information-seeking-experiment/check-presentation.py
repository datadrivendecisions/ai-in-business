#!/usr/bin/env python3
"""Phase 6 — brand, access, publication. Checked against the shipped page.

PR-1  the brand token block is byte-identical to the one in index.html
PR-3  every text/background pair that can actually occur meets WCAG AA,
      and --text-muted never lands on --bg-cream
PR-5  one sticky nav, whose wordmark matches index.html's
PR-6  one footer, carrying one credit line that points at the colophon

PR-2 and PR-4 are verified by demonstration -- a person on a real phone, a
person on a real keyboard -- and nothing here replaces that. What is here are
the two screens a person should not have to be the first to run: the longest
unbreakable run of text on the page measured against a 400 px content box,
and the markup patterns that make a keyboard trap. Both are named (screen)
in the output so a pass is not mistaken for the demonstration.

PR-3 is the only one that needs work. A colour pair is not a property of a
rule -- it is a property of an element, whose foreground comes from one rule
and whose background comes from whichever ancestor last set one. So this
builds the document tree, runs a small cascade over it, and asks each text
node what colour it ends up being on what.

The cascade is deliberately small: tag, class, id, attribute, descendant and
child combinators, and the interactive states (:hover, :focus-visible, and
:has(input:checked)) evaluated as separate variants because several of them
swap both colours at once. Anything it cannot parse is reported rather than
skipped, so a selector this does not understand fails loudly.

No dependencies, no package manager, same as everything else here.
"""

import html.parser
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "site"))
PAGE = (sys.argv[1] if len(sys.argv) > 1
        else os.path.join(SITE, "tool-bias-experiment.html"))
INDEX = os.path.join(SITE, "index.html")

NARROW_PX = 400.0          # the width PR-2 names
NARROW_PADDING_PX = 16.0   # var(--space-4), the .bds-page padding under 720 px
NARROW_CONTENT_PX = NARROW_PX - 2 * NARROW_PADDING_PX

# Strings the script injects, and the element each one lands in. A card's APA
# reference never appears in the markup, so a check that reads only the HTML
# would miss the longest text on the page by a factor of three.
INJECTED = {
    "c-meta": "ref",
    "c-teaser": "teaser",
    "c-title": "title",
    "c-extract": "extract",
}

BREAKING = {
    "overflow-wrap": ("anywhere", "break-word"),
    "word-break": ("break-all", "break-word"),
    "word-wrap": ("break-word",),
}

AA_NORMAL = 4.5
AA_LARGE = 3.0
ROOT_FONT_PX = 16.0

# ---------------------------------------------------------------- colour ---

NAMED = {"white": "#ffffff", "black": "#000000", "transparent": None}


def parse_colour(value):
    """A colour, or None for 'no colour here' (transparent, a gradient, none)."""
    v = value.strip().lower()
    if not v or v in ("none", "inherit", "initial", "unset", "currentcolor"):
        return None
    if v in NAMED:
        return NAMED[v]
    m = re.match(r"^#([0-9a-f]{3}|[0-9a-f]{6})$", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return "#" + h
    m = re.match(r"^rgba?\(([^)]*)\)$", v)
    if m:
        parts = [p.strip() for p in re.split(r"[,\s/]+", m.group(1)) if p.strip()]
        try:
            r, g, b = (int(float(p)) for p in parts[:3])
        except ValueError:
            return None
        if len(parts) > 3 and float(parts[3]) == 0:
            return None
        return "#%02x%02x%02x" % (r, g, b)
    # a shorthand such as "background: var(--x) url(...) no-repeat" -- take the
    # first thing in it that reads as a colour
    for token in v.split():
        if token.startswith("#") or token in NAMED:
            return parse_colour(token)
    return None


def luminance(hex_colour):
    r, g, b = (int(hex_colour[i:i + 2], 16) / 255.0 for i in (1, 3, 5))

    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# ------------------------------------------------------------------- css ---

def strip_comments(text):
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def expand_vars(value, tokens):
    """Resolve var(--x) and var(--x, fallback) against the :root block."""
    for _ in range(8):
        m = re.search(r"var\(\s*(--[\w-]+)\s*(?:,([^()]*))?\)", value)
        if not m:
            return value
        name, fallback = m.group(1), (m.group(2) or "").strip()
        value = value[:m.start()] + tokens.get(name, fallback) + value[m.end():]
    return value


def parse_css(css):
    """[(selector, {property: value})], at-rule blocks flattened into the list.

    Media queries are flattened deliberately. Nothing in this page changes a
    colour inside one, so a colour pair that is unsafe at any width is unsafe
    -- and flattening means a pair that only appears under a media query is
    still checked rather than quietly skipped.
    """
    css = strip_comments(css)
    rules = []

    def block(body):
        i = 0
        while i < len(body):
            brace = body.find("{", i)
            if brace < 0:
                break
            selector = body[i:brace].strip()
            if selector.startswith("@"):
                depth, j = 1, brace + 1
                while j < len(body) and depth:
                    if body[j] == "{":
                        depth += 1
                    elif body[j] == "}":
                        depth -= 1
                    j += 1
                if selector.split()[0] in ("@media", "@supports"):
                    block(body[brace + 1:j - 1])
                i = j
                continue
            close = body.find("}", brace)
            if close < 0:
                break
            decls = {}
            for decl in body[brace + 1:close].split(";"):
                if ":" not in decl:
                    continue
                prop, _, val = decl.partition(":")
                decls[prop.strip().lower()] = val.strip()
            for sel in selector.split(","):
                sel = sel.strip()
                if sel:
                    rules.append((sel, decls))
            i = close + 1

    block(css)
    return rules


# -------------------------------------------------------------- selector ---

STATES = (":hover", ":focus", ":focus-visible", ":focus-within", ":active",
          ":checked", ":visited", ":last-child", ":first-child", ":disabled")

SIMPLE = re.compile(
    r"""(?P<tag>^[a-zA-Z][\w-]*|\*)|
        (?P<cls>\.[\w-]+)|
        (?P<id>\#[\w-]+)|
        (?P<attr>\[[^\]]*\])|
        (?P<has>:has\([^)]*\))|
        (?P<pseudo>::?[\w-]+(\([^)]*\))?)""",
    re.X)


class Unparseable(Exception):
    pass


def compound(text):
    """One compound selector -> (tag, classes, id, attrs, is_state)."""
    tag, classes, el_id, attrs, state = None, set(), None, [], False
    pos = 0
    while pos < len(text):
        m = SIMPLE.match(text, pos)
        if not m or m.end() == pos:
            raise Unparseable(text)
        if m.group("tag"):
            tag = m.group("tag").lower()
        elif m.group("cls"):
            classes.add(m.group("cls")[1:])
        elif m.group("id"):
            el_id = m.group("id")[1:]
        elif m.group("attr"):
            body = m.group("attr")[1:-1]
            name, _, want = body.partition("=")
            attrs.append((name.strip().lower(), want.strip().strip("\"'") or None))
        elif m.group("has"):
            state = True
        else:
            p = m.group("pseudo")
            if p.startswith("::"):
                raise Unparseable(text)   # pseudo-elements carry their own box
            if p.split("(")[0] in STATES:
                state = True
            else:
                raise Unparseable(text)
        pos = m.end()
    return tag, classes, el_id, attrs, state


def parse_selector(sel):
    """-> ([(combinator, compound)], is_state). Combinator ' ' or '>'."""
    sel = re.sub(r"\s*>\s*", " > ", sel.strip())
    parts, state = [], False
    combinator = " "
    for chunk in sel.split():
        if chunk == ">":
            combinator = ">"
            continue
        tag, classes, el_id, attrs, st = compound(chunk)
        state = state or st
        parts.append((combinator, (tag, classes, el_id, attrs)))
        combinator = " "
    return parts, state


def specificity(parts):
    a = b = c = 0
    for _, (tag, classes, el_id, attrs) in parts:
        if el_id:
            a += 1
        b += len(classes) + len(attrs)
        if tag and tag != "*":
            c += 1
    return (a, b, c)


# -------------------------------------------------------------------- dom ---

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


class Node:
    __slots__ = ("tag", "attrs", "classes", "id", "parent", "kids", "text", "line")

    def __init__(self, tag, attrs, parent, line):
        self.tag = tag
        self.attrs = attrs
        self.classes = set((attrs.get("class") or "").split())
        self.id = attrs.get("id")
        self.parent = parent
        self.kids = []
        self.text = ""
        self.line = line


class Tree(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None, 0)
        self.stack = [self.root]
        self.styles = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        node = Node(tag, a, self.stack[-1], self.getpos()[0])
        self.stack[-1].kids.append(node)
        if tag == "style":
            self._in_style = True
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        self.stack[-1].kids.append(Node(tag, a, self.stack[-1], self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)
        elif data.strip():
            self.stack[-1].text += data


def matches(node, parts):
    """Rightmost-first walk up the ancestor chain."""
    def one(n, comp):
        tag, classes, el_id, attrs = comp
        if tag and tag != "*" and n.tag != tag:
            return False
        if el_id and n.id != el_id:
            return False
        if not classes <= n.classes:
            return False
        for name, want in attrs:
            if name not in n.attrs:
                return False
            if want is not None and n.attrs[name] != want:
                return False
        return True

    def walk(n, i):
        combinator, comp = parts[i]
        if not one(n, comp):
            return False
        if i == 0:
            return True
        prev_comb = parts[i][0]
        parent = n.parent
        if prev_comb == ">":
            return bool(parent) and walk(parent, i - 1)
        while parent and parent.tag != "#root":
            if walk(parent, i - 1):
                return True
            parent = parent.parent
        return False

    return walk(node, len(parts) - 1)


# ------------------------------------------------------------------ sizes ---

def font_px(value, inherited):
    v = value.strip().lower()
    m = re.match(r"^([\d.]+)(px|rem|em|%)?$", v)
    if not m:
        return inherited
    n = float(m.group(1))
    unit = m.group(2) or "px"
    if unit == "px":
        return n
    if unit == "rem":
        return n * ROOT_FONT_PX
    if unit == "em":
        return n * inherited
    return inherited * n / 100.0


def weight_of(value, inherited):
    v = value.strip().lower()
    if v == "bold":
        return 700
    if v == "normal":
        return 400
    if v.isdigit():
        return int(v)
    return inherited


# ----------------------------------------------------------------- cascade ---

def computed(tree, rules, tokens, state_on):
    """{node: (colour, background, font_px, weight)} for every element."""
    compiled = []
    unparsed = []
    for sel, decls in rules:
        if not ({"color", "background", "background-color", "font-size",
                 "font-weight"} & set(decls)):
            continue
        try:
            parts, is_state = parse_selector(sel)
        except Unparseable:
            unparsed.append(sel)
            continue
        if is_state and not state_on:
            continue
        compiled.append((specificity(parts), len(compiled), parts, decls))
    compiled.sort(key=lambda r: (r[0], r[1]))

    out = {}

    def visit(node, colour, background, size, weight):
        for _, _, parts, decls in compiled:
            if not matches(node, parts):
                continue
            if "color" in decls:
                c = parse_colour(expand_vars(decls["color"], tokens))
                if c:
                    colour = c
            for prop in ("background", "background-color"):
                if prop in decls:
                    b = parse_colour(expand_vars(decls[prop], tokens))
                    if b:
                        background = b
            if "font-size" in decls:
                size = font_px(expand_vars(decls["font-size"], tokens), size)
            if "font-weight" in decls:
                weight = weight_of(decls["font-weight"], weight)
        if node.tag in ("strong", "b", "th", "h1", "h2", "h3", "h4", "legend",
                        "summary", "dt"):
            weight = max(weight, 700)
        if node.tag in ("small", "code"):
            pass
        out[node] = (colour, background, size, weight)
        for kid in node.kids:
            if kid.tag in ("script", "style", "svg", "head", "title", "meta"):
                continue
            visit(kid, colour, background, size, weight)

    for kid in tree.root.kids:
        if kid.tag in ("script", "style", "!doctype"):
            continue
        visit(kid, "#000000", "#ffffff", ROOT_FONT_PX, 400)
    return out, unparsed


def path_of(node):
    bits = []
    n = node
    while n and n.tag != "#root":
        bit = n.tag
        if n.id:
            bit += "#" + n.id
        elif n.classes:
            bit += "." + ".".join(sorted(n.classes))
        bits.append(bit)
        n = n.parent
    return " > ".join(reversed(bits[:6]))


# ------------------------------------------------------------------ checks ---

# Where a browser will break a long run that has no space in it. Measured in
# Chrome at a 400 px viewport rather than taken from the spec: of
# / - ? & # = _ . : , + ~ % @ | only the hyphen and the question mark are
# break opportunities. That distinction is the whole check. The longest URL in
# the deck is 157 characters and wraps without help because it is full of
# hyphens; the one that pushes the page sideways is a 73-character USENIX path
# with no hyphen in it. Splitting on whitespace alone reports the first and
# misses the second.
BREAK_AFTER = re.compile(r"[\s?]+|(?<=-)")


def longest_run(text):
    runs = [t for t in BREAK_AFTER.split(text) if t]
    return max(runs, key=len) if runs else ""


def estimate_px(token, size, mono):
    """Roughly how wide that run renders. 0.5 em a character for the system
    sans stack, 0.6 for the monospace one -- deliberately generous, since a
    URL is lowercase-heavy and this is a screen rather than a measurement."""
    return len(token) * size * (0.6 if mono else 0.5)


def check_narrow(tree, rules, tokens, page):
    """PR-2 (screen): nothing unbreakable is wider than a 400 px content box."""
    styles, _ = computed(tree, rules, tokens, False)

    breakable = set()
    mono = set()
    compiled = []
    for sel, decls in rules:
        if not ({"overflow-wrap", "word-break", "word-wrap", "font-family"}
                & set(decls)):
            continue
        try:
            parts, is_state = parse_selector(sel)
        except Unparseable:
            continue
        if is_state:
            continue
        compiled.append((parts, decls))

    for node in styles:
        for parts, decls in compiled:
            if not matches(node, parts):
                continue
            for prop, values in BREAKING.items():
                if decls.get(prop, "").strip().lower() in values:
                    breakable.add(node)
            if "mono" in decls.get("font-family", "").lower():
                mono.add(node)

    def inherits(node, marked):
        n = node
        while n is not None and n.tag != "#root":
            if n in marked:
                return True
            n = n.parent
        return False

    by_id = {}
    for node in styles:
        if node.id:
            by_id[node.id] = node

    findings = []
    for node, (_, _, size, _) in styles.items():
        texts = []
        if node.text.strip():
            texts.append(node.text)
        field = INJECTED.get(node.id or "")
        if field:
            for m in re.finditer(field + r': "((?:[^"\\\\]|\\\\.)*)"', page):
                texts.append(m.group(1))
        if not texts:
            continue
        if inherits(node, breakable):
            continue
        is_mono = inherits(node, mono)
        for text in texts:
            token = longest_run(text)
            width = estimate_px(token, size, is_mono)
            if width > NARROW_CONTENT_PX:
                findings.append(
                    "%s  line %d  a %d-character run at %.0f px is about %.0f px "
                    "wide in a %.0f px box\n              %s"
                    % (node.tag, node.line, len(token), size, width,
                       NARROW_CONTENT_PX, token[:70] + ("..." if len(token) > 70 else "")))
                break

    for sel, decls in rules:
        for prop in ("width", "min-width"):
            v = decls.get(prop, "").strip().lower()
            m = re.match(r"^([\d.]+)(px|rem)$", expand_vars(v, tokens))
            if not m:
                continue
            px = float(m.group(1)) * (ROOT_FONT_PX if m.group(2) == "rem" else 1)
            if px > NARROW_CONTENT_PX:
                findings.append("%s sets %s: %s (%.0f px), wider than the box"
                                % (sel, prop, v, px))

    return findings


def check_keyboard(tree, page):
    """PR-4 (screen): the markup patterns that make a trap."""
    findings = []
    for m in re.finditer(r'tabindex="(-?\d+)"', page):
        if int(m.group(1)) > 0:
            findings.append(
                "a positive tabindex (%s) takes an element out of document order"
                % m.group(1))

    interactive = ("button", "select", "textarea", "summary")

    def walk(node):
        if node.tag in interactive or (node.tag == "a" and node.attrs.get("href")) \
                or (node.tag == "input" and node.attrs.get("type") != "hidden"):
            if node.attrs.get("tabindex") == "-1":
                findings.append("%s at line %d is removed from the tab order"
                                % (node.tag, node.line))
            if node.attrs.get("aria-hidden") == "true":
                findings.append("%s at line %d is focusable but aria-hidden"
                                % (node.tag, node.line))
        for kid in node.kids:
            walk(kid)

    walk(tree.root)

    script = "\n".join(re.findall(r"<script>(.*?)</script>", page, re.S))
    if re.search(r"key(down|press|up)", script) and "preventDefault" in script:
        findings.append("a key handler calls preventDefault; check it does not "
                        "swallow Tab")
    if "inert" in script or re.search(r"\.focus\(\)[^\n]*loop", script):
        findings.append("focus is being managed in script; walk it by hand")
    if "focus-visible" not in page:
        findings.append("no :focus-visible style, so the focused control is invisible")
    return findings


def token_block(text):
    m = re.search(r":root\s*\{.*?\}", text, re.S)
    return m.group(0) if m else None


def report(name, ok, detail):
    print(("  PASS  " if ok else "  FAIL  ") + name)
    for line in detail:
        print("        " + line)
    return ok


def main():
    page = open(PAGE, encoding="utf-8").read()
    index = open(INDEX, encoding="utf-8").read()
    ok = True

    print("Phase 6 — brand, access, publication")
    print("site/tool-bias-experiment.html\n")

    # PR-1 ---------------------------------------------------------------
    mine, theirs = token_block(page), token_block(index)
    ok &= report(
        "PR-1  token block byte-identical to index.html",
        mine is not None and mine == theirs,
        [] if mine == theirs else ["the :root blocks differ; diff the two files"])

    # PR-5 ---------------------------------------------------------------
    navs = re.findall(r'<nav class="bds-nav".*?</nav>', page, re.S)
    index_nav = re.findall(r'<nav class="bds-nav".*?</nav>', index, re.S)
    detail = []
    nav_ok = len(navs) == 1 and len(index_nav) == 1
    if nav_ok:
        wordmark = re.compile(r'<a href="index.html" class="bds-wordmark".*?</a>', re.S)
        a, b = wordmark.search(navs[0]), wordmark.search(index_nav[0])
        nav_ok = bool(a and b and a.group(0) == b.group(0))
        if not nav_ok:
            detail.append("the wordmark differs from index.html's")
    else:
        detail.append("found %d bds-nav elements, expected 1" % len(navs))
    ok &= report("PR-5  one sticky nav, wordmark matching index.html", nav_ok, detail)

    # PR-6 ---------------------------------------------------------------
    footers = re.findall(r'<footer class="bds-footer">.*?</footer>', page, re.S)
    detail = []
    foot_ok = len(footers) == 1
    if foot_ok:
        credits = re.findall(r'class="bds-credit"', footers[0])
        foot_ok = len(credits) == 1 and 'index.html#colophon' in footers[0]
        if not foot_ok:
            detail.append("expected 1 bds-credit pointing at index.html#colophon")
    else:
        detail.append("found %d bds-footer elements, expected 1" % len(footers))
    ok &= report("PR-6  one footer, one credit, pointing at the colophon", foot_ok, detail)

    # PR-3 ---------------------------------------------------------------
    tree = Tree()
    tree.feed(page)
    css = "\n".join(tree.styles)
    tokens = {}
    root = token_block(css) or ""
    for decl in root[root.find("{") + 1:root.rfind("}")].split(";"):
        if ":" in decl:
            k, _, v = decl.partition(":")
            tokens[k.strip()] = v.strip()
    rules = parse_css(css)

    muted = parse_colour(tokens.get("--text-muted", ""))
    cream = {parse_colour(tokens.get(t, "")) for t in ("--bg-cream", "--bg-cream-2")}

    failures, muted_on_cream, unparsed_all = [], [], set()
    for state_on in (False, True):
        styles, unparsed = computed(tree, rules, tokens, state_on)
        unparsed_all.update(unparsed)
        for node, (colour, background, size, weight) in styles.items():
            if not node.text.strip():
                continue
            floor = AA_LARGE if (size >= 24 or (size >= 18.66 and weight >= 700)) else AA_NORMAL
            ratio = contrast(colour, background)
            label = "%s  line %d  %s on %s  %.2f:1 (needs %.1f)%s" % (
                node.tag, node.line, colour, background, ratio, floor,
                "  [hover/focus state]" if state_on else "")
            if ratio < floor - 0.005:
                failures.append((ratio, label, path_of(node)))
            if colour == muted and background in cream:
                muted_on_cream.append(label + "  " + path_of(node))

    seen, unique = set(), []
    for ratio, label, path in sorted(failures):
        if label in seen:
            continue
        seen.add(label)
        unique.append("%s\n              %s" % (label, path))

    detail = list(unique[:20])
    if len(unique) > 20:
        detail.append("... and %d more" % (len(unique) - 20))
    if muted_on_cream:
        detail.append("--text-muted on cream, %d instances" % len(muted_on_cream))
    if unparsed_all:
        detail.append("selectors this check could not read, so did not apply: "
                      + ", ".join(sorted(unparsed_all)))
    ok &= report(
        "PR-3  contrast >= %.1f:1 on every text node; 0 muted-on-cream" % AA_NORMAL,
        not unique and not muted_on_cream and not unparsed_all,
        detail)

    # PR-2 (screen) --------------------------------------------------------
    narrow = check_narrow(tree, rules, tokens, page)
    ok &= report("PR-2  (screen) nothing unbreakable exceeds a %.0f px content box"
                 % NARROW_CONTENT_PX, not narrow, narrow[:12])

    # PR-4 (screen) --------------------------------------------------------
    keyboard = check_keyboard(tree, page)
    ok &= report("PR-4  (screen) no markup pattern that makes a keyboard trap",
                 not keyboard, keyboard[:12])

    nodes_checked = sum(1 for n, _ in computed(tree, rules, tokens, False)[0].items()
                        if n.text.strip())
    print("\n%d text-bearing elements examined, in 2 state variants." % nodes_checked)
    print("PR-2 and PR-4 still need their demonstration: a real phone, a real keyboard.")
    print("RESULT: " + ("all checks pass" if ok else "one or more checks failed"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
