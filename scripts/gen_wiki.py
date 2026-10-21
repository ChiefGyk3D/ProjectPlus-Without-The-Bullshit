"""Build the GitHub wiki from the docs.

The wiki is a generated mirror of docs/, never a place to write: the publish
workflow replaces every page with what this script writes. Standard library
only.

  Home                     what this is, the exam at a glance, every objective
  1.0 .. 4.0               one page per domain, listing its objectives
  1.1 .. 4.5               one page per exam objective, split from the domain pages
  Gaps-from-the-book       docs/05-gaps.md
  Cheat-sheet              docs/06-cheatsheet.md
  Mind-map, Flashcards     where the generated study aids live
  _Sidebar, _Footer        navigation and the "edit docs/, not the wiki" notice

MkDocs-only syntax (admonitions, attr_list) is rewritten to plain Markdown and
relative links are pointed at wiki pages. A leftover relative link or admonition
fails the run, so a broken wiki is caught in review rather than published.

Usage: python3 scripts/gen_wiki.py --out wiki-out [--commit SHA]
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

DOMAIN_FILES = ["01-concepts.md", "02-lifecycle.md", "03-tools.md", "04-it-governance.md"]
GAPS_PAGE = "Gaps-from-the-book"
CHEAT_PAGE = "Cheat-sheet"
MINDMAP_PAGE = "Mind-map"
ANKI_PAGE = "Flashcards"
BUILD_PAGE = "How-this-is-built"


def mkdocs_setting(key: str) -> str:
    m = re.search(rf"^{key}:\s*(\S+)", (ROOT / "mkdocs.yml").read_text(), re.MULTILINE)
    if not m:
        sys.exit(f"mkdocs.yml has no {key}")
    return m.group(1).rstrip("/")


SITE = mkdocs_setting("site_url")
REPO = mkdocs_setting("repo_url")


def page_name(heading: str) -> str:
    """Wiki file name for a heading: words joined by hyphens, punctuation dropped."""
    words = re.sub(r"[^\w.\s-]", "", heading).split()
    return "-".join(words)


def clean(cell: str) -> str:
    cell = re.sub(r"\*\*|`", "", cell)
    cell = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cell)
    return cell.replace("\\", "").strip()


def count_rows(text: str) -> int:
    """Table body rows: what the flashcards and the mind map are built from."""
    lines = text.split("\n")
    n = 0
    for i, ln in enumerate(lines):
        if not ln.startswith("|") or re.match(r"^\|\s*-", ln):
            continue
        if i + 1 < len(lines) and re.match(r"^\|\s*-", lines[i + 1]):
            continue  # header row
        n += 1
    return n


def split_domain(path: Path):
    """(domain title, weight, intro text, [(objective heading, body)])."""
    lines = path.read_text().split("\n")
    m = re.match(r"# (.+?)\s*\((\d+%)\)\s*$", lines[0])
    if not m:
        sys.exit(f"{path.name}: first line must be '# N.0 Title (NN%)'")
    title, weight = m.groups()
    intro: list[str] = []
    objectives: list[tuple[str, list[str]]] = []
    for ln in lines[1:]:
        if ln.startswith("### "):
            objectives.append((ln[4:].strip(), []))
        elif objectives:
            objectives[-1][1].append(ln)
        else:
            intro.append(ln)
    return title, weight, "\n".join(intro).strip(), [(h, "\n".join(b).strip()) for h, b in objectives]


def convert_admonitions(text: str) -> str:
    """'!!! tip "Title"' plus an indented body becomes a titled blockquote."""
    out: list[str] = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r'^!!! (\w+)(?: "(.*)")?\s*$', lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        kind, title = m.groups()
        title = title or kind.capitalize()
        i += 1
        body: list[str] = []
        while i < len(lines) and (lines[i].startswith("    ") or (lines[i] == "" and i + 1 < len(lines) and lines[i + 1].startswith("    "))):
            body.append(lines[i][4:])
            i += 1
        if len(body) == 1:
            first = body[0]
            if first[:1].islower():
                first = first[0].upper() + first[1:]
            out.append(f"> **{title}:** {first}")
        else:
            out.append(f"> **{title}**")
            out.append(">")
            out.extend(("> " + b).rstrip() for b in body)
    return "\n".join(out)


def rewrite_links(text: str, pages: dict[str, str]) -> str:
    """Point relative links at wiki pages; drop attr_list suffixes."""
    text = re.sub(r"\)\{[^}]*\}", ")", text)

    def fix(m: re.Match) -> str:
        label, target = m.group(1), m.group(2)
        if re.match(r"[a-z]+://|#|mailto:", target):
            return m.group(0)
        base = target.split("#")[0]
        if base in pages:
            return f"[{label}]({pages[base]})"
        if base == "mindmap-full.html":
            return f"[{label}]({SITE}/mindmap-full.html)"
        sys.exit(f"unresolved relative link: ({target})")

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", fix, text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, required=True, help="directory to write the wiki into")
    parser.add_argument("--commit", default="unknown", help="source commit SHA for the footer")
    args = parser.parse_args()

    domains = [split_domain(DOCS / f) for f in DOMAIN_FILES]

    # Link targets: docs file name -> wiki page.
    pages: dict[str, str] = {
        "05-gaps.md": GAPS_PAGE,
        "06-cheatsheet.md": CHEAT_PAGE,
        "mindmap.md": MINDMAP_PAGE,
        "index.md": "Home",
    }
    for f, (title, _, _, _) in zip(DOMAIN_FILES, domains):
        pages[f] = page_name(title)

    out: dict[str, str] = {}
    toc: list[tuple[str, str, str, int]] = []  # domain page, objective page, objective heading, rows
    sidebar = ["**[Home](Home)**", "", "**Exam objectives**"]

    for (title, weight, intro, objectives), f in zip(domains, DOMAIN_FILES):
        dpage = page_name(title)
        sidebar.append(f"- [{title} ({weight})]({dpage})")
        listing = []
        for heading, body in objectives:
            opage = page_name(heading)
            rows = count_rows(body)
            toc.append((dpage, opage, heading, rows))
            sidebar.append(f"  - [{heading}]({opage})")
            listing.append(f"- [{heading}]({opage})")
            body = rewrite_links(convert_admonitions(body), pages)
            out[opage] = f"# {heading}\n\nPart of [{title} ({weight})]({dpage}).\n\n{body}\n"
        intro = rewrite_links(convert_admonitions(intro), pages)
        out[dpage] = f"# {title} ({weight})\n\n{intro}\n\n## Objectives\n\n" + "\n".join(listing) + "\n"

    for src, page, heading in (("05-gaps.md", GAPS_PAGE, "Gaps from the book"), ("06-cheatsheet.md", CHEAT_PAGE, "Cheat sheet")):
        body = (DOCS / src).read_text().split("\n", 1)[1].strip()
        out[page] = f"# {heading}\n\n{rewrite_links(convert_admonitions(body), pages)}\n"
    sidebar += ["", "**Cram**", f"- [{CHEAT_PAGE.replace('-', ' ')}]({CHEAT_PAGE})", f"- [Gaps from the book]({GAPS_PAGE})"]

    mindmap_rows = sum(r for *_, r in toc)
    out[MINDMAP_PAGE] = (
        "# Mind map\n\n"
        "The whole exam on one screen: domain, objective, then every term, with its definition one click away.\n\n"
        f"**[Open the mind map]({SITE}/mindmap-full.html)** (it needs a browser; a wiki cannot embed it).\n\n"
        f"It is generated from the domain pages by `scripts/build_mindmap.py`.\n"
    )
    out[ANKI_PAGE] = (
        "# Flashcards\n\n"
        f"[`anki/projectplus.csv`]({REPO}/blob/main/anki/projectplus.csv) has one card for every table row in the guide, "
        "tagged with the objective it came from.\n\n"
        "Import it in Anki with **File → Import**, field separator **comma**, **Allow HTML off**, "
        "first row is the header, tags in the third field.\n\n"
        "The file is generated by `scripts/build_anki.py`. Edit the pages, not the CSV.\n"
    )
    out[BUILD_PAGE] = (
        "# How this is built\n\n"
        f"The pages in `docs/` are the source. The [site]({SITE}/), this wiki, the mind map and the flashcards are all generated from them.\n\n"
        "| Output | Built by |\n| --- | --- |\n"
        f"| [Site]({SITE}/) | `mkdocs build --strict` |\n"
        "| Mind map | `scripts/build_mindmap.py` |\n"
        "| Flashcards | `scripts/build_anki.py` |\n"
        f"| [PDF]({SITE}/ProjectPlus-PK0-005.pdf) | `scripts/build_pdf.py` (WeasyPrint), deployed with the site |\n"
        "| This wiki | `scripts/gen_wiki.py`, published by `.github/workflows/wiki.yml` |\n\n"
        "**Do not edit the wiki.** Every publish replaces every page. Edit `docs/`, open a pull request, and the wiki follows when it merges to `main`.\n\n"
        "CI regenerates the mind map and the flashcards and fails if they are stale, and fails if the wiki generator finds a link it cannot resolve. "
        f"All of it comes from [git-your-ship-together](https://github.com/ChiefGyk3D/git-your-ship-together). "
        f"Source: [{REPO.split('github.com/')[1]}]({REPO}).\n"
    )
    sidebar += ["", "**More**", f"- [Mind map]({MINDMAP_PAGE})", f"- [Flashcards]({ANKI_PAGE})", f"- [How this is built]({BUILD_PAGE})", f"- [Read it as a site]({SITE}/)"]

    # Home: the exam at a glance, built from the index page, plus every objective.
    index = (DOCS / "index.md").read_text().split("\n", 1)[1].strip()
    index = index.split("\n\n", 1)[1]  # the tagline is repeated on Home already
    index = re.sub(r"^- \*\*(Read|See it whole|Memorize|Print|Cram):\*\*.*\n?", "", index, flags=re.MULTILINE).strip()
    index = rewrite_links(convert_admonitions(index), pages)
    table = ["| Objective | Domain | Terms |", "| --- | --- | ---: |"]
    for dpage, opage, heading, rows in toc:
        table.append(f"| [{heading}]({opage}) | [{dpage.replace('-', ' ')}]({dpage}) | {rows} |")
    out["Home"] = (
        "# Project+ Without The Bullshit\n\n"
        "A CompTIA Project+ PK0-005 study guide for people who already know how to run projects and just need the cert. "
        "Every objective, the terms, the traps, nothing else.\n\n"
        f"Prefer a sidebar and search? Read it as a [site]({SITE}/).\n\n"
        "| Want to | Go to |\n| --- | --- |\n"
        f"| See the whole exam on one screen | [Mind map]({MINDMAP_PAGE}) |\n"
        f"| Drill terms with spaced repetition | [Flashcards]({ANKI_PAGE}) |\n"
        f"| Print it | [PDF]({SITE}/ProjectPlus-PK0-005.pdf), the whole guide on US Letter |\n"
        f"| Cram the night before | [Cheat sheet]({CHEAT_PAGE}) and [Gaps from the book]({GAPS_PAGE}) |\n\n"
        f"{index}\n\n"
        "## Every objective\n\n" + "\n".join(table) + "\n"
    )
    out["_Sidebar"] = "\n".join(sidebar) + "\n"
    stamp = args.commit[:7] if args.commit != "unknown" else "unknown commit"
    out["_Footer"] = (
        f"Generated from [`docs/`]({REPO}/tree/main/docs) at {stamp}. "
        f"Edit the docs, not the wiki. Not affiliated with CompTIA. MIT licensed.\n"
    )

    # A page that still carries MkDocs syntax or a dangling relative link is a bug.
    for name, text in out.items():
        if re.search(r"^!!! ", text, re.MULTILINE):
            sys.exit(f"{name}: admonition left unconverted")
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if target.startswith(("http://", "https://", "#")):
                continue
            if target not in out:
                sys.exit(f"{name}: link to missing page ({target})")
    if not out:
        sys.exit("nothing to write")

    args.out.mkdir(parents=True, exist_ok=True)
    for old in args.out.glob("*.md"):
        old.unlink()
    for name, text in out.items():
        (args.out / f"{name}.md").write_text(text)
    print(f"wiki: {len(out)} pages ({mindmap_rows} table rows across {len(toc)} objectives) -> {args.out}")


if __name__ == "__main__":
    main()
