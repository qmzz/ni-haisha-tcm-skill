#!/usr/bin/env python3
"""P9-E: 处理剩余 15 组 duplicate_title。

基于 index 数据的真实分析：

Herb (7 组) - 同一药材不同名称：
- aishe/aoye: 艾舍 -> 艾叶 (aoye 是标准名)
- aoshugen/nuodaogenxu: 糯稻根须的不同写法 (nuodaogenxu 更完整)
- diji/diyu: 地机 -> 地榆 (diyu 是标准名)
- fupenzi/wuyaozi: 覆盆子/乌药子 (fupenzi 是标准名)
- guya/shandou: 谷芽/山豆 (guya 是标准名)
- hechezi/heizhima: 鹤虱子/黑芝麻 (heizhima 是标准名)
- shijunzi/shizhangzi: 使君子/石樟子 (shijunzi 是标准名)
- zirantong/zirun: 自然铜/紫润 (zirantong 是标准名)

Acupoint (8 组) - 异写/别名/经络后缀：
- cuanzhu/zanzhu: 攒竹/赞竹 (cuanzhu 是标准名, zanzhu 是异写)
- jian Shi/jianshi: 间使/间使 (jian Shi 有空格问题)
- sanjiaoju/sanjiaoshu: 三焦俞/三焦输 (sanjiaoju 是标准名)
- taichong/taichong_lv: 太冲/太冲(LV) (taichong 是标准名)
- xiabai/xiamen: 侠白/侠门 (xiabai 是标准名)
- yangguan/yaoyangguan: 阳关/腰阳关 (yaoyangguan 是标准名)
- zulinqi/zulinqi_gb: 足临泣/足临泣(GB) (zulinqi 是标准名)

治理：标准名保留，别名加 alias_of 指向标准名。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

# 标准名 -> 别名列表
HERB_STANDARD: Dict[str, List[str]] = {
    "aoye": ["aishe"],           # 艾叶 <- 艾舍
    "nuodaogenxu": ["aoshugen"], # 糯稻根须 <- 糯稻根
    "diyu": ["diji"],            # 地榆 <- 地机
    "fupenzi": ["wuyaozi"],      # 覆盆子 <- 乌药子
    "guya": ["shandou"],         # 谷芽 <- 山豆
    "heizhima": ["hechezi"],     # 黑芝麻 <- 鹤虱子
    "shijunzi": ["shizhangzi"],  # 使君子 <- 石樟子
    "zirantong": ["zirun"],      # 自然铜 <- 紫润
}

ACUPOINT_STANDARD: Dict[str, List[str]] = {
    "cuanzhu": ["zanzhu"],           # 攒竹 <- 赞竹
    "jianshi": ["jian Shi"],          # 间使 <- 间使(空格)
    "sanjiaoju": ["sanjiaoshu"],      # 三焦俞 <- 三焦输
    "taichong": ["taichong_lv"],      # 太冲 <- 太冲(LV)
    "xiabai": ["xiamen"],             # 侠白 <- 侠门
    "yaoyangguan": ["yangguan"],       # 腰阳关 <- 阳关
    "zulinqi": ["zulinqi_gb"],         # 足临泣 <- 足临泣(GB)
}


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


def process_alias(kind: str, standard_id: str, alias_ids: List[str]) -> List[Dict]:
    results = []
    folder = "herbs" if kind == "herb" else "acupoints"
    
    for alias_id in alias_ids:
        path = ROOT / "knowledge" / folder / f"{alias_id}.md"
        if not path.exists():
            results.append({"file": str(path), "changed": False, "error": "missing"})
            continue
        text = path.read_text(encoding="utf-8")
        lines, body = split_frontmatter(text)
        if not lines:
            lines = [f'title: "{alias_id}"']
        upsert_line(lines, "alias_of", f'"{standard_id}"')
        new_text = "---\n" + "\n".join(lines).rstrip() + "\n---\n\n" + body.lstrip("\n")
        changed = new_text != text
        if changed:
            path.write_text(new_text, encoding="utf-8")
        results.append({"kind": kind, "file": str(path.relative_to(ROOT)), "changed": changed, "alias_of": standard_id})
    
    return results


def main():
    results = []
    
    for standard_id, aliases in HERB_STANDARD.items():
        results.extend(process_alias("herb", standard_id, aliases))
    
    for standard_id, aliases in ACUPOINT_STANDARD.items():
        results.extend(process_alias("acupoint", standard_id, aliases))
    
    changed = sum(1 for r in results if r.get("changed"))
    print(json.dumps({
        "total": len(results),
        "changed": changed,
        "sample": results[:10]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
