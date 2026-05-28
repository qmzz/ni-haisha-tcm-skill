#!/usr/bin/env python3
"""Audit P7-B external-source review queue consistency."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p37_external_source_queue_audit.md"
REQUIRED = ["p7b_category", "p7b_phase", "risk_tier", "recommended_source_scopes", "required_review"]


def load_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    comp = load_jsonl(DATA / "knowledge_completeness.jsonl")
    queue = load_jsonl(DATA / "p36_external_source_queue.jsonl")
    ns = [r for r in comp if r.get("source_quality_level") == "no_source"]
    problems = []
    ns_keys = {(r.get("kind"), r.get("item_id")) for r in ns}
    q_keys = {(r.get("kind"), r.get("item_id")) for r in queue}
    if ns_keys != q_keys:
        problems.append({"type":"queue_key_mismatch", "missing": sorted(ns_keys-q_keys), "extra": sorted(q_keys-ns_keys)})
    for r in ns:
        for f in REQUIRED:
            if not r.get(f):
                problems.append({"type":"missing_comp_field", "key": (r.get("kind"), r.get("item_id")), "field": f})
    for r in queue:
        for f in ["kind","item_id","name",*REQUIRED]:
            if not r.get(f):
                problems.append({"type":"missing_queue_field", "key": (r.get("kind"), r.get("item_id")), "field": f})
        if r.get("required_review") != "manual_review_required_before_content_or_quality_promotion":
            problems.append({"type":"review_policy_violation", "key": (r.get("kind"), r.get("item_id"))})
    cats=Counter(r.get("p7b_category") for r in queue)
    phases=Counter(r.get("p7b_phase") for r in queue)
    risks=Counter(r.get("risk_tier") for r in queue)
    lines=["# P37 / P7-B External Source Queue Audit","",f"- Problems: {len(problems)}",f"- Queue rows: {len(queue)}","","## Category counts","","| category | count |","|---|---:|"]
    for k,v in sorted(cats.items()): lines.append(f"| `{k}` | {v} |")
    lines += ["","## Phase counts","","| phase | count |","|---|---:|"]
    for k,v in sorted(phases.items()): lines.append(f"| `{k}` | {v} |")
    lines += ["","## Risk counts","","| risk | count |","|---|---:|"]
    for k,v in sorted(risks.items()): lines.append(f"| `{k}` | {v} |")
    if problems:
        lines += ["", "## Problems", ""]
        for p in problems[:100]: lines.append(f"- `{p}`")
    REPORT.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(json.dumps({"problems": len(problems), "queue_rows": len(queue), "by_category": dict(cats), "by_phase": dict(phases), "by_risk": dict(risks), "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 1 if problems else 0

if __name__ == "__main__": raise SystemExit(main())
