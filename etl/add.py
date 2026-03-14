# add.py
import os
import click
from pathlib import Path
from dotenv import load_dotenv

from chunkers.markdown import chunk_markdown
from embedder import embed_texts, EmbedderConfig
from store import KnowledgeStore, StoreConfig

load_dotenv()


@click.command()
@click.option("--text", required=True, help="Knowledge text to add")
@click.option("--source", default="manual", help="Source label (default: manual)")
@click.option("--channel", default="cli", help="Channel/section label")
@click.option("--tags", default="", help="Comma-separated tags")
def add(text: str, source: str, channel: str, tags: str):
    """Add a single knowledge entry to the database."""
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    chunks = chunk_markdown(f"## Entry\n\n{text}", source=source, channel=channel, tags=tag_list)

    embedder_cfg = EmbedderConfig(
        backend=os.getenv("EMBED_BACKEND", "ollama"),
        ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
    )
    store = KnowledgeStore(StoreConfig(
        lancedb_path=os.getenv("LANCEDB_PATH", str(Path(__file__).parent.parent / "data" / "lancedb")),
    ))

    embeddings = embed_texts([c["content"] for c in chunks], embedder_cfg)
    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb

    store.upsert(chunks)
    click.echo(f"Added {len(chunks)} chunk(s). Total in DB: {store.count()}")


if __name__ == "__main__":
    add()
