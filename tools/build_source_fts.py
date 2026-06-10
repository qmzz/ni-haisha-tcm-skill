#!/usr/bin/env python3
"""Build data/source_fts.sqlite from source JSON files.

Default source path is the sibling directory `../nihaixia`.
Override with `NIHAIXIA_SOURCE_DIR` when needed.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(os.environ.get("NIHAIXIA_SOURCE_DIR", ROOT.parent / "nihaixia"))
DB_PATH = ROOT / "data" / "source_fts.sqlite"


def clean_ocr(text: str) -> str:
    text = re.sub(r"([\u4e00-\u9fff])\1{2,}", r"\1", text)
    text = re.sub(r"[-=]{5,}", " ", text)
    text = re.sub(r"[·.…]{3,}", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def extract_pages(source_file: str, data: dict) -> list[tuple[str, int | None, str]]:
    rows: list[tuple[str, int | None, str]] = []
    pages = data.get("pages", [])
    if isinstance(pages, list) and pages:
        for page in pages:
            text = clean_ocr(page.get("text") or page.get("content") or "")
            if len(text) >= 20:
                rows.append((source_file, page.get("page_num") or page.get("page"), text))
        return rows

    full_text = clean_ocr(data.get("full_text") or "")
    chunk_size = 2000
    for idx in range(0, len(full_text), chunk_size):
        chunk = full_text[idx : idx + chunk_size]
        if len(chunk) >= 20:
            rows.append((source_file, idx // chunk_size + 1, chunk))
    return rows


def main() -> int:
    if not SOURCE_DIR.exists():
        raise SystemExit(f"source dir not found: {SOURCE_DIR}")

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            CREATE TABLE source_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file TEXT NOT NULL,
                page_num INTEGER,
                text TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE VIRTUAL TABLE source_pages_fts USING fts5(
                source_file,
                page_num UNINDEXED,
                text,
                content='source_pages',
                content_rowid='id'
            )
            """
        )
        conn.execute("CREATE INDEX idx_source_pages_source_file ON source_pages(source_file)")

        total = 0
        for path in sorted(SOURCE_DIR.glob("*.json")):
            with path.open(encoding="utf-8") as f:
                data = json.load(f)
            rows = extract_pages(path.name, data)
            conn.executemany(
                "INSERT INTO source_pages (source_file, page_num, text) VALUES (?, ?, ?)",
                rows,
            )
            total += len(rows)

        conn.execute(
            """
            INSERT INTO source_pages_fts (rowid, source_file, page_num, text)
            SELECT id, source_file, page_num, text FROM source_pages
            """
        )
        conn.commit()
    finally:
        conn.close()

    print(f"built {DB_PATH} from {SOURCE_DIR} ({total} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
