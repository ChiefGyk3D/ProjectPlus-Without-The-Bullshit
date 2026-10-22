"""Settings for the study tool, from the environment or study/.env.local.

Nothing here names a host. Defaults assume one local Ollama on its default
port. Put real addresses in study/.env.local (gitignored), one KEY=value per
line, or export them.
"""
import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / "study" / ".env.local"  # or the file STUDY_ENV_FILE names


def _read_env_file(path: Path) -> dict:
    out = {}
    if not path.is_file():
        return out
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        out[key.strip()] = value.strip().strip("'\"")
    return out


@dataclass(frozen=True)
class Config:
    embed_url: str
    embed_model: str
    embed_num_ctx: int
    embed_query_prefix: str
    gen_url: str
    gen_model: str
    gen_num_ctx: int | None
    gen_timeout: int
    book: Path | None
    data_dir: Path
    guide_dir: Path


QWEN3_PREFIX = (
    "Instruct: Given a study question about CompTIA Project+, retrieve the "
    "passages that answer it\nQuery: "
)


def load(env: dict | None = None) -> Config:
    environ = os.environ if env is None else env
    env_file = Path(environ["STUDY_ENV_FILE"]).expanduser() if environ.get("STUDY_ENV_FILE") else ENV_FILE
    merged = {**_read_env_file(env_file), **environ}

    def get(key: str, default: str = "") -> str:
        return merged.get(key, default)

    embed_model = get("STUDY_EMBED_MODEL", "qwen3-embedding:0.6b")
    prefix = get("STUDY_EMBED_QUERY_PREFIX", None)
    if prefix is None:
        prefix = QWEN3_PREFIX if embed_model.startswith("qwen3-embedding") else ""
    default_url = get("STUDY_OLLAMA_URL", "http://localhost:11434")
    gen_ctx = get("STUDY_GEN_NUM_CTX")
    book = get("STUDY_BOOK")
    return Config(
        embed_url=get("STUDY_EMBED_URL", default_url).rstrip("/"),
        embed_model=embed_model,
        embed_num_ctx=int(get("STUDY_EMBED_NUM_CTX", "2048")),
        embed_query_prefix=prefix,
        gen_url=get("STUDY_GEN_URL", default_url).rstrip("/"),
        gen_model=get("STUDY_GEN_MODEL", "gemma4:12b"),
        gen_num_ctx=int(gen_ctx) if gen_ctx else None,
        gen_timeout=int(get("STUDY_GEN_TIMEOUT", "300")),
        book=Path(book).expanduser() if book else None,
        data_dir=Path(get("STUDY_DATA_DIR", str(ROOT / "study" / "data"))).expanduser(),
        guide_dir=Path(get("STUDY_GUIDE_DIR", str(ROOT / "docs"))).expanduser(),
    )
