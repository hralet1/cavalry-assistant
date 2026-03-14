# store.py
from dataclasses import dataclass
from typing import Any
import lancedb
import pyarrow as pa

SCHEMA = pa.schema([
    pa.field("id", pa.string()),
    pa.field("schema_version", pa.int32()),
    pa.field("content", pa.string()),
    pa.field("embedding", pa.list_(pa.float32(), 768)),
    pa.field("source", pa.string()),
    pa.field("channel", pa.string()),
    pa.field("author", pa.string()),
    pa.field("timestamp", pa.string()),
    pa.field("tags", pa.list_(pa.string())),
    pa.field("metadata", pa.string()),
])

TABLE_NAME = "cavalry_knowledge"


@dataclass
class StoreConfig:
    lancedb_path: str = "./data/lancedb"
    backend: str = "local"


class KnowledgeStore:
    def __init__(self, cfg: StoreConfig):
        self._cfg = cfg
        self._db = lancedb.connect(cfg.lancedb_path)
        self._table = self._get_or_create_table()

    def _get_or_create_table(self):
        try:
            return self._db.open_table(TABLE_NAME)
        except Exception:
            return self._db.create_table(TABLE_NAME, schema=SCHEMA)

    def upsert(self, chunks: list[dict[str, Any]]) -> None:
        if not chunks:
            return
        existing_ids = set()
        try:
            rows = self._table.to_pandas()[["id"]]
            existing_ids = set(rows["id"].tolist())
        except Exception:
            pass
        new_chunks = [c for c in chunks if c["id"] not in existing_ids]
        if new_chunks:
            self._table.add(new_chunks)

    def search(self, query_embedding: list[float], top_k: int = 10) -> list[dict[str, Any]]:
        results = (
            self._table.search(query_embedding)
            .limit(top_k)
            .to_list()
        )
        return results

    def count(self) -> int:
        return self._table.count_rows()

    def reset(self) -> None:
        self._db.drop_table(TABLE_NAME)
        self._table = self._get_or_create_table()
