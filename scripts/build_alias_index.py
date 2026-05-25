#!/usr/bin/env python3
"""P10-B: 构建 alias 索引。

从知识文件的 frontmatter 提取 aliases / alias_of 关系，
生成 data/alias_index.jsonl 供查询使用。

不修改知识文件，只构建索引。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

KINDS = {
    "formula": ROOT / "knowledge" / "formulas",
    "herb": ROOT / "knowledge" / "herbs",
    "acupoint": ROOT / "knowledge" / "acupoints",
}


def parse_frontmatter(text: str) -> Tuple[Dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 5 :]
    fm: Dict[str, object] = {}
    key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", line):
            k, v = line.split(":", 1)
            key = k.strip()
            fm[key] = v.strip().strip('"')
        elif key:
            fm[key] = fm.get(key, "") or "__complex__"
    return fm, body


def extract_aliases(fm: Dict) -> List[str]:
    """提取 aliases 列表。"""
    val = fm.get("aliases", "")
    if not val or val == "__complex__":
        return []
    try:
        return json.loads(val)
    except json.JSONDecodeError:
        return []


def main():
    index: List[Dict] = []

    for kind, folder in KINDS.items():
        for path in sorted(folder.glob("*.md")):
            if "index" in path.name:
                continue
            text = path.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(text)

            item_id = path.stem
            title = fm.get("title", item_id)
            alias_of = fm.get("alias_of", "").strip('"')
            aliases = extract_aliases(fm)

            # alias_of 关系：当前条目是别名，指向标准条目
            # 只使用 alias_of，不使用 aliases 避免双向循环
            if alias_of:
                index.append({
                    "kind": kind,
                    "alias_id": item_id,
                    "alias_title": title,
                    "target_id": alias_of,
                    "target_title": "",  # 后续回填
                    "rel_type": "alias_of",
                    "source": "frontmatter.alias_of",
                })

    # 回填 target_title：从所有知识文件收集
    title_map = {}
    for kind, folder in KINDS.items():
        for path in sorted(folder.glob("*.md")):
            if "index" in path.name:
                continue
            text = path.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(text)
            title_map[path.stem] = fm.get("title", path.stem)

    for entry in index:
        if entry["rel_type"] == "alias_of" and entry["target_id"] in title_map:
            entry["target_title"] = title_map[entry["target_id"]]

    # 去重
    seen = set()
    unique = []
    for e in index:
        key = (e["kind"], e["alias_id"], e["target_id"])
        if key not in seen:
            seen.add(key)
            unique.append(e)

    OUT = DATA / "alias_index.jsonl"
    with OUT.open("w", encoding="utf-8") as f:
        for e in unique:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    print(json.dumps({
        "total_aliases": len(unique),
        "by_kind": {k: sum(1 for e in unique if e["kind"] == k) for k in KINDS},
        "sample": unique[:5]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
