#!/usr/bin/env python3
"""P8-C: herb verified expansion batch.

Constraints:
- Small manual whitelist only.
- Use the first source_ref from data/herb_index.jsonl.
- Do not infer or generate medical content.
- verified means traceability review passed, not medical truth or clinical advice.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p8_herb_verified_batch_report.md"

REVIEWER = "p8_herb_verified_batch"
DEFAULT_THRESHOLD = 95
QUALITY_OVERRIDES: dict[str, int] = {
    # Mid-score tail items are explicit manual whitelist entries.
    # They are accepted as traceability candidates only, not medical validation.
    "dongchongxiacao": 90,
    "gejie": 90,
    "meiguihua": 90,
    "nanguazi": 90,
    "zhuru": 90,
}

ITEMS = [
    "zisu",
    "zicao",
    "zhusha",
    "zhuling",
    "zhizi",
    "zhebeimu",
    "zaojiaoci",
    "zaojia",
    "yuyuliang",
    "yujin",
    "yuanzhi",
    "yiyiren",
    "yitang",
    "yinyanghuo",
    "yimucao",
    "yangqishi",
    "xuduan",
    "xuanshen",
    "xuanfuhua",
    "xionghuang",
    "xinyi",
    "xiaoji",
    "xiangru",
    "xiakucao",
    "wuyi",
    "wuyaozi",
    "wujiapi",
    "wugong",
    "tujuzi",
    "tianma",
    # P8-C high-score tail: remaining herb candidates with first source_ref quality_score >= 95.
    "aoye",
    "baijiangcao",
    "baijiezi",
    "baimaogen",
    "baiqian",
    "bajitian",
    "bianxu",
    "bixie",
    "cebaiye",
    "changshan",
    "changshanmiao",
    "chantui",
    "chishizhi",
    "chuanshanjia",
    "chuanwu",
    "cishi",
    "ciweipi",
    "dafupi",
    "daizheshi",
    "danfan",
    "diji",
    "dilong",
    "diyu",
    "duhuo",
    "fangfeng",
    "fengfang",
    "fengmi",
    "fupenzi",
    "fuxiaomai",
    "gaoben",
    "gegen",
    "gongcao",
    "gouqizi",
    "guadi",
    "gualue",
    "guiban",
    "gusuibu",
    "haizaomu",
    "hehuanpi",
    "huaihua",
    "huaijiao",
    "huangbai",
    "huangjing",
    "huashi",
    "huomaren",
    "hupo",
    "jiangcan",
    "jili",
    "jineijin",
    "jingjie",
    "jinyingzi",
    "jinyinhua",
    "juemingzi",
    "juhua",
    "kualianpi",
    "kuandonghua",
    "kulianpi",
    "kunbu",
    "kushen",
    "leiwan",
    "lianzi",
    "lingxiaohua",
    "lingyangjiao",
    "lingzhi",
    "liuhuang",
    "longdancao",
    "lujiao",
    "lujiaoshuang",
    "luoshiteng",
    "lurong",
    "madouling",
    "mahuanggen",
    "maiya",
    "manjingzi",
    "mengchong",
    "mengshi",
    "mingfan",
    "mugua",
    "muxiang",
    "niuhuang",
    "niuxi",
    "nvzhenzi",
    "paojiang",
    "peilan",
    "pipaye",
    "puhuang",
    "qiancao",
    "qianghuo",
    "qianshi",
    "qingxiangzi",
    "qinjiao",
    "qinpi",
    "quanxie",
    "rougui",
    "rousuirong",
    "sangbaipi",
    "sangjisheng",
    "sangpiaoxiao",
    "sangzhi",
    "sanleng",
    "sanyu",
    "shanglu",
    "shanzhuyu",
    "shashen",
    "shechuangzi",
    "shegan",
    "shengma",
    "shenjincao",
    "shenqu",
    "shexiang",
    "shichangpu",
    "shijunzi",
    "shixiaoming",
    "shizhangzi",
    "shuizhi",
    "songjie",
    "suanzaoren",
    "suoyang",
    "suzi",
    "taoren",
    "wubeizi",
    "wushaoshe",
    "wuweizi",
    "xueyutan",
    "zaoxintu",
    "zhongruzi",
    "ziheche",
    "zirun",
    "zisuan",
    # P8-C mid-score tail: remaining herb candidates with first source_ref quality_score >= 90.
    "dongchongxiacao",
    "gejie",
    "meiguihua",
    "nanguazi",
    "zhuru",
]


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_report(summary: dict, added_rows: list[dict], errors: list[dict]) -> None:
    lines = [
        "# P8-C 药材 verified 扩展报告",
        "",
        "## 阶段定位",
        "",
        "P8-C 启动药材知识库数据完备化。本批采用小批量人工白名单，只读取 `data/herb_index.jsonl` 中既有首选 `source_ref`，不凭模型记忆补医学内容。",
        "",
        "## 本批结果",
        "",
        f"- whitelist: {summary['whitelist']}",
        f"- added: {summary['added']}",
        f"- skipped_existing: {summary['skipped_existing']}",
        f"- errors: {len(errors)}",
        f"- herb_verified_after: {summary['herb_verified_after']}",
        f"- verified_total_after: {summary['verified_total_after']}",
        "",
        "## 新增药材",
        "",
        "| item_id | name | source_file | page_num | quality_score | threshold |",
        "|---------|------|-------------|----------|---------------|-----------|",
    ]
    for row in added_rows:
        lines.append(
            f"| {row['item_id']} | {row['name']} | {row['source_file']} | {row.get('page_num')} | {row['quality_score']} | {row['threshold']} |"
        )
    if not added_rows:
        lines.append("| - | - | - | - | - | - |")
    lines += [
        "",
        "## 边界",
        "",
        "- verified 仅表示来源追溯链路通过复核，不代表医学真实性或临床适用性。",
        "- 本批不修改医学正文，只通过既有标准化脚本补治理 frontmatter 与安全边界。",
        "- candidate 不等于 verified；未进入本白名单的条目保持原状态。",
        "- quality_score 仅用于治理排序和复核优先级，不等于医学真实性判定。",
    ]
    if errors:
        lines += ["", "## 未通过条目", "", "| item_id | error | quality_score | threshold |", "|---------|-------|---------------|-----------|"]
        for err in errors:
            lines.append(f"| {err['item_id']} | {err['error']} | {err.get('quality_score')} | {err.get('threshold')} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    index = {row["herb_id"]: row for row in load_jsonl(DATA / "herb_index.jsonl")}
    decisions_path = DATA / "review_decisions.jsonl"
    decisions = load_jsonl(decisions_path)
    by_key = {(row.get("kind"), row.get("item_id")): row for row in decisions}
    today = date.today().isoformat()
    added_rows = []
    errors = []
    skipped_existing = 0

    for item_id in ITEMS:
        key = ("herb", item_id)
        if key in by_key and by_key[key].get("decision") == "verified":
            skipped_existing += 1
            continue
        item = index.get(item_id)
        if not item:
            errors.append({"item_id": item_id, "error": "missing_herb_index_item"})
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
        decisions.append({
            "kind": "herb",
            "item_id": item_id,
            "name": item.get("name"),
            "file": item.get("file"),
            "decision": "verified",
            "source_file": ref.get("source_file"),
            "page_num": ref.get("page_num"),
            "quote": ref.get("quote"),
            "reviewer": REVIEWER,
            "reviewed_at": today,
            "notes": "P8-C herb verified batch; first source_ref from herb_index; traceability only, not medical validation.",
        })
        added_rows.append({"item_id": item_id, "name": item.get("name"), "source_file": ref.get("source_file"), "page_num": ref.get("page_num"), "quality_score": ref.get("quality_score"), "threshold": threshold})

    decisions_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in decisions) + "\n", encoding="utf-8")
    verified_after = [row for row in decisions if row.get("decision") == "verified"]
    summary = {
        "whitelist": len(ITEMS),
        "added": len(added_rows),
        "skipped_existing": skipped_existing,
        "errors": errors,
        "herb_verified_after": sum(1 for row in verified_after if row.get("kind") == "herb"),
        "verified_total_after": len(verified_after),
    }
    write_report(summary, added_rows, errors)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
