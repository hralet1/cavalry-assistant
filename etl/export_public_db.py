"""export_public_db.py — Build a public-safe LanceDB snapshot.

Reads the private DB, strips all Discord chunks (which contain community
member messages and usernames), and writes a clean snapshot ready for
GitHub Releases.

Private sources (excluded):  discord
Public sources (included):   docs, manual, scenery, cv_scene, script

Usage:
    python etl/export_public_db.py
    python etl/export_public_db.py --out C:/custom/path

Output: data/lancedb_public/ (gitignored — zip this for GitHub Releases)
"""
import os
import shutil
from pathlib import Path

import click
import lancedb
from dotenv import load_dotenv

load_dotenv()

PRIVATE_SOURCES = {"discord"}

DEFAULT_SRC = os.getenv("LANCEDB_PATH", str(Path(__file__).resolve().parent.parent / "data" / "lancedb"))
# Default output: sibling of private DB on same local drive (avoids network drive issues)
_src_parent = Path(DEFAULT_SRC).parent
DEFAULT_DST = str(_src_parent / "lancedb_public")
TABLE = "cavalry_knowledge"


@click.command()
@click.option("--src", default=DEFAULT_SRC, help="Path to private LanceDB (default: LANCEDB_PATH from .env)")
@click.option("--out", default=DEFAULT_DST, help="Output path for public DB")
@click.option("--zip", "do_zip", is_flag=True, default=False, help="Also create a .zip archive for release")
def main(src: str, out: str, do_zip: bool):
    """Export a public DB snapshot, excluding private sources."""

    click.echo(f"Reading from: {src}")
    src_db = lancedb.connect(src)

    try:
        tbl = src_db.open_table(TABLE)
    except Exception as e:
        click.echo(f"Error: could not open table '{TABLE}': {e}")
        raise

    df = tbl.to_pandas()
    total = len(df)
    click.echo(f"Total chunks in private DB: {total}")

    # Filter out private sources
    df_public = df[~df["source"].isin(PRIVATE_SOURCES)].copy()
    excluded = total - len(df_public)
    click.echo(f"Excluded {excluded} private chunks (sources: {PRIVATE_SOURCES})")
    click.echo(f"Public chunks: {len(df_public)}")

    # Source breakdown
    click.echo("\nSources in public DB:")
    for source, count in df_public["source"].value_counts().items():
        click.echo(f"  {source}: {count}")

    # Write public DB
    out_path = Path(out)
    if out_path.exists():
        click.echo(f"\nRemoving existing output at {out_path}")
        shutil.rmtree(out_path)

    click.echo(f"\nWriting public DB to: {out_path}")
    dst_db = lancedb.connect(str(out_path))
    dst_db.create_table(TABLE, df_public)
    click.echo("Done.")

    if do_zip:
        zip_path = str(out_path) + ".zip"
        click.echo(f"Creating zip: {zip_path}")
        shutil.make_archive(str(out_path), "zip", str(out_path.parent), out_path.name)
        size_mb = Path(zip_path).stat().st_size / 1_000_000
        click.echo(f"Zip ready: {zip_path} ({size_mb:.1f} MB)")
        click.echo("\nNext step: upload to GitHub Releases")
        click.echo("  gh release create v1.x --title 'Knowledge Base vX' " + zip_path)


if __name__ == "__main__":
    main()
