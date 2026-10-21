"""Build a printable PDF of the whole guide from the docs.

Concatenates docs/index.md and the seven pages (not the mind map, which needs a
browser) into one US Letter document with a contents page, running headers,
page numbers and table rows that do not split across pages, then renders it
with WeasyPrint. The site build publishes the result next to the site.

Usage: python3 scripts/build_pdf.py --out site/ProjectPlus-PK0-005.pdf [--commit SHA]
"""
import argparse
import re
import sys
from html import escape
from pathlib import Path
from urllib.parse import unquote, urlparse

import markdown
from markdown.extensions.toc import slugify
from weasyprint import CSS, HTML
from weasyprint.urls import FatalURLFetchingError, URLFetcher

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PAGES = ["index.md", "01-concepts.md", "02-lifecycle.md", "03-tools.md", "04-it-governance.md", "05-gaps.md", "06-cheatsheet.md", "07-practice.md"]

STYLE = """
@page { size: Letter; margin: 0.7in 0.6in 0.75in;
  @bottom-center { content: counter(page); font: 8pt sans-serif; color: #555; }
  @top-right { content: string(chapter); font: 8pt sans-serif; color: #555; } }
@page :first { @top-right { content: none; } @bottom-center { content: none; } }
html { font: 9.5pt/1.4 "DejaVu Sans", sans-serif; color: #111; }
h1 { string-set: chapter content(); font-size: 18pt; border-bottom: 2pt solid #3f51b5; padding-bottom: 3pt; margin: 0 0 8pt; break-before: page; }
h1.cover, .contents h1 { break-before: auto; }
h3 { font-size: 12pt; margin: 14pt 0 4pt; color: #283593; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 10pt 0 3pt; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 8.5pt; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th, td { border: 0.5pt solid #bbb; padding: 2pt 4pt; vertical-align: top; text-align: left; }
th { background: #e8eaf6; }
code, pre { font: 8.5pt "DejaVu Sans Mono", monospace; background: #f3f3f3; }
pre { padding: 4pt 6pt; break-inside: avoid; }
.admonition { border-left: 3pt solid #3f51b5; background: #f1f3fb; padding: 3pt 8pt; margin: 6pt 0; break-inside: avoid; }
.admonition-title { font-weight: bold; margin: 0 0 2pt; }
.admonition p, .admonition ul { margin: 2pt 0; }
a { color: inherit; text-decoration: none; }
.cover { margin-top: 2.2in; font-size: 28pt; border: 0; text-align: center; }
.cover-page { break-after: page; }
.sub { text-align: center; font-size: 12pt; }
.small { text-align: center; font-size: 8.5pt; color: #555; margin-top: 2in; }
.contents ul { list-style: none; padding-left: 0; }
.contents li { margin: 2pt 0; }
.contents li.ch { margin-top: 8pt; font-weight: bold; }
.contents a::after { content: leader('.') target-counter(attr(href), page); }
"""


class LocalOnly(URLFetcher):
    """Fetch only data: URLs and files under docs/. A page that asks for anything
    else (an image on the network, a file:// path elsewhere) fails the build,
    because the PDF is published and the build runs with the runner's files."""

    def fetch(self, url, headers=None):
        if not url.startswith("data:"):
            parsed = urlparse(url)
            if parsed.scheme != "file" or not Path(unquote(parsed.path)).resolve().is_relative_to(DOCS.resolve()):
                raise FatalURLFetchingError(f"the PDF build may not fetch {url}")
        return super().fetch(url, headers)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--commit", default="unknown")
    args = ap.parse_args()

    site = re.search(r"^site_url:\s*(\S+)", (ROOT / "mkdocs.yml").read_text(), re.MULTILINE)
    if not site:
        sys.exit("mkdocs.yml has no site_url")
    site_url = site.group(1).rstrip("/")

    ids = {p: "p-" + Path(p).stem for p in PAGES}
    sections, toc = [], []
    for p in PAGES:
        text = (DOCS / p).read_text()
        title = re.match(r"# (.+)", text).group(1)
        if p == "index.md":
            text = text.split("\n", 1)[1]  # the cover carries the title
            title = "Start here"
            text = "# Start here\n" + text
        # Links between pages become in-document anchors; the mind map stays on the site.
        text = re.sub(r"\]\(mindmap\.md\)", f"]({site_url}/mindmap-full.html)", text)
        text = re.sub(r"\]\((\d\d-[\w-]+\.md|index\.md)(?:#([\w-]*))?\)", lambda m: f"](#{ids[m.group(1)]}{'-' + m.group(2) if m.group(2) else ''})", text)
        if p == "index.md":  # the bullets point at the sidebar and the site; print has neither
            text = re.sub(r"^- \*\*(Read|See it whole|Memorize|Test yourself|Print|Cram):\*\*.*\n?", "", text, flags=re.MULTILINE)
        prefix = ids[p]
        html = markdown.markdown(
            text,
            extensions=["tables", "admonition", "attr_list", "fenced_code", "sane_lists", "toc"],
            extension_configs={"toc": {"slugify": lambda value, sep, prefix=prefix: f"{prefix}-{slugify(value, sep)}"}},
        )
        sections.append(f'<section id="{ids[p]}">{html}</section>')
        toc.append((ids[p], re.sub(r"\s*\(\d+%\)", "", title)))

    items = [f'<li class="ch"><a href="#{sid}">{escape(title)}</a></li>' for sid, title in toc]
    contents = '<div class="contents"><h1>Contents</h1><ul>' + "".join(items) + "</ul></div>"
    stamp = args.commit[:7] if args.commit != "unknown" else ""
    cover = (
        '<div class="cover-page"><h1 class="cover">Project+ Without The Bullshit</h1>'
        '<p class="sub">CompTIA Project+ PK0-005 study guide</p>'
        f'<p class="small">Print edition{" · " + escape(stamp) if stamp else ""}<br>Latest version: {escape(site_url)}/<br>'
        "Not affiliated with CompTIA. MIT licensed.</p></div>"
    )
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Project+ Without The Bullshit</title></head><body>{cover}{contents}{"".join(sections)}</body></html>'

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fetcher = LocalOnly()
    HTML(string=doc, base_url=str(DOCS), url_fetcher=fetcher).write_pdf(
        args.out, stylesheets=[CSS(string=STYLE, url_fetcher=fetcher)]
    )
    print(f"pdf: {args.out} ({args.out.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    main()
