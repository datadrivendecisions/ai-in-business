/* Phases 1, 3 and 4: drive whole sessions through the shipped page's own code.
 *
 * The stub here is fuller than runpage.mjs's: it remembers the click handlers
 * the page registers and it keeps the state of the radio groups, which is
 * enough to take a session from the consent screen to a result line. It is not
 * a browser and does not pretend to be one — what it checks is the runner's
 * behaviour, which is logic. Layout, focus order, the network panel and a real
 * phone are checked in a browser, by a person.
 *
 *     node check-session.mjs [-v]
 */

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import vm from "node:vm";

const here = dirname(fileURLToPath(import.meta.url));
const pagePath = join(here, "..", "..", "..", "site", "tool-bias-experiment.html");
const html = readFileSync(pagePath, "utf8");
const source = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
const verbose = process.argv.includes("-v");

function makePage(initialStorage) {
  const handlers = new Map();
  const nodes = new Map();
  const radios = new Map();
  const store = new Map();
  if (initialStorage) store.set("bxp-v1", initialStorage);
  let reloaded = false;

  function el(id) {
    const node = {
      id,
      style: {}, classList: { add() {}, remove() {} },
      textContent: "", value: "", href: "", hidden: false, checked: false,
      disabled: false, type: "", name: "",
      addEventListener(ev, fn) {
        if (ev === "click") handlers.set(id, fn);
      },
      appendChild() {}, removeChild() {}, focus() {}, select() {},
      setAttribute() {}, removeAttribute() {},
      querySelector: () => el(id + ":q"),
      querySelectorAll: () => [],
    };
    node.parentNode = { hidden: false };
    return node;
  }

  const document = {
    getElementById(id) {
      if (!nodes.has(id)) nodes.set(id, el(id));
      return nodes.get(id);
    },
    createElement: () => el("(new)"),
    createTextNode: (t) => ({ nodeValue: String(t) }),
    querySelector(sel) {
      const m = /^input\[name="([^"]+)"\]:checked$/.exec(sel);
      if (m) {
        const v = radios.get(m[1]);
        return v === undefined ? null : { value: v };
      }
      const g = /^input\[name="([^"]+)"\]$/.exec(sel);
      if (g) return { focus() {} };
      return null;
    },
    querySelectorAll(sel) {
      const m = /^input\[name="([^"]+)"\](:checked)?$/.exec(sel);
      if (!m) return [];
      // Enough of a radio group for setSide to clear or set it.
      return [1, 2, 3, 4, 5, 6, 7].map((n) => ({
        value: String(n),
        set checked(on) { if (on) radios.set(m[1], String(n)); },
        get checked() { return radios.get(m[1]) === String(n); },
      })).concat([
        { value: "agree", set checked(on) { if (on) radios.set(m[1], "agree"); }, get checked() { return radios.get(m[1]) === "agree"; } },
        { value: "disagree", set checked(on) { if (on) radios.set(m[1], "disagree"); }, get checked() { return radios.get(m[1]) === "disagree"; } },
      ]);
    },
    body: el("body"),
    execCommand() {},
  };

  const windowObj = {
    document,
    localStorage: {
      getItem: (k) => (store.has(k) ? store.get(k) : null),
      setItem: (k, v) => store.set(k, String(v)),
      removeItem: (k) => store.delete(k),
    },
    navigator: {},
    location: { search: "", reload() { reloaded = true; } },
    setTimeout: () => 0,
    confirm: () => true,
    scrollTo() {},
  };
  windowObj.window = windowObj;

  const sandbox = {
    window: windowObj, document, localStorage: windowObj.localStorage,
    navigator: windowObj.navigator, console,
    Math, Date, JSON, isFinite, Number, String, Object, Array, RegExp, Error,
    parseInt, parseFloat, setTimeout: () => 0,
  };
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(source, sandbox, { filename: "tool-bias-experiment.html" });

  return {
    sandbox, store, radios, nodes,
    reloaded: () => reloaded,
    click(id) {
      const fn = handlers.get(id);
      if (!fn) throw new Error("no click handler on " + id);
      fn();
    },
    set(id, value) { document.getElementById(id).value = value; },
    pick(name, value) { radios.set(name, value); },
    text(id) { return document.getElementById(id).textContent; },
    screen() { return sandbox.S.screen; },
    S() { return sandbox.S; },
  };
}

const fails = [];
function ok(label, cond, detail) {
  if (!cond) fails.push(label + (detail ? " — " + detail : ""));
  else if (verbose) console.log("   " + label);
}

function start(p, code, team) {
  p.set("f-code", code);
  p.set("f-team", String(team));
  p.click("b-consent");
}
function lockPosition(p, side, text) {
  p.pick("side", side);
  p.set("f-position", text);
  p.click("b-position");
}
function answerQuestions(p, v) {
  for (const item of p.sandbox.window.BXP.TLX.concat(p.sandbox.window.BXP.PERCEPTION)) {
    p.radios.set("q-" + item.id, String(v));
  }
  p.click("b-questions");
}

/* ---- SM-1, SM-2, SM-9: the deck, the shuffle, and the record of it ---- */
{
  const orders = new Set();
  let everyRoundHad16 = true, everyOrderStored = true;
  for (let i = 0; i < 20; i++) {
    const p = makePage();
    start(p, "c" + i, (i % 8) + 1);
    const order = p.S().rounds[1].order;
    if (order.length !== 16 || new Set(order).size !== 16) everyRoundHad16 = false;
    const stored = JSON.parse(p.store.get("bxp-v1"));
    if (!stored || !stored.rounds || !stored.rounds[1] || stored.rounds[1].order.join() !== order.join()) {
      everyOrderStored = false;
    }
    orders.add(order.join(","));
  }
  console.log("\nSM-1, SM-2, SM-9 — the deck and its order");
  ok("16 distinct cards in every round", everyRoundHad16);
  ok(`at least 19 distinct orders in 20 sessions (got ${orders.size})`, orders.size >= 19);
  ok("the shown order is in stored state, 20 of 20", everyOrderStored);
}

/* ---- SM-3, SM-4: the budget and the one-way walk ---- */
{
  console.log("\nSM-3, SM-4 — the budget of eight and no way back");
  let refusals = 0, everOverBudget = false, revisited = false;
  for (let attempt = 0; attempt < 100; attempt++) {
    const p = makePage();
    start(p, "b" + attempt, 1);          // team 1: the assistant is in round 2
    lockPosition(p, "agree", "because.");
    const seen = [];
    for (let i = 0; i < 16; i++) {
      const before = p.S().rounds[1].opens;
      p.click("b-open");
      const after = p.S().rounds[1].opens;
      if (before === 8 && after === 8) refusals++;
      if (after > 8) everOverBudget = true;
      const idx = p.S().rounds[1].idx;
      const id = p.S().rounds[1].order[idx];
      if (seen.includes(id)) revisited = true;
      seen.push(id);
      p.click(after > before ? "b-next" : "b-pass");
    }
    if (p.S().rounds[1].opens !== 8) everOverBudget = true;
  }
  ok(`the 9th open refused in 100 of 100 attempts (${refusals} refusals over ${100 * 8} tries past the budget)`, refusals === 800);
  ok("no session ever exceeded 8 opens", !everOverBudget);
  ok("no card was shown twice", !revisited);

  // A passed card leaves no route back: idx only ever rises, and a choice is
  // recorded for every index below it.
  const p = makePage();
  start(p, "back", 1);
  lockPosition(p, "agree", "because.");
  let monotone = true, lastIdx = -1;
  for (let i = 0; i < 16; i++) {
    const idx = p.S().rounds[1].idx;
    if (idx <= lastIdx) monotone = false;
    lastIdx = idx;
    p.click("b-pass");
  }
  ok("the card index only ever rises", monotone);
  ok("a choice is recorded for every card shown", p.S().rounds[1].choices.length === 16);
}

/* ---- DA-1: one key ---- */
{
  console.log("\nDA-1 — one storage key");
  const p = makePage();
  ok("nothing is written before consent", p.store.size === 0);
  start(p, "kite", 3);
  ok(`1 storage key after consent (got ${p.store.size}: ${[...p.store.keys()]})`, p.store.size === 1);
  lockPosition(p, "agree", "because.");
  ok("still 1 key mid-session", p.store.size === 1);
  p.click("b-erase");
  ok("erase removes the key", p.store.size === 0);
  ok("erase reloads the page", p.reloaded());
}

/* ---- AG-3, and which round carries the assistant ---- */
{
  console.log("\nAG-1 placement, AG-3 — the assistant step");
  for (let team = 1; team <= 8; team++) {
    const expected = team <= 4 ? 2 : 1;
    const p = makePage();
    start(p, "t" + team, team);
    ok(`team ${team}: the assistant is assigned to round ${expected}`,
       p.S().rounds[1].agent === (expected === 1), `round 1 agent = ${p.S().rounds[1].agent}`);
    lockPosition(p, "agree", "because.");
    if (expected === 1) {
      ok(`team ${team}: the assistant screen precedes card 1`, p.screen() === "agent", "screen is " + p.screen());
      // AG-3: an empty box is not a way through.
      p.set("f-agent-reply", "   ");
      p.click("b-agent");
      ok(`team ${team}: an empty paste box does not let you past`, p.screen() === "agent");
      p.set("f-agent-reply", "1. What would change your mind?");
      p.click("b-agent");
      ok(`team ${team}: a pasted reply does`, p.screen() === "card");
    } else {
      ok(`team ${team}: round 1 goes straight to the cards`, p.screen() === "card", "screen is " + p.screen());
    }
  }
}

/* ---- MS-5: the clock ---- */
{
  console.log("\nMS-5 — per-card timing");
  const p = makePage();
  start(p, "clock", 1);
  lockPosition(p, "agree", "because.");
  const wait = 220;
  const t0 = Date.now();
  for (let i = 0; i < 5; i++) {
    const until = Date.now() + wait;
    while (Date.now() < until) { /* a real wait: the page reads a real clock */ }
    p.click("b-pass");
  }
  const wall = Date.now() - t0;
  const recorded = p.S().rounds[1].choices.slice(0, 5).reduce((a, c) => a + c.ms, 0);
  ok(`5 cards timed within 100 ms of the wall clock (wall ${wall} ms, recorded ${recorded} ms)`,
     Math.abs(wall - recorded) < 100);
  ok("every card carries its own timing", p.S().rounds[1].choices.slice(0, 5).every((c) => c.ms >= wait - 5));
}

/* ---- a whole session, and the line it produces ---- */
{
  console.log("\nPhase 4 gate — one complete session end to end");
  const p = makePage();
  start(p, "kite", 3);                   // team 3: the assistant is in round 2
  for (const round of [1, 2]) {
    lockPosition(p, round === 1 ? "agree" : "disagree", "round " + round + " opening sentence.");
    if (p.screen() === "agent") {
      p.set("f-agent-reply", "1. What would change your mind? 2. What does the other side rest on? 3. What would have to hold?");
      p.click("b-agent");
    }
    ok(`round ${round}: the cards come up`, p.screen() === "card");
    for (let i = 0; i < 16; i++) {
      const before = p.S().rounds[round].opens;
      if (i % 2 === 0) p.click("b-open");
      p.click(p.S().rounds[round].opens > before ? "b-next" : "b-pass");
    }
    ok(`round ${round}: the final position screen`, p.screen() === "final");
    p.pick("fside", round === 1 ? "agree" : "agree");
    p.set("f-final", round === 1 ? "round 1 opening sentence." : "a different sentence.");
    p.click("b-final");
    ok(`round ${round}: the closing questions`, p.screen() === "questions");
    answerQuestions(p, 4);
    if (round === 1) {
      ok("round 1 ends at the bridge", p.screen() === "bridge");
      p.click("b-bridge");
    }
  }
  ok("the session finishes", p.screen() === "done");

  const line = p.text("d-line");
  if (verbose) console.log("\n   " + line + "\n");
  const parsed = p.sandbox.window.BXP.parseLine(line);
  ok("the line parses under the lecturer view's own parser", !parsed.error, parsed.error);
  if (!parsed.error) {
    const [r1, r2] = parsed.rec.rounds;
    ok("round 1 is marked without the assistant", r1.agent === false);
    ok("round 2 is marked with it", r2.agent === true);
    ok("8 opens recorded in each round", r1.opened === 8 && r2.opened === 8);
    ok("round 1 did not move its sentence", r1.moved === false);
    ok("round 2 did", r2.moved === true);
    ok("round 2 changed sides", r2.side !== r2.endSide);
    ok("both rounds carry a workload total in 0-100", [r1.tlx, r2.tlx].every((t) => t >= 0 && t <= 100));
    ok("both rounds carry a perception total in 2-14", [r1.q, r2.q].every((q) => q >= 2 && q <= 14));
    ok("the two rounds used different claims", r1.claim !== r2.claim);
  }
  ok("the code is in the line and no name is", line.includes("|kite|") && !/name/i.test(line));
}

/* ---- resuming mid-session ---- */
{
  console.log("\nDA-1 — a reload keeps the place");
  const first = makePage();
  start(first, "resume", 6);              // team 6: the assistant is in round 1
  lockPosition(first, "disagree", "because.");
  first.set("f-agent-reply", "1. one 2. two 3. three");
  first.click("b-agent");
  for (let i = 0; i < 5; i++) first.click("b-pass");
  const saved = first.store.get("bxp-v1");
  const at = first.S().rounds[1].idx;

  // A reload is a page that starts with the key already written, so that is
  // exactly how it is built here.
  const again = makePage(saved);
  ok("a reload comes back on the card screen", again.screen() === "card", "screen is " + again.screen());
  ok(`a reload comes back on the same card (${at})`, again.S().rounds[1].idx === at);
  ok("the locked sentence is still locked", again.S().rounds[1].locked === "because.");
  ok("the pasted reply survives", again.S().rounds[1].agentReply.startsWith("1. one"));
  ok("the opens left are unchanged", again.S().rounds[1].opens === first.S().rounds[1].opens);
  ok("the order is unchanged", again.S().rounds[1].order.join() === first.S().rounds[1].order.join());
  ok("still 1 storage key after the reload", again.store.size === 1);
}

/* ---- SM-8: no answer key in the file that ships ---- */
{
  console.log("\nSM-8 — the published page carries no card's cell");
  // The cell codes themselves. If one of these is in the file, something has
  // put the codebook back.
  const cells = [...html.matchAll(/\b(NA|A)(S|W)[1-4]\b/g)].map((m) => m[0]);
  ok("0 cell codes in the file", cells.length === 0, cells.join(", "));

  // A card id within a short reach of anything that reads as a stance or a
  // quality. This is the check that catches an encoded key as well as a
  // written one, because the encoding still has to sit beside the id.
  const ids = [...html.matchAll(/\bc[12]-\d{2}\b/g)];
  const labelish = /\b(stance|quality|congenial|supporting|opposing|strong|weak|cell|denominator|agrees|disagrees|code[bd])/i;
  const near = ids.filter((m) => labelish.test(html.slice(m.index, m.index + 160))).map((m) => m[0]);
  ok("0 card ids sitting next to a stance or quality word", near.length === 0, near.join(", "));

  // And the deck records themselves carry only the six fields the contract
  // names. A seventh would be the key by another name.
  const page = makePage();
  const fields = new Set();
  for (const deck of [page.sandbox.DECK1, page.sandbox.DECK2]) {
    for (const card of deck) for (const k of Object.keys(card)) fields.add(k);
  }
  const allowed = ["id", "title", "ref", "teaser", "extract", "href"];
  const extra = [...fields].filter((f) => !allowed.includes(f));
  ok(`each card carries only ${allowed.join(", ")}`, extra.length === 0, "also found " + extra.join(", "));
  ok("32 cards across the two decks",
     page.sandbox.DECK1.length === 16 && page.sandbox.DECK2.length === 16);
}

/* ---- AG-1: nothing in the file can make a request ---- */
{
  console.log("\nAG-1 — no way for the page to call anywhere");
  const calls = ["fetch(", "XMLHttpRequest", "WebSocket", "sendBeacon", "EventSource",
                 "navigator.connection", "import(", "importScripts"];
  const found = calls.filter((c) => html.includes(c));
  ok("0 network calls anywhere in the shipped file", found.length === 0, found.join(", "));
  const external = [...html.matchAll(/<(script|link|img|iframe)\b[^>]*\b(src|href)="(https?:)?\/\/[^"]*"/g)];
  ok("0 external resources loaded by the page", external.length === 0,
     external.map((m) => m[0].slice(0, 60)).join(" | "));
}

console.log();
if (fails.length) {
  console.log(`${fails.length} failure(s):`);
  for (const f of fails) console.log("  " + f);
  process.exit(1);
}
console.log("Every session-level rule holds.");
