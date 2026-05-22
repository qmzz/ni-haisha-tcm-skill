#!/usr/bin/env python3
"""P6-C：no_source_found 专项治理报告。

本脚本不凭空补来源，只对 review_queue 中仍未解决的 no_source_found 条目做分类、
别名建议与 FTS 线索汇总，作为后续人工复核入口。
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p6_no_source_report.md"


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_alias_candidates():
    path = DATA / "alias_candidates.jsonl"
    rows = load_jsonl(path)
    by_key = {}
    for row in rows:
        key = (row.get("kind"), row.get("item_id"))
        by_key.setdefault(key, []).append(row)
    return by_key


def main():
    queue = load_jsonl(DATA / "review_queue.jsonl")
    decisions = {(r.get("kind"), r.get("item_id")) for r in load_jsonl(DATA / "review_decisions.jsonl")}
    alias_candidates = load_alias_candidates()
    unresolved = [r for r in queue if (r.get("kind"), r.get("item_id")) not in decisions]
    no_source = [r for r in unresolved if r.get("review_status") == "no_source_found"]
    needs_review = [r for r in unresolved if r.get("review_status") == "needs_review"]

    kind_counts = Counter(r.get("kind") for r in no_source)
    alias_hits = [r for r in no_source if alias_candidates.get((r.get("kind"), r.get("item_id")))]

    lines = [
        "# P6-C no_source_found 专项治理报告",
        "",
        "## 治理原则",
        "",
        "- `no_source_found` 不自动提升为 verified。",
        "- alias / FTS / 同义线索只进入候选与人工复核，不作为医学真实性判定。",
        "- 找不到明确来源时保持待考，不凭模型记忆补写。",
        "",
        "## 当前队列概览",
        "",
        f"- review_queue 总数：{len(queue)}",
        f"- 已有决策条目：{len(decisions)}",
        f"- 未决队列：{len(unresolved)}",
        f"- 未决 no_source_found：{len(no_source)}",
        f"- 未决 needs_review：{len(needs_review)}",
        "",
        "### 未决 no_source_found 类型分布",
        "",
    ]
    for kind, count in sorted(kind_counts.items()):
        lines.append(f"- {kind}: {count}")

    lines.extend([
        "",
        "## alias 候选线索",
        "",
        f"当前 no_source_found 中带 alias candidate 的条目数：{len(alias_hits)}",
        "",
    ])
    if alias_hits:
        lines.append("| kind | item_id | name | alias_candidates |")
        lines.append("|------|---------|------|------------------|")
        for item in alias_hits[:50]:
            cands = alias_candidates.get((item.get("kind"), item.get("item_id")), [])
            aliases = ", ".join(str(c.get("alias") or c.get("candidate") or c.get("matched_keyword")) for c in cands[:5])
            lines.append(f"| {item.get('kind')} | {item.get('item_id')} | {item.get('name')} | {aliases} |")
    else:
        lines.append("暂无可直接应用的 alias candidate。")

    lines.extend([
        "",
        "## 优先处理建议",
        "",
        "1. 先处理 `needs_review`：多数已有候选来源，复核成本低于 no_source_found。",
        "2. 对 herb no_source_found 做同名异写、简繁、古今名二次 alias 整理。",
        "3. 对 acupoint no_source_found 优先补经穴编号 / 别名 / 经络归属，再重建来源索引。",
        "4. 仍无来源者保留 `no_source_found`，不要降格自动写入正文。",
        "",
        "## 未决样例（前 80 条）",
        "",
        "| kind | status | item_id | name | reason |",
        "|------|--------|---------|------|--------|",
    ])
    for item in unresolved[:80]:
        reason = str(item.get("reason") or "").replace("|", "\\|")
        lines.append(f"| {item.get('kind')} | {item.get('review_status')} | {item.get('item_id')} | {item.get('name')} | {reason} |")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "report": str(REPORT.relative_to(ROOT)),
        "review_queue": len(queue),
        "unresolved": len(unresolved),
        "no_source_found": len(no_source),
        "needs_review": len(needs_review),
        "kind_counts": dict(kind_counts),
        "alias_candidate_items": len(alias_hits),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
