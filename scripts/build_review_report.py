#!/usr/bin/env python3
"""生成 review_queue Markdown 审核报告。

输出：report/review_report.md
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "report"


def load_queue() -> List[Dict]:
    path = DATA_DIR / "review_queue.jsonl"
    if not path.exists():
        raise SystemExit("missing data/review_queue.jsonl, run: python3 scripts/build_review_queue.py")
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def render_table(items: List[Dict], limit: int = 20) -> str:
    lines = ["| kind | id | name | status | reason |", "|------|----|------|--------|--------|"]
    for item in items[:limit]:
        lines.append(
            f"| {item.get('kind')} | {item.get('item_id')} | {item.get('name')} | "
            f"{item.get('review_status')} | {item.get('reason')} |"
        )
    return "\n".join(lines)


def build_report() -> str:
    items = load_queue()
    by_kind = Counter(item.get("kind") for item in items)
    by_status = Counter(item.get("review_status") for item in items)
    by_pair = Counter((item.get("kind"), item.get("review_status")) for item in items)
    groups = defaultdict(list)
    for item in items:
        groups[(item.get("kind"), item.get("review_status"))].append(item)

    lines = [
        "# P3 Review Queue 审核报告",
        "",
        "> 本报告由 `scripts/build_review_report.py` 生成，用于辅助 P3 阶段处理来源复核队列。",
        "",
        "## 总览",
        "",
        f"- 复核队列总数：**{len(items)}**",
        "",
        "### 按类型统计",
        "",
        "| kind | count |",
        "|------|------:|",
    ]
    for kind, count in sorted(by_kind.items()):
        lines.append(f"| {kind} | {count} |")

    lines.extend(["", "### 按状态统计", "", "| status | count |", "|--------|------:|"])
    for status, count in sorted(by_status.items()):
        lines.append(f"| {status} | {count} |")

    lines.extend(["", "### 类型 × 状态", "", "| kind | status | count |", "|------|--------|------:|"])
    for (kind, status), count in sorted(by_pair.items()):
        lines.append(f"| {kind} | {status} | {count} |")

    lines.extend([
        "",
        "## 优先处理建议",
        "",
        "1. 先处理 `formula:needs_review`，数量少且影响辨证辅助主链路。",
        "2. 再处理 `herb:needs_review` 与 `acupoint:needs_review`，优先高频药材/穴位。",
        "3. `no_source_found` 不直接补写，先走 alias / 异名匹配后再判定。",
        "",
    ])

    for key in sorted(groups):
        kind, status = key
        lines.extend([
            f"## {kind} / {status}",
            "",
            render_table(groups[key], limit=30),
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    out_path = REPORT_DIR / "review_report.md"
    out_path.write_text(build_report(), encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
