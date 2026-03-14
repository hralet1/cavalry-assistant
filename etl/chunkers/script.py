# chunkers/script.py
import hashlib
import re
from datetime import datetime, timezone
from typing import Any

SCHEMA_VERSION = 1


def _make_id(source: str, content: str) -> str:
    return hashlib.sha256(f"{source}:{content}".encode()).hexdigest()[:32]


def chunk_script(
    code: str,
    filename: str,
    tags: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Treat each JS file as a single chunk. Description from // @description on line 1."""
    first_line = code.strip().splitlines()[0] if code.strip() else ""
    match = re.match(r"^//\s*@description\s+(.+)$", first_line)
    description = match.group(1).strip() if match else filename

    content = f"// Script: {description}\n{code.strip()}"

    return [{
        "id": _make_id("script", content),
        "schema_version": SCHEMA_VERSION,
        "content": content,
        "source": "script",
        "channel": filename,
        "author": "system",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tags": tags or ["script"],
        "metadata": "{}",
    }]
