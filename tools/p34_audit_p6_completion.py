#!/usr/bin/env python3
"""Audit P6 no_source governance completion."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p34_p6_completion_audit.md"


def load_jsonl(path: Path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    comp = load_jsonl(DATA / "knowledge_completeness.jsonl")
    queue = load_jsonl(DATA / "p30_no_source_classification.jsonl")
    ns = [r for r in comp if r.get("source_quality_level") == "no_source"]
    problems = []
    qkeys = {(r.get("kind"), r.get("item_id")) for r in queue}
    nskeys = {(r.get("kind"), r.get("item_id")) for r in ns}
    if qkeys != nskeys:
        problems.append({"type": "queue_mismatch", "missing_in_queue": sorted(nskeys - qkeys), "extra_in_queue": sorted(qkeys - nskeys)})
    for r in ns:
        key = (r.get("kind"), r.get("item_id"))
        for field in ["no_source_classification", "no_source_reason", "next_action", "external_source_policy_version", "external_source_status", "source_scope"]:
            if not r.get(field):
                problems.append({"type": "missing_field", "key": key, "field": field})
    counts = Counter(r.get("source_quality_level") for r in comp)
    ns_counts = Counter(r.get("no_source_classification") for r in ns)
    output = {"problems": len(problems), "source_quality_levels": dict(counts), "remaining_no_source_by_classification": dict(ns_counts), "queue_rows": len(queue), "report": str(REPORT.relative_to(ROOT))}
    lines = [
        "# P34 / P6 Completion Audit",
        "",
        f"- Problems: {len(problems)}",
        f"- Queue rows: {len(queue)}",
        "",
        "## Source quality levels",
        "",
        "| level | count |",
        "|---|---:|",
    ]
    for k, v in sorted(counts.items()):
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "## Remaining no_source by classification", "", "| classification | count |", "|---|---:|"]
    for k, v in sorted(ns_counts.items()):
        lines.append(f"| `{k}` | {v} |")
    if problems:
        lines += ["", "## Problems", ""]
        for p in problems[:100]:
            lines.append(f"- `{p}`")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 1 if problems else 0

if __name__ == "__main__":
    raise SystemExit(main())
