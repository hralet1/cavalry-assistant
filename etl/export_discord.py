"""
Export Discord channel messages to JSON for ETL ingestion.

Usage:
    python export_discord.py                          # export channels from DISCORD_CHANNEL_IDS
    python export_discord.py --channel 1458753656022241292
    python export_discord.py --channel 1458753656022241292 --ingest   # export + ingest in one step
"""

import json
import os
import sys
import time
from pathlib import Path

import click
import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Fix Windows console encoding for emoji in channel names
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

API_BASE = "https://discord.com/api/v10"
RATE_LIMIT_BUFFER = 0.5  # seconds between requests


def _headers():
    token = os.environ.get("DISCORD_TOKEN", "")
    if not token:
        click.echo("Error: DISCORD_TOKEN not set in .env", err=True)
        sys.exit(1)
    return {"Authorization": token, "Content-Type": "application/json"}


def _get(endpoint: str) -> dict | list | None:
    """Make a GET request to Discord API with rate-limit handling."""
    url = f"{API_BASE}{endpoint}"
    while True:
        resp = requests.get(url, headers=_headers(), timeout=30)
        if resp.status_code == 429:
            retry_after = resp.json().get("retry_after", 5)
            click.echo(f"  Rate limited, waiting {retry_after:.1f}s...")
            time.sleep(retry_after)
            continue
        if resp.status_code == 401:
            click.echo("Error: Invalid or expired DISCORD_TOKEN.", err=True)
            sys.exit(1)
        if resp.status_code == 403:
            click.echo(f"Error: No access to {endpoint}. Check permissions.", err=True)
            return None
        resp.raise_for_status()
        time.sleep(RATE_LIMIT_BUFFER)
        return resp.json()


def get_channel_info(channel_id: str) -> dict | None:
    return _get(f"/channels/{channel_id}")


def get_server_text_channels(guild_id: str) -> list[dict]:
    """Fetch all text channels from a server (guild)."""
    channels = _get(f"/guilds/{guild_id}/channels")
    if not channels:
        return []
    # type 0 = text channel, 5 = announcement channel — both have messages
    return [ch for ch in channels if ch.get("type") in (0, 5)]


def fetch_all_messages(channel_id: str) -> list[dict]:
    """Fetch all messages from a channel using backward pagination."""
    all_messages = []
    before = None
    batch = 0

    with tqdm(desc="Fetching messages", unit=" msgs") as pbar:
        while True:
            endpoint = f"/channels/{channel_id}/messages?limit=100"
            if before:
                endpoint += f"&before={before}"

            messages = _get(endpoint)
            if messages is None or len(messages) == 0:
                break

            all_messages.extend(messages)
            pbar.update(len(messages))
            before = messages[-1]["id"]
            batch += 1

            if len(messages) < 100:
                break

    # Discord returns newest-first; reverse to chronological order
    all_messages.reverse()
    return all_messages


def format_for_chunker(channel_name: str, raw_messages: list[dict]) -> dict:
    """Convert Discord API messages to the format our chunker expects."""
    messages = []
    for msg in raw_messages:
        content = msg.get("content", "").strip()
        if not content:
            continue

        entry = {
            "id": msg["id"],
            "author": {"name": msg["author"].get("username", "unknown")},
            "timestamp": msg["timestamp"],
            "content": content,
        }

        # Preserve embeds (YouTube, links, etc.) for metadata extraction
        if msg.get("embeds"):
            entry["embeds"] = [
                {k: v for k, v in e.items() if k in ("url", "title", "description", "video", "type")}
                for e in msg["embeds"]
            ]

        messages.append(entry)

    return {
        "channel": {"name": channel_name},
        "messages": messages,
    }


def export_channel(channel_id: str, output_dir: Path) -> Path | None:
    """Export a single channel to JSON. Returns output path or None on failure."""
    click.echo(f"\nChannel: {channel_id}")

    info = get_channel_info(channel_id)
    if not info:
        return None

    channel_name = info.get("name", channel_id)
    click.echo(f"  Name: #{channel_name}")

    raw = fetch_all_messages(channel_id)
    click.echo(f"  Total messages fetched: {len(raw)}")

    if not raw:
        click.echo("  Skipped (no messages)")
        return None

    data = format_for_chunker(channel_name, raw)
    click.echo(f"  Non-empty messages: {len(data['messages'])}")

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{channel_name}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    click.echo(f"  Saved: {out_path}")
    return out_path


@click.command()
@click.option("--channel", "channel_ids", multiple=True, help="Channel ID(s) to export")
@click.option("--server", "server_id", default=None, help="Server (guild) ID — exports all text channels")
@click.option("--ingest", is_flag=True, help="Run ETL ingest after export")
def main(channel_ids: tuple[str], server_id: str | None, ingest: bool):
    """Export Discord channels to JSON for cavalry-assistant knowledge base."""

    # --server: discover all text channels in the guild
    if server_id:
        click.echo(f"Discovering channels in server {server_id}...")
        text_channels = get_server_text_channels(server_id)
        if not text_channels:
            click.echo("Error: No text channels found (check token permissions).", err=True)
            sys.exit(1)
        click.echo(f"Found {len(text_channels)} text channels:")
        for ch in text_channels:
            click.echo(f"  #{ch['name']} ({ch['id']})")
        channel_ids = [ch["id"] for ch in text_channels]

    # Fall back to CLI args or env var
    if not channel_ids:
        env_ids = os.environ.get("DISCORD_CHANNEL_IDS", "")
        channel_ids = [cid.strip() for cid in env_ids.split(",") if cid.strip()]

    if not channel_ids:
        click.echo("Error: No channel IDs. Use --channel, --server, or set DISCORD_CHANNEL_IDS in .env", err=True)
        sys.exit(1)

    output_dir = Path(__file__).resolve().parent / "sources" / "discord"
    exported = []

    click.echo(f"Exporting {len(channel_ids)} channel(s)...")
    for cid in channel_ids:
        path = export_channel(cid, output_dir)
        if path:
            exported.append(path)

    click.echo(f"\nDone. {len(exported)}/{len(channel_ids)} channels exported.")

    if ingest and exported:
        click.echo("\nRunning ETL ingest...")
        from ingest import ingest as run_ingest
        run_ingest.main(["--source", "discord"], standalone_mode=False)


if __name__ == "__main__":
    main()
