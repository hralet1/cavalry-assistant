"""
Batch export all remaining Discord channels with checkpoints and progress bar.

Usage:
    python export_batch.py --server 538287787649007618
    python export_batch.py --server 538287787649007618 --ingest
"""

import json
import os
import sys
import time
from pathlib import Path

import click
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from export_discord import get_server_text_channels, export_channel

SOURCES_DIR = Path(__file__).resolve().parent / "sources" / "discord"
CHECKPOINT_FILE = SOURCES_DIR / "_checkpoint.json"


def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8"))
    return {"exported": [], "failed": [], "skipped": []}


def save_checkpoint(state: dict):
    CHECKPOINT_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def already_exported(channel_name: str) -> bool:
    for f in SOURCES_DIR.glob("*.json"):
        if f.stem == channel_name and f.name != "_checkpoint.json":
            return True
    return False


def progress_bar(current, total, ok, fail, skip, channel, width=40):
    """Render a visual progress bar for Claude Code terminal."""
    pct = current / total if total else 0
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return (
        f"\r  [{bar}] {current}/{total} ({pct:.0%})"
        f"  ✓{ok} ✗{fail} ⊘{skip}"
        f"  → #{channel}"
    )


@click.command()
@click.option("--server", "server_id", required=True, help="Server (guild) ID")
@click.option("--ingest", is_flag=True, help="Run ETL ingest after all exports")
@click.option("--skip-private/--include-private", default=True, help="Skip private channels (default: true)")
@click.option("--force", is_flag=True, help="Re-export already exported channels")
def main(server_id: str, ingest: bool, skip_private: bool, force: bool):
    """Batch export Discord channels with checkpoint recovery."""

    click.echo(f"\n  Discovering channels in server {server_id}...")
    channels = get_server_text_channels(server_id)

    if not channels:
        click.echo("  No text channels found.", err=True)
        sys.exit(1)

    # Filter private channels
    if skip_private:
        before = len(channels)
        channels = [
            ch for ch in channels
            if "private" not in ch["name"].lower()
            and "moderator" not in ch["name"].lower()
        ]
        priv_count = before - len(channels)
        if priv_count:
            click.echo(f"  Filtered out {priv_count} private/mod channels.")

    total = len(channels)
    click.echo(f"  {total} public channels found.\n")

    # Show channel list
    click.echo("  ┌─ Channel List ─────────────────────────────────")
    for ch in channels:
        status = "✓" if already_exported(ch["name"]) else "○"
        click.echo(f"  │ {status} #{ch['name']}")
    click.echo("  └────────────────────────────────────────────────\n")

    state = load_checkpoint()
    exported_ids = set(state["exported"])
    ok = 0
    fail = 0
    skip = 0
    total_msgs = 0
    start_time = time.time()

    for i, ch in enumerate(channels, 1):
        cid = ch["id"]
        name = ch["name"]

        # Print progress bar
        sys.stderr.write(progress_bar(i, total, ok, fail, skip, name) + "  \n")
        sys.stderr.flush()

        # Skip already done (unless --force)
        if not force and (cid in exported_ids or already_exported(name)):
            skip += 1
            continue

        try:
            path = export_channel(cid, SOURCES_DIR)
            if path:
                state["exported"].append(cid)
                ok += 1
                # Count messages in exported file
                data = json.loads(path.read_text(encoding="utf-8"))
                msg_count = len(data.get("messages", []))
                total_msgs += msg_count
                click.echo(f"  ✓ #{name}: {msg_count} messages")
            else:
                state["skipped"].append(cid)
                skip += 1
                click.echo(f"  ⊘ #{name}: no messages or no access")
        except Exception as e:
            state["failed"].append({"id": cid, "name": name, "error": str(e)})
            fail += 1
            click.echo(f"  ✗ #{name}: {e}")

        # Checkpoint after each channel
        save_checkpoint(state)

    elapsed = time.time() - start_time
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)

    # Final summary
    click.echo(f"\n  ┌─ BATCH COMPLETE ─────────────────────────────────")
    click.echo(f"  │  Time:     {mins}m {secs}s")
    click.echo(f"  │  Exported: {ok} channels ({total_msgs} messages)")
    click.echo(f"  │  Skipped:  {skip} (already done)")
    click.echo(f"  │  Failed:   {fail}")
    click.echo(f"  └────────────────────────────────────────────────────")

    if state["failed"]:
        click.echo("\n  Failed channels:")
        for f in state["failed"]:
            click.echo(f"    ✗ #{f['name']}: {f['error']}")

    if ingest:
        click.echo("\n  Starting full ingest (--source all)...\n")
        from ingest import ingest as run_ingest
        run_ingest.main(["--reset", "--source", "all"], standalone_mode=False)


if __name__ == "__main__":
    main()
