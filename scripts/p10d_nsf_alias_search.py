#!/usr/bin/env python3
"""P10-D: no_source_found 别名扩展搜索。

从 data/aliases.json 读取已知别名，对当前 no_source_found 条目在原始 JSON 中做精确文本搜索。
只产出 candidate hits，不写 review_decisions，不自动 verified。

输出:
- data/p10d_nsf_alias_hits.jsonl
- report/p10d_nsf_alias_hits.md
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT.parent / "nihaixia"
ALIASES = ROOT / "data" / "aliases.json"
OUT = ROOT / "data" / "p10d_nsf_alias_hits.jsonl"
REPORT = ROOT / "report" / "p10d_nsf_alias_hits.md"


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def load_name_maps() -> Dict[Tuple[str, str], str]:
    maps: Dict[Tuple[str, str], str] = {}
    for row in load_jsonl(ROOT / "data" / "herb_index.jsonl"):
        maps[("herb", row.get("herb_id", ""))] = row.get("name", "")
    for row in load_jsonl(ROOT / "data" / "acupoint_index.jsonl"):
        maps[("acupoint", row.get("acupoint_id", ""))] = row.get("name", "")
    return maps


def current_no_source_found() -> List[Dict]:
    name_maps = load_name_maps()
    rows = load_jsonl(ROOT / "data" / "knowledge_completeness.jsonl")
    items = []
    for row in rows:
        if row.get("trace_status") != "no_source_found":
            continue
        kind = row.get("kind")
        item_id = row.get("item_id")
        name = name_maps.get((kind, item_id), row.get("title", ""))
        items.append({"kind": kind, "item_id": item_id, "name": name})
    return items


def keywords_for_item(kind: str, name: str, aliases: Dict) -> List[str]:
    kws = []
    kind_aliases = aliases.get(kind, {}) if isinstance(aliases, dict) else {}
    if name:
        kws.append(name)
        for a in kind_aliases.get(name, []) or []:
            if a and a not in kws:
                kws.append(a)
    return kws


def iter_source_pages():
    if not SOURCE_DIR.exists():
        return
    for path in sorted(SOURCE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        pages = data.get("pages") if isinstance(data, dict) else None
        if not isinstance(pages, list):
            continue
        for page in pages:
            if not isinstance(page, dict):
                continue
            text = page.get("text") or ""
            if not text:
                continue
            yield path.name, page.get("page_num", 0), text


def main():
    aliases = json.loads(ALIASES.read_text(encoding="utf-8")) if ALIASES.exists() else {}
    items = current_no_source_found()
    pages = list(iter_source_pages())

    hits = []
    for item in items:
        kws = keywords_for_item(item["kind"], item["name"], aliases)
        for kw in kws:
            if not kw or len(kw) < 2:
                continue
            found_for_kw = False
            for source_file, page_num, text in pages:
                if kw not in text:
                    continue
                idx = text.find(kw)
                quote = text[max(0, idx - 80): min(len(text), idx + len(kw) + 120)].strip()
                hits.append({
                    "kind": item["kind"],
                    "item_id": item["item_id"],
                    "name": item["name"],
                    "matched_keyword": kw,
                    "source_file": source_file,
                    "page_num": page_num,
                    "quote": quote[:300],
                    "match_type": "alias_or_name_exact",
                    "decision": "candidate",
                    "needs_review_reason": "P10-D alias/name exact hit; requires human source review before verified",
                })
                found_for_kw = True
                break
            if found_for_kw:
                break

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for h in hits:
            f.write(json.dumps(h, ensure_ascii=False) + "\n")

    by_kind = Counter(h["kind"] for h in hits)
    lines = [
        "# P10-D no_source_found 别名扩展命中",
        "",
        f"- 当前 no_source_found: {len(items)}",
        f"- 命中条目: {len(hits)}",
        f"- herb: {by_kind.get('herb', 0)}",
        f"- acupoint: {by_kind.get('acupoint', 0)}",
        "",
        "说明：本报告仅表示别名/正名在原始资料中有精确文本命中；不自动 verified。",
        "",
        "| kind | item_id | name | matched_keyword | source_file | page |",
        "|------|---------|------|-----------------|-------------|------|",
    ]
    for h in hits:
        lines.append(f"| {h['kind']} | {h['item_id']} | {h['name']} | {h['matched_keyword']} | {h['source_file']} | {h['page_num']} |")
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "no_source_found": len(items),
        "hit_items": len(hits),
        "by_kind": dict(by_kind),
        "out": str(OUT.relative_to(ROOT)),
        "report": str(REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
