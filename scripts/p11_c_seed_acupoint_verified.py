#!/usr/bin/env python3
"""P11-C: acupoint 高置信 candidate verified 第一批。

约束：
- 只处理 data/acupoint_index.jsonl 中 trace_status=candidate 的 acupoint
- 只接受最高 quality_score >= 80 的 source_ref
- 默认最多处理 50 条，避免一次性扩大风险
- 不改医学正文
- verified 仅表示来源追溯链路通过，不代表医学真实性或针灸操作适用性
- 默认 dry-run，传 --apply 才写入 review_decisions.jsonl
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p11_c_acupoint_verified_batch_report.md"
THRESHOLD = 80
REVIEWER = "p11_c_acupoint_high_confidence_batch1"
DEFAULT_LIMIT = 50


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def write_jsonl(path: Path, rows: List[Dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def best_source_ref(row: Dict) -> Dict | None:
    refs = row.get("source_refs") or []
    if not refs:
        return None
    return max(refs, key=lambda r: r.get("quality_score") or 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write review_decisions.jsonl")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="max items to add")
    args = parser.parse_args()

    acupoint_rows = load_jsonl(DATA / "acupoint_index.jsonl")
    decisions = load_jsonl(DATA / "review_decisions.jsonl")
    existing = {(d.get("kind"), d.get("item_id"), d.get("decision")) for d in decisions}

    pool = []
    skipped_existing = 0
    skipped_low_score = 0
    skipped_no_ref = 0

    for row in acupoint_rows:
        item_id = row.get("acupoint_id")
        if not item_id or row.get("trace_status") != "candidate":
            continue
        if ("acupoint", item_id, "verified") in existing:
            skipped_existing += 1
            continue
        ref = best_source_ref(row)
        if not ref:
            skipped_no_ref += 1
            continue
        score = ref.get("quality_score") or 0
        if score < THRESHOLD:
            skipped_low_score += 1
            continue
        pool.append((row, ref, score))

    # 稳定排序：高分优先，其次 item_id，默认取前 limit 条
    pool.sort(key=lambda x: (-(x[2]), x[0].get("acupoint_id") or ""))
    selected = pool[: max(0, args.limit)]

    candidates = []
    for row, ref, score in selected:
        candidates.append({
            "kind": "acupoint",
            "item_id": row.get("acupoint_id"),
            "name": row.get("name"),
            "file": row.get("file"),
            "decision": "verified",
            "source_file": ref.get("source_file"),
            "page_num": ref.get("page_num"),
            "quote": (ref.get("quote") or "")[:500],
            "reviewer": REVIEWER,
            "reviewed_at": date.today().isoformat(),
            "notes": "P11-C acupoint high-confidence batch1; source_ref quality_score >=80; traceability only, not medical validation or acupuncture operation guidance.",
            "quality_score": score,
            "match_reason": ref.get("match_reason") or [],
            "risk_flags": ref.get("risk_flags") or [],
        })

    if args.apply and candidates:
        decisions.extend(candidates)
        write_jsonl(DATA / "review_decisions.jsonl", decisions)

    REPORT.parent.mkdir(exist_ok=True)
    lines = [
        "# P11-C acupoint 高置信 candidate verified 第一批",
        "",
        f"- threshold: {THRESHOLD}",
        f"- limit: {args.limit}",
        f"- apply: {args.apply}",
        f"- pool_size: {len(pool)}",
        f"- selected: {len(candidates)}",
        f"- skipped_existing: {skipped_existing}",
        f"- skipped_low_score: {skipped_low_score}",
        f"- skipped_no_ref: {skipped_no_ref}",
        "",
        "说明：verified 仅表示来源追溯链路通过，不代表医学真实性、临床适用性或针灸操作指导。",
        "",
        "| item_id | name | score | source_file | page |",
        "|---------|------|-------|-------------|------|",
    ]
    for c in candidates:
        lines.append(f"| {c['item_id']} | {c['name']} | {c['quality_score']} | {c['source_file']} | {c['page_num']} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "apply": args.apply,
        "threshold": THRESHOLD,
        "limit": args.limit,
        "pool_size": len(pool),
        "selected": len(candidates),
        "skipped_existing": skipped_existing,
        "skipped_low_score": skipped_low_score,
        "skipped_no_ref": skipped_no_ref,
        "report": str(REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
