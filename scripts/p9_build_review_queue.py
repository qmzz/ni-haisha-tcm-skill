#!/usr/bin/env python3
"""P9-B: 生成质量复核队列。

把 P9 审计中的 review/warning 项分类写入 data/p9_review_queue.jsonl。
不修改任何知识文件。
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

REVIEW_QUEUE = DATA / "p9_review_queue.jsonl"


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def classify_duplicate(detail: str) -> str:
    """判断 duplicate_title 的类型。"""
    files = [f.strip() for f in detail.split(",")]
    kinds = set()
    for f in files:
        if "/herbs/" in f:
            kinds.add("herb")
        elif "/acupoints/" in f:
            kinds.add("acupoint")
        elif "/formulas/" in f:
            kinds.add("formula")
    if len(kinds) > 1:
        return "cross_kind_duplicate"
    kind = kinds.pop() if kinds else "unknown"
    if kind == "acupoint":
        # 检查是否有经络后缀变体
        has_suffix = any(
            any(f.endswith(s) for s in ["_gb", "_bl", "_li", "_lu", "_st", "_sp", "_ht", "_si", "_tb", "_pc", "_lv", "_kd", "_cv", "_gv", "_ren", "_du"])
            for f in files
        )
        return "acupoint_variant" if has_suffix else "acupoint_same_name"
    if kind == "herb":
        return "herb_alias_pair"
    return "same_kind_duplicate"


def build_review_queue():
    audit = load_jsonl(DATA / "p9_quality_audit.jsonl")
    queue = []
    for item in audit:
        entry = {
            "level": item["level"],
            "kind": item["kind"],
            "code": item["code"],
            "file": item["file"],
            "detail": item.get("detail", ""),
            "status": "pending",
        }
        if item["code"] == "duplicate_title":
            entry["duplicate_type"] = classify_duplicate(item.get("detail", ""))
        queue.append(entry)
    with REVIEW_QUEUE.open("w", encoding="utf-8") as f:
        for entry in queue:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"wrote {len(queue)} entries to {REVIEW_QUEUE}")
    # 统计
    by_type = {}
    for entry in queue:
        key = entry["code"]
        if entry["code"] == "duplicate_title":
            key = f"duplicate_title:{entry['duplicate_type']}"
        by_type[key] = by_type.get(key, 0) + 1
    for k, v in sorted(by_type.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    build_review_queue()
