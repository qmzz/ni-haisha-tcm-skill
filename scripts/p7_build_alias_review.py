#!/usr/bin/env python3
"""P7-B：alias/synonym 治理增强。

从 P7-A 分类结果生成 alias review 文件；默认不修改 data/aliases.json。
使用 --apply-safe 可仅应用 safe_alias 项。
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REVIEW = DATA / "alias_review.jsonl"
REPORT = ROOT / "report" / "p7_alias_review.md"
ALIASES = DATA / "aliases.json"

SAFE_MANUAL = {
    ("herb", "海桐皮", "刺桐皮"),
    ("herb", "樟脑", "韶脑"),
    ("herb", "紫花地丁", "地丁"),
    ("acupoint", "四神聪", "四神聪穴"),
}


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_aliases():
    if not ALIASES.exists():
        return {"formula": {}, "herb": {}, "acupoint": {}}
    return json.loads(ALIASES.read_text(encoding="utf-8"))


def decision_for(row, alias):
    key = (row.get("kind"), row.get("name"), alias)
    if key in SAFE_MANUAL:
        return "safe_alias"
    if row.get("category") == "acupoint_name_variant" and alias == (row.get("name") or "") + "穴":
        return "needs_manual_review"
    return "needs_manual_review"


def build_rows():
    classification = load_jsonl(DATA / "no_source_classification.jsonl")
    rows = []
    for row in classification:
        for alias in row.get("suggested_aliases") or []:
            rows.append({
                "kind": row.get("kind"),
                "item_id": row.get("item_id"),
                "name": row.get("name"),
                "alias": alias,
                "decision": decision_for(row, alias),
                "source": "p7_no_source_classification",
                "notes": "alias 仅用于提升检索召回；命中后仍需 review，不自动 verified。",
            })
    return rows


def apply_safe(rows):
    aliases = load_aliases()
    changed = 0
    for row in rows:
        if row.get("decision") != "safe_alias":
            continue
        kind = row["kind"]
        name = row["name"]
        alias = row["alias"]
        aliases.setdefault(kind, {})
        aliases[kind].setdefault(name, [])
        if alias not in aliases[kind][name]:
            aliases[kind][name].append(alias)
            changed += 1
    if changed:
        ALIASES.write_text(json.dumps(aliases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main():
    apply = "--apply-safe" in sys.argv
    rows = build_rows()
    with REVIEW.open("w", encoding="utf-8") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    changed = apply_safe(rows) if apply else 0
    counts = Counter(row["decision"] for row in rows)
    by_kind = Counter(row["kind"] for row in rows)

    lines = [
        "# P7-B alias / synonym 复核报告",
        "",
        "## 原则",
        "",
        "- alias 用于扩大来源检索召回。",
        "- alias hit 只能进入 candidate / needs_review，不自动 verified。",
        "- 默认只生成 review 文件；`--apply-safe` 只应用白名单 safe_alias。",
        "",
        "## 总览",
        "",
        f"- alias review rows: {len(rows)}",
        f"- apply_safe: {apply}",
        f"- aliases_changed: {changed}",
        "",
        "### decision 分布",
        "",
    ]
    for key, count in sorted(counts.items()):
        lines.append(f"- {key}: {count}")
    lines.extend(["", "### kind 分布", ""])
    for key, count in sorted(by_kind.items()):
        lines.append(f"- {key}: {count}")
    lines.extend(["", "## review 样例", "", "| kind | item_id | name | alias | decision |", "|------|---------|------|-------|----------|"])
    for row in rows[:80]:
        lines.append(f"| {row['kind']} | {row['item_id']} | {row['name']} | {row['alias']} | {row['decision']} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "review": str(REVIEW.relative_to(ROOT)),
        "report": str(REPORT.relative_to(ROOT)),
        "rows": len(rows),
        "decision_counts": dict(counts),
        "by_kind": dict(by_kind),
        "apply_safe": apply,
        "aliases_changed": changed,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
