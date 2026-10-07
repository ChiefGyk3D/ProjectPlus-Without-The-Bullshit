"""Build the Anki flashcard CSV from the docs.

Every two-or-more-column table in docs/01-*.md through docs/06-*.md becomes
cards: first column on the front, the rest on the back, tagged with the
objective the table sits under. Writes anki/projectplus.csv.

Import in Anki with File -> Import, field separator comma, "Allow HTML" off,
first row is the header, tags in the third field.
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "anki" / "projectplus.csv"


def clean(cell: str) -> str:
    cell = re.sub(r"\*\*|`", "", cell)
    cell = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cell)
    return cell.replace("\\", "").strip()


rows = []
for page in sorted(DOCS.glob("0[1-6]-*.md")):
    text = page.read_text().split("\n")
    section = page.stem
    for i, ln in enumerate(text):
        if ln.startswith(("## ", "### ")):
            section = ln.lstrip("# ").strip()
        if not ln.startswith("|") or re.match(r"^\|\s*-", ln):
            continue
        if i + 1 < len(text) and re.match(r"^\|\s*-", text[i + 1]):
            continue  # header row
        cells = [clean(c) for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2 or not cells[0] or not cells[1]:
            continue
        back = " — ".join(c for c in cells[1:] if c and c.lower() != "n/a")
        tag = "ProjectPlus::" + re.sub(r"[^A-Za-z0-9]+", "_", section).strip("_")
        rows.append((cells[0], back, tag))

OUT.parent.mkdir(exist_ok=True)
with OUT.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Front", "Back", "Tags"])
    w.writerows(rows)
print(f"anki: {len(rows)} cards -> {OUT.relative_to(ROOT)}")
