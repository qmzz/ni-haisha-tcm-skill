#!/usr/bin/env python3
"""构建方剂结构化索引。

输出：data/formula_index.jsonl

该索引用于 P1 阶段：把现有 Markdown 方剂知识与原始 JSON 来源候选关联起来。
注意：本脚本不自动改写知识正文，只产出可审计索引。
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]
FORMULA_DIR = ROOT / "knowledge" / "formulas"
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
        value = value.strip().strip('"').strip("'")
        data[key.strip()] = value
    return data


def first_heading(text: str) -> str:
    m = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def load_formula_sources() -> Dict[str, Dict]:
    path = DATA_DIR / "formula_sources.jsonl"
    if not path.exists():
        raise SystemExit("missing data/formula_sources.jsonl, run: python3 scripts/build_formula_sources.py")
    items = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            items[record["formula_id"]] = record
    return items


def main():
    DATA_DIR.mkdir(exist_ok=True)
    source_map = load_formula_sources()
    out_path = DATA_DIR / "formula_index.jsonl"
    count = 0
    with out_path.open("w", encoding="utf-8") as out:
        for path in sorted(FORMULA_DIR.glob("*.md")):
            if path.name == "jingfang_index.md":
                continue
            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            formula_id = path.stem
            source_record = source_map.get(formula_id, {})
            source_hits = source_record.get("source_hits", [])
            record = {
                "formula_id": formula_id,
                "name": fm.get("title") or first_heading(text) or formula_id,
                "file": str(path.relative_to(ROOT)),
                "source": fm.get("source"),
                "category": fm.get("category"),
                "tags": fm.get("tags"),
                "trace_status": "candidate" if source_hits else "no_source_found",
                "source_refs": source_hits[:3],
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    print(f"wrote {out_path}")
    print(f"formula records: {count}")


if __name__ == "__main__":
    main()
