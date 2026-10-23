"use strict";
// All model and book text goes in through textContent, never innerHTML.
const $ = (id) => document.getElementById(id);
function h(tag, props, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(props || {})) {
    if (k === "class") el.className = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v);
  }
  for (const kid of kids.flat()) if (kid != null) el.append(kid);
  return el;
}
async function api(path, body) {
  const opts = body === undefined ? {} : {
    method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)};
  const res = await fetch(path, opts);
  const data = await res.json().catch(() => ({error: "bad response"}));
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}
const clear = (el) => el.replaceChildren();
const errBox = (e) => h("p", {class: "verdict bad"}, e.message || String(e));
let INFO = null;

// ---- tabs ----------------------------------------------------------------
function showTab(name) {
  for (const b of document.querySelectorAll("#tabs button"))
    b.setAttribute("aria-selected", String(b.dataset.tab === name));
  for (const p of document.querySelectorAll(".panel")) p.hidden = p.id !== name;
  if (name === "progress") loadProgress();
}
$("tabs").addEventListener("click", (e) => { if (e.target.dataset.tab) showTab(e.target.dataset.tab); });

// ---- selects ---------------------------------------------------------------
function label(src, ch) {
  if (src === "sheet") return `Simulation: ${ch}`;
  if (src === "book") return /^\d+$/.test(ch) ? `Book chapter ${ch}` : `Book ${ch}`;
  return `Guide ${ch}`;
}
function fillSource(sel, withBoth = true) {
  clear(sel);
  const names = INFO.sources;
  if (withBoth && names.length > 1) sel.append(h("option", {value: "both"}, "Book and guide"));
  for (const s of names) sel.append(h("option", {value: s}, s === "book" ? "Book" : "Guide"));
}
function fillChapters(chSel, srcSel, list) {
  clear(chSel);
  chSel.append(h("option", {value: ""}, "All chapters"));
  for (const c of list)
    if (srcSel.value === "both" || srcSel.value === c.source)
      chSel.append(h("option", {value: c.chapter}, label(c.source, c.chapter)));
}
function link(srcSel, chSel, listFn) {
  const refresh = () => fillChapters(chSel, srcSel, listFn());
  srcSel.addEventListener("change", refresh);
  refresh();
  return refresh;
}

// ---- rendering a question --------------------------------------------------
function letter(i) { return "ABCDEFGH"[i]; }
function questionCard(item, opts) {
  // opts.instant: answer on click (single pick); opts.onChange(selected Set); returns {el, selected, reveal}
  const selected = new Set();
  const buttons = item.choices.map((text, i) => h("button", {type: "button", class: "choice"},
    h("b", {}, letter(i) + "."), h("span", {}, text)));
  const card = h("div", {class: "card"},
    h("p", {class: "q"}, item.question),
    item.pick > 1 ? h("p", {class: "muted"}, `Choose ${item.pick}.`) : null,
    buttons, h("div", {class: "feedback"}));
  let locked = false;
  buttons.forEach((b, i) => b.addEventListener("click", () => {
    if (locked) return;
    if (item.pick === 1) { selected.clear(); selected.add(i); } else if (selected.has(i)) selected.delete(i); else selected.add(i);
    buttons.forEach((x, j) => x.classList.toggle("picked", selected.has(j)));
    if (opts.onChange) opts.onChange(selected);
  }));
  return {
    el: card, selected, lock() { locked = true; },
    reveal(res) {
      locked = true;
      buttons.forEach((b, i) => {
        b.classList.remove("picked");
        if (res.answer.includes(i)) b.classList.add("right");
        else if (res.chosen.includes(i)) b.classList.add("wrong");
      });
      const fb = card.querySelector(".feedback");
      clear(fb);
      fb.append(h("p", {class: "verdict " + (res.correct ? "ok" : "bad")},
        res.correct ? "Correct." : `${res.chosen.length ? "Not quite" : "Not answered"}. The answer is ${res.answer.map(letter).join(", ")}.`));
      if (res.explanation) fb.append(h("p", {class: "answer"}, res.explanation));
      if (res.evidence) fb.append(h("blockquote", {}, `“${res.evidence}”`));
      fb.append(h("p", {class: "src"}, res.ref));
    },
  };
}

// ---- ask -------------------------------------------------------------------
async function onAsk(e) {
  e.preventDefault();
  const out = $("ask-out");
  clear(out);
  out.append(h("p", {class: "spin"}, "Searching and answering…"));
  try {
    const r = await api("/api/ask", {question: $("ask-q").value, source: $("ask-source").value,
                                      chapter: $("ask-chapter").value});
    clear(out);
    out.append(h("div", {class: "card"}, h("p", {class: "answer"}, r.answer),
      r.cites.length ? h("p", {class: "src"}, "Sources") : null,
      r.cites.map((c) => h("div", {}, h("span", {class: "cite"}, `[${c.n}]`), `${c.ref} `, h("span", {class: "src"}, `(${c.source})`)))));
  } catch (err) { clear(out); out.append(errBox(err)); }
}

// ---- drill -----------------------------------------------------------------
const drill = {tally: [0, 0], last: null};
async function drillNext() {
  const out = $("drill-out");
  const gen = $("drill-kind").value === "gen";
  const weak = $("drill-mode").value === "weak";
  clear(out);
  out.append(h("p", {class: "spin"}, gen ? "Writing a question from the book…" : "Picking a question…"));
  let r;
  try {
    r = gen
      ? await api("/api/quiz/next", {source: $("drill-source").value, chapter: $("drill-chapter").value,
                                     topic: $("drill-topic").value, weak})
      : await api("/api/bank/next", {source: $("drill-source").value, chapter: $("drill-chapter").value,
                                     mode: $("drill-mode").value, after: drill.last});
  } catch (err) { clear(out); out.append(errBox(err)); return; }
  clear(out);
  if (!r.item) {
    out.append(h("p", {}, "No more questions match those settings."), scoreLine());
    return;
  }
  const item = r.item;
  drill.last = item.id;
  const q = questionCard(item, {onChange(sel) { if (item.pick > 1) check.disabled = sel.size !== item.pick; if (item.pick === 1) submit(); }});
  const check = h("button", {type: "button", class: "primary", disabled: ""}, "Check");
  const next = h("button", {type: "button", class: "primary"}, "Next question");
  let done = false;
  async function submit() {
    if (done) return;
    done = true;
    q.lock();
    try {
      const res = await api("/api/answer", {id: item.id, choice: [...q.selected], kind: "drill"});
      drill.tally[0] += 1; drill.tally[1] += res.correct ? 1 : 0;
      q.reveal(res);
      check.remove();
      out.append(next, scoreLine());
    } catch (err) { out.append(errBox(err)); }
  }
  check.addEventListener("click", submit);
  next.addEventListener("click", drillNext);
  out.append(q.el);
  if (item.pick > 1) out.append(check);
}
function scoreLine() { return h("p", {class: "muted"}, `This session: ${drill.tally[1]} of ${drill.tally[0]} correct.`); }

// ---- practice test -----------------------------------------------------------
const test = {timer: null};
async function onTest(e) {
  e.preventDefault();
  const out = $("test-out");
  clear(out);
  let r;
  try {
    r = await api("/api/test/start", {n: +$("test-n").value, source: $("test-source").value, chapter: $("test-chapter").value});
  } catch (err) { out.append(errBox(err)); return; }
  const answers = {};
  const cards = r.items.map((item, i) => {
    const c = questionCard(item, {onChange(sel) { answers[item.id] = [...sel]; refreshCount(); }});
    c.el.prepend(h("p", {class: "src"}, `Question ${i + 1} of ${r.items.length}`));
    return c;
  });
  const count = h("span", {class: "muted"});
  const clock = h("span", {class: "timer"});
  const finish = h("button", {type: "button", class: "primary"}, "Finish test");
  const bar = h("div", {class: "row"}, finish, count, clock);
  function refreshCount() { count.textContent = `${Object.values(answers).filter((a) => a.length).length} of ${r.items.length} answered`; }
  refreshCount();
  let over = false;
  async function end() {
    if (over) return;
    over = true;
    clearInterval(test.timer);
    cards.forEach((c) => c.lock());
    try { showResults(await api("/api/test/finish", {test: r.test, answers})); }
    catch (err) { out.append(errBox(err)); }
  }
  finish.addEventListener("click", end);
  const minutes = +$("test-min").value;
  if (minutes > 0) {
    let left = minutes * 60;
    const tick = () => {
      clock.textContent = `${Math.floor(left / 60)}:${String(left % 60).padStart(2, "0")} left`;
      if (left-- <= 0) end();
    };
    tick();
    test.timer = setInterval(tick, 1000);
  }
  out.append(bar, cards.map((c) => c.el), h("div", {class: "row"}, finish.cloneNode(true)));
  out.lastChild.firstChild.addEventListener("click", end);
}
function showResults(r) {
  const out = $("test-out");
  clear(out);
  const pct = Math.round((100 * r.right) / r.total);
  out.append(h("div", {class: "card"},
    h("p", {class: "q"}, `${r.right} of ${r.total} correct (${pct}%) in ${Math.floor(r.seconds / 60)} min ${r.seconds % 60} s`),
    chapterTable(r.by_chapter)));
  r.results.forEach((res, i) => {
    const item = {question: `${i + 1}. ${res.question}`, choices: res.choices, pick: res.answer.length};
    const c = questionCard(item, {});
    c.reveal(res);
    out.append(c.el);
  });
}

// ---- simulations -------------------------------------------------------------
const sim = {sheets: 0, perfect: 0, parts: [0, 0]};
async function simNew() {
  const out = $("sim-out");
  clear(out);
  let sheet;
  try { ({sheet} = await api("/api/sheet/new", {type: $("sim-type").value})); }
  catch (err) { out.append(errBox(err)); return; }
  const inputs = {};
  const rows = sheet.parts.map((p) => {
    let control;
    if (p.kind === "set") {
      control = h("span", {}, p.options.map((o) => {
        const box = h("input", {type: "checkbox", value: o});
        inputs[p.key] = inputs[p.key] || [];
        inputs[p.key].push(box);
        return h("label", {class: "inline"}, box, o);
      }));
    } else {
      const box = h("input", {type: "number", step: "any", inputmode: "decimal", "aria-label": p.label});
      inputs[p.key] = box;
      control = h("span", {}, p.unit === "$" ? "$ " : "", box, p.unit && p.unit !== "$" ? ` ${p.unit}` : "");
    }
    return h("div", {class: "part", "data-key": p.key}, h("div", {class: "part-label"}, p.label), control, h("div", {class: "part-fb"}));
  });
  const check = h("button", {type: "button", class: "primary"}, "Check");
  out.append(h("div", {class: "card"}, h("p", {class: "q"}, sheet.title), h("p", {}, sheet.scenario),
    sheetTable(sheet.table), rows, h("div", {class: "row"}, check)));
  check.addEventListener("click", async () => {
    const answers = {};
    for (const p of sheet.parts)
      answers[p.key] = p.kind === "set" ? inputs[p.key].filter((b) => b.checked).map((b) => b.value) : inputs[p.key].value;
    check.disabled = true;
    try {
      const r = await api("/api/sheet/check", {id: sheet.id, answers});
      for (const part of r.parts) {
        const row = out.querySelector(`.part[data-key="${CSS.escape(part.key)}"]`);
        const fb = row.querySelector(".part-fb");
        fb.className = "part-fb " + (part.correct ? "ok" : "bad");
        fb.textContent = part.correct ? "Correct." : `Not quite. Expected ${part.unit === "$" ? "$" : ""}${part.expected}${part.unit && part.unit !== "$" ? " " + part.unit : ""}${part.given ? `; you entered ${part.given}` : ""}.`;
      }
      for (const el of out.querySelectorAll("input")) el.disabled = true;
      sim.sheets += 1; sim.perfect += r.correct ? 1 : 0; sim.parts[0] += r.right; sim.parts[1] += r.total;
      out.append(h("div", {class: "card"}, h("p", {class: "verdict " + (r.correct ? "ok" : "bad")}, `${r.right} of ${r.total} parts correct.`),
        h("p", {class: "src"}, "Working"), h("pre", {}, r.working.join("\n"))),
        h("button", {type: "button", class: "primary", onclick: simNew}, "Another sheet"),
        h("p", {class: "muted"}, `This session: ${sim.perfect} of ${sim.sheets} sheets fully right, ${sim.parts[0]} of ${sim.parts[1]} parts.`));
    } catch (err) { out.append(errBox(err)); check.disabled = false; }
  });
}
function sheetTable(t) {
  return h("table", {}, h("thead", {}, h("tr", {}, t.columns.map((c) => h("th", {}, c)))),
    h("tbody", {}, t.rows.map((row) => h("tr", {}, row.map((cell) => h("td", {}, cell))))));
}

// ---- cards -----------------------------------------------------------------
async function onCards(e) {
  e.preventDefault();
  const out = $("cards-out");
  clear(out);
  const status = h("p", {class: "spin"}, "Starting…");
  out.append(status);
  try {
    const {job} = await api("/api/cards", {source: $("cards-source").value, chapter: $("cards-chapter").value, limit: +$("cards-limit").value});
    for (;;) {
      await new Promise((r) => setTimeout(r, 1500));
      const s = await api("/api/job?id=" + encodeURIComponent(job));
      if (s.error) throw new Error(s.error);
      if (s.done) {
        clear(out);
        out.append(h("p", {}, `Wrote ${s.count} cards. `, h("a", {href: "/api/download?id=" + encodeURIComponent(job)}, "Download for Anki")));
        return;
      }
      status.textContent = s.last || "Working…";
    }
  } catch (err) { clear(out); out.append(errBox(err)); }
}

// ---- progress --------------------------------------------------------------
function chapterTable(rows) {
  if (!rows.length) return h("p", {class: "muted"}, "Nothing yet.");
  return h("table", {}, h("thead", {}, h("tr", {}, ...["Material", "Right", "Asked", ""].map((t) => h("th", {}, t)))),
    h("tbody", {}, rows.map((r) => {
      const pct = r.asked ? Math.round((100 * r.right) / r.asked) : 0;
      const fill = h("i");
      fill.style.width = `${pct}%`;  // a style attribute would be blocked by the CSP
      return h("tr", {}, h("td", {}, label(r.source, r.chapter)), h("td", {}, String(r.right)), h("td", {}, `${r.asked} (${pct}%)`),
        h("td", {}, h("div", {class: "bar"}, fill)));
    })));
}
async function loadProgress() {
  const out = $("progress-out");
  clear(out);
  try {
    const p = await api("/api/progress");
    out.append(h("p", {}, `${p.answered} answered so far. ${p.weak} questions you missed last time.`),
      p.weak ? h("button", {type: "button", class: "primary", onclick() { $("drill-mode").value = "weak"; showTab("drill"); drillNext(); }}, "Drill the ones I missed") : null,
      chapterTable(p.by_chapter));
  } catch (err) { out.append(errBox(err)); }
}

// ---- start -----------------------------------------------------------------
async function init() {
  INFO = await api("/api/info");
  for (const id of ["ask-source", "drill-source", "test-source", "cards-source"]) fillSource($(id));
  // generated questions and cards use every chunk; fixed questions use the bank's own chapters
  link($("ask-source"), $("ask-chapter"), () => INFO.chapters);
  link($("cards-source"), $("cards-chapter"), () => INFO.chapters);
  const sel = (id, list) => link($(id + "-source"), $(id + "-chapter"), list);
  const refreshDrill = sel("drill", () => ($("drill-kind").value === "gen" ? INFO.chapters : INFO.bank_chapters));
  sel("test", () => INFO.bank_chapters);
  $("drill-kind").addEventListener("change", () => {
    const gen = $("drill-kind").value === "gen";
    $("drill-topic-label").hidden = !gen;
    refreshDrill();
  });
  $("ask-form").addEventListener("submit", onAsk);
  $("drill-form").addEventListener("submit", (e) => { e.preventDefault(); drill.tally = [0, 0]; drill.last = null; drillNext(); });
  $("test-form").addEventListener("submit", onTest);
  const types = $("sim-type");
  types.append(h("option", {value: "any"}, "Any type"));
  for (const [k, v] of Object.entries(INFO.sheet_types)) types.append(h("option", {value: k}, v));
  $("sim-form").addEventListener("submit", (e) => { e.preventDefault(); simNew(); });
  $("cards-form").addEventListener("submit", onCards);
  const fromHash = () => {
    const wanted = location.hash.slice(1);
    if (document.querySelector(`#tabs [data-tab="${CSS.escape(wanted)}"]`)) showTab(wanted);
  };
  window.addEventListener("hashchange", fromHash);
  fromHash();
  const b = Object.entries(INFO.bank).map(([k, v]) => `${v} fixed ${k} questions`).join(", ");
  $("foot").textContent = `Local only. ${b}. Models: ${INFO.models.generate} (answers), ${INFO.models.embed} (search).`;
}
init().catch((e) => { document.body.prepend(errBox(e)); });
