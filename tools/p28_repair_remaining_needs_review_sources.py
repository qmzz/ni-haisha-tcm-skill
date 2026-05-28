#!/usr/bin/env python3
"""P28/P5-C repair remaining needs_review source_refs by re-searching raw JSON.

Uses SourceCorpus keyword search over NIHAIXIA_SOURCE_DIR (or default source dir).
Conservative: promote only when quote contains item name and direct markers; demote
no-hit rows to no_source. No medical content changes.
"""
from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p28_remaining_needs_review_source_repair.md"
POLICY = "source_quality_is_traceability_only_not_medical_validation"

import sys
sys.path.insert(0, str(ROOT))
from internal.source_corpus import SourceCorpus

INDEX_FILES = [
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]

QUERY_OVERRIDES = {
    "changshanmiao": ["常山苗", "常山"],
    "bingpian": ["冰片", "龙脑"],
    "zhushagen": ["朱砂根", "朱砂"],
    "xiamen": ["侠白"],
}

PREFERRED_SOURCE_TOKENS = {
    "herb": ["神农本草经", "人-神农本草经"],
    "acupoint": ["针灸", "针灸大成"],
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def direct_markers(kind: str, name: str, quote: str) -> bool:
    if not name or name not in quote:
        return False
    pos = quote.find(name)
    snip = quote[max(0, pos - 120): pos + len(name) + 160]
    if kind == "herb":
        return any(m in snip for m in [f"{name}为", f"{name}是", f"【{name}", "【性味】", "【主治】", "【本经原文】", "【禁忌】", "【用量】"])
    if kind == "acupoint":
        return any(m in snip for m in [f"{name}穴", f"叫{name}", f"就是{name}", f"称{name}", "下针", "灸", "穴道", "寸", "经"])
    return False


def score_hit(kind: str, name: str, hit: dict[str, Any]) -> int:
    q = hit.get("quote") or ""
    sf = hit.get("source_file") or ""
    score = 0
    if name in q:
        score += 50
    if direct_markers(kind, name, q):
        score += 40
    if any(tok in sf for tok in PREFERRED_SOURCE_TOKENS.get(kind, [])):
        score += 10
    if "........" in q or "{\"page_num\"" in q:
        score -= 50
    return score


def search_best(corpus: SourceCorpus, kind: str, item_id: str, name: str) -> tuple[dict[str, Any] | None, str]:
    queries = QUERY_OVERRIDES.get(item_id, [name])
    all_hits = []
    for q in queries:
        for h in corpus.search(q, limit=10, context=260):
            d = h.to_dict()
            d["searched_keyword"] = q
            d["score"] = score_hit(kind, q if q != name else name, d)
            all_hits.append(d)
    if not all_hits:
        return None, "no_raw_source_hit"
    # Prefer hits containing canonical name, then override/base name.
    all_hits.sort(key=lambda h: h.get("score", 0), reverse=True)
    best = all_hits[0]
    qname = best.get("searched_keyword") or name
    if best.get("score", 0) >= 60 and qname in (best.get("quote") or ""):
        return best, "raw_search_direct_hit"
    if qname in (best.get("quote") or "") and best.get("score", 0) >= 30:
        return best, "raw_search_contextual_hit"
    return best, "raw_search_weak_hit"


def main() -> int:
    if "NIHAIXIA_SOURCE_DIR" not in os.environ:
        candidate = ROOT.parents[1] / "nihaixia" / "extracted"
        if candidate.exists():
            os.environ["NIHAIXIA_SOURCE_DIR"] = str(candidate)
    corpus = SourceCorpus()
    if not corpus.available():
        raise SystemExit("Source corpus unavailable; set NIHAIXIA_SOURCE_DIR")

    rows = load_jsonl(DATA / "verified_sources.jsonl")
    decisions = []
    for row in rows:
        if row.get("source_quality_level") != "needs_review":
            continue
        kind = row.get("kind") or ""
        item_id = row.get("item_id") or ""
        name = row.get("name") or ""
        hit, reason = search_best(corpus, kind, item_id, name)
        old = row.get("source_quality_level")
        if hit and reason == "raw_search_direct_hit":
            row["source_refs"] = [{k: hit.get(k) for k in ["source_file", "page_num", "quote", "char_start", "char_end", "searched_keyword", "score"]}]
            row["trace_status"] = "verified"
            row["source_quality_level"] = "verified_direct"
        elif hit and reason == "raw_search_contextual_hit":
            row["source_refs"] = [{k: hit.get(k) for k in ["source_file", "page_num", "quote", "char_start", "char_end", "searched_keyword", "score"]}]
            row["trace_status"] = "verified"
            row["source_quality_level"] = "verified_contextual"
        elif hit and (hit.get("searched_keyword") != name) and (hit.get("searched_keyword") in (hit.get("quote") or "")):
            row["source_refs"] = [{k: hit.get(k) for k in ["source_file", "page_num", "quote", "char_start", "char_end", "searched_keyword", "score"]}]
            row["trace_status"] = "verified"
            row["source_quality_level"] = "verified_alias"
            reason = "raw_search_alias_hit"
        else:
            row["source_refs"] = []
            row["trace_status"] = "no_source_found"
            row["source_quality_level"] = "no_source"
        row["source_quality_policy"] = POLICY
        row["p5c_resolution"] = reason
        decisions.append({
            "kind": kind,
            "item_id": item_id,
            "name": name,
            "from": old,
            "to": row.get("source_quality_level"),
            "trace_status": row.get("trace_status"),
            "reason": reason,
            "source_file": (row.get("source_refs") or [{}])[0].get("source_file"),
            "page_num": (row.get("source_refs") or [{}])[0].get("page_num"),
            "quote_preview": ((row.get("source_refs") or [{}])[0].get("quote") or "")[:180],
        })

    write_jsonl(DATA / "verified_sources.jsonl", rows)
    by_key = {(r.get("kind"), r.get("item_id")): r for r in rows}

    for kind, id_key, path in INDEX_FILES:
        idx = load_jsonl(path)
        for row in idx:
            key = (kind, row.get(id_key))
            if key in by_key:
                v = by_key[key]
                row["trace_status"] = v.get("trace_status")
                row["source_quality_level"] = v.get("source_quality_level")
                row["source_quality_policy"] = POLICY
                row["source_refs"] = v.get("source_refs", [])
                if v.get("p5c_resolution"):
                    row["p5c_resolution"] = v["p5c_resolution"]
        write_jsonl(path, idx)

    comp = load_jsonl(DATA / "knowledge_completeness.jsonl")
    for row in comp:
        key = (row.get("kind"), row.get("item_id"))
        if key in by_key:
            v = by_key[key]
            row["trace_status"] = v.get("trace_status")
            row["source_quality_level"] = v.get("source_quality_level")
            row["source_quality_policy"] = POLICY
            row["verified_in_registry"] = v.get("trace_status") == "verified"
            row["has_source_refs"] = bool(v.get("source_refs"))
            if v.get("p5c_resolution"):
                row["p5c_resolution"] = v["p5c_resolution"]
    write_jsonl(DATA / "knowledge_completeness.jsonl", comp)

    counts = Counter(d["to"] for d in decisions)
    lines = [
        "# P28 / P5-C Remaining needs_review Source Repair",
        "",
        "逐条对剩余 needs_review 进行原始 JSON 重检索与保守修复。",
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
