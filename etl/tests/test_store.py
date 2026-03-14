# tests/test_store.py
import pytest
import tempfile
from store import KnowledgeStore, StoreConfig

SAMPLE_CHUNK = {
    "id": "abc123",
    "schema_version": 1,
    "content": "Use api.primitive('rectangle') for rectangles",
    "source": "manual",
    "channel": "workflow",
    "author": "system",
    "timestamp": "2024-01-01T00:00:00+00:00",
    "tags": ["api", "shapes"],
    "metadata": "{}",
    "embedding": [0.1] * 768,
}


@pytest.fixture
def tmp_store():
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = StoreConfig(lancedb_path=tmpdir)
        store = KnowledgeStore(cfg)
        yield store


def test_upsert_and_count(tmp_store):
    tmp_store.upsert([SAMPLE_CHUNK])
    assert tmp_store.count() == 1


def test_upsert_deduplicates(tmp_store):
    tmp_store.upsert([SAMPLE_CHUNK])
    tmp_store.upsert([SAMPLE_CHUNK])
    assert tmp_store.count() == 1


def test_upsert_different_ids(tmp_store):
    chunk2 = {**SAMPLE_CHUNK, "id": "def456", "content": "Different content"}
    tmp_store.upsert([SAMPLE_CHUNK, chunk2])
    assert tmp_store.count() == 2


def test_search_returns_results(tmp_store):
    tmp_store.upsert([SAMPLE_CHUNK])
    query_vec = [0.1] * 768
    results = tmp_store.search(query_vec, top_k=5)
    assert len(results) >= 1
    assert "content" in results[0]


def test_reset_clears_table(tmp_store):
    tmp_store.upsert([SAMPLE_CHUNK])
    tmp_store.reset()
    assert tmp_store.count() == 0
