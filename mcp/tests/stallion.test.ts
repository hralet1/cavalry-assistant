// tools/cavalry-assistant/mcp/tests/stallion.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { Stallion } from "../src/stallion.js";

describe("Stallion", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it("sends POST to /post with script payload", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      text: async () => "Success",
    });
    global.fetch = mockFetch as any;

    const stallion = new Stallion("127.0.0.1:8080");
    await stallion.runScript("var x = 1;");

    expect(mockFetch).toHaveBeenCalledWith(
      "http://127.0.0.1:8080/post",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ type: "script", code: "var x = 1;" }),
      })
    );
  });

  it("ping returns reachable=true when host responds", async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, text: async () => "Success" }) as any;

    const stallion = new Stallion("127.0.0.1:8080");
    const result = await stallion.ping();

    expect(result.reachable).toBe(true);
    expect(result.latency_ms).toBeGreaterThanOrEqual(0);
  });

  it("ping returns reachable=false when host unreachable", async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error("ECONNREFUSED")) as any;

    const stallion = new Stallion("127.0.0.1:8080");
    const result = await stallion.ping();

    expect(result.reachable).toBe(false);
    expect(result.latency_ms).toBe(-1);
  });

  it("runScript returns Success string", async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, text: async () => "Success" }) as any;

    const stallion = new Stallion("127.0.0.1:8080");
    const result = await stallion.runScript("api.saveScene();");

    expect(result).toBe("Success");
  });
});
