"""Thin Ollama client: embeddings and one-shot chat. Standard library only."""
import json
import urllib.error
import urllib.request


class OllamaError(RuntimeError):
    pass


def _post(url: str, body: dict, timeout: int) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        raise OllamaError(f"{url} -> HTTP {e.code}: {detail}") from e
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise OllamaError(f"cannot reach {url}: {e}") from e


def embed(cfg, texts: list[str], batch: int = 16) -> list[list[float]]:
    out: list[list[float]] = []
    for i in range(0, len(texts), batch):
        reply = _post(
            f"{cfg.embed_url}/api/embed",
            {
                "model": cfg.embed_model,
                "input": texts[i:i + batch],
                "truncate": False,
                "options": {"num_ctx": cfg.embed_num_ctx},
            },
            timeout=120,
        )
        vectors = reply.get("embeddings") or []
        if len(vectors) != len(texts[i:i + batch]):
            raise OllamaError("embedding count does not match input count")
        out.extend(vectors)
    return out


def chat(cfg, system: str, user: str, schema: dict | None = None) -> str:
    body = {
        "model": cfg.gen_model,
        "stream": False,
        "think": False,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "options": {"temperature": 0.2},
    }
    if cfg.gen_num_ctx:  # send exactly the loaded context, or omit it
        body["options"]["num_ctx"] = cfg.gen_num_ctx
    if schema:
        body["format"] = schema
    reply = _post(f"{cfg.gen_url}/api/chat", body, timeout=cfg.gen_timeout)
    return (reply.get("message") or {}).get("content", "").strip()
