<img src="https://cavalry.scenegroup.co/wp-content/uploads/2022/03/cavalry-logo.svg" alt="Cavalry" width="200"/>

# WRA Cavalry Assistant

An AI assistant for [Cavalry](https://cavalry.scenegroup.co/) that lets Claude write and run Cavalry scripts directly — no copy-pasting, no switching windows.

---

## What it does

- **Write & run scripts** — Claude executes Cavalry JavaScript live via the Stallion bridge
- **Knows the docs** — searches 37,000+ chunks of Cavalry documentation semantically
- **Scene-aware** — reads and saves your active scene
- **Stays current** — auto-loads a verified best-practices reference on every session

---

## Requirements

| Tool | Purpose |
|------|---------|
| [Cavalry](https://cavalry.scenegroup.co/) | The app — needs Stallion enabled |
| [Node.js 18+](https://nodejs.org/) | Runs the MCP server |
| [Ollama](https://ollama.com/) | Local embeddings (or Docker) |
| [Claude Code](https://claude.ai/claude-code) | The AI client |

---

## Setup

### 1. Install

```bash
git clone <repo-url> cavalry-assistant
cd cavalry-assistant
cp .env.example .env
npm install --prefix mcp
npm run build --prefix mcp
```

### 2. Start Ollama

```bash
# Docker (recommended)
docker compose up ollama -d
docker exec -it cavalry-assistant-ollama-1 ollama pull nomic-embed-text

# Or local Ollama
ollama pull nomic-embed-text
```

### 3. Connect to Claude Code

The `.mcp.json` in this folder auto-registers when you open it in Claude Code. Or manually:

```bash
claude mcp add cavalry-assistant node mcp/dist/index.js
```

### 4. Enable Stallion in Cavalry

`Scripts > Stallion` — leave it running on port 8080.

### 5. Start a session

```
/cavalry
```

Claude pings Stallion and confirms the connection.

---

## Docker (full stack)

```bash
docker compose up -d
```

Rebuild the knowledge base (optional):

```bash
docker compose --profile tools run etl python ingest.py --source all
```

---

## Rebuilding the Knowledge Base

The knowledge base comes pre-built in `data/lancedb/`. To rebuild:

```bash
cd etl
pip install -r requirements.txt

python ingest.py --source docs      # official docs
python ingest.py --source discord   # Discord export (needs DISCORD_TOKEN)
python ingest.py --source all --reset
```

---

## Good to know

- Stallion always responds `"Success"` — check Cavalry's console panel for actual errors
- Always start scene-modifying scripts with `api.stop()`
- Full API reference: `prompts/cavalry-best-practices.md`

---

## Credits

Built with:

- [Cavalry](https://cavalry.scenegroup.co/) by **Scene Group** — the animation software this wraps
- [Stallion](https://docs.cavalry.scenegroup.co/) — Cavalry's built-in scripting bridge
- [Model Context Protocol SDK](https://github.com/modelcontextprotocol/typescript-sdk) by **Anthropic**
- [LanceDB](https://github.com/lancedb/lancedb) — vector database for RAG
- [Ollama](https://ollama.com/) + [nomic-embed-text](https://ollama.com/library/nomic-embed-text) — local embeddings

Knowledge base sourced from the [Cavalry official docs](https://docs.cavalry.scenegroup.co/) and the Cavalry community.
