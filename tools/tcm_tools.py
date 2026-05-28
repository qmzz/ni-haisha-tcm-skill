#!/usr/bin/env python3
"""OpenClaw/QwenPaw 可调用的中医 Skill 工具入口。

用法：
  python3 tools/tcm_tools.py tcm_safety_check '{"text":"胸痛,呼吸困难"}'
  python3 tools/tcm_tools.py tcm_trace '{"query":"桂枝汤"}'

所有输出均为 JSON，且医学相关结果必须包含安全边界或来源状态。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from internal.diagnosis_engine import DiagnosisEngine
from internal.safety_guard import DISCLAIMER, build_missing_questions, check_red_flags, normalize_symptoms, safety_policy
from internal.source_corpus import SourceCorpus
from internal.trace_service import TraceService
from internal.fts_search import FtsSearch


def _payload() -> Dict[str, Any]:
    if len(sys.argv) >= 3:
        return json.loads(sys.argv[2])
    raw = sys.stdin.read().strip()
    return json.loads(raw) if raw else {}


def _print(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def tcm_safety_check(payload: Dict[str, Any]) -> Dict[str, Any]:
    raw = payload.get("symptoms") or payload.get("text") or ""
    symptoms = normalize_symptoms(raw)
    safety = check_red_flags(symptoms)
    if safety.get("risk_level") == "high":
        message = "检测到急症红旗，建议优先联系急救或及时就医；本工具不继续给出方剂或穴位建议。"
    elif safety.get("risk_level") == "medium":
        message = "检测到特殊人群或实际治疗意图；本工具只保留资料检索与学习边界，不给出处方、剂量、服药或针灸操作建议。"
    else:
        message = "未检测到内置红旗；仍仅作中医理论学习和资料检索参考。"
    return {
        "disclaimer": DISCLAIMER,
        "risk_level": safety.get("risk_level"),
        "high_risk": safety.get("risk_level") == "high",
        "blocked": bool(safety.get("should_stop_formula")),
        "red_flags": safety.get("red_flags", []),
        "safety": safety,
        "message": message,
    }


def tcm_source_search(payload: Dict[str, Any]) -> Dict[str, Any]:
    keyword = payload.get("keyword") or payload.get("query") or ""
    limit = int(payload.get("limit", 5))
    context = int(payload.get("context", 100))
    corpus = SourceCorpus()
    return {
        "query": keyword,
        "available": corpus.available(),
        "hits": [h.to_dict() for h in corpus.search(keyword, limit=limit, context=context)],
    }


def tcm_trace(payload: Dict[str, Any]) -> Dict[str, Any]:
    query = payload.get("query") or payload.get("name") or ""
    return TraceService().trace(query, limit=int(payload.get("limit", 5)))


def _query_markdown(kind: str, subdir: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    name = payload.get("name") or payload.get("query") or ""
    root = ROOT / "knowledge" / subdir
    matches = []
    for path in sorted(root.glob("*.md")):
        if "index" in path.name:
            continue
        text = path.read_text(encoding="utf-8")
        if name in path.stem or name in text[:300]:
            matches.append({
                "file": str(path.relative_to(ROOT)),
                "preview": text[: int(payload.get("chars", 1200))],
            })
            if len(matches) >= int(payload.get("limit", 3)):
                break
    return {"kind": kind, "query": name, "matches": matches, "trace": TraceService().trace(name, limit=3)}


def tcm_formula_query(payload: Dict[str, Any]) -> Dict[str, Any]:
    return _query_markdown("formula", "formulas", payload)


def tcm_herb_query(payload: Dict[str, Any]) -> Dict[str, Any]:
    return _query_markdown("herb", "herbs", payload)


def tcm_acupoint_query(payload: Dict[str, Any]) -> Dict[str, Any]:
    return _query_markdown("acupoint", "acupoints", payload)


def tcm_diagnose_assist(payload: Dict[str, Any]) -> Dict[str, Any]:
    symptoms = normalize_symptoms(payload.get("symptoms") or [])
    text = ",".join(symptoms)
    safety = tcm_safety_check({"text": text})
    if safety["blocked"]:
        return {
            "disclaimer": DISCLAIMER,
            "safety": safety,
            "stopped": True,
            "reason": "检测到安全风险或实际治疗意图，停止输出方剂参考。",
            "allowed_response_scope": safety["safety"].get("allowed_response_scope"),
            "missing_questions": build_missing_questions(symptoms),
        }
    result = DiagnosisEngine().analyze(symptoms)
    formula = result.get("formula") or {}
    formula_name = formula.get("name")
    formula_id = formula.get("formula_id")
    trace_query = formula_id or formula_name
    result["formula_trace"] = TraceService().trace(trace_query, limit=3) if trace_query else {"trace_status": "no_formula", "source_quality_level": "no_source"}
    result["safety"] = safety["safety"]
    result["safety_boundary"] = "辨证结果仅供学习参考，不构成诊断、处方、剂量、服药或针灸操作建议。"
    result["stopped"] = False
    return result


def _load_jsonl(path: Path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]



def _count_by(rows, key):
    counts = {}
    for row in rows:
        value = row.get(key)
        counts[value] = counts.get(value, 0) + 1
    return counts


def _compact_trace(trace: Dict[str, Any], limit: int = 3) -> Dict[str, Any]:
    matches = []
    for item in (trace.get("matches") or [])[:limit]:
        refs = item.get("source_refs") or []
        first_ref = refs[0] if refs else item
        matches.append({
            "kind": item.get("kind"),
            "item_id": item.get("item_id"),
            "name": item.get("name"),
            "file": item.get("file"),
            "source_quality_level": item.get("source_quality_level", trace.get("source_quality_level", "")),
            "source_file": first_ref.get("source_file"),
            "page_num": first_ref.get("page_num"),
            "quote": (first_ref.get("quote") or "")[:260],
        })
    result = {
        "query": trace.get("query"),
        "trace_status": trace.get("trace_status"),
        "source_quality_level": trace.get("source_quality_level", ""),
        "summary": f"{trace.get('trace_status')}，命中 {len(trace.get('matches') or [])} 条；优先展示 verified 来源。",
        "matches": matches,
    }
    # P10-B: pass through alias_redirect if present
    if trace.get("alias_redirect"):
        result["alias_redirect"] = trace["alias_redirect"]
    return result


def tcm_trace_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    query = payload.get("query") or payload.get("name") or ""
    trace = TraceService().trace(query, limit=int(payload.get("limit", 5)))
    return {"disclaimer": DISCLAIMER, **_compact_trace(trace, limit=int(payload.get("summary_limit", 3)))}


def tcm_verified_stats(payload: Dict[str, Any]) -> Dict[str, Any]:
    rows = _load_jsonl(ROOT / "data" / "verified_sources.jsonl")
    return {
        "verified_count": len(rows),
        "by_kind": _count_by(rows, "kind"),
        "boundary": "verified 表示来源已纳入复核链路，不代表医学真实性或临床适用性结论。",
    }


def tcm_no_source_report(payload: Dict[str, Any]) -> Dict[str, Any]:
    path = ROOT / "report" / "p6_no_source_report.md"
    return {"available": path.exists(), "report": path.read_text(encoding="utf-8") if path.exists() else ""}

def tcm_search_sources_fts(payload: Dict[str, Any]) -> Dict[str, Any]:
    query = payload.get("query") or payload.get("keyword") or ""
    return {
        "query": query,
        "hits": FtsSearch().search(query, limit=int(payload.get("limit", 5)), context=int(payload.get("context", 100))),
    }


def tcm_review_next(payload: Dict[str, Any]) -> Dict[str, Any]:
    kind = payload.get("kind")
    status = payload.get("status")
    limit = int(payload.get("limit", 10))
    decisions = {(r.get("kind"), r.get("item_id")) for r in _load_jsonl(ROOT / "data" / "review_decisions.jsonl")}
    rows = []
    for item in _load_jsonl(ROOT / "data" / "review_queue.jsonl"):
        if kind and item.get("kind") != kind:
            continue
        if status and item.get("review_status") != status:
            continue
        if (item.get("kind"), item.get("item_id")) in decisions:
            continue
        rows.append(item)
    return {"count": len(rows), "items": rows[:limit]}


def tcm_review_stats(payload: Dict[str, Any]) -> Dict[str, Any]:
    counts = {}
    for item in _load_jsonl(ROOT / "data" / "review_queue.jsonl"):
        key = f"{item.get('kind')}:{item.get('review_status')}"
        counts[key] = counts.get(key, 0) + 1
    return {"review_queue_count": sum(counts.values()), "counts": counts}


def tcm_quality_report(payload: Dict[str, Any]) -> Dict[str, Any]:
    path = ROOT / "report" / "quality_report.md"
    return {"available": path.exists(), "report": path.read_text(encoding="utf-8") if path.exists() else ""}


def _compare(kind: str, subdir: str, names):
    if isinstance(names, str):
        names = [x.strip() for x in names.replace("，", ",").split(",") if x.strip()]
    return {"kind": kind, "items": [_query_markdown(kind, subdir, {"name": name, "chars": 600, "limit": 1}) for name in names]}


def tcm_compare_formulas(payload: Dict[str, Any]) -> Dict[str, Any]:
    return _compare("formula", "formulas", payload.get("names") or payload.get("query") or [])


def tcm_compare_herbs(payload: Dict[str, Any]) -> Dict[str, Any]:
    return _compare("herb", "herbs", payload.get("names") or payload.get("query") or [])


def tcm_lookup(payload: Dict[str, Any]) -> Dict[str, Any]:
    query = payload.get("query") or payload.get("name") or ""
    kind = payload.get("kind")
    kind_map = {"formula": "formulas", "herb": "herbs", "acupoint": "acupoints"}
    if not kind:
        trace = TraceService().trace(query, limit=1)
        first = (trace.get("matches") or [{}])[0]
        kind = first.get("kind") or "formula"
    subdir = kind_map.get(kind, "formulas")
    markdown = _query_markdown(kind, subdir, {"name": query, "chars": int(payload.get("chars", 900)), "limit": 1})
    trace = TraceService().trace(query, limit=int(payload.get("limit", 5)))
    return {
        "disclaimer": DISCLAIMER,
        "query": query,
        "kind": kind,
        "trace": _compact_trace(trace, limit=int(payload.get("summary_limit", 3))),
        "source_quality_level": trace.get("source_quality_level", ""),
        "markdown": markdown.get("matches", []),
        "safety_boundary": "学习参考与资料检索，不作为诊断、处方、用药、针灸操作或治疗建议。",
    }


def tcm_explain_trace(payload: Dict[str, Any]) -> Dict[str, Any]:
    query = payload.get("query") or payload.get("name") or ""
    trace = TraceService().trace(query, limit=int(payload.get("limit", 5)))
    status = trace.get("trace_status")
    explanations = {
        "verified": "命中 data/verified_sources.jsonl，说明该条目已有复核来源链路。",
        "candidate": "命中 index 候选来源，但尚未进入 verified；需要人工复核。",
        "needs_review": "命中 review_queue，说明候选不足或来源相关性需要人工确认。",
        "source_search": "未命中治理索引，已退回原始语料关键词搜索。",
        "no_source_found": "当前未找到可用来源，保持待考，不应补写医学结论。",
        "empty_query": "查询为空。",
    }
    return {
        "query": query,
        "trace_status": status,
        "explanation": explanations.get(status, "未知状态，需要人工检查。"),
        "boundary": "trace 状态只代表来源治理状态，不代表医学真实性或临床适用性。",
        "source_quality_level": trace.get("source_quality_level", ""),
        "trace": _compact_trace(trace, limit=int(payload.get("summary_limit", 3))),
    }


def tcm_safety_policy(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return P2 medical safety policy for Agent callers."""
    return safety_policy()


def tcm_source_quality_levels(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return source quality/status policy for Agent callers."""
    return {
        "boundary": "来源质量只描述资料链路可信度，不判断医学真实性、临床适用性或治疗建议。",
        "trace_status": {
            "verified": "来源追溯链路已登记；可引用来源摘录，但必须保留学习参考与安全边界。",
            "candidate": "有候选来源但未验证；只能说可能相关，不能当作 verified。",
            "needs_review": "相关性或条目归属仍需人工确认；不输出确定医学结论。",
            "no_source_found": "当前来源范围内未找到依据；不凭模型记忆补写医学细节。",
            "source_search": "仅原始语料关键词命中；只能作为检索线索。",
        },
        "suggested_verified_sublevels": {
            "verified_direct": "来源片段以条目名为主题，包含专门讲解/本经原文/方剂组成/穴位定位等。",
            "verified_contextual": "来源片段明确提到条目名，但主题可能是病案、其他方剂或上下文说明。",
            "verified_alias": "通过别名/父级名/异名命中，且已人工确认归属。",
            "candidate_alias": "alias 命中但未人工确认。",
        },
        "doc": "docs/source_quality_levels.md",
    }

def tcm_review_dashboard(payload: Dict[str, Any]) -> Dict[str, Any]:
    verified = _load_jsonl(ROOT / "data" / "verified_sources.jsonl")
    queue = _load_jsonl(ROOT / "data" / "review_queue.jsonl")
    decisions = {(r.get("kind"), r.get("item_id")) for r in _load_jsonl(ROOT / "data" / "review_decisions.jsonl")}
    unresolved = [r for r in queue if (r.get("kind"), r.get("item_id")) not in decisions]
    audit_path = ROOT / "report" / "frontmatter_audit.md"
    audit = audit_path.read_text(encoding="utf-8").splitlines()[:5] if audit_path.exists() else []
    return {
        "verified": {"count": len(verified), "by_kind": _count_by(verified, "kind")},
        "review_queue": {"count": len(queue), "unresolved": len(unresolved), "by_status": _count_by(queue, "review_status")},
        "frontmatter_audit_head": audit,
        "reports": {
            "p7_no_source_classification": str((ROOT / "report" / "p7_no_source_classification.md").relative_to(ROOT)),
            "p7_alias_review": str((ROOT / "report" / "p7_alias_review.md").relative_to(ROOT)),
        },
        "boundary": "治理统计用于复核排程，不作为医学建议。",
    }


def tcm_batch_trace(payload: Dict[str, Any]) -> Dict[str, Any]:
    queries = payload.get("queries") or payload.get("names") or payload.get("query") or []
    if isinstance(queries, str):
        queries = [x.strip() for x in queries.replace("，", ",").split(",") if x.strip()]
    limit = int(payload.get("limit", 3))
    return {
        "count": len(queries),
        "items": [_compact_trace(TraceService().trace(q, limit=limit), limit=limit) for q in queries],
        "boundary": "批量 trace 仅展示来源治理状态。",
    }


TOOLS = {
    "tcm_safety_check": tcm_safety_check,
    "tcm_source_search": tcm_source_search,
    "tcm_trace": tcm_trace,
    "tcm_formula_query": tcm_formula_query,
    "tcm_herb_query": tcm_herb_query,
    "tcm_acupoint_query": tcm_acupoint_query,
    "tcm_diagnose_assist": tcm_diagnose_assist,
    "tcm_search_sources_fts": tcm_search_sources_fts,
    "tcm_trace_summary": tcm_trace_summary,
    "tcm_verified_stats": tcm_verified_stats,
    "tcm_no_source_report": tcm_no_source_report,
    "tcm_lookup": tcm_lookup,
    "tcm_explain_trace": tcm_explain_trace,
    "tcm_safety_policy": tcm_safety_policy,
    "tcm_source_quality_levels": tcm_source_quality_levels,
    "tcm_review_dashboard": tcm_review_dashboard,
    "tcm_batch_trace": tcm_batch_trace,
    "tcm_review_next": tcm_review_next,
    "tcm_review_stats": tcm_review_stats,
    "tcm_quality_report": tcm_quality_report,
    "tcm_compare_formulas": tcm_compare_formulas,
    "tcm_compare_herbs": tcm_compare_herbs,
}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in TOOLS:
        _print({"error": "unknown_tool", "available_tools": sorted(TOOLS)})
        return 2
    try:
        _print(TOOLS[sys.argv[1]](_payload()))
        return 0
    except Exception as exc:
        _print({"error": type(exc).__name__, "message": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
