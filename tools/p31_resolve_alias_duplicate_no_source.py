#!/usr/bin/env python3
"""P31/P6-B resolve alias_or_duplicate_needs_mapping no_source queue.

No medical content changes. Creates canonical mappings for duplicate/variant
no_source items and updates classification metadata. Only promotes when a verified
canonical item exists; otherwise keeps no_source but records duplicate mapping.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p31_alias_duplicate_no_source_resolution.md"
POLICY = "source_quality_is_traceability_only_not_medical_validation"

# canonical_id values are conservative registry mappings, not medical claims.
CANONICAL = {
    ("herb", "biba"): "bichengqie",        # duplicate name 荜澄茄
    ("herb", "bichengqie"): "bichengqie",  # canonical placeholder remains no_source
    ("herb", "hechezi"): "heizhima",       # duplicate name 黑芝麻
    ("herb", "heizhima"): "heizhima",      # canonical placeholder remains no_source
    ("herb", "hezi"): "hesi",              # duplicate name 鹤虱
    ("herb", "luobuma"): "luobumaye",      # duplicate name 罗布麻叶
    ("acupoint", "fuyang2"): "fuyang_bl",  # 跗阳 duplicate maps to verified canonical
    ("acupoint", "yaoyangguan"): "yangguan", # duplicate name 腰阳关; canonical still no_source
    ("acupoint", "yinjiao_ren"): "yinjiao",  # 阴交二 likely name variant; canonical 龈交 is verified, keep alias marker
}

INDEX_FILES = [
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def main() -> int:
    comp = load_jsonl(DATA / "knowledge_completeness.jsonl")
    idx_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    index_rows: dict[Path, list[dict[str, Any]]] = {}
    for kind, id_key, path in INDEX_FILES:
        rows = load_jsonl(path)
        index_rows[path] = rows
        for row in rows:
            idx_by_key[(kind, row.get(id_key))] = row

    decisions = []
    for row in comp:
        if row.get("source_quality_level") != "no_source":
            continue
        key = (row.get("kind"), row.get("item_id"))
        if key not in CANONICAL:
            continue
        canonical_id = CANONICAL[key]
        canonical = idx_by_key.get((key[0], canonical_id))
        row["canonical_item_id"] = canonical_id
        row["no_source_classification"] = "alias_or_duplicate_mapped"
        row["no_source_reason"] = "P6-B mapped duplicate/variant item to canonical registry id; no medical content changed"
        row["next_action"] = "review_canonical_source_status"
        row["source_quality_policy"] = POLICY
        if canonical and canonical.get("trace_status") == "verified":
            row["trace_status"] = "verified"
            row["source_quality_level"] = "verified_alias"
            row["verified_in_registry"] = True
            row["has_source_refs"] = bool(canonical.get("source_refs"))
            row["p6b_resolution"] = "mapped_to_verified_canonical_as_alias"
        else:
            row["trace_status"] = "no_source_found"
            row["source_quality_level"] = "no_source"
            row["verified_in_registry"] = False
            row["p6b_resolution"] = "mapped_to_canonical_but_canonical_is_no_source"
        decisions.append({
            "kind": key[0],
            "item_id": key[1],
            "name": row.get("name"),
            "canonical_item_id": canonical_id,
            "canonical_status": canonical.get("trace_status") if canonical else None,
            "to_source_quality_level": row.get("source_quality_level"),
            "resolution": row.get("p6b_resolution"),
        })

    write_jsonl(DATA / "knowledge_completeness.jsonl", comp)

    # Sync index rows from completeness mapping.
    comp_by_key = {(r.get("kind"), r.get("item_id")): r for r in comp}
    for kind, id_key, path in INDEX_FILES:
        rows = index_rows[path]
        for row in rows:
            key = (kind, row.get(id_key))
            c = comp_by_key.get(key)
            if not c:
                continue
            for field in ["canonical_item_id", "no_source_classification", "no_source_reason", "next_action", "p6b_resolution"]:
                if c.get(field):
                    row[field] = c[field]
            if c.get("p6b_resolution"):
                row["trace_status"] = c.get("trace_status")
                row["source_quality_level"] = c.get("source_quality_level")
                row["source_quality_policy"] = POLICY
                if c.get("source_quality_level") == "verified_alias":
                    canonical = idx_by_key.get((kind, c.get("canonical_item_id")))
                    row["source_refs"] = canonical.get("source_refs", []) if canonical else []
                elif c.get("source_quality_level") == "no_source":
                    row["source_refs"] = []
        write_jsonl(path, rows)

    # Refresh P30 queue from completeness no_source rows only.
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
            })
    write_jsonl(DATA / "p30_no_source_classification.jsonl", queue)

    counter = Counter(d["to_source_quality_level"] for d in decisions)
    lines = [
        "# P31 / P6-B alias_or_duplicate no_source Resolution",
        "",
        "本报告记录 P6-B 对 alias/duplicate no_source 队列的 canonical mapping 处理。",
        "",
        "> 边界：只建立 canonical mapping 与来源治理状态，不改写医学内容，不判断医学真实性或疗效。",
        "",
        f"- Decisions: {len(decisions)}",
        "",
        "## By target source_quality_level",
        "",
        "| target | count |",
        "|---|---:|",
    ]
    for k, v in sorted(counter.items()):
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "## Decision list", ""]
    for d in decisions:
        lines.append(f"- `{d['kind']}:{d['item_id']}` {d['name']} → `{d['canonical_item_id']}`; canonical_status={d['canonical_status']}; target=`{d['to_source_quality_level']}` ({d['resolution']})")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"decisions": len(decisions), "by_target": dict(counter), "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
