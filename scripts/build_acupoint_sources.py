#!/usr/bin/env python3
"""为现有穴位知识文件生成原始来源候选索引。

输出：data/acupoint_sources.jsonl

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
ACUPOINT_DIR = ROOT / "knowledge" / "acupoints"
DATA_DIR = ROOT / "data"


def clean_title(title: str) -> str:
    title = re.sub(r"\s*\([^)]*\)\s*$", "", title).strip()
    if title.endswith("穴") and len(title) > 1:
        title = title[:-1]
    return title


def parse_file(path: Path) -> Dict:
    text = path.read_text(encoding="utf-8")
    title = None
    meridian = None
    m = re.search(r'^title:\s*["\']?([^"\'\n]+)["\']?\s*$', text, re.MULTILINE)
    if m:
        title = m.group(1).strip()
    if not title:
        m = re.search(r'^#\s+(.+?)\s*$', text, re.MULTILINE)
        if m:
            title = m.group(1).strip()
    m = re.search(r'\*\*归经：\*\*\s*([^\n]+)', text)
    if m:
        meridian = m.group(1).strip().rstrip('  ')
    name = clean_title(title or path.stem)
    return {
        "acupoint_id": path.stem,
        "name": name,
        "display_name": title or path.stem,
        "meridian": meridian,
        "file": str(path.relative_to(ROOT)),
    }


def score_hit(name: str, hit: Dict, expected_source: Optional[str] = None) -> int:
    quote = hit.get("quote", "")
    source_file = hit.get("source_file", "")
    score = quote.count(name) * 10
    for preferred in ["针灸大成", "人-针灸篇"]:
        if preferred in source_file:
            score += 30
    if f"{name}穴" in quote:
        score += 10
    for kw in ["穴", "针", "灸", "经", "督脉", "任脉", "定位", "寸", "主治", "倪"]:
        if kw in quote:
            score += 1
    return score


def build(limit_per_item: int = 5) -> List[Dict]:
    corpus = SourceCorpus()
    records = []
    for path in sorted(ACUPOINT_DIR.glob("*.md")):
        if "index" in path.name:
            continue
        item = parse_file(path)
        hits = []
        for keyword in keywords_for("acupoint", item["name"]):
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
        hits.sort(key=lambda h: score_hit(h.get("matched_keyword") or item["name"], h), reverse=True)
        item["searched_keywords"] = keywords_for("acupoint", item["name"])
        item["source_hits"] = hits[:limit_per_item]
        item["source_hit_count"] = len(hits)
        item["status"] = "candidate" if hits else "no_source_found"
        records.append(item)
    return records


def main():
    DATA_DIR.mkdir(exist_ok=True)
    out_path = DATA_DIR / "acupoint_sources.jsonl"
    records = build()
    with out_path.open("w", encoding="utf-8") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    total = len(records)
    with_hits = sum(1 for r in records if r["source_hits"])
    print(f"wrote {out_path}")
    print(f"acupoints: {total}, with source candidates: {with_hits}, no source: {total - with_hits}")


if __name__ == "__main__":
    main()
