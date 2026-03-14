# Cavalry Learning Resources & Community

## Official
- Docs: https://docs.cavalry.scenegroup.co/
- YouTube: https://www.youtube.com/@cavalryapp/videos
- Discord: https://discord.com/invite/avzgNKk
- Support: https://cavalry.scenegroup.co/support/

## Community
- Scenery.io (https://scenery.io/) — 140+ downloadable scene files, scripts, palettes, easing curves. Free + patron tier with scene graphs. Best way to learn by reverse-engineering real projects.
- Canvalry Scripts (https://github.com/phillip-motion/Canvalry-scripts) — Canva's Motion team scripts: Convert Frame Rate, Renamer, CSS Gradient Converter, Reduce Compositions, Remove Unused Assets, Localiser, Find and Replace Text
- cavalry-types NPM (https://www.npmjs.com/package/@scenery/cavalry-types) — TypeScript definitions for IDE autocompletion

## YouTube Channels (community recommended)
- Pepko Motion — "Cavalry pro" per community, advanced techniques
- Mojiff — Quick 2-3 min tutorials
- Kyle Daily — Image Sampler, Domestika course author
- Heyalisa Motion — Various techniques + Notion learning template
- Alex Amor, Eliott Mosher, Nick the Ritter

## Courses
- Kyle Daily on Domestika — "Introduction to Cavalry for Motion Graphics" (98% positive, 5k students)
- Scenery Typographic Animations workshop (Antonin Waterkeyn)
- LinkedIn Learning — "Learning Cavalry" course
- Heyalisa Notion Guide (https://heyalisa.gumroad.com/l/cavalryguide)

## Official Example Files (14 scenes, all on scenery.io)
1. Text, Sleep, Repeat — string manipulation + duplicated backgrounds
2. Infrequency — line + duplicator + oscillator deformation + staggered frequency
3. Concentrick — concentric circles via point distribution + staggered radius
4. Mazin — grid pattern, rotated lines, value arrays + falloff
5. Joy Rig — rig control + keyframe layers
6. Ring Ting — dots in ring + path deformation + noise
7. Interlink — arcs duplicated into interlocking patterns
8. Focus — conical gradient shader + oscillating blur
9. Optical Art — masked circles + staggered positioning
10. Button — UI mockup, drop shadow + falloff interaction
11. See — rectangle on path + noise deformation
12. Night and Day — scene states via null-controlled multipliers
13. Quad Tree — sub-mesh distribution
14. Data — Google Sheets integration, dynamic bar charts

## Learning Path (Elena Kudriavtseva)
1. Start with 4-5 min tutorials for quick wins
2. Learn basics (shapes, duplicators, behaviours)
3. Study project files from Scenery.io — reverse-engineer
4. Read official docs + practice examples
5. Search Discord for specific questions
6. Recreate tutorials, save organized files
7. Keep it fun and experimental

## Key Concepts to Master First
- Duplicator + Distribution types (Grid, Circle, Path, Linear)
- Oscillator (wave types, stagger, frequency, looping)
- Stagger behaviour
- Noise behaviour
- Sub-Mesh for per-copy control
- Connections (procedural graph thinking)
- Falloffs for spatial control

## Stallion Bridge (VSCode Extension)
- HTTP bridge: POST to http://127.0.0.1:8080/post
- Format: {"type": "script", "code": "..."}
- Port 8080 hardcoded, localhost only
- Supports: script, javaScriptShape, javaScript, javaScriptModifier, javaScriptDeformer, javaScriptEmitter, skslShader, skslFilter, renderSetupExpression, preRenderExpression, postRenderExpression
- Use "path" instead of "code" for UI scripts (avoid merging into Stallion UI)
- GitHub: https://github.com/scenery-io/stallion
- VSCode Marketplace: search "Cavalry Bridge" by Scenery
