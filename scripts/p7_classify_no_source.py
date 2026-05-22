#!/usr/bin/env python3
"""P7-A：no_source_found 分类治理。

只做分类和候选建议，不自动修改 alias，不自动 verified。
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "no_source_classification.jsonl"
REPORT = ROOT / "report" / "p7_no_source_classification.md"

ACU_SUFFIXES = ["穴", "穴位"]
HERB_SUFFIXES = ["子", "皮", "根", "花", "草", "仁", "叶", "藤", "实", "石", "香", "木", "粉", "胶"]

MANUAL_ALIAS_HINTS = {
    ("herb", "haitongpi"): ["刺桐皮"],
    ("herb", "zhangnao"): ["韶脑"],
    ("herb", "zihuadiding"): ["地丁"],
    ("acupoint", "sishencong"): ["四神聪穴"],
}


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_alias_candidates():
    rows = load_jsonl(DATA / "alias_candidates.jsonl")
    by_key = {}
    for row in rows:
        by_key.setdefault((row.get("kind"), row.get("item_id")), []).append(row.get("alias"))
    for key, hints in MANUAL_ALIAS_HINTS.items():
        by_key.setdefault(key, [])
        for hint in hints:
            if hint not in by_key[key]:
                by_key[key].append(hint)
    return by_key


def classify(item, alias_map):
    kind = item.get("kind")
    item_id = item.get("item_id")
    name = item.get("name") or ""
    aliases = [a for a in alias_map.get((kind, item_id), []) if a]
    signals = []
    category = "no_obvious_lead"

    if aliases:
        category = "alias_candidate"
        signals.append("has_alias_candidate")
    elif kind == "acupoint":
        category = "acupoint_name_variant"
        aliases = [name + suffix for suffix in ACU_SUFFIXES if name and not name.endswith(suffix)]
        signals.append("suggest_acupoint_suffix_alias")
    elif kind == "herb":
        suffix_hit = [suffix for suffix in HERB_SUFFIXES if name.endswith(suffix)]
        if suffix_hit:
            category = "herb_name_review"
            signals.append("herb_suffix_name")
        if any(ch in name for ch in ["藿", "薢", "蒺", "苁", "萹", "螵", "蛸"]):
            signals.append("rare_character_check")
        aliases = []

    return {
        "kind": kind,
        "item_id": item_id,
        "name": name,
        "file": item.get("file"),
        "review_status": item.get("review_status"),
        "category": category,
        "suggested_aliases": aliases[:5],
        "signals": signals,
        "action": "manual_alias_review" if category == "alias_candidate" else ("add_acupoint_suffix_alias_candidate" if category == "acupoint_name_variant" else "manual_source_review"),
        "source_policy": "classification_only_not_verified",
    }


def main():
    DATA.mkdir(exist_ok=True)
    REPORT.parent.mkdir(exist_ok=True)
    queue = load_jsonl(DATA / "review_queue.jsonl")
    no_source = [r for r in queue if r.get("review_status") == "no_source_found"]
    alias_map = load_alias_candidates()
    rows = [classify(item, alias_map) for item in no_source]

    with OUT.open("w", encoding="utf-8") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")

    kind_counts = Counter(r["kind"] for r in rows)
    category_counts = Counter(r["category"] for r in rows)
    action_counts = Counter(r["action"] for r in rows)

    lines = [
        "# P7-A no_source_found 分类治理报告",
        "",
        "## 原则",
        "",
        "- 本报告只做分类与候选建议，不自动修改 alias。",
        "- 分类结果不等于 verified。",
        "- 找不到明确来源时保持 no_source_found / 待复核。",
        "",
        "## 总览",
        "",
        f"- no_source_found 条目：{len(rows)}",
        "",
        "### kind 分布",
        "",
    ]
    for key, count in sorted(kind_counts.items()):
        lines.append(f"- {key}: {count}")
    lines.extend(["", "### 分类分布", ""])
    for key, count in sorted(category_counts.items()):
        lines.append(f"- {key}: {count}")
    lines.extend(["", "### 建议动作分布", ""])
    for key, count in sorted(action_counts.items()):
        lines.append(f"- {key}: {count}")

    lines.extend([
        "",
        "## alias candidate 样例",
        "",
        "| kind | item_id | name | suggested_aliases | action |",
        "|------|---------|------|-------------------|--------|",
    ])
    for row in [r for r in rows if r["category"] == "alias_candidate"][:30]:
        lines.append(f"| {row['kind']} | {row['item_id']} | {row['name']} | {', '.join(row['suggested_aliases'])} | {row['action']} |")

    lines.extend([
        "",
        "## 全量分类样例（前 80 条）",
        "",
        "| kind | item_id | name | category | signals |",
        "|------|---------|------|----------|---------|",
    ])
    for row in rows[:80]:
        lines.append(f"| {row['kind']} | {row['item_id']} | {row['name']} | {row['category']} | {', '.join(row['signals'])} |")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT.relative_to(ROOT)),
        "report": str(REPORT.relative_to(ROOT)),
        "total": len(rows),
        "kind_counts": dict(kind_counts),
        "category_counts": dict(category_counts),
        "action_counts": dict(action_counts),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
