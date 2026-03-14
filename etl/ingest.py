# ingest.py
import os
import json
import click
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv

from chunkers.cv import chunk_cv
from chunkers.discord import chunk_discord_export
from chunkers.markdown import chunk_markdown
from chunkers.script import chunk_script
from embedder import embed_texts, EmbedderConfig
from store import KnowledgeStore, StoreConfig

load_dotenv()

SOURCES_DIR = Path(__file__).parent / "sources"


def get_embedder_cfg() -> EmbedderConfig:
    backend = os.getenv("EMBED_BACKEND", "ollama")
    return EmbedderConfig(
        backend=backend,
        ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
    )


def get_store_cfg() -> StoreConfig:
    return StoreConfig(
        lancedb_path=os.getenv("LANCEDB_PATH", str(Path(__file__).resolve().parent.parent / "data" / "lancedb")),
    )


def embed_and_upsert(chunks: list[dict], embedder_cfg: EmbedderConfig, store: KnowledgeStore) -> int:
    if not chunks:
        return 0
    texts = [c["content"] for c in chunks]
    embeddings = embed_texts(texts, embedder_cfg)
    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb
    store.upsert(chunks)
    return len(chunks)


CV_DIR = Path(__file__).resolve().parent.parent / "data" / "scenery_cv"


@click.command()
@click.option("--source", type=click.Choice(["discord", "docs", "manual", "scripts", "scenery", "cv", "all"]), required=True)
@click.option("--path", default=None, help="Path to specific file (discord source only)")
@click.option("--reset", is_flag=True, default=False, help="Wipe and re-ingest all data")
def ingest(source: str, path: str | None, reset: bool):
    """Ingest knowledge sources into LanceDB."""
    embedder_cfg = get_embedder_cfg()
    store = KnowledgeStore(get_store_cfg())

    if reset:
        click.echo("Resetting knowledge base...")
        store.reset()

    total = 0

    if source in ("discord", "all"):
        discord_dir = SOURCES_DIR / "discord"
        files = [Path(path)] if path else list(discord_dir.glob("*.json"))
        for f in tqdm(files, desc="Discord"):
            data = json.loads(f.read_text(encoding="utf-8"))
            chunks = chunk_discord_export(data)
            total += embed_and_upsert(chunks, embedder_cfg, store)

    if source in ("manual", "docs", "scenery", "all"):
        dirs = []
        if source in ("manual", "all"):
            dirs.append(SOURCES_DIR / "manual")
        if source in ("docs", "all"):
            dirs.append(SOURCES_DIR / "docs")
        if source in ("scenery", "all"):
            dirs.append(SOURCES_DIR / "scenery")
        for d in dirs:
            for f in tqdm(list(d.glob("*.md")) + list(d.glob("*.txt")), desc=f"Markdown ({d.name})"):
                text = f.read_text(encoding="utf-8")
                chunks = chunk_markdown(text, source=d.name, channel=f.stem)
                total += embed_and_upsert(chunks, embedder_cfg, store)

    if source in ("scripts", "all"):
        scripts_dir = SOURCES_DIR / "scripts"
        for f in tqdm(list(scripts_dir.glob("*.js")), desc="Scripts"):
            code = f.read_text(encoding="utf-8")
            chunks = chunk_script(code, filename=f.name)
            total += embed_and_upsert(chunks, embedder_cfg, store)

    if source in ("cv", "all"):
        for f in tqdm(list(CV_DIR.glob("*.cv")), desc="CV Scenes"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                chunks = chunk_cv(data, filename=f.name)
                total += embed_and_upsert(chunks, embedder_cfg, store)
            except Exception as e:
                click.echo(f"  Warning: skipping {f.name}: {e}")

    click.echo(f"Done. {total} chunks ingested. Total in DB: {store.count()}")


if __name__ == "__main__":
    ingest()
