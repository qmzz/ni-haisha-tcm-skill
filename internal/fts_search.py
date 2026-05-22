#!/usr/bin/env python3
"""SQLite FTS / LIKE 原始资料检索。"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "source_fts.sqlite"


def _quote(text: str, keyword: str, context: int) -> str:
    idx = text.find(keyword)
    if idx < 0:
        return text[: context * 2].replace("\n", " ").strip()
    left = max(0, idx - context)
    right = min(len(text), idx + len(keyword) + context)
    return text[left:right].replace("\n", " ").strip()


class FtsSearch:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = Path(db_path or DB_PATH)

    def available(self) -> bool:
        return self.db_path.exists()

    def search(self, query: str, limit: int = 10, context: int = 100) -> List[Dict]:
        query = query.strip()
        if not query or not self.available():
            return []
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            rows = self._match(conn, query, limit)
            mode = "fts"
            if not rows:
                rows = self._like(conn, query, limit)
                mode = "like"
            return [
                {
                    "source_file": row["source_file"],
                    "page_num": row["page_num"],
                    "quote": _quote(row["text"], query, context),
                    "search_mode": mode,
                }
                for row in rows
            ]
        finally:
            conn.close()

    def _match(self, conn: sqlite3.Connection, query: str, limit: int):
        try:
            return conn.execute(
                "SELECT source_file, page_num, text FROM source_pages_fts WHERE source_pages_fts MATCH ? LIMIT ?",
                (query, limit),
            ).fetchall()
        except sqlite3.OperationalError:
            return []

    def _like(self, conn: sqlite3.Connection, query: str, limit: int):
        return conn.execute(
            "SELECT source_file, page_num, text FROM source_pages WHERE text LIKE ? LIMIT ?",
            (f"%{query}%", limit),
        ).fetchall()
