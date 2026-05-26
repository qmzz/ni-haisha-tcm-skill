#!/usr/bin/env python3
"""P11-A: 内容质量提升队列。

目标：把 P10 后剩余内容质量问题拆成可执行队列。
不修改医学正文，只生成治理队列和报告。

优先级：
- P0: verified 条目缺关键正文结构（如 formula usage）
- P1: candidate 条目有 source_refs，可进入人工复核/verified 扩展
- P2: no_source_found 条目，需外部来源策略或明确保持边界
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "p11_content_quality_queue.jsonl"
REPORT = ROOT / "report" / "p11_content_quality_queue.md"


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def main():
    rows = load_jsonl(ROOT / "data" / "knowledge_completeness.jsonl")
    queue: List[Dict] = []

    for r in rows:
        kind = r.get("kind")
        item_id = r.get("item_id")
        title = r.get("title") or item_id
        trace_status = r.get("trace_status")
        missing = r.get("missing_content_fields") or []
        file = r.get("file")
        has_source_refs = bool(r.get("has_source_refs"))

        # P0: verified but missing key content field
        if trace_status == "verified" and missing:
            queue.append({
                "priority": "P0",
                "task_type": "fill_verified_missing_content_field",
                "kind": kind,
                "item_id": item_id,
                "title": title,
                "file": file,
                "missing_content_fields": missing,
                "trace_status": trace_status,
                "has_source_refs": has_source_refs,
                "action": "use existing source_refs to fill only missing structured sections; no unsourced expansion",
            })
            continue

        # P1: candidate with source_refs -> suitable for review and promotion
        if trace_status == "candidate" and has_source_refs:
            queue.append({
                "priority": "P1",
                "task_type": "review_candidate_source_refs",
                "kind": kind,
                "item_id": item_id,
                "title": title,
                "file": file,
                "missing_content_fields": missing,
                "trace_status": trace_status,
                "has_source_refs": has_source_refs,
                "action": "human/strict source review; promote to verified only if quote directly supports item",
            })
            continue

        # P2: no_source_found -> boundary/external source strategy
        if trace_status == "no_source_found":
            queue.append({
                "priority": "P2",
                "task_type": "no_source_boundary_or_external_source",
                "kind": kind,
                "item_id": item_id,
                "title": title,
                "file": file,
                "missing_content_fields": missing,
                "trace_status": trace_status,
                "has_source_refs": has_source_refs,
                "action": "do not expand from model memory; either keep no_source_found or add explicit external source workflow",
            })

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for q in queue:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")

    by_priority = Counter(q["priority"] for q in queue)
    by_task = Counter(q["task_type"] for q in queue)
    by_kind = Counter(q["kind"] for q in queue)

    lines = [
        "# P11 内容质量提升队列",
        "",
        "本队列只用于治理排序，不自动修改医学正文。所有正文补强必须来自现有 `source_refs` 或明确可追溯来源。",
        "",
        "## 摘要",
        "",
        f"- total: {len(queue)}",
        f"- P0: {by_priority.get('P0', 0)}",
        f"- P1: {by_priority.get('P1', 0)}",
        f"- P2: {by_priority.get('P2', 0)}",
        "",
        "## 按任务类型",
        "",
    ]
    for k, v in by_task.most_common():
        lines.append(f"- {k}: {v}")
    lines += ["", "## 按类型", ""]
    for k, v in by_kind.most_common():
        lines.append(f"- {k}: {v}")

    lines += [
        "",
        "## P0 明细：verified 但缺关键正文结构",
        "",
        "| kind | item_id | title | missing | file |",
        "|------|---------|-------|---------|------|",
    ]
    for q in queue:
        if q["priority"] == "P0":
            lines.append(f"| {q['kind']} | {q['item_id']} | {q['title']} | {','.join(q['missing_content_fields'])} | {q['file']} |")

    lines += [
        "",
        "## P1 示例：candidate with source_refs（前 30）",
        "",
        "| kind | item_id | title | file |",
        "|------|---------|-------|------|",
    ]
    shown = 0
    for q in queue:
        if q["priority"] == "P1" and shown < 30:
            lines.append(f"| {q['kind']} | {q['item_id']} | {q['title']} | {q['file']} |")
            shown += 1

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "total": len(queue),
        "by_priority": dict(by_priority),
        "by_task": dict(by_task),
        "by_kind": dict(by_kind),
        "out": str(OUT.relative_to(ROOT)),
        "report": str(REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
