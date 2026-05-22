#!/usr/bin/env python3
"""生成 P3 知识治理质量报告。"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "quality_report.md"


def load(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    REPORT.parent.mkdir(exist_ok=True)
    formula = load(DATA / "formula_sources.jsonl")
    herb = load(DATA / "herb_sources.jsonl")
    acupoint = load(DATA / "acupoint_sources.jsonl")
    review = load(DATA / "review_queue.jsonl")
    verified = load(DATA / "verified_sources.jsonl") if (DATA / "verified_sources.jsonl").exists() else []
    alias = json.loads((DATA / "aliases.json").read_text(encoding="utf-8")) if (DATA / "aliases.json").exists() else {}

    lines = ["# P3 质量看板", "", "## 来源候选覆盖率", "", "| kind | total | with_candidates | no_source | coverage |", "|------|------:|----------------:|----------:|---------:|"]
    for kind, rows in [("formula", formula), ("herb", herb), ("acupoint", acupoint)]:
        total = len(rows)
        with_hits = sum(1 for r in rows if r.get("source_hits"))
        coverage = with_hits / total * 100 if total else 0
        lines.append(f"| {kind} | {total} | {with_hits} | {total-with_hits} | {coverage:.1f}% |")

    q = Counter((r.get("kind"), r.get("review_status")) for r in review)
    lines += ["", "## Review Queue", "", "| kind | status | count |", "|------|--------|------:|"]
    for (kind, status), count in sorted(q.items()):
        lines.append(f"| {kind} | {status} | {count} |")

    lines += ["", "## Verified / Alias", "", f"- verified_sources：{len(verified)}", f"- alias kind 数：{len(alias)}"]
    for kind, mapping in sorted(alias.items()):
        lines.append(f"- {kind} alias 条目：{len(mapping)}")

    lines += ["", "## 治理原则", "", "- candidate 不等于 verified。", "- no_source_found 不自动补写医学内容。", "- alias 命中只作为候选来源，仍需人工复核。", "- 高风险症状不输出方剂治疗建议。", ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
