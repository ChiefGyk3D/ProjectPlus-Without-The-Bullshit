"""Build the mind map from the docs.

Reads docs/01-*.md through docs/05-*.md and writes:
  docs/mindmap-full.html  a standalone markmap page (domain > objective > term)
  docs/mindmap.md         the site page that embeds it

Run from the repository root. No dependencies beyond the standard library. The
page runs d3 and markmap from docs/assets/vendor/ (see VENDOR.txt there), so it
loads nothing from a third party and works offline.
"""
import hashlib
import json
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

def slug(heading: str) -> str:
    """The anchor mkdocs' toc extension gives a heading."""
    h = re.sub(r"[^\w\s-]", "", heading).strip().lower()
    return re.sub(r"[\s]+", "-", h)


def clean(cell: str) -> str:
    cell = re.sub(r"\*\*|`", "", cell)
    cell = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cell)
    cell = cell.replace("\\", "").strip()
    # markmap renders node text as HTML; a cell is text, never markup.
    return cell.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def check_vendor() -> None:
    """The vendored libraries must match the checksums recorded in VENDOR.txt."""
    vendor = DOCS / "assets" / "vendor"
    listed = re.findall(r"^([0-9a-f]{64})  (\S+)$", (vendor / "VENDOR.txt").read_text(), re.MULTILINE)
    if not listed:
        raise SystemExit("assets/vendor/VENDOR.txt lists no checksums")
    for digest, name in listed:
        if hashlib.sha256((vendor / name).read_bytes()).hexdigest() != digest:
            raise SystemExit(f"assets/vendor/{name} does not match VENDOR.txt; update both together")


check_vendor()
lines = ["# CompTIA Project+ PK0-005"]
terms = 0
for page in sorted(DOCS.glob("0[1-5]-*.md")):
    text = page.read_text().split("\n")
    page_url = page.stem + "/"
    section_url = page_url
    header: list[str] = []
    for i, ln in enumerate(text):
        if ln.startswith("# "):
            lines.append("## " + re.sub(r"\s*\(\d+%\)", "", ln[2:].strip()))
        elif ln.startswith("### "):
            # H3 inside the gaps page are sub-topics of a H2; keep depth consistent
            lines.append("#### " + ln[4:].strip())
            section_url = page_url + "#" + slug(ln[4:].strip())
        elif ln.startswith("## "):
            lines.append("### " + ln[3:].strip())
            section_url = page_url + "#" + slug(ln[3:].strip())
        elif ln.startswith("|") and section_url != page_url and not re.match(r"^\|\s*-", ln):
            cells = [clean(c) for c in ln.strip().strip("|").split("|")]
            next_is_sep = i + 1 < len(text) and re.match(r"^\|\s*-", text[i + 1]) is not None
            if next_is_sep:
                header = cells
                continue
            if len(cells) < 2 or not cells[0] or len(cells[0]) >= 60:
                continue
            # Term node links to its section; the definition is a collapsed child.
            # Extra columns are labelled with their header so a 3-column row reads.
            lines.append(f"- [{cells[0]}]({section_url})")
            parts = []
            for j, c in enumerate(cells[1:], start=1):
                if not c or c.lower() == "n/a":
                    continue
                label = header[j] if j < len(header) and len(cells) > 2 else ""
                parts.append(f"**{label}:** {c}" if label else c)
            if parts:
                lines.append("  - " + " <br> ".join(parts))
                terms += 1

outline = "\n".join(lines) + "\n"
if "</script" in outline.lower() or "<!--" in outline:
    raise SystemExit("the outline contains markup that would end the embedding script early")
outline_json = json.dumps(outline)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Project+ mind map</title>
<style>
  /* Forced light scheme: markmap draws its labels in the page's text colour,
     and the OS dark theme otherwise leaves near-black text on a dark page. */
  :root {{ color-scheme: light only; }}
  html, body {{ margin: 0; height: 100%; background: #ffffff; color: #111111; }}
  .markmap {{ width: 100%; height: 100%; color: #111111; --markmap-text-color: #111111;
             --markmap-highlight-bg: #fff3b0; font: 15px/1.3 system-ui, sans-serif; }}
  .markmap > svg {{ width: 100%; height: 100%; background: #ffffff; }}
  .markmap-foreign {{ color: #111111 !important; }}
  .markmap-link {{ stroke-width: 2.5px; }}
  #hint {{ position: fixed; top: 8px; left: 12px; font: 13px system-ui, sans-serif; color: #555;
          background: rgba(255,255,255,.9); padding: 4px 8px; border-radius: 4px; }}
</style>
</head>
<body>
<div id="hint">Click a circle to expand or collapse. Click a term to open its definition; click the term text to jump to its section. Scroll to zoom, drag to pan.</div>
<div class="markmap"><svg id="mm"></svg></div>
<script src="assets/vendor/d3.min.js"></script>
<script src="assets/vendor/markmap-lib.min.js"></script>
<script src="assets/vendor/markmap-view.js"></script>
<script>
  const outline = {outline_json};
  const {{ Transformer, Markmap, deriveOptions }} = window.markmap;
  const {{ root }} = new Transformer().transform(outline);
  Markmap.create("#mm", deriveOptions({{
    colorFreezeLevel: 2,
    initialExpandLevel: 2,
    maxWidth: 360,
    spacingVertical: 8,
    paddingX: 12,
  }}), root);
</script>
<script>
  // A term links to its section on the site. Inside the embedded view that
  // link must replace the whole page, not just the frame.
  document.addEventListener("click", (e) => {{
    const a = e.target.closest("a[href]");
    if (a && window.top !== window) {{ e.preventDefault(); window.top.location = a.href; }}
  }});
</script>
</body>
</html>
"""
(DOCS / "mindmap-full.html").write_text(page)

(DOCS / "mindmap.md").write_text(
    "# Mind map\n\n"
    "The whole exam on one screen: domain, objective, then every term. "
    "Click a term to show its definition; click the term's text to jump to its section. "
    "[Open full screen](mindmap-full.html){ target=_blank }.\n\n"
    '<iframe src="mindmap-full.html" title="Project+ mind map" '
    'style="width:100%;height:80vh;border:1px solid var(--md-default-fg-color--lightest);border-radius:4px"></iframe>\n\n'
    f"Generated by `scripts/build_mindmap.py` from the domain pages; {terms} terms with definitions.\n"
)
print(f"mind map: {len(lines)} nodes, {terms} defined terms")
