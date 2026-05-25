#!/usr/bin/env python3
"""P10-D: 对 no_source_found 条目做中文名文本搜索。

策略:
- 从 herb_index / acupoint_index 获取中文名
- 在所有 JSON 源文件中搜索中文名
- 只产出候选命中，不做 verified 决策

输出:
- data/p10d_nsf_hits.jsonl
- report/p10d_nsf_hits.md
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
NSF_PATH = ROOT / "data" / "no_source_found_items.jsonl"
HERB_INDEX = ROOT / "data" / "herb_index.jsonl"
ACU_INDEX = ROOT / "data" / "acupoint_index.jsonl"
SRC_FOLDERS = [
    ROOT.parent / "nihaixia",
]
HITS_PATH = ROOT / "data" / "p10d_nsf_hits.jsonl"
REPORT = ROOT / "report" / "p10d_nsf_hits.md"


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def load_index_map() -> Dict[Tuple[str, str], str]:
    """kind/item_id -> Chinese name"""
    mapping = {}
    for row in load_jsonl(HERB_INDEX):
        mapping[("herb", row.get("herb_id", ""))] = row.get("name", "")
    for row in load_jsonl(ACU_INDEX):
        mapping[("acupoint", row.get("acupoint_id", ""))] = row.get("name", "")
    return mapping


def get_nsf_items() -> List[Tuple[str, str, str]]:
    """Return [(kind, item_id, name)]"""
    rows = load_jsonl(ROOT / "data" / "knowledge_completeness.jsonl")
    nsf = [(r["kind"], r["item_id"]) for r in rows if r.get("trace_status") == "no_source_found"]
    index_map = load_index_map()
    return [(k, i, index_map.get((k, i), "")) for k, i in nsf]


def search_source_files(kind: str, name: str, item_id: str) -> List[Dict]:
    """Search all JSON source files for Chinese name."""
    hits = []
    
    if not name or len(name) < 2:
        return hits
    
    for folder in SRC_FOLDERS:
        if not folder.exists():
            continue
        for json_path in sorted(folder.glob("*.json")):
            try:
                content = json.loads(json_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            
            # Handle structure: {pages: [...], full_text: str}
            pages = content.get("pages") if isinstance(content, dict) else None
            if not isinstance(pages, list):
                continue
            
            for page in pages:
                if not isinstance(page, dict):
                    continue
                page_num = page.get("page_num", 0)
                text = page.get("text") or page.get("content") or ""
                if not text:
                    continue
                
                if name in text:
                    idx = text.find(name)
                    start = max(0, idx - 80)
                    end = min(len(text), idx + len(name) + 120)
                    quote = text[start:end].strip()
                    
                    hits.append({
                        "kind": kind,
                        "item_id": item_id,
                        "name": name,
                        "source_file": json_path.name,
                        "page_num": page_num,
                        "quote": quote[:300],
                        "match_type": "chinese_name_exact",
                    })
                    break  # one hit per file
    
    return hits


def main():
    items = get_nsf_items()
    print(f"Total no_source_found: {len(items)}")
    
    all_hits = []
    hit_count = 0
    
    for kind, item_id, name in items:
        hits = search_source_files(kind, name, item_id)
        if hits:
            hit_count += 1
            all_hits.extend(hits[:3])  # max 3 hits per item
    
    # Write hits
    HITS_PATH.parent.mkdir(exist_ok=True)
    with HITS_PATH.open("w", encoding="utf-8") as f:
        for h in all_hits:
            f.write(json.dumps(h, ensure_ascii=False) + "\n")
    
    # Write report
    report_lines = [
        "# P10-D no_source_found 中文名搜索命中",
        "",
        f"- 搜索条目: {len(items)}",
        f"- 命中条目: {hit_count}",
        f"- 总命中数: {len(all_hits)}",
        "",
        "## 命中列表",
        "",
        "| kind | item_id | name | source_file | page |",
        "|------|---------|------|-------------|------|",
    ]
    for h in all_hits:
        report_lines.append(f"| {h['kind']} | {h['item_id']} | {h['name']} | {h['source_file']} | {h['page_num']} |")
    
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    
    print(json.dumps({
        "searched": len(items),
        "hit_items": hit_count,
        "total_hits": len(all_hits),
        "by_kind": {k: sum(1 for h in all_hits if h["kind"] == k) for k in ["herb", "acupoint"]},
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
