#!/usr/bin/env python3
"""P29/P5-D resolve remaining candidate_contextual rows.

For rows where index/frontmatter say no_source_found but completeness still says
candidate_contextual, prefer the trace registry/frontmatter/index state and demote
to no_source. No medical content changes.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p29_candidate_contextual_resolution.md"
POLICY = "source_quality_is_traceability_only_not_medical_validation"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def main() -> int:
    herb_index = {r.get("herb_id"): r for r in load_jsonl(DATA / "herb_index.jsonl")}
    decisions = []
    rows = load_jsonl(DATA / "knowledge_completeness.jsonl")
    for row in rows:
        if row.get("source_quality_level") != "candidate_contextual":
            continue
        if row.get("kind") == "herb":
            idx = herb_index.get(row.get("item_id"))
            if idx and idx.get("trace_status") == "no_source_found" and idx.get("source_quality_level") == "no_source":
                old = dict(row)
                row["trace_status"] = "no_source_found"
                row["frontmatter_trace_status"] = "no_source_found"
                row["verified_in_registry"] = False
                row["review_status"] = "needs_source"
                row["quality_tier"] = "needs_source"
                row["has_source_refs"] = False
                row["source_quality_level"] = "no_source"
                row["source_quality_policy"] = POLICY
                row["source_policy"] = "p5d_resolved_to_index_frontmatter_no_source"
                row["p5d_resolution"] = "candidate_contextual contradicted index/frontmatter no_source_found; demoted to no_source"
                decisions.append({
                    "kind": row.get("kind"),
                    "item_id": row.get("item_id"),
                    "name": row.get("name"),
                    "from_trace_status": old.get("trace_status"),
                    "to_trace_status": row.get("trace_status"),
                    "from_source_quality_level": old.get("source_quality_level"),
                    "to_source_quality_level": row.get("source_quality_level"),
                    "reason": row.get("p5d_resolution"),
                })
    write_jsonl(DATA / "knowledge_completeness.jsonl", rows)

    counts = Counter(d["to_source_quality_level"] for d in decisions)
    lines = [
        "# P29 / P5-D candidate_contextual Resolution",
        "",
        "本报告记录对剩余 `candidate_contextual` 的处理。",
        "",
        "> 边界：只同步来源治理状态，不改写医学内容，不判断医学真实性或疗效。",
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
