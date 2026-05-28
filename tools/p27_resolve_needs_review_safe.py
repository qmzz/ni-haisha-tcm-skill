#!/usr/bin/env python3
"""P27/P5-B safely resolve part of needs_review.

Resolution policy:
- Empty quote: demote to no_source_found/no_source because there is no traceable quote.
- Name mismatch caused only by duplicate suffixes like 二/三/外 and quote contains base name: verified_alias.
- Dirty quote that still contains the item name: keep needs_review for manual source re-extraction.
- Other mismatch/dirty rows stay needs_review.

No medical content changes.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p27_needs_review_safe_resolution.md"
POLICY = "source_quality_is_traceability_only_not_medical_validation"

INDEX_FILES = [
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def base_name(name: str) -> str:
    for suffix in ["二", "三", "外"]:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def quote_text(row: dict[str, Any]) -> str:
    refs = row.get("source_refs") or []
    return "\n".join((r.get("quote") or "") for r in refs[:3]).strip()


def classify_resolution(row: dict[str, Any]) -> tuple[str, str, str]:
    seg = row.get("p5b_review_segment") or ""
    name = row.get("name") or ""
    quote = quote_text(row)
    b = base_name(name)
    if seg == "empty_quote":
        return "no_source_found", "no_source", "empty_quote_demoted_to_no_source"
    if seg == "name_mismatch" and b and b != name and b in quote:
        return "verified", "verified_alias", "duplicate_suffix_base_name_match"
    return "verified", "needs_review", "manual_review_required"


def main() -> int:
    verified = load_jsonl(DATA / "verified_sources.jsonl")
    decisions = []
    by_key = {}
    for row in verified:
        if row.get("source_quality_level") == "needs_review":
            trace_status, level, reason = classify_resolution(row)
            if level != row.get("source_quality_level") or trace_status != row.get("trace_status"):
                decisions.append({
                    "kind": row.get("kind"),
                    "item_id": row.get("item_id"),
                    "name": row.get("name"),
                    "from_trace_status": row.get("trace_status"),
                    "to_trace_status": trace_status,
                    "from_source_quality_level": row.get("source_quality_level"),
                    "to_source_quality_level": level,
                    "reason": reason,
                })
            row["trace_status"] = trace_status
            row["source_quality_level"] = level
            row["source_quality_policy"] = POLICY
            row["p5b_resolution"] = reason
            if level == "no_source":
                row["source_refs"] = []
                row["review_status"] = "needs_source"
        by_key[(row.get("kind"), row.get("item_id"))] = row
    write_jsonl(DATA / "verified_sources.jsonl", verified)

    # Sync indexes
    for kind, id_key, path in INDEX_FILES:
        rows = load_jsonl(path)
        for row in rows:
            key = (kind, row.get(id_key))
            if key in by_key:
                v = by_key[key]
                row["trace_status"] = v.get("trace_status")
                row["source_quality_level"] = v.get("source_quality_level")
                row["source_quality_policy"] = POLICY
                row["source_refs"] = v.get("source_refs", [])
                for k in ["p5a_review_reason", "p5b_review_segment", "p5b_review_segment_reason", "p5b_resolution"]:
                    if v.get(k):
                        row[k] = v[k]
        write_jsonl(path, rows)

    # Sync completeness
    rows = load_jsonl(DATA / "knowledge_completeness.jsonl")
    for row in rows:
        key = (row.get("kind"), row.get("item_id"))
        if key in by_key:
            v = by_key[key]
            row["trace_status"] = v.get("trace_status")
            row["source_quality_level"] = v.get("source_quality_level")
            row["source_quality_policy"] = POLICY
            row["verified_in_registry"] = v.get("trace_status") == "verified"
            row["has_source_refs"] = bool(v.get("source_refs"))
            if v.get("p5b_resolution"):
                row["p5b_resolution"] = v["p5b_resolution"]
    write_jsonl(DATA / "knowledge_completeness.jsonl", rows)

    counts = Counter(d["to_source_quality_level"] for d in decisions)
    lines = [
        "# P27 / P5-B needs_review Safe Resolution",
        "",
        "本报告记录对 P26 队列中可安全机械处理部分的处理结果。",
        "",
        "> 边界：不改写医学内容；只调整无来源/重复后缀 alias 等来源关系状态。",
        "",
        f"- Decisions: {len(decisions)}",
        "",
        "## Decisions by target level",
        "",
        "| target | count |",
        "|---|---:|",
    ]
    for level, count in sorted(counts.items()):
        lines.append(f"| `{level}` | {count} |")
    lines += ["", "## Decision list", ""]
    for d in decisions:
        lines.append(f"- `{d['kind']}:{d['item_id']}` {d['name']} — `{d['from_source_quality_level']}` → `{d['to_source_quality_level']}` ({d['reason']})")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"decisions": len(decisions), "by_target_level": dict(counts), "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
