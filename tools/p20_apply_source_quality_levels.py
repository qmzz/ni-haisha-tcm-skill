#!/usr/bin/env python3
"""P20/P1 apply source_quality_level across trace registry files.

Adds source-chain quality fields to registry/index/completeness/review rows.
This is traceability governance only; it does not validate medical truth or
rewrite medical content.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p20_source_quality_rollout.md"

import sys
sys.path.insert(0, str(ROOT))
from internal.source_quality import classify_source_quality

INDEX_FILES = [
    ("formula", "formula_id", DATA / "formula_index.jsonl"),
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]
POLICY = "source_quality_is_traceability_only_not_medical_validation"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def apply_level(row: dict[str, Any], kind: str, id_key: str | None = None) -> str:
    name = row.get("name") or row.get("target_title") or ""
    status = row.get("trace_status") or row.get("review_status") or ""
    refs = row.get("source_refs") or []
    if not refs and row.get("top_source"):
        refs = [row["top_source"]]
    level = classify_source_quality(kind, name, status, refs, notes=row.get("notes", ""))
    row["source_quality_level"] = level
    row["source_quality_policy"] = POLICY
    return level


def main() -> int:
    changed = {}
    counters: dict[str, Counter] = defaultdict(Counter)

    verified = load_jsonl(DATA / "verified_sources.jsonl")
    verified_by_key = {}
    for row in verified:
        kind = row.get("kind") or ""
        level = apply_level(row, kind)
        verified_by_key[(kind, row.get("item_id"))] = row
        counters["verified_sources"][level] += 1
    write_jsonl(DATA / "verified_sources.jsonl", verified)
    changed["verified_sources.jsonl"] = len(verified)

    # Apply to indexes and sync source_quality from verified registry where present.
    for kind, id_key, path in INDEX_FILES:
        rows = load_jsonl(path)
        for row in rows:
            key = (kind, row.get(id_key))
            if row.get("trace_status") == "no_source_found":
                row["source_refs"] = []
                row["source_quality_level"] = "no_source"
                row["source_quality_policy"] = POLICY
            elif key in verified_by_key:
                verified_row = verified_by_key[key]
                row["trace_status"] = "verified"
                row["source_refs"] = verified_row.get("source_refs", row.get("source_refs", []))
                row["source_quality_level"] = verified_row.get("source_quality_level")
                row["source_quality_policy"] = POLICY
            else:
                apply_level(row, kind, id_key)
            counters[path.name][row["source_quality_level"]] += 1
        write_jsonl(path, rows)
        changed[path.name] = len(rows)

    completeness = load_jsonl(DATA / "knowledge_completeness.jsonl")
    for row in completeness:
        kind = row.get("kind") or ""
        key = (kind, row.get("item_id"))
        if row.get("trace_status") == "no_source_found":
            row["verified_in_registry"] = False
            row["has_source_refs"] = False
            row["source_quality_level"] = "no_source"
        elif key in verified_by_key:
            verified_row = verified_by_key[key]
            row["trace_status"] = "verified"
            row["verified_in_registry"] = True
            row["has_source_refs"] = bool(verified_row.get("source_refs"))
            row["source_quality_level"] = verified_row.get("source_quality_level")
        else:
            row["source_quality_level"] = classify_source_quality(
                kind, row.get("name") or "", row.get("trace_status") or "", [], notes=row.get("source_policy", "")
            )
        row["source_quality_policy"] = POLICY
        counters["knowledge_completeness"][row["source_quality_level"]] += 1
    write_jsonl(DATA / "knowledge_completeness.jsonl", completeness)
    changed["knowledge_completeness.jsonl"] = len(completeness)

    review = load_jsonl(DATA / "review_queue.jsonl")
    for row in review:
        apply_level(row, row.get("kind") or "")
        counters["review_queue"][row["source_quality_level"]] += 1
    write_jsonl(DATA / "review_queue.jsonl", review)
    changed["review_queue.jsonl"] = len(review)

    lines = [
        "# P20 / P1 Source Quality Rollout",
        "",
        "本报告记录 P1 将 source quality 分级从文档说明落地到数据行的结果。",
        "",
        "> 边界：source_quality_level 只描述资料链路可信度，不代表医学真实性、临床适用性、疗效或治疗建议。",
        "",
        "## Changed files",
        "",
    ]
    for name, count in changed.items():
        lines.append(f"- `data/{name}`: {count} rows")
    lines += ["", "## Distribution", ""]
    for bucket, counter in counters.items():
        lines.append(f"### {bucket}")
        lines.append("")
        lines.append("| source_quality_level | count |")
        lines.append("|---|---:|")
        for level, count in sorted(counter.items()):
            lines.append(f"| `{level}` | {count} |")
        lines.append("")
    lines += [
        "## Rules applied",
        "",
        "- `verified_direct`: verified row with source quote that appears to discuss the item directly.",
        "- `verified_contextual`: verified row with source refs but quote appears contextual or insufficiently direct.",
        "- `verified_alias`: verified row involving alias/异名/别名 risk or notes.",
        "- `candidate_direct/contextual/alias`: candidate rows with analogous relation quality; still require review.",
        "- `no_source`: no source refs or explicit no_source_found.",
        "- `needs_review`: review queue entries or unresolved source relationship.",
        "",
        "## Next P1 work",
        "",
        "- Expose source_quality_level in trace/lookup outputs.",
        "- Add registry consistency tests for mandatory source_quality_level.",
        "- Audit registry/index/frontmatter conflicts using the new field.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"changed": changed, "report": str(REPORT.relative_to(ROOT)), "distribution": {k: dict(v) for k, v in counters.items()}}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
