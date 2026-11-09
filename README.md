# Project+ Without The Bullshit

A CompTIA Project+ PK0-005 study guide for people who already know how to run
projects and just need the cert. Every objective, the terms, the traps,
nothing else.

## Why this exists

I have worked in the field for years, and I think the Project+ cert is dumb: it takes things people do every day and overcomplicates the language to seem more difficult than it is. I still need the paper, though, and the paper is gated by that vocabulary, so this guide translates it back into what the work actually is and says plainly where the objectives skip something the exam asks anyway.

And yes, I see the irony. I built a study guide for an exam that tests Agile by running the repo like an Agile project, an issue for every change, small pull requests, a CI gate, and merge when green, so I practiced the thing the exam wants me to define while building the thing that helps me define it.

**Read it as a site:** https://chiefgyk3d.github.io/ProjectPlus-Without-The-Bullshit/

| Want to | Go to |
| --- | --- |
| Read the guide with a sidebar and search | the site above, or [`docs/`](docs/) on GitHub |
| See the whole exam on one screen | [mind map](https://chiefgyk3d.github.io/ProjectPlus-Without-The-Bullshit/mindmap-full.html) |
| Drill terms with spaced repetition | [`anki/projectplus.csv`](anki/projectplus.csv), import into Anki 2.1.54 or later with File → Import; the file carries its own settings, and importing a newer version updates your cards instead of duplicating them |
| Browse by objective | the [wiki](https://github.com/ChiefGyk3D/ProjectPlus-Without-The-Bullshit/wiki), one page per exam objective |
| Print it | the [PDF](https://chiefgyk3d.github.io/ProjectPlus-Without-The-Bullshit/ProjectPlus-PK0-005.pdf), the whole guide on US Letter, rebuilt on every push to `main` |
| Test yourself | [practice questions](docs/07-practice.md), forty-two scenarios with an answer key |
| Ask, drill and practice-test against your own copy of a book, locally | the [study tool](study/README.md): `python3 -m study web` opens a page on your own machine |
| Cram the night before | [cheat sheet](docs/06-cheatsheet.md) and [gaps from the book](docs/05-gaps.md) |

## Layout

```
docs/
  index.md              start here: exam format, weights, how to study
  01-concepts.md        1.0 Project Management Concepts (33%)
  02-lifecycle.md       2.0 Project Life Cycle Phases (30%)
  03-tools.md           3.0 Tools and Documentation (19%)
  04-it-governance.md   4.0 Basics of IT and Governance (18%)
  05-gaps.md            what the objectives don't say but the exam asks
  06-cheatsheet.md      formulas, acronyms, easily confused pairs
  07-practice.md        forty-two scenario questions with an answer key
  mindmap.md            embeds mindmap-full.html (generated)
anki/projectplus.csv    flashcards (generated)
scripts/                build_mindmap.py, build_anki.py, gen_wiki.py, build_pdf.py
study/                  local study tool: cited Q&A, quizzes, practice tests, flashcards (see below)
```

The domain pages are the source. The mind map, the flashcards and the wiki are
generated from them, so edit a page and re-run the scripts:

```sh
python3 scripts/build_mindmap.py
python3 scripts/build_anki.py
python3 scripts/gen_wiki.py --out wiki-out   # the wiki pages, for a look; CI publishes them
pip install -r requirements.txt && mkdocs serve   # preview at http://127.0.0.1:8000
```

## Local study tool

`study/` runs on your own machine against your own copy of a book (an epub you
own) plus this guide, using a local Ollama server. Nothing from the book is ever
committed: the index, quiz log and flashcards live in `~/.local/share/`, and the
settings in a private env file.

```sh
python3 -m study index          # once: build the search index
python3 -m study web            # http://127.0.0.1:8765/  (ask, drill, practice test, simulations, flashcards, progress)
python3 -m study ask "what is a RACI chart?"   # or use it from the terminal
```

Setup, every command, the settings and what is checked in code are in
[`study/README.md`](study/README.md). The published site and the PDF do not
include it.

## Preview the site locally

```sh
pip install -r requirements.txt && mkdocs serve   # http://127.0.0.1:8000
```

## CI

All of it comes from [git-your-ship-together](https://github.com/ChiefGyk3D/git-your-ship-together),
pinned to a release SHA and bumped by Dependabot:

| Workflow | Shared workflow | What it does here |
| --- | --- | --- |
| `ci.yml` | `python-ci.yml` | `ruff` on the scripts, regenerates the mind map and flashcards and fails if they were stale, `mkdocs build --strict`. `ci / CI green` is the branch-protection gate. |
| `docs.yml` | `docs-pages.yml` | Builds the site on every push and PR, deploys to GitHub Pages from `main` |
| `docs.yml` (PDF) | same | `scripts/build_pdf.py` renders the pages to `ProjectPlus-PK0-005.pdf` (WeasyPrint) and ships it beside the site |
| `wiki.yml` | `wiki-publish.yml` | Runs `gen_wiki.py` and replaces every page of the GitHub wiki from `main`. The wiki is a mirror: edit `docs/`, never the wiki. |
| `security.yml` | `security.yml` | CodeQL (python, actions), gitleaks, pip-audit, dependency review, Scorecard |
| `dependabot-auto-merge.yml` | `dependabot-auto-merge.yml` | Merges Dependabot bumps up to minor once CI is green |

The repository is in that project's `baseline/repos.txt`, so its settings are audited weekly against
[BASELINE.md](https://github.com/ChiefGyk3D/git-your-ship-together/blob/main/BASELINE.md).

## Sources

Written from the PK0-005 exam objectives and cross-checked against the
*CompTIA Project+ Certification All-in-One Exam Guide (Exam PK0-005)* by
Joseph Phillips (McGraw Hill, 2023), in particular its exam tips and
"Critical Exam Information" appendix. No text is copied from the book.
Not affiliated with CompTIA.

MIT licensed.
