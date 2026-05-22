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
from internal.safety_guard import DISCLAIMER, build_missing_questions, check_red_flags
from internal.source_corpus import SourceCorpus
from internal.trace_service import TraceService


def _payload() -> Dict[str, Any]:
    if len(sys.argv) >= 3:
        return json.loads(sys.argv[2])
    raw = sys.stdin.read().strip()
    return json.loads(raw) if raw else {}


def _print(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def tcm_safety_check(payload: Dict[str, Any]) -> Dict[str, Any]:
    raw = payload.get("symptoms") or payload.get("text") or ""
    if isinstance(raw, str):
        symptoms = [s.strip() for s in raw.replace("，", ",").split(",") if s.strip()]
    else:
        symptoms = [str(s).strip() for s in raw if str(s).strip()]
    safety = check_red_flags(symptoms)
    return {
        "disclaimer": DISCLAIMER,
        "high_risk": bool(safety.get("should_stop_formula")),
        "red_flags": safety.get("red_flags", []),
        "safety": safety,
        "message": "建议优先联系专业医师或及时就医；本工具不继续给出方剂参考。" if safety.get("should_stop_formula") else "未检测到内置红旗症状。",
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
    symptoms = payload.get("symptoms") or []
    if isinstance(symptoms, str):
        symptoms = [s.strip() for s in symptoms.replace("，", ",").split(",") if s.strip()]
    text = ",".join(symptoms)
    safety = tcm_safety_check({"text": text})
    if safety["high_risk"]:
        return {
            "disclaimer": DISCLAIMER,
            "safety": safety,
            "stopped": True,
            "reason": "检测到高风险信号，停止输出方剂参考。",
            "missing_questions": build_missing_questions(symptoms),
        }
    result = DiagnosisEngine().analyze(symptoms)
    formula_name = (result.get("formula") or {}).get("name")
    result["formula_trace"] = TraceService().trace(formula_name, limit=3) if formula_name else {"trace_status": "no_formula"}
    result["stopped"] = False
    return result


TOOLS = {
    "tcm_safety_check": tcm_safety_check,
    "tcm_source_search": tcm_source_search,
    "tcm_trace": tcm_trace,
    "tcm_formula_query": tcm_formula_query,
    "tcm_herb_query": tcm_herb_query,
    "tcm_acupoint_query": tcm_acupoint_query,
    "tcm_diagnose_assist": tcm_diagnose_assist,
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
