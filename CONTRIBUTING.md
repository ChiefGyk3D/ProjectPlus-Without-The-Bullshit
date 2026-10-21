# Contributing

The guide is Markdown in `docs/`. Everything else is generated from it: the
mind map, the flashcards, the wiki and the PDF. Edit a page, never a
generated file.

## Fixing a mistake in the material

A factual error is the most useful thing you can report. Open an issue with
the section, what the guide says, what is right, and where you checked it.
The exam objectives and CompTIA's exam page are the authority; the book the
guide was cross-checked against is *CompTIA Project+ Certification
All-in-One Exam Guide (Exam PK0-005)*. Do not paste text from the book or
from exam dumps, and do not send real exam questions.

## Changing a page

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt ruff
python3 scripts/build_mindmap.py
python3 scripts/build_anki.py
python3 scripts/gen_wiki.py --out wiki-out
python3 scripts/build_pdf.py --out guide.pdf
mkdocs build --strict
```

Commit the regenerated `docs/mindmap-full.html`, `docs/mindmap.md` and
`anki/projectplus.csv` with your change; CI fails if they are stale. The wiki
and the PDF are built by CI and are not committed.

Keep the existing shape: a table row is `term | definition`, an exam tip is a
`!!! tip "Exam tip"` block that starts with a capital letter, and new
objectives keep the N.N numbering.

## Practice questions

`docs/07-practice.md` is written for this guide. A new question needs one
correct answer, distractors from the same group the correct answer belongs to,
and an answer that names the section it comes from.
