#!/usr/bin/env python3
"""构建原始 JSON 轻量 SQLite FTS 检索库。

输出：data/source_fts.sqlite

说明：
- 同时建立普通 source_pages 表和 FTS5 表；
- 中文场景下 FTS5 分词可能不完美，查询层会做 MATCH + LIKE fallback；
- 只存储原始 JSON page/text，不生成医学结论。
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from internal.source_corpus import SourceCorpus

DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "source_fts.sqlite"


def iter_pages():
    corpus = SourceCorpus()
    for path in corpus.files():
        data = corpus._load_json(path)
        pages = corpus._pages(data)
        if pages:
            for page in pages:
                text = page.get("text") or page.get("content") or ""
                page_num = page.get("page_num") or page.get("page")
                if text.strip():
                    yield path.name, page_num, text
        else:
            text = corpus._full_text(data)
            if text.strip():
                yield path.name, None, text


def main():
    DATA_DIR.mkdir(exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE source_pages (id INTEGER PRIMARY KEY, source_file TEXT, page_num INTEGER, text TEXT)")
    try:
        cur.execute("CREATE VIRTUAL TABLE source_pages_fts USING fts5(source_file, page_num UNINDEXED, text, content='source_pages', content_rowid='id')")
        has_fts = True
    except sqlite3.OperationalError:
        has_fts = False

    count = 0
    for source_file, page_num, text in iter_pages():
        cur.execute("INSERT INTO source_pages(source_file, page_num, text) VALUES (?, ?, ?)", (source_file, page_num, text))
        rowid = cur.lastrowid
        if has_fts:
            cur.execute("INSERT INTO source_pages_fts(rowid, source_file, page_num, text) VALUES (?, ?, ?, ?)", (rowid, source_file, page_num, text))
        count += 1
    conn.commit()
    conn.close()
    print(f"wrote {DB_PATH}")
    print(f"pages: {count}, fts5: {has_fts}")


if __name__ == "__main__":
    main()
