# chunkers/discord.py
import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from typing import Any

URL_RE = re.compile(r'https?://[^\s<>\])"]+')
YOUTUBE_RE = re.compile(r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)')
VIDEO_DOMAINS = {"youtube.com", "youtu.be", "vimeo.com", "twitch.tv"}

# Code block signals — people share fixes as code, not prose
CODE_BLOCK_RE = re.compile(r'```[\s\S]+?```')
INLINE_CODE_RE = re.compile(r'`[^`]+`')
# Gratitude signals — when someone says thanks, the prior messages likely contain the fix
GRATITUDE_RE = re.compile(r'(?i)(?:thanks|thank you|that worked|perfect|awesome|solved|got it|cheers)')
BUG_CHANNELS = {"bugs", "🐛-bugs", "bug-reports"}

SCHEMA_VERSION = 1
WINDOW_MINUTES = 5


def _make_id(source: str, content: str) -> str:
    return hashlib.sha256(f"{source}:{content}".encode()).hexdigest()[:32]


def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def chunk_discord_export(
    export: dict,
    tags: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Group Discord messages by 5-minute proximity windows."""
    channel_name = export.get("channel", {}).get("name", "unknown")
    messages = [m for m in export.get("messages", []) if m.get("content", "").strip()]

    if not messages:
        return []

    groups: list[list[dict]] = []
    current_group: list[dict] = []
    last_ts: datetime | None = None

    for msg in messages:
        ts = _parse_ts(msg["timestamp"])
        if last_ts is None or (ts - last_ts) <= timedelta(minutes=WINDOW_MINUTES):
            current_group.append(msg)
        else:
            if current_group:
                groups.append(current_group)
            current_group = [msg]
        last_ts = ts

    if current_group:
        groups.append(current_group)

    chunks = []
    for group in groups:
        lines = [f"{m['author']['name']}: {m['content']}" for m in group]
        content = "\n".join(lines)
        msg_ids = ":".join(m["id"] for m in group)

        # Extract URLs and classify them
        urls = []
        video_urls = []
        for m in group:
            for url in URL_RE.findall(m.get("content", "")):
                urls.append(url)
                if any(domain in url for domain in VIDEO_DOMAINS):
                    video_urls.append(url)
            # Also capture Discord embeds (from exporter)
            for embed in m.get("embeds", []):
                if embed.get("url"):
                    urls.append(embed["url"])
                if embed.get("video", {}).get("url"):
                    video_urls.append(embed["video"]["url"])

        # Collect all unique contributors in this chunk
        authors = list(dict.fromkeys(m["author"]["name"] for m in group))

        meta = {"authors": authors}
        if urls:
            meta["urls"] = list(dict.fromkeys(urls))  # dedupe, preserve order
        if video_urls:
            meta["videos"] = list(dict.fromkeys(video_urls))

        chunk_tags = list(tags or [])
        if video_urls:
            chunk_tags.append("video")
        # Tag chunks that contain code (high-value: someone sharing a snippet/fix)
        has_code = bool(CODE_BLOCK_RE.search(content) or INLINE_CODE_RE.search(content))
        if has_code:
            chunk_tags.append("has-code")
        # Tag conversations where someone expressed gratitude (likely contains a fix)
        has_thanks = bool(GRATITUDE_RE.search(content))
        if has_thanks:
            chunk_tags.append("resolved")
        # Bug channel tagging
        if channel_name in BUG_CHANNELS:
            chunk_tags.append("bug")
            if has_code and has_thanks:
                chunk_tags.append("fix")

        chunks.append({
            "id": _make_id(f"discord:{channel_name}", msg_ids),
            "schema_version": SCHEMA_VERSION,
            "content": content,
            "source": "discord",
            "channel": channel_name,
            "author": authors[0],
            "timestamp": group[0]["timestamp"],
            "tags": chunk_tags,
            "metadata": json.dumps(meta),
        })
    return chunks
