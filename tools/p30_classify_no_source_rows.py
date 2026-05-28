#!/usr/bin/env python3
"""P30/P6 classify no_source rows into actionable policy buckets.

No source promotion and no medical content changes. This labels why an item is
no_source so future work can decide whether to re-search internal sources, add
external sources, or preserve as out-of-scope.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p30_no_source_classification.md"
QUEUE = DATA / "p30_no_source_classification.jsonl"
POLICY = "source_quality_is_traceability_only_not_medical_validation"

INDEX_FILES = [
    ("herb", "herb_id", DATA / "herb_index.jsonl"),
    ("acupoint", "acupoint_id", DATA / "acupoint_index.jsonl"),
]

# Items demoted in P5-B because verified registry had empty source_refs.
# They likely need internal re-search before external source expansion.
P5B_EMPTY_DEMOTED_REASON = "empty_quote_demoted_to_no_source"

EXTERNAL_HERB_HINTS = {
    # modern/local/common materia medica not expected in Ni Haixia core corpus
    "aidicha", "anxixiang", "banzhilian", "chuanyubeimu", "chuipencao", "chouwutong",
    "daidaihua", "diercao", "dijincao", "foshou", "gijingcao", "gouteng", "guya",
    "haifengteng", "haifushi", "haigeqiao", "haima", "haitongpi", "hamayou", "hongteng",
    "huangyaozi", "huazuirushi", "huoxiang", "huzhang", "jiangxiang", "jiguanhua",
    "jinguolan", "jinqiancao", "jiucaizi", "jixueteng", "laifuzi", "laoguancao",
    "leigongteng", "lianxu", "liujinu", "lulutong", "luobuma", "luobumaye", "luohanguo",
    "lvtuomei", "mabo", "machixian", "maqianzi", "menghua", "mohantian", "muhudie",
    "mujinpi", "niubangzi", "nuodaogenxu", "oujie", "poshi", "qianjinzi", "qiannianjian",
    "qianniuzi", "qishe", "sangshen", "sangye", "shandou", "shandougen", "shanzha",
    "shayuanzi", "shidi", "shiliupi", "shouwuteng", "suhexiang", "sumu", "suomu",
    "taizishen", "tanxiang", "tianzhuhuang", "tubiechong", "tujingpi", "xiangyuan",
    "xianhecao", "xianmao", "xiecao", "xihonghua", "xiqiancao", "xuelianhua", "xungufeng",
    "yadanzi", "yangjinhua", "yingsuqiao", "yubaifu", "yubaizi", "yuejihua", "yuganzi",
    "yuxingcao", "zhangnao", "zhechong", "zhenzhumu", "zhuli", "zhumagen", "zihuadiding",
    "zonglu", "zonglutan", "fanxieye", "baidoukou", "biandou", "bibo", "biba", "bichengqie",
    "caodoukou", "caoguo", "aoshu", "aoshugen", "hechezi", "heizhima", "hetaoren", "hezi",
    "feizi", "cansha", "cangerzi", "cijili", "gaoliangjiang", "guya", "hugulu", "roudoukou",
}

EXTERNAL_ACU_HINTS = {
    "ershenmen", "sishencong", "xiaji", "yaotongdian", "yaoyangguan", "fuyang2", "yinjiao_ren",
}

DUPLICATE_OR_ALIAS_HINTS = {
    "gualue", "huangbo", "hechezi", "heizhima", "hezi", "biba", "bichengqie", "luobuma",
    "yaoyangguan", "fuyang2", "yinjiao_ren",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def classify(kind: str, item_id: str, row: dict[str, Any]) -> tuple[str, str, str]:
    if row.get("p5b_resolution") == P5B_EMPTY_DEMOTED_REASON:
        return "internal_research_needed", "P5-B empty source_refs demotion; re-search raw Ni corpus before external expansion", "research_raw_source"
    if item_id in DUPLICATE_OR_ALIAS_HINTS:
        return "alias_or_duplicate_needs_mapping", "appears to be duplicate/variant naming; map to canonical item before source expansion", "review_alias_mapping"
    if kind == "herb" and item_id in EXTERNAL_HERB_HINTS:
        return "external_source_required", "not found in current Ni corpus; likely requires explicit external materia-medica source", "external_source_policy_required"
    if kind == "acupoint" and item_id in EXTERNAL_ACU_HINTS:
        return "external_source_required", "not found in current Ni corpus; likely extra/variant acupoint needing explicit external source", "external_source_policy_required"
    return "internal_research_needed", "no_source item not otherwise classified; re-search raw corpus and aliases first", "research_raw_source"


def main() -> int:
    # Use knowledge_completeness as canonical no_source inventory.
    rows = load_jsonl(DATA / "knowledge_completeness.jsonl")
    decisions = []
    by_key = {}
    for row in rows:
        key = (row.get("kind"), row.get("item_id"))
        if row.get("source_quality_level") != "no_source":
            by_key[key] = row
            continue
        kind = row.get("kind") or ""
        item_id = row.get("item_id") or ""
        cls, reason, next_action = classify(kind, item_id, row)
        row["no_source_classification"] = cls
        row["no_source_reason"] = reason
        row["next_action"] = next_action
        row["source_quality_policy"] = POLICY
        decisions.append({
            "kind": kind,
            "item_id": item_id,
            "name": row.get("name"),
            "file": row.get("file"),
            "no_source_classification": cls,
            "no_source_reason": reason,
            "next_action": next_action,
        })
        by_key[key] = row
    write_jsonl(DATA / "knowledge_completeness.jsonl", rows)
    write_jsonl(QUEUE, decisions)

    # Sync classification into indexes where present.
    for kind, id_key, path in INDEX_FILES:
        idx = load_jsonl(path)
        for row in idx:
            key = (kind, row.get(id_key))
            comp = by_key.get(key)
            if comp and comp.get("source_quality_level") == "no_source":
                for k in ["no_source_classification", "no_source_reason", "next_action"]:
                    row[k] = comp.get(k)
        write_jsonl(path, idx)

    counter = Counter(d["no_source_classification"] for d in decisions)
    by_kind = defaultdict(Counter)
    for d in decisions:
        by_kind[d["kind"]][d["no_source_classification"]] += 1

    lines = [
        "# P30 / P6 no_source Classification",
        "",
        "本报告将 no_source 条目分入后续治理队列。",
        "",
        "> 边界：只做分类，不引入新来源，不补写医学内容，不判断医学真实性或疗效。",
        "",
        f"- Classified no_source rows: {len(decisions)}",
        "",
        "## By classification",
        "",
        "| classification | count |",
        "|---|---:|",
    ]
    for k, v in sorted(counter.items()):
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "## By kind", "", "| kind | classification | count |", "|---|---|---:|"]
    for kind, c in sorted(by_kind.items()):
        for cls, count in sorted(c.items()):
            lines.append(f"| {kind} | `{cls}` | {count} |")
    lines += [
        "",
        "## Policy",
        "",
        "- `internal_research_needed`: 先重搜倪海厦原始 JSON/alias，不能直接外部补源。",
        "- `alias_or_duplicate_needs_mapping`: 先确认 canonical mapping，再决定是否同步 source_refs。",
        "- `external_source_required`: 当前倪师语料无来源；如要补内容必须建立外部来源白名单与引用字段。",
        "",
        f"Queue file: `{QUEUE.relative_to(ROOT)}`",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"classified": len(decisions), "by_classification": dict(counter), "by_kind": {k: dict(v) for k, v in by_kind.items()}, "queue": str(QUEUE.relative_to(ROOT)), "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
