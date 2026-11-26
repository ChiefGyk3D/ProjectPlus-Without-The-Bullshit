"""Hermetic tests for the calculation sheets: keys are re-derived independently."""
import math
import random
import unittest

from study import pbq


def dollars(text):
    return float(text.replace("$", "").replace(",", ""))


def all_paths(preds, names):
    succ = {k: [n for n in names if k in preds[n]] for k in names}
    out = []

    def walk(node, path):
        if not succ[node]:
            out.append(path)
        for nxt in succ[node]:
            walk(nxt, [*path, nxt])
    walk(names[0], [names[0]])
    return out


class Sheets(unittest.TestCase):
    def sheets(self, kind, n=300):
        rng = random.Random(7)
        return [pbq.generate(kind, rng) | {"id": f"s{i}"} for i in range(n)]

    def test_critical_path_keys_match_a_brute_force_search(self):
        for sheet in self.sheets("critical-path"):
            rows = sheet["table"]["rows"]
            names = [r[0] for r in rows]
            dur = {r[0]: int(r[1]) for r in rows}
            preds = {r[0]: [] if r[2] == "none" else r[2].split(", ") for r in rows}
            paths = all_paths(preds, names)
            length = {tuple(p): sum(dur[k] for k in p) for p in paths}
            longest = max(length.values())
            best = [p for p, n in length.items() if n == longest]
            self.assertEqual(len(best), 1, "the critical path must be unique")
            key = {p["key"]: p["answer"] for p in sheet["parts"]}
            self.assertEqual(key["duration"], longest)
            self.assertEqual(key["path"], list(best[0]))
            for name, value in key.items():
                if name.startswith("float-"):
                    node = name[6:]
                    through = max(n for p, n in length.items() if node in p)
                    self.assertEqual(value, longest - through)
                    self.assertGreater(value, 0)

    def test_evm_keys_follow_the_formulas(self):
        for sheet in self.sheets("evm"):
            v = {r[0].split("(")[1][:-1]: dollars(r[1]) for r in sheet["table"]["rows"]}
            bac, pv, ev, ac = v["BAC"], v["PV"], v["EV"], v["AC"]
            self.assertLess(ac, bac)
            one_off = "one-off" in sheet["scenario"]
            eac = ac + (bac - ev) if one_off else bac / (ev / ac)
            want = {"CV": ev - ac, "SV": ev - pv, "CPI": ev / ac, "SPI": ev / pv, "EAC": eac,
                    "ETC": eac - ac, "VAC": bac - eac, "TCPI": (bac - ev) / (bac - ac)}
            self.assertEqual(len(sheet["parts"]), 5)
            for part in sheet["parts"]:
                self.assertAlmostEqual(part["answer"], want[part["key"]], places=6)

    def test_pert_and_emv_keys(self):
        for sheet in self.sheets("pert", 100):
            tasks = {r[0]: [int(x) for x in r[1:]] for r in sheet["table"]["rows"]}
            exp = {k: (o + 4 * m + p) / 6 for k, (o, m, p) in tasks.items()}
            key = {p["key"]: p["answer"] for p in sheet["parts"]}
            self.assertAlmostEqual(key["total"], sum(exp.values()))
            self.assertAlmostEqual(key["sigma"], math.sqrt(sum(((p - o) / 6) ** 2 for o, m, p in tasks.values())))
            for k, val in key.items():
                if k.startswith("e-"):
                    self.assertAlmostEqual(val, exp[k[2:]])
        for sheet in self.sheets("emv", 100):
            rows = {r[0]: (float(r[1][:-1]), dollars(r[2])) for r in sheet["table"]["rows"]}
            key = {p["key"]: p["answer"] for p in sheet["parts"]}
            self.assertAlmostEqual(key["net"], sum(p * i / 100 for p, i in rows.values()))
            self.assertAlmostEqual(key["threats"], sum(p * i / 100 for p, i in rows.values() if i < 0))

    def test_grading_has_tolerance_and_partial_credit(self):
        sheet = pbq.generate("evm", random.Random(3)) | {"id": "x"}
        exact = {p["key"]: p["answer"] for p in sheet["parts"]}
        self.assertTrue(pbq.grade(sheet, exact)["correct"])
        first = sheet["parts"][0]
        off = dict(exact, **{first["key"]: first["answer"] + first["tol"] * 5 + 5})
        res = pbq.grade(sheet, off)
        self.assertEqual((res["right"], res["total"]), (4, 5))
        blank = dict(exact, **{first["key"]: ""})
        self.assertFalse(pbq.grade(sheet, blank)["parts"][0]["correct"])
        comma = dict(exact, **{first["key"]: f"${first['answer']:,.2f}"})
        self.assertTrue(pbq.grade(sheet, comma)["parts"][0]["correct"])

    def test_a_set_answer_needs_the_exact_set(self):
        sheet = pbq.generate("critical-path", random.Random(4)) | {"id": "x"}
        part = next(p for p in sheet["parts"] if p["kind"] == "set")
        full = {p["key"]: p["answer"] for p in sheet["parts"]}
        self.assertTrue(pbq.grade(sheet, full)["correct"])
        short = dict(full, path=part["answer"][:-1])
        self.assertFalse(next(r for r in pbq.grade(sheet, short)["parts"] if r["key"] == "path")["correct"])

    def test_the_public_sheet_has_no_key_and_unknown_types_fail(self):
        sheet = pbq.generate("pert", random.Random(1)) | {"id": "x"}
        shown = pbq.public(sheet)
        self.assertNotIn("working", shown)
        self.assertTrue(all("answer" not in p and "tol" not in p for p in shown["parts"]))
        with self.assertRaises(ValueError):
            pbq.generate("nonsense")


class Sorting(unittest.TestCase):
    def test_sets_are_unambiguous(self):
        from study.pbq_sets import MATCHINGS, ORDERINGS
        for steps in ORDERINGS.values():
            self.assertEqual(len(set(steps)), len(steps))
        for pairs in MATCHINGS.values():
            self.assertEqual(len(set(pairs.values())), len(pairs))

    def test_ordering_keys_follow_the_source_and_options_are_shuffled(self):
        from study.pbq_sets import ORDERINGS
        rng = random.Random(3)
        for i in range(200):
            item = pbq.generate("ordering", rng) | {"id": f"o{i}"}
            title = item["title"].split(": ", 1)[1]
            answers = [p["answer"] for p in item["parts"]]
            source = ORDERINGS[title]
            self.assertEqual(answers, sorted(answers, key=source.index))
            self.assertNotEqual(answers, item["parts"][0]["options"])
            self.assertEqual(sorted(answers), sorted(item["parts"][0]["options"]))

    def test_matching_keys_and_grading(self):
        from study.pbq_sets import MATCHINGS
        rng = random.Random(4)
        for i in range(200):
            item = pbq.generate("matching", rng) | {"id": f"m{i}"}
            pairs = MATCHINGS[item["title"].split(": ", 1)[1]]
            for p in item["parts"]:
                self.assertEqual(p["answer"], pairs[p["label"]])
            given = {p["key"]: p["answer"] for p in item["parts"]}
            res = pbq.grade(item, given)
            self.assertTrue(res["correct"])
            given[item["parts"][0]["key"]] = ""
            res = pbq.grade(item, given)
            self.assertEqual((res["right"], res["total"]), (len(item["parts"]) - 1, len(item["parts"])))

    def test_public_hides_answers(self):
        item = pbq.generate("ordering", random.Random(1)) | {"id": "x"}
        text = str(pbq.public(item))
        self.assertNotIn("'answer'", text)
        self.assertNotIn("working", text)
