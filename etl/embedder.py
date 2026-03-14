# embedder.py
from dataclasses import dataclass
from typing import Literal
import ollama
import openai

OLLAMA_DIM = 768
OPENAI_DIM = 1536
OLLAMA_MODEL = "nomic-embed-text"
OPENAI_MODEL = "text-embedding-3-small"


@dataclass
class EmbedderConfig:
    backend: Literal["ollama", "openai"] = "ollama"
    ollama_host: str = "http://localhost:11434"
    openai_api_key: str = ""
    openai_model: str = OPENAI_MODEL
    ollama_model: str = OLLAMA_MODEL


def embed_texts(texts: list[str], cfg: EmbedderConfig) -> list[list[float]]:
    if cfg.backend == "ollama":
        return _embed_ollama(texts, cfg)
    elif cfg.backend == "openai":
        return _embed_openai(texts, cfg)
    else:
        raise ValueError(f"Unknown backend: {cfg.backend}")


def _embed_ollama(texts: list[str], cfg: EmbedderConfig) -> list[list[float]]:
    # nomic-embed-text has 8192 token context window.
    # Code-heavy text tokenizes at ~2 chars/token, so use conservative limit.
    MAX_CHARS = 4_000
    results = []
    for text in texts:
        t = text[:MAX_CHARS] if len(text) > MAX_CHARS else text
        try:
            response = ollama.embeddings(model=cfg.ollama_model, prompt=t)
        except Exception:
            # If still too long, halve it
            t = t[:len(t) // 2]
            response = ollama.embeddings(model=cfg.ollama_model, prompt=t)
        results.append(response["embedding"])
    return results


def _embed_openai(texts: list[str], cfg: EmbedderConfig) -> list[list[float]]:
    client = openai.OpenAI(api_key=cfg.openai_api_key)
    response = client.embeddings.create(model=cfg.openai_model, input=texts)
    return [item.embedding for item in response.data]
