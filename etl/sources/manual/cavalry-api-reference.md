# Cavalry API Complete Reference (from official docs)

## API Namespaces
- `api.*` — JavaScript Editor only (Pro). Scene manipulation, layers, rendering, files
- `cavalry.*` — JS Editor + JS Layers. Path, Line, Mesh, Matrix, math, color, text
- `ctx.*` — JS Layers only. Index, count, position, layerId, transformationMatrix
- `def.*` — JS Deformer only. Mesh access, falloff, points, depth-based operations
- `ui.*` — Script UIs. Widgets, layouts, callbacks, file dialogs

## Composition
| Function | Returns |
|----------|---------|
| `api.setFrame(frame:int)` | void |
| `api.getFrame()` | int |
| `api.play()` / `api.stop()` | void |
| `api.getCompLayers(isTopLevel:bool)` | [string] |
| `api.getCompLayersOfType(isTopLevel:bool, type:string)` | [string] |
| `api.getParentComp(layerId)` | string |
| `api.getActiveComp()` | string |
| `api.getComps()` | [string] |
| `api.createComp(name)` | string |
| `api.setActiveComp(compId)` | void |
| `api.preCompose(name)` | string |
| `api.createCompReference(compId)` | string |
| `api.getCompFromReference(layerId)` | string |
| `api.createTimeMarker(time:int)` | string |
| `api.getTimeMarkers()` | [string] |
| `api.removeTimeMarker(markerId)` | void |
| `api.getNthBeat(beat:int)` | int |
| `api.addGuide(compId, isVertical:bool, position:int)` | int |
| `api.deleteGuide(compId, id:int)` | void |
| `api.clearGuides(compId)` | void |
| `api.getGuideInfo(compId)` | [{id, direction, position}] |
| `api.timecodeToFrames(timecode, fps)` | int |
| `api.framesToTimecode(frame, fps)` | string |

## Layers — Creation & Deletion
| Function | Returns |
|----------|---------|
| `api.primitive(type, name)` | string (layerId) |
| `api.create(layerType, name, allowDefaultPreset=false)` | string |
| `api.createEditable(path:Path, name)` | string |
| `api.deleteLayer(layerId)` | void |
| `api.duplicate(layerId, withInputConnections:bool)` | void |
| `api.layerExists(layerId)` | bool |

### Valid Primitives
rectangle, ellipse, star, polygon, arrow, arc, ring, superEllipse, squircle

## Layers — Properties
| Function | Returns |
|----------|---------|
| `api.getLayerType(layerId)` | string |
| `api.isShape(layerId)` | bool |
| `api.isTransform(layerId)` | bool |
| `api.isVisible(layerId, includeHierarchy:bool)` | bool |
| `api.isReferenced(layerId)` | bool |
| `api.getNiceName(layerId)` | string |
| `api.rename(layerId, name)` | void |
| `api.getInFrame(layerId)` / `api.setInFrame(layerId, frame)` | int / void |
| `api.getOutFrame(layerId)` / `api.setOutFrame(layerId, frame)` | int / void |
| `api.offsetLayerTime(layerId, delta:int)` | void |
| `api.getBoundingBox(layerId, worldSpace:bool)` | {x,y,width,height,centre,left,right,top,bottom} |
| `api.getSelectionBoundingBox()` | same |
| `api.setStroke(layerId, isOn)` / `api.hasStroke(layerId)` | void / bool |
| `api.setFill(layerId, isOn)` / `api.hasFill(layerId)` | void / bool |
| `api.resetLayerAttributes(layerId)` | void |
| `api.showInAttributeEditor(layerId)` | void |

## Layers — Hierarchy
| Function | Returns |
|----------|---------|
| `api.parent(childId, parentId)` | void |
| `api.unParent(layerId)` | void |
| `api.getParent(layerId)` | string |
| `api.getChildren(layerId)` | [string] |
| `api.reorder(layerIdToReorder, underLayerId)` | void |
| `api.sortLayerIdsByHierarchy(layerIds)` | [string] |
| `api.bringForward()` / `api.bringToFront()` | void |
| `api.moveBackward()` / `api.moveToBack()` | void |

## Layers — Selection
| Function | Returns |
|----------|---------|
| `api.getSelection(sortByHierarchyOrder=false)` | [string] |
| `api.select(layers:[string])` | void |
| `api.invertSelection()` | void |
| `api.soloLayers(layerIds)` | void |
| `api.getAllSceneLayers()` | [string] |

## Attributes — Get/Set
| Function | Returns |
|----------|---------|
| `api.set(layerId, {attrPath: value, ...})` | void |
| `api.get(layerId, attrId)` | value |
| `api.getAttrType(layerId, attrId)` | string |
| `api.getAttributes(layerId)` | [string] |
| `api.hasAttribute(layerId, attrId)` | bool |
| `api.getAttrChildren(layerId, attrId)` | [string] |
| `api.getAttrParent(layerId, attrId)` | string |
| `api.getAttributeNiceName(layerId, attrId)` | string |
| `api.getAttributeDefinition(layerId, attrId)` | object |
| `api.resetAttribute(layerId, attrId)` | void |
| `api.isAttrDefault(layerId, attrId)` | bool |
| `api.renameAttribute(layerId, attrId, newName)` | void |
| `api.addDynamic(layerId, attrId, type)` | void — types: int, double, bool, string, color, int2d, double2d, position2d |
| `api.getSelectedAttributes()` | [object] |

## Attributes — Arrays
| Function | Returns |
|----------|---------|
| `api.addArrayIndex(layerId, attrId)` | int |
| `api.removeArrayIndex(layerId, attrId)` | void |
| `api.reorderArrayAttr(layerId, attrId, oldIndex, newIndex)` | void |
| `api.getArrayCount(layerId, attrId)` | int |

## Attributes — Generators
| Function | Returns |
|----------|---------|
| `api.setGenerator(layerId, attrId, type)` | void — 3 ARGS always! |
| `api.getCurrentGenerator(layerId, attrId)` | string |
| `api.getGenerators(layerId)` | [string] |
| `api.getCurrentGeneratorType(layerId, attrId)` | string |

## Attributes — Connections
| Function | Returns |
|----------|---------|
| `api.connect(fromId, fromAttr, toId, toAttr, force:bool)` | void |
| `api.disconnect(fromId, fromAttr, toId, toAttr)` | void |
| `api.disconnectInput(layerId, attrId)` | void |
| `api.disconnectOutputs(layerId, attrId)` | void |
| `api.getInConnection(layerId, attrId)` | string |
| `api.getOutConnections(layerId, attrId)` | [string] |
| `api.getInConnectedAttributes(layerId)` | [string] |
| `api.getOutConnectedAttributes(layerId)` | [string] |

## Attributes — Expressions
| Function | Returns |
|----------|---------|
| `api.setAttributeExpression(layerId, attrId, expr)` | void |
| `api.hasAttributeExpression(layerId, attrId)` | bool |
| `api.getAttributeExpression(layerId, attrId)` | string |

## Keyframes & Animation
| Function | Returns |
|----------|---------|
| `api.keyframe(layerId, frame, {attr: value})` | string |
| `api.deleteKeyframe(layerId, attrId, frame)` | void |
| `api.deleteAnimation(layerId, attrId)` | void |
| `api.modifyKeyframe(layerId, data)` | void |
| `api.modifyKeyframeTangent(layerId, data)` | void |
| `api.setKeyframeVelocity(layerId, dict)` | void |
| `api.clearKeyframeVelocity(layerId, dict)` | void |
| `api.getKeyframeIdsForAttribute(layerId, attrId)` | void |
| `api.getKeyframeTimes(layerId, attrId)` | void |
| `api.getSelectedKeyframes()` | object |
| `api.getSelectedKeyframeIds()` | [string] |
| `api.setSelectedKeyframeIds(ids)` | void |
| `api.getAttributeFromKeyframeId(keyframeId)` | string |
| `api.isAnimatedAttribute(layerId, attrId)` | bool |
| `api.getAnimatedAttributes(layerId)` | [string] |
| `api.graphPreset(layerId, attrId, presetIndex)` | void |
| `api.flipGraph(layerId, attrId, direction)` | void |

### Magic Easing
`api.magicEasing(layerId, attrId, frame, easingName, expression)`

Valid easing names: SlowIn, SlowOut, SlowInSlowOut, VerySlowIn, VerySlowOut, VerySlowInVerySlowOut, SpringIn, SpringOut, SpringInSpringOut, SmallSpringIn, SmallSpringOut, SmallSpringInSmallSpringOut, AnticipateIn, OvershootOut, AnticipateInOvershootOut, BounceIn, BounceOut, BounceInBounceOut, Custom, None

### Animation Curve Loop Modes
```javascript
// Get the animCurve layer from a keyframed attribute:
var inConn = api.getInConnection(layerId, attrId);
var animCurveId = inConn.split('.')[0];
api.set(animCurveId, {"postInfinity": 1, "preInfinity": 1});
// 0=Constant, 1=Loop, 2=Loop with Offset, 4=Oscillate, 5=Zero
```

## Rendering
| Function | Returns |
|----------|---------|
| `api.renderPNGFrame(filePath, scalePercent)` | void |
| `api.renderSVGFrame(filePath, scalePercent, skipComps)` | void |
| `api.render(renderQueueItemId)` | void |
| `api.renderAll()` | void |
| `api.backgroundRender(id)` / `api.backgroundRenderAll()` | void |
| `api.cancelRender()` | void |
| `api.getRenderQueueItems()` | [string] |
| `api.addRenderQueueItem(compId)` | string |

## Scene & Assets
| Function | Returns |
|----------|---------|
| `api.openScene(filePath, force:bool)` | void |
| `api.saveScene()` / `api.saveSceneAs(filePath)` | bool |
| `api.sceneHasUnsavedChanges()` | bool |
| `api.importScene(path)` | void |
| `api.exportSceneAs(filePath)` / `api.exportSelected(filePath)` | bool |
| `api.loadAsset(path, isSequence:bool)` | string |
| `api.loadSmartFolderAsset(path, type)` | string |
| `api.reloadAsset(assetId)` | void |
| `api.replaceAsset(assetId, newPath)` | void |
| `api.addAssetToComp(assetId)` | string |
| `api.jsonFromAsset(assetId)` | object |
| `api.textFromAsset(assetId)` | string |
| `api.loadGoogleSheet(spreadsheetId, sheetId)` | string |
| `api.isFileAsset(assetId)` / `api.isGoogleSheetAsset(assetId)` | bool |
| `api.getAssetFilePath(assetId)` | string |
| `api.getAssetType(assetId)` | string |
| `api.getAssetWindowLayers(topLevel:bool)` | [string] |
| `api.convertSVGToLayers(filename)` | [string] |

## Editable Shapes
| Function | Returns |
|----------|---------|
| `api.makeEditable(layerId, makeACopy:bool)` | string |
| `api.getEditablePath(layerId, worldSpace:bool)` | [object] |
| `api.setEditablePath(layerId, worldSpace:bool, pathObj)` | void |
| `api.centrePivot(layerId, centroid:bool)` | void |
| `api.getPivotPosition(layerId, worldSpace:bool)` | {x, y} |
| `api.freezeTransform(layerId)` | void |
| `api.resetTransform(layerId)` | void |
| `api.move(x, y)` | void — moves selection |

## Files & Paths
| Function | Returns |
|----------|---------|
| `api.writeToFile(filePath, content, overwrite:bool)` | bool |
| `api.readFromFile(filePath)` | string |
| `api.filePathExists(path)` | bool |
| `api.makeFolder(path, overwrite:bool)` | bool |
| `api.deleteFilePath(path)` | bool |
| `api.copyFilePath(from, to)` | bool |
| `api.listDirectory(path)` | [string] |
| `api.listDirectoryPaths(path, includeDirs:bool)` | [string] |
| `api.listDirectoryRecursive(path)` | [string] |
| `api.isFile(path)` / `api.isDirectory(path)` | bool |
| `api.getAbsolutePath(path)` / `api.getRelativePath(from, to)` | string |
| `api.getFileNameFromPath(path, includeExt:bool)` | string |
| `api.getExtensionFromPath(path)` | string |
| `api.getFolderFromPath(path)` | string |
| `api.getFileModifiedDate(path)` | number |
| `api.getFileSize(path)` | number |
| `api.unzip(zipPath, destPath)` | [string] |

### Special Paths
| Function | Example |
|----------|---------|
| `api.getHomeFolder()` | C:/Users/LEX |
| `api.getDesktopFolder()` | |
| `api.getDownloadsFolder()` | |
| `api.getTempFolder()` | C:/Users/LEX/AppData/Local/Temp |
| `api.getAppDataFolder()` | C:/Users/LEX/AppData/Roaming/Cavalry |
| `api.getProjectPath()` | project root |
| `api.getSceneFilePath()` | current .cv path |
| `api.getPresetsPath()` | presets folder |

## Utilities
| Function | Returns |
|----------|---------|
| `api.setClipboardText(text)` | void |
| `api.getClipboardText()` | string |
| `api.runProcess(cmd, [args])` | object |
| `api.runDetachedProcess(cmd, [args])` | void |
| `api.load(filePath)` | bool — load & run a JS file |
| `api.exec(scriptId, scriptSource)` | bool |

## WebClient (Pro)
```javascript
var client = new api.WebClient("https://base-url.com");
client.addHeader("key", "value");
client.setTokenAuthentication("bearer-token");
client.get("/path");
client.post("/path", JSON.stringify(data), "application/json");
client.status(); // 200
client.body();   // response string
client.writeBodyToBinaryFile("path"); // for images
```

## WebServer (Pro)
```javascript
var server = new api.WebServer();
server.listen("localhost", 1234);
server.setResultForGet("hello");
server.postCount(); // queued POSTs
server.getNextPost(); // {result, headers}
server.stop();
```

## Timer
```javascript
function Callbacks() { this.onTimeout = function() { /* ... */ } }
var cb = new Callbacks();
var timer = new api.Timer(cb);
timer.setRepeating(true);
timer.setInterval(5000); // ms
timer.start(); // timer.stop();
```

---

# cavalry.* Namespace (JS Editor + JS Layers)

## Path Class
```javascript
var p = new cavalry.Path();
p.moveTo(x, y); p.lineTo(x, y); p.cubicTo(cp1X,cp1Y, cp2X,cp2Y, endX,endY);
p.quadTo(cpX,cpY, endX,endY); p.close();
p.addRect(fromX,fromY, toX,toY); p.addEllipse(cx,cy, rx,ry);
p.addText(text, fontSize, posX, posY);
p.translate(x,y); p.rotate(deg); p.scale(x,y);
p.unite(path); p.intersect(path); p.difference(path);
p.length(); p.pointAtParam(t); p.tangentAtParam(t); p.normalAtParam(t);
p.angleAtParam(t); p.paramAtLength(len); p.contains(x,y);
p.offset(distance, round); p.trim(start, end, travel, reverse);
p.resample(edgeLength); p.relax(iter, radius, strength);
p.smooth(iter, strength); p.scatter(count, seed, seq, relaxIter, dist);
p.toObject(); p.fromObject(obj);
```

## Line Class
```javascript
var l = new cavalry.Line(x1,y1, x2,y2);
l.length(); l.angle(); l.start(); l.end(); l.pointAt(t); l.normalAt(t);
l.distance({x,y}); l.closestPointTo({x,y}); l.lineIntersection(otherLine);
```

## Mesh Class
```javascript
var m = new cavalry.Mesh();
m.addPath(path, material?); m.count(); m.empty(); m.clear();
m.getPathAtIndex(i); m.setPathAtIndex(i, path);
m.setMaterialAtIndex(i, material); m.getFlattenedPath();
m.addChildMesh(mesh); m.getChildMeshAtIndex(i);
```

## Material Class
```javascript
var mat = new cavalry.Material();
mat.fill = true; mat.fillColor = "#FF0000";
mat.stroke = true; mat.strokeColor = "#000000"; mat.strokeWidth = 2;
mat.trim = true; mat.trimStart = 0; mat.trimEnd = 1;
```

## Math Functions
```javascript
cavalry.random(min, max, seed, sequence?);
cavalry.uniform(min, max, seed);
cavalry.noise1d(x, seed, freq); cavalry.noise2d(x,y, seed, freq);
cavalry.map(val, inMin, inMax, outMin, outMax);
cavalry.clamp(val, min, max); cavalry.lerp(min, max, t);
cavalry.dist(x1,y1, x2,y2);
cavalry.degreesToRadians(deg); cavalry.radiansToDegrees(rad);
```

## Color Functions
```javascript
cavalry.rgbToHex(r,g,b); cavalry.hexToRgba(hex);
cavalry.rgbToHsv(r,g,b); cavalry.hsvToHex(h,s,v);
cavalry.nameThatColor(hex); // returns color name!
```

## Text Functions
```javascript
cavalry.fontExists(family, style);
cavalry.getFontFamilies(); cavalry.getFontStyles(family);
cavalry.measureText(text, family, style, size); // {width, height, x, y, centreX, centreY}
```

---

# ctx.* Namespace (JS Layers only)

| Property/Method | Returns |
|----------------|---------|
| `ctx.index` | int — current duplicator index |
| `ctx.count` | int — total count |
| `ctx.positionX` / `ctx.positionY` | number |
| `ctx.attributeId` | string |
| `ctx.layerId` | string |
| `ctx.niceName()` | string |
| `ctx.transformationMatrix()` | matrix |
| `ctx.globalTransformationMatrix()` | matrix |
| `ctx.saveObject(name, obj)` | void |
| `ctx.loadObject(name)` | object |
| `ctx.hasObject(name)` | bool |

---

# All Node Categories

## Shapes (36 types)
Background Shape, Basic Line, Basic Shape, Cel Animation Shape, Component,
Composition, Connect Shape, Convex Hull, Corner Pin, Custom Shape, Duplicator,
Editable Shape, Extract Sub-Meshes, Extrude, Footage Shape, Forge Dynamics,
Group, Image to Shapes, Isolines Shape, JavaScript Shape, Layouts, Merge,
Mesh Shape, Outline, Particle Shape, Points to Path, Quad Tree Shape, Ray,
Rectangle Pattern, SVG, Segment Path, Shortest Path, Spacer,
Sub-Mesh Bounding Box, Text Shape, Trails

## Behaviours (80 types)
3D Matrix, Add Divisions, Align, Alpha Material Override, Apply Distribution,
Apply Layout, Area Range, Auto-Animate, Auto-Crop, Behaviour Mixer,
Bend Deformer, Bevel, Blend Shape, Blend Sub-Mesh Positions, Boolean,
Chop Path, Clean Up, Color Blend, Color Material Override,
Contours to Sub-Meshes, Curves to Lines, Distance, Extend Open Paths,
Fill Rule, Flare, Flatten Shape Layers, Four Point Warp, Frame, Get Vector,
HSV Material Override, Is Within, JavaScript Deformer, Knot,
Lattice Deformer, Look At, Manipulator, Material Sampler, Mesh Solver,
Modulate, Morph, Motion Stretch, Noise, Number Range, Number Range to Color,
Oscillator, Path Average, Path Offset, Path Relax, Pathfinder, Pinch,
Position Blend, Push Along Vector, Random, Resample Path, Reverse Path,
Round, Rubber Hose Limb, Skew, Sound, Spring, Squash and Stretch,
Stagger, Stitches, Sub-Mesh, Subdivide, Swap Color Override,
Travel Deformer, Value, Value2, Value3, Value Blend, Value2 Blend,
Value3 Blend, Value Solver, Value2 Solver, Visibility Sequence,
Voxelize, Wave

## Distribution Types (21)
Array, Circle, Custom, Fibonacci, Grid, Intersections, Linear, Mask,
Math, Particle, Path, Point, Random, Rose, Shape Edges, Shape Points,
Sort, Shuffle, Sub-Mesh, Transform, Voxelize

## Filters/Effects
Blur, Glow, Drop Shadow, Halftone, Pixelate, Posterize,
Chromatic Aberration, Vignette, Threshold
