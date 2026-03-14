# Cavalry Best Practices & Patterns (from official docs)

Extracted from the complete Cavalry documentation (docs.cavalry.scenegroup.co).
This is the authoritative reference for AI-assisted Cavalry scripting.

---

## 1. Layer Creation — Exact Type Strings

### api.primitive(type, name) — Shape Primitives ONLY

These create a `basicShape` with a specific generator preset. They have `generator.*` attributes.

| String | Creates | Key Attributes |
|--------|---------|---------------|
| `"rectangle"` | Rectangle | `generator.dimensions` [w,h], `generator.cornerRadius`, `generator.topRadii` [l,r], `generator.bottomRadii` [l,r], `generator.chamfer` |
| `"ellipse"` | Ellipse | `generator.radius` [rx,ry] — MUST be array, `generator.divisions` |
| `"polygon"` | Polygon | `generator.radius` (single number), `generator.sides`, `generator.divisions` |
| `"star"` | Star | `generator.outerRadius`, `generator.innerRadius`, `generator.sides`, `generator.useInnerRadius`, `generator.divisions` |
| `"arc"` | Arc | `generator.radius`, `generator.startAngle`, `generator.endAngle` |
| `"ring"` | Ring | `generator.outerRadius`, `generator.innerRadius` |
| `"arrow"` | Arrow | `generator.*` arrow-specific attrs |
| `"capsule"` | Capsule | `generator.*` capsule-specific attrs |
| `"cogwheel"` | Cogwheel | `generator.*` cogwheel-specific attrs |
| `"superEllipse"` | Super Ellipse | `generator.*` super-ellipse attrs |
| `"circle"` | Circle (alias for ellipse with equal radii) | Same as ellipse |

### api.create(type, name) — ALL Other Layer Types

#### Shapes (non-primitive)
| String | Creates |
|--------|---------|
| `"basicShape"` | Basic Shape (generic — defaults to polygon generator) |
| `"textShape"` | Text Shape |
| `"duplicator"` | Duplicator |
| `"group"` | Group (folder) |
| `"connectShape"` | Connect Shape |
| `"customShape"` | Custom Shape (instances another shape) |
| `"backgroundShape"` | Background Shape (auto-sizes to comp) |
| `"editableShape"` | Editable Shape |
| `"merge"` | Merge (joins two open paths) |
| `"outline"` | Outline (geometry stroke) |
| `"svgShape"` | SVG Shape |
| `"component"` | Component |
| `"extractSubMeshes"` | Extract Sub-Meshes |
| `"extrude"` | Extrude (Pro) |
| `"footageShape"` | Footage Shape |
| `"meshShape"` | Mesh Shape |
| `"particleShape"` | Particle Shape (Experimental, Pro) |
| `"rectanglePattern"` | Rectangle Pattern |
| `"pointsToPath"` | Points to Path |
| `"convexHull"` | Convex Hull |
| `"cornerPin"` | Corner Pin |
| `"quadTreeShape"` | Quad Tree Shape |
| `"ray"` | Ray |
| `"segmentPath"` | Segment Path |
| `"shortestPath"` | Shortest Path |
| `"isolinesShape"` | Isolines Shape |
| `"celAnimationShape"` | Cel Animation Shape |
| `"imageToShapes"` | Image to Shapes |
| `"trails"` | Trails |
| `"subMeshBoundingBox"` | Sub-Mesh Bounding Box |
| `"javaScriptShape"` | JavaScript Shape |

#### Layouts
| String | Creates |
|--------|---------|
| `"layoutGroup"` | Layout Group (replacement for deprecated Layout Shape) |
| `"spacerItem"` | Spacer Item (for use in Layout Group) |

#### Behaviours
| String | Creates |
|--------|---------|
| `"oscillator"` | Oscillator |
| `"noise"` | Noise |
| `"random"` | Random |
| `"stagger"` | Stagger |
| `"value"` | Value |
| `"value2"` | Value2 (outputs x,y) |
| `"value3"` | Value3 (outputs x,y,z) |
| `"valueBlend"` | Value Blend |
| `"value2Blend"` | Value2 Blend |
| `"value3Blend"` | Value3 Blend |
| `"valueSolver"` | Value Solver |
| `"value2Solver"` | Value2 Solver |
| `"colorBlend"` | Color Blend |
| `"subMesh"` | Sub-Mesh |
| `"pathfinder"` | Pathfinder |
| `"boolean"` | Boolean |
| `"modulate"` | Modulate |
| `"align"` | Align |
| `"lookAt"` | Look At |
| `"distance"` | Distance |
| `"bend"` | Bend Deformer |
| `"wave"` | Wave |
| `"pinch"` | Pinch |
| `"skew"` | Skew |
| `"squashAndStretch"` | Squash and Stretch |
| `"motionStretch"` | Motion Stretch |
| `"spring"` | Spring |
| `"numberRange"` | Number Range |
| `"numberRangeToColor"` | Number Range to Color |
| `"areaRange"` | Area Range |
| `"isWithin"` | Is Within |
| `"blendShape"` | Blend Shape |
| `"positionBlend"` | Position Blend |
| `"morph"` | Morph |
| `"round"` | Round |
| `"bevel"` | Bevel |
| `"chopPath"` | Chop Path |
| `"resamplePath"` | Resample Path |
| `"reversePath"` | Reverse Path |
| `"pathOffsetBehaviour"` | Path Offset |
| `"pathRelax"` | Path Relax |
| `"pathAverage"` | Path Average |
| `"extendOpenPaths"` | Extend Open Paths |
| `"applyDistribution"` | Apply Distribution |
| `"applyLayout"` | Apply Layout |
| `"autoAnimate"` | Auto Animate |
| `"autoCrop"` | Auto Crop |
| `"behaviourMixer"` | Behaviour Mixer |
| `"blendSubMeshPositions"` | Blend Sub-Mesh Positions |
| `"cleanUp"` | Clean Up |
| `"colorMaterialOverride"` | Color Material Override |
| `"alphaMaterialOverride"` | Alpha Material Override |
| `"hsvMaterialOverride"` | HSV Material Override |
| `"contoursToSubMeshes"` | Contours to Sub-Meshes |
| `"curvesToLines"` | Curves to Lines |
| `"fillRule"` | Fill Rule |
| `"flare"` | Flare |
| `"flattenShapeLayers"` | Flatten Shape Layers |
| `"fourPointWarp"` | Four Point Warp |
| `"frame"` | Frame |
| `"getVector"` | Get Vector |
| `"javaScriptDeformer"` | JavaScript Deformer |
| `"knot"` | Knot |
| `"lattice"` | Lattice |
| `"manipulator"` | Manipulator |
| `"materialSampler"` | Material Sampler |
| `"meshSolver"` | Mesh Solver |
| `"pushAlongVector"` | Push Along Vector |
| `"rubberHoseLimb"` | Rubber Hose Limb |
| `"sound"` | Sound |
| `"stitches"` | Stitches |
| `"subdivide"` | Subdivide |
| `"swapColor"` | Swap Color |
| `"travel"` | Travel Deformer |
| `"visibilitySequence"` | Visibility Sequence |
| `"voxelize"` | Voxelize |
| `"addDivisions"` | Add Divisions |
| `"3dMatrix"` | 3D Matrix |

#### Utilities
| String | Creates |
|--------|---------|
| `"null"` | Null (visible, not renderable) |
| `"math"` | Math (single channel) |
| `"math2"` | Math2 (two channels x,y) |
| `"math3"` | Math3 (three channels x,y,z) |
| `"jsMath"` | JS Math (expression-based math) |
| `"comparison"` | Comparison |
| `"logic"` | Logic |
| `"ifElse"` | If Else |
| `"falloff"` | Falloff |
| `"rangeFalloff"` | Range Falloff |
| `"colorArray"` | Color Array |
| `"valueArray"` | Value Array |
| `"value2Array"` | Value2 Array |
| `"value3Array"` | Value3 Array |
| `"stringArray"` | String Array |
| `"shapeArray"` | Shape Array |
| `"shaderArray"` | Shader Array |
| `"assetArray"` | Asset Array |
| `"typefaceArray"` | Typeface Array |
| `"sequence"` | Sequence (non-repeating numbers) |
| `"spreadsheet"` | Spreadsheet |
| `"spreadsheetLookup"` | Spreadsheet Lookup |
| `"string"` | String |
| `"stringLength"` | String Length |
| `"stringGenerator"` | String Generator |
| `"schedulingGroup"` | Scheduling Group (Pro) |
| `"indexContext"` | Index Context |
| `"lengthContext"` | Length Context |
| `"velocityContext"` | Velocity Context |
| `"velocityMagnitudeContext"` | Velocity Magnitude Context |
| `"layerSeed"` | Layer Seed |
| `"localTime"` | Local Time |
| `"accumulator"` | Accumulator |
| `"animationControl"` | Animation Control |
| `"secondsToFrames"` | Seconds to Frames |
| `"timelineCounter"` | Timeline Counter |
| `"planarCamera"` | Camera |
| `"cameraGuide"` | Camera Guide |
| `"boundingBox"` | Bounding Box |
| `"measure"` | Measure |
| `"measureText"` | Measure Text |
| `"pathLength"` | Path Length |
| `"radius"` | Radius |
| `"colorInfo"` | Color Info |
| `"contrastingColor"` | Contrasting Color |
| `"hsvColor"` | HSV Color |
| `"countSubMeshes"` | Count Sub-Meshes |
| `"getSubMeshTransform"` | Get Sub-Mesh Transform |
| `"getName"` | Get Name |
| `"imageSampler"` | Image Sampler |
| `"rigControl"` | Rig Control |
| `"javaScript"` | JavaScript Utility |
| `"dataModifier"` | Data Modifier |
| `"typeface"` | Typeface |

#### Effects — Shaders
| String | Creates |
|--------|---------|
| `"gradientShader"` | Gradient Shader |
| `"colorShader"` | Color Shader |
| `"noiseShader"` | Noise Shader |
| `"checkerboardShader"` | Checkerboard Shader |
| `"imageShader"` | Image Shader |
| `"blendShader"` | Blend Shader |
| `"voronoiShader"` | Voronoi Shader |
| `"multiPointGradientShader"` | Multi-Point Gradient Shader |
| `"shapeToShader"` | Shape to Shader |
| `"slaShader"` | SLA Shader |
| `"skslShader"` | SkSL Shader |

#### Effects — Filters
> **NOTE:** Type strings marked ✓ are batch-tested and confirmed working. Others are from docs but unverified via scripting.

| String | Creates | Status |
|--------|---------|--------|
| `"gaussianBlurFilter"` | Gaussian Blur Filter | ⚠ getAttributes returns [] — attrs inaccessible |
| `"blurFilter"` | Fast Blur Filter | ✓ (docs incorrectly said `"fastBlurFilter"`) |
| `"backgroundBlurFilter"` | Background Blur Filter | ✓ |
| `"dropShadowFilter"` | Drop Shadow Filter | ✓ color attr = `shadowColor` NOT `color` |
| `"innerShadowFilter"` | Inner Shadow Filter | ✓ |
| `"glowFilter"` | Glow Filter | ✓ blur attr = `blur` [double2] NOT `radius` |
| `"hsvAdjustmentFilter"` | HSV Adjustment Filter | ✓ |
| `"brightnessAndContrast"` | Brightness and Contrast Filter | ✓ (docs said `"brightnessAndContrastFilter"`) |
| `"levels"` | Levels Filter | ✓ (docs said `"levelsFilter"`) |
| `"invert"` | Invert Filter | ✓ (docs said `"invertFilter"`) |
| `"blackAndWhite"` | Black and White Filter | ✓ (docs said `"blackAndWhiteFilter"`) |
| `"posterizeFilter"` | Posterize Filter | ✓ |
| `"thresholdFilter"` | Threshold Filter | ✓ |
| `"gradientMapFilter"` | Gradient Map Filter | ✓ |
| `"chromaticAberrationFilter"` | Chromatic Aberration Filter | ✓ |
| `"rgbSplitFilter"` | RGB Split Filter | ✓ |
| `"distortionFilter"` | Distortion Filter | ✓ |
| `"mirrorFilter"` | Mirror Filter | ✓ |
| `"pixelateFilter"` | Pixelate Filter | ✓ |
| `"halftoneFilter"` | Halftone Filter | ✓ |
| `"ditheringFilter"` | Dithering Filter | ✓ |
| `"sharpenFilter"` | Sharpen Filter | ✓ |
| `"vignetteFilter"` | Vignette Filter | ✓ |
| `"edgeDetection"` | Edge Detection Filter | ✓ (docs said `"edgeDetectionFilter"`) |
| `"linearWipe"` | Linear Wipe Filter | ✓ (docs said `"linearWipeFilter"`) |
| `"boxBlurFilter"` | Box Blur Filter | ⚠ unverified |
| `"directionalBlurFilter"` | Directional Blur Filter | ⚠ unverified |
| `"zoomBlurFilter"` | Zoom Blur Filter | ⚠ unverified |
| `"bilateralBlurFilter"` | Bilateral Blur Filter | ⚠ unverified |
| `"luminanceBlurFilter"` | Luminance Blur Filter | ⚠ unverified |
| `"gammaFilter"` | Gamma Correction Filter | ⚠ unverified |
| `"tritoneFilter"` | Tritone Filter | ⚠ unverified |
| `"fillColorFilter"` | Fill Color Filter | ⚠ unverified |
| `"chromaKeyFilter"` | Chroma Key Filter | ⚠ unverified |
| `"shiftChannelsFilter"` | Shift Channels Filter | ⚠ unverified |
| `"distortEdgesFilter"` | Distort Edges Filter | ⚠ unverified |
| `"bulgeFilter"` | Bulge Filter | ⚠ unverified |
| `"spheriseFilter"` | Spherise Filter | ⚠ unverified |
| `"polarCoordinatesFilter"` | Polar Coordinates Filter | ⚠ unverified |
| `"grainFilter"` | Grain Filter | ⚠ unverified |
| `"scanLinesFilter"` | Scan Lines Filter | ⚠ unverified |
| `"pixelSortingFilter"` | Pixel Sorting Filter | ⚠ unverified |
| `"erosionFilter"` | Erosion Filter | ⚠ unverified |
| `"lightSweepFilter"` | Light Sweep Filter | ⚠ unverified |
| `"radialWipeFilter"` | Radial Wipe Filter | ⚠ unverified |
| `"venetianBlindsFilter"` | Venetian Blinds Filter | ⚠ unverified |
| `"slitScanFilter"` | Slit Scan Filter | ⚠ unverified |
| `"scrapeFilter"` | Scrape Filter | ⚠ unverified |
| `"stripesFilter"` | Stripes Filter | ⚠ unverified |
| `"skslFilter"` | SkSL Filter | ⚠ unverified |

#### Materials
| String | Creates |
|--------|---------|
| `"colorMaterial"` | Color Material (Fill utility) |
| `"strokeMaterial"` | Stroke Material (Stroke utility) |

---

## 2. Attribute Paths Reference

### Common Shape Attributes (all shapes)
```
position           — [x, y] (double2)
position.x         — number
position.y         — number
rotation           — compound (use rotation.z to READ — api.get returns object, not number!)
scale              — [x, y] (double2)
scale.x            — number
scale.y            — number
skew               — [x, y] (double2)
skew.x             — number
skew.y             — number
pivot              — [x, y] (double2)
pivot.x            — number
pivot.y            — number
opacity            — number (0-100)
blendMode          — int (enum)
hidden             — bool
wireframe          — bool
motionBlur         — int (enum: 0=None, 1=Full, 2=TransformOnly)
hierarchy          — bool (collapse/expand in scene tree)
deformers          — array (connect behaviours here)
filters            — array (connect filters here)
```

### Fill Attributes (shapes with fill)
```
material.materialColor   — color (RGBA object, NOT hex string)
material.colorShaders    — array (connect shaders here)
material.alpha           — number (0-100)
```

### Stroke Attributes (shapes with stroke)
```
stroke.strokeColor       — color (RGBA object)
stroke.colorShaders      — array (connect shaders here)
stroke.width             — number
stroke.alpha             — number (0-100)
stroke.capStyle          — int (0=Flat, 1=Round, 2=Projecting)
stroke.joinStyle         — int (0=Mitre, 1=Round, 2=Bevel)
stroke.mitreLimit        — number
stroke.dashPattern       — string ("10,5")
stroke.dashOffset        — number
stroke.align             — int (0=Centre, 1=Inner, 2=Outer)
stroke.trim              — bool
stroke.trimStart         — number (0..1)
stroke.trimEnd           — number (0..1)
stroke.trimTravel        — number
stroke.trimReversePath   — bool
stroke.taperedWidth      — bool
stroke.startWidth        — number
stroke.endWidth          — number
```

### Rectangle (api.primitive("rectangle"))
```
generator.dimensions     — [w, h] (MUST be array)
generator.dimensions.x   — number
generator.dimensions.y   — number
generator.cornerRadius   — number
generator.radiusMode     — int (0=All, 1=Individual)
generator.topRadii       — [l, r]
generator.bottomRadii    — [l, r]
generator.chamfer        — bool
generator.edgeDivisions  — [w, h]
```

### Ellipse (api.primitive("ellipse"))
```
generator.radius         — [rx, ry] (MUST be array, e.g. [100, 100])
generator.radius.x       — number
generator.radius.y       — number
generator.bezier         — bool
generator.divisions      — int
```

### Polygon (api.primitive("polygon"))
```
generator.radius         — number (single value, NOT array)
generator.sides          — int
generator.divisions      — int
```

### Star (api.primitive("star"))
```
generator.outerRadius    — number
generator.innerRadius    — number
generator.useInnerRadius — bool
generator.sides          — int
generator.divisions      — int
```

### Text Shape (api.create("textShape"))
```
text                     — string
font                     — compound: {"font": "Arial", "style": "Bold"}
font.font                — string (font family name)
font.style               — string (font style name)
fontSize                 — int
alignment                — int (0=Left, 1=Centre, 2=Right, 3=Justified)
verticalAlignment        — int (0=Top, 1=Centre, 2=Bottom, 3=Baseline)
characterSpacing         — number
wordSpacing              — number
lineSpacing              — number
paragraphSpacing         — number
textBoxSize              — [w, h]
autoWidth                — bool
autoHeight               — bool
shrinkToFitTextBox       — bool
avoidOrphans             — bool
forceMonospacing         — bool
formattingInputs         — array (connect other text shapes)
textPath                 — layer (connect shape for text on path)
pathLoop                 — bool
pathTravel               — number
pathPush                 — number
fontAxes.0               — number (variable font first axis)
```

### Duplicator (api.create("duplicator"))
```
shapes                   — array (connect input shapes to "shapes")
generator                — distribution generator (use api.setGenerator)
shapePosition            — [x, y] (per-duplicate position)
shapePosition.x          — number
shapePosition.y          — number
shapeRotation            — number (per-duplicate rotation)
shapeScale               — [x, y] (per-duplicate scale)
shapeScale.x             — number
shapeScale.y             — number
shapeVisibility          — bool (per-duplicate visibility)
shapeOpacity             — number (per-duplicate opacity)
autoId                   — bool (auto-cycle input shapes)
shapeId                  — int (which input shape to use, 0-based)
shapeTimeOffset          — number (animation time offset per duplicate)
useIndexContext          — bool (Advanced tab)
indexContext              — output (connect to other layers)
skipInvisibleDuplicates  — bool
```

### Grid Distribution (on duplicator after setGenerator)
```
generator.count          — [x, y]
generator.count.x        — int
generator.count.y        — int
generator.size           — [w, h]
generator.size.x         — number
generator.size.y         — number
generator.patternOffset  — [x, y]
generator.sizeMode       — int (0=Fit, 1=Step)
generator.direction      — int (0=FlowColumns, 1=FlowRows)
```

### Circle Distribution
```
generator.count          — int
generator.radius         — number
generator.startAngle     — number
generator.angle          — number (default 360)
generator.includeEnd     — bool
generator.useRotation    — bool
generator.flip           — bool
generator.travel         — number
```

### Linear Distribution
```
generator.count          — int
generator.size           — number
generator.direction      — int (0=Horizontal, 1=Vertical)
generator.sizeMode       — int (0=Fit, 1=Step)
```

### Path Distribution
```
generator.count          — int
generator.inputShape     — layer (connect a shape)
generator.travel         — number
generator.length         — number (0..1)
generator.useRotation    — bool
generator.flip           — bool
generator.countMode      — int (0=PerShape, 1=PerSubMesh, 2=PerContour)
```

### Oscillator (api.create("oscillator"))
```
trigType                 — int (0=Sine, 1=Cosine, 2=Tangent)  ← NOT "type"
waveType                 — int (0=Normal, 1=Square, 2=Triangle, 3=Sawtooth, 4=Custom)  ← NOT "waveStyle"
minimum                  — number
maximum                  — number
offset                   — number
stagger                  — number  ← ALWAYS set, never skip
separateChannels         — bool
timeMode                 — int (0=Seconds, 1=Minutes/BPM)
frequency                — number
time                     — auto-connected to comp time
timeOffset               — number (seconds)
timeScale                — number (multiplier)
strength                 — number
strengthToZero           — bool  ← NOT "strengthFadeToZero". Must be false for loops!
graph                    — Graph widget
useNormals               — bool (Deformer tab)
numberOfWaves            — int (Deformer tab)
```

### Noise (api.create("noise"))
> **CRITICAL:** ALL noise value attrs use the `generator.*` prefix. Top-level only: `strength`, `strengthToZero`, `useNormals`, `falloffs`.
```
generator.minimum        — number  ← NOT bare "minimum"
generator.maximum        — number  ← NOT bare "maximum"
generator.frequency      — number  ← NOT bare "frequency"
generator.seed           — int     ← NOT bare "seed"
generator.stagger        — number
generator.offset         — number
generator.looping        — bool
generator.loopLength     — int (frames)
generator.timeScale      — number
generator.noisePosition  — [x, y]
generator.noiseRotation  — number
generator.noiseScale     — [x, y]
generator.separateChannels — bool
generator.octaves        — int
generator.lacunarity     — number
generator.gain           — number
generator.curl           — bool
generator.curlAmplitude  — number
generator.useIndex       — bool
generator.useLayerAsSeed — bool
generator.usePosition    — bool
generator.time           — auto-connected
strength                 — number  (top-level)
strengthToZero           — bool    (top-level, NOT "strengthFadeToZero")
useNormals               — bool    (top-level)
falloffs                 — array   (top-level)
```

### Random (api.create("random"))
```
minimum                  — number
maximum                  — number
seed                     — int
useLayerAsSeed           — bool
offset                   — number
separateChannels         — bool
useBiasGraph             — bool
strength                 — number
strengthFadeToZero       — bool
useNormals               — bool
```

### Stagger (api.create("stagger"))
```
minimum                  — number
maximum                  — number
offset                   — number
graph                    — Graph widget
```

### Value (api.create("value"))
```
value                    — number
offset                   — number
timeOffset               — number
```

### Color Blend (api.create("colorBlend"))
```
gradientMode             — int
gradient                 — gradient stops
useAlpha                 — bool
```

### Gradient Shader (api.create("gradientShader"))
> **CRITICAL:** Several attrs are TOP-LEVEL, NOT under `generator.*`. See below.
```
generator.gradient       — gradient (use api.setGradientFromColors)
generator.scale          — number (Linear mode)
generator.rotation       — number (Linear mode)
generator.offset         — [x, y] (most modes)
generator.wrapUVs        — bool
gradientMode             — int (0=Conical, 1=Linear, 2=Radial, 3=Shape, 4=Sweep)  ← TOP-LEVEL, not generator.mode
screenSpace              — bool  ← TOP-LEVEL, not generator.screenSpace
reverse                  — bool  ← TOP-LEVEL, not generator.reverse
tiling                   — int (0=Clamp, 1=Repeat, 2=Mirror, 3=Decal)  ← TOP-LEVEL, not generator.tiling
alpha                    — number
blendMode                — int
```

### Sub-Mesh (api.create("subMesh"))
```
shapePosition            — [x, y]   ← NOT "position"
shapePosition.x          — number
shapePosition.y          — number
shapeRotation            — number   ← NOT "rotation"
shapeScale               — [x, y]   ← NOT "scale"
shapeOpacity             — number   ← NOT "opacity"
shapeVisibility          — bool     ← NOT "visibility"
shapeTimeOffset          — number   ← NOT "timeOffset"
pivotPosition            — int (enum)
deformers                — array
filters                  — array
levelMode                — int (0=Custom, 1=TextLines, 2=TextWords, 3=TextChars, 4=All)
flattenMeshAtLevel       — int
indexMode                — int (0=Unique, 1=ChildIndex)
fillReplacementMode      — int (0=ReplaceAll, 1=ReplaceMissing, 2=ReplaceExisting)
strength                 — number
useIndex                 — bool
material                 — layerId (connect a colorMaterial)
```

### Falloff (api.create("falloff"))
```
strength                 — number
shapeType                — int (0=Circle, 1=Rectangle, 2=Linear, 3=Sweep, 4=Shape)
size                     — [x, y]
falloffGraph             — Graph
probability              — bool
seed                     — int
enabled                  — bool
```

### Scheduling Group (api.create("schedulingGroup"))
```
childOffset              — number (connect a stagger)
sequencing               — bool
overlap                  — number
scheduleFromEnd          — bool
startFrame               — int
endFrame                 — int
orderingPolicy           — int (0=LayerOrder, 1=Alphabetical)
flipOrder                — bool
shapesOnly               — bool
```

### Color Array (api.create("colorArray"))
```
autoIndex                — bool
arrayIndex               — int  ← NOT "index"
reverse                  — bool
count                    — int (read-only)
array.0                  — color
array.1                  — color (after api.addArrayIndex)
```

### Math (api.create("math"))
```
first                    — number (first operand)
operation                — int (enum)
second                   — number (second operand)
out                      — number (read-only output — use "id" for connection)  ← NOT "result"
```

### Null (api.create("null"))
```
position                 — [x, y]
rotation                 — number
scale                    — [x, y]
shape                    — int (0=Cross, 1=Circle, 2=Square)
customColor              — bool
color                    — color
limitPosition            — bool
minimumPosition          — [x, y]
maximumPosition          — [x, y]
limitRotation            — bool
limitScale               — bool
```

### Group (api.create("group"))
```
position                 — [x, y]
rotation                 — number
scale                    — [x, y]
blendingAndOpacityMode   — int (0=Artboard, 1=IndividualShapes)
```

---

## 3. Connection Patterns

### The "id" Connection (Layer Output)
Every layer has an `id` output — this is the RESULT or OUTPUT of the layer.
When docs show `layer.id`, it means connect FROM `"id"` attribute.

```javascript
// Connect oscillator output to shape's rotation
api.connect(oscillatorId, "id", shapeId, "rotation");

// Connect shape to duplicator's input shapes
api.connect(ellipseId, "id", duplicatorId, "shapes");

// Connect shader to shape's fill
api.connect(gradientId, "id", shapeId, "material.colorShaders");

// Connect fill utility to overwrite shape's fill (force=true overwrites)
api.connect(fillId, "id", starId, "material", true);

// Connect behaviour as deformer
api.connect(noiseId, "id", shapeId, "deformers");

// Connect filter
api.connect(blurId, "id", shapeId, "filters");
```

### One-to-Many Pattern (1 behaviour -> many shapes)
One oscillator/noise/random can drive MANY shapes. Just connect multiple times:
```javascript
var osc = api.create("oscillator", "Shared Osc");
api.connect(osc, "id", shape1, "position.y");
api.connect(osc, "id", shape2, "position.y");
api.connect(osc, "id", shape3, "position.y");
```

### Behaviour -> Specific Attribute
```javascript
// Oscillator to position.x (single axis)
api.connect(oscId, "id", shapeId, "position.x");

// Oscillator to rotation
api.connect(oscId, "id", shapeId, "rotation");

// Stagger to duplicator's shapePosition.y
api.connect(staggerId, "id", duplicatorId, "shapePosition.y");

// Stagger to duplicator's shapeTimeOffset
api.connect(staggerId, "id", duplicatorId, "shapeTimeOffset");

// Random to duplicator's shapeId (pick random input shapes)
api.connect(randomId, "id", duplicatorId, "shapeId");

// Random to colorArray's index
api.connect(randomId, "id", colorArrayId, "index");

// Modulate to duplicator's shapeId
api.connect(modulateId, "id", duplicatorId, "shapeId");

// Value to text shape's fontAxes
api.connect(valueId, "id", textId, "fontAxes.0");

// Falloff to behaviour
api.connect(falloffId, "id", behaviourId, "falloffs");

// Context Index to string generator
api.connect(contextIndexId, "id", stringGenId, "generator.number");
```

### Shape -> Distribution Input Shape
```javascript
// Path distribution needs an input shape
api.connect(shapeId, "id", duplicatorId, "generator.inputShape");
```

### Duplicator Distribution Setup
```javascript
var dupId = api.create("duplicator", "Dup");
api.connect(ellipseId, "id", dupId, "shapes");
api.setGenerator(dupId, "generator", "circleDistribution");
api.set(dupId, {"generator.count": 12, "generator.radius": 200});
```

### Shader -> Shape Fill/Stroke
```javascript
// Connect to fill shaders list
api.connect(shaderId, "id", shapeId, "material.colorShaders");

// Connect to stroke shaders list
api.connect(shaderId, "id", shapeId, "stroke.colorShaders");
```

### Sub-Mesh -> Shape's Deformers
```javascript
api.connect(subMeshId, "id", textShapeId, "deformers");
```

### Scheduling Group Pattern
```javascript
var schedGroup = api.create("schedulingGroup", "Schedule");
api.parent(shape1, schedGroup);
api.parent(shape2, schedGroup);
api.parent(shape3, schedGroup);
var stagger = api.create("stagger", "Stagger");
api.connect(stagger, "id", schedGroup, "childOffset");
```

---

## 4. Scene Organization

### Parenting Rules
- `api.parent(childId, parentId)` — makes childId a child of parentId
- NOT `api.setParent()` — does not exist
- To un-parent: `api.unParent(layerId)` — moves layer up one hierarchy level
- Groups organize layers: `api.create("group", "My Group")`

### Mandatory Organization Pattern
ALWAYS parent shaders, deformers, and effects as children of the shape they affect:
```javascript
var shape = api.primitive("ellipse", "Circle");
var grad = api.create("gradientShader", "Gradient");
api.connect(grad, "id", shape, "material.colorShaders");
api.parent(grad, shape);  // ALWAYS — keeps scene tree clean

var noise = api.create("noise", "Noise Deformer");
api.connect(noise, "id", shape, "deformers");
api.parent(noise, shape);

var blur = api.create("gaussianBlurFilter", "Blur");
api.connect(blur, "id", shape, "filters");
api.parent(blur, shape);
```

### Duplicator Input Shape Transform Rule
The Duplicator IGNORES the transform (position, rotation, scale, skew, pivot) of its direct Input Shapes. This is by design to prevent confusion.

To pass transforms through to a Duplicator:
1. Create a Group
2. Make the animated shape a child of the Group
3. Add the Group as the Duplicator's Input Shape
The Group's transform is ignored, but the child shape's transform within the Group IS respected.

### Naming
- `api.rename(layerId, "New Name")` — rename a layer
- Text Shapes auto-name from their String content (disable with `automaticNaming: false`)

---

## 5. Gradient & Shader Workflows

### Creating a Gradient Fill (Verified Pattern)
```javascript
// 1. Create the gradient shader as a SEPARATE layer
var grad = api.create("gradientShader", "My Gradient");

// 2. Set gradient mode (Linear=1 is default for most uses)
api.set(grad, {"generator.mode": 1}); // 0=Conical, 1=Linear, 2=Radial, 3=Shape, 4=Sweep

// 3. Set colors using hex strings (ONLY api that accepts hex!)
api.setGradientFromColors(grad, "generator.gradient", ["#0000FF", "#FF0000"]);

// 4. Optionally set interpolation
api.setGradientInterpolation(grad, "generator.gradient", 0); // 0=Linear, 1=Step, 2=Smooth, 3=Crush, 4=SmoothBlend, 5=Contrast

// 5. Connect to shape's fill shaders
api.connect(grad, "id", shapeId, "material.colorShaders");

// 6. Parent for organization
api.parent(grad, shapeId);
```

### Gradient Shader Modes
- `0` = Conical (two-point conical gradient)
- `1` = Linear (linear gradient with scale, rotation, offset)
- `2` = Radial (centre-out gradient with radius)
- `3` = Shape (polygonal radial gradient)
- `4` = Sweep (angular sweep gradient)

### Screen Space Gradients
When `generator.screenSpace` is true, the gradient is fixed in screen space — the shape moves THROUGH the gradient. When false, the gradient "sticks" to the shape.

### Color Shader (Simple Solid Fill Override)
```javascript
var colorShader = api.create("colorShader", "Color Override");
api.set(colorShader, {"color": {r: 255, g: 0, b: 0, a: 255}});
api.connect(colorShader, "id", shapeId, "material.colorShaders");
```

### Shared Fill Utility Pattern
One Fill Utility can control multiple shapes' colors:
```javascript
var fill = api.create("colorMaterial", "Shared Fill");
api.set(fill, {"materialColor": "#6437ff"});
api.connect(fill, "id", shape1, "material", true); // force=true overwrites default
api.connect(fill, "id", shape2, "material", true);
```

### What DOES NOT work for gradients
- `api.create("linearGradient")` — no such layer type
- `api.setGenerator(id, "material", "linearGradientMaterial")` — silently ignored
- Setting `colorA`/`colorB` on shader sub-paths — no visible effect
- Setting `material.materialColor` to a gradient — materials only accept solid colors

---

## 6. Animation Patterns

### Oscillator Best Practices
```javascript
var osc = api.create("oscillator", "Osc");
api.set(osc, {
    "type": 0,              // 0=Sine, 1=Cosine, 2=Tangent
    "waveStyle": 0,         // 0=Normal, 1=Square, 2=Triangle, 3=Sawtooth
    "minimum": -100,
    "maximum": 100,
    "frequency": 1.0,       // periods per second (when timeMode=0)
    "timeScale": 1.0,       // speed multiplier
    "stagger": 25,          // ALWAYS set for duplicator use
    "strength": 100
});
```

### Perfect Loop Oscillator
```javascript
// Formula: frequency = N / duration_seconds (N = integer for complete cycles)
// duration_seconds = totalFrames / fps
// Example: 120 frames at 30fps = 4s, frequency = 1/4.0 = 0.25 for 1 cycle

api.set(oscId, {
    "frequency": 0.25,          // = 1 cycle / 4 seconds
    "strengthFadeToZero": false  // MUST be false for clean loops
});
```

### Loop with Math Utility
For frame-precise loops:
1. Create a Math Utility
2. Connect Composition's Frame Rate to Math's First
3. Set Math's Second to the number of frames for one loop
4. Set Operation to Divide
5. Connect Math output to Oscillator's Frequency

### Circular Motion Pattern
Use two oscillators with a Time Offset of 0.25 on one:
```javascript
var oscX = api.create("oscillator", "OscX");
api.set(oscX, {"type": 0, "minimum": -200, "maximum": 200, "frequency": 1});
api.connect(oscX, "id", shapeId, "position.x");

var oscY = api.create("oscillator", "OscY");
api.set(oscY, {"type": 0, "minimum": -200, "maximum": 200, "frequency": 1, "timeOffset": 0.25});
api.connect(oscY, "id", shapeId, "position.y");
```

### Stagger + Duplicator Time Offset
For sequential animation across duplicates:
```javascript
var stagger = api.create("stagger", "Time Stagger");
api.set(stagger, {"minimum": -50, "maximum": 0}); // negative min so animation starts at frame 0
api.connect(stagger, "id", duplicatorId, "shapeTimeOffset");
```
Tip: Flip the stagger graph to reverse the order (`api.flipGraph(staggerId, "graph", "vertical")`).

### Keyframe Animation
```javascript
// Set keyframes
api.keyframe(shapeId, 0, {"position.x": 0});
api.keyframe(shapeId, 60, {"position.x": 500});

// Apply Magic Easing
api.magicEasing(shapeId, "position.x", 0, "SlowOut");
api.magicEasing(shapeId, "position.x", 60, "SlowIn");
```

### Magic Easing Names (exact strings)
`"SlowIn"`, `"SlowOut"`, `"SlowInSlowOut"`, `"VerySlowIn"`, `"VerySlowOut"`, `"VerySlowInVerySlowOut"`, `"SpringIn"`, `"SpringOut"`, `"SpringInSpringOut"`, `"SmallSpringIn"`, `"SmallSpringOut"`, `"SmallSpringInSmallSpringOut"`, `"AnticipateIn"`, `"OvershootOut"`, `"AnticipateInOvershootOut"`, `"BounceIn"`, `"BounceOut"`, `"BounceInBounceOut"`, `"Custom"`, `"None"`

### Loop Animation Curves
```javascript
// Get the animation curve layer id from a keyframed attribute
var inConn = api.getInConnection(shapeId, "position.x");
var animCurveId = inConn.split('.')[0];

// Set loop modes: 0=Constant, 1=Loop, 2=LoopWithOffset, 4=Oscillate, 5=Zero
api.set(animCurveId, {"postInfinity": 1, "preInfinity": 1});
```

---

## 7. Common Workflows

### Duplicator with Random Colors
```javascript
// Create shape + duplicator
var ellipse = api.primitive("ellipse", "Dot");
api.set(ellipse, {"generator.radius": [20, 20], "hidden": true});

var dup = api.create("duplicator", "Duplicator");
api.connect(ellipse, "id", dup, "shapes");
api.setGenerator(dup, "generator", "gridDistribution");
api.set(dup, {"generator.count": [5, 5], "generator.size": [400, 400]});

// Create color array with 3 colors
var colors = api.create("colorArray", "Colors");
api.addArrayIndex(colors, "array");
api.addArrayIndex(colors, "array");
api.set(colors, {"array.0": "#ff0000", "array.1": "#00ff00", "array.2": "#0000ff"});

// Random index picker
var rand = api.create("random", "Random Color");
api.set(rand, {"minimum": 0, "maximum": 2});
api.connect(rand, "id", colors, "index");
api.connect(colors, "id", ellipse, "material.materialColor");
```

### Text Per-Character Animation
```javascript
var text = api.create("textShape", "My Text");
api.set(text, {"text": "HELLO", "fontSize": 100});

var subMesh = api.create("subMesh", "Char Animator");
api.set(subMesh, {"levelMode": 3}); // 3 = Text (Characters)
api.connect(subMesh, "id", text, "deformers");

// Now connect behaviours to subMesh attributes
var osc = api.create("oscillator", "Bounce");
api.set(osc, {"minimum": 0, "maximum": -30, "frequency": 2, "stagger": 0.1});
api.connect(osc, "id", subMesh, "position.y");
```

### Connect Shape Pattern
```javascript
var connectShape = api.create("connectShape", "Connections");
// Source distribution defaults to grid. Change if needed:
api.setGenerator(connectShape, "sourceDistribution", "circleDistribution");
api.set(connectShape, {"sourceDistribution.count": 20, "sourceDistribution.radius": 200});
```

### Scheduling Group for Sequential Timing
```javascript
var group = api.create("schedulingGroup", "Schedule");
api.parent(shape1, group);
api.parent(shape2, group);
api.parent(shape3, group);
var stagger = api.create("stagger", "Offset");
api.set(stagger, {"minimum": 0, "maximum": 30});
api.connect(stagger, "id", group, "childOffset");
```

---

## 8. Distribution Types — setGenerator Strings

Use `api.setGenerator(layerId, "generator", distributionType)`:

| Distribution String | Type |
|---------------------|------|
| `"gridDistribution"` | Grid |
| `"circleDistribution"` | Circle |
| `"linearDistribution"` | Linear |
| `"pathDistribution"` | Path (needs inputShape) |
| `"randomDistribution"` | Random |
| `"fibonacciDistribution"` | Fibonacci |
| `"mathDistribution"` | Math |
| `"arrayDistribution"` | Array |
| `"customDistribution"` | Custom (JavaScript) |
| `"pointDistribution"` | Point (single point at 0,0) |
| `"maskDistribution"` | Mask |
| `"intersectionsDistribution"` | Intersections |
| `"roseDistribution"` | Rose |
| `"shapeEdgesDistribution"` | Shape Edges |
| `"shapePointsDistribution"` | Shape Points |
| `"sortDistribution"` | Sort |
| `"shuffleDistribution"` | Shuffle |
| `"subMeshDistribution"` | Sub-Mesh |
| `"transformDistribution"` | Transform |
| `"voxelizeDistribution"` | Voxelize |
| `"particleDistribution"` | Particle |

### Generator Strings for Basic Shape
Use `api.setGenerator(layerId, "generator", type)`:

| Generator String | Shape Type |
|-----------------|------------|
| `"ellipse"` | Ellipse |
| `"rectangle"` | Rectangle |
| `"polygon"` | Polygon |
| `"star"` | Star |
| `"arc"` | Arc |
| `"ring"` | Ring |
| `"arrow"` | Arrow |
| `"capsule"` | Capsule |
| `"cogwheel"` | Cogwheel |
| `"superEllipse"` | Super Ellipse |
| `"superShape"` | Super Shape |

---

## 9. Common Gotchas

### Colors Are RGBA Objects, NOT Hex Strings
```javascript
// WRONG — silently fails or sets to black:
api.set(shapeId, {"material.materialColor": "#ff0000"});

// CORRECT:
api.set(shapeId, {"material.materialColor": {r: 255, g: 0, b: 0, a: 255}});
```
**Exception**: `api.setGradientFromColors()` DOES accept hex strings. It is the ONLY API that does.
**Exception**: Color Array values can be set with hex: `api.set(colorArrayId, {"array.0": "#ff0000"})`.

### Compound Attributes MUST Use Arrays
```javascript
// WRONG — sets to 0 or fails:
api.set(ellipseId, {"generator.radius": 100});

// CORRECT:
api.set(ellipseId, {"generator.radius": [100, 100]});
```

### api.get() Fails on Compound Types
```javascript
// WRONG — throws error:
var dims = api.get(rectId, "generator.dimensions");

// CORRECT — get children:
var w = api.get(rectId, "generator.dimensions.x");
var h = api.get(rectId, "generator.dimensions.y");
```

### api.set() With Font Compound
```javascript
// Font is a special compound — use nested object:
api.set(textId, {"font": {"font": "Arial", "style": "Bold"}});

// OR set children individually:
api.set(textId, {"font.font": "Arial", "font.style": "Bold"});
```

### Functions That DO NOT EXIST
| Wrong | Correct |
|-------|---------|
| `api.debug()` | `console.log()` |
| `api.setParent()` | `api.parent(childId, parentId)` |
| `api.setNiceName()` | `api.rename(layerId, name)` |
| `api.setCurrentFrame()` | `api.setFrame(frame)` |
| `api.createShape()` | `api.primitive(type, name)` or `api.create(type, name)` |
| `api.getAllSceneLayers()` | `api.getCompLayers(false)` |

### api.setGenerator Requires 3 Arguments
```javascript
// WRONG:
api.setGenerator(dupId, "circleDistribution");

// CORRECT:
api.setGenerator(dupId, "generator", "circleDistribution");
```

### api.primitive vs api.create for Shapes
- `api.primitive("rectangle")` creates a basicShape with rectangle generator preset
- `api.create("basicShape")` creates a basicShape with default (polygon) generator
- These produce DIFFERENT generator attribute paths depending on the preset
- For text, duplicators, groups, etc., you MUST use `api.create()`

### Enable/Disable Fill and Stroke Programmatically
Use the convenience functions — do NOT try to set fill/stroke via attribute paths:
```javascript
api.setFill(shapeId, true);   // enable fill
api.setFill(shapeId, false);  // disable fill
api.setStroke(shapeId, true); // enable stroke
api.setStroke(shapeId, false);// disable stroke
```

### Duplicator Ignores Input Shape Transforms
The Duplicator intentionally ignores position/rotation/scale of direct Input Shapes. Use a Group wrapper to pass transforms through (see Scene Organization section).

### Oscillator Updated in v2.4
The Oscillator was redesigned in Cavalry 2.4. Key differences:
- `frequency` now depends on `timeMode` (Seconds or BPM)
- Use `numberOfWaves` (Deformer tab) to control deformation wave count
- `timeScale` values from old scenes may need reducing

### Stallion Returns "Success" Not Data
Scripts executed via Stallion always return "Success". To extract data from the scene:
```javascript
var result = api.get(layerId, "someAttr");
api.writeToFile("D:/debug.json", JSON.stringify(result), true);
```

### Always Check Layer Existence
```javascript
if (!api.layerExists(myLayerId)) {
    // layer was deleted or doesn't exist
}
```

### Array Attributes — Adding Items
```javascript
// Add to array:
var index = api.addArrayIndex(layerId, "array");
api.set(layerId, {"array." + index: value});

// Remove from array:
api.removeArrayIndex(layerId, "array.1");

// Get count:
var count = api.getArrayCount(layerId, "array");
```

### Dynamic Attributes on JavaScript Utilities
```javascript
var jsId = api.create("javaScript", "JS Layer");
api.addDynamic(jsId, "array", "double");   // types: double, bool, string, int2, double2, color
api.set(jsId, {"array.1": 10});            // access by INDEX, not by name
```

### Pre-Comps Are Created From Assets Window
You cannot `api.create("composition")`. Compositions are created via:
- Assets Window button
- `api.preCompose()` (with selection)
- Dragging compositions between each other

### Gradient Tiling Modes
0=Clamp, 1=Repeat, 2=Mirror, 3=Decal

### Gradient Interpolation Modes
0=Linear, 1=Step, 2=Smooth, 3=Crush, 4=SmoothBlend, 5=Contrast

### Graph Presets (for Stagger, Oscillator, etc.)
```javascript
api.graphPreset(layerId, "graph", presetIndex);
// 0=S-Curve, 1=Ramp, 2=Linear, 3=Flat

api.flipGraph(layerId, "graph", "vertical");   // flip graph
api.flipGraph(layerId, "graph", "horizontal"); // flip graph
```

### Context — How Duplicators Provide Indices
- Duplicators assign an index (0, 1, 2...) to each duplicate
- Connected behaviours (Random, Noise, Stagger) automatically receive this index
- Random uses the index to vary its Seed per duplicate
- Noise uses the index to vary its output per duplicate
- Stagger maps the index linearly between min and max
- Uncheck "Use Index Context" on a nested Duplicator to prevent index accumulation

### Clip Timing
```javascript
api.setInFrame(layerId, 0);     // set first frame of clip
api.setOutFrame(layerId, 100);  // set last frame of clip
api.offsetLayerTime(layerId, 50); // offset clip and animation
```

### Control Centre
```javascript
api.addToControlCentre(layerId, "position.x"); // expose attr in Control Centre
api.removeFromControlCentre(layerId, "position.x");
```

---

## 10. cavalry Module — Utility Functions

Available in JavaScript Editor AND JavaScript Utility/Shape expressions.

### Path Class
```javascript
var path = new cavalry.Path();
path.moveTo(0, 0);
path.lineTo(100, 0);
path.cubicTo(cp1X, cp1Y, cp2X, cp2Y, endX, endY);
path.quadTo(cp1X, cp1Y, endX, endY);
path.arcTo(cp1X, cp1Y, cp2X, cp2Y, radius);
path.close();
path.addRect(fromX, fromY, toX, toY);
path.addEllipse(centreX, centreY, radiusX, radiusY);
path.addText("hello", fontSize, posX, posY);
path.translate(x, y);
path.rotate(degrees);
path.scale(x, y);
path.append(otherPath);
path.intersect(otherPath);
path.unite(otherPath);
path.difference(otherPath);
path.trim(start, end, travel, reverse);
path.offset(distance, round);
path.resample(edgeLength);
path.length();
path.pointAtParam(0.5);
path.tangentAtParam(0.5);
path.normalAtParam(0.5);
path.angleAtParam(0.5);
path.paramAtLength(length);
path.boundingBox();
path.contains(x, y);
path.pathData();          // get array of verbs for modification
path.setPathData(data);   // set back after modification
api.createEditable(path, "My Path");  // create editable shape from path
```

### Mesh Class (for JavaScript Shape)
```javascript
var mesh = new cavalry.Mesh();
var material = new cavalry.Material();
material.fillColor = "#ff24e0";
material.stroke = true;
material.strokeColor = "#000000";
material.strokeWidth = 10;
material.trim = true;
material.trimStart = 0.0;
material.trimEnd = 0.5;
material.trimTravel = 0.0;
mesh.addPath(path, material);
return mesh; // from JavaScript Shape expression
```

### Math Functions
```javascript
cavalry.random(min, max, seed, sequence);
cavalry.uniform(min, max, seed);
cavalry.noise1d(x, seed, frequency);
cavalry.noise2d(x, y, seed, frequency);
cavalry.noise3d(x, y, z, seed, frequency);
cavalry.dist(x1, y1, x2, y2);
cavalry.map(value, inMin, inMax, outMin, outMax);
cavalry.norm(value, min, max);
cavalry.clamp(value, min, max);
cavalry.lerp(min, max, t);
cavalry.angleFromVector(x, y);     // returns radians
cavalry.vectorFromAngle(radians);  // returns {x, y}
cavalry.radiansToDegrees(rad);
cavalry.degreesToRadians(deg);
```

### Color Functions
```javascript
cavalry.rgbToHsv(r, g, b, normalised);      // normalised=true means 0..1 input
cavalry.rgbToHex(r, g, b, normalised);
cavalry.rgbaToHex(r, g, b, a, normalised);
cavalry.hsvToRgba(h, s, v, normalised);      // H: 0..360, S: 0..1, V: 0..1
cavalry.hsvToHex(h, s, v);
cavalry.hexToRgba(hex, normalised);
cavalry.hexToHsv(hex);
cavalry.nameThatColor(hex);                   // returns closest W3C color name
```

### Text Functions
```javascript
cavalry.fontExists("Lato", "Regular");        // check if font available
cavalry.getFontFamilies();                     // list all font families
cavalry.getFontStyles("Lato");                 // list styles for family
cavalry.measureText("text", "Lato", "Regular", 72); // returns bounding box
cavalry.fontMetrics("Lato", "Regular", 72);    // returns font metrics
```

---

## 11. Filter Connection Pattern

Filters are image-based effects connected to shapes:
```javascript
var blur = api.create("gaussianBlurFilter", "Blur");
api.set(blur, {"radius": 10});
api.connect(blur, "id", shapeId, "filters");
api.parent(blur, shapeId);
```

Filter common attributes:
- `blendMode` — how filter blends with others in the stack
- `opacity` — reduce/increase filter effect
- `mattes` — connect shapes as mattes for selective filtering

---

## 12. Behaviour Common Attributes

All behaviours share:
- `strength` — multiplier (0-100)
- `graph` — Graph widget to shape the effect curve
- `falloffs` — array to connect Falloff utilities

Graph presets: 0=S-Curve, 1=Ramp, 2=Linear, 3=Flat

Falloff Layer Modes:
- 0 = Normal (Add)
- 1 = Min
- 2 = Max
- 3 = Minus
- 4 = Multiply
- 5 = Screen
- 6 = Overlay

---

## 13. Modulate Pattern (Repeating Sequences)

```javascript
var mod = api.create("modulate", "Pattern");
// modulateMode: 0=Remainder, 1=Pass/Fail, 2=CustomPattern  ← NOT "mode"
// "value" acts as the divisor  ← NOT "divisor"
api.set(mod, {"modulateMode": 0, "value": 3}); // outputs 0,1,2,0,1,2...
api.connect(mod, "id", duplicatorId, "shapeId");
```

For alternating patterns (e.g., every 3rd):
```javascript
api.set(mod, {"modulateMode": 1, "value": 3, "passValue": 0, "failValue": 1});
```

---

## 14. Composition Management via Script

```javascript
// Get active composition
var compId = api.getActiveComp();

// Get all layers in active comp
var allLayers = api.getCompLayers(false);     // all layers
var topLayers = api.getCompLayers(true);      // top-level only

// Get layers of specific type
var nulls = api.getCompLayersOfType(false, "null");

// Pre-compose selected layers
api.select([shape1, shape2]);
var preCompId = api.preCompose();

// Set frame
api.setFrame(50);
var frame = api.getFrame();
```

---

## 15. Render Queue (from API module)

```javascript
// Get render queue items
var items = api.getRenderQueueItems();

// Delete all render items
for (var item of items) {
    api.deleteLayer(item);
}
```

---

## 16. User Data (Metadata on Layers)

> **WARNING:** `api.getUserData()` does NOT exist (batch-tested: TypeError). Only `api.setUserData` and `api.clearUserData` work.

```javascript
api.setUserData(layerId, "myKey", "myValue");
// api.getUserData() — does NOT exist, will throw TypeError
api.clearUserData(layerId);
```

---

## 17. Web APIs & External Data

```javascript
var client = new api.WebClient("https://api.example.com");
client.get("/endpoint");
if (client.status() == 200) {
    var data = JSON.parse(client.body());
}

// Shell commands
api.runProcess("/bin/echo", ["hello"]);
```

---

## 18. File I/O

```javascript
// Write file
api.writeToFile("D:/output/data.json", JSON.stringify(data), true); // overwrite=true

// Read file
var content = api.readFromFile("D:/input/data.json");

// Load external script
api.load("D:/scripts/myHelpers.js");
```

---

## 19. Quick Reference — Most Common Mistakes

| Mistake | Fix |
|---------|-----|
| Setting color as hex string | Use RGBA object: `{r:255, g:0, b:0, a:255}` |
| Single number for radius/dimensions | Use array: `[100, 100]` |
| `api.get()` on compound attr | Get children: `"position.x"` not `"position"` |
| `api.get()` on `rotation` | Returns object — read as `rotation.z` |
| `api.setGenerator(id, type)` | Need 3 args: `api.setGenerator(id, "generator", type)` |
| `api.setParent()` | Use `api.parent(child, parent)` |
| `api.debug()` | Use `console.log()` |
| `api.duplicate(id)` | Requires 2 args: `api.duplicate(id, false)` |
| `api.getUserData()` | Does NOT exist — throws TypeError |
| `api.getAllSceneLayers()` | Use `api.getCompLayers(false)` |
| Oscillator `waveStyle` | Does not exist — use `waveType` |
| Oscillator `type` | Does not exist — use `trigType` |
| Oscillator `strengthFadeToZero` | Does not exist — use `strengthToZero` |
| Noise `minimum/maximum/frequency/seed` | ALL noise attrs need `generator.*` prefix |
| `api.create("bendDeformer")` | Wrong — correct is `"bend"` |
| `api.create("pathOffset")` | Wrong — correct is `"pathOffsetBehaviour"` |
| `api.create("travelDeformer")` | Wrong — correct is `"travel"` |
| `api.create("fastBlurFilter")` | Wrong — correct is `"blurFilter"` |
| `api.create("brightnessAndContrastFilter")` | Wrong — correct is `"brightnessAndContrast"` |
| `api.create("levelsFilter")` | Wrong — correct is `"levels"` |
| `api.create("invertFilter")` | Wrong — correct is `"invert"` |
| `api.create("blackAndWhiteFilter")` | Wrong — correct is `"blackAndWhite"` |
| `api.create("edgeDetectionFilter")` | Wrong — correct is `"edgeDetection"` |
| `api.create("linearWipeFilter")` | Wrong — correct is `"linearWipe"` |
| GradientShader `generator.mode` | Wrong — use top-level `gradientMode` |
| GradientShader `generator.screenSpace/tiling/reverse` | Wrong — these are top-level attrs |
| GlowFilter `radius` | Wrong — use `blur` as double2 array |
| DropShadowFilter `color` | Wrong — use `shadowColor` |
| ColorArray `index` | Wrong — use `arrayIndex` |
| SubMesh `position/rotation/scale/opacity` | Wrong — use `shapePosition/shapeRotation/shapeScale/shapeOpacity` |
| Math `result` | Wrong — output attr is `out` |
| Modulate `mode` / `divisor` | Wrong — use `modulateMode` / `value` |
| NumberRange `minimum/maximum` | Wrong — use `min/max`, `sourceMin/sourceMax` |
| Leaving shaders/effects at root | Always `api.parent()` under affected shape |
| Not setting stagger on oscillator | Always include stagger for duplicator use |
| Hex colors in `api.set()` for fill | ONLY `api.setGradientFromColors()` accepts hex |
| Creating gradient as inline material | Gradients are separate shader layers |
| Trying to create a composition | Compositions can't be created via `api.create()` |
| Forgetting `hidden: true` on duplicator input | Input shapes should usually be hidden |
| Not calling `api.stop()` first | Always first line in scene-modifying scripts |
