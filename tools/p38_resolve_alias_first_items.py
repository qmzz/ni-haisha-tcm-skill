#!/usr/bin/env python3
"""P38/P7-B-A resolve alias_first no_source items.

Maps duplicate/variant no_source items to their canonical ids where a verified
canonical exists. Items without a verified canonical stay no_source but get
explicit alias mapping metadata.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p38_alias_first_resolution.md"
POLICY = "source_quality_is_traceability_only_not_medical_validation"

# Conservative alias mapping (not medical claims, just registry-level naming).
CANONICAL = {
    # Already mapped in P6-B but canonical was no_source. Map all to single canonical.
    ("herb", "biba"): "bichengqie",
    ("herb", "bichengqie"): "bichengqie",
    ("herb", "hechezi"): "heizhima",
    ("herb", "heizhima"): "heizhima",
    ("herb", "hezi"): "hesi",
    ("herb", "luobuma"): "luobumaye",
    ("acupoint", "yaoyangguan"): "yangguan",
    # Duplicate no_source pairs → consolidate to one canonical.
    ("herb", "aoshu"): "nuodaogenxu",       # 糯稻根 → 糯稻根须 (canonical no_source)
    ("herb", "aoshugen"): "nuodaogenxu",    # 糯稻根须 → 糯稻根须
    ("herb", "shandou"): "guya",            # 谷芽 → guya (canonical no_source)
    ("herb", "luobumaye"): "luobumaye",     # self-canonical
    ("herb", "hesi"): "hesi",               # self-canonical
    ("herb", "nuodaogenxu"): "nuodaogenxu",
    ("herb", "guya"): "guya",
    ("acupoint", "yangguan"): "yangguan",
}

INDEX_FILES = [
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def main() -> int:
    comp = load_jsonl(DATA / "knowledge_completeness.jsonl")
    ver = load_jsonl(DATA / "verified_sources.jsonl")
    ver_by_key = {(r.get("kind"), r.get("item_id")): r for r in ver}

    decisions = []
    for row in comp:
        if row.get("source_quality_level") != "no_source":
            continue
        key = (row.get("kind"), row.get("item_id"))
        canonical_id = CANONICAL.get(key)
        if not canonical_id:
            continue
        canonical_key = (key[0], canonical_id)
        canonical_ver = ver_by_key.get(canonical_key)
        canonical_comp = next((r for r in comp if (r.get("kind"), r.get("item_id")) == canonical_key), None)

        row["canonical_item_id"] = canonical_id
        row["p7ba_action"] = "alias_mapped"
        row["p7ba_rationale"] = "P7-B-A: mapped to canonical no_source item for deduplication"
        if canonical_ver and canonical_ver.get("trace_status") == "verified":
            row["trace_status"] = "verified"
            row["source_quality_level"] = "verified_alias"
            row["verified_in_registry"] = True
            row["has_source_refs"] = bool(canonical_ver.get("source_refs"))
            row["source_refs"] = canonical_ver.get("source_refs", [])
            row["p7ba_outcome"] = "promoted_to_verified_alias_via_canonical"
        else:
            row["trace_status"] = "no_source_found"
            row["source_quality_level"] = "no_source"
            row["verified_in_registry"] = False
            row["has_source_refs"] = False
            row["p7ba_outcome"] = "canonical_is_no_source_stays_no_source"
        row["source_quality_policy"] = POLICY
        decisions.append({
            "kind": key[0],
            "item_id": key[1],
            "name": row.get("name"),
            "canonical_item_id": canonical_id,
            "canonical_status": canonical_ver.get("trace_status") if canonical_ver else None,
            "to_quality": row.get("source_quality_level"),
            "p7ba_outcome": row.get("p7ba_outcome"),
        })

    write_jsonl(DATA / "knowledge_completeness.jsonl", comp)

    # Sync indexes.
    comp_by_key = {(r.get("kind"), r.get("item_id")): r for r in comp}
    for kind, id_key, path in INDEX_FILES:
        rows = load_jsonl(path)
        for row in rows:
            c = comp_by_key.get((kind, row.get(id_key)))
            if c and c.get("p7ba_action"):
                for f in ["canonical_item_id","p7ba_action","p7ba_rationale","p7ba_outcome",
                          "trace_status","source_quality_level","source_quality_policy",
                          "verified_in_registry","has_source_refs","source_refs"]:
                    if f in c: row[f] = c[f]
        write_jsonl(path, rows)

    # Refresh verified registry.
    for d in decisions:
        if d["to_quality"] == "verified_alias":
            key = (d["kind"], d["item_id"])
            if key not in ver_by_key:
                c = comp_by_key[key]
                ver.append({k: c.get(k) for k in ["kind","item_id","name","file","trace_status","source_refs","source_quality_level","source_quality_policy","canonical_item_id","p7ba_action"]})
                ver_by_key[key] = ver[-1]
    write_jsonl(DATA / "verified_sources.jsonl", ver)

    # Refresh P30 queue.
    p30 = []
    for r in comp:
        if r.get("source_quality_level") == "no_source":
            p30.append({k: r.get(k) for k in ["kind","item_id","name","file","no_source_classification","no_source_reason","next_action","canonical_item_id","p6c_resolution","external_source_policy_version","external_source_status","source_scope","p7a_action","p7ba_action","p7ba_outcome","p7b_category","p7b_phase","risk_tier"]})
    write_jsonl(DATA / "p30_no_source_classification.jsonl", p30)

    counts = Counter(d["p7ba_outcome"] for d in decisions)
    lines = ["# P38 / P7-B-A alias_first Resolution","","> 边界：只做 registry 级 canonical mapping，不补写医学内容。","",f"- Decisions: {len(decisions)}","","## By outcome","","| outcome | count |","|---|---:|"]
    for k,v in sorted(counts.items()): lines.append(f"| `{k}` | {v} |")
    lines += ["","## Decisions",""]
    for d in decisions: lines.append(f"- `{d['kind']}:{d['item_id']}` {d['name']} → `{d['canonical_item_id']}` ({d['p7ba_outcome']})")
    REPORT.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(json.dumps({"decisions": len(decisions), "by_outcome": dict(counts), "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
