#!/usr/bin/env python3
"""来源候选质量评分。"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

PREFERRED_BY_KIND = {
    "formula": ["伤寒论", "金匮要略", "方剂讲解", "桂林古本"],
    "herb": ["神农本草经", "人-神农本草经"],
    "acupoint": ["针灸", "针灸大成"],
}

CONTEXT_BY_KIND = {
    "formula": ["方", "汤", "丸", "散", "主之", "组成"],
    "herb": ["性味", "主治", "本经", "药", "草", "毒", "无毒"],
    "acupoint": ["穴", "针", "灸", "经", "刺", "寸"],
}


def score_source_hit(kind: str, name: str, hit: Dict, expected_source: Optional[str] = None) -> Tuple[int, List[str], List[str], str]:
    quote = hit.get("quote") or ""
    source_file = hit.get("source_file") or ""
    matched_keyword = hit.get("matched_keyword") or name
    reasons: List[str] = []
    risks: List[str] = []
    score = 0

    if name in quote:
        score += 40
        reasons.append("matched_exact_name")
    elif matched_keyword and matched_keyword in quote:
        score += 20
        reasons.append("matched_alias_keyword")
        risks.append("alias_match_only")

    if matched_keyword == name:
        score += 10
        reasons.append("primary_keyword")
    else:
        score -= 10
        risks.append("alias_requires_review")

    if expected_source and expected_source in source_file:
        score += 25
        reasons.append("expected_source_file")

    for token in PREFERRED_BY_KIND.get(kind, []):
        if token in source_file:
            score += 15
            reasons.append("preferred_source_file")
            break

    context_hits = [kw for kw in CONTEXT_BY_KIND.get(kind, []) if kw in quote]
    if context_hits:
        score += min(15, len(context_hits) * 3)
        reasons.append("contains_tcm_context_keyword")

    if len(quote) < 30:
        score -= 20
        risks.append("quote_too_short")
    if len(quote) > 500:
        score -= 5
        risks.append("quote_long_context")

    score = max(0, min(100, score))
    if risks:
        needs_review_reason = "；".join(risks)
    elif score < 60:
        needs_review_reason = "quality_score_below_verified_threshold"
    else:
        needs_review_reason = "候选来源需人工复核"
    return score, reasons, risks, needs_review_reason


def enrich_hits(kind: str, name: str, hits: List[Dict], expected_source: Optional[str] = None) -> List[Dict]:
    enriched = []
    for hit in hits:
        record = dict(hit)
        score, reasons, risks, review_reason = score_source_hit(kind, name, record, expected_source)
        record["quality_score"] = score
        record["match_reason"] = reasons
        record["risk_flags"] = risks
        record["needs_review_reason"] = review_reason
        enriched.append(record)
    enriched.sort(key=lambda h: h.get("quality_score", 0), reverse=True)
    return enriched



def _has_alias_risk(refs: List[Dict]) -> bool:
    for ref in refs or []:
        risks = ref.get("risk_flags") or []
        if any("alias" in str(r) for r in risks):
            return True
        matched = ref.get("matched_keyword")
        # matched_keyword may be absent in manually verified rows.
        if matched and ref.get("name") and matched != ref.get("name"):
            return True
    return False


def _looks_direct(kind: str, name: str, refs: List[Dict]) -> bool:
    """Conservative direct-source heuristic.

    Direct means the quoted source appears to discuss the item itself, not only
    mention it in a distant context. This is source-chain quality only, not
    medical validation.
    """
    if not refs:
        return False
    for ref in refs[:3]:
        quote = ref.get("quote") or ""
        if not name or name not in quote:
            continue
        pos = quote.find(name)
        if pos <= 160:
            return True
        reasons = set(ref.get("match_reason") or [])
        score = ref.get("quality_score")
        if "matched_exact_name" in reasons and (score is None or int(score) >= 80):
            return True
        if kind == "formula" and f"{name}方" in quote:
            return True
        if kind == "herb" and (f"、{name}" in quote or f"【{name}" in quote or f"{name} ——" in quote):
            return True
        if kind == "acupoint" and (f"{name}穴" in quote or f"、{name}" in quote):
            return True
    return False


def classify_source_quality(kind: str, name: str, trace_status: str, refs: List[Dict] | None = None, notes: str = "") -> str:
    """Classify source-chain quality for registry/index rows.

    This does not judge medical truth, efficacy, clinical applicability, or
    safety. It only grades traceability/source relation quality.
    """
    refs = refs or []
    status = trace_status or ""
    notes_l = (notes or "").lower()

    if status in {"no_source_found", "no_source"} or not refs:
        if status == "verified":
            return "verified_contextual"
        if status == "candidate":
            return "candidate_contextual"
        return "no_source"
    if status == "source_search":
        return "source_search"
    if status == "needs_review":
        return "needs_review"

    alias = _has_alias_risk(refs) or "alias" in notes_l or "异名" in notes or "别名" in notes
    direct = _looks_direct(kind, name, refs)

    if status == "verified":
        if alias:
            return "verified_alias"
        if direct:
            return "verified_direct"
        return "verified_contextual"
    if status == "candidate":
        if alias:
            return "candidate_alias"
        if direct:
            return "candidate_direct"
        return "candidate_contextual"
    return "needs_review" if refs else "no_source"
