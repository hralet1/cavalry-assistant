"""
Scrape Scenery.io scenes — download .cv files + metadata for knowledge base.

Usage:
    python scrape_scenery.py --limit 3          # test with 3 scenes
    python scrape_scenery.py                     # all scenes
    python scrape_scenery.py --ingest            # scrape + ingest metadata
    python scrape_scenery.py --update            # only scrape new scenes
"""

import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import click
import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_URL = "https://scenery.io"
SCENES_URL = f"{BASE_URL}/scenes"
METADATA_DIR = Path(__file__).resolve().parent / "sources" / "scenery"
CV_DIR = Path(__file__).resolve().parent.parent / "data" / "scenery_cv"
MANIFEST_PATH = METADATA_DIR / "_manifest.json"
RATE_LIMIT = 0.5


def load_manifest() -> dict:
    """Load scrape manifest — tracks scene_path → {hash, scraped_at} for incremental updates."""
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict):
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def get_cookie():
    cookie = os.environ.get("SCENERY_COOKIE", "")
    if not cookie:
        click.echo("Error: SCENERY_COOKIE not set in .env", err=True)
        click.echo("  Get it from Playwright: browser cookies after login", err=True)
        sys.exit(1)
    return cookie


def fetch_page(url: str, cookie: str) -> str | None:
    try:
        resp = requests.get(url, headers={"Cookie": cookie}, timeout=30)
        if resp.status_code != 200:
            return None
        return resp.text
    except Exception:
        return None


def extract_scene_metadata(html: str, url: str) -> dict | None:
    """Extract metadata from a scene page."""
    title_m = re.search(r'<h2[^>]*>(.*?)</h2>', html)
    title = title_m.group(1).strip() if title_m else "Unknown"

    author_m = re.search(r'<a[^>]*href="/@([^"]*)"[^>]*>', html)
    author = author_m.group(1).strip() if author_m else "unknown"

    license_m = re.search(r'Licensed\s*(CC[^<"]*)', html)
    license_type = license_m.group(1).strip() if license_m else "unknown"

    version_m = re.search(r'Made in Cavalry\s*([\d.]+)', html)
    version = version_m.group(1).strip() if version_m else "unknown"

    # Extract nodes used
    nodes_section = re.search(r'Made in Cavalry.*?</h3>\s*<div[^>]*>(.*?)</div>', html, re.DOTALL)
    nodes = []
    if nodes_section:
        nodes = re.findall(r'>([^<]+)</a>', nodes_section.group(1))
        nodes = [n.strip() for n in nodes if n.strip()]

    # Download URL
    dl_m = re.search(r'href="(/download/scenes/[^"]+)"', html)
    download_path = dl_m.group(1) if dl_m else None

    # Scene ID from URL
    scene_id = url.rstrip("/").split("-")[-1] if "-" in url else url.rstrip("/").split("/")[-1]

    return {
        "title": title,
        "author": author,
        "license": license_type,
        "cavalry_version": version,
        "nodes": nodes,
        "download_path": download_path,
        "scene_id": scene_id,
        "url": url,
    }


def save_metadata_md(meta: dict, output_dir: Path) -> Path:
    """Save scene metadata as markdown for RAG ingestion."""
    slug = meta["url"].rstrip("/").split("/")[-1]
    path = output_dir / f"{slug}.md"

    nodes_str = ", ".join(meta["nodes"]) if meta["nodes"] else "none listed"

    md = f"""# {meta['title']}

Source: {BASE_URL}{meta['url']}
Author: {meta['author']}
License: {meta['license']}
Cavalry Version: {meta['cavalry_version']}

## Nodes Used

{nodes_str}

## Description

Cavalry scene "{meta['title']}" by {meta['author']}. Made with Cavalry {meta['cavalry_version']}, using: {nodes_str}. This scene demonstrates how these nodes work together.
"""
    path.write_text(md.strip(), encoding="utf-8")
    return path


def download_cv(download_path: str, title: str, cookie: str, output_dir: Path) -> Path | None:
    """Download the .cv file."""
    try:
        url = f"{BASE_URL}{download_path}"
        resp = requests.get(url, headers={"Cookie": cookie}, timeout=60, allow_redirects=True)
        if resp.status_code != 200 or len(resp.content) < 100:
            return None

        # Clean filename
        safe_name = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-').lower()
        path = output_dir / f"{safe_name}.cv"
        path.write_bytes(resp.content)
        return path
    except Exception:
        return None


@click.command()
@click.option("--limit", default=0, help="Limit number of scenes (0 = all)")
@click.option("--ingest", is_flag=True, help="Run ETL ingest after scraping")
@click.option("--no-download", is_flag=True, help="Skip .cv file downloads, metadata only")
@click.option("--update", is_flag=True, help="Only scrape new scenes (skip already-scraped)")
@click.option("--refresh-urls", is_flag=True, help="Force re-fetch scene URLs from site")
def main(limit: int, ingest: bool, no_download: bool, update: bool, refresh_urls: bool):
    """Scrape Scenery.io scenes for knowledge base + .cv files."""

    cookie = get_cookie()

    # Load scene URLs from cached file or fetch from site
    urls_cache = METADATA_DIR / "_scene_urls.json"
    if urls_cache.exists() and not refresh_urls:
        scene_paths = json.loads(urls_cache.read_text(encoding="utf-8"))
        click.echo(f"  Loaded {len(scene_paths)} scene URLs from cache.")
    else:
        click.echo("  Fetching scene list from scenery.io...")
        html = fetch_page(SCENES_URL, cookie)
        if not html:
            click.echo("Error: Could not fetch scenes page.", err=True)
            sys.exit(1)
        scene_paths = list(set(re.findall(r'href="(/scenes/[^"]+)"', html)))
        scene_paths = [p for p in scene_paths if p != "/scenes"]
        METADATA_DIR.mkdir(parents=True, exist_ok=True)
        urls_cache.write_text(json.dumps(scene_paths), encoding="utf-8")
        click.echo(f"  Found {len(scene_paths)} scenes.")

    manifest = load_manifest() if update else {}

    if update:
        new_paths = [p for p in scene_paths if p not in manifest]
        if new_paths:
            click.echo(f"  Update mode: {len(new_paths)} new scenes to scrape (skipping {len(scene_paths) - len(new_paths)} already scraped).")
            scene_paths = new_paths
        else:
            click.echo(f"  Update mode: all {len(scene_paths)} scenes already scraped. Nothing to do.")
            return

    if limit:
        scene_paths = scene_paths[:limit]
        click.echo(f"  Limited to {limit} scenes (test mode).")

    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    if not no_download:
        CV_DIR.mkdir(parents=True, exist_ok=True)

    ok = 0
    dl_ok = 0
    fail = 0
    now = datetime.now(timezone.utc).isoformat()

    for scene_path in tqdm(scene_paths, desc="Scraping", unit=" scenes"):
        url = f"{BASE_URL}{scene_path}"
        html = fetch_page(url, cookie)
        if not html:
            fail += 1
            time.sleep(RATE_LIMIT)
            continue

        meta = extract_scene_metadata(html, scene_path)
        if not meta:
            fail += 1
            time.sleep(RATE_LIMIT)
            continue

        save_metadata_md(meta, METADATA_DIR)
        manifest[scene_path] = {"scraped_at": now, "title": meta["title"]}
        ok += 1

        if not no_download and meta["download_path"]:
            cv_path = download_cv(meta["download_path"], meta["title"], cookie, CV_DIR)
            if cv_path:
                dl_ok += 1

        time.sleep(RATE_LIMIT)

    # Always save manifest for future --update runs
    save_manifest(manifest)

    click.echo(f"\n  ┌─ SCENERY SCRAPE COMPLETE ────────────────────")
    click.echo(f"  │  Metadata:  {ok} scenes")
    click.echo(f"  │  Downloads: {dl_ok} .cv files")
    click.echo(f"  │  Failed:    {fail}")
    click.echo(f"  │  Metadata:  {METADATA_DIR}")
    if not no_download:
        click.echo(f"  │  CV files:  {CV_DIR}")
    click.echo(f"  └───────────────────────────────────────────────")

    if ingest:
        click.echo("\n  Running ingest for scenery metadata...")
        # Scenery files go through the docs chunker (markdown)
        from ingest import ingest as run_ingest
        run_ingest.main(["--source", "docs"], standalone_mode=False)


if __name__ == "__main__":
    main()
