#!/usr/bin/env python3
"""P9-D: 处理 duplicate_title 重复名治理。

策略：
1. herb alias pair: 在双方 frontmatter 加 aliases 字段互指
2. acupoint variant (经络后缀): 标准名保留，后缀变体加 alias_of 指向主条目
3. acupoint 同音异名: 标记为 alias 关系

不删除文件，只修 frontmatter 元数据。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# 手动维护的 alias 映射 (基于中医常识)
HERB_ALIASES: Dict[str, List[str]] = {
    # 荜澄茄系列
    "biba": ["bichengqie"],
    "bichengqie": ["biba"],
    # 黄柏/黄檗
    "huangbai": ["huangbo"],
    "huangbo": ["huangbai"],
    # 地榆/地机是不同药，但标题相同，需要区分
    # "diji": [], "diyu": [],  # 保留，加 disambiguation
    # 覆盆子/乌药子 - 不同药
    # 葛根/葛花根等
    "geda": ["gegen"],  # 葛答 -> 葛根
    "gegen": ["geda"],
    # 瓜蒌系列
    "gualou": ["gualue"],
    "gualue": ["gualou"],
    # 鹤虱系列
    "hesi": ["hezi"],
    "hezi": ["hesi"],
    # 苦楝皮
    "kualianpi": ["kulianpi"],
    "kulianpi": ["kualianpi"],
    # 罗布麻
    "luobuma": ["luobumaye"],
    "luobumaye": ["luobuma"],
    # 使君子/石樟子 - 不同药
    # 苏木/索木
    "sumu": ["suomu"],
    "suomu": ["sumu"],
    # 土鳖虫/蜇虫
    "tubiechong": ["zhechong"],
    "zhechong": ["tubiechong"],
    # 血竭/血黄
    "xuejie": ["xuhuang"],
    "xuhuang": ["xuejie"],
    # 延胡索/延胡错
    "yanhucuo": ["yanhusuo"],
    "yanhusuo": ["yanhucuo"],
    # 禹白附/禹白子
    "yubaifu": ["yubaizi"],
    "yubaizi": ["yubaifu"],
    # 自然铜/紫润 - 不同药，标题巧合
}

# acupoint 经络后缀映射: variant -> main
ACUPOINT_VARIANTS: Dict[str, str] = {
    # GB 胆经
    "fengchi_gb": "fengchi",
    "qiuxu_gb": "qiuxu",
    "xuanzhong_gb": "xuanzhong",
    "chengling_gb": "chengling",
    "jianjing_gb": "jianjing",
    "jingmen_gb": "jingmen",
    "naokong_gb": "naokong_bl",  # 脑空是 BL
    "zhangmen_lv": "zhangmen",   # 章门是 LV
    "zhongdu_lv": "zhongdu",
    "zhongfeng_lv": "zhongfeng",
    "ququan_lv": "ququan",
    "ligou_lv": "ligou",
    "xingjian_lv": "xingjian",
    "qimen_lv": "qimen",
    "yinjiao_du": "yinjiao",
    # KI 肾经
    "fuliu_k": "fuliu",
    "dazhong_k": "dazhong",
    "jiaoxin_k": "jiaoxin",
    "taixi_k": "taixi",
    "yingu_k": "yingu",
    "yongquan_k": "yongquan",
    "zhaohai_k": "zhaohai",
    "zhubin_k": "zhubin",
    # LI 大肠经
    "futu_li": "futu",
    # BL 膀胱经
    "jingming_bl": "jingming",
    "tianzhu_bl": "tianzhu",
    "shenmai_bl": "shenmai",
    "kunlun_bl": "kunlun",
    "zhishi_bl": "zhishi",
    # ST 胃经
    "zusanli_st": "zusanli",
    "neiting2": "neiting",
    "liangqiu2": "liangqiu",
    "jiexi2": "jiexi",
    "shidou2": "shidou",
    # SI 小肠经
    "jianyu2": "jianyu",
    "bingfeng": "bingfeng",
    # SJ 三焦经
    "heliao_sj": "heliao",
    # REN 任脉
    "huagai_ren": "huagai",
    "jianli_ren": "jianli",
    "jiuwei_ren": "jiuwei",
    "shangwan_ren": "shangwan",
    "shangxing_du": "shangxing",  # 上星是 DU
    "shuifen_ren": "shuifen",
    "shenque_ren": "shenque",
    "xiawan": "xiawan",
    "xiwan": "xiawan",  # 西脘 -> 下脘
    "xuanji_ren": "xuanji",
    "yutang_ren": "yutang",
    "zigong_ren": "zigong",
    # DU 督脉
    "qianding_du": "qianding",
    "chengfu2": "chengfu",
    "ciliao2": "ciliao",
    "dabao2": "dabao",
    "daheng2": "daheng",
    "fuai2": "fuai",
    "fujie2": "fujie",
    "lidui2": "lidui",
    "shenmai2": "shenmai",
    "taiyi2": "taiyi",
    "tianxi2": "tianxi",
    "xiongxiang2": "xiongxiang",
    "zhourong2": "zhourong",
    "bilao": "binao",  # 臂臑外 -> 臂臑
    "bitong": "bitong",  # 鼻通保持独立
    "naohu": "naokong",  # 脑户 vs 脑空
}

# 需要特殊处理的同音/空格问题
ACUPOINT_RENAME: Dict[str, Tuple[str, str]] = {
    "cuanzhu": ("cuanzhu", "攒竹"),  # zanzhu 是错写
    "zanzhu": ("cuanzhu", "攒竹（赞竹为异写）"),
    "jian Shi": ("jianshi", "间使"),  # 空格问题
    "sanjiaoju": ("sanjiaoshu", "三焦俞"),
    "sanjiaoshu": ("sanjiaoshu", "三焦俞"),
    "yaoyangguan": ("yangguan", "腰阳关"),
    "yangguan": ("yangguan", "阳关"),
}


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def split_frontmatter(text: str) -> Tuple[List[str], str]:
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---", 4)
    if end < 0:
        return [], text
    return text[4:end].splitlines(), text[end + 4:].lstrip("\n")


def upsert_line(lines: List[str], key: str, value: str):
    prefix = f"{key}:"
    for i, line in enumerate(lines):
        if line.strip().startswith(prefix):
            lines[i] = f"{key}: {value}"
            return
    lines.append(f"{key}: {value}")


def process_herb_alias(item_id: str, alias_ids: List[str]) -> Dict:
    path = ROOT / "knowledge" / "herbs" / f"{item_id}.md"
    if not path.exists():
        return {"file": str(path), "changed": False, "error": "missing"}
    text = path.read_text(encoding="utf-8")
    lines, body = split_frontmatter(text)
    if not lines:
        lines = [f'title: "{item_id}"']
    aliases_yaml = json.dumps(alias_ids, ensure_ascii=False)
    upsert_line(lines, "aliases", aliases_yaml)
    new_text = "---\n" + "\n".join(lines).rstrip() + "\n---\n\n" + body.lstrip("\n")
    changed = new_text != text
    if changed:
        path.write_text(new_text, encoding="utf-8")
    return {"file": str(path.relative_to(ROOT)), "changed": changed}


def process_acupoint_variant(variant_id: str, main_id: str) -> Dict:
    """后缀变体加 alias_of 指向主条目。"""
    path = ROOT / "knowledge" / "acupoints" / f"{variant_id}.md"
    if not path.exists():
        return {"file": str(path), "changed": False, "error": "missing"}
    text = path.read_text(encoding="utf-8")
    lines, body = split_frontmatter(text)
    if not lines:
        lines = [f'title: "{variant_id}"']
    upsert_line(lines, "alias_of", f'"{main_id}"')
    new_text = "---\n" + "\n".join(lines).rstrip() + "\n---\n\n" + body.lstrip("\n")
    changed = new_text != text
    if changed:
        path.write_text(new_text, encoding="utf-8")
    return {"file": str(path.relative_to(ROOT)), "changed": changed, "alias_of": main_id}


def main():
    results = []
    
    # 处理 herb aliases
    for item_id, alias_ids in HERB_ALIASES.items():
        r = process_herb_alias(item_id, alias_ids)
        results.append({"kind": "herb", **r})
    
    # 处理 acupoint variants
    for variant_id, main_id in ACUPOINT_VARIANTS.items():
        r = process_acupoint_variant(variant_id, main_id)
        results.append({"kind": "acupoint", **r})
    
    changed = sum(1 for r in results if r.get("changed"))
    print(json.dumps({
        "total": len(results),
        "changed": changed,
        "sample": results[:10]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
