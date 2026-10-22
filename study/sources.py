"""Turn the epub and the guide pages into labeled chunks.

A chunk is a dict: id, source ("book" or "guide"), ref (what the learner sees
as the citation), chapter (key for --chapter), heading path, text.
"""
import posixpath
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

TARGET = 1100   # characters a chunk grows to before it is closed
MAX = 1800      # hard ceiling for one chunk
MIN = 200       # a trailing scrap shorter than this joins the previous chunk
INCLUDE = re.compile(r"^(intro|ch\d+|app[A-Z]|glossary)$")
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "div", "blockquote"}
HEADINGS = {"h2": 2, "h3": 3, "h4": 4}
SKIP = {"script", "style", "head"}


class _Blocks(HTMLParser):
    """Yield ("heading", level, cls, text, page) and ("text", text, page)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.events = []
        self.page = None
        self._buf = []
        self._skip = 0
        self._heading = None  # (level, class) while inside a heading

    def _flush(self):
        text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
        self._buf = []
        if not text:
            return
        if self._heading:
            self.events.append(("heading", *self._heading, text, self.page))
        else:
            self.events.append(("text", text, self.page))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP:
            self._skip += 1
        if a.get("epub:type") == "pagebreak" or str(a.get("id", "")).startswith("page_"):
            m = re.match(r"page_(\d+)$", str(a.get("id", "")))
            if m:
                self.page = int(m.group(1))
        if tag in BLOCK:
            self._flush()
            self._heading = (HEADINGS[tag], a.get("class", "")) if tag in HEADINGS else None
        elif tag == "br":
            self._buf.append(" ")

    def handle_endtag(self, tag):
        if tag in SKIP and self._skip:
            self._skip -= 1
        if tag in BLOCK:
            self._flush()
            self._heading = None

    def handle_data(self, data):
        if not self._skip:
            self._buf.append(data)

    def close(self):
        super().close()
        self._flush()


def _xml(data: bytes):
    """Parse package XML, refusing entity tricks (stdlib parsers expand them)."""
    if re.search(rb"<!(DOCTYPE|ENTITY)", data, re.IGNORECASE):
        raise ValueError("epub package XML declares a DOCTYPE or ENTITY; refusing to parse")
    return ET.fromstring(data)


def _package(zf: zipfile.ZipFile):
    root = _xml(zf.read("META-INF/container.xml"))
    opf = root.find(".//{*}rootfile").attrib["full-path"]
    pkg = _xml(zf.read(opf))
    base = posixpath.dirname(opf)
    manifest = {i.attrib["id"]: i.attrib["href"] for i in pkg.iterfind(".//{*}manifest/{*}item")}
    spine = [r.attrib["idref"] for r in pkg.iterfind(".//{*}spine/{*}itemref")]
    return base, manifest, spine


def _chapter_key(idref: str) -> str:
    m = re.match(r"ch(\d+)$", idref)
    if m:
        return m.group(1)
    return {"intro": "intro", "glossary": "glossary"}.get(idref, idref.lower())


def _chapter_label(idref: str) -> str:
    m = re.match(r"ch(\d+)$", idref)
    if m:
        return f"Ch {m.group(1)}"
    if idref.startswith("app"):
        return f"Appendix {idref[3:]}"
    return idref.capitalize()


def _pack(blocks: list[tuple[str, int | None]]) -> list[tuple[str, int | None, int | None]]:
    """Group consecutive blocks into ~TARGET-sized (text, first page, last page)."""
    out, cur, first, last = [], [], None, None
    size = 0
    for text, page in blocks:
        pieces = [text]
        if len(text) > MAX:  # a very long block: split at sentence ends
            pieces = re.split(r"(?<=[.!?])\s+", text)
        for piece in pieces:
            if cur and size + len(piece) > MAX or (size >= TARGET and cur):
                out.append((" ".join(cur), first, last))
                cur, size, first = [], 0, None
            if first is None:
                first = page
            last = page
            cur.append(piece)
            size += len(piece) + 1
    if cur:
        text = " ".join(cur)
        if out and len(text) < MIN:
            prev = out.pop()
            out.append((prev[0] + " " + text, prev[1], last))
        else:
            out.append((text, first, last))
    return out


def book_chunks(epub: Path) -> list[dict]:
    chunks = []
    with zipfile.ZipFile(epub) as zf:
        base, manifest, spine = _package(zf)
        for idref in spine:
            if not INCLUDE.match(idref) or idref not in manifest:
                continue
            parser = _Blocks()
            parser.feed(zf.read(posixpath.join(base, manifest[idref])).decode("utf8"))
            parser.close()
            chapter_title, h3, h4 = "", "", ""
            section, blocks = ("", ""), []

            def close(section, blocks, idref=idref, chapter_title=chapter_title):
                for text, p1, p2 in _pack(blocks):
                    chunks.append(_make_chunk(idref, chapter_title, section, text, p1, p2, len(chunks)))

            for ev in parser.events:
                if ev[0] == "heading":
                    _, level, cls, text, _page = ev
                    if cls == "h2chap":
                        chapter_title = text
                        continue
                    if level == 2:  # the "CHAPTER 3" marker, not a section
                        continue
                    close(section, blocks, chapter_title=chapter_title)
                    blocks = []
                    if level == 3:
                        h3, h4 = text, ""
                    else:
                        h4 = text
                    section = (h3, h4)
                else:
                    blocks.append((ev[1], ev[2]))
            close(section, blocks, chapter_title=chapter_title)
    return chunks


def _make_chunk(idref, chapter_title, section, text, p1, p2, n):
    label = _chapter_label(idref)
    path = [x for x in (chapter_title, *section) if x]
    pages = ""
    if p1:
        pages = f", p. {p1}" if not p2 or p2 == p1 else f", pp. {p1}-{p2}"
    where = " > ".join(path[1:]) if len(path) > 1 else ""
    ref = f"{label}{pages}" + (f" - {where}" if where else "")
    return {
        "id": f"book-{n:04d}",
        "source": "book",
        "ref": ref,
        "chapter": _chapter_key(idref),
        "heading": " > ".join(path),
        "text": text,
    }


def guide_chunks(docs: Path) -> list[dict]:
    chunks = []
    for page in sorted(docs.glob("0[1-6]-*.md")):
        heading, blocks = page.stem, []

        def close(heading, blocks, page=page):
            body = "\n".join(blocks).strip()
            for text, _, _ in _pack([(b, None) for b in body.split("\n") if b.strip()]):
                chunks.append({
                    "id": f"guide-{len(chunks):04d}",
                    "source": "guide",
                    "ref": f"guide {page.name} - {heading}",
                    "chapter": page.stem.split("-")[0],
                    "heading": heading,
                    "text": re.sub(r"\*\*|`", "", text),
                })

        for line in page.read_text().splitlines():
            if line.startswith(("## ", "### ")):
                close(heading, blocks)
                heading, blocks = line.lstrip("# ").strip(), []
            elif not re.match(r"^\|\s*-", line):
                blocks.append(line)
        close(heading, blocks)
    return chunks
