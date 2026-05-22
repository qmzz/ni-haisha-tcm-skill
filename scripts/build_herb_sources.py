#!/usr/bin/env python3
"""为现有药材知识文件生成原始来源候选索引。

输出：data/herb_sources.jsonl

原则：只生成候选来源，不自动改正文；候选来源来自 `project/nihaixia/*.json`。
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from internal.source_corpus import SourceCorpus
from internal.alias_registry import keywords_for

ROOT = Path(__file__).resolve().parents[1]
HERB_DIR = ROOT / "knowledge" / "herbs"
DATA_DIR = ROOT / "data"


def parse_file(path: Path) -> Dict:
    text = path.read_text(encoding="utf-8")
    title = None
    source = None
    m = re.search(r'^title:\s*["\']?([^"\'\n]+)["\']?\s*$', text, re.MULTILINE)
    if m:
        title = m.group(1).strip()
    if not title:
        m = re.search(r'^#\s+(.+?)\s*$', text, re.MULTILINE)
        if m:
            title = m.group(1).strip()
    m = re.search(r'^source:\s*["\']?([^"\'\n]+)["\']?\s*$', text, re.MULTILINE)
    if m:
        source = m.group(1).strip()
    return {
        "herb_id": path.stem,
        "name": title or path.stem,
        "source": source,
        "file": str(path.relative_to(ROOT)),
    }


def score_hit(name: str, hit: Dict, expected_source: Optional[str] = None) -> int:
    quote = hit.get("quote", "")
    source_file = hit.get("source_file", "")
    score = quote.count(name) * 10
    if expected_source and expected_source in source_file:
        score += 30
    for preferred in ["神农本草经", "人-神农本草经", "倪海厦人纪系列之神农本草经"]:
        if preferred in source_file:
            score += 20
    for kw in ["性味", "主治", "本经", "药", "草", "经", "毒", "无毒", "倪"]:
        if kw in quote:
            score += 1
    return score


def build(limit_per_item: int = 5) -> List[Dict]:
    corpus = SourceCorpus()
    records = []
    for path in sorted(HERB_DIR.glob("*.md")):
        if "index" in path.name:
            continue
        item = parse_file(path)
        hits = []
        for keyword in keywords_for("herb", item["name"]):
            for hit in corpus.search(keyword, limit=80, context=120):
                record = hit.to_dict()
                record["matched_keyword"] = keyword
                hits.append(record)
        seen = set()
        deduped = []
        for hit in hits:
            key = (hit.get("source_file"), hit.get("page_num"), hit.get("char_start"), hit.get("matched_keyword"))
            if key not in seen:
                seen.add(key)
                deduped.append(hit)
        hits = deduped
        hits.sort(key=lambda h: score_hit(h.get("matched_keyword") or item["name"], h, item.get("source")), reverse=True)
        item["searched_keywords"] = keywords_for("herb", item["name"])
        item["source_hits"] = hits[:limit_per_item]
        item["source_hit_count"] = len(hits)
        item["status"] = "candidate" if hits else "no_source_found"
        records.append(item)
    return records


def main():
    DATA_DIR.mkdir(exist_ok=True)
    out_path = DATA_DIR / "herb_sources.jsonl"
    records = build()
    with out_path.open("w", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    total = len(records)
    with_hits = sum(1 for r in records if r["source_hits"])
    print(f"wrote {out_path}")
    print(f"herbs: {total}, with source candidates: {with_hits}, no source: {total - with_hits}")


if __name__ == "__main__":
    main()
