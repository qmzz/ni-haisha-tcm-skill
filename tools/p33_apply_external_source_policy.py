#!/usr/bin/env python3
"""P33/P6-D apply external-source governance markers to remaining no_source rows.

No source promotion and no medical content changes.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p33_external_source_policy.md"
POLICY_PATH = DATA / "external_source_policy.json"
QUALITY_POLICY = "source_quality_is_traceability_only_not_medical_validation"

INDEX_FILES = [
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def main() -> int:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    next_map = policy["next_action_map"]
    comp = load_jsonl(DATA / "knowledge_completeness.jsonl")
    decisions = []
    for row in comp:
        if row.get("source_quality_level") != "no_source":
            continue
        cls = row.get("no_source_classification")
        row["external_source_policy_version"] = policy["policy_version"]
        row["source_scope"] = "nihaixia_corpus_not_found"
        row["source_quality_policy"] = QUALITY_POLICY
        row["external_source_allowed_scopes"] = policy["allowed_external_source_scopes"]
        row["next_action"] = next_map.get(cls, "manual_review_required")
        if cls == "external_source_required":
            row["external_source_status"] = "policy_required_before_any_content_expansion"
            row["no_source_reason"] = "Current Ni corpus has no traceable source; future expansion requires whitelisted external source_refs and manual review"
        elif cls == "internal_research_exhausted":
            row["external_source_status"] = "eligible_for_manual_review_or_external_source_policy"
            row["no_source_reason"] = "P6-C raw Ni corpus re-search exhausted without reliable source_refs"
        elif cls == "alias_or_duplicate_mapped":
            row["external_source_status"] = "canonical_mapping_recorded_but_canonical_no_source"
            row["no_source_reason"] = "P6-B canonical mapping recorded; canonical item still has no traceable source_refs"
        else:
            row["external_source_status"] = "manual_review_required"
        decisions.append({
            "kind": row.get("kind"),
            "item_id": row.get("item_id"),
            "name": row.get("name"),
            "classification": cls,
            "external_source_status": row.get("external_source_status"),
            "next_action": row.get("next_action"),
        })
    write_jsonl(DATA / "knowledge_completeness.jsonl", comp)
    comp_by_key = {(r.get("kind"), r.get("item_id")): r for r in comp}

    for kind, id_key, path in INDEX_FILES:
        rows = load_jsonl(path)
        for row in rows:
            c = comp_by_key.get((kind, row.get(id_key)))
            if c and c.get("source_quality_level") == "no_source":
                for f in [
                    "external_source_policy_version", "source_scope", "external_source_allowed_scopes",
                    "external_source_status", "next_action", "no_source_reason", "source_quality_policy",
                ]:
                    row[f] = c.get(f)
        write_jsonl(path, rows)

    # Refresh no_source queue with policy markers.
    queue = []
    for row in comp:
        if row.get("source_quality_level") == "no_source":
            queue.append({
                "kind": row.get("kind"),
                "item_id": row.get("item_id"),
                "name": row.get("name"),
                "file": row.get("file"),
                "no_source_classification": row.get("no_source_classification"),
                "no_source_reason": row.get("no_source_reason"),
                "next_action": row.get("next_action"),
                "canonical_item_id": row.get("canonical_item_id"),
                "p6c_resolution": row.get("p6c_resolution"),
                "external_source_policy_version": row.get("external_source_policy_version"),
                "external_source_status": row.get("external_source_status"),
                "source_scope": row.get("source_scope"),
            })
    write_jsonl(DATA / "p30_no_source_classification.jsonl", queue)

    counts = Counter(d["classification"] for d in decisions)
    status_counts = Counter(d["external_source_status"] for d in decisions)
    lines = [
        "# P33 / P6-D External Source Policy",
        "",
        "本报告记录对剩余 no_source 行应用外部来源治理策略。",
        "",
        "> 边界：P6-D 不引入外部来源，不补写医学内容，不做医学真实性/疗效判断；只规定未来补源所需白名单、字段与人工复核要求。",
        "",
        f"- Remaining no_source rows governed: {len(decisions)}",
        f"- Policy file: `{POLICY_PATH.relative_to(ROOT)}`",
        "",
        "## By classification",
        "",
        "| classification | count |",
        "|---|---:|",
    ]
    for k, v in sorted(counts.items()):
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "## By external_source_status", "", "| status | count |", "|---|---:|"]
    for k, v in sorted(status_counts.items()):
        lines.append(f"| `{k}` | {v} |")
    lines += [
        "",
        "## Required future external source fields",
        "",
    ]
    for f in policy["required_fields_for_future_external_source_ref"]:
        lines.append(f"- `{f}`")
    lines += [
        "",
        "## Forbidden without manual review",
        "",
    ]
    for f in policy["forbidden_actions_without_manual_review"]:
        lines.append(f"- {f}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"governed": len(decisions), "by_classification": dict(counts), "report": str(REPORT.relative_to(ROOT)), "policy": str(POLICY_PATH.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
