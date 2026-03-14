# chunkers/cv.py
"""Chunker for Cavalry .cv scene files (JSON format).

Produces two chunk types per scene:
1. Scene summary — node types + sampled connections (good for "what does X scene do")
2. Per-source-type connection groups — "oscillator connects to..." (good for pattern queries)
"""
import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any

SCHEMA_VERSION = 1

NOISE_TYPES = {
    "keyframe", "hiddenFolder", "visibilityCurve", "animationCurve",
    "compNode", "asset", "renderQueue", "paletteContainer",
    "dynamicIndexManager", "timeMarker", "timeMarkerFolder",
}


def _make_id(source: str, content: str) -> str:
    return hashlib.sha256(f"{source}:{content}".encode()).hexdigest()[:32]


def _node_type(ref: str) -> str:
    """'ringShape#13' → 'ringShape'"""
    return ref.split("#")[0] if "#" in ref else ref


def _attr_path(ref: str) -> str:
    """'animationCurve#106.out' → 'animationCurve.out'"""
    parts = ref.split(".", 1)
    t = _node_type(parts[0])
    return f"{t}.{parts[1]}" if len(parts) > 1 else t


def _from_type(conn_from: str) -> str:
    """Get the node type from the 'from' side of a connection."""
    return _node_type(conn_from.split(".")[0] if "." in conn_from else conn_from)


def chunk_cv(data: dict, filename: str) -> list[dict[str, Any]]:
    """Parse a Cavalry .cv scene file into searchable chunks."""
    now = datetime.now(timezone.utc).isoformat()
    scene_name = filename.replace(".cv", "").replace("-", " ").replace("_", " ")
    author = data.get("author", {}).get("name", "unknown")
    source_tag = "cv_scene"

    nodes = data.get("nodes", [])
    connections = data.get("connections", [])

    # Count node types (skip infrastructure noise)
    node_type_counts = Counter(
        _node_type(n.get("nodeId", ""))
        for n in nodes
        if "#" in n.get("nodeId", "")
    )
    signal_types = {k: v for k, v in node_type_counts.items() if k not in NOISE_TYPES}

    # Normalize connection patterns
    conn_patterns = [
        (_attr_path(c["from"]), _attr_path(c["to"]))
        for c in connections
        if "from" in c and "to" in c
    ]

    # Filter to signal connections (skip pure infrastructure)
    signal_conns = [
        (f, t) for f, t in conn_patterns
        if _node_type(f.split(".")[0]) not in NOISE_TYPES
        or _node_type(t.split(".")[0]) not in NOISE_TYPES
    ]

    # --- Chunk 1: Scene Summary ---
    node_list = ", ".join(
        f"{t}×{n}" if n > 1 else t
        for t, n in sorted(signal_types.items(), key=lambda x: -x[1])[:20]
    )
    conn_lines = "\n".join(
        f"  {f} -> {t}" for f, t in signal_conns[:40]
    )

    summary_content = f"""## Cavalry Scene: {scene_name}
Source: Scenery (by {author})
Node types: {node_list or "(no signal nodes)"}

Connections:
{conn_lines or "  (none)"}"""

    chunks = [{
        "id": _make_id("cv_scene", summary_content),
        "schema_version": SCHEMA_VERSION,
        "content": summary_content,
        "source": "cv_scene",
        "channel": filename,
        "author": author,
        "timestamp": now,
        "tags": [source_tag, "scene-structure"] + list(signal_types.keys())[:8],
        "metadata": "{}",
    }]

    # --- Chunk 2+: Per-source-type connection groups ---
    by_from_type: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for f, t in signal_conns:
        ft = _node_type(f.split(".")[0])
        if ft not in NOISE_TYPES:
            by_from_type[ft].append((f, t))

    for ft, pairs in by_from_type.items():
        # Deduplicate patterns within this scene
        seen = set()
        unique_pairs = []
        for pair in pairs:
            if pair not in seen:
                seen.add(pair)
                unique_pairs.append(pair)

        lines = "\n".join(f"  {f} -> {t}" for f, t in unique_pairs)
        content = f"""## Cavalry Connection Pattern: {ft} (scene: {scene_name})
Source node type: {ft}
Scene: {scene_name} (by {author})

{ft} connections in this scene:
{lines}"""

        chunks.append({
            "id": _make_id("cv_pattern", content),
            "schema_version": SCHEMA_VERSION,
            "content": content,
            "source": "cv_scene",
            "channel": filename,
            "author": author,
            "timestamp": now,
            "tags": [source_tag, "connection-pattern", ft],
            "metadata": "{}",
        })

    return chunks
