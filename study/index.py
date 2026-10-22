"""Build, store and search the chunk index (dense vectors plus BM25 keywords)."""
import hashlib
import json
import math
import re
from array import array
from collections import Counter

from . import llm, sources

WORD = re.compile(r"[a-z0-9][a-z0-9+\-']*")
STOP = frozenset(
    ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "have", "how", "in", "is", "it", "its", "of", "on", "or", "that", "the", "this", "to", "was", "what", "when", "where", "which", "who", "why", "with", "do", "does", "you", "your", "i", "can", "should"]
)
K1, B = 1.4, 0.75


def tokens(text: str) -> list[str]:
    return [w for w in WORD.findall(text.lower()) if w not in STOP]


def _unit(vec: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def embed_text(chunk: dict) -> str:
    return f"{chunk['heading']}\n{chunk['text']}"


def fingerprint(cfg, chunks: list[dict]) -> str:
    h = hashlib.sha256(cfg.embed_model.encode())
    for c in chunks:
        h.update(c["id"].encode())
        h.update(c["text"].encode())
    return h.hexdigest()


class Index:
    def __init__(self, chunks, vectors, meta):
        self.chunks = chunks
        self.vectors = vectors  # list of array('f'), unit length
        self.meta = meta
        self._docs = [Counter(tokens(embed_text(c))) for c in chunks]
        self._len = [sum(d.values()) for d in self._docs]
        self._avg = (sum(self._len) / len(self._len)) if self._len else 1.0
        df = Counter()
        for d in self._docs:
            df.update(d.keys())
        n = len(chunks)
        self._idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def _dense(self, qvec):
        q = _unit(qvec)
        return [sum(a * b for a, b in zip(q, v)) for v in self.vectors]

    def _bm25(self, query: str):
        terms = tokens(query)
        scores = []
        for doc, length in zip(self._docs, self._len):
            s = 0.0
            for t in terms:
                f = doc.get(t, 0)
                if f:
                    s += self._idf.get(t, 0) * f * (K1 + 1) / (f + K1 * (1 - B + B * length / self._avg))
            scores.append(s)
        return scores

    def search(self, cfg, query: str, k: int = 6, allow=None) -> list[tuple[float, dict]]:
        """Reciprocal-rank fusion of dense and keyword ranks; allow(chunk) filters."""
        qvec = llm.embed(cfg, [cfg.embed_query_prefix + query])[0]
        dense, lexical = self._dense(qvec), self._bm25(query)
        pool = [i for i, c in enumerate(self.chunks) if allow is None or allow(c)]
        fused = Counter()
        for scores in (dense, lexical):
            ranked = sorted(pool, key=lambda i: scores[i], reverse=True)
            for rank, i in enumerate(ranked):
                if scores is lexical and scores[i] == 0:
                    break
                fused[i] += 1.0 / (60 + rank)
        top = [i for i, _ in fused.most_common(k)]
        return [(dense[i], self.chunks[i]) for i in top]


def build(cfg, chunks: list[dict], name: str, say=print) -> None:
    out = cfg.data_dir / name
    out.mkdir(parents=True, exist_ok=True)
    meta_path = out / "meta.json"
    fp = fingerprint(cfg, chunks)
    if meta_path.is_file() and json.loads(meta_path.read_text()).get("fingerprint") == fp:
        say(f"{name}: index is current ({len(chunks)} chunks)")
        return
    say(f"{name}: embedding {len(chunks)} chunks with {cfg.embed_model} ...")
    vectors = [_unit(v) for v in llm.embed(cfg, [embed_text(c) for c in chunks])]
    dims = len(vectors[0])
    flat = array("f")
    for v in vectors:
        flat.extend(v)
    (out / "vectors.f32").write_bytes(flat.tobytes())
    (out / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False))
    meta_path.write_text(json.dumps({
        "fingerprint": fp, "model": cfg.embed_model, "dims": dims, "count": len(chunks),
    }))
    say(f"{name}: wrote {len(chunks)} x {dims} vectors to {out}")


def load(cfg, names: list[str]) -> Index:
    chunks, vectors, meta = [], [], {}
    for name in names:
        d = cfg.data_dir / name
        if not (d / "meta.json").is_file():
            raise FileNotFoundError(f"no index for '{name}' - run: python3 -m study index")
        m = json.loads((d / "meta.json").read_text())
        if m["model"] != cfg.embed_model:
            raise ValueError(
                f"'{name}' was embedded with {m['model']}, config says {cfg.embed_model}; "
                "re-run: python3 -m study index"
            )
        flat = array("f")
        flat.frombytes((d / "vectors.f32").read_bytes())
        dims = m["dims"]
        part = json.loads((d / "chunks.json").read_text())
        chunks.extend(part)
        vectors.extend(flat[i * dims:(i + 1) * dims] for i in range(len(part)))
        meta[name] = m
    return Index(chunks, vectors, meta)


def build_all(cfg, say=print) -> None:
    if cfg.book:
        build(cfg, sources.book_chunks(cfg.book), "book", say)
    else:
        say("book: STUDY_BOOK is not set, skipping")
    build(cfg, sources.guide_chunks(cfg.guide_dir), "guide", say)
