# tests/test_chunkers.py
import pytest
from chunkers.markdown import chunk_markdown

def test_splits_on_h2_headings():
    text = "# Title\n\nIntro text.\n\n## Section A\n\nContent A.\n\n## Section B\n\nContent B."
    chunks = chunk_markdown(text, source="manual", channel="test")
    assert len(chunks) == 3  # intro + Section A + Section B
    assert "Content A." in chunks[1]["content"]
    assert chunks[1]["source"] == "manual"
    assert chunks[1]["channel"] == "test"

def test_chunk_has_required_fields():
    text = "## Only Section\n\nSome content here."
    chunks = chunk_markdown(text, source="docs", channel="api-ref")
    assert len(chunks) == 1
    chunk = chunks[0]
    for field in ["id", "content", "source", "channel", "author", "timestamp", "tags", "schema_version"]:
        assert field in chunk

def test_deterministic_id():
    text = "## Section\n\nContent."
    c1 = chunk_markdown(text, source="manual", channel="test")
    c2 = chunk_markdown(text, source="manual", channel="test")
    assert c1[0]["id"] == c2[0]["id"]

def test_different_content_different_id():
    c1 = chunk_markdown("## A\n\nContent A.", source="manual", channel="x")
    c2 = chunk_markdown("## B\n\nContent B.", source="manual", channel="x")
    assert c1[0]["id"] != c2[0]["id"]

def test_empty_sections_skipped():
    text = "## Empty\n\n## Has content\n\nActual text here."
    chunks = chunk_markdown(text, source="manual", channel="test")
    contents = [c["content"] for c in chunks]
    assert not any(c.strip() == "" for c in contents)


from chunkers.discord import chunk_discord_export
import json

SAMPLE_EXPORT = {
    "channel": {"name": "scripting"},
    "messages": [
        {"id": "111", "author": {"name": "alice"}, "timestamp": "2024-01-01T10:00:00+00:00", "content": "How do I create a rectangle in Cavalry?"},
        {"id": "112", "author": {"name": "bob"}, "timestamp": "2024-01-01T10:01:00+00:00", "content": "Use api.primitive('rectangle', 'MyRect') then set generator.dimensions"},
        {"id": "113", "author": {"name": "alice"}, "timestamp": "2024-01-01T10:02:00+00:00", "content": "Thanks!"},
    ]
}

def test_discord_groups_nearby_messages():
    chunks = chunk_discord_export(SAMPLE_EXPORT)
    assert len(chunks) == 1
    assert "api.primitive" in chunks[0]["content"]

def test_discord_chunk_fields():
    chunks = chunk_discord_export(SAMPLE_EXPORT)
    chunk = chunks[0]
    for field in ["id", "content", "source", "channel", "author", "timestamp", "tags", "schema_version"]:
        assert field in chunk
    assert chunk["source"] == "discord"
    assert chunk["channel"] == "scripting"

def test_discord_deterministic_id():
    c1 = chunk_discord_export(SAMPLE_EXPORT)
    c2 = chunk_discord_export(SAMPLE_EXPORT)
    assert c1[0]["id"] == c2[0]["id"]

def test_discord_splits_on_time_gap():
    export = {
        "channel": {"name": "tips"},
        "messages": [
            {"id": "1", "author": {"name": "x"}, "timestamp": "2024-01-01T10:00:00+00:00", "content": "First message"},
            {"id": "2", "author": {"name": "y"}, "timestamp": "2024-01-01T10:10:00+00:00", "content": "Different topic after gap"},
        ]
    }
    chunks = chunk_discord_export(export)
    assert len(chunks) == 2

def test_discord_skips_empty_content():
    export = {
        "channel": {"name": "test"},
        "messages": [
            {"id": "1", "author": {"name": "bot"}, "timestamp": "2024-01-01T10:00:00+00:00", "content": ""},
            {"id": "2", "author": {"name": "alice"}, "timestamp": "2024-01-01T10:00:30+00:00", "content": "Real content here"},
        ]
    }
    chunks = chunk_discord_export(export)
    assert len(chunks) == 1
    assert "Real content" in chunks[0]["content"]


from chunkers.script import chunk_script

SAMPLE_SCRIPT = """// @description Grid duplicator with random colors
var grid = api.create("gridDistribution", "Grid");
api.set(grid, {"count": [8, 8], "size": [900, 900]});
var dup = api.create("duplicator", "Dup");
api.connect(grid, "id", dup, "generator", true);
"""

SCRIPT_NO_DESC = """var rect = api.primitive("rectangle", "MyRect");
api.set(rect, {"generator.dimensions": [200, 200]});
"""

def test_script_single_chunk():
    chunks = chunk_script(SAMPLE_SCRIPT, filename="grid_colors.js")
    assert len(chunks) == 1

def test_script_description_from_annotation():
    chunks = chunk_script(SAMPLE_SCRIPT, filename="grid_colors.js")
    assert "Grid duplicator with random colors" in chunks[0]["content"]

def test_script_description_fallback_to_filename():
    chunks = chunk_script(SCRIPT_NO_DESC, filename="my_rect.js")
    assert "my_rect.js" in chunks[0]["content"]

def test_script_chunk_fields():
    chunks = chunk_script(SAMPLE_SCRIPT, filename="grid_colors.js")
    chunk = chunks[0]
    for field in ["id", "content", "source", "channel", "author", "timestamp", "tags", "schema_version"]:
        assert field in chunk
    assert chunk["source"] == "script"

def test_script_deterministic_id():
    c1 = chunk_script(SAMPLE_SCRIPT, filename="grid_colors.js")
    c2 = chunk_script(SAMPLE_SCRIPT, filename="grid_colors.js")
    assert c1[0]["id"] == c2[0]["id"]
