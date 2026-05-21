#!/usr/bin/env python3
"""构建药材结构化索引。

输出：data/herb_index.jsonl
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]
HERB_DIR = ROOT / "knowledge" / "herbs"
DATA_DIR = ROOT / "data"


def parse_frontmatter(text: str) -> Dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    data = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def first_heading(text: str) -> str:
    m = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def load_sources() -> Dict[str, Dict]:
    path = DATA_DIR / "herb_sources.jsonl"
    if not path.exists():
        raise SystemExit("missing data/herb_sources.jsonl, run: python3 scripts/build_herb_sources.py")
    items = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            items[record["herb_id"]] = record
    return items


def main():
    DATA_DIR.mkdir(exist_ok=True)
    source_map = load_sources()
    out_path = DATA_DIR / "herb_index.jsonl"
    count = 0
    with out_path.open("w", encoding="utf-8") as out:
        for path in sorted(HERB_DIR.glob("*.md")):
            if "index" in path.name:
                continue
            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            herb_id = path.stem
            source_hits = source_map.get(herb_id, {}).get("source_hits", [])
            record = {
                "herb_id": herb_id,
                "name": fm.get("title") or first_heading(text) or herb_id,
                "file": str(path.relative_to(ROOT)),
                "source": fm.get("source"),
                "category": fm.get("category"),
                "properties": fm.get("性味"),
                "meridian": fm.get("归经"),
                "effects": fm.get("功效"),
                "trace_status": "candidate" if source_hits else "no_source_found",
                "source_refs": source_hits[:3],
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    print(f"wrote {out_path}")
    print(f"herb records: {count}")


if __name__ == "__main__":
    main()
