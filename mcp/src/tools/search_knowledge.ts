import { search, RagConfig, Chunk } from "../rag.js";

export async function handleSearchKnowledge(
  query: string,
  topK: number = 10,
  ragCfg: RagConfig
): Promise<string> {
  const chunks = await search(query, ragCfg, topK);

  if (chunks.length === 0) {
    return "No relevant knowledge found. The knowledge base may be empty — run the ETL pipeline first.";
  }

  const formatted = chunks.map((c: Chunk, i: number) =>
    `--- Result ${i + 1} [${c.source}/${c.channel}] score: ${(c.score ?? 0).toFixed(3)} ---\n${c.content}`
  ).join("\n\n");

  return formatted;
}
