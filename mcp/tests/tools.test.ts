// tests/tools.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { Stallion } from "../src/stallion.js";
import { handlePing } from "../src/tools/ping.js";
import { handleRunScript } from "../src/tools/run_script.js";
import { handleSaveScene } from "../src/tools/save_scene.js";
import { handleGetSceneInfo } from "../src/tools/get_scene_info.js";
import { handleSearchKnowledge } from "../src/tools/search_knowledge.js";
import { RagConfig } from "../src/rag.js";

describe("ping tool", () => {
  it("returns reachable status as text", async () => {
    const mockStallion = {
      ping: vi.fn().mockResolvedValue({ reachable: true, latency_ms: 5 }),
    } as unknown as Stallion;

    const result = await handlePing(mockStallion);
    expect(result).toContain("reachable");
    expect(result).toContain("true");
  });

  it("returns unreachable message when Stallion is down", async () => {
    const mockStallion = {
      ping: vi.fn().mockResolvedValue({ reachable: false, latency_ms: -1 }),
    } as unknown as Stallion;

    const result = await handlePing(mockStallion);
    expect(result).toContain("false");
    expect(result.toLowerCase()).toContain("stallion");
  });
});

describe("run_script tool", () => {
  it("sends script to Stallion and returns result", async () => {
    const mockStallion = {
      runScript: vi.fn().mockResolvedValue("Success"),
    } as unknown as Stallion;

    const result = await handleRunScript("var x = 1;", mockStallion);
    expect(mockStallion.runScript).toHaveBeenCalledWith("var x = 1;");
    expect(result).toContain("Success");
  });
});

describe("save_scene tool", () => {
  it("runs save script without filePath", async () => {
    const mockStallion = {
      runScript: vi.fn().mockResolvedValue("Success"),
    } as unknown as Stallion;

    await handleSaveScene(undefined, mockStallion);
    const script = (mockStallion.runScript as any).mock.calls[0][0];
    expect(script).toContain("api.saveScene");
    expect(script).not.toContain("saveSceneAs");
  });

  it("runs saveSceneAs when filePath provided", async () => {
    const mockStallion = {
      runScript: vi.fn().mockResolvedValue("Success"),
    } as unknown as Stallion;

    await handleSaveScene("/tmp/test.cv", mockStallion);
    const script = (mockStallion.runScript as any).mock.calls[0][0];
    expect(script).toContain("saveSceneAs");
    expect(script).toContain("/tmp/test.cv");
  });
});

describe("get_scene_info tool", () => {
  it("writes to temp file and returns instruction", async () => {
    const mockStallion = {
      runScript: vi.fn().mockResolvedValue("Success"),
    } as unknown as Stallion;

    const result = await handleGetSceneInfo(mockStallion);
    const script = (mockStallion.runScript as any).mock.calls[0][0];
    expect(script).toContain("api.writeToFile");
    expect(result).toContain("cavalry_scene_info");
  });
});

// vi.mock at module scope — hoisted by Vitest. Use mockImplementation per-test.
const mockRagSearch = vi.fn();
vi.mock("../src/rag.js", () => ({
  search: (...args: any[]) => mockRagSearch(...args),
  RagConfig: vi.fn(),
}));

describe("search_knowledge tool", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it("returns formatted chunks when results found", async () => {
    mockRagSearch.mockResolvedValue([
      { id: "1", content: "Use api.primitive for rectangles", source: "manual", channel: "workflow", author: "system", timestamp: "", tags: [], score: 0.05 },
      { id: "2", content: "oscillator.frequency = N/duration", source: "discord", channel: "scripting", author: "alice", timestamp: "", tags: [], score: 0.12 },
    ]);

    const ragCfg = {} as RagConfig;
    const result = await handleSearchKnowledge("how to create a rectangle", 10, ragCfg);
    expect(result).toContain("api.primitive");
    expect(result).toContain("Result 1");
    expect(result).toContain("manual/workflow");
  });

  it("returns empty KB message when no results", async () => {
    mockRagSearch.mockResolvedValue([]);

    const ragCfg = {} as RagConfig;
    const result = await handleSearchKnowledge("anything", 10, ragCfg);
    expect(result.toLowerCase()).toContain("empty");
  });
});

describe("tool dispatch coverage", () => {
  it("all 5 tool handlers exist and return strings", async () => {
    const mockStallion = {
      ping: vi.fn().mockResolvedValue({ reachable: true, latency_ms: 1 }),
      runScript: vi.fn().mockResolvedValue("Success"),
    } as unknown as Stallion;

    await expect(handlePing(mockStallion)).resolves.toBeTypeOf("string");
    await expect(handleRunScript("var x=1;", mockStallion)).resolves.toBeTypeOf("string");
    await expect(handleSaveScene(undefined, mockStallion)).resolves.toBeTypeOf("string");
    await expect(handleGetSceneInfo(mockStallion)).resolves.toBeTypeOf("string");
  });

  it("all 5 named exports are functions", () => {
    expect(handlePing).toBeTypeOf("function");
    expect(handleRunScript).toBeTypeOf("function");
    expect(handleSaveScene).toBeTypeOf("function");
    expect(handleGetSceneInfo).toBeTypeOf("function");
    expect(handleSearchKnowledge).toBeTypeOf("function");
  });
});
