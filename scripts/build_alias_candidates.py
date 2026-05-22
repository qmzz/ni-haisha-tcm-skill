#!/usr/bin/env python3
"""P4-B：为 no_source_found 条目生成二次 alias 候选。"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "alias_candidates.md"

MANUAL_CANDIDATES = {
    "herb": {
        "青蒿": ["草蒿", "香蒿"],
        "贯众": ["贯节", "贯渠"],
        "紫花地丁": ["地丁"],
        "败酱草": ["败酱"],
        "络石藤": ["络石"],
        "石韦": ["石皮"],
        "海金沙": ["金沙藤"],
        "萹蓄": ["扁蓄"],
        "瞿麦": ["巨句麦"],
        "灯心草": ["灯草"],
        "地肤子": ["地肤"],
        "海桐皮": ["刺桐皮"],
        "秦皮": ["梣皮"],
        "白薇": ["薇草"],
        "银柴胡": ["银胡"],
        "胡黄连": ["胡连"],
        "瓦楞子": ["瓦垄子"],
        "僵蚕": ["白僵蚕"],
        "全蝎": ["全虫"],
        "蜈蚣": ["天龙"],
        "龙骨": ["青龙骨"],
        "牡蛎": ["左牡蛎"],
        "磁石": ["慈石"],
        "代赭石": ["赭石"],
        "自然铜": ["石髓铅"],
        "血竭": ["麒麟竭"],
        "乳香": ["熏陆香"],
        "没药": ["末药"],
        "儿茶": ["孩儿茶"],
        "硼砂": ["鹏砂"],
        "炉甘石": ["甘石"],
        "轻粉": ["水银粉"],
        "砒石": ["砒霜"],
        "雄黄": ["黄金石"],
        "硫黄": ["硫磺"],
        "铅丹": ["黄丹"],
        "密陀僧": ["没多僧"],
        "樟脑": ["韶脑"],
        "冰片": ["龙脑"],
        "麝香": ["当门子"]
    },
    "acupoint": {
        "印堂": ["印堂穴"],
        "太阳": ["太阳穴"],
        "夹脊": ["华佗夹脊", "夹脊穴"],
        "四神聪": ["四神聪穴"],
        "子宫": ["子宫穴"],
        "十宣": ["十宣穴"],
        "鹤顶": ["鹤顶穴"],
        "阑尾": ["阑尾穴"],
        "胆囊": ["胆囊穴"],
        "腰眼": ["腰眼穴"],
        "定喘": ["定喘穴"]
    }
}


def load_jsonl(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    queue = load_jsonl(DATA / "review_queue.jsonl")
    rows = []
    for item in queue:
        if item.get("review_status") != "no_source_found":
            continue
        kind = item.get("kind")
        name = item.get("name")
        aliases = MANUAL_CANDIDATES.get(kind, {}).get(name, [])
        for alias in aliases:
            rows.append({
                "kind": kind,
                "item_id": item.get("item_id"),
                "name": name,
                "alias": alias,
                "alias_source": "manual_candidate",
                "confidence": "medium",
                "status": "candidate_only",
            })
    out = DATA / "alias_candidates.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    REPORT.parent.mkdir(exist_ok=True)
    lines = ["# Alias Candidates", "", f"候选数：{len(rows)}", "", "| kind | name | alias | confidence |", "|------|------|-------|------------|"]
    for row in rows:
        lines.append(f"| {row['kind']} | {row['name']} | {row['alias']} | {row['confidence']} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    print(f"wrote {REPORT}")
    print(f"alias candidates: {len(rows)}")


if __name__ == "__main__":
    main()
