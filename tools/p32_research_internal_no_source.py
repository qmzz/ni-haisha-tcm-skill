#!/usr/bin/env python3
"""P32/P6-C re-search internal_research_needed no_source rows in raw Ni corpus.

No medical content changes. If raw JSON search finds a traceable quote, update
source_refs/source_quality_level conservatively. Otherwise keep no_source with an
explicit P6-C exhausted marker.
"""
from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p32_internal_no_source_research.md"
POLICY = "source_quality_is_traceability_only_not_medical_validation"

import sys
sys.path.insert(0, str(ROOT))
from internal.source_corpus import SourceCorpus

INDEX_FILES = [
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]

PREFERRED_SOURCE_TOKENS = {
    "herb": ["神农本草经", "人-神农本草经"],
    "acupoint": ["针灸", "针灸大成"],
}

QUERY_OVERRIDES = {
    "gualue": ["瓜蒌"],
    "huangbo": ["黄柏"],
    "hezi": ["鹤虱"],
    "luobuma": ["罗布麻叶", "罗布麻"],
    "aoshu": ["糯稻根"],
    "aoshugen": ["糯稻根须", "糯稻根"],
    "hechezi": ["黑芝麻", "胡麻"],
    "heizhima": ["黑芝麻", "胡麻"],
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def direct_markers(kind: str, name: str, quote: str) -> bool:
    if name not in quote:
        return False
    pos = quote.find(name)
    snip = quote[max(0, pos - 140): pos + len(name) + 180]
    if kind == "herb":
        return any(m in snip for m in [f"{name}为", f"{name}是", f"【{name}", "【性味】", "【主治】", "【本经原文】", "【禁忌】", "【用量】", "产地", "性味", "主治"])
    if kind == "acupoint":
        return any(m in snip for m in [f"{name}穴", f"叫{name}", f"就是{name}", f"称{name}", "下针", "灸", "穴道", "寸", "经", "络穴"])
    return False


def score_hit(kind: str, name: str, hit: dict[str, Any]) -> int:
    q = hit.get("quote") or ""
    sf = hit.get("source_file") or ""
    score = 0
    if name in q:
        score += 50
    if direct_markers(kind, name, q):
        score += 35
    if any(tok in sf for tok in PREFERRED_SOURCE_TOKENS.get(kind, [])):
        score += 15
    if "........" in q or "{\"page_num\"" in q or len(q.strip()) < 30:
        score -= 40
    return score


def search_best(corpus: SourceCorpus, kind: str, item_id: str, name: str) -> tuple[dict[str, Any] | None, str]:
    queries = QUERY_OVERRIDES.get(item_id, [name])
    hits = []
    for q in queries:
        for h in corpus.search(q, limit=12, context=300):
            d = h.to_dict()
            d["searched_keyword"] = q
            d["score"] = score_hit(kind, q, d)
            hits.append(d)
    if not hits:
        return None, "internal_no_hit"
    hits.sort(key=lambda h: h.get("score", 0), reverse=True)
    best = hits[0]
    q = best.get("searched_keyword") or name
    if best.get("score", 0) >= 70:
        return best, "internal_direct_hit"
    if best.get("score", 0) >= 45 and q in (best.get("quote") or ""):
        return best, "internal_contextual_hit"
    return best, "internal_weak_hit_kept_no_source"


def main() -> int:
    if "NIHAIXIA_SOURCE_DIR" not in os.environ:
        candidate = ROOT.parents[1] / "nihaixia" / "extracted"
        if candidate.exists():
            os.environ["NIHAIXIA_SOURCE_DIR"] = str(candidate)
    corpus = SourceCorpus()
    if not corpus.available():
        raise SystemExit("Source corpus unavailable; set NIHAIXIA_SOURCE_DIR")

    comp = load_jsonl(DATA / "knowledge_completeness.jsonl")
    verified = load_jsonl(DATA / "verified_sources.jsonl")
    verified_by_key = {(r.get("kind"), r.get("item_id")): r for r in verified}

    decisions = []
    for row in comp:
        if row.get("source_quality_level") != "no_source":
            continue
        if row.get("no_source_classification") != "internal_research_needed":
            continue
        kind = row.get("kind") or ""
        item_id = row.get("item_id") or ""
        name = row.get("name") or ""
        hit, reason = search_best(corpus, kind, item_id, name)
        old_level = row.get("source_quality_level")
        source_refs = []
        if hit and reason == "internal_direct_hit":
            new_status = "verified"
            new_level = "verified_direct"
            source_refs = [{k: hit.get(k) for k in ["source_file", "page_num", "quote", "char_start", "char_end", "searched_keyword", "score"]}]
        elif hit and reason == "internal_contextual_hit":
            new_status = "verified"
            new_level = "verified_contextual"
            source_refs = [{k: hit.get(k) for k in ["source_file", "page_num", "quote", "char_start", "char_end", "searched_keyword", "score"]}]
        else:
            new_status = "no_source_found"
            new_level = "no_source"

        row["trace_status"] = new_status
        row["source_quality_level"] = new_level
        row["source_quality_policy"] = POLICY
        row["verified_in_registry"] = new_status == "verified"
        row["has_source_refs"] = bool(source_refs)
        row["p6c_resolution"] = reason
        if new_level == "no_source":
            row["no_source_classification"] = "internal_research_exhausted"
            row["next_action"] = "external_source_policy_or_manual_review"
        else:
            row["no_source_classification"] = "resolved_by_internal_research"
            row["next_action"] = "none"

        key = (kind, item_id)
        if new_status == "verified":
            v = verified_by_key.get(key)
            if not v:
                v = {"kind": kind, "item_id": item_id, "name": name, "file": row.get("file")}
                verified.append(v)
                verified_by_key[key] = v
            v.update({
                "trace_status": "verified",
                "source_refs": source_refs,
                "review_status": "trace_review_passed",
                "source_quality_level": new_level,
                "source_quality_policy": POLICY,
                "p6c_resolution": reason,
            })
        elif key in verified_by_key:
            v = verified_by_key[key]
            v.update({
                "trace_status": "no_source_found",
                "source_refs": [],
                "review_status": "needs_source",
                "source_quality_level": "no_source",
                "source_quality_policy": POLICY,
                "p6c_resolution": reason,
            })

        decisions.append({
            "kind": kind,
            "item_id": item_id,
            "name": name,
            "from": old_level,
            "to": new_level,
            "trace_status": new_status,
            "reason": reason,
            "source_file": source_refs[0].get("source_file") if source_refs else None,
            "page_num": source_refs[0].get("page_num") if source_refs else None,
            "quote_preview": (source_refs[0].get("quote") if source_refs else "")[:180],
        })

    write_jsonl(DATA / "knowledge_completeness.jsonl", comp)
    write_jsonl(DATA / "verified_sources.jsonl", verified)
    comp_by_key = {(r.get("kind"), r.get("item_id")): r for r in comp}
    ver_by_key = {(r.get("kind"), r.get("item_id")): r for r in verified}

    for kind, id_key, path in INDEX_FILES:
        rows = load_jsonl(path)
        for row in rows:
            key = (kind, row.get(id_key))
            c = comp_by_key.get(key)
            if not c:
                continue
            if c.get("p6c_resolution"):
                row["trace_status"] = c.get("trace_status")
                row["source_quality_level"] = c.get("source_quality_level")
                row["source_quality_policy"] = POLICY
                row["p6c_resolution"] = c.get("p6c_resolution")
                row["no_source_classification"] = c.get("no_source_classification")
                row["next_action"] = c.get("next_action")
                if c.get("trace_status") == "verified":
                    row["source_refs"] = ver_by_key.get(key, {}).get("source_refs", [])
                else:
                    row["source_refs"] = []
        write_jsonl(path, rows)

    # Refresh no_source queue
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
            })
    write_jsonl(DATA / "p30_no_source_classification.jsonl", queue)

    counts = Counter(d["to"] for d in decisions)
    lines = [
        "# P32 / P6-C internal no_source Research",
        "",
        "本报告记录对 `internal_research_needed` 队列的倪海厦原始 JSON 重检索。",
        "",
        "> 边界：只更新来源关系与 source_refs，不改写医学内容，不判断医学真实性或疗效。",
        "",
        f"- Processed: {len(decisions)}",
        "",
        "## By target level",
        "",
        "| target | count |",
        "|---|---:|",
    ]
    for k, v in sorted(counts.items()):
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "## Decisions", ""]
    for d in decisions:
        lines.append(f"- `{d['kind']}:{d['item_id']}` {d['name']} — `{d['from']}` → `{d['to']}` ({d['reason']}; {d.get('source_file')} p{d.get('page_num')})")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"processed": len(decisions), "by_target": dict(counts), "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
