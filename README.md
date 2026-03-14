# WRA Cavalry Assistant

MCP server for [Cavalry](https://cavalry.scenegroup.co/) animation software. Lets Claude (or any MCP-compatible AI) write and execute Cavalry JavaScript directly, with a RAG knowledge base built from the official docs and community.

## What it does

- **Execute scripts** — runs Cavalry JS in real-time via the Stallion bridge
- **Search knowledge** — semantic search over 37,000+ chunks of Cavalry docs
- **Scene awareness** — reads and saves the active Cavalry scene
- **System prompt** — auto-loads `prompts/system.md` + `prompts/cavalry-best-practices.md` as reference

## Architecture

```
cavalry-assistant/
├── mcp/              TypeScript MCP server (Stallion bridge + RAG)
├── etl/              Python ingestion pipeline (, docs, scripts)
├── prompts/          System prompt + verified best-practices reference
├── data/lancedb/     Vector knowledge base (LanceDB + nomic-embed-text)
└── docker-compose.yml  Ollama + MCP server orchestration
```

## Requirements

- [Cavalry](https://cavalry.scenegroup.co/) with Stallion enabled (`Scripts > Stallion`)
- [Node.js](https://nodejs.org/) 18+
- [Ollama](https://ollama.com/) (for local embeddings) — or Docker
- [Claude Code](https://claude.ai/claude-code) or any MCP-compatible client

## Quick Start

### 1. Clone and install

```bash
git clone <repo-url> cavalry-assistant
cd cavalry-assistant
cp .env.example .env
npm install --prefix mcp
npm run build --prefix mcp
```

### 2. Start Ollama (for embeddings)

```bash
# Option A: Docker (recommended)
docker compose up ollama -d
docker exec -it cavalry-assistant-ollama-1 ollama pull nomic-embed-text

# Option B: Local Ollama
ollama pull nomic-embed-text
```

### 3. Register with Claude Code

The `.mcp.json` in this directory auto-registers the server when you open the folder in Claude Code. Or register manually:

```bash
claude mcp add cavalry-assistant node mcp/dist/index.js
```

### 4. Open Cavalry and enable Stallion

In Cavalry: `Scripts > Stallion` — leave it running on port 8080.

### 5. Start a session

```
/cavalry
```

Claude will ping Stallion and confirm it's connected.

## Docker (full stack)

Runs Ollama + MCP server together:

```bash
docker compose up -d
```

For ETL ingestion (optional, rebuilds the knowledge base):

```bash
docker compose --profile tools run etl python ingest.py --source all
```

## ETL — Rebuilding the Knowledge Base

The knowledge base is pre-built and included in `data/lancedb/`. To rebuild from scratch:

```bash
cd etl
pip install -r requirements.txt
cp ../.env .env

# Ingest official docs (scraped from docs.cavalry.scenegroup.co)
python ingest.py --source docs

# Ingest Discord exports (requires DISCORD_TOKEN in .env)
python ingest.py --source discord

# Ingest all
python ingest.py --source all --reset
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `cavalry_ping` | Check Stallion is reachable |
| `cavalry_run_script` | Execute Cavalry JavaScript |
| `cavalry_get_scene_info` | Get active scene info |
| `cavalry_save_scene` | Save the current scene |
| `cavalry_search_knowledge` | Semantic search the knowledge base |

## Environment Variables

See `.env.example` for all configuration options.

Key variables:
- `CAVALRY_HOST` — Stallion bridge address (default: `127.0.0.1:8080`)
- `EMBED_BACKEND` — `ollama` (default) or `openai`
- `DB_BACKEND` — `local` (LanceDB, default) or `supabase`

## Notes

- Stallion always returns `"Success"` — errors appear in Cavalry's console panel
- Always call `api.stop()` as the first line of scene-modifying scripts
- See `prompts/cavalry-best-practices.md` for the full verified API reference (batch-tested)
