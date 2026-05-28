#!/usr/bin/env python3
"""P35/P7-A tighten verified_contextual rows.

Re-searches contextual rows in the Ni source corpus. Promotes to verified_direct
only when a quote has a direct item marker. Otherwise keeps verified_contextual
but adds an explicit rationale. Demotes noisy false-positive sourceRefs to
no_source when the source quote is clearly unrelated.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p35_verified_contextual_tightening.md"
POLICY = "source_quality_is_traceability_only_not_medical_validation"

sys.path.insert(0, str(ROOT))
from internal.source_corpus import SourceCorpus

INDEX_FILES = [
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]

DIRECT_BAD = {("acupoint", "shiqixue")}
DIRECT_ALIAS = {"naokong_bl": "脑空"}

# Conservative direct markers: item name near a teaching section, location, needle/moxa, or benjing title.
HERB_MARKERS = ["【本经原文】", "【性味】", "【主治】", "【禁忌】", "【用量】", "【倪注】", "【炮制】", "味", "主"]
ACU_MARKERS = ["穴", "下针", "灸", "取穴", "络穴", "募穴", "俞穴", "寸", "近取", "远取", "禁刺", "禁灸", "骨之始"]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"(.)\1{2,}", r"\1", text.replace("\n", " "))


def snippet_around(q: str, needle: str, left=220, right=360) -> str:
    i = q.find(needle)
    if i < 0:
        return q[: left + right]
    return q[max(0, i-left): i+len(needle)+right]


def direct_score(kind: str, name: str, quote: str, source_file: str) -> int:
    q = normalized(quote)
    keys = [name]
    if kind == "herb":
        # common pinyin/variant item ids are handled by searched name only; avoid guessing aliases here.
        pass
    score = 0
    if name in q:
        score += 40
    snip = snippet_around(q, name)
    markers = HERB_MARKERS if kind == "herb" else ACU_MARKERS
    if any(m in snip for m in markers):
        score += 40
    if kind == "acupoint" and "针灸篇" in source_file:
        score += 20
    if kind == "herb" and "神农本草经" in source_file:
        score += 20
    if "····" in snip and len(snip) < 250:
        score -= 40
    if "目录" in snip[:100]:
        score -= 40
    return score


def find_best(corpus: SourceCorpus, kind: str, item_id: str, name: str):
    queries = [DIRECT_ALIAS.get(item_id, name)]
    if item_id == "jiangcan": queries.append("白僵蚕")
    if item_id == "gualou" or item_id == "gualue": queries += ["瓜蒌根", "瓜蒌实"]
    hits=[]
    for q in queries:
        for h in corpus.search(q, limit=8, context=420):
            d=h.to_dict(); d["searched_keyword"]=q
            d["direct_score"]=direct_score(kind, q, d.get("quote") or "", d.get("source_file") or "")
            hits.append(d)
    hits.sort(key=lambda d: d.get("direct_score",0), reverse=True)
    return hits[0] if hits else None


def apply_update(row: dict[str, Any], action: str, hit: dict[str, Any] | None, rationale: str):
    row["p7a_action"] = action
    row["p7a_rationale"] = rationale
    row["source_quality_policy"] = POLICY
    if action == "promoted_to_verified_direct":
        row["trace_status"] = "verified"
        row["source_quality_level"] = "verified_direct"
        row["source_refs"] = [{k: hit.get(k) for k in ["source_file", "page_num", "quote", "char_start", "char_end", "searched_keyword", "direct_score"]}]
    elif action == "demoted_false_positive_to_no_source":
        row["trace_status"] = "no_source_found"
        row["source_quality_level"] = "no_source"
        row["source_refs"] = []
        row["no_source_classification"] = "contextual_false_positive_demoted"
        row["no_source_reason"] = rationale
        row["next_action"] = "manual_review_or_external_source_policy"
    else:
        row["source_quality_level"] = "verified_contextual"
        row["trace_status"] = "verified"
        if hit and hit.get("direct_score", 0) > 0:
            row["source_refs"] = [{k: hit.get(k) for k in ["source_file", "page_num", "quote", "char_start", "char_end", "searched_keyword", "direct_score"]}]


def main() -> int:
    if "NIHAIXIA_SOURCE_DIR" not in os.environ:
        candidate = ROOT.parents[1] / "nihaixia" / "extracted"
        if candidate.exists(): os.environ["NIHAIXIA_SOURCE_DIR"] = str(candidate)
    corpus = SourceCorpus()
    if not corpus.available(): raise SystemExit("source corpus unavailable")

    verified = load_jsonl(DATA / "verified_sources.jsonl")
    decisions=[]
    for row in verified:
        if row.get("source_quality_level") != "verified_contextual": continue
        kind,item_id,name=row.get("kind"),row.get("item_id"),row.get("name")
        if (kind,item_id) in DIRECT_BAD:
            action="demoted_false_positive_to_no_source"; hit=None; rationale="P7-A: existing quote is numeric chapter/page noise, not a traceable item source"
        else:
            hit=find_best(corpus, kind, item_id, name)
            if hit and hit.get("direct_score",0) >= 90:
                action="promoted_to_verified_direct"; rationale="P7-A: re-search found direct item marker in Ni source corpus"
            else:
                action="kept_verified_contextual_with_rationale"; rationale="P7-A: quote mentions item but lacks conservative direct marker; retained as contextual trace only"
        apply_update(row, action, hit, rationale)
        decisions.append({"kind":kind,"item_id":item_id,"name":name,"action":action,"target":row.get("source_quality_level"),"source_file":(row.get("source_refs") or [{}])[0].get("source_file"),"score":(row.get("source_refs") or [{}])[0].get("direct_score")})

    write_jsonl(DATA / "verified_sources.jsonl", verified)
    verified_by_key={(r.get("kind"),r.get("item_id")):r for r in verified}

    # Sync indexes and completeness.
    for kind,id_key,path in INDEX_FILES:
        rows=load_jsonl(path)
        for r in rows:
            v=verified_by_key.get((kind,r.get(id_key)))
            if v and v.get("p7a_action"):
                for f in ["trace_status","source_refs","source_quality_level","source_quality_policy","p7a_action","p7a_rationale","no_source_classification","no_source_reason","next_action"]:
                    if f in v: r[f]=v[f]
        write_jsonl(path, rows)

    comp=load_jsonl(DATA / "knowledge_completeness.jsonl")
    for r in comp:
        v=verified_by_key.get((r.get("kind"),r.get("item_id")))
        if v and v.get("p7a_action"):
            for f in ["trace_status","source_quality_level","source_quality_policy","p7a_action","p7a_rationale","no_source_classification","no_source_reason","next_action"]:
                if f in v: r[f]=v[f]
            r["verified_in_registry"] = v.get("trace_status") == "verified"
            r["has_source_refs"] = bool(v.get("source_refs"))
    write_jsonl(DATA / "knowledge_completeness.jsonl", comp)

    # Demoted rows should leave verified registry.
    verified=[r for r in verified if not (r.get("p7a_action") == "demoted_false_positive_to_no_source")]
    write_jsonl(DATA / "verified_sources.jsonl", verified)

    counts=Counter(d["action"] for d in decisions)
    targets=Counter(d["target"] for d in decisions)
    lines=["# P35 / P7-A verified_contextual Tightening","","> 边界：只调整来源追溯等级与 rationale，不改写医学内容。","",f"- Processed: {len(decisions)}","","## Actions","","| action | count |","|---|---:|"]
    for k,v in sorted(counts.items()): lines.append(f"| `{k}` | {v} |")
    lines += ["","## Target levels","","| level | count |","|---|---:|"]
    for k,v in sorted(targets.items()): lines.append(f"| `{k}` | {v} |")
    lines += ["","## Decisions",""]
    for d in decisions: lines.append(f"- `{d['kind']}:{d['item_id']}` {d['name']} → `{d['target']}` ({d['action']}; score={d.get('score')}; {d.get('source_file')})")
    REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"processed":len(decisions),"actions":dict(counts),"targets":dict(targets),"report":str(REPORT.relative_to(ROOT))},ensure_ascii=False,indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
