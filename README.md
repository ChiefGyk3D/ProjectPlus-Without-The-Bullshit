# Project+ Without The Bullshit

A CompTIA Project+ PK0-005 study guide for people who already know how to run
projects and just need the cert. Every objective, the terms, the traps,
nothing else.

**Read it as a site:** https://chiefgyk3d.github.io/ProjectPlus-Without-The-Bullshit/

| Want to | Go to |
| --- | --- |
| Read the guide with a sidebar and search | the site above, or [`docs/`](docs/) on GitHub |
| See the whole exam on one screen | [mind map](https://chiefgyk3d.github.io/ProjectPlus-Without-The-Bullshit/mindmap-full.html) |
| Drill terms with spaced repetition | [`anki/projectplus.csv`](anki/projectplus.csv), import into Anki (File → Import, comma separated, tags in field 3) |
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
  mindmap.md            embeds mindmap-full.html (generated)
anki/projectplus.csv    flashcards (generated)
scripts/                build_mindmap.py, build_anki.py
```

The domain pages are the source. The mind map and the flashcards are
generated from them, so edit a page and re-run the scripts:

```sh
python3 scripts/build_mindmap.py
python3 scripts/build_anki.py
pip install -r requirements.txt && mkdocs serve   # preview at http://127.0.0.1:8000
```

## CI

All of it comes from [git-your-ship-together](https://github.com/ChiefGyk3D/git-your-ship-together),
pinned to a release SHA and bumped by Dependabot:

| Workflow | Shared workflow | What it does here |
| --- | --- | --- |
| `ci.yml` | `python-ci.yml` | `ruff` on the scripts, regenerates the mind map and flashcards and fails if they were stale, `mkdocs build --strict`. `ci / CI green` is the branch-protection gate. |
| `docs.yml` | `docs-pages.yml` | Builds the site on every push and PR, deploys to GitHub Pages from `main` |
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
