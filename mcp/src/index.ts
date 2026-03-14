// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

import { Stallion } from "./stallion.js";
import { RagConfig } from "./rag.js";
import { handlePing } from "./tools/ping.js";
import { handleRunScript } from "./tools/run_script.js";
import { handleSaveScene } from "./tools/save_scene.js";
import { handleGetSceneInfo } from "./tools/get_scene_info.js";
import { handleSearchKnowledge } from "./tools/search_knowledge.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const CAVALRY_HOST = process.env.CAVALRY_HOST ?? "127.0.0.1:8080";
const stallion = new Stallion(CAVALRY_HOST);
const ragCfg = new RagConfig(process.env as Record<string, string>);

const PROMPTS_PATH = path.resolve(__dirname, "../../prompts/system.md");
const BEST_PRACTICES_PATH = path.resolve(__dirname, "../../prompts/cavalry-best-practices.md");
let systemPrompt = "";
try {
  systemPrompt = fs.readFileSync(PROMPTS_PATH, "utf-8");
  // Append best practices reference if available
  try {
    const bestPractices = fs.readFileSync(BEST_PRACTICES_PATH, "utf-8");
    systemPrompt += "\n\n---\n\n" + bestPractices;
  } catch {
    // Best practices file not found — continue with system prompt only
  }
} catch {
  systemPrompt = "WRA Cavalry Assistant — system prompt not found. Run from cavalry-assistant/ root.";
}

const server = new Server(
  { name: "wra-cavalry-assistant", version: "1.0.0" },
  { capabilities: { tools: {}, prompts: {} } }
);

server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [{
    name: "cavalry_system_prompt",
    description: "WRA Cavalry Assistant system prompt — Cavalry JS API reference, coding standards, and workflow guidance",
  }],
}));

server.setRequestHandler(GetPromptRequestSchema, async (req) => {
  if (req.params.name !== "cavalry_system_prompt") {
    throw new Error(`Unknown prompt: ${req.params.name}`);
  }
  return {
    description: "WRA Cavalry Assistant system prompt",
    messages: [{
      role: "user",
      content: { type: "text", text: systemPrompt },
    }],
  };
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "cavalry_ping",
      description: "Check if Stallion bridge is reachable. Call at session start before any scripting.",
      inputSchema: { type: "object", properties: {}, required: [] },
    },
    {
      name: "cavalry_run_script",
      description: "Execute Cavalry JavaScript via Stallion. Always returns 'Success' — check Cavalry console for errors. Use api.writeToFile() to extract data.",
      inputSchema: {
        type: "object",
        properties: { script: { type: "string", description: "Cavalry JavaScript to execute" } },
        required: ["script"],
      },
    },
    {
      name: "cavalry_search_knowledge",
      description: "Search the Cavalry knowledge base (Discord, docs, workflows). Call before complex operations to get relevant patterns and gotchas.",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "Natural language search query" },
          top_k: { type: "number", description: "Number of results (default: 10)", default: 10 },
        },
        required: ["query"],
      },
    },
    {
      name: "cavalry_save_scene",
      description: "Save the current Cavalry scene.",
      inputSchema: {
        type: "object",
        properties: { filePath: { type: "string", description: "Optional: save as new file path" } },
        required: [],
      },
    },
    {
      name: "cavalry_get_scene_info",
      description: "Get current scene composition info and all layer IDs/names/types. Writes to cavalry_scene_info.json — read that file for results.",
      inputSchema: { type: "object", properties: {}, required: [] },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args } = req.params;

  try {
    let text = "";

    if (name === "cavalry_ping") {
      text = await handlePing(stallion);
    } else if (name === "cavalry_run_script") {
      const { script } = z.object({ script: z.string() }).parse(args);
      text = await handleRunScript(script, stallion);
    } else if (name === "cavalry_search_knowledge") {
      const { query, top_k } = z.object({
        query: z.string(),
        top_k: z.number().optional().default(10),
      }).parse(args);
      text = await handleSearchKnowledge(query, top_k, ragCfg);
    } else if (name === "cavalry_save_scene") {
      const { filePath } = z.object({ filePath: z.string().optional() }).parse(args ?? {});
      text = await handleSaveScene(filePath, stallion);
    } else if (name === "cavalry_get_scene_info") {
      text = await handleGetSceneInfo(stallion);
    } else {
      throw new Error(`Unknown tool: ${name}`);
    }

    return { content: [{ type: "text", text }] };
  } catch (err) {
    return {
      content: [{ type: "text", text: `Error: ${err instanceof Error ? err.message : String(err)}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("WRA Cavalry Assistant MCP server running");
