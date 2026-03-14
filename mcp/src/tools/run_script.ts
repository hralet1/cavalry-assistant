import { Stallion } from "../stallion.js";

export async function handleRunScript(script: string, stallion: Stallion): Promise<string> {
  const result = await stallion.runScript(script);
  return `Executed. Stallion response: ${result}\n\nNote: Stallion always returns "Success" even if the script errored. Check the Cavalry console for errors. Use api.writeToFile() to extract data.`;
}
