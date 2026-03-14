# Cavalry MCP + Stallion — Patterns & Lessons

## Stallion Bridge
- Built into Cavalry: **Scripts > Stallion** to start
- Listens on `127.0.0.1:8080`
- POST to `/post` with JSON `{"type": "script", "code": "..."}`
- **Always returns "Success"** — no script output/return values come back
- Scripts DO execute! Errors only visible in Cavalry's console panel (user must report them)
- `console.log()` output goes to Cavalry console, not returned via HTTP
- `api.writeToFile()` WORKS in Stallion — use it to get data back

## MCP Server
- Location: `C:/Users/LEX/cavalry-mcp/` (also synced to project `tools/cavalry-mcp/`)
- **Known issue**: MCP read tools return "Success" not actual data (Stallion constraint)
- **Workaround**: Use `api.writeToFile()` to temp file, then Read tool to get data

## Cavalry JavaScript API — Verified Reference

### Core Functions
```
api.create(layerType, name) → string
api.primitive(type, name) → string          // rectangle, ellipse, star, polygon, arrow, arc, ring, superEllipse, squircle
api.deleteLayer(layerId)
api.rename(layerId, name)                   // NOT setNiceName
api.getNiceName(layerId) → string
api.getLayerType(layerId) → string
api.layerExists(layerId) → bool
api.set(layerId, {attrPath: value, ...})
api.get(layerId, attrPath) → value          // FAILS on compound types (int2, double2) — get children instead
api.getAttributes(layerId) → [string]
api.getAttrType(layerId, attrPath) → string // int, double, int2, double2, enum, bool, layerId, color
api.hasAttribute(layerId, attrId) → bool
api.connect(fromId, fromAttr, toId, toAttr, force?)
api.disconnect(fromId, fromAttr, toId, toAttr)
api.setGenerator(layerId, "generator", type)     // 3 ARGS always
api.getGenerators(layerId) → [string]            // returns ["material","generator","stroke"]
api.parent(childId, parentId)
api.getChildren(layerId) → [string]
api.select(layers)
api.getSelection() → [string]
api.getAllSceneLayers() → [string]
api.getActiveComp() → string
api.setFrame(frame)                         // NOT setCurrentFrame
api.getFrame() → int
api.play() / api.stop()
api.keyframe(layerId, frame, {attrs})
api.magicEasing(layerId, attrId, frame, easingName)
api.setFill(layerId, isOn) / api.setStroke(layerId, isOn)
api.renderPNGFrame(filePath, scalePercent)
api.saveScene() → bool
api.saveSceneAs(filePath)
api.openScene(filePath)
api.writeToFile(path, content, overwrite?) → bool
api.readFromFile(path) → string
api.duplicate(layerId) → string
```

### Functions That DO NOT Exist
- `api.setNiceName()` → use `api.rename()`
- `api.setCurrentFrame()` → use `api.setFrame()`
- `api.getAllLayerTypes()` → needs 1 arg (unknown what)
- `cavalry.alert()` → does NOT work in Stallion
- `api.getSceneLayers()` → use `api.getAllSceneLayers()`
- `javaScriptUtility` layer type → does NOT exist, only `javaScriptShape`

## Verified Attribute Types & Paths

### basicShape (via api.primitive("rectangle"))
| Attribute | Type | Default |
|-----------|------|---------|
| `generator.dimensions` | double2 | [200, 200] |
| `generator.cornerRadius` | double | 0 |
| `generator.chamfer` | bool | false |
| `generator.edgeDivisions` | int2 | [0, 0] |
| `material.materialColor` | color | {r:100,g:100,b:100,a:255} |
| `material.alpha` | int | 100 |
| `opacity` | int | 100 |
| `position` | point | {x:0,y:0,z:0} |
| `rotation` | point | {x:0,y:0,z:0} |
| `scale` | point | {x:1,y:1} |

**IMPORTANT**: `api.primitive("rectangle")` gives `generator.dimensions`. `api.create("basicShape")` gives polygon with `generator.radius` and `generator.sides`. They are DIFFERENT!

### oscillator (verified)
| Attribute | Type | Default |
|-----------|------|---------|
| `minimum` | double | -10 |
| `maximum` | double | 10 |
| `frequency` | double | 5 |
| `stagger` | double | 20 |
| `strength` | double | 100 |
| `strengthToZero` | bool | true |
| `waveType` | enum | 0 |
| `trigType` | enum | 0 |
| `numberOfWaves` | double | 10 |
| `timeOffset` | double | 0 |
| `timeScale` | double | 1 |
| `offset` | double | 0 |

### duplicator (verified)
| Attribute | Type | Default |
|-----------|------|---------|
| `generator.count` | int2 | {x:3,y:3} |
| `generator.size` | double2 | {x:200,y:200} |
| `generator.direction` | enum | 0 |
| `generator.offset` | double2 | {x:0,y:0} |
| `generator.distributionMode` | enum | 0 |
| `shapes` | array | null — connect shapes here |
| `shapePosition` | point | {x:0,y:0} |
| `shapeRotation` | double | 0 |
| `shapeScale` | point | {x:1,y:1} |
| `shapeOpacity` | double | 100 |
| `shapeVisibility` | bool | true |
| `shapeTimeOffset` | double | 0 |
| `deformers` | array | null — connect subMesh here |
| `filters` | array | null — connect filters here |

### gridDistribution (separate layer, connect to duplicator.generator)
| Attribute | Type | Default |
|-----------|------|---------|
| `count` | int2 | {x:3,y:3} |
| `size` | double2 | {x:200,y:200} |
| `offset` | double2 | {x:0,y:0} |
| `direction` | enum | 0 |
| `distributionMode` | enum | 0 |

### glowFilter (verified)
| Attribute | Type | Default |
|-----------|------|---------|
| `blur` | double2 | [20,20] |
| `intensity` | double | 1 |
| `glowColor` | color | {r:255,g:255,b:255,a:255} |
| `blendMode` | enum | 12 |
| `drawMode` | enum | 0 |
| `gamma` | double | 1 |
| `whitePoint` | double | 1 |

### subMesh (verified)
| Attribute | Type | Default |
|-----------|------|---------|
| `shapeOpacity` | double | 100 |
| `shapePosition` | point | {x:0,y:0} |
| `shapeRotation` | double | 0 |
| `shapeScale` | point | {x:1,y:1} |
| `material` | layerId | null — connect colorMaterial here |
| `fillReplacementMode` | enum | 0 (0=none, 1=replace) |
| `fillBehaviours` | array | null |
| `levels` | int2 | {x:3,y:3} |
| `levelMode` | enum | 0 |
| `indexMode` | enum | 0 |
| `strength` | double | 100 |

### colorMaterial
| Attribute | Type | Default |
|-----------|------|---------|
| `materialColor` | color | {r:100,g:100,b:100,a:255} |
| `alpha` | int | 100 |

### random
| Attribute | Type | Default |
|-----------|------|---------|
| `minimum` | double | 0 |
| `maximum` | double | 10 |
| `seed` | int | 0 |
| `useIndex` | bool | true |

### Color Format
Colors use RGBA object: `{"r": 255, "g": 0, "b": 0, "a": 255}`
NOT hex strings!

### Compound Types (int2, double2)
Set with arrays `[x, y]` or objects `{"x": N, "y": N}`.
`api.get()` on compound types may throw "expected String, typeof=object" — get child attrs instead.

## Working Patterns

### Perfect Loop Oscillator (CRITICAL)
```
Formula: freq = N / duration_seconds (N = integer cycles)
  duration = totalFrames / fps

At 30fps, 120 frames = 4.0s:
  freq = N/4.0 → 0.25, 0.5, 0.75, 1.0, 1.25...
  period = 1/freq → 4.0, 2.0, 1.333, 1.0, 0.8...

At 25fps, 120 frames = 4.8s:
  freq = N/4.8 → 0.625 (N=3), 1.25 (N=6)

Loop-safe stagger with visible wave:
  stagger = period × M (M = any positive integer)
  This offsets each copy by whole periods → all loop perfectly
  e.g. freq=0.75, period=1.333: stagger=1.333 (1 period spread)

  WARNING: stagger = arbitrary value BREAKS the loop!
  The fraction period/num_copies does NOT guarantee looping.

strengthToZero MUST be false for looping

ALWAYS audit layer IDs before setting attrs — deleted layers cause
"Attribute not found" errors that kill the entire script.
Use api.layerExists(id) or re-scan with getAllSceneLayers().
```

### Random Colors on Duplicator Copies
```javascript
var randR = api.create("random", "RandR");
api.set(randR, {"minimum": 50, "maximum": 255, "seed": 42});
api.connect(randR, "id", rect, "material.materialColor.r", true);
// repeat for G, B with different seeds
```

### SubMesh Blue Chaser
```javascript
var sub = api.create("subMesh", "Chaser");
api.connect(sub, "id", dup, "deformers");
var blueMat = api.create("colorMaterial", "Blue");
api.set(blueMat, {"materialColor": {"r": 30, "g": 100, "b": 255, "a": 255}});
api.connect(blueMat, "id", sub, "material", true);
api.set(sub, {"fillReplacementMode": 1});
var osc = api.create("oscillator", "ChaseOsc");
api.connect(osc, "id", sub, "shapeOpacity");
```

### Grid Duplicator
```javascript
var grid = api.create("gridDistribution", "Grid");
api.set(grid, {"count": [8, 8], "size": [900, 900]});
var dup = api.create("duplicator", "Dup");
api.connect(grid, "id", dup, "generator", true);
```

### Mixed Shapes in Duplicator
```javascript
// Create both shapes yourself, connect both to duplicator.shapes
var rect = api.primitive("rectangle", "Square");
api.set(rect, {"generator.dimensions": [80, 80]});
var circle = api.primitive("ellipse", "Circle");
api.set(circle, {"generator.radius": [40, 40]});
api.connect(rect, "id", dup, "shapes");
api.connect(circle, "id", dup, "shapes");
// autoId=true (default) cycles through shapes automatically
```

### writeToFile — Use Project Path
```javascript
// Temp folder path can fail silently. Use project path instead:
api.writeToFile("D:/00-Projet_en_cours/MULTICOLORE_100SC_26/cav_debug.txt", info, true);
```

## Gotchas
1. Stallion wraps code in `(function() { ... })()` — top-level `return` won't work
2. `api.set()` silently ignores invalid attribute names — errors only in Cavalry console
3. **Stallion always returns "Success"** even when scripts error
4. `api.writeToFile()` DOES work in Stallion — use temp files for data extraction
5. Always clean up ALL layers before rebuilding to avoid stale references
6. `api.setGenerator` takes 3 args: `(layerId, "generator", "rectangle")`
7. `api.primitive("rectangle")` has `generator.dimensions`, `api.create("basicShape")` has `generator.radius`/`generator.sides`
8. Duplicator uses `shapes` not `inputShape`
9. Grid requires separate `gridDistribution` layer connected to duplicator's `generator`
10. Colors are RGBA objects, NOT hex strings
11. `api.get()` fails on compound types — use child attributes
12. `api.duplicate()` takes 2 args: `(layerId, withInputConnections:bool)`
13. Magic easing — FIXED: MCP now uses official names: SlowIn, SlowOut, SlowInSlowOut, VerySlowIn, VerySlowOut, SpringIn, SpringOut, AnticipateIn, OvershootOut, BounceIn, BounceOut, BounceInBounceOut, None
14. `api.openScene()` takes 2 args: `(filePath, force:bool)` — force=true skips save dialog

## MCP Tool Reference (18 tools)

### Scene Tools
| Tool | What it does | Notes |
|------|-------------|-------|
| `cavalry_ping` | Check Stallion bridge reachable | No args |
| `cavalry_get_composition_info` | Get resolution, fps, frame range | Returns via writeToFile workaround |
| `cavalry_get_scene_layers` | List all layers with IDs/types | Returns via writeToFile |
| `cavalry_open_scene` | Open .cv file | Needs absolute path |
| `cavalry_save_scene` | Save / Save As | Optional filePath for Save As |

### Layer Tools
| Tool | What it does | Notes |
|------|-------------|-------|
| `cavalry_create_layer` | Create by layerType + name | Use for behaviours, materials, etc |
| `cavalry_delete_layers` | Delete by ID array | layerIds: [string] |
| `cavalry_duplicate_layer` | Duplicate a layer | Single layerId |
| `cavalry_get_selected_layers` | Get selection | No args |
| `cavalry_select_layers` | Select by ID array | layerIds: [string] |
| `cavalry_get_bounding_box` | Get bbox of layer | Returns via writeToFile |

### Attribute Tools
| Tool | What it does | Notes |
|------|-------------|-------|
| `cavalry_get_attribute` | Read attribute value | Returns via writeToFile |
| `cavalry_set_attribute` | Set attributes map | {attrPath: value, ...} |
| `cavalry_connect` | Connect layers | sourceAttr="id" for main output |
| `cavalry_set_generator` | Change generator type | e.g. "rectangle", "ellipse" |
| `cavalry_add_dynamic_attribute` | Add custom attr | Types: int, double, bool, string, color, int2d, double2d, position2d |
| `cavalry_get_attributes` | List all attrs + types + values | Great for discovery |
| `cavalry_disconnect` | Disconnect a connection | Mirror of cavalry_connect |
| `cavalry_get_connections` | Inspect all in/out connections | Returns JSON graph info |

### Animation Tools
| Tool | What it does | Notes |
|------|-------------|-------|
| `cavalry_keyframe` | Set keyframe | frame + {attr: value} map |
| `cavalry_magic_easing` | Apply easing | SlowIn, SlowOut, SlowInSlowOut, VerySlowIn, VerySlowOut, SpringIn, SpringOut, BounceIn, BounceOut, BounceInBounceOut, AnticipateIn, OvershootOut, None |
| `cavalry_set_current_frame` | Set playhead | frame number |

### Render Tools
| Tool | What it does | Notes |
|------|-------------|-------|
| `cavalry_render_png` | Render current frame | filePath + optional scale% |

### Scripting
| Tool | What it does | Notes |
|------|-------------|-------|
| `cavalry_run_script` | Execute arbitrary JS | Most flexible — use when no tool fits |

## Distribution Types (21 total)
Array, Circle, Custom, Fibonacci, Grid, Intersections, Linear, Mask,
Math, Particle, Path, Point, Random, Rose, Shape Edges, Shape Points,
Sort, Shuffle, Sub-Mesh, Transform, Voxelize

## Script UI Widgets (for run_script UIs)
Button, Checkbox, NumericField, LineEdit, MultiLineEdit, Slider, DropDown,
FilePath, ColorChip, ColorWheel, ColorPicker, Label, Image, ProgressBar,
Draw, List, Container, Modal, ImageButton
Layouts: HLayout, VLayout, FlowLayout, TabView, PageView, ScrollView

## Official Example Patterns Worth Studying
- **Isometric**: rotation + scale.y + skew.x (SSR30 technique)
- **Variable Font with Falloff**: Layout Group + individual letter Text Shapes + Value + Falloff
- **Loop Animation Curves**: set animCurve.postInfinity=1, preInfinity=1
- **Transfer Materials**: get stroke/fill from one shape, apply to selection
- **Convert External Data**: dictionary → forEach → create shapes programmatically
