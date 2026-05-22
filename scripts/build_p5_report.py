#!/usr/bin/env python3
"""生成 P5 精修阶段汇总报告。"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p5_refinement_report.md"

SAMPLE_FILES = [
    "knowledge/formulas/guizhi_tang.md",
    "knowledge/formulas/mahuang_tang.md",
    "knowledge/formulas/xiaochaihu_tang.md",
    "knowledge/formulas/wuling_san.md",
    "knowledge/formulas/banxia_xiexin.md",
    "knowledge/herbs/mahuang.md",
    "knowledge/herbs/guizhi.md",
    "knowledge/herbs/gancao.md",
    "knowledge/herbs/fuzi.md",
    "knowledge/herbs/banxia.md",
]


def load_jsonl(path: Path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    REPORT.parent.mkdir(exist_ok=True)
    verified = load_jsonl(DATA / "verified_sources.jsonl")
    decisions = load_jsonl(DATA / "review_decisions.jsonl")
    queue = load_jsonl(DATA / "review_queue.jsonl")
    verified_by_kind = Counter(r.get("kind") for r in verified)
    decisions_by_reviewer = Counter(r.get("reviewer") for r in decisions)
    queue_by_pair = Counter((r.get("kind"), r.get("review_status")) for r in queue)
    sample_ok = []
    for rel in SAMPLE_FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        sample_ok.append({
            "file": rel,
            "standardized": "<!-- P5_STANDARD_NOTICE_START -->" in text and "safety_disclaimer_required: true" in text,
        })

    lines = [
        "# P5 数据精修阶段汇总报告",
        "",
        "## 总览",
        "",
        f"- verified_sources：{len(verified)}",
        f"- review_decisions：{len(decisions)}",
        f"- review_queue：{len(queue)}",
        f"- 样板标准化条目：{sum(1 for r in sample_ok if r['standardized'])}/{len(sample_ok)}",
        "",
        "## Verified 分布",
        "",
        "| kind | count |",
        "|------|------:|",
    ]
    for kind, count in sorted(verified_by_kind.items()):
        lines.append(f"| {kind} | {count} |")

    lines += ["", "## P5 Reviewer 分布", "", "| reviewer | count |", "|----------|------:|"]
    for reviewer, count in sorted(decisions_by_reviewer.items()):
        if reviewer and str(reviewer).startswith("p5_"):
            lines.append(f"| {reviewer} | {count} |")

    lines += ["", "## Review Queue 分布", "", "| kind | status | count |", "|------|--------|------:|"]
    for (kind, status), count in sorted(queue_by_pair.items()):
        lines.append(f"| {kind} | {status} | {count} |")

    lines += ["", "## P5 样板标准化条目", "", "| file | standardized |", "|------|--------------|"]
    for row in sample_ok:
        lines.append(f"| {row['file']} | {row['standardized']} |")

    lines += [
        "",
        "## P5 已完成内容",
        "",
        "- P5-A：核心方剂 verified 扩展首批 20 个。",
        "- P5-B：核心药材 verified 扩展首批 17 个。",
        "- P5-C：核心穴位 verified 扩展首批 20 个。",
        "- P5-D：10 个样板条目完成 frontmatter / 安全边界标准化。",
        "- P5-E：生成本汇总报告与发布说明。",
        "",
        "## 后续精修建议",
        "",
        "1. 每批继续只处理 10-20 个 verified 条目。",
        "2. 优先扩展已 verified 但未标准化的方剂、药材、穴位。",
        "3. 不自动改写医学正文，不新增未溯源医学结论。",
        "4. 候选来源仍需人工复核，candidate 不等于 verified。",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
