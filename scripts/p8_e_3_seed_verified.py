#!/usr/bin/env python3
"""P8-E-3: 将高置信扩展命中落库为 verified。

输入:
- data/p8_e_no_source_expand_hits.jsonl
- data/review_decisions.jsonl

输出:
- data/review_decisions.jsonl (append)
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
HITS_PATH = ROOT / "data" / "p8_e_no_source_expand_hits.jsonl"
DECISIONS_PATH = ROOT / "data" / "review_decisions.jsonl"
INDEX_PATHS = {
    "acupoint": ROOT / "data" / "acupoint_index.jsonl",
    "herb": ROOT / "data" / "herb_index.jsonl",
}


def load_jsonl(path: Path) -> List[Dict]:
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def load_file_map() -> Dict[Tuple[str, str], str]:
    mapping: Dict[Tuple[str, str], str] = {}
    id_keys = {"acupoint": "acupoint_id", "herb": "herb_id"}
    for kind, path in INDEX_PATHS.items():
        for row in load_jsonl(path):
            item_id = row.get(id_keys[kind])
            file = row.get("file")
            if item_id and file:
                mapping[(kind, item_id)] = file
    return mapping


def best_hit_per_item(hits: List[Dict]) -> Dict[Tuple[str, str], Dict]:
    best: Dict[Tuple[str, str], Dict] = {}
    for h in hits:
        key = (h["kind"], h["item_id"])
        q = h.get("matched_hit", {}).get("quality_score", 0)
        if key not in best or q > (best[key].get("matched_hit", {}).get("quality_score", -1)):
            best[key] = h
    return best


def main():
    best = best_hit_per_item(load_jsonl(HITS_PATH))
    decisions = load_jsonl(DECISIONS_PATH)
    file_map = load_file_map()

    # Idempotency: skip items already in decisions
    existing_keys = {(d.get('kind'), d.get('item_id'), d.get('decision')) for d in decisions}

    added = []

    for (kind, item_id), hit in sorted(best.items()):
        reason = hit.get("expand_reason", "")
        score = hit.get("matched_hit", {}).get("quality_score", 0)

        if kind == "acupoint" and "acupoint_trim_variant" in reason and score >= 74:
            category = "acupoint_parent_expand"
        elif kind == "herb" and reason in {"herb_alias_fallback", "herb_trim_suffix"} and score >= 95:
            category = "herb_parent_expand"
        else:
            continue

        key = (kind, item_id, "verified")
        if key in existing_keys:
            continue

        decisions.append({
            "kind": kind,
            "item_id": item_id,
            "name": hit.get("name"),
            "file": file_map.get((kind, item_id), ""),
            "decision": "verified",
            "source_file": hit.get("matched_hit", {}).get("source_file"),
            "page_num": hit.get("matched_hit", {}).get("page_num"),
            "quote": (hit.get("matched_hit", {}).get("quote") or "")[:500],
            "reviewer": "p8_e_parent_expand",
            "reviewed_at": datetime.now().strftime("%Y-%m-%d"),
            "notes": f"P8-E parent name expand trace ({category}, score={score}, variant={hit.get('search_variant')})"
        })
        added.append(hit)

    DECISIONS_PATH.parent.mkdir(exist_ok=True)
    with DECISIONS_PATH.open("w", encoding="utf-8") as f:
        for d in decisions:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    print(json.dumps({
        "added": len(added),
        "decisions_after": len(decisions),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
