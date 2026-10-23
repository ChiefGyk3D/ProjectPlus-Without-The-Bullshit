"""Local web page over the study tool: python3 -m study web

Binds to 127.0.0.1 only, serves four fixed static files, and takes JSON POSTs.
The answer key of a question never leaves the server until the question is answered.
"""
import collections
import json
import random
import threading
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import bank, llm, modes

STATIC = Path(__file__).resolve().parent / "static"
FILES = {"/": ("index.html", "text/html; charset=utf-8"),
         "/app.js": ("app.js", "text/javascript; charset=utf-8"),
         "/app.css": ("app.css", "text/css; charset=utf-8")}
MAX_BODY = 64 * 1024
MAX_KEPT = 400  # generated questions remembered for answer checking
LOCAL_HOSTS = {"127.0.0.1", "localhost", "[::1]"}


def public(item: dict) -> dict:
    """An item without its key."""
    return {k: item[k] for k in ("id", "source", "chapter", "question", "choices", "ref")} | {
        "pick": len(item["answer"]), "kind": item.get("kind", "bank")}


class Feeder:
    """Generates quiz questions ahead of the one being answered, per (source, chapter, topic, weak)."""

    AHEAD = 2

    def __init__(self, cfg, index, weak_chunks):
        self.cfg, self.index, self.weak_chunks = cfg, index, weak_chunks
        self.cond = threading.Condition()
        self.streams = {}

    def _stream(self, key):
        if key not in self.streams:
            source, chapter, topic, weak = key
            pool = modes.pick(self.cfg, self.index, 50, source, chapter, topic)
            if weak:
                wanted = self.weak_chunks()
                pool = [c for c in pool if c["id"] in wanted] or \
                       [c for c in self.index.chunks if c["id"] in wanted]
            random.shuffle(pool)
            self.streams[key] = {"pool": pool, "ready": collections.deque(), "busy": False}
        return self.streams[key]

    def _kick(self, key, s):  # call with the lock held
        if not s["busy"] and s["pool"] and len(s["ready"]) < self.AHEAD:
            s["busy"] = True
            threading.Thread(target=self._fill, args=(key, s), daemon=True).start()

    def _fill(self, key, s):
        try:
            while True:
                with self.cond:
                    if len(s["ready"]) >= self.AHEAD or not s["pool"]:
                        return
                    chunk = s["pool"].pop()
                try:
                    item = modes.make_question(self.cfg, chunk)
                except llm.OllamaError:
                    item = None
                with self.cond:
                    if item:
                        s["ready"].append(item)
                        self.cond.notify_all()
        finally:
            with self.cond:
                s["busy"] = False
                self.cond.notify_all()

    def next(self, key, timeout=180):
        with self.cond:
            s = self._stream(key)
            self._kick(key, s)
            self.cond.wait_for(lambda: s["ready"] or not s["busy"], timeout)
            item = s["ready"].popleft() if s["ready"] else None
            self._kick(key, s)
            return item


class App:
    def __init__(self, cfg, index, guide_file: Path | None = None):
        self.cfg, self.index = cfg, index
        self.lock = threading.Lock()
        self.log_path = cfg.data_dir / "quiz-log.jsonl"
        items = bank.book_items(index.chunks) if "book" in index.meta else []
        items += bank.guide_items(guide_file or cfg.guide_dir / "07-practice.md")
        items += bank.generated_items(cfg.data_dir / bank.GENERATED)
        self.bank = {i["id"]: i for i in items}
        self.generated = collections.OrderedDict()
        self.tests = {}
        self.jobs = {}
        self.feeder = Feeder(cfg, index, self.weak_chunks)
        self.chapter_of = {c["id"]: c["chapter"] for c in index.chunks}

    # -- the log ------------------------------------------------------------------
    def _log(self, entry: dict) -> None:
        with self.lock, self.log_path.open("a") as fh:
            fh.write(json.dumps(entry) + "\n")

    def history(self) -> list[dict]:
        if not self.log_path.is_file():
            return []
        out = []
        for line in self.log_path.read_text().splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict) and row.get("correct") is not None:
                out.append(row)
        return out

    def last_result(self) -> dict:
        return {r["chunk"]: r["correct"] for r in self.history()}

    def weak_chunks(self) -> set:
        return {k for k, ok in self.last_result().items() if not ok}

    # -- handlers (each returns a JSON-able dict) ---------------------------------
    def info(self):
        chapters = collections.OrderedDict()
        for c in self.index.chunks:
            chapters.setdefault((c["source"], c["chapter"]), 0)
            chapters[(c["source"], c["chapter"])] += 1
        counts = collections.Counter(i.get("set", i["source"]) for i in self.bank.values())
        bank_ch = sorted({(i["source"], i["chapter"]) for i in self.bank.values()},
                         key=lambda t: (t[0], int(t[1]) if t[1].isdigit() else 0, t[1]))
        return {"sources": sorted(self.index.meta),
                "chapters": [{"source": s, "chapter": ch} for s, ch in chapters],
                "bank_chapters": [{"source": s, "chapter": ch} for s, ch in bank_ch],
                "bank": dict(counts), "models": {"embed": self.cfg.embed_model,
                                                 "generate": self.cfg.gen_model}}

    def ask(self, body):
        question = str(body.get("question", "")).strip()
        if not question or len(question) > 1000:
            raise ValueError("ask a question of 1 to 1000 characters")
        answer, cites = modes.ask(self.cfg, self.index, question, *self._scope(body))
        return {"answer": answer, "cites": [{"n": n, "ref": r, "source": s} for n, r, s in cites]}

    def _scope(self, body):
        source = body.get("source", "both")
        if source not in ("book", "guide", "both"):
            raise ValueError("bad source")
        chapter = str(body["chapter"]) if body.get("chapter") else None
        return source, chapter

    def quiz_next(self, body):
        source, chapter = self._scope(body)
        topic = str(body.get("topic", "")).strip()[:200] or None
        key = (source, chapter, topic, bool(body.get("weak")))
        item = self.feeder.next(key)
        if item is None:
            return {"item": None}
        item = dict(item, id=f"gen-{uuid.uuid4().hex[:10]}", kind="generated",
                    answer=[item["answer"]], key_chunk=item["chunk"])
        with self.lock:
            self.generated[item["id"]] = item
            while len(self.generated) > MAX_KEPT:
                self.generated.popitem(last=False)
        return {"item": public(item)}

    def _eligible(self, body):
        source, chapter = self._scope(body)
        return [i for i in self.bank.values()
                if (source == "both" or i["source"] == source)
                and (chapter is None or i["chapter"] == chapter)]

    def bank_next(self, body):
        pool, last = self._eligible(body), self.last_result()
        mode = body.get("mode", "random")
        if mode == "unseen":
            pool = [i for i in pool if i["id"] not in last]
        elif mode == "weak":
            pool = [i for i in pool if last.get(i["id"]) is False]
        elif mode != "random":
            raise ValueError("bad mode")
        if len(pool) > 1:
            pool = [i for i in pool if i["id"] != body.get("after")]
        return {"item": public(random.choice(pool)) if pool else None, "left": len(pool)}

    def _find(self, item_id):
        item = self.bank.get(item_id) or self.generated.get(item_id)
        if item is None:
            raise KeyError("unknown question - ask for a new one")
        return item

    def _grade(self, item, choice, kind):
        picked = sorted({int(x) for x in choice})
        correct = picked == item["answer"]
        chunk = item.get("key_chunk", item["id"])
        self._log({"t": int(time.time()), "chunk": chunk, "correct": correct, "kind": kind,
                   "chapter": item["chapter"], "source": item["source"]})
        out = {"id": item["id"], "correct": correct, "answer": item["answer"],
               "chosen": picked, "explanation": item.get("explanation", ""), "ref": item["ref"]}
        if item.get("evidence"):
            out["evidence"] = item["evidence"]
        return out

    def answer(self, body):
        return self._grade(self._find(body.get("id")), body.get("choice", []), body.get("kind", "drill"))

    def test_start(self, body):
        pool = self._eligible(body)
        n = max(1, min(int(body.get("n", 20)), 90, len(pool)))
        if not pool:
            raise ValueError("no questions match")
        picked = random.sample(pool, n)
        test_id = uuid.uuid4().hex[:10]
        self.tests[test_id] = {"ids": [i["id"] for i in picked], "t0": time.time()}
        return {"test": test_id, "items": [public(i) for i in picked]}

    def test_finish(self, body):
        t = self.tests.pop(body.get("test"), None)
        if t is None:
            raise KeyError("unknown or finished test")
        given = body.get("answers", {})
        results, by_ch = [], collections.defaultdict(lambda: [0, 0])
        for item_id in t["ids"]:
            item = self.bank[item_id]
            res = self._grade(item, given.get(item_id, []), "test")
            res["question"] = item["question"]
            res["choices"] = item["choices"]
            results.append(res)
            tally = by_ch[(item["source"], item["chapter"])]
            tally[0] += 1
            tally[1] += res["correct"]
        right = sum(r["correct"] for r in results)
        return {"right": right, "total": len(results), "seconds": int(time.time() - t["t0"]),
                "by_chapter": [{"source": s, "chapter": c, "asked": a, "right": r}
                               for (s, c), (a, r) in sorted(by_ch.items())],
                "results": results}

    def progress(self, _body=None):
        rows = collections.defaultdict(lambda: [0, 0])
        for r in self.history():
            ch = r.get("chapter") or self.chapter_of.get(r["chunk"], "?")
            tally = rows[(r.get("source", "book"), ch)]
            tally[0] += 1
            tally[1] += bool(r["correct"])
        last = self.last_result()
        return {"by_chapter": [{"source": s, "chapter": c, "asked": a, "right": r}
                               for (s, c), (a, r) in sorted(rows.items())],
                "weak": sum(1 for ok in last.values() if not ok),
                "answered": sum(a for a, _ in rows.values())}

    def cards_start(self, body):
        source, chapter = self._scope(body)
        limit = max(1, min(int(body.get("limit", 10)), 60))
        job_id = uuid.uuid4().hex[:10]
        path = self.cfg.data_dir / "cards" / f"web-{job_id}.csv"
        job = {"lines": [], "done": False, "count": 0, "error": None, "path": path}
        self.jobs[job_id] = job

        def run():
            try:
                job["count"] = modes.cards(self.cfg, self.index, source, chapter, None,
                                           limit, None, path, out=job["lines"].append)
            except (llm.OllamaError, OSError, ValueError) as e:  # shown on the page
                job["error"] = str(e)
            job["done"] = True
        threading.Thread(target=run, daemon=True).start()
        return {"job": job_id}

    def job(self, job_id):
        job = self.jobs.get(job_id)
        if job is None:
            raise KeyError("unknown job")
        return {"done": job["done"], "count": job["count"], "error": job["error"],
                "last": job["lines"][-1] if job["lines"] else ""}


POST_ROUTES = {"/api/ask": "ask", "/api/quiz/next": "quiz_next", "/api/bank/next": "bank_next",
               "/api/answer": "answer", "/api/test/start": "test_start",
               "/api/test/finish": "test_finish", "/api/cards": "cards_start"}


def make_handler(app: App):
    class Handler(BaseHTTPRequestHandler):
        server_version = "study"

        def log_message(self, *_):  # keep questions and answers out of the terminal
            pass

        def _send(self, status, body: bytes, ctype: str, extra=None):
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy",
                             "default-src 'none'; script-src 'self'; style-src 'self'; "
                             "connect-src 'self'; base-uri 'none'; form-action 'none'")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status, data):
            self._send(status, json.dumps(data).encode(), "application/json")

        def _local(self) -> bool:
            host = self.headers.get("Host") or ""
            name = host[:host.rfind("]") + 1] if host.startswith("[") else host.split(":")[0]
            return name in LOCAL_HOSTS

        def do_GET(self):
            if not self._local():
                return self._json(HTTPStatus.FORBIDDEN, {"error": "local access only"})
            url = urlparse(self.path)
            if url.path in FILES:
                name, ctype = FILES[url.path]
                return self._send(200, (STATIC / name).read_bytes(), ctype)
            try:
                q = {k: v[0] for k, v in parse_qs(url.query).items()}
                if url.path == "/api/info":
                    return self._json(200, app.info())
                if url.path == "/api/progress":
                    return self._json(200, app.progress())
                if url.path == "/api/job":
                    return self._json(200, app.job(q.get("id", "")))
                if url.path == "/api/download":
                    job = app.jobs.get(q.get("id", ""))
                    if job is None or not job["done"] or not job["path"].is_file():
                        return self._json(404, {"error": "no file"})
                    return self._send(200, job["path"].read_bytes(), "text/csv; charset=utf-8",
                                      {"Content-Disposition": 'attachment; filename="flashcards.csv"'})
            except KeyError as e:
                return self._json(404, {"error": str(e).strip("'\"")})
            self._json(404, {"error": "not found"})

        def do_POST(self):
            if not self._local():
                return self._json(HTTPStatus.FORBIDDEN, {"error": "local access only"})
            method = POST_ROUTES.get(urlparse(self.path).path)
            if method is None:
                return self._json(404, {"error": "not found"})
            origin = self.headers.get("Origin")
            if (self.headers.get("Content-Type", "").split(";")[0] != "application/json"
                    or (origin and origin != f"http://{self.headers.get('Host')}")):
                return self._json(HTTPStatus.FORBIDDEN, {"error": "same-origin JSON only"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = -1
            if not 0 <= length <= MAX_BODY:
                return self._json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "body too large"})
            try:
                body = json.loads(self.rfile.read(length) or b"{}")
                if not isinstance(body, dict):
                    raise TypeError("body must be an object")
                self._json(200, getattr(app, method)(body))
            except (ValueError, TypeError, json.JSONDecodeError) as e:
                self._json(400, {"error": str(e)})
            except KeyError as e:
                self._json(404, {"error": str(e).strip("'\"")})
            except llm.OllamaError as e:
                self._json(502, {"error": f"model server: {e}"})

    return Handler


def serve(cfg, index, port=8765, say=print):
    app = App(cfg, index)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), make_handler(app))
    httpd.daemon_threads = True
    say(f"study web: http://127.0.0.1:{httpd.server_address[1]}/  (Ctrl-C to stop)")
    say(f"  question bank: {len(app.bank)} fixed questions "
        f"({', '.join(f'{k} {v}' for k, v in collections.Counter(i.get('set', i['source']) for i in app.bank.values()).items())})")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return httpd
