#!/usr/bin/env python3
"""P39/P7-B-D create high-risk external-source safety review template.

No medical content or external references are imported. This marks high-risk
no_source rows with required review fields for future human validation.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
QUEUE = DATA / "p39_high_risk_external_review_queue.jsonl"
REPORT = ROOT / "report" / "p39_high_risk_safety_review_template.md"
POLICY = "source_quality_is_traceability_only_not_medical_validation"

REQUIRED_SAFETY_FIELDS = [
    "toxicity_profile",
    "contraindications",
    "pregnancy_lactation_warning",
    "pediatric_warning",
    "dose_range_source_required",
    "processing_method_if_applicable",
    "drug_interaction_or_modern_caution",
    "legal_or_restricted_status",
    "emergency_red_flags",
    "reviewer",
    "review_status",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def main() -> int:
    comp = load_jsonl(DATA / "knowledge_completeness.jsonl")
    extq = load_jsonl(DATA / "p36_external_source_queue.jsonl")
    high_keys = {(r.get("kind"), r.get("item_id")) for r in extq if r.get("risk_tier") == "high"}
    high = []
    for row in comp:
        key = (row.get("kind"), row.get("item_id"))
        if key not in high_keys:
            continue
        row["p7bd_high_risk_review_required"] = True
        row["p7bd_required_safety_fields"] = REQUIRED_SAFETY_FIELDS
        row["p7bd_review_status"] = "pending_human_review"
        row["p7bd_promotion_blocker"] = "cannot_promote_or_add_external_medical_content_without_required_safety_fields"
        row["source_quality_policy"] = POLICY
        high.append({
            "kind": row.get("kind"),
            "item_id": row.get("item_id"),
            "name": row.get("name"),
            "file": row.get("file"),
            "p7b_category": row.get("p7b_category"),
            "risk_tier": row.get("risk_tier"),
            "required_safety_fields": REQUIRED_SAFETY_FIELDS,
            "review_status": "pending_human_review",
            "promotion_blocker": row["p7bd_promotion_blocker"],
        })
    write_jsonl(DATA / "knowledge_completeness.jsonl", comp)
    write_jsonl(QUEUE, high)

    # Sync p30 and p36 queues.
    comp_by_key = {(r.get("kind"), r.get("item_id")): r for r in comp}
    for path in [DATA / "p30_no_source_classification.jsonl", DATA / "p36_external_source_queue.jsonl"]:
        rows = load_jsonl(path)
        for r in rows:
            c = comp_by_key.get((r.get("kind"), r.get("item_id")))
            if c and c.get("p7bd_high_risk_review_required"):
                r["p7bd_high_risk_review_required"] = True
                r["p7bd_required_safety_fields"] = REQUIRED_SAFETY_FIELDS
                r["p7bd_review_status"] = "pending_human_review"
                r["p7bd_promotion_blocker"] = c["p7bd_promotion_blocker"]
        write_jsonl(path, rows)

    counts = Counter(r["p7b_category"] for r in high)
    lines = [
        "# P39 / P7-B-D High-risk Safety Review Template",
        "",
        "> 边界：不引入外部正文，不补写医学内容；仅为 high-risk no_source 行设置未来人工复核必填字段。",
        "",
        f"- High-risk rows: {len(high)}",
        "",
        "## By category",
        "",
        "| category | count |",
        "|---|---:|",
    ]
    for k,v in sorted(counts.items()): lines.append(f"| `{k}` | {v} |")
    lines += ["", "## Required safety fields", ""]
    for f in REQUIRED_SAFETY_FIELDS: lines.append(f"- `{f}`")
    lines += ["", "## Queue", ""]
    for r in high: lines.append(f"- `{r['kind']}:{r['item_id']}` {r['name']} — `{r['p7b_category']}`")
    REPORT.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(json.dumps({"high_risk_rows": len(high), "by_category": dict(counts), "queue": str(QUEUE.relative_to(ROOT)), "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
