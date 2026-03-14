import { Stallion } from "../stallion.js";

export async function handlePing(stallion: Stallion): Promise<string> {
  const result = await stallion.ping();
  if (result.reachable) {
    return JSON.stringify({ reachable: true, latency_ms: result.latency_ms });
  }
  return JSON.stringify({
    reachable: false,
    latency_ms: -1,
    message: "Stallion is not reachable. Open Cavalry → Scripts → Stallion to start the bridge.",
  });
}
