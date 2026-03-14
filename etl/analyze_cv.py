#!/usr/bin/env python
"""analyze_cv.py — Mine 270 Scenery .cv files for real-world Cavalry patterns.

Generates a markdown section for cavalry-best-practices.md with:
- Node type frequency across all scenes
- Most common connection patterns
- Per-behaviour connection targets (oscillator, noise, gradientShader, etc.)
- Common co-occurrences

Usage:
    python etl/analyze_cv.py                     # print to stdout
    python etl/analyze_cv.py --append            # append section to prompts/cavalry-best-practices.md
    python etl/analyze_cv.py --out path/to.md    # write to specific file
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import click

CV_DIR = Path(__file__).resolve().parent.parent / "data" / "scenery_cv"
BEST_PRACTICES = Path(__file__).resolve().parent.parent / "prompts" / "cavalry-best-practices.md"

# Node types to exclude from signal analysis (plumbing / infrastructure)
NOISE_TYPES = {
    "keyframe", "hiddenFolder", "visibilityCurve", "animationCurve",
    "compNode", "asset", "renderQueue", "paletteContainer",
    "dynamicIndexManager", "timeMarker", "timeMarkerFolder",
    "keyframeLayer",
}

# Behaviour nodes to profile individually
BEHAVIOUR_NODES = {
    "oscillator", "noise", "simplexNoise", "random", "stagger",
    "value", "value2", "value3", "numberRange", "mathDistribution",
    "behaviourMixer", "falloff", "attractorField",
}

# Shader / material nodes
SHADER_NODES = {
    "gradientShader", "linearGradientShader", "colorArray", "indexToColor",
    "colorBlend", "colorMaterial", "strokeMaterial",
}


def _node_type(ref: str) -> str:
    return ref.split("#")[0] if "#" in ref else ref


def _attr_path(ref: str) -> str:
    parts = ref.split(".", 1)
    t = _node_type(parts[0])
    return f"{t}.{parts[1]}" if len(parts) > 1 else t


def analyze():
    files = list(CV_DIR.glob("*.cv"))
    if not files:
        print(f"No .cv files found in {CV_DIR}", file=sys.stderr)
        sys.exit(1)

    all_node_types: Counter = Counter()
    all_conn_patterns: Counter = Counter()
    by_from_type: dict[str, Counter] = defaultdict(Counter)
    by_to_type: dict[str, Counter] = defaultdict(Counter)
    scenes_with: dict[str, int] = defaultdict(int)  # type → scene count

    scene_node_sets: list[set] = []

    for fpath in files:
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception:
            continue

        scene_types = set()
        for n in data.get("nodes", []):
            nid = n.get("nodeId", "")
            if "#" in nid:
                t = nid.split("#")[0]
                all_node_types[t] += 1
                scene_types.add(t)

        for t in scene_types:
            scenes_with[t] += 1

        scene_node_sets.append(scene_types)

        for c in data.get("connections", []):
            f, t = c.get("from", ""), c.get("to", "")
            if not f or not t:
                continue
            fp = _attr_path(f)
            tp = _attr_path(t)
            pat = f"{fp} -> {tp}"
            ft = _node_type(f.split(".")[0] if "." in f else f)
            tt = _node_type(t.split(".")[0] if "." in t else t)
            all_conn_patterns[pat] += 1
            if ft not in NOISE_TYPES:
                by_from_type[ft][pat] += 1
            if tt not in NOISE_TYPES:
                by_to_type[tt][pat] += 1

    return {
        "total_scenes": len(files),
        "node_types": all_node_types,
        "conn_patterns": all_conn_patterns,
        "by_from_type": by_from_type,
        "by_to_type": by_to_type,
        "scenes_with": scenes_with,
    }


def generate_markdown(data: dict) -> str:
    total = data["total_scenes"]
    node_types = data["node_types"]
    conn_patterns = data["conn_patterns"]
    by_from_type = data["by_from_type"]
    scenes_with = data["scenes_with"]

    lines = []
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Real-World Patterns from Scenery (270 .cv scenes)")
    lines.append("")
    lines.append(f"Mined from {total} Cavalry scenes published on Scenery.")
    lines.append("Counts show how many scene instances contain each node/pattern.")
    lines.append("Use these as ground-truth for what actually works in production Cavalry scenes.")
    lines.append("")

    # --- Node types ---
    lines.append("### Most-Used Node Types (signal nodes only)")
    lines.append("")
    lines.append("| Node Type | Instances | Scenes |")
    lines.append("|-----------|-----------|--------|")
    signal_types = {k: v for k, v in node_types.items() if k not in NOISE_TYPES}
    for t, count in sorted(signal_types.items(), key=lambda x: -x[1])[:40]:
        sc = scenes_with.get(t, 0)
        lines.append(f"| `{t}` | {count} | {sc}/{total} |")
    lines.append("")

    # --- Top connection patterns ---
    lines.append("### Top Connection Patterns (all scenes)")
    lines.append("")
    lines.append("Format: `source.attribute -> target.attribute [count]`")
    lines.append("")
    signal_conns = {
        p: n for p, n in conn_patterns.items()
        if not all(
            _node_type(side.split(".")[0]) in NOISE_TYPES
            for side in p.split(" -> ")
        )
    }
    for pat, count in sorted(signal_conns.items(), key=lambda x: -x[1])[:50]:
        lines.append(f"- `{pat}` [{count}]")
    lines.append("")

    # --- Per-behaviour profiles ---
    lines.append("### Behaviour Node Connection Profiles")
    lines.append("")
    lines.append("What each behaviour node connects TO in real scenes:")
    lines.append("")

    for btype in sorted(BEHAVIOUR_NODES):
        if btype not in by_from_type:
            continue
        top = by_from_type[btype].most_common(20)
        if not top:
            continue
        sc = scenes_with.get(btype, 0)
        lines.append(f"#### `{btype}` (in {sc} scenes)")
        lines.append("")
        for pat, count in top:
            lines.append(f"- `{pat}` [{count}]")
        lines.append("")

    # --- Shader profiles ---
    lines.append("### Shader / Material Connection Profiles")
    lines.append("")

    for stype in sorted(SHADER_NODES):
        if stype not in by_from_type:
            continue
        top = by_from_type[stype].most_common(20)
        if not top:
            continue
        sc = scenes_with.get(stype, 0)
        lines.append(f"#### `{stype}` (in {sc} scenes)")
        lines.append("")
        for pat, count in top:
            lines.append(f"- `{pat}` [{count}]")
        lines.append("")

    # --- Common duplicator patterns ---
    lines.append("### Duplicator Input Patterns")
    lines.append("")
    lines.append("What feeds into duplicator attributes:")
    lines.append("")
    dup_inputs = data["by_to_type"].get("duplicator", Counter())
    for pat, count in dup_inputs.most_common(30):
        lines.append(f"- `{pat}` [{count}]")
    lines.append("")

    return "\n".join(lines)


@click.command()
@click.option("--append", "mode", flag_value="append", help="Append to cavalry-best-practices.md")
@click.option("--out", "out_path", default=None, help="Write markdown to this file path")
@click.option("--print", "mode", flag_value="print", default=True, help="Print to stdout (default)")
def main(mode: str, out_path: str | None):
    """Analyze .cv files and generate a real-world patterns section for best-practices."""
    click.echo("Analyzing .cv files...", err=True)
    data = analyze()
    click.echo(f"Processed {data['total_scenes']} scenes, "
               f"{sum(data['node_types'].values())} node instances, "
               f"{sum(data['conn_patterns'].values())} connections.", err=True)

    md = generate_markdown(data)

    if out_path:
        Path(out_path).write_text(md, encoding="utf-8")
        click.echo(f"Written to {out_path}", err=True)
    elif mode == "append":
        with open(BEST_PRACTICES, "a", encoding="utf-8") as f:
            f.write(md)
        click.echo(f"Appended to {BEST_PRACTICES}", err=True)
    else:
        print(md)


if __name__ == "__main__":
    main()
