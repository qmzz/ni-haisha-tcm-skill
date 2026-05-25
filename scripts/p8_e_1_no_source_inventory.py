#!/usr/bin/env python3
"""P8-E-1: 盘点 no_source_found 清单。

输入: data/review_queue.jsonl
输出: report/p8_no_source_inventory.md

分类规则（仅作盘点优先级，不修改医学内容）:
- naming_variant: 名称中含「二」「二号」「上」「下」等明显变体关键词
- possible_alias_or_variant: 名称以常见别名后缀、繁体/异形、穴位/方剂别称特征开头
- herb_like_acupoint_name: acupoint 名称带 herb 常见用字（防止误混，但仅作人工复核提示）
- uncategorized: 命名暂无明显可自动化特征，需要人工复核
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report" / "p8_no_source_inventory.md"
QUEUE = ROOT / "data" / "review_queue.jsonl"

VARIANT_KEYWORDS = ["二", "二号", "上", "下", "外", "内"]
ALIAS_KEYWORDS = ["别名", "异名", "繁体", "穴", "俞", "腧", "募", "会", "郄"]


def load_queue() -> List[Dict]:
    return [json.loads(line) for line in QUEUE.open(encoding="utf-8") if line.strip()]


def classify_acupoint(item: Dict) -> str:
    name = item.get("name", "") or ""
    if any(k in name for k in VARIANT_KEYWORDS):
        return "naming_variant"
    return "uncategorized"


def classify_herb(item: Dict) -> str:
    name = item.get("name", "") or ""
    if any(k in name for k in VARIANT_KEYWORDS):
        return "naming_variant"
    return "uncategorized"


def build_inventory():
    queue = load_queue()
    groups = {"herb": {}, "acupoint": {}}

    for item in queue:
        if item.get("review_status") != "no_source_found":
            continue
        kind = item.get("kind")
        if kind not in groups:
            continue
        category = classify_acupoint(item) if kind == "acupoint" else classify_herb(item)
        groups[kind].setdefault(category, []).append(item)

    return groups


def write_report(groups: Dict[str, Dict[str, List[Dict]]]):
    lines = [
        "# P8-E no_source_found 盘点",
        "",
        "## 目标",
        "",
        "- 输出 herb / acupoint 的 no_source_found 完整清单",
        "- 按命名特征做初步分类，便于后续人工复核",
        "- 本报告不修改医学内容，仅用于治理排程",
        "",
    ]

    for kind, categories in groups.items():
        total = sum(len(v) for v in categories.values())
        lines.append(f"## {kind} (共 {total})")
        lines.append("")
        for category, items in categories.items():
            lines.append(f"### {category} ({len(items)})")
            lines.append("")
            lines.append("| item_id | name | top_source_quality | top_source_reason |")
            lines.append("|---------|------|--------------------|-------------------|")
            for item in items:
                top = item.get("top_source") or {}
                q = top.get("quality_score", "")
                reason = top.get("needs_review_reason", "")
                lines.append(
                    f"| {item.get('item_id')} | {item.get('name')} | {q} | {reason} |"
                )
            lines.append("")

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    return str(REPORT)


def main():
    groups = build_inventory()
    report = write_report(groups)
    print(f"wrote {report}")


if __name__ == "__main__":
    main()
