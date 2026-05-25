#!/usr/bin/env python3
"""P8-E-2: 对 no_source_found 条目做扩展搜索，产出候选来源。

输入:
- data/review_queue.jsonl
- data/herb_sources.jsonl
- data/acupoint_sources.jsonl

输出:
- data/p8_e_no_source_expand_hits.jsonl
- report/p8_e_no_source_expand_hits.md

策略:
- 对 acupoint 命名变体（二/三/外/内/耳/足/腰）回退到主名搜索
- 对 herb 名称去常见后缀/常见别名前缀回退搜索
- 仅产出候选命中，不做 verified 决策
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "data" / "review_queue.jsonl"
HERB_SRC = ROOT / "data" / "herb_sources.jsonl"
ACU_SRC = ROOT / "data" / "acupoint_sources.jsonl"
HITS_PATH = ROOT / "data" / "p8_e_no_source_expand_hits.jsonl"
REPORT = ROOT / "report" / "p8_e_no_source_expand_hits.md"


def load_jsonl(path: Path) -> List[Dict]:
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def normalize_base_name(name: str, kind: str) -> List[Tuple[str, str]]:
    """返回 [(variant_keyword, base_name), ...] 用于扩展搜索。"""
    variants = []

    if kind == "acupoint":
        m = re.match(r"^(.*?)(二|三|上|下|外|内|耳|足|腰|头)(号|俞|腧)?$", name)
        if m:
            base = m.group(1)
            variants.append((f"acupoint_trim_variant:{m.group(2)}", base))

    if kind == "herb":
        # 去“叶/皮/仁/花/草/根/子”等常见后缀做广义检索
        m = re.match(r"^(.*?)(叶|皮|仁|花|草|根|子|壳|须|油|藤|片)$", name)
        if m:
            variants.append(("herb_trim_suffix", m.group(1)))

        # 繁简/常见混写回退
        mapping = [
            ("广藿香", "藿香"),
            ("川贝母", "贝母"),
            ("罗布麻叶", "罗布麻"),
        ]
        for src, dst in mapping:
            if name == src:
                variants.append(("herb_alias_fallback", dst))

    if not variants:
        variants.append(("identity", name))

    return variants


def index_by_name(records: List[Dict], name_key: str) -> Dict[str, List[Dict]]:
    idx: Dict[str, List[Dict]] = {}
    for r in records:
        for hit in r.get("source_hits") or []:
            for kw in ([r.get(name_key, ""), hit.get("matched_keyword", "")]):
                if not kw:
                    continue
                idx.setdefault(kw, []).append({"record": r, "hit": hit})
    return idx


def main():
    queue = [q for q in load_jsonl(QUEUE_PATH) if q.get("review_status") == "no_source_found"]
    herb_idx = index_by_name(load_jsonl(HERB_SRC), "herb_id")
    acu_idx = index_by_name(load_jsonl(ACU_SRC), "acupoint_id")

    results = []

    for item in queue:
        kind = item.get("kind")
        name = item.get("name") or ""
        if kind == "herb":
            idx = herb_idx
        elif kind == "acupoint":
            idx = acu_idx
        else:
            continue

        for reason, variant in normalize_base_name(name, kind):
            hits = idx.get(variant, [])
            if not hits:
                continue
            for h in hits[:3]:
                results.append({
                    "kind": kind,
                    "item_id": item.get("item_id"),
                    "name": name,
                    "search_variant": variant,
                    "expand_reason": reason,
                    "matched_hit": h["hit"],
                    "record_id": h["record"].get("herb_id") or h["record"].get("acupoint_id"),
                })

    # Write JSONL
    HITS_PATH.parent.mkdir(exist_ok=True)
    with HITS_PATH.open("w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Write report
    lines = [
        "# P8-E-2 no_source_found 扩展命中",
        "",
        "- 仅作候选，不直接 verified",
        "- 用于判断是否值得进入第二轮人工复核",
        "",
        f"## 总计: {len(results)}",
        "",
        "## 前 100 条",
        "",
        "| kind | item_id | name | expand_reason | search_variant | quality_score | matched_keyword |",
        "|------|---------|------|---------------|----------------|---------------|-----------------|",
    ]

    for r in results[:100]:
        hit = r["matched_hit"]
        lines.append(
            f"| {r['kind']} | {r['item_id']} | {r['name']} | {r['expand_reason']} | {r['search_variant']} | {hit.get('quality_score', '')} | {hit.get('matched_keyword', '')} |"
        )

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {HITS_PATH}")
    print(f"wrote {REPORT}")
    print(json.dumps({"expand_hits": len(results)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
