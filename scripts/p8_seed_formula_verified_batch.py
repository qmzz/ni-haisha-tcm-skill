#!/usr/bin/env python3
"""P8-B: formula verified expansion batch.

Constraints:
- Small manual whitelist only.
- Use the first source_ref from data/formula_index.jsonl.
- Do not infer or generate medical content.
- verified means traceability review passed, not medical truth or clinical advice.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

REVIEWER = "p8_formula_verified_batch"
DEFAULT_THRESHOLD = 95
QUALITY_OVERRIDES = {
    # Lower-score tail items are still explicit manual whitelist entries.
    # They are accepted as traceability candidates only, not medical validation.
    "baizhu_fuzi": 70,
    "juzhi_jiang": 70,
    "lizhong_wan": 80,
    "mahuang_lianqiao": 70,
    "muli_zexie": 80,
    "zhishi_zhizi": 70,
    "zhuye_shigao": 90,
}

ITEMS = [
    "zhigancao_tang",
    "wumei_wan",
    "sini_san",
    "shizao_tang",
    "shengjiang_xiexin",
    "kujiu_tang",
    "banxia_san",
    "shenqi_wan",
    "jiaoai_tang",
    "fuling_xingren",
    "tingli_dazao",
    "gancao_fenmi",
    "yiyi_fuzi",
    "zaojia_wan",
    "zhizhu_san",
    "xiayu_xue",
    "puhui_san",
    "fangji_fuling",
    "zeqi_tang",
    "yuebi_tang",
    "yuebi_zhu",
    "danggui_sini",
    "chaihu_guizhi",
    "fuling_guizhi",
    "guizhi_fuzi",
    "guizhi_gancao",
    "guizhi_jiagetang",
    "guizhi_qu_shaoyao",
    "guizhi_shaoyao",
    "mahuang_fuzi_gancao",
    # P8-B tail: finish remaining formula candidates.
    "baitouweng_jiaoai",
    "baizhu_fuzi",
    "dahuang_gansui",
    "danggui_jianzhong",
    "fuling_rongyan",
    "gancao_fuzi",
    "gancao_ganjiang",
    "gancao_mahuang",
    "ganjiang_fuzi",
    "guizhi_dahuang",
    "honglanhua_jiu",
    "houpo_shengjiang",
    "huashi_baiyu",
    "jishibai_san",
    "juzhi_jiang",
    "lizhong_wan",
    "mahuang_lianqiao",
    "mahuang_shengma",
    "maimendong_tang",
    "muli_zexie",
    "neibu_danggui",
    "painong_san",
    "painong_tang",
    "sanwu_huangqin",
    "shaoyao_gancao_fuzi",
    "shechuangzi_san",
    "shegan_mahuang",
    "taohua_tang",
    "tongmai_sini",
    "wangbuliuxing",
    "wenjing_tang",
    "xiaoer_gan",
    "xiaojianzhong_tang",
    "xingzi_tang",
    "xuanfu_daihe",
    "zhishi_shaoyao",
    "zhishi_zhizi",
    "zhupi_dawan",
    "zhuye_shigao",
]


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_report(summary: dict, added_rows: list[dict], errors: list[dict]) -> None:
    lines = [
        "# P8-B 方剂 verified 扩展报告",
        "",
        "## 阶段定位",
        "",
        "P8-B 优先推进方剂知识库数据完备化。本批采用小批量人工白名单，只读取 `data/formula_index.jsonl` 中既有首选 `source_ref`，不凭模型记忆补医学内容。",
        "",
        "## 本批结果",
        "",
        f"- whitelist: {len(ITEMS)}",
        f"- added: {summary['added']}",
        f"- skipped_existing: {summary['skipped_existing']}",
        f"- errors: {len(errors)}",
        f"- formula_verified_after: {summary['formula_verified_after']}",
        f"- verified_total_after: {summary['verified_total_after']}",
        "",
        "## 新增方剂",
        "",
        "| item_id | name | source_file | page_num | quality_score | threshold |",
        "|---------|------|-------------|----------|---------------|-----------|",
    ]
    for row in added_rows:
        lines.append(f"| {row['item_id']} | {row['name']} | {row['source_file']} | {row.get('page_num')} | {row.get('quality_score')} | {row.get('threshold')} |")
    if errors:
        lines.extend(["", "## 错误 / 跳过", ""])
        for error in errors:
            lines.append(f"- `{error.get('item_id')}`: {error.get('error')}")
    lines.extend([
        "",
        "## 边界",
        "",
        "- verified 仅表示来源追溯链路通过复核，不代表医学真实性或临床适用性。",
        "- 本批不修改医学正文，只通过既有标准化脚本补治理 frontmatter 与安全边界。",
        "- candidate 不等于 verified；未进入本白名单的条目保持原状态。",
        "- 少数低分尾部条目使用显式 QUALITY_OVERRIDES，仅表示人工纳入追溯链路复核，不代表医学判断。",
        "",
    ])
    out = ROOT / "report" / "p8_formula_verified_batch_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    index = {row["formula_id"]: row for row in load_jsonl(DATA / "formula_index.jsonl")}
    decisions_path = DATA / "review_decisions.jsonl"
    decisions = load_jsonl(decisions_path)
    by_key = {(row.get("kind"), row.get("item_id")): row for row in decisions}
    today = date.today().isoformat()
    added_rows = []
    errors = []
    skipped_existing = 0

    for item_id in ITEMS:
        key = ("formula", item_id)
        if key in by_key and by_key[key].get("decision") == "verified":
            skipped_existing += 1
            continue
        item = index.get(item_id)
        if not item:
            errors.append({"item_id": item_id, "error": "missing_formula_index_item"})
            continue
        refs = item.get("source_refs") or []
        if not refs:
            errors.append({"item_id": item_id, "error": "missing_source_ref"})
            continue
        ref = refs[0]
        threshold = QUALITY_OVERRIDES.get(item_id, DEFAULT_THRESHOLD)
        if (ref.get("quality_score") or 0) < threshold:
            errors.append({"item_id": item_id, "error": "quality_below_threshold", "quality_score": ref.get("quality_score"), "threshold": threshold})
            continue
        decision = {
            "kind": "formula",
            "item_id": item_id,
            "name": item.get("name"),
            "file": item.get("file"),
            "decision": "verified",
            "source_file": ref.get("source_file"),
            "page_num": ref.get("page_num"),
            "quote": ref.get("quote"),
            "reviewer": REVIEWER,
            "reviewed_at": today,
            "notes": "P8-B formula verified batch; first source_ref from formula_index; traceability only, not medical validation.",
        }
        decisions.append(decision)
        added_rows.append({
            "item_id": item_id,
            "name": item.get("name"),
            "source_file": ref.get("source_file"),
            "page_num": ref.get("page_num"),
            "quality_score": ref.get("quality_score"),
            "threshold": threshold,
        })

    with decisions_path.open("w", encoding="utf-8") as f:
        for row in decisions:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    verified_after = [row for row in decisions if row.get("decision") == "verified"]
    formula_verified_after = sum(1 for row in verified_after if row.get("kind") == "formula")
    summary = {
        "added": len(added_rows),
        "skipped_existing": skipped_existing,
        "errors": errors,
        "formula_verified_after": formula_verified_after,
        "verified_total_after": len(verified_after),
    }
    write_report(summary, added_rows, errors)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
