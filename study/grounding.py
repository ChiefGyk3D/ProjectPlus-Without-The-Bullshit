"""Checks run in code on what the model returns. The model's word is never enough."""
import re

_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                         "–": "-", "—": "-", " ": " "})
MIN_EVIDENCE = 25


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.translate(_QUOTES)).strip().lower()


def evidence_ok(evidence: str, passage: str) -> bool:
    """True when the quoted evidence really appears in the passage."""
    e = norm(evidence).strip(" .\"'")
    return len(e) >= MIN_EVIDENCE and e in norm(passage)


def split_citations(answer: str, n_passages: int) -> tuple[str, list[int]]:
    """Return the answer without citation markers that point at nothing, and the
    sorted passage numbers that were really cited."""
    used = set()

    def keep(m):
        nums = [int(x) for x in re.findall(r"\d+", m.group(0))]
        good = [x for x in nums if 1 <= x <= n_passages]
        used.update(good)
        return "[" + ", ".join(str(x) for x in good) + "]" if good else ""

    cleaned = re.sub(r"\[\s*\d+(?:\s*[,;]\s*\d+)*\s*\]", keep, answer)
    return re.sub(r"[ \t]+\n", "\n", cleaned).strip(), sorted(used)
