// src/rag.ts
import * as lancedb from "@lancedb/lancedb";

export interface Chunk {
  id: string;
  content: string;
  source: string;
  channel: string;
  author: string;
  timestamp: string;
  tags: string[];
  score?: number;
}

export class RagConfig {
  backend: string;
  lancedbPath: string;
  ollamaHost: string;
  supabaseUrl: string;
  supabaseKey: string;

  constructor(env: Record<string, string | undefined>) {
    this.backend = env["DB_BACKEND"] ?? "local";
    this.lancedbPath = env["LANCEDB_PATH"] ?? "./data/lancedb";
    this.ollamaHost = env["OLLAMA_HOST"] ?? "http://localhost:11434";
    this.supabaseUrl = env["SUPABASE_URL"] ?? "";
    this.supabaseKey = env["SUPABASE_KEY"] ?? "";
  }
}

async function embedQuery(query: string, ollamaHost: string): Promise<number[]> {
  const response = await fetch(`${ollamaHost}/api/embeddings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model: "nomic-embed-text", prompt: query }),
  });
  const data = await response.json() as { embedding: number[] };
  return data.embedding;
}

export async function search(
  query: string,
  cfg: RagConfig,
  topK: number = 10
): Promise<Chunk[]> {
  try {
    const embedding = await embedQuery(query, cfg.ollamaHost);

    if (cfg.backend === "local") {
      const db = await lancedb.connect(cfg.lancedbPath);
      const table = await db.openTable("cavalry_knowledge");
      const results = await table
        .vectorSearch(embedding)
        .limit(topK)
        .toArray();

      return results.map((r: any) => ({
        id: r.id,
        content: r.content,
        source: r.source,
        channel: r.channel,
        author: r.author,
        timestamp: r.timestamp,
        tags: r.tags ?? [],
        score: r._distance,
      }));
    }

    if (cfg.backend === "supabase") {
      const { createClient } = await import("@supabase/supabase-js");
      const supabase = createClient(cfg.supabaseUrl, cfg.supabaseKey);
      const { data, error } = await supabase.rpc("match_cavalry_knowledge", {
        query_embedding: embedding,
        match_count: topK,
      });
      if (error) throw error;
      return (data ?? []).map((r: any) => ({
        id: r.id,
        content: r.content,
        source: r.source,
        channel: r.channel,
        author: r.author,
        timestamp: r.timestamp,
        tags: r.tags ?? [],
        score: r.similarity,
      }));
    }

    throw new Error(`Unknown backend: ${cfg.backend}`);
  } catch (err) {
    console.error("[rag] search failed:", err);
    return [];
  }
}
