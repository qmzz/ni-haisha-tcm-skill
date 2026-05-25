#!/usr/bin/env python3
"""P8-E-3: 根据扩展命中生成候选白名单（自动 + 人工）。

输入:
- data/p8_e_no_source_expand_hits.jsonl
- data/review_queue.jsonl

输出:
- data/p8_e_3_auto_candidates.jsonl
- report/p8_e_3_auto_candidates.md

规则（保守）:
- acupoint:
  - 名称明显是主名变体（二/三/外/内）
  - 扩展命中 parent_name 存在
  - 最高命中 quality_score >= 74
- herb:
  - alias_fallback / trim_suffix 存在
  - 最高命中 quality_score >= 95
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
HITS_PATH = ROOT / "data" / "p8_e_no_source_expand_hits.jsonl"
QUEUE_PATH = ROOT / "data" / "review_queue.jsonl"
CAND_PATH = ROOT / "data" / "p8_e_3_auto_candidates.jsonl"
REPORT = ROOT / "report" / "p8_e_3_auto_candidates.md"


def load_jsonl(path: Path) -> List[Dict]:
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def best_hit_per_item(hits: List[Dict]) -> Dict[Tuple[str, str], Dict]:
    best: Dict[Tuple[str, str], Dict] = {}
    for h in hits:
        key = (h["kind"], h["item_id"])
        q = h.get("matched_hit", {}).get("quality_score", 0)
        if key not in best or q > (best[key].get("matched_hit", {}).get("quality_score", -1)):
            best[key] = h
    return best


def main():
    queue_map = {(q.get("kind"), q.get("item_id")): q for q in load_jsonl(QUEUE_PATH)}
    best = best_hit_per_item(load_jsonl(HITS_PATH))

    auto = []
    manual = []

    for (kind, item_id), hit in sorted(best.items()):
        score = hit.get("matched_hit", {}).get("quality_score", 0)
        reason = hit.get("expand_reason", "")
        q = queue_map.get((kind, item_id), {})

        if kind == "acupoint" and "acupoint_trim_variant" in reason and score >= 74:
            auto.append({**hit, "category": "auto_accept_variant_acupoint"})
        elif kind == "herb" and reason in {"herb_alias_fallback", "herb_trim_suffix"} and score >= 95:
            auto.append({**hit, "category": "auto_accept_alias_herb"})
        else:
            manual.append({**hit, "category": "needs_manual_review"})

    CAND_PATH.parent.mkdir(exist_ok=True)
    with CAND_PATH.open("w", encoding="utf-8") as f:
        for r in auto + manual:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    lines = [
        "# P8-E-3 候选白名单",
        "",
        "- 自动候选：acupoint 变体 parent_name >= 74；herb alias >= 95",
        "- 其余命中进入人工复核",
        "",
        f"## auto: {len(auto)}",
        "",
        "| kind | item_id | name | expand_reason | quality_score |",
        "|------|---------|------|---------------|---------------|",
    ]

    for r in auto:
        lines.append(f"| {r['kind']} | {r['item_id']} | {r['name']} | {r['expand_reason']} | {r['matched_hit']['quality_score']} |")

    lines += ["", f"## manual: {len(manual)}", ""]
    lines.append("| kind | item_id | name | expand_reason | quality_score |")
    lines.append("|------|---------|------|---------------|---------------|")
    for r in manual[:100]:
        lines.append(f"| {r['kind']} | {r['item_id']} | {r['name']} | {r['expand_reason']} | {r['matched_hit']['quality_score']} |")

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {CAND_PATH}")
    print(f"wrote {REPORT}")
    print(json.dumps({"auto": len(auto), "manual": len(manual)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
