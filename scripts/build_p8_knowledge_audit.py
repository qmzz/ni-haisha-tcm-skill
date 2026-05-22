#!/usr/bin/env python3
"""P8-A knowledge completeness audit.

This script audits formula / herb / acupoint markdown entries for governance and
content completeness. It does not modify knowledge files and does not infer any
medical facts. The output is for data-improvement planning only.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from internal.frontmatter import audit_file, parse_frontmatter  # noqa: E402

KINDS = {
    "formula": {
        "folder": ROOT / "knowledge" / "formulas",
        "id_key": "formula_id",
        "index": ROOT / "data" / "formula_index.jsonl",
        "content_checks": {
            "composition": ["## 组成", "**组成", "组成："],
            "indication": ["## 主治", "**主治", "主治："],
            "usage": ["## 用法", "煎服法", "用法："],
            "ni_commentary": ["倪师讲解", "倪海厦"],
            "safety_boundary": ["学习与安全边界", "不构成诊断", "不能替代"],
        },
    },
    "herb": {
        "folder": ROOT / "knowledge" / "herbs",
        "id_key": "herb_id",
        "index": ROOT / "data" / "herb_index.jsonl",
        "content_checks": {
            "properties": ["性味", "四气五味"],
            "meridian": ["归经"],
            "effects": ["功效", "主治"],
            "contraindication": ["禁忌", "慎用", "注意"],
            "ni_commentary": ["倪师", "倪海厦"],
            "safety_boundary": ["学习与安全边界", "不构成诊断", "不能替代"],
        },
    },
    "acupoint": {
        "folder": ROOT / "knowledge" / "acupoints",
        "id_key": "acupoint_id",
        "index": ROOT / "data" / "acupoint_index.jsonl",
        "content_checks": {
            "meridian": ["归经"],
            "location": ["定位", "取穴"],
            "indication": ["主治", "治疗"],
            "safety_boundary": ["学习与安全边界", "不作为针灸操作指导", "不构成诊断"],
            "source_trace_notice": ["来源追溯状态", "source_refs", "追溯状态"],
        },
    },
}


def load_jsonl(path: Path) -> List[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def normalize_status(status: object) -> str:
    if not status:
        return "unknown"
    return str(status)


def title_from_markdown(path: Path, text: str, fm: Dict[str, object]) -> str:
    if fm.get("title"):
        return str(fm["title"]).strip('"\'')
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def item_id_from_path(path: Path) -> str:
    return path.stem


def load_index_maps() -> Dict[Tuple[str, str], dict]:
    maps: Dict[Tuple[str, str], dict] = {}
    for kind, cfg in KINDS.items():
        id_key = cfg["id_key"]
        for row in load_jsonl(cfg["index"]):
            item_id = row.get(id_key) or Path(row.get("file", "")).stem
            if item_id:
                maps[(kind, str(item_id))] = row
    return maps


def load_review_maps() -> Tuple[Dict[Tuple[str, str], dict], Dict[Tuple[str, str], dict]]:
    verified = {}
    for row in load_jsonl(ROOT / "data" / "verified_sources.jsonl"):
        key = (row.get("kind"), row.get("item_id"))
        if all(key):
            verified[(str(key[0]), str(key[1]))] = row
    review = {}
    for row in load_jsonl(ROOT / "data" / "review_queue.jsonl"):
        key = (row.get("kind"), row.get("item_id"))
        if all(key):
            review[(str(key[0]), str(key[1]))] = row
    return verified, review


def has_any(text: str, needles: Iterable[str]) -> bool:
    return any(needle in text for needle in needles)


def quality_tier(trace_status: str, frontmatter_complete: bool, has_source_refs: bool, has_safety_boundary: bool, missing_content: List[str]) -> str:
    if trace_status == "verified" and frontmatter_complete and has_source_refs and has_safety_boundary and not missing_content:
        return "complete"
    if trace_status == "verified" and frontmatter_complete and has_source_refs and has_safety_boundary:
        return "refined"
    if trace_status == "verified":
        return "verified"
    if trace_status in {"candidate", "needs_review"}:
        return "traced"
    return "seed"


def audit_entry(kind: str, path: Path, index_maps: Dict[Tuple[str, str], dict], verified_maps: Dict[Tuple[str, str], dict], review_maps: Dict[Tuple[str, str], dict]) -> dict:
    text = path.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(text)
    item_id = item_id_from_path(path)
    key = (kind, item_id)
    index_row = index_maps.get(key, {})
    verified_row = verified_maps.get(key, {})
    review_row = review_maps.get(key, {})
    fm_audit = audit_file(path, kind)

    index_status = normalize_status(index_row.get("trace_status") or review_row.get("review_status"))
    frontmatter_status = normalize_status(fm.get("trace_status"))
    verified_in_registry = bool(verified_row)
    if verified_in_registry:
        trace_status = "verified"
    elif index_status != "unknown":
        trace_status = index_status
    else:
        trace_status = frontmatter_status
    review_status = normalize_status(fm.get("review_status") or review_row.get("review_status") or trace_status)
    source_refs = fm.get("source_refs") or index_row.get("source_refs") or verified_row.get("source_refs") or []
    has_source_refs = bool(source_refs)

    checks = {}
    for field, needles in KINDS[kind]["content_checks"].items():
        checks[field] = has_any(text, needles)
    missing_content = [field for field, ok in checks.items() if not ok]
    has_safety_boundary = bool(checks.get("safety_boundary")) or bool(fm.get("safety_disclaimer_required"))
    frontmatter_complete = bool(fm) and not fm_audit["missing"] and not fm_audit["warnings"]

    tier = quality_tier(trace_status, frontmatter_complete, has_source_refs, has_safety_boundary, missing_content)
    return {
        "kind": kind,
        "item_id": item_id,
        "name": index_row.get("name") or title_from_markdown(path, text, fm),
        "file": rel(path),
        "trace_status": trace_status,
        "frontmatter_trace_status": frontmatter_status,
        "verified_in_registry": verified_in_registry,
        "review_status": review_status,
        "quality_tier": tier,
        "has_frontmatter": bool(fm),
        "frontmatter_complete": frontmatter_complete,
        "frontmatter_missing": fm_audit["missing"],
        "frontmatter_warnings": fm_audit["warnings"],
        "has_source_refs": has_source_refs,
        "has_safety_boundary": has_safety_boundary,
        "content_checks": checks,
        "missing_content_fields": missing_content,
        "source_policy": "audit_only_not_medical_validation",
    }


def build_rows() -> List[dict]:
    index_maps = load_index_maps()
    verified_maps, review_maps = load_review_maps()
    rows: List[dict] = []
    for kind, cfg in KINDS.items():
        for path in sorted(cfg["folder"].glob("*.md")):
            if "index" in path.name:
                continue
            rows.append(audit_entry(kind, path, index_maps, verified_maps, review_maps))
    return rows


def count_by(rows: List[dict], field: str) -> Dict[str, int]:
    return dict(sorted(Counter(str(row.get(field)) for row in rows).items()))


def kind_summary(rows: List[dict]) -> Dict[str, dict]:
    summary = {}
    for kind in KINDS:
        subset = [row for row in rows if row["kind"] == kind]
        summary[kind] = {
            "total": len(subset),
            "trace_status": count_by(subset, "trace_status"),
            "quality_tier": count_by(subset, "quality_tier"),
            "frontmatter_complete": sum(1 for row in subset if row["frontmatter_complete"]),
            "verified_registry": sum(1 for row in subset if row["verified_in_registry"]),
            "stale_verified_frontmatter": sum(1 for row in subset if row["frontmatter_trace_status"] == "verified" and not row["verified_in_registry"]),
            "has_source_refs": sum(1 for row in subset if row["has_source_refs"]),
            "has_safety_boundary": sum(1 for row in subset if row["has_safety_boundary"]),
        }
    return summary


def content_gap_summary(rows: List[dict]) -> Dict[str, Dict[str, int]]:
    gaps: Dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        for field in row["missing_content_fields"]:
            gaps[row["kind"]][field] += 1
    return {kind: dict(sorted(counter.items())) for kind, counter in gaps.items()}


def write_jsonl(rows: List[dict]) -> None:
    out = ROOT / "data" / "knowledge_completeness.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {out.relative_to(ROOT)}")


def write_report(rows: List[dict]) -> None:
    summary = kind_summary(rows)
    gaps = content_gap_summary(rows)
    total = len(rows)
    verified = sum(1 for row in rows if row["verified_in_registry"])
    stale_verified_frontmatter = sum(1 for row in rows if row["frontmatter_trace_status"] == "verified" and not row["verified_in_registry"])
    frontmatter_complete = sum(1 for row in rows if row["frontmatter_complete"])
    complete = sum(1 for row in rows if row["quality_tier"] == "complete")
    refined = sum(1 for row in rows if row["quality_tier"] == "refined")

    lines = [
        "# P8-A 知识库完整度审计",
        "",
        "## 阶段定位",
        "",
        "P8-A 用于盘点方剂、药材、穴位知识库的治理状态与内容完备度。此报告只做数据治理和补全优先级排序，不判断医学真实性，不生成新的医学结论。",
        "",
        "## 总览",
        "",
        f"- 条目总数：{total}",
        f"- verified 来源链路：{verified}",
        f"- frontmatter 标记 verified 但未进入 registry：{stale_verified_frontmatter}",
        f"- frontmatter 完整：{frontmatter_complete}",
        f"- refined 条目：{refined}",
        f"- complete 条目：{complete}",
        "- 数据明细：`data/knowledge_completeness.jsonl`",
        "",
        "## 按类别统计",
        "",
        "| kind | total | verified_registry | candidate | needs_review | no_source_found | unknown | stale_verified_fm | frontmatter_complete | source_refs | safety_boundary | refined | complete |",
        "|------|-------|-------------------|-----------|--------------|-----------------|---------|-------------------|----------------------|-------------|-----------------|---------|----------|",
    ]
    for kind, item in summary.items():
        ts = item["trace_status"]
        tier = item["quality_tier"]
        lines.append(
            f"| {kind} | {item['total']} | {item['verified_registry']} | {ts.get('candidate', 0)} | {ts.get('needs_review', 0)} | {ts.get('no_source_found', 0)} | {ts.get('unknown', 0)} | {item['stale_verified_frontmatter']} | {item['frontmatter_complete']} | {item['has_source_refs']} | {item['has_safety_boundary']} | {tier.get('refined', 0)} | {tier.get('complete', 0)} |"
        )
    lines.extend(["", "## quality_tier 分布", ""])
    for kind, item in summary.items():
        lines.append(f"### {kind}")
        for tier, count in item["quality_tier"].items():
            lines.append(f"- {tier}: {count}")
        lines.append("")

    lines.extend(["## 内容缺口统计", ""])
    for kind in KINDS:
        lines.append(f"### {kind}")
        if not gaps.get(kind):
            lines.append("- 暂无缺口")
        else:
            for field, count in gaps[kind].items():
                lines.append(f"- {field}: {count}")
        lines.append("")

    lines.extend([
        "## P8-B/P8-C/P8-D 建议",
        "",
        "1. 方剂优先：方剂总量较小，应优先把 verified 与 refined 覆盖继续拉高。",
        "2. 药材分层：药材总量大，建议先做核心 100 味精修，不一次性铺开。",
        "3. 穴位谨慎：穴位涉及操作风险，补全时必须保留“不作为针灸操作指导”的安全边界。",
        "4. no_source_found 继续按 P7 分类结果小批量人工复核，alias hit 不自动 verified。",
        "",
        "## 边界",
        "",
        "- 本报告不凭模型记忆补医学内容。",
        "- `quality_tier` 只代表资料治理完备度，不代表医学真实性或临床适用性。",
        "- `verified` 只表示来源追溯链路通过复核。",
        "- 找不到依据的条目继续保持 `no_source_found` / `needs_review` / `待考` / `待补充`。",
        "",
    ])
    out = ROOT / "report" / "p8_knowledge_audit.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


def main() -> None:
    rows = build_rows()
    write_jsonl(rows)
    write_report(rows)
    summary = kind_summary(rows)
    print(json.dumps({"rows": len(rows), "summary": summary}, ensure_ascii=False))


if __name__ == "__main__":
    main()
