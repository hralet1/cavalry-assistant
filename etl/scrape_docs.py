"""
Scrape Cavalry documentation from docs.cavalry.scenegroup.co into markdown files.

Usage:
    python scrape_docs.py                      # scrape all pages
    python scrape_docs.py --limit 5            # test with 5 pages
    python scrape_docs.py --ingest             # scrape + ingest
    python scrape_docs.py --update             # only scrape new/changed pages
"""

import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import click
import requests
from tqdm import tqdm

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SITEMAP_URL = "https://docs.cavalry.scenegroup.co/sitemap.xml"
BASE_URL = "https://docs.cavalry.scenegroup.co"
OUTPUT_DIR = Path(__file__).resolve().parent / "sources" / "docs"
RATE_LIMIT = 0.3  # seconds between requests
MANIFEST_PATH = Path(__file__).resolve().parent / "sources" / "docs" / "_manifest.json"

# Skip non-content pages
SKIP_PATTERNS = ["/search/", "/tags/", "/category/"]


def load_manifest() -> dict:
    """Load scrape manifest — tracks URL → {hash, scraped_at} for incremental updates."""
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict):
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def fetch_sitemap() -> list[str]:
    """Get all page URLs from sitemap.xml."""
    resp = requests.get(SITEMAP_URL, timeout=30)
    resp.raise_for_status()
    urls = re.findall(r"<loc>(.*?)</loc>", resp.text)
    # Filter out non-content pages
    urls = [u for u in urls if not any(skip in u for skip in SKIP_PATTERNS)]
    # Remove the root URL duplicate if present alongside /
    return list(dict.fromkeys(urls))


def url_to_filename(url: str) -> str:
    """Convert URL path to a flat filename."""
    path = urlparse(url).path.strip("/")
    if not path:
        return "welcome"
    return path.replace("/", "_")


def extract_content(html: str) -> dict:
    """Extract title and main content from Docusaurus HTML page."""
    # Use basic regex — avoids bs4 dependency
    # Title from <h1> or <title>
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    if title_match:
        title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip()
    else:
        title_match = re.search(r"<title>(.*?)</title>", html)
        title = title_match.group(1).replace(" | Cavalry", "").strip() if title_match else "Untitled"

    # Main content is inside <article>
    article_match = re.search(r"<article[^>]*>(.*?)</article>", html, re.DOTALL)
    if not article_match:
        return {"title": title, "content": ""}

    article_html = article_match.group(1)

    # Remove breadcrumb nav
    article_html = re.sub(r"<nav[^>]*aria-label=\"Breadcrumbs\"[^>]*>.*?</nav>", "", article_html, flags=re.DOTALL)
    # Remove pagination nav
    article_html = re.sub(r"<nav[^>]*aria-label=\"Docs pages\"[^>]*>.*?</nav>", "", article_html, flags=re.DOTALL)
    # Remove anchor link icons (Docusaurus heading anchors like "â" or "🔗")
    article_html = re.sub(r'<a[^>]*class="hash-link"[^>]*>.*?</a>', "", article_html, flags=re.DOTALL)
    article_html = re.sub(r'<a[^>]*aria-hidden="true"[^>]*>.*?</a>', "", article_html, flags=re.DOTALL)
    # Remove "On this page" sidebar content
    article_html = re.sub(r"On this page", "", article_html)

    # Convert HTML to markdown-ish text
    content = html_to_markdown(article_html)
    return {"title": title, "content": content}


def html_to_markdown(html: str) -> str:
    """Convert HTML to readable markdown. Not perfect, but good enough for RAG."""
    text = html

    # Code blocks: <pre><code>...</code></pre>
    text = re.sub(
        r"<pre[^>]*><code[^>]*>(.*?)</code></pre>",
        lambda m: "\n```\n" + _decode_html(m.group(1)) + "\n```\n",
        text, flags=re.DOTALL
    )

    # Inline code
    text = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)

    # Headings
    for level in range(6, 0, -1):
        prefix = "#" * level
        text = re.sub(
            rf"<h{level}[^>]*>(.*?)</h{level}>",
            lambda m, p=prefix: f"\n{p} {_strip_tags(m.group(1)).strip()}\n",
            text, flags=re.DOTALL
        )

    # Bold / italic
    text = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", text, flags=re.DOTALL)
    text = re.sub(r"<em[^>]*>(.*?)</em>", r"*\1*", text, flags=re.DOTALL)

    # Links
    text = re.sub(
        r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
        lambda m: f"[{_strip_tags(m.group(2))}]({m.group(1)})",
        text, flags=re.DOTALL
    )

    # List items
    text = re.sub(r"<li[^>]*>(.*?)</li>", lambda m: f"- {_strip_tags(m.group(1)).strip()}\n", text, flags=re.DOTALL)

    # Paragraphs and line breaks
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<p[^>]*>", "\n", text)
    text = re.sub(r"</p>", "\n", text)
    text = re.sub(r"<div[^>]*>", "\n", text)
    text = re.sub(r"</div>", "\n", text)

    # Tables: basic conversion
    text = re.sub(r"<th[^>]*>(.*?)</th>", lambda m: f"| {_strip_tags(m.group(1)).strip()} ", text, flags=re.DOTALL)
    text = re.sub(r"<td[^>]*>(.*?)</td>", lambda m: f"| {_strip_tags(m.group(1)).strip()} ", text, flags=re.DOTALL)
    text = re.sub(r"<tr[^>]*>", "", text)
    text = re.sub(r"</tr>", "|\n", text)

    # Strip remaining tags
    text = _strip_tags(text)

    # Decode HTML entities
    text = _decode_html(text)

    # Remove stray anchor characters (â, ðŸ"—, etc.)
    text = re.sub(r"[â\u200b\u00b6]", "", text)
    # Remove duplicate titles (first line often repeats h1)
    lines = text.split("\n")
    if len(lines) > 2 and lines[0].strip() and lines[0].strip() in text[len(lines[0]):]:
        text = "\n".join(lines[1:])
    # Clean up whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)

    return text.strip()


def _strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def _decode_html(text: str) -> str:
    import html
    return html.unescape(text)


def scrape_page(url: str) -> dict | None:
    """Scrape a single docs page. Returns {title, content, url} or None."""
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code != 200:
            return None
        data = extract_content(resp.text)
        if not data["content"]:
            return None
        data["url"] = url
        return data
    except Exception as e:
        click.echo(f"  Error: {url} — {e}")
        return None


def save_as_markdown(data: dict, output_dir: Path) -> Path:
    """Save scraped page as markdown file."""
    filename = url_to_filename(data["url"])
    path = output_dir / f"{filename}.md"

    md = f"# {data['title']}\n\n"
    md += f"Source: {data['url']}\n\n"
    md += data["content"]

    path.write_text(md, encoding="utf-8")
    return path


@click.command()
@click.option("--limit", default=0, help="Limit number of pages (0 = all)")
@click.option("--ingest", is_flag=True, help="Run ETL ingest after scraping")
@click.option("--update", is_flag=True, help="Only scrape new/changed pages (skip unchanged)")
def main(limit: int, ingest: bool, update: bool):
    """Scrape Cavalry docs into markdown for knowledge base."""

    click.echo("  Fetching sitemap...")
    urls = fetch_sitemap()
    click.echo(f"  Found {len(urls)} pages in sitemap.")

    manifest = load_manifest() if update else {}

    if limit:
        urls = urls[:limit]
        click.echo(f"  Limited to {limit} pages (test mode).")

    output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    ok = 0
    skip = 0
    unchanged = 0
    total_chars = 0
    now = datetime.now(timezone.utc).isoformat()

    for url in tqdm(urls, desc="Scraping", unit=" pages"):
        data = scrape_page(url)
        if data and len(data["content"]) > 50:
            h = content_hash(data["content"])
            # Skip if content unchanged since last scrape
            if update and url in manifest and manifest[url].get("hash") == h:
                unchanged += 1
                continue
            save_as_markdown(data, output_dir)
            manifest[url] = {"hash": h, "scraped_at": now}
            ok += 1
            total_chars += len(data["content"])
        else:
            skip += 1
        time.sleep(RATE_LIMIT)

    # Always save manifest for future --update runs
    save_manifest(manifest)

    click.echo(f"\n  ┌─ SCRAPE COMPLETE ────────────────────────────")
    click.echo(f"  │  Pages scraped: {ok}")
    if update:
        click.echo(f"  │  Unchanged:     {unchanged} (skipped)")
    click.echo(f"  │  Pages skipped: {skip} (empty/error)")
    click.echo(f"  │  Total content: {total_chars:,} chars")
    click.echo(f"  │  Output: {output_dir}")
    click.echo(f"  └───────────────────────────────────────────────")

    if ingest:
        click.echo("\n  Running ingest --source docs...")
        from ingest import ingest as run_ingest
        run_ingest.main(["--source", "docs"], standalone_mode=False)


if __name__ == "__main__":
    main()
