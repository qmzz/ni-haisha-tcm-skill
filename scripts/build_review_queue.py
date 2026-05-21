#!/usr/bin/env python3
"""生成 P1 来源复核队列。

输出：data/review_queue.jsonl

进入队列的情况：
- no_source_found：没有任何来源候选；
- needs_review：候选存在但命中来源与预期来源弱相关，或上下文不足。
"""

import json
from pathlib import Path
from typing import Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

CONFIG = [
    {
        "kind": "formula",
        "path": DATA_DIR / "formula_sources.jsonl",
        "id_key": "formula_id",
        "preferred_sources": ["伤寒论", "金匮", "方剂讲解"],
    },
    {
        "kind": "herb",
        "path": DATA_DIR / "herb_sources.jsonl",
        "id_key": "herb_id",
        "preferred_sources": ["神农本草经", "人-神农本草经"],
    },
    {
        "kind": "acupoint",
        "path": DATA_DIR / "acupoint_sources.jsonl",
        "id_key": "acupoint_id",
        "preferred_sources": ["针灸", "针灸大成"],
    },
]


def load_jsonl(path: Path) -> Iterable[Dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def classify(record: Dict, preferred_sources: List[str]) -> str:
    hits = record.get("source_hits") or []
    if not hits:
        return "no_source_found"
    first = hits[0]
    source_file = first.get("source_file", "")
    quote = first.get("quote", "")
    name = record.get("name", "")
    if name and name not in quote:
        return "needs_review"
    if preferred_sources and not any(src in source_file for src in preferred_sources):
        return "needs_review"
    return "candidate"


def main():
    DATA_DIR.mkdir(exist_ok=True)
    out_path = DATA_DIR / "review_queue.jsonl"
    queue = []
    for cfg in CONFIG:
        for record in load_jsonl(cfg["path"]):
            status = classify(record, cfg["preferred_sources"])
            if status in {"no_source_found", "needs_review"}:
                hits = record.get("source_hits") or []
                queue.append({
                    "kind": cfg["kind"],
                    "item_id": record.get(cfg["id_key"]),
                    "name": record.get("name"),
                    "file": record.get("file"),
                    "review_status": status,
                    "reason": "未检索到来源候选" if status == "no_source_found" else "候选来源需人工复核",
                    "top_source": hits[0] if hits else None,
                })
    with out_path.open("w", encoding="utf-8") as out:
        for item in queue:
            out.write(json.dumps(item, ensure_ascii=False) + "\n")

    counts = {}
    for item in queue:
        key = (item["kind"], item["review_status"])
        counts[key] = counts.get(key, 0) + 1
    print(f"wrote {out_path}")
    print(f"review items: {len(queue)}")
    for key in sorted(counts):
        print(f"{key[0]} {key[1]}: {counts[key]}")


if __name__ == "__main__":
    main()
