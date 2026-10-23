"""Fixed question banks parsed in code: the book's chapter-review questions and the guide's practice file.

No model is involved, so these are instant and the answer keys are the sources' own.
An item is {id, source, chapter, n, question, choices, answer (list of indexes),
explanation, ref}. Anything that does not parse cleanly is dropped, never guessed.
"""
import json
import re
from pathlib import Path

LETTERS = "ABCDEFGH"
_CHOICE = re.compile(r"(?:(?<=\s)|^)([A-H])\. ")


QUESTION_START = r"(?=[A-Z\"“(])"  # a stem starts with a capital, never '2. is'
ANSWER_START = r"(?=[A-H](?:\s*(?:,|and)\s*[A-H])*\. )"  # '2. A, C. why', never '2. is'


def _split_numbered(text: str, lead: str) -> dict[int, str]:
    """Split '1. ... 2. ... 3. ...' on the next expected number that looks like the
    start of an item, so a '2. ' inside a sentence is never taken for a new item."""
    parts, pos, n = {}, 0, 1
    start = None
    while True:
        m = re.compile(rf"(?:(?<=\s)|^){n}\. {lead}").search(text, pos)
        if not m:
            break
        if start is not None:
            parts[n - 1] = text[start:m.start()].strip()
        start, pos, n = m.end(), m.end(), n + 1
    if start is not None:
        parts[n - 1] = text[start:].strip()
    return parts


def _choices(body: str):
    """(stem, [choice texts]) with choices lettered A, B, C ... in order, or None."""
    marks = list(_CHOICE.finditer(body))
    want = 0
    picked = []
    for m in marks:  # keep only the A, B, C ... run, in order
        if m.group(1) == LETTERS[want]:
            picked.append(m)
            want += 1
    if len(picked) < 3:
        return None
    stem = body[:picked[0].start()].strip()
    texts = []
    for i, m in enumerate(picked):
        end = picked[i + 1].start() if i + 1 < len(picked) else len(body)
        texts.append(body[m.end():end].strip())
    if not stem or not all(texts):
        return None
    return stem, texts


def _answers(body: str):
    m = re.match(r"((?:[A-H](?:\s*(?:,|and)\s*)?)+)\.\s*(.*)$", body, re.DOTALL)
    if not m:
        return None
    letters = re.findall(r"[A-H]", m.group(1))
    return [LETTERS.index(x) for x in letters], m.group(2).strip()


def _joined(chunks: list[dict], chapter: str, kind: str) -> str:
    return " ".join(c["text"] for c in chunks if c["source"] == "book"
                    and c["chapter"] == chapter and c["heading"].endswith(kind))


def book_items(chunks: list[dict]) -> list[dict]:
    items = []
    chapters = sorted({c["chapter"] for c in chunks if c["source"] == "book"},
                      key=lambda s: (not s.isdigit(), int(s) if s.isdigit() else 0, s))
    for ch in chapters:
        questions, answers = (_joined(chunks, ch, "Questions"), _joined(chunks, ch, "Answers"))
        if not questions or not answers:
            continue
        keys = _split_numbered(answers, ANSWER_START)
        for n, body in _split_numbered(questions, QUESTION_START).items():
            parsed, key = _choices(body), _answers(keys.get(n, ""))
            if not parsed or not key:
                continue
            stem, texts = parsed
            picks, why = key
            if any(i >= len(texts) for i in picks):
                continue
            items.append({
                "id": f"book-ch{ch}-q{n}", "source": "book", "chapter": ch, "n": n,
                "question": stem, "choices": texts, "answer": sorted(set(picks)),
                "explanation": why, "ref": f"Ch {ch}, chapter review, question {n}",
            })
    return items


def guide_items(path: Path) -> list[dict]:
    """Parse docs/07-practice.md: '**N.** stem', '- A. choice' bullets, then an
    '### Answers' section with '**N. A.** explanation' (or 'A, C')."""
    if not path.is_file():
        return []
    text = path.read_text()
    body, _, key_text = text.partition("### Answers")
    keys = {}
    for m in re.finditer(r"^\*\*(\d+)\. ([A-H](?:(?:,| and) ?[A-H])*)\.\*\* (.*)$", key_text, re.MULTILINE):
        letters = re.findall(r"[A-H]", m.group(2))
        keys[int(m.group(1))] = ([LETTERS.index(x) for x in letters], m.group(3).strip())
    items, domain = [], ""
    blocks = re.split(r"^(?=(?:### |\*\*\d+\.\*\* ))", body, flags=re.MULTILINE)
    for block in blocks:
        if block.startswith("### "):
            domain = block[4:].strip().splitlines()[0]
            continue
        m = re.match(r"\*\*(\d+)\.\*\* (.*)", block, re.DOTALL)
        if not m or int(m.group(1)) not in keys:
            continue
        n = int(m.group(1))
        stem_lines, texts = [], []
        for line in m.group(2).splitlines():
            cm = re.match(r"- ([A-H])\. (.*)", line)
            if cm and cm.group(1) == LETTERS[len(texts)]:
                texts.append(cm.group(2).strip())
            elif not texts and line.strip():
                stem_lines.append(line.strip())
        picks, why = keys[n]
        if len(texts) < 3 or any(i >= len(texts) for i in picks):
            continue
        items.append({
            "id": f"guide-q{n}", "source": "guide", "chapter": domain.split()[0] if domain else "",
            "n": n, "question": " ".join(stem_lines).replace("**", ""), "choices": texts,
            "answer": sorted(set(picks)), "explanation": re.sub(r"\s*See \[[^\]]*\]\([^)]*\)\.?$", "", why),
            "ref": f"guide 07-practice.md, question {n}" + (f" ({domain})" if domain else ""),
        })
    return items


GENERATED = "generated-bank.jsonl"


def generated_items(path: Path) -> list[dict]:
    """Items written by `study build-bank`, in the same shape as the fixed banks."""
    if not path.is_file():
        return []
    items = []
    for line in path.read_text().splitlines():
        try:
            row = json.loads(line)
            ok = (isinstance(row["answer"], list) and row["choices"] and row["question"]
                  and all(0 <= i < len(row["choices"]) for i in row["answer"]))
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
        if ok:
            items.append(row | {"set": "generated"})
    return items
