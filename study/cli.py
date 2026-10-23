"""python3 -m study {index,ask,quiz,cards,stats,web}"""
import argparse
import sys

from . import config, llm, modes
from . import index as idx


def _sources(cfg, which: str) -> list[str]:
    names = ["book", "guide"] if which == "both" else [which]
    if "book" in names and not (cfg.data_dir / "book" / "meta.json").is_file():
        if which == "book":
            sys.exit("No book index yet. Set STUDY_BOOK to the epub, then: python3 -m study index")
        names.remove("book")
        print("note: no book index, using the guide only", file=sys.stderr)
    return names


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="study", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--source", choices=["book", "guide", "both"], default="both")
        sp.add_argument("--chapter", help="chapter number (book) or page prefix like 03 (guide)")

    sub.add_parser("index", help="(re)build the indexes")
    sub.add_parser("stats", help="show what is indexed and which models are configured")
    w = sub.add_parser("web", help="local web page: ask, quiz, practice test, flashcards")
    w.add_argument("--port", type=int, default=8765)
    a = sub.add_parser("ask", help="ask a question, get a cited answer")
    a.add_argument("question", nargs="+")
    a.add_argument("-k", type=int, default=6, help="passages to retrieve")
    common(a)
    q = sub.add_parser("quiz", help="multiple-choice questions from the material")
    q.add_argument("-n", type=int, default=5)
    q.add_argument("--topic")
    q.add_argument("--seed", type=int)
    q.add_argument("--print", dest="show", action="store_true",
                   help="print questions with answers instead of asking you")
    common(q)
    c = sub.add_parser("cards", help="write an Anki CSV of flashcards")
    c.add_argument("--topic")
    c.add_argument("--limit", type=int, help="max passages to turn into cards")
    c.add_argument("--seed", type=int)
    c.add_argument("--out")
    common(c)

    args = p.parse_args(argv)
    cfg = config.load()
    cfg.data_dir.mkdir(parents=True, exist_ok=True)
    try:
        if args.cmd == "index":
            idx.build_all(cfg)
            return 0
        names = _sources(cfg, getattr(args, "source", "both"))
        index = idx.load(cfg, names)
        if args.cmd == "web":
            from . import web
            web.serve(cfg, index, args.port)
            return 0
        if args.cmd == "stats":
            print(f"embed: {cfg.embed_model}   generate: {cfg.gen_model}")
            for n, m in index.meta.items():
                print(f"{n}: {m['count']} chunks, {m['dims']} dims ({m['model']})")
            return 0
        source = args.source if args.source != "both" or len(names) == 2 else names[0]
        if args.cmd == "ask":
            answer, cites = modes.ask(cfg, index, " ".join(args.question), source,
                                      args.chapter, args.k)
            print(answer)
            if cites:
                print("\nSources:")
                for n, ref, src in cites:
                    print(f"  [{n}] {ref}  ({src})")
        elif args.cmd == "quiz":
            modes.quiz(cfg, index, args.n, source, args.chapter, args.topic,
                       not args.show and sys.stdin.isatty(), args.seed, cfg.data_dir)
        elif args.cmd == "cards":
            label = args.topic or args.chapter or "all"
            safe = "".join(ch if ch.isalnum() else "_" for ch in str(label))
            out = cfg.data_dir / "cards" / f"{source}-{safe}.csv"
            from pathlib import Path
            modes.cards(cfg, index, source, args.chapter, args.topic, args.limit,
                        args.seed, Path(args.out) if args.out else out)
        return 0
    except (llm.OllamaError, FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
