"""The three study modes: ask, quiz, cards."""
import csv
import hashlib
import json
import random
import re
import time
from pathlib import Path

from . import grounding, llm

NOT_COVERED = "Not covered in the provided passages."
MIN_PASSAGE = 400  # skip scraps too short to write a good question from

ASK_SYSTEM = (
    "You are a study assistant for the CompTIA Project+ (PK0-005) exam. Answer ONLY "
    "from the numbered passages. Put the passage number in square brackets after each "
    "claim, like [2]. If the passages do not answer the question, reply exactly: "
    f"{NOT_COVERED} Be concise. Use American English."
)

QUIZ_SYSTEM = (
    "You write one multiple-choice exam question from a passage. Use ONLY the passage. "
    "Give the one correct answer and three plausible but wrong distractors that are about "
    "the same topic and similar in length; no joke or absurd options. 'evidence' must be a "
    "sentence or phrase copied EXACTLY from the passage that proves the correct answer. "
    "Use American English."
)
QUIZ_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "correct": {"type": "string"},
        "distractors": {"type": "array", "items": {"type": "string"},
                        "minItems": 3, "maxItems": 3},
        "evidence": {"type": "string"},
        "explanation": {"type": "string"},
    },
    "required": ["question", "correct", "distractors", "evidence", "explanation"],
}
SOLVE_SYSTEM = (
    "Answer the multiple-choice question using ONLY the passage. Reply with the index "
    "(0-3) of the choice the passage supports."
)
SOLVE_SCHEMA = {
    "type": "object",
    "properties": {"answer": {"type": "integer", "minimum": 0, "maximum": 3}},
    "required": ["answer"],
}

CARDS_SYSTEM = (
    "You write flashcards for exam study from a passage. Use ONLY the passage. Write one "
    "to three cards that each test one fact, with a short front (a question or term) and "
    "a short back. Each card's 'evidence' must be a sentence or phrase copied EXACTLY from "
    "the passage. Use American English."
)
CARDS_SCHEMA = {
    "type": "object",
    "properties": {
        "cards": {
            "type": "array", "minItems": 1, "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {"front": {"type": "string"}, "back": {"type": "string"},
                               "evidence": {"type": "string"}},
                "required": ["front", "back", "evidence"],
            },
        },
    },
    "required": ["cards"],
}


def allow_for(source: str, chapter: str | None):
    def allow(c):
        return (source == "both" or c["source"] == source) and (
            chapter is None or c["chapter"] == chapter)
    return allow


def ask(cfg, index, question: str, source="both", chapter=None, k=6):
    hits = index.search(cfg, question, k=k, allow=allow_for(source, chapter))
    if not hits:
        return NOT_COVERED, []
    passages = "\n\n".join(
        f"[{i}] ({c['ref']})\n{c['text']}" for i, (_, c) in enumerate(hits, 1))
    raw = llm.chat(cfg, ASK_SYSTEM, f"Passages:\n\n{passages}\n\nQuestion: {question}")
    answer, used = grounding.split_citations(raw, len(hits))
    if NOT_COVERED.lower() in answer.lower():
        return NOT_COVERED, []
    cites = [(n, hits[n - 1][1]["ref"], hits[n - 1][1]["source"]) for n in used]
    if not cites:
        answer += "\n\n(warning: the answer cited no passage - treat it as unverified)"
    return answer, cites


def pick(cfg, index, n, source, chapter, topic, seed=None):
    allow = allow_for(source, chapter)
    if topic:
        pool = [c for _, c in index.search(cfg, topic, k=max(n * 3, 12), allow=allow)]
    else:
        pool = [c for c in index.chunks if allow(c)]
        random.Random(seed).shuffle(pool)
    qa = re.compile(r"(Questions|Answers)$")  # end-of-chapter Q&A fragments
    return [c for c in pool if len(c["text"]) >= MIN_PASSAGE and not qa.search(c["heading"])]


def make_question(cfg, chunk, tries=3, rng=random):
    """One validated multiple-choice item from a chunk, or None.

    Checks in code: four distinct non-empty choices, evidence quoted verbatim from
    the passage, and an independent solver call that must pick the same choice.
    """
    prompt = f"Passage:\n{chunk['text']}"
    for _ in range(tries):
        try:
            item = json.loads(llm.chat(cfg, QUIZ_SYSTEM, prompt, QUIZ_SCHEMA))
            correct = str(item["correct"]).strip()
            choices = [correct] + [str(x).strip() for x in item["distractors"]]
            question = str(item["question"]).strip()
        except (json.JSONDecodeError, KeyError, TypeError, llm.OllamaError):
            continue
        if not (question and len(choices) == 4 and all(choices)
                and len({grounding.norm(x) for x in choices}) == 4
                and grounding.evidence_ok(str(item.get("evidence", "")), chunk["text"])):
            continue
        order = list(range(4))
        rng.shuffle(order)  # code decides the position, not the model
        shuffled = [choices[i] for i in order]
        answer = order.index(0)
        listing = "\n".join(f"{i}. {t}" for i, t in enumerate(shuffled))
        try:
            solved = json.loads(llm.chat(
                cfg, SOLVE_SYSTEM, f"{prompt}\n\nQuestion: {question}\n{listing}",
                SOLVE_SCHEMA))["answer"]
        except (json.JSONDecodeError, KeyError, TypeError, llm.OllamaError):
            continue
        if solved != answer:
            continue
        return {
            "question": question, "choices": shuffled, "answer": answer,
            "evidence": item["evidence"].strip(),
            "explanation": str(item.get("explanation", "")).strip(),
            "ref": chunk["ref"], "chunk": chunk["id"], "source": chunk["source"],
        }
    return None


def quiz(cfg, index, n, source, chapter, topic, interactive, seed, data_dir: Path,
         read=input, out=print):
    pool = pick(cfg, index, n, source, chapter, topic, seed)
    rng = random.Random(seed)
    asked, right, missed = 0, 0, []
    log = (data_dir / "quiz-log.jsonl").open("a")
    for chunk in pool:
        if asked >= n:
            break
        item = make_question(cfg, chunk, rng=rng)
        if item is None:
            continue
        asked += 1
        out(f"\nQ{asked}. {item['question']}")
        for letter, text in zip("ABCD", item["choices"]):
            out(f"  {letter}. {text}")
        correct = "ABCD"[item["answer"]]
        if interactive:
            try:
                reply = read("Your answer (A-D): ").strip().upper()[:1]
            except EOFError:
                break
            got = reply == correct
        else:
            got = None
        if got is not None:
            right += got
            if not got:
                missed.append(item["ref"])
            out("Correct." if got else f"Not quite - the answer is {correct}.")
        else:
            out(f"Answer: {correct}")
        out(f"  Why: {item['explanation']}")
        who = "Book" if item["source"] == "book" else "Guide"
        out(f"  {who} says: \"{item['evidence']}\"  [{item['ref']}]")
        log.write(json.dumps({"t": int(time.time()), "chunk": item["chunk"],
                              "correct": got}) + "\n")
    log.close()
    if asked == 0:
        out("No question could be written from the selected material.")
    elif interactive:
        out(f"\nScore: {right}/{asked}")
        for ref in dict.fromkeys(missed):
            out(f"  review: {ref}")
    return asked


def make_cards(cfg, chunk, tries=2):
    prompt = f"Passage:\n{chunk['text']}"
    for _ in range(tries):
        try:
            data = json.loads(llm.chat(cfg, CARDS_SYSTEM, prompt, CARDS_SCHEMA))
        except (json.JSONDecodeError, llm.OllamaError):
            continue
        cards = []
        for c in data.get("cards", []):
            if (isinstance(c, dict) and str(c.get("front", "")).strip()
                    and str(c.get("back", "")).strip()
                    and grounding.evidence_ok(str(c.get("evidence", "")), chunk["text"])):
                cards.append({"front": c["front"].strip(), "back": c["back"].strip(),
                              "ref": chunk["ref"], "chapter": chunk["chapter"],
                              "source": chunk["source"]})
        if cards:
            return cards
    return []


def cards(cfg, index, source, chapter, topic, limit, seed, out_path: Path, out=print):
    pool = pick(cfg, index, limit or 10**6, source, chapter, topic, seed)
    if not topic:
        pool = sorted(pool, key=lambda c: c["id"])  # book order reads best
    if limit:
        pool = pool[:limit]
    seen, rows = set(), []
    for n, chunk in enumerate(pool, 1):
        out(f"  card chunk {n}/{len(pool)}: {chunk['ref']}")
        for card in make_cards(cfg, chunk):
            key = grounding.norm(card["front"])
            if key not in seen:
                seen.add(key)
                rows.append(card)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as fh:
        fh.write("#separator:Comma\n#html:false\n#notetype:Basic\n"
                 "#deck:Project+ PK0-005 (private study)\n"
                 "#columns:Front,Back,Tags,GUID\n#tags column:3\n#guid column:4\n")
        w = csv.writer(fh)
        for card in rows:
            tag = f"ProjectPlusStudy::{card['source']}::" + re.sub(
                r"[^A-Za-z0-9]+", "_", card["chapter"]).strip("_")
            guid = hashlib.sha1(("study|" + card["front"]).encode()).hexdigest()[:10]
            w.writerow([card["front"], f"{card['back']}\n\n[{card['ref']}]", tag, guid])
    out(f"wrote {len(rows)} cards to {out_path}")
    return len(rows)
