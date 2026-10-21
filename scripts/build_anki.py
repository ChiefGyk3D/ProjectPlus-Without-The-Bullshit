"""Build the Anki flashcard CSV from the docs.

Every table row in docs/01-*.md through docs/06-*.md becomes a card: the first
column on the front, the rest on the back, tagged with the objective the table
sits under. Writes anki/projectplus.csv.

Two rules keep the cards usable. A table whose first column repeats (the
meeting types, grouped by category) uses "category: item" as the front. A front
that still appears in two places gets its objective appended, so no two cards
look the same. Tables with three or more columns label each back line with its
column header.

Each card carries a stable ID, so importing a newer file updates the cards you
already have instead of adding duplicates. The file starts with Anki header
lines (Anki 2.1.54 or later), so the import dialog needs no settings: File ->
Import, pick the file, Import.
"""
import csv
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "anki" / "projectplus.csv"

HEADER = """#separator:Comma
#html:false
#notetype:Basic
#deck:Project+ PK0-005
#columns:Front,Back,Tags,GUID
#tags column:3
#guid column:4
"""


def clean(cell: str) -> str:
    cell = re.sub(r"\*\*|`", "", cell)
    cell = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cell)
    return cell.replace("\\", "").strip()


def is_sep(line: str) -> bool:
    return re.match(r"^\|\s*-", line) is not None


def label_for(section: str, page: str) -> str:
    """Short objective label for telling duplicate fronts apart."""
    m = re.match(r"(\d+\.\d+)", section)
    if m:
        return m.group(1)
    return {"05-gaps": "gaps", "06-cheatsheet": "cheat sheet"}.get(page, page)


# (front, back lines, section, page) per row, grouped by table.
tables = []
for page in sorted(DOCS.glob("0[1-6]-*.md")):
    lines = page.read_text().split("\n")
    section = page.stem
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith(("## ", "### ")):
            section = ln.lstrip("# ").strip()
        if ln.startswith("|") and i + 1 < len(lines) and is_sep(lines[i + 1]):
            header = [clean(c) for c in ln.strip().strip("|").split("|")]
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([clean(c) for c in lines[i].strip().strip("|").split("|")])
                i += 1
            tables.append((header, rows, section, page.stem))
            continue
        i += 1

cards = []  # [front, back, section, page]
for header, rows, section, page in tables:
    rows = [r for r in rows if len(r) >= 2 and r[0] and r[1]]
    firsts = [r[0].lower() for r in rows]
    grouped = len(set(firsts)) < len(firsts)  # first column is a category, not a term
    for cells in rows:
        if grouped and len(cells) >= 3:
            front, rest, rest_hdr = f"{cells[0]}: {cells[1]}", cells[2:], header[2:]
        else:
            front, rest, rest_hdr = cells[0], cells[1:], header[1:]
        parts = []
        for j, c in enumerate(rest):
            if not c or c.lower() == "n/a":
                continue
            label = rest_hdr[j] if j < len(rest_hdr) and len(rest) > 1 else ""
            parts.append(f"{label}: {c}" if label else c)
        if parts:
            cards.append([front, "\n".join(parts), section, page])

seen: dict[str, int] = {}
for c in cards:
    seen[c[0].lower()] = seen.get(c[0].lower(), 0) + 1
for c in cards:
    if seen[c[0].lower()] > 1:
        c[0] = f"{c[0]} ({label_for(c[2], c[3])})"

rows_out = []
guids = set()
for front, back, section, _ in cards:
    tag = "ProjectPlus::" + re.sub(r"[^A-Za-z0-9]+", "_", section).strip("_")
    guid = hashlib.sha1(f"{tag}|{front}".encode()).hexdigest()[:12]
    if guid in guids:
        raise SystemExit(f"duplicate card: {front!r} under {section!r}")
    guids.add(guid)
    rows_out.append((front, back, tag, guid))

OUT.parent.mkdir(exist_ok=True)
with OUT.open("w", newline="") as f:
    f.write(HEADER)
    csv.writer(f).writerows(rows_out)
print(f"anki: {len(rows_out)} cards -> {OUT.relative_to(ROOT)}")
