# chunkers/markdown.py
import hashlib
import re
from datetime import datetime, timezone
from typing import Any


SCHEMA_VERSION = 1


def _make_id(source: str, content: str) -> str:
    return hashlib.sha256(f"{source}:{content}".encode()).hexdigest()[:32]


def chunk_markdown(
    text: str,
    source: str,
    channel: str,
    author: str = "system",
    tags: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Split markdown by ## headings. Returns list of chunk dicts."""
    parts = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    chunks = []
    for part in parts:
        content = part.strip()
        if not content:
            continue
        chunks.append({
            "id": _make_id(source, content),
            "schema_version": SCHEMA_VERSION,
            "content": content,
            "source": source,
            "channel": channel,
            "author": author,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tags": tags or [],
            "metadata": "{}",
        })
    return chunks
