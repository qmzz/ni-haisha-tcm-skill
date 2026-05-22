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
