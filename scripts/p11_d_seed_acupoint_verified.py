#!/usr/bin/env python3
"""P11-D: acupoint 高置信 candidate verified 第二阶段。

约束：
- 固定白名单 30 条
- 条件：source_ref quality_score >=80 且 quote 直接包含穴位中文名
- 不改医学正文
- verified 仅表示来源追溯链路通过，不代表医学真实性或针灸操作指导
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
REPORT = ROOT / "report" / "p11_d_acupoint_verified_batch_report.md"
REVIEWER = "p11_d_acupoint_direct_quote_batch"
THRESHOLD = 80

ITEMS = [
    "xuanzhong_gb", "yamen", "yangbai", "yangchi", "yangfu", "yanggu", "yangjiao", "yanglao",
    "yangxi", "yifeng", "yindu", "yinlian", "yongquan_k", "yuji", "yunmen", "zanzhu",
    "zhangmen", "zhaohai", "zhaohai_k", "zhejin", "zhigou", "zhishi", "zhishi_bl", "zhiyin",
    "zhongdu_gb", "zhongfu", "zhongji", "zhongting", "zigong", "zigong_ex",
]


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
    args = parser.parse_args()

    acupoint_rows = {r["acupoint_id"]: r for r in load_jsonl(DATA / "acupoint_index.jsonl") if r.get("acupoint_id")}
    decisions = load_jsonl(DATA / "review_decisions.jsonl")
    existing = {(d.get("kind"), d.get("item_id"), d.get("decision")) for d in decisions}

    candidates = []
    skipped_existing = 0
    skipped_not_found = 0
    skipped_not_candidate = 0
    skipped_no_ref = 0
    skipped_low_score = 0
    skipped_quote_not_direct = 0

    for item_id in ITEMS:
        if ("acupoint", item_id, "verified") in existing:
            skipped_existing += 1
            continue
        row = acupoint_rows.get(item_id)
        if not row:
            skipped_not_found += 1
            continue
        if row.get("trace_status") != "candidate":
            skipped_not_candidate += 1
            continue
        ref = best_source_ref(row)
        if not ref:
            skipped_no_ref += 1
            continue
        score = ref.get("quality_score") or 0
        if score < THRESHOLD:
            skipped_low_score += 1
            continue
        quote = ref.get("quote") or ""
        name = row.get("name") or ""
        if name not in quote:
            skipped_quote_not_direct += 1
            continue

        candidates.append({
            "kind": "acupoint",
            "item_id": item_id,
            "name": name,
            "file": row.get("file"),
            "decision": "verified",
            "source_file": ref.get("source_file"),
            "page_num": ref.get("page_num"),
            "quote": quote[:500],
            "reviewer": REVIEWER,
            "reviewed_at": date.today().isoformat(),
            "notes": "P11-D acupoint direct-quote fixed whitelist; source_ref quality_score >=80 and quote contains canonical Chinese name; traceability only, not medical validation.",
            "quality_score": score,
            "match_reason": ref.get("match_reason") or [],
            "risk_flags": ref.get("risk_flags") or [],
        })

    if args.apply and candidates:
        decisions.extend(candidates)
        write_jsonl(DATA / "review_decisions.jsonl", decisions)

    REPORT.parent.mkdir(exist_ok=True)
    lines = [
        "# P11-D acupoint 高置信 direct-quote verified 第二阶段",
        "",
        f"- whitelist: {len(ITEMS)}",
        f"- threshold: {THRESHOLD}",
        f"- apply: {args.apply}",
        f"- added: {len(candidates)}",
        f"- skipped_existing: {skipped_existing}",
        f"- skipped_not_found: {skipped_not_found}",
        f"- skipped_not_candidate: {skipped_not_candidate}",
        f"- skipped_no_ref: {skipped_no_ref}",
        f"- skipped_low_score: {skipped_low_score}",
        f"- skipped_quote_not_direct: {skipped_quote_not_direct}",
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
        "whitelist": len(ITEMS),
        "added": len(candidates),
        "skipped_existing": skipped_existing,
        "skipped_not_found": skipped_not_found,
        "skipped_not_candidate": skipped_not_candidate,
        "skipped_no_ref": skipped_no_ref,
        "skipped_low_score": skipped_low_score,
        "skipped_quote_not_direct": skipped_quote_not_direct,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
