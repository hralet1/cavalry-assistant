import { Stallion } from "../stallion.js";

export async function handleSaveScene(
  filePath: string | undefined,
  stallion: Stallion
): Promise<string> {
  const script = filePath
    ? `api.saveSceneAs("${filePath}");`
    : `api.saveScene();`;
  await stallion.runScript(script);
  return filePath ? `Scene saved to: ${filePath}` : "Scene saved.";
}
