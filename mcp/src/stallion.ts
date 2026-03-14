// tools/cavalry-assistant/mcp/src/stallion.ts
export interface PingResult {
  reachable: boolean;
  latency_ms: number;
}

export class Stallion {
  private baseUrl: string;

  constructor(host: string) {
    this.baseUrl = `http://${host}`;
  }

  async runScript(code: string): Promise<string> {
    const response = await fetch(`${this.baseUrl}/post`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: "script", code }),
    });
    return response.text();
  }

  async ping(): Promise<PingResult> {
    const start = Date.now();
    try {
      await fetch(`${this.baseUrl}/post`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: "script", code: "// ping" }),
      });
      return { reachable: true, latency_ms: Date.now() - start };
    } catch {
      return { reachable: false, latency_ms: -1 };
    }
  }
}
