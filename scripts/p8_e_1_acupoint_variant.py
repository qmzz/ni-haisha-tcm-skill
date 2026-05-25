#!/usr/bin/env python3
"""P8-E-1: 提取 acupoint no_source_found 的命名变体清单。

输入: data/review_queue.jsonl
输出: report/p8_acupoint_no_source_variant.md
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "review_queue.jsonl"
REPORT = ROOT / "report" / "p8_acupoint_no_source_variant.md"

VARIANT_KEYWORDS = ["二", "二号", "上", "下", "外", "内", "俞", "腧"]


def load_queue() -> List[Dict]:
    return [json.loads(line) for line in QUEUE.open(encoding="utf-8") if line.strip()]


def classify(item: Dict) -> str:
    name = item.get("name", "") or ""
    if any(k in name for k in VARIANT_KEYWORDS):
        return "naming_variant"
    return "uncategorized"


def main():
    variants = []
    uncategorized = []

    for item in load_queue():
        if item.get("review_status") != "no_source_found":
            continue
        if item.get("kind") != "acupoint":
            continue
        category = classify(item)
        if category == "naming_variant":
            variants.append(item)
        else:
            uncategorized.append(item)

    lines = [
        "# P8-E acupoint no_source_found 变体盘点",
        "",
        "## 目标",
        "",
        "- 拎出 acupoint no_source_found 中的明显变体条目",
        "- 主要用于判断是否为命名衍生、重复命名或需要降级/合并处理",
        "- 不修改医学内容",
        "",
        f"## 总计",
        "",
        f"- no_source_found: {len(variants) + len(uncategorized)}",
        f"- naming_variant: {len(variants)}",
        f"- uncategorized: {len(uncategorized)}",
        "",
        "## naming_variant",
        "",
        "| item_id | name |",
        "|---------|------|",
    ]

    for item in sorted(variants, key=lambda x: x.get("item_id", "")):
        lines.append(f"| {item.get('item_id')} | {item.get('name')} |")

    lines += ["", "## uncategorized (前 50)", ""]
    lines.append("| item_id | name |")
    lines.append("|---------|------|")
    for item in sorted(uncategorized, key=lambda x: x.get("item_id", ""))[:50]:
        lines.append(f"| {item.get('item_id')} | {item.get('name')} |")

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
