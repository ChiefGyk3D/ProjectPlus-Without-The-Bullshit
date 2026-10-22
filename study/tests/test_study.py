"""Hermetic tests: no network, no real book. Run: python3 -m unittest discover -s study/tests -t ."""
import csv
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from typing import ClassVar
from unittest import mock

from study import config, grounding, modes, sources
from study import index as idx

PASSAGE = (
    "In a balanced matrix the project manager and the functional manager have equal "
    "power and autonomy over the project team. Team members report to two bosses. " * 4
)


def make_epub(path: Path, doctype: bool = False):
    head = '<!DOCTYPE x [<!ENTITY a "b">]>' if doctype else ""
    opf = (head + '<package xmlns="http://www.idpf.org/2007/opf"><manifest>'
           '<item id="ch1" href="ch1.xhtml"/><item id="ad" href="ad.xhtml"/></manifest>'
           '<spine><itemref idref="ch1"/><itemref idref="ad"/></spine></package>')
    container = ('<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
                 '<rootfile full-path="OEBPS/book.opf"/></rootfiles></container>')
    ch1 = ('<html><body><h2 class="h2">CHAPTER 1</h2><h2 class="h2chap">Launching</h2>'
           '<span epub:type="pagebreak" id="page_10"/><h3 class="h3">Structures</h3>'
           f'<p>{PASSAGE}</p><span id="page_11"/><h4 class="h4">Matrix</h4><p>{PASSAGE}</p>'
           '</body></html>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("META-INF/container.xml", container)
        z.writestr("OEBPS/book.opf", opf)
        z.writestr("OEBPS/ch1.xhtml", ch1)
        z.writestr("OEBPS/ad.xhtml", "<html><body><p>Buy more books</p></body></html>")


class Parsing(unittest.TestCase):
    def test_book_chunks_have_refs_pages_and_skip_ads(self):
        with tempfile.TemporaryDirectory() as d:
            epub = Path(d) / "b.epub"
            make_epub(epub)
            chunks = sources.book_chunks(epub)
        self.assertTrue(chunks)
        self.assertTrue(all(c["chapter"] == "1" for c in chunks))
        self.assertFalse(any("Buy more" in c["text"] for c in chunks))
        self.assertTrue(any("Matrix" in c["ref"] and "p. 11" in c["ref"] for c in chunks))
        self.assertTrue(all(len(c["text"]) <= sources.MAX + 200 for c in chunks))

    def test_doctype_in_package_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            epub = Path(d) / "b.epub"
            make_epub(epub, doctype=True)
            with self.assertRaises(ValueError):
                sources.book_chunks(epub)


class Grounding(unittest.TestCase):
    def test_evidence_must_be_a_real_quote(self):
        self.assertTrue(grounding.evidence_ok(
            "equal power and autonomy over the project team", PASSAGE))
        self.assertFalse(grounding.evidence_ok("the moon is made of cheese cheese", PASSAGE))
        self.assertFalse(grounding.evidence_ok("equal power", PASSAGE))  # too short to prove

    def test_curly_quotes_match(self):
        self.assertTrue(grounding.evidence_ok(
            "management’s job is to support the vision", "Management's job is to support the vision."))

    def test_invalid_citations_are_dropped(self):
        text, used = grounding.split_citations("A [1]. B [2, 9]. C [7].", 3)
        self.assertEqual(used, [1, 2])
        self.assertNotIn("9", text)
        self.assertNotIn("[7]", text)


class Search(unittest.TestCase):
    def test_hybrid_search_finds_acronym_and_respects_filter(self):
        chunks = [
            {"id": "a", "source": "book", "chapter": "1", "ref": "r", "heading": "WBS", "text": "The WBS decomposes deliverables."},
            {"id": "b", "source": "guide", "chapter": "01", "ref": "r", "heading": "Risk", "text": "Risk register tracks threats."},
        ]
        vecs = [[1.0, 0.0], [0.0, 1.0]]
        index = idx.Index(chunks, vecs, {})
        cfg = config.load({})
        with mock.patch("study.llm.embed", return_value=[[0.0, 1.0]]):
            top = index.search(cfg, "what is a WBS", k=2)
            self.assertEqual(top[0][1]["id"], "a")  # keywords beat a misleading vector
            only_guide = index.search(cfg, "what is a WBS", k=2, allow=modes.allow_for("guide", None))
        self.assertEqual([c["id"] for _, c in only_guide], ["b"])


class Questions(unittest.TestCase):
    CHUNK: ClassVar[dict] = {"id": "book-1", "source": "book", "ref": "Ch 1", "chapter": "1",
             "heading": "h", "text": PASSAGE}
    GOOD: ClassVar[dict] = {"question": "Who has equal power in a balanced matrix?",
            "correct": "Project manager and functional manager",
            "distractors": ["Only the sponsor", "Only the team", "The customer"],
            "evidence": "the project manager and the functional manager have equal power and autonomy",
            "explanation": "Stated in the passage."}

    def _run(self, gen, solver):
        calls = iter([json.dumps(gen), json.dumps({"answer": solver})] * 3)
        with mock.patch("study.llm.chat", side_effect=lambda *a, **k: next(calls)):
            return modes.make_question(config.load({}), self.CHUNK, tries=1,
                                       rng=mock.Mock(shuffle=lambda x: None))

    def test_accepts_when_solver_agrees(self):
        item = self._run(self.GOOD, 0)
        self.assertEqual(item["choices"][item["answer"]], self.GOOD["correct"])

    def test_rejects_when_solver_disagrees(self):
        self.assertIsNone(self._run(self.GOOD, 2))

    def test_rejects_fabricated_evidence_and_duplicate_choices(self):
        self.assertIsNone(self._run({**self.GOOD, "evidence": "made up sentence that is not there"}, 0))
        self.assertIsNone(self._run({**self.GOOD, "distractors": ["Only the sponsor"] * 3}, 0))

    def test_cards_drop_ungrounded_and_write_anki_csv(self):
        reply = json.dumps({"cards": [
            {"front": "Q1?", "back": "A1", "evidence": "equal power and autonomy over the project team"},
            {"front": "Q2?", "back": "A2", "evidence": "nothing like this in the passage at all"},
        ]})
        with mock.patch("study.llm.chat", return_value=reply), tempfile.TemporaryDirectory() as d:
            index = idx.Index([self.CHUNK], [[1.0]], {})
            out = Path(d) / "c.csv"
            n = modes.cards(config.load({}), index, "book", "1", None, None, 1, out, out=lambda *_: None)
            rows = [r for r in csv.reader(io.StringIO(out.read_text())) if r and not r[0].startswith("#")]
        self.assertEqual(n, 1)
        self.assertEqual(rows[0][0], "Q1?")
        self.assertIn("[Ch 1]", rows[0][1])


class Config(unittest.TestCase):
    def test_defaults_name_no_host_and_use_prefix_for_qwen3(self):
        cfg = config.load({})
        self.assertEqual(cfg.embed_url, "http://localhost:11434")
        self.assertTrue(cfg.embed_query_prefix.startswith("Instruct:"))
        self.assertIsNone(cfg.gen_num_ctx)
        self.assertEqual(config.load({"STUDY_EMBED_MODEL": "bge-m3"}).embed_query_prefix, "")


if __name__ == "__main__":
    unittest.main()
