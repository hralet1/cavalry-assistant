# Cavalry Assistant — Claude Code Instructions

## Model
**Always use Sonnet** (`claude-sonnet-4-6`) for this project. If another model is active, remind the user to switch with `/model sonnet`. Haiku is not sufficient for Cavalry MCP scripting — too many silent-failure traps and design decisions.

## You are a Cavalry motion design scripting expert

When working with Cavalry, follow these rules strictly. Every error wastes the artist's time.

## Workflow: Action-First, No Brainstorming
- **NO brainstorming or planning skills.** Go straight to building.
- **Minimal questions.** Only ask what's strictly needed for art direction (colors, sizes, specific values). Don't over-ask.
- **Respect art direction literally.** "4 balls in each corner" = create 4 new balls, place them in corners. Don't repurpose existing elements or question clear instructions.
- **Complete, well-piped designs.** Every script must produce a finished scene — proper connections, parenting, stagger, animation, clean naming.

## Research Before Scripting (MANDATORY)

NEVER guess attribute paths, function names, or layer types. Look them up FIRST:

1. **Read** `prompts/cavalry-best-practices.md` — complete reference of all layer types, attribute paths, connection patterns
2. **Grep** `etl/sources/docs/` — full scraped official docs from docs.cavalry.scenegroup.co
3. **Call** `cavalry_search_knowledge` — RAG knowledge base (Discord + docs)
4. **LAST resort**: web search

## Critical API Rules

### Shapes vs Behaviours
- `api.primitive(type, name)` — shapes ONLY: "rectangle", "ellipse", "star", "polygon", "arc", "ring"
- `api.create(type, name)` — everything else: behaviours, shaders, filters, utilities, materials

### Functions That DO NOT EXIST (will crash!)
- `api.debug()` → use `console.log()`
- `api.setParent()` → use `api.parent(childId, parentId)`
- `api.setNiceName()` → use `api.rename()`
- `api.setCurrentFrame()` → use `api.setFrame()`

### Colors = RGBA Objects, NEVER Hex Strings
```javascript
{ r: 255, g: 0, b: 0, a: 255 }   // CORRECT
"#ff0000"                          // WRONG — silently fails
```
Exception: `api.setGradientFromColors()` uses hex strings.

### Compound Attributes MUST Be Arrays
```javascript
api.set(id, {"generator.radius": [100, 100]});      // CORRECT
api.set(id, {"generator.radius": 100});              // WRONG — stays at 0!
api.set(id, {"generator.dimensions": [200, 200]});   // CORRECT
```

### Stallion Returns "Success" Always
Use `api.writeToFile()` to extract data. `console.log()` goes to Cavalry console only.

### api.get() Fails on Compound Types
```javascript
var w = api.get(id, "generator.dimensions.x");  // CORRECT — get children
var dims = api.get(id, "generator.dimensions");  // WRONG — throws error
```

## Scene Organization (MANDATORY)

### Parent behaviours to their shape
```javascript
var grad = api.create("gradientShader", "Gradient");
api.connect(grad, "id", circle, "material.colorShaders");
api.parent(grad, circle);  // ALWAYS parent to affected shape
```
Never leave shaders, deformers, or effects floating at comp root.

### One behaviour → many shapes
Create 1 oscillator/noise/random, connect to multiple shapes. Do NOT create duplicates.
```javascript
var osc = api.create("oscillator", "Dance");
api.connect(osc, "id", circle1, "position.y");
api.connect(osc, "id", circle2, "position.y");
api.connect(osc, "id", circle3, "position.y");
// Stagger handles the offset between shapes
```

### Always add stagger on oscillators
```javascript
api.set(osc, {
  "minimum": -100, "maximum": 100,
  "frequency": 1.0,
  "stagger": 25,              // ALWAYS — never skip stagger
  "strength": 100,
  "strengthToZero": false      // false for loops
});
```

## Gradient Fills

Gradients are **separate shader layers**, connected to shape fill:
```javascript
var grad = api.create("gradientShader", "Gradient");
api.setGradientFromColors(grad, "generator.gradient", ["#0000FF", "#FF0000"]);
api.connect(grad, "id", circle, "material.colorShaders");
api.parent(grad, circle);
```

What DOESN'T work: `api.create("linearGradient")`, setting material generator to gradient types, colorA/colorB paths.

## Key References

- `prompts/cavalry-best-practices.md` — ALL layer types, attribute paths, connection patterns (1,468 lines)
- `prompts/system.md` — MCP system prompt with critical rules
- `etl/sources/docs/` — full scraped Cavalry official documentation
- `etl/sources/docs/tech-info_scripting_api-module.md` — complete JS API reference
- `etl/sources/docs/nodes_effects_shaders_gradient-shader.md` — gradient shader docs
- `etl/sources/docs/nodes_behaviours_oscillator.md` — oscillator docs
