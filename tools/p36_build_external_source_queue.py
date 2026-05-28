#!/usr/bin/env python3
"""P36/P7-B build external-source whitelist and review queues for no_source rows.

No external content is imported here. The output only defines a whitelist,
required fields, risk tiers, and candidate work queues for manual/external source
review.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p36_external_source_queue.md"
QUEUE = DATA / "p36_external_source_queue.jsonl"
POLICY = DATA / "external_source_policy.json"
QUALITY_POLICY = "source_quality_is_traceability_only_not_medical_validation"

HIGH_RISK_HERBS = {
    "leigongteng", "maqianzi", "qianjinzi", "yadanzi", "yangjinhua", "gansui", "daji", "chuanwu", "caowu",
    "luhui", "fanxieye", "liuhuang", "qishe", "zhugensha", "shandougen", "huangyaozi", "tubiechong", "zhechong",
}
ANIMAL_OR_RESTRICTED = {
    "haima", "qishe", "chuanshanjia", "lingyangjiao", "ciweipi", "hamayou", "tubiechong", "zhechong",
}
MODERN_OR_REGIONAL = {
    "aidicha", "banzhilian", "chuipencao", "chouwutong", "diercao", "dijincao", "jinguolan", "jixueteng",
    "luobuma", "luobumaye", "luohanguo", "mabo", "machixian", "mohantian", "pugongying", "yuxingcao", "zihuadiding",
}
ALIAS_FIRST = {
    "biba", "bichengqie", "hechezi", "heizhima", "hezi", "luobuma", "yaoyangguan", "shandou", "aoshu", "aoshugen", "nuodaogenxu",
}
EXTRA_ACU = {"shiqixue", "sishencong", "yaotongdian", "ershenmen", "xiaji"}
STANDARD_ACU = {"liangmen", "tianliao", "touqiaoyin", "xiyangguan", "yanggang", "yangguan", "zutonggu", "zuwuli"}

SOURCE_BUNDLES = {
    "herb_standard": ["official_pharmacopoeia", "modern_tcm_reference", "classical_tcm_text"],
    "herb_high_risk": ["official_pharmacopoeia", "modern_tcm_reference"],
    "herb_animal_or_restricted": ["official_pharmacopoeia", "modern_tcm_reference"],
    "herb_alias": ["official_pharmacopoeia", "modern_tcm_reference"],
    "acupoint_standard": ["acupoint_standard_reference"],
    "acupoint_extra": ["acupoint_standard_reference", "modern_tcm_reference"],
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def category(kind: str, item_id: str, cls: str) -> tuple[str, str, str]:
    if cls == "alias_or_duplicate_mapped" or item_id in ALIAS_FIRST:
        return "alias_first", "P7B-A", "resolve canonical/alias before external sourcing"
    if kind == "acupoint":
        if item_id in EXTRA_ACU or cls == "contextual_false_positive_demoted":
            return "acupoint_extra_or_uncertain", "P7B-C", "extra/uncertain acupoint requires acupoint-standard reference and manual review"
        if item_id in STANDARD_ACU or cls == "internal_research_exhausted":
            return "acupoint_standard", "P7B-B", "standard acupoint candidate; use acupoint standard reference"
        return "acupoint_uncertain", "P7B-C", "uncertain acupoint; manual source review first"
    if item_id in HIGH_RISK_HERBS:
        return "herb_high_risk", "P7B-D", "toxicity/strong action/reproductive risk; external source review must include safety fields"
    if item_id in ANIMAL_OR_RESTRICTED:
        return "herb_animal_or_restricted", "P7B-D", "animal/restricted material; source review must include legal/ethical status"
    if item_id in MODERN_OR_REGIONAL:
        return "herb_modern_or_regional", "P7B-E", "modern/regional materia medica; external source likely required"
    if cls == "internal_research_exhausted":
        return "herb_internal_exhausted", "P7B-F", "not found after Ni corpus re-search; external/reference review next"
    return "herb_standard", "P7B-F", "standard external source candidate"


def source_bundle(cat: str) -> list[str]:
    if cat in {"herb_high_risk"}: return SOURCE_BUNDLES["herb_high_risk"]
    if cat == "herb_animal_or_restricted": return SOURCE_BUNDLES["herb_animal_or_restricted"]
    if cat == "alias_first": return SOURCE_BUNDLES["herb_alias"]
    if cat.startswith("acupoint_standard"): return SOURCE_BUNDLES["acupoint_standard"]
    if cat.startswith("acupoint") : return SOURCE_BUNDLES["acupoint_extra"]
    return SOURCE_BUNDLES["herb_standard"]


def main() -> int:
    comp = load_jsonl(DATA / "knowledge_completeness.jsonl")
    queue = []
    for row in comp:
        if row.get("source_quality_level") != "no_source":
            continue
        kind, item_id, cls = row.get("kind"), row.get("item_id"), row.get("no_source_classification")
        cat, phase, rationale = category(kind, item_id, cls)
        risk = "high" if cat in {"herb_high_risk", "herb_animal_or_restricted"} else ("medium" if cat in {"acupoint_extra_or_uncertain", "acupoint_uncertain", "alias_first"} else "low")
        q = {
            "kind": kind,
            "item_id": item_id,
            "name": row.get("name"),
            "file": row.get("file"),
            "current_classification": cls,
            "p7b_category": cat,
            "p7b_phase": phase,
            "risk_tier": risk,
            "recommended_source_scopes": source_bundle(cat),
            "required_review": "manual_review_required_before_content_or_quality_promotion",
            "rationale": rationale,
            "source_quality_policy": QUALITY_POLICY,
            "external_source_policy_version": row.get("external_source_policy_version"),
            "canonical_item_id": row.get("canonical_item_id"),
        }
        queue.append(q)
        row["p7b_category"] = cat
        row["p7b_phase"] = phase
        row["risk_tier"] = risk
        row["recommended_source_scopes"] = source_bundle(cat)
        row["required_review"] = q["required_review"]
        row["p7b_rationale"] = rationale
    write_jsonl(DATA / "knowledge_completeness.jsonl", comp)
    write_jsonl(QUEUE, queue)

    # refresh p30 queue with p7b markers
    p30=[]
    for row in comp:
        if row.get("source_quality_level") == "no_source":
            p30.append({k: row.get(k) for k in [
                "kind","item_id","name","file","no_source_classification","no_source_reason","next_action",
                "canonical_item_id","p6c_resolution","external_source_policy_version","external_source_status","source_scope",
                "p7a_action","p7b_category","p7b_phase","risk_tier","recommended_source_scopes","required_review",
            ]})
    write_jsonl(DATA / "p30_no_source_classification.jsonl", p30)

    counts = Counter(q["p7b_category"] for q in queue)
    phases = Counter(q["p7b_phase"] for q in queue)
    risks = Counter(q["risk_tier"] for q in queue)
    lines = [
        "# P36 / P7-B External Source Queue",
        "",
        "> 边界：本阶段只建立外部来源白名单与人工复核队列，不引入外部正文，不提升 source_quality_level，不补写医学内容。",
        "",
        f"- Queue rows: {len(queue)}",
        "",
        "## By category",
        "",
        "| category | count |",
        "|---|---:|",
    ]
    for k,v in sorted(counts.items()): lines.append(f"| `{k}` | {v} |")
    lines += ["", "## By phase", "", "| phase | count |", "|---|---:|"]
    for k,v in sorted(phases.items()): lines.append(f"| `{k}` | {v} |")
    lines += ["", "## By risk", "", "| risk | count |", "|---|---:|"]
    for k,v in sorted(risks.items()): lines.append(f"| `{k}` | {v} |")
    lines += ["", "## Source bundles", ""]
    for k,v in SOURCE_BUNDLES.items(): lines.append(f"- `{k}`: {', '.join(v)}")
    REPORT.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(json.dumps({"queue_rows":len(queue),"by_category":dict(counts),"by_phase":dict(phases),"by_risk":dict(risks),"queue":str(QUEUE.relative_to(ROOT)),"report":str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
