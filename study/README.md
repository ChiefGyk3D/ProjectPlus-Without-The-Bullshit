# Study tool

Ask questions, take quizzes and make flashcards from your own copy of the
*CompTIA Project+ All-in-One Exam Guide (PK0-005)* and from this guide, using
a local Ollama. Every answer, question and card carries a chapter and page
reference, and everything the model writes is checked in code.

**The book is copyrighted. Nothing derived from it is committed.** The index,
quizzes and cards live in a data directory outside the repository (or in the
gitignored `study/data/`). The guide's own pages are indexed too and labeled
as a separate source, so you can see where each answer came from.

## Setup

Standard library only, Python 3.12 or newer. You need an Ollama with an
embedding model (for example `ollama pull qwen3-embedding:0.6b`) and a chat
model.

Settings come from the environment or a file of `KEY=value` lines
(`study/.env.local`, gitignored, or the file named by `STUDY_ENV_FILE`):

| Setting | Default | Meaning |
|---|---|---|
| `STUDY_BOOK` | unset | path to your epub; unset means guide only |
| `STUDY_OLLAMA_URL` | `http://localhost:11434` | one server for both jobs |
| `STUDY_EMBED_URL` / `STUDY_GEN_URL` | `STUDY_OLLAMA_URL` | split embedding and chat across servers |
| `STUDY_EMBED_MODEL` | `qwen3-embedding:0.6b` | any Ollama embedding model |
| `STUDY_EMBED_NUM_CTX` | `2048` | context sent for embeddings |
| `STUDY_GEN_MODEL` | `gemma4:12b` | chat model for answers, questions, cards |
| `STUDY_GEN_NUM_CTX` | unset | send exactly the context the model is loaded with, or leave unset |
| `STUDY_DATA_DIR` | `study/data` | where indexes, quiz log and cards go |

Qwen3 embedding models get their recommended query instruction
automatically; set `STUDY_EMBED_QUERY_PREFIX` to change it.

## Use

Run from the repository root.

```sh
python3 -m study index                          # build or refresh (skips if current)
python3 -m study ask what is a matrix organization
python3 -m study ask --source guide --chapter 03 "RACI vs RASCI"
python3 -m study quiz -n 5 --chapter 3          # interactive
python3 -m study quiz --topic "risk response" --print   # show answers
python3 -m study cards --chapter 3 --limit 20   # Anki CSV in the data dir
python3 -m study build-bank -n 300 --source book   # more fixed questions, see below
python3 -m study stats
```

`--source book|guide|both` picks the material. `--chapter` is the book
chapter number (or `intro`, `glossary`, `appb`) and, for the guide, the page
prefix such as `03`.

## More questions

`build-bank` writes verified questions to `generated-bank.jsonl` in the data
directory (never the repository), spread evenly across the chapters. It uses the
same checks as live quizzes: four distinct choices, evidence quoted from the
passage, and an independent solver call that must agree with the key. It is
resumable (a passage is used once, a repeated question is skipped), so run it as
often as you like. About 5 seconds per question. The web page loads the file, so
those questions are instant and count toward Progress like the rest.

## Web page

```sh
STUDY_ENV_FILE=~/.config/projectplus-study/env python3 -m study web   # http://127.0.0.1:8765/
```

One page, five tabs, localhost only (`--port` changes the port):

- **Ask:** a cited answer with the chapter and page of each source.
- **Drill:** one question at a time with instant feedback. *Fixed* questions are the
  book's own chapter-review questions (180, with the book's answer keys), the
  guide's practice file and anything `build-bank` wrote, so they are instant. *Generated* questions are
  new ones written from a random passage; the next one is prepared while you answer
  the current one. Order can be random, not seen yet, or the ones you missed.
- **Practice test:** pick a size, a chapter and an optional timer. Answers are held
  until you finish, then you get a score, a per-chapter breakdown and a review.
- **Flashcards:** pick a chapter and a size, download the Anki CSV.
- **Progress:** accuracy by chapter from `quiz-log.jsonl`, and a one-click drill of the
  questions you missed last time.

The server binds to 127.0.0.1, rejects other Host and Origin headers, accepts only
JSON POSTs, and sends a strict Content-Security-Policy. An answer key is not sent to
the page until you have answered. The book's questions come from your own epub and
are never written into the repo.

## What is checked in code

- **Ask:** the model may only cite the passages it was given; citation
  markers pointing at nothing are removed, the source list is built from the
  markers that remain, and an answer that cites nothing is flagged. Out-of-book
  questions return "Not covered in the provided passages."
- **Quiz and cards:** each item must quote its evidence word for word from the
  passage. Questions also need four distinct choices, code shuffles them, and a
  second independent model call must pick the same answer before you see it.
  Items that fail are dropped.
- Local models still make mistakes. Treat the book as the authority and use the
  reference to check.

## Tests

```sh
python3 -m unittest discover -s study/tests -t .
```
