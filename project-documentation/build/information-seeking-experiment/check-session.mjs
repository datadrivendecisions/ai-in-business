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
const override = process.argv.slice(2).find((a) => a.endsWith(".html"));
const pagePath = override || join(here, "..", "..", "..", "site", "tool-bias-experiment.html");
const html = readFileSync(pagePath, "utf8");
const source = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
const verbose = process.argv.includes("-v");

/* The page ships with the service's address in it. Most checks here are about
   the session, not the service, so by default they run the page with that one
   value blanked -- the state the page is in whenever the service is switched
   off -- and the checks that are about the service set an origin of their own.
   makePage(..., { shipped: true }) runs the file exactly as published. */
const ORIGIN_LINE = /(var SERVICE = \{\s*origin:\s*)"[^"]*"/;
if (!ORIGIN_LINE.test(source)) throw new Error("cannot find SERVICE.origin in the page");
const SHIPPED_ORIGIN = source.match(ORIGIN_LINE)[0].match(/"([^"]*)"$/)[1];
const blankedSource = source.replace(ORIGIN_LINE, '$1""');

function makePage(initialStorage, { shipped = false } = {}) {
  const handlers = new Map();
  const nodes = new Map();
  const radios = new Map();
  const onChange = new Map();   // radio group name -> the page's change handlers
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
      // Enough of a radio group for setSide to clear or set it, and for
      // the page to hear a side being chosen.
      const listen = (ev, fn) => {
        if (ev !== "change") return;
        if (!onChange.has(m[1])) onChange.set(m[1], []);
        if (!onChange.get(m[1]).includes(fn)) onChange.get(m[1]).push(fn);
      };
      return [1, 2, 3, 4, 5, 6, 7].map((n) => ({
        addEventListener: listen,
        value: String(n),
        set checked(on) { if (on) radios.set(m[1], String(n)); },
        get checked() { return radios.get(m[1]) === String(n); },
      })).concat([
        { value: "agree", addEventListener: listen, set checked(on) { if (on) radios.set(m[1], "agree"); }, get checked() { return radios.get(m[1]) === "agree"; } },
        { value: "disagree", addEventListener: listen, set checked(on) { if (on) radios.set(m[1], "disagree"); }, get checked() { return radios.get(m[1]) === "disagree"; } },
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
    clearTimeout: () => {},
    confirm: () => true,
    scrollTo() {},
    /* No fetch by default. A page that reaches for one without a test
       having supplied it should fail loudly rather than silently do
       nothing, because "nothing happened" is also what a pass looks like. */
  };
  windowObj.window = windowObj;

  const sandbox = {
    window: windowObj, document, localStorage: windowObj.localStorage,
    navigator: windowObj.navigator, console,
    Math, Date, JSON, isFinite, Number, String, Object, Array, RegExp, Error,
    parseInt, parseFloat, setTimeout: () => 0, clearTimeout: () => {},
    Promise, AbortController,
  };
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(shipped ? source : blankedSource, sandbox, { filename: "tool-bias-experiment.html" });

  return {
    sandbox, store, radios, nodes,
    reloaded: () => reloaded,
    click(id) {
      const fn = handlers.get(id);
      if (!fn) throw new Error("no click handler on " + id);
      fn();
    },
    set(id, value) { document.getElementById(id).value = value; },
    pick(name, value) {
      radios.set(name, value);
      for (const fn of onChange.get(name) || []) fn();
    },
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
/* One whole session, consent to finish, opening the first `opens` cards of
   each round. Written once here because three checks now need it. */
function wholeSession(p, { code = "kite", team = 3, opens = 4 } = {}) {
  start(p, code, team);
  for (const round of [1, 2]) {
    lockPosition(p, "agree", "round " + round + " opening sentence.");
    if (p.screen() === "agent") {
      p.set("f-agent-reply", "1. What would change your mind? 2. What does the other side rest on? 3. What would have to hold?");
      p.click("b-agent");
    }
    for (let i = 0; i < 16; i++) {
      const before = p.S().rounds[round].opens;
      if (i < opens) p.click("b-open");
      p.click(p.S().rounds[round].opens > before ? "b-next" : "b-pass");
    }
    p.pick("fside", "agree");
    p.set("f-final", "round " + round + " closing sentence.");
    p.click("b-final");
    answerQuestions(p, 4);
    if (round === 1) p.click("b-bridge");
  }
  return p;
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

/* ---- AG-1: one origin, two routes, and no other way out ---- */
/* This check used to assert that the file contained no network call at all,
   and it passed for four phases. ADR-0016 then gave this one page a
   submission endpoint, and an assertion that something is absent turns into
   a requirement that it stay absent — which is not what AG-1 says and never
   was. AG-1 says the tool calls no origin other than the experiment
   service, using at most two routes.
   So the check now pins that concern: every way out of the page is
   enumerated, each one is accounted for, and the ways nothing here should
   ever use are still forbidden outright. */
{
  console.log("\nAG-1 — one origin, two routes, and no other way out");

  const forbidden = ["XMLHttpRequest", "WebSocket", "sendBeacon", "EventSource",
                     "importScripts", "navigator.connection"];
  const found = forbidden.filter((c) => html.includes(c));
  ok("0 uses of a transport this page has no business having", found.length === 0,
     found.join(", "));

  // Every fetch in the file, and what it is aimed at.
  const fetches = [...html.matchAll(/fetch\s*\(\s*([^,)]+)/g)].map((m) => m[1].trim());
  ok("every request is built from SERVICE.origin, all " + fetches.length + " of them",
     fetches.length > 0 && fetches.every((f) => f.startsWith("SERVICE.origin")),
     fetches.join(" | "));

  // The routes named in the config, and the ones actually reached for.
  const page = makePage();
  const service = page.sandbox.SERVICE;
  const routes = Object.keys(service).filter((k) => k !== "origin" && k !== "timeoutMs");
  ok("the config names at most 2 routes: " + routes.join(", "), routes.length <= 2,
     routes.join(", "));
  // Since the service was deployed the page names it. What must hold is that
  // it names exactly one host, over https, and that host is a Cloud Run one.
  ok("the page names one service address, https, on Cloud Run",
     /^https:\/\/[a-z0-9-]+(\.[a-z0-9-]+)*\.run\.app$/.test(SHIPPED_ORIGIN), JSON.stringify(SHIPPED_ORIGIN));
  const shippedPage = makePage(undefined, { shipped: true });
  ok("serviceOn() is true in the page as published", shippedPage.sandbox.serviceOn() === true);
  ok("serviceOn() is false with the address blanked", page.sandbox.serviceOn() === false);

  // An absolute URL anywhere in the script would be a second origin by
  // another name. The deck's card links are markup-free data and open in a
  // new tab; they are not requests this page makes.
  const script = html.slice(html.indexOf("<script>"));
  const cardHrefs = new Set([...page.sandbox.DECK1, ...page.sandbox.DECK2].map((c) => c.href));
  const urls = [...script.matchAll(/["'](https?:\/\/[^"']+)["']/g)]
    .map((m) => m[1]).filter((u) => !cardHrefs.has(u) && u !== SHIPPED_ORIGIN);
  ok("0 hard-coded origins in the script beyond the card links and the one service",
     urls.length === 0, urls.join(" | "));

  const external = [...html.matchAll(/<(script|link|img|iframe)\b[^>]*\b(src|href)="(https?:)?\/\/[^"]*"/g)];
  ok("0 external resources loaded by the page", external.length === 0,
     external.map((m) => m[0].slice(0, 60)).join(" | "));
}

/* ---- SV-1, SV-2: what is sent, and only when it is asked for ---- */
{
  console.log("\nSV-1, SV-2 — what is sent, and only on a press");

  const p = makePage();
  const calls = [];
  p.sandbox.SERVICE.origin = "https://experiment.example";
  p.sandbox.window.fetch = (url, opts) => { calls.push({ url, opts }); return Promise.resolve({
    ok: true, json: () => Promise.resolve({ stored: true, count: 1 }) }); };

  wholeSession(p, { code: "kite", team: 3, opens: 4 });
  ok("0 requests across a complete two-round session", calls.length === 0, String(calls.length));
  ok("the session ends on the submit screen, which asks", p.screen() === "submit", p.screen());
  ok("nothing is marked as sent yet", p.S().sent === false, JSON.stringify(p.S().sent));

  p.click("b-submit");
  ok("1 request after 1 press", calls.length === 1, String(calls.length));
  ok("it goes to the one origin and the one route",
     calls[0] && calls[0].url === "https://experiment.example/submit", calls[0] && calls[0].url);

  const body = JSON.parse(calls[0].opts.body);
  const flat = JSON.stringify(body);
  ok("0 of the student's sentences anywhere in the body",
     !flat.includes("opening sentence") && !flat.includes("closing sentence")
     && !flat.includes("What would change your mind"), flat.slice(0, 160));
  ok("the body carries exactly v, code, team, rounds",
     JSON.stringify(Object.keys(body).sort()) === JSON.stringify(["code", "rounds", "team", "v"]),
     Object.keys(body).join(","));
  const roundKeys = Object.keys(body.rounds[0]).sort().join(",");
  ok("a round carries exactly the 11 fields the schema names",
     roundKeys === "agent,claim,endSide,moved,n,opened,pick,q,seconds,side,tlx", roundKeys);
  ok("4 opened cards in round 1, matching the session",
     body.rounds[0].opened.length === 4, String(body.rounds[0].opened.length));
  ok("the assistant is marked in exactly one round",
     body.rounds[0].agent !== body.rounds[1].agent);

  await new Promise((r) => setTimeout(r, 0));   // the send settles, the finish renders
  ok("a successful send is marked as sent", p.S().sent === true, JSON.stringify(p.S().sent));
  ok("and the finish screen is reached", p.screen() === "done", p.screen());

  // The line and the payload are built from the same records, and a check
  // that they agree is what stops the two drifting apart later.
  const parsed = p.sandbox.window.BXP.parseLine(p.text("d-line"));
  ok("the line and the payload describe the same session",
     !parsed.error
     && parsed.rec.code === body.code && parsed.rec.team === body.team
     && parsed.rec.rounds[0].ids.join() === body.rounds[0].opened.join()
     && parsed.rec.rounds[1].ids.join() === body.rounds[1].opened.join(),
     parsed.error || "");
}

/* ---- SV-6: the service is down and the session finishes anyway ---- */
{
  console.log("\nSV-6 — the service is down, and nothing is blocked");

  const failures = [
    ["the request is refused",     (p) => { p.sandbox.window.fetch = () => Promise.reject(new Error("offline")); }],
    ["the service answers 500",    (p) => { p.sandbox.window.fetch = () => Promise.resolve({ ok: false, status: 500 }); }],
    ["the service answers 401",    (p) => { p.sandbox.window.fetch = () => Promise.resolve({ ok: false, status: 401 }); }],
    ["the request never settles",  (p) => {
      // The one failure the others cannot show: a service that accepts the
      // connection and then says nothing. The timeout is what rescues the
      // student here, so the stub's clock is made to fire.
      p.sandbox.window.fetch = () => new Promise(() => {});
      p.sandbox.window.setTimeout = (fn) => { fn(); return 0; };
    }],
    ["there is no fetch at all",   (p) => { delete p.sandbox.window.fetch; }],
  ];

  let finished = 0, lines = 0;
  for (let i = 0; i < 10; i++) {
    const [, arrange] = failures[i % failures.length];
    const p = makePage();
    p.sandbox.SERVICE.origin = "https://experiment.example";
    arrange(p);

    wholeSession(p, { code: "s" + i, team: (i % 8) + 1, opens: 3 });
    p.click("b-submit");
    await new Promise((r) => setTimeout(r, 0));   // let the rejection land

    if (p.screen() === "done") finished += 1;
    const line = p.text("d-line");
    if (!p.sandbox.window.BXP.parseLine(line).error) lines += 1;
    if (p.S().sent !== false) ok("session " + i + " wrongly marked as sent", false);
  }
  ok("10 of 10 sessions finish with the service unreachable", finished === 10, String(finished));
  ok("10 of 10 still produce a line the lecturer view can read", lines === 10, String(lines));

  // And the copy button is where it was.
  const p = makePage();
  p.sandbox.SERVICE.origin = "https://experiment.example";
  p.sandbox.window.fetch = () => Promise.reject(new Error("offline"));
  wholeSession(p, { code: "reed", team: 2, opens: 5 });
  p.click("b-submit");
  await new Promise((r) => setTimeout(r, 0));
  p.click("b-copy-line");
  ok("the copy button still works after a failed send", true);
  ok("the screen says what happened, in words", p.text("d-status-text").length > 40,
     p.text("d-status-text"));

  /* Not a failure, and pinned here so it is not later mistaken for one: a
     200 whose body will not parse means the service stored the submission
     and only the count came back unreadable. Treating that as a failure
     would invite a second send of a row that is already there. */
  const q = makePage();
  q.sandbox.SERVICE.origin = "https://experiment.example";
  q.sandbox.window.fetch = () => Promise.resolve({ ok: true, json: () => Promise.reject(new Error("nope")) });
  wholeSession(q, { code: "brack", team: 5, opens: 4 });
  q.click("b-submit");
  await new Promise((r) => setTimeout(r, 0));
  ok("a 200 with an unreadable body still counts as sent", q.S().sent === true,
     JSON.stringify(q.S().sent));
}

/* ---- the page as published: the submit screen, and the consent that says so ---- */
{
  console.log("\nThe page as published — a service to send to");
  const p = makePage(undefined, { shipped: true });
  let touched = 0;
  p.sandbox.window.fetch = () => { touched += 1; return new Promise(() => {}); };
  wholeSession(p, { code: "live", team: 2, opens: 2 });
  ok("the session ends on the submit screen, not the copy-your-line finish", p.screen() === "submit", p.screen());
  ok("0 requests before the button is pressed", touched === 0, String(touched));
  ok("the consent screen says numbers may be sent, and sentences never",
     /choose whether to send your numbers/.test(p.text("storage-statement"))
     && /sentences never leave/.test(p.text("storage-statement")), p.text("storage-statement"));
}

/* ---- the switched-off page: no service, no request, the phase 5 finish ---- */
{
  console.log("\nWith SERVICE.origin blanked — no request is even attempted");
  const p = makePage();
  let touched = 0;
  p.sandbox.window.fetch = () => { touched += 1; return Promise.reject(new Error("x")); };
  wholeSession(p, { code: "unset", team: 6, opens: 2 });
  ok("the session goes straight to the finish", p.screen() === "done", p.screen());
  ok("0 requests attempted", touched === 0, String(touched));
  ok("the consent screen promised nothing would leave",
     p.text("storage-statement").includes("sent nowhere"), p.text("storage-statement"));
}

/* ---- SV-9, SV-10, AN-2: the dashboard and what it is allowed to say ---- */
{
  console.log("\nSV-9, SV-10, AN-2 — the dashboard and the sentences it may say");
  const B = makePage().sandbox.window.BXP;

  // SV-9: a fixed set, and every sentence that appears is one of them.
  const regions = [
    ["interval entirely below zero", { n: 20, lo: -0.40, hi: -0.10, mdeUnits: 0.30, sdDiff: 0.5 }],
    ["interval entirely above zero", { n: 20, lo: 0.10, hi: 0.40, mdeUnits: 0.30, sdDiff: 0.5 }],
    ["interval spanning zero",       { n: 20, lo: -0.40, hi: 0.40, mdeUnits: 0.30, sdDiff: 0.5 }],
  ];
  const chosen = regions.map(([, st]) => B.chooseInterpretation(st));
  ok("3 fixtures produce 3 chosen sentences", chosen.every(Boolean),
     JSON.stringify(chosen.map((c) => c && c.pick.id)));
  ok("3 different sentences, 0 repeats",
     new Set(chosen.map((c) => c.pick.id)).size === 3,
     chosen.map((c) => c.pick.id).join(", "));

  /* Every stored sentence must be reachable. A template nobody can select
     reads like a case the page handles and is dead code — which is what the
     fourth one was: an interval narrower than the smallest detectable effect
     cannot happen, because a 95% interval is about 1.4 times that width at
     every sample size, both being fixed multiples of the same standard
     error. This check is here so the next one added has to prove it can
     appear. */
  const seen = new Set();
  const sd = 0.5;
  // Sample sizes rather than every integer: detectableEffect solves a
  // non-central t numerically, and the regions turn on the sign structure of
  // the interval, which does not hide between n = 41 and n = 42.
  for (const n of [3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 64, 100, 200, 500]) {
    const half = B.tinv(0.975, n - 1) * sd / Math.sqrt(n);
    const mde = B.detectableEffect(n) * sd;
    for (const centre of [-2, -1, -0.3, -0.05, 0, 0.05, 0.3, 1, 2]) {
      const c = B.chooseInterpretation({ n, lo: centre - half, hi: centre + half,
                                         mdeUnits: mde, sdDiff: sd });
      if (c) seen.add(c.pick.id);
    }
  }
  ok(`all ${B.INTERPRETATIONS.length} stored sentences are reachable by some real summary`,
     seen.size === B.INTERPRETATIONS.length,
     "reachable: " + [...seen].join(", ") + " of " + B.INTERPRETATIONS.map((t) => t.id).join(", "));
  ok("every one comes out of the stored set, 0 composed",
     chosen.every((c) => B.INTERPRETATIONS.indexOf(c.pick) >= 0));
  ok("the rendered text is the template's own output, character for character",
     chosen.every((c) => c.pick.text(c.numbers) === c.pick.text(c.numbers)
                      && typeof c.pick.text(c.numbers) === "string"));

  // SV-10: nothing renders without both governing numbers.
  const crippled = [
    ["no interval low end",  { n: 20, lo: null, hi: 0.4, mdeUnits: 0.3, sdDiff: 0.5 }],
    ["no interval high end", { n: 20, lo: -0.4, hi: null, mdeUnits: 0.3, sdDiff: 0.5 }],
    ["no detectable effect", { n: 20, lo: -0.4, hi: 0.4, mdeUnits: null, sdDiff: 0.5 }],
    ["a NaN detectable effect", { n: 20, lo: -0.4, hi: 0.4, mdeUnits: NaN, sdDiff: 0.5 }],
    ["an infinite interval", { n: 20, lo: -Infinity, hi: 0.4, mdeUnits: 0.3, sdDiff: 0.5 }],
    ["one pair",             { n: 1 }],
    ["no pairs",             { n: 0 }],
  ];
  const rendered = crippled.filter(([, st]) => B.chooseInterpretation(st) !== null);
  ok("7 summaries missing a governing number, 0 render a sentence",
     rendered.length === 0, rendered.map((r) => r[0]).join(", "));

  // AN-3 still governs the set: none of them states a finding.
  const verdicts = [
    "the assistant reduced", "the assistant increased", "proves", "shows that",
    "we can conclude", "therefore the assistant", "confirms", "demonstrates that",
    "students who used", "the effect is real", "significant effect of",
  ];
  const offending = [];
  for (const t of B.INTERPRETATIONS) {
    const text = t.text({ pairs: 20, loText: "−0.100", hiText: "0.100", mdeText: "0.300",
                          lo: -0.1, hi: 0.1, mde: 0.3, widerThanDetectable: true }).toLowerCase();
    for (const v of verdicts) if (text.includes(v)) offending.push(t.id + ": " + v);
  }
  ok(`${B.INTERPRETATIONS.length} stored sentences, 0 carrying a verdict phrase`,
     offending.length === 0, offending.join(" | "));
  ok("every stored sentence names what the data cannot do",
     B.INTERPRETATIONS.every((t) => {
       const text = t.text({ pairs: 20, loText: "a", hiText: "b", mdeText: "c",
                             lo: -1, hi: 1, mde: 0.3, widerThanDetectable: true }).toLowerCase();
       return /does not|cannot|nothing follows|rules out|remains on the table|not rule out/.test(text);
     }));

  // AN-2: the live path and the paste path are the same arithmetic, not two
  // implementations that happen to agree. Build records, turn them into the
  // rows the service would hold, turn those back, and compare the summary.
  const book = {};
  const cells = [["A", "S"], ["A", "W"], ["NA", "S"], ["NA", "W"]];
  for (const claim of [1, 2]) {
    for (let i = 1; i <= 16; i++) {
      const [stance, quality] = cells[(i - 1) % 4];
      book[`c${claim}-${String(i).padStart(2, "0")}`] = { stance, quality };
    }
  }
  const rnd = (() => { let x = 12345; return () => (x = (x * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff; })();
  const records = [];
  for (let p = 0; p < 24; p++) {
    const mk = (n, claim, agent) => {
      const k = 2 + Math.floor(rnd() * 7);
      const ids = [];
      while (ids.length < k) {
        const id = `c${claim}-${String(1 + Math.floor(rnd() * 16)).padStart(2, "0")}`;
        if (!ids.includes(id)) ids.push(id);
      }
      return { round: n, agent, claim: "c" + claim, side: rnd() < 0.5 ? "agree" : "disagree",
               pick: 5 + Math.floor(rnd() * 80), opened: ids.length, ids, secs: 60 + Math.floor(rnd() * 200),
               endSide: rnd() < 0.5 ? "agree" : "disagree", moved: rnd() < 0.5,
               tlx: Math.floor(rnd() * 101), q: 2 + Math.floor(rnd() * 13) };
    };
    const agentFirst = p % 2 === 0;
    records.push({ code: "p" + p, team: (p % 8) + 1,
                   rounds: [mk(1, 1, agentFirst), mk(2, 2, !agentFirst)] });
  }

  // The shape the service stores, built from the same records.
  const asRows = records.map((rec) => ({
    id: rec.code, team: rec.team, at: 1,
    rounds: rec.rounds.map((r) => ({
      n: r.round, agent: r.agent, claim: Number(r.claim.slice(1)),
      side: r.side === "agree" ? "a" : "d", pick: r.pick, opened: r.ids.slice(), seconds: r.secs,
      endSide: r.endSide === "agree" ? "a" : "d", moved: r.moved, tlx: r.tlx, q: r.q,
    })),
  }));
  const viaLive = asRows.map((row) => B.recordFromRow(row));
  ok("the seconds to a side survive the trip through the service's rows",
     viaLive.every((rec, i) => rec.rounds.every((r, j) => r.pick === records[i].rounds[j].pick)));
  const auPasted = B.pilotAudit(records, null), auLive = B.pilotAudit(viaLive, null);
  ok("the pilot audit reads the same from the live feed as from the paste box",
     JSON.stringify(auPasted.rows) === JSON.stringify(auLive.rows));

  const pasted = B.summarise(B.pairUp(records, book).pairs);
  const live = B.summarise(B.pairUp(viaLive, book).pairs);

  const keys = Object.keys(pasted).filter((k) => typeof pasted[k] === "number");
  const off = keys.filter((k) => {
    const a = pasted[k], b = live[k];
    return !(a === b || (a !== null && b !== null && Math.abs(a - b) < 5e-4));
  });
  ok(`${keys.length} figures, live feed against paste box, all equal to 3 dp on 24 pairs`,
     off.length === 0 && pasted.n === 24, off.join(", ") + " n=" + pasted.n);
  ok("and the same sentence is selected from both",
     B.chooseInterpretation(pasted).pick.id === B.chooseInterpretation(live).pick.id);

  // A row the service could not have produced is listed, not silently dropped.
  const strayRow = {
    id: "x", team: 1, at: 1,
    rounds: [
      { n: 1, agent: true, claim: 1, side: "a", pick: 1, opened: ["c1-99"], seconds: 1,
        endSide: "a", moved: false, tlx: 1, q: 2 },
      { n: 2, agent: false, claim: 2, side: "a", pick: 1, opened: ["c2-01"], seconds: 1,
        endSide: "a", moved: false, tlx: 1, q: 2 },
    ],
  };
  const strayResult = B.pairUp([B.recordFromRow(strayRow)], book);
  ok("a row with an unknown card id is listed as dropped, not absorbed",
     strayResult.pairs.length === 0 && strayResult.dropped.length === 1,
     JSON.stringify(strayResult.dropped));
}

/* ---- CL-10: the seconds to a side ---- */
{
  console.log("\nCL-10 — the time to choose a side, not to lock it");
  const busy = (ms) => { const until = Date.now() + ms; while (Date.now() < until) { /* a real wait */ } };
  const p = makePage();
  start(p, "clock2", 5);
  busy(700);
  p.pick("side", "disagree");     // the side is chosen here...
  busy(1400);
  p.set("f-position", "because.");
  p.click("b-position");          // ...and locked after the sentence is written
  const ms = p.S().rounds[1].pickMs;
  ok(`the clock stops at the choice, not the lock (${ms} ms for a side chosen at 700 ms and locked at 2100)`,
     ms >= 650 && ms < 1100, String(ms));

  const q = makePage();
  start(q, "clock3", 5);
  busy(300);
  q.pick("side", "agree");
  busy(300);
  q.pick("side", "disagree");     // a change of mind moves the clock to the last choice
  q.set("f-position", "because.");
  q.click("b-position");
  const ms2 = q.S().rounds[1].pickMs;
  ok(`a second choice restarts nothing and counts to itself (${ms2} ms)`, ms2 >= 550 && ms2 < 900, String(ms2));

  wholeSession(q, { code: "clock3", team: 5, opens: 2 });
  const parsed = q.sandbox.window.BXP.parseLine(q.text("d-line"));
  ok("the line carries the seconds to a side, and parses", !parsed.error && typeof parsed.rec.rounds[0].pick === "number",
     parsed.error || q.text("d-line").slice(0, 80));
}

/* ---- Phase 0: the pilot audit, wired ---- */
{
  console.log("\nPhase 0 — the pilot audit fills in from the lines and the coders");
  const cells = [["A", "S"], ["A", "W"], ["NA", "S"], ["NA", "W"]];
  const text = [];
  for (const claim of [1, 2]) {
    for (let i = 1; i <= 16; i++) {
      const [stance, quality] = cells[(i - 1) % 4];
      text.push(`| c${claim}-${String(i).padStart(2, "0")} | ${stance}${quality} |`);
    }
  }
  const lines = [];
  for (let i = 0; i < 12; i++) {
    const s = wholeSession(makePage(), { code: "au" + i, team: (i % 8) + 1, opens: 3 });
    lines.push(s.text("d-line"));
  }
  const p = makePage();
  ok("before anything arrives, all 7 criteria are open", p.text("au-open") === "7" && p.text("au-met") === "0",
     `${p.text("au-met")}/${p.text("au-missed")}/${p.text("au-open")}`);

  p.set("f-codebook", text.join("\n"));
  p.set("f-lines", lines.join("\n"));
  p.click("b-analyse");
  // Every one of the twelve agreed, so CL-1 misses twice, CL-7 is met (0
  // points apart), CL-10 is met twice (no clock ran), CL-5 waits.
  const t1 = `${p.text("au-met")}/${p.text("au-missed")}/${p.text("au-open")}`;
  ok("12 pasted lines: 3 met, 2 not met, 2 open", t1 === "3/2/2", t1);

  p.set("f-coder1", text.join("\n"));
  p.set("f-coder2", text.join("\n"));
  p.click("b-coders");
  const t2 = `${p.text("au-met")}/${p.text("au-missed")}/${p.text("au-open")}`;
  ok("two identical codebooks close CL-5 for both decks: 5 met, 2 not met, 0 open", t2 === "5/2/0", t2);

  p.set("f-coder2", "");
  p.click("b-coders");
  ok("an empty second codebook is refused, and CL-5 goes back to open",
     !p.nodes.get("e-audit").hidden && p.text("au-open") === "2", p.text("au-open"));
}

console.log();
if (fails.length) {
  console.log(`${fails.length} failure(s):`);
  for (const f of fails) console.log("  " + f);
  process.exit(1);
}
console.log("Every session-level rule holds.");
