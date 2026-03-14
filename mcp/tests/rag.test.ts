// tests/rag.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { RagConfig, search } from "../src/rag.js";

describe("RagConfig", () => {
  it("defaults to local backend", () => {
    const cfg = new RagConfig({});
    expect(cfg.backend).toBe("local");
  });

  it("reads backend from env", () => {
    const cfg = new RagConfig({ DB_BACKEND: "supabase" });
    expect(cfg.backend).toBe("supabase");
  });

  it("reads lancedb path from env", () => {
    const cfg = new RagConfig({ LANCEDB_PATH: "/custom/path" });
    expect(cfg.lancedbPath).toBe("/custom/path");
  });

  it("reads ollama host from env", () => {
    const cfg = new RagConfig({ OLLAMA_HOST: "http://ollama:11434" });
    expect(cfg.ollamaHost).toBe("http://ollama:11434");
  });
});

// vi.hoisted ensures mockToArray is initialized before vi.mock hoisting runs
const { mockToArray } = vi.hoisted(() => ({ mockToArray: vi.fn() }));
vi.mock("@lancedb/lancedb", () => ({
  connect: vi.fn().mockResolvedValue({
    openTable: vi.fn().mockResolvedValue({
      vectorSearch: vi.fn().mockReturnValue({
        limit: vi.fn().mockReturnValue({ toArray: mockToArray }),
      }),
    }),
  }),
}));

describe("search()", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns empty array when embedQuery fetch fails (non-fatal)", async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error("ECONNREFUSED")) as any;
    const cfg = new RagConfig({ DB_BACKEND: "local", LANCEDB_PATH: "/nonexistent" });
    const results = await search("oscillator loop", cfg, 5);
    expect(results).toEqual([]);
  });

  it("returns empty array when LanceDB toArray throws (non-fatal)", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      json: async () => ({ embedding: new Array(768).fill(0.1) }),
    }) as any;
    mockToArray.mockRejectedValue(new Error("table not found"));
    const cfg = new RagConfig({ DB_BACKEND: "local", LANCEDB_PATH: "/mocked" });
    const results = await search("rectangle", cfg, 5);
    expect(results).toEqual([]);
  });

  it("maps LanceDB rows to Chunk shape", async () => {
    const mockRow = {
      id: "abc123",
      content: "Use api.primitive for rectangles",
      source: "manual",
      channel: "workflow",
      author: "system",
      timestamp: "2024-01-01T00:00:00Z",
      tags: ["api"],
      _distance: 0.05,
    };
    global.fetch = vi.fn().mockResolvedValue({
      json: async () => ({ embedding: new Array(768).fill(0.1) }),
    }) as any;
    mockToArray.mockResolvedValue([mockRow]);

    const cfg = new RagConfig({ DB_BACKEND: "local", LANCEDB_PATH: "/mocked" });
    const results = await search("rectangle", cfg, 5);

    expect(results).toHaveLength(1);
    expect(results[0].id).toBe("abc123");
    expect(results[0].content).toContain("api.primitive");
    expect(results[0].score).toBe(0.05);
  });
});
