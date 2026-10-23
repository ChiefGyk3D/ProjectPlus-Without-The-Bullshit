"""Hermetic tests for the fixed question banks and the local web server."""
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from study import bank, modes, web

QUESTIONS = (
    "1. What is the first thing to do? A. Act B. Ask C. Wait D. Run "
    "2. Which are two risk responses? A. Mitigate B. Lunch C. Share D. Nap "
    "3. A broken question with no choices at all. "
    "4. Last one? A. Yes B. No C. Maybe"
)
ANSWERS = (
    "1. B. Asking comes first, because 2. is not a step. "
    "2. A, C. Mitigate and share are responses. "
    "3. A. This one has no choices. "
    "4. C. Maybe is right."
)


def chunks():
    def chunk(i, kind, text):
        return {"id": f"book-{i}", "source": "book", "chapter": "1",
                "heading": f"Chapter Review > {kind}", "text": text, "ref": f"Ch 1, p. {i}"}
    return [chunk(1, "Questions", QUESTIONS), chunk(2, "Answers", ANSWERS)]


GUIDE_MD = """# Practice

### 1.0 Concepts

**1.** Which comes first?

- A. One
- B. Two
- C. Three
- D. Four

**2.** Which **two** apply? **Choose two.**

- A. Alpha
- B. Beta
- C. Gamma

### Answers

**1. B.** Two comes first. See [1.1](01.md#11).

**2. A, C.** Alpha and gamma apply.
"""


class Banks(unittest.TestCase):
    def test_book_questions_parse_with_keys_and_multi_answers(self):
        items = {i["n"]: i for i in bank.book_items(chunks())}
        self.assertEqual(sorted(items), [1, 2, 4])  # 3 has no choices and is dropped
        self.assertEqual(items[1]["answer"], [1])
        self.assertIn("2. is not a step", items[1]["explanation"])  # a '2. ' inside text is not a new item
        self.assertEqual(items[2]["answer"], [0, 2])
        self.assertEqual(len(items[4]["choices"]), 3)

    def test_guide_questions_parse(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "07-practice.md"
            path.write_text(GUIDE_MD)
            items = bank.guide_items(path)
        self.assertEqual([i["answer"] for i in items], [[1], [0, 2]])
        self.assertNotIn("**", items[1]["question"])
        self.assertNotIn("See [", items[0]["explanation"])

    def test_missing_guide_file_is_empty(self):
        self.assertEqual(bank.guide_items(Path("/nonexistent/x.md")), [])


class Server(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        data = Path(self.tmp.name)
        guide = data / "07-practice.md"
        guide.write_text(GUIDE_MD)
        cfg = SimpleNamespace(data_dir=data, guide_dir=data, embed_model="e", gen_model="g")
        index = SimpleNamespace(chunks=chunks(), meta={"book": {}})
        app = web.App(cfg, index, guide)
        self.app = app
        self.httpd = web.ThreadingHTTPServer(("127.0.0.1", 0), web.make_handler(app))
        self.httpd.daemon_threads = True
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()

    def call(self, path, body=None, headers=None):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(self.base + path, data=data, headers={
            "Content-Type": "application/json", **(headers or {})})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_the_key_is_not_sent_with_the_question(self):
        _, r = self.call("/api/bank/next", {"source": "guide"})
        self.assertNotIn("answer", r["item"])
        self.assertNotIn("explanation", r["item"])

    def test_grading_a_single_and_a_multi_answer(self):
        _, r = self.call("/api/answer", {"id": "guide-q1", "choice": [1]})
        self.assertTrue(r["correct"])
        _, r = self.call("/api/answer", {"id": "guide-q2", "choice": [0]})
        self.assertFalse(r["correct"])  # needs both
        _, r = self.call("/api/answer", {"id": "guide-q2", "choice": [2, 0]})
        self.assertTrue(r["correct"])
        self.assertEqual(self.call("/api/answer", {"id": "nope", "choice": [0]})[0], 404)

    def test_progress_weak_and_unseen_follow_the_log(self):
        self.call("/api/answer", {"id": "guide-q1", "choice": [0]})  # wrong
        _, p = self.call("/api/progress")
        self.assertEqual((p["answered"], p["weak"]), (1, 1))
        _, r = self.call("/api/bank/next", {"source": "guide", "mode": "weak"})
        self.assertEqual(r["item"]["id"], "guide-q1")
        _, r = self.call("/api/bank/next", {"source": "guide", "mode": "unseen"})
        self.assertEqual(r["item"]["id"], "guide-q2")

    def test_a_practice_test_is_graded_at_the_end(self):
        _, t = self.call("/api/test/start", {"n": 99, "source": "guide"})
        self.assertEqual(len(t["items"]), 2)  # capped to what exists
        answers = {"guide-q1": [1], "guide-q2": [0, 2]}
        _, r = self.call("/api/test/finish", {"test": t["test"], "answers": answers})
        self.assertEqual((r["right"], r["total"]), (2, 2))
        self.assertEqual(self.call("/api/test/finish", {"test": t["test"], "answers": {}})[0], 404)

    def test_generated_questions_are_checked_by_the_server(self):
        item = {"question": "Q?", "choices": ["a", "b", "c", "d"], "answer": 2, "evidence": "quote",
                "explanation": "why", "ref": "Ch 1, p. 1", "chunk": "book-1", "source": "book",
                "chapter": "1"}
        with mock.patch.object(modes, "pick", return_value=[chunks()[0]]), \
                mock.patch.object(modes, "make_question", return_value=item):
            _, r = self.call("/api/quiz/next", {"source": "book"})
        self.assertNotIn("answer", r["item"])
        _, res = self.call("/api/answer", {"id": r["item"]["id"], "choice": [2]})
        self.assertTrue(res["correct"])
        self.assertEqual(res["evidence"], "quote")

    def test_only_local_same_origin_json_is_accepted(self):
        self.assertEqual(self.call("/api/info", headers={"Host": "evil.example"})[0], 403)
        self.assertEqual(self.call("/api/answer", {"id": "guide-q1", "choice": [1]},
                                   {"Origin": "http://evil.example"})[0], 403)
        req = urllib.request.Request(self.base + "/api/answer", data=b"{}", headers={"Content-Type": "text/plain"})
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(req)
        self.assertEqual(cm.exception.code, 403)

    def test_bad_input_is_a_400_not_a_crash(self):
        self.assertEqual(self.call("/api/bank/next", {"mode": "nonsense"})[0], 400)
        self.assertEqual(self.call("/api/ask", {"question": ""})[0], 400)
        self.assertEqual(self.call("/api/bank/next", {"source": "movies"})[0], 400)

    def test_static_files_and_unknown_paths(self):
        with urllib.request.urlopen(self.base + "/") as r:
            self.assertIn("Project+ study", r.read().decode())
            self.assertIn("default-src 'none'", r.headers["Content-Security-Policy"])
        self.assertEqual(self.call("/api/nothing")[0], 404)
