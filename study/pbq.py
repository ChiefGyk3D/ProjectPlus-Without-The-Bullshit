"""Performance-based practice: calculation sheets generated and graded by code.

Nothing here uses a model and nothing comes from the book or the exam. Every number
is drawn at random and every answer is computed, so the key is always right and the
supply is unlimited. These are our own practice versions of the hands-on items;
CompTIA does not publish the exam's formats.

A sheet is {id, type, title, scenario, table, parts, working}. A part is
{key, label, kind ('number', 'set' or 'choice'), answer, tol, unit, options}.
"""
import math
import random

from .pbq_sets import MATCHINGS, ORDERINGS

KINDS = {
    "evm": "Earned value",
    "critical-path": "Critical path",
    "pert": "PERT estimate",
    "emv": "Risk exposure (EMV)",
    "ordering": "Put in order",
    "matching": "Match terms",
}
LETTERS = "ABCDEFG"


def _usd(x: float) -> str:
    return f"-${abs(x):,.0f}" if x < 0 else f"${x:,.0f}"


def _money_tol(x: float) -> float:
    return max(1.0, abs(x) * 0.01)


def _part(key, label, answer, unit="", tol=0.0, kind="number", options=None):
    return {"key": key, "label": label, "kind": kind, "answer": answer, "tol": tol,
            "unit": unit, "options": options or []}


def evm(rng: random.Random) -> dict:
    bac = rng.randrange(100_000, 900_001, 20_000)
    planned = rng.choice(range(20, 61, 5))
    done = planned + rng.choice([-10, -5, 5, 10])
    pv, ev = bac * planned / 100, bac * done / 100
    ac = round(ev * rng.choice([0.8, 0.9, 1.1, 1.25]) / 1000) * 1000
    one_off = rng.random() < 0.35
    cpi, spi = ev / ac, ev / pv
    eac = ac + (bac - ev) if one_off else bac / cpi
    values = {
        "CV": ("Cost variance (CV)", ev - ac, "$", _money_tol(ev - ac), f"CV = EV - AC = {_usd(ev)} - {_usd(ac)}"),
        "SV": ("Schedule variance (SV)", ev - pv, "$", _money_tol(ev - pv), f"SV = EV - PV = {_usd(ev)} - {_usd(pv)}"),
        "CPI": ("Cost performance index (CPI)", cpi, "", 0.01, f"CPI = EV / AC = {_usd(ev)} / {_usd(ac)}"),
        "SPI": ("Schedule performance index (SPI)", spi, "", 0.01, f"SPI = EV / PV = {_usd(ev)} / {_usd(pv)}"),
        "EAC": ("Estimate at completion (EAC)", eac, "$", _money_tol(eac),
                f"EAC = AC + (BAC - EV) = {_usd(ac)} + ({_usd(bac)} - {_usd(ev)})" if one_off
                else f"EAC = BAC / CPI = {_usd(bac)} / {cpi:.4f}"),
        "ETC": ("Estimate to complete (ETC)", eac - ac, "$", _money_tol(eac - ac),
                f"ETC = EAC - AC = {_usd(eac)} - {_usd(ac)}"),
        "VAC": ("Variance at completion (VAC)", bac - eac, "$", _money_tol(bac - eac),
                f"VAC = BAC - EAC = {_usd(bac)} - {_usd(eac)}"),
        "TCPI": ("To-complete performance index (TCPI, to BAC)", (bac - ev) / (bac - ac), "", 0.01,
                 f"TCPI = (BAC - EV) / (BAC - AC) = ({_usd(bac)} - {_usd(ev)}) / ({_usd(bac)} - {_usd(ac)})"),
    }
    chosen = set(rng.sample(list(values), 5))
    asked = [k for k in values if k in chosen]
    parts = [_part(k, values[k][0], values[k][1], values[k][2], values[k][3]) for k in asked]
    note = ("Assume the cost variance so far is a one-off and the rest of the work will be done at the "
            "budgeted rate." if one_off else
            "Assume the cost performance so far will continue for the rest of the project.")
    return {
        "title": KINDS["evm"],
        "scenario": "A project is being status-checked. Work out the values below. Round indexes to two "
                    f"decimals; dollars may be rounded to the nearest dollar. {note}",
        "table": {"columns": ["Measure", "Value"], "rows": [
            ["Budget at completion (BAC)", _usd(bac)], ["Planned value (PV)", _usd(pv)],
            ["Earned value (EV)", _usd(ev)], ["Actual cost (AC)", _usd(ac)]]},
        "parts": parts,
        "working": [values[k][4] + f" = {_usd(values[k][1]) if values[k][2] == '$' else f'{values[k][1]:.2f}'}"
                    for k in asked],
    }


def _network(rng: random.Random):
    """A small activity network with exactly one longest path and at least two off it."""
    for _ in range(500):
        n = rng.choice([6, 7])
        names = LETTERS[:n]
        dur = {k: rng.randint(2, 9) for k in names}
        preds = {names[0]: []}
        for i in range(1, n):
            pool = names[max(0, i - 3):i]
            preds[names[i]] = sorted(rng.sample(pool, rng.choice([1, 1, 2]) if len(pool) > 1 else 1))
        succ = {k: [] for k in names}
        for k in names[1:]:
            for p in preds[k]:
                succ[p].append(k)
        for k in names[:-1]:
            if not succ[k]:
                preds[names[-1]] = sorted({*preds[names[-1]], k})
                succ[k].append(names[-1])
        es, ef, tight = {}, {}, {}
        for k in names:
            es[k] = max((ef[p] for p in preds[k]), default=0)
            ef[k] = es[k] + dur[k]
            tight[k] = 1 if not preds[k] else sum(tight[p] for p in preds[k] if ef[p] == es[k])
        total = ef[names[-1]]
        lf, ls = {}, {}
        for k in reversed(names):
            lf[k] = min((ls[s] for s in succ[k]), default=total)
            ls[k] = lf[k] - dur[k]
        flt = {k: ls[k] - es[k] for k in names}
        critical = [k for k in names if flt[k] == 0]
        if tight[names[-1]] == 1 and len(critical) <= n - 2:
            return names, dur, preds, es, ef, ls, lf, flt, total, critical
    raise RuntimeError("could not build a network")


def critical_path(rng: random.Random) -> dict:
    names, dur, preds, es, ef, ls, lf, flt, total, critical = _network(rng)
    off = [k for k in names if flt[k] > 0]
    asked = sorted(rng.sample(off, 2))
    parts = [_part("duration", "Project duration", total, "days", 0.0),
             _part("path", "Activities on the critical path", critical, kind="set", options=list(names))]
    parts += [_part(f"float-{k}", f"Total float of activity {k}", flt[k], "days", 0.0) for k in asked]
    return {
        "title": KINDS["critical-path"],
        "scenario": "Use the activity table. The first activity starts at day 0, so a finish equals its start "
                    "plus its duration. Every activity starts as soon as all its predecessors finish.",
        "table": {"columns": ["Activity", "Duration (days)", "Predecessors"], "rows": [
            [k, str(dur[k]), ", ".join(preds[k]) or "none"] for k in names]},
        "parts": parts,
        "working": [f"{k}: ES {es[k]}, EF {ef[k]}, LS {ls[k]}, LF {lf[k]}, float {flt[k]}" for k in names]
                   + [f"Critical path: {' > '.join(critical)} ({total} days). Float = LS - ES."],
    }


def pert(rng: random.Random) -> dict:
    tasks = []
    for k in "ABC":
        o = rng.randint(2, 10)
        m = o + rng.randint(1, 6)
        p = m + rng.randint(2, 12)
        tasks.append((k, o, m, p, (o + 4 * m + p) / 6, (p - o) / 6))
    total = sum(t[4] for t in tasks)
    sigma = math.sqrt(sum(t[5] ** 2 for t in tasks))
    first, second = rng.sample(tasks, 2)
    parts = [_part(f"e-{t[0]}", f"Expected duration of task {t[0]}", t[4], "days", 0.05)
             for t in sorted((first, second))]
    parts += [_part("total", "Expected duration of the whole project", total, "days", 0.05),
              _part("sigma", "Standard deviation of the whole project", sigma, "days", 0.05)]
    return {
        "title": KINDS["pert"],
        "scenario": "Three tasks run one after another. Use the PERT weighted average, (O + 4M + P) / 6, for each "
                    "task. A task's standard deviation is (P - O) / 6; for tasks in sequence add the variances "
                    "(standard deviation squared) and take the square root. Round to two decimals.",
        "table": {"columns": ["Task", "Optimistic (O)", "Most likely (M)", "Pessimistic (P)"],
                  "rows": [[t[0], str(t[1]), str(t[2]), str(t[3])] for t in tasks]},
        "parts": parts,
        "working": [f"{t[0]}: E = ({t[1]} + 4 x {t[2]} + {t[3]}) / 6 = {t[4]:.2f}; "
                    f"sd = ({t[3]} - {t[1]}) / 6 = {t[5]:.2f}" for t in tasks]
                   + [f"Total E = {total:.2f}; sd = sqrt({' + '.join(f'{t[5]:.2f}^2' for t in tasks)}) = {sigma:.2f}"],
    }


RISKS = ["Vendor delivers late", "Key developer leaves", "Requirements change", "Server delivery slips",
         "Early sign-off by the sponsor", "Reusable module found", "Permit delayed", "Test environment fails",
         "Volume discount offered", "Regulation changes"]


def emv(rng: random.Random) -> dict:
    picked = rng.sample(RISKS, 4)
    rows = []
    for name in picked:
        opportunity = name in ("Early sign-off by the sponsor", "Reusable module found", "Volume discount offered")
        prob = rng.choice(range(10, 71, 5))
        impact = rng.randrange(5_000, 60_001, 5_000) * (1 if opportunity else -1)
        rows.append((name, prob, impact, prob * impact / 100))
    threats = sum(r[3] for r in rows if r[3] < 0)
    net = sum(r[3] for r in rows)
    first, second = rng.sample(rows, 2)
    parts = [_part(f"emv-{r[0]}", f"EMV of '{r[0]}'", r[3], "$", 1.0) for r in (first, second)]
    parts += [_part("threats", "Total EMV of the threats only", threats, "$", 1.0),
              _part("net", "Net EMV of all four risks", net, "$", 1.0)]
    return {
        "title": KINDS["emv"],
        "scenario": "EMV = probability x impact. Threats have a negative impact (cost) and opportunities a "
                    "positive one (saving). Enter threats as negative numbers.",
        "table": {"columns": ["Risk", "Probability", "Impact"],
                  "rows": [[r[0], f"{r[1]}%", _usd(r[2])] for r in rows]},
        "parts": parts,
        "working": [f"{r[0]}: {r[1]}% x {_usd(r[2])} = {_usd(r[3])}" for r in rows]
                   + [f"Threats only = {_usd(threats)}; net = {_usd(net)}"],
    }


def ordering(rng: random.Random) -> dict:
    title = rng.choice(list(ORDERINGS))
    steps = ORDERINGS[title]
    run = sorted(rng.sample(range(len(steps)), min(6, len(steps))))
    chosen = [steps[i] for i in run]
    shuffled = chosen[:]
    while len(chosen) > 1 and shuffled == chosen:
        rng.shuffle(shuffled)
    parts = [_part(f"step-{i}", f"Step {i}", s, kind="choice", options=shuffled)
             for i, s in enumerate(chosen, 1)]
    return {
        "title": f"{KINDS['ordering']}: {title}",
        "scenario": "Pick what comes at each position, first to last. Every item is used once.",
        "table": None, "parts": parts,
        "working": [f"{i}. {s}" for i, s in enumerate(chosen, 1)],
    }


def matching(rng: random.Random) -> dict:
    title = rng.choice(list(MATCHINGS))
    pairs = MATCHINGS[title]
    terms = rng.sample(list(pairs), min(5, len(pairs)))
    options = [pairs[t] for t in terms]
    rng.shuffle(options)
    parts = [_part(f"term-{i}", t, pairs[t], kind="choice", options=options) for i, t in enumerate(terms)]
    return {
        "title": f"{KINDS['matching']}: {title}",
        "scenario": "Pick the description that fits each term. Every description is used once.",
        "table": None, "parts": parts,
        "working": [f"{t}: {pairs[t]}" for t in terms],
    }


GENERATORS = {"evm": evm, "critical-path": critical_path, "pert": pert, "emv": emv,
              "ordering": ordering, "matching": matching}


def generate(kind: str | None = None, rng: random.Random | None = None) -> dict:
    rng = rng or random.Random()
    if kind in (None, "", "any"):
        kind = rng.choice(list(GENERATORS))
    if kind not in GENERATORS:
        raise ValueError(f"unknown sheet type: {kind}")
    return GENERATORS[kind](rng) | {"type": kind}


def public(item: dict) -> dict:
    """The sheet without its answers or working."""
    parts = [{k: p[k] for k in ("key", "label", "kind", "unit", "options")} for p in item["parts"]]
    return {"id": item["id"], "type": item["type"], "title": item["title"],
            "scenario": item["scenario"], "table": item["table"], "parts": parts}


def _number(value):
    try:
        return float(str(value).replace(",", "").replace("$", "").strip())
    except ValueError:
        return None


def grade(item: dict, given: dict) -> dict:
    """Per-part results with the key and the working. Partial credit: one point per part."""
    results = []
    for p in item["parts"]:
        got = given.get(p["key"])
        if p["kind"] == "set":
            ok = isinstance(got, list) and sorted(map(str, got)) == sorted(p["answer"])
            shown, want = ", ".join(sorted(map(str, got))) if isinstance(got, list) else "", " > ".join(p["answer"])
        elif p["kind"] == "choice":
            ok, shown, want = got == p["answer"], str(got or ""), p["answer"]
        else:
            num = _number(got) if got not in (None, "") else None
            ok = num is not None and abs(num - p["answer"]) <= p["tol"] + 1e-9
            shown, want = ("" if num is None else f"{num:g}"), f"{p['answer']:,.2f}".rstrip("0").rstrip(".")
        results.append({"key": p["key"], "label": p["label"], "correct": ok, "given": shown,
                        "expected": want, "unit": p["unit"]})
    right = sum(r["correct"] for r in results)
    return {"parts": results, "right": right, "total": len(results), "correct": right == len(results),
            "working": item["working"]}
