/* Runs site/tool-bias-experiment.html's own script outside a browser, so the
   fixtures are checked against the code that actually ships rather than
   against a copy of it that can drift.
   
   The stub below is not a DOM. It is the smallest object that lets the page's
   top-level code finish without throwing: every element answers every call and
   remembers nothing. The page's arithmetic touches none of it — that is the
   point of keeping those functions pure — so a stub is enough to reach them,
   and anything that genuinely needs a browser is tested in one instead.
   
   Usage:  node runpage.mjs <fixtures.json>   → results on stdout as JSON */

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import vm from "node:vm";

const here = dirname(fileURLToPath(import.meta.url));
const pagePath = join(here, "..", "..", "..", "site", "tool-bias-experiment.html");
const html = readFileSync(pagePath, "utf8");

/* The page carries two script blocks: its own, and the instructor-view block
   copied verbatim from index.html. The first is the one with the arithmetic. */
const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
if (blocks.length < 1) throw new Error("no script block found in the page");
const source = blocks[0];

function el() {
  const node = {
    style: {}, classList: { add() {}, remove() {} },
    textContent: "", value: "", href: "", hidden: false, checked: false,
    disabled: false, type: "", name: "",
    addEventListener() {}, appendChild() {}, removeChild() {}, focus() {},
    select() {}, setAttribute() {}, removeAttribute() {},
    querySelector: () => el(), querySelectorAll: () => [],
  };
  node.parentNode = { hidden: false };
  return node;
}

const byId = new Map();
const store = new Map();

const document = {
  getElementById(id) {
    if (!byId.has(id)) byId.set(id, el());
    return byId.get(id);
  },
  createElement: () => el(),
  querySelector: () => null,
  querySelectorAll: () => [],
  body: el(),
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
  location: { search: "", reload() {} },
  setTimeout: () => 0,
  confirm: () => false,
  scrollTo() {},
  Math, Date, JSON, isFinite, Number, String, Object, Array,
};
windowObj.window = windowObj;

const sandbox = {
  window: windowObj,
  document,
  localStorage: windowObj.localStorage,
  navigator: windowObj.navigator,
  console,
  Math, Date, JSON, isFinite, Number, String, Object, Array, RegExp, Error,
  parseInt, parseFloat, setTimeout: () => 0,
};
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(source, sandbox, { filename: "tool-bias-experiment.html" });

const BXP = sandbox.window.BXP;
if (!BXP) throw new Error("the page did not expose window.BXP");

const fixtures = JSON.parse(readFileSync(process.argv[2], "utf8"));
const book = BXP.parseCodebook(fixtures.codebookText);

const out = { codebookCards: book.n, measures: [], totals: [], datasets: [], kappas: [], prompt: null };

/* MS-1, MS-2: one round's numbers from a known set of opens. */
for (const m of fixtures.measures) {
  const r = BXP.roundIndex({ ids: m.ids, side: m.side }, book.map);
  out.measures.push({
    name: m.name, opened: r.opened, congenial: r.congenial,
    uncongenial: r.uncongenial, strongOpposing: r.strongOpposing, index: r.index,
  });
}

/* MS-6 arithmetic: the two closing totals. */
for (const t of fixtures.totals) {
  out.totals.push({ name: t.name, tlx: BXP.tlxTotal(t.answers), q: BXP.perceptionTotal(t.answers) });
}

/* AN-1, AN-2, AN-4, AN-6: a whole class at a time. */
for (const d of fixtures.datasets) {
  const accepted = [], rejected = [];
  for (const [i, raw] of d.lines.entries()) {
    if (!raw.trim()) continue;
    const p = BXP.parseLine(raw);
    if (p.error) rejected.push({ n: i + 1, why: p.error });
    else accepted.push(p.rec);
  }
  const up = BXP.pairUp(accepted, book.map);
  const st = BXP.summarise(up.pairs);
  out.datasets.push({
    name: d.name, accepted: accepted.length, rejected: rejected.length,
    rejectReasons: rejected, dropped: up.dropped.length, pairs: up.pairs.length,
    meanAsk: st.meanAsk ?? null, meanNone: st.meanNone ?? null,
    diff: st.diff ?? null, sdDiff: st.sdDiff ?? null,
    lo: st.lo ?? null, hi: st.hi ?? null, tcrit: st.tcrit ?? null,
    dz: st.dz ?? null, mdeUnits: st.mdeUnits ?? null,
  });
}

/* AN-5, AN-7. */
for (const k of fixtures.kappas) {
  const r = BXP.kappa2x2(k.a, k.b, k.c, k.d);
  out.kappas.push({ name: k.name, n: r.n, po: r.po, pe: r.pe, kappa: r.kappa ?? null });
}

/* AG-2, AG-4, AG-5: the prompt as it is actually built. */
out.prompt = BXP.agentPrompt(fixtures.promptClaim, fixtures.promptSide, fixtures.promptLocked);

/* SM-2, SM-3, SM-4, SM-9 and the line format all need the runner rather than
   the arithmetic, so they are checked in a browser, not here. */
process.stdout.write(JSON.stringify(out, null, 1));
