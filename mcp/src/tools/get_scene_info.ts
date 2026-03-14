import { Stallion } from "../stallion.js";

const OUTPUT_PATH = process.env.SCENE_INFO_PATH ?? "cavalry_scene_info.json";

export async function handleGetSceneInfo(stallion: Stallion): Promise<string> {
  const script = `
var comp = api.getActiveComp();
var info = {
  comp: comp,
  layers: api.getAllSceneLayers().map(function(id) {
    return { id: id, name: api.getNiceName(id), type: api.getLayerType(id) };
  })
};
api.writeToFile("${OUTPUT_PATH}", JSON.stringify(info, null, 2), true);
`.trim();

  await stallion.runScript(script);
  return `Scene info written to: ${OUTPUT_PATH}\nRead that file to get the layer list and composition details.`;
}
