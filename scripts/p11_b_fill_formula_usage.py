#!/usr/bin/env python3
"""P11-B: 为 P0 方剂补 usage 结构。

策略：
1. 从 source_refs.quote 中搜索煎服法关键词
2. 如果命中，摘录为来源引用
3. 如果没命中，添加占位符，标注待补充

不凭空扩写医学内容，只基于现有 source_refs。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "data" / "p11_content_quality_queue.jsonl"
OUT_REPORT = ROOT / "report" / "p11_b_usage_fill_report.md"

# 煎服法关键词
USAGE_KEYWORDS = [
    "煎服", "温服", "日三服", "日二服", "顿服", "分服",
    "水煎服", "煮取", "去滓", "温分再服", "温覆取微似汗",
    "以水", "煮", "升", "合", "方寸匕", "钱匕",
    "煮三沸", "煮一沸", "煮二沸", "去滓温服",
]


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def parse_frontmatter(text: str) -> tuple:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 4:]
    data = {}
    current_key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(line[4:].strip().strip('"\''))
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if value == "":
                data[key] = []
            elif value in {"true", "false"}:
                data[key] = value == "true"
            else:
                data[key] = value.strip('"\'')
    return data, body


def extract_usage_from_quote(quote: str) -> Optional[Dict]:
    """从 quote 中提取煎服法相关信息。"""
    if not quote:
        return None
    
    # 搜索关键词
    found = []
    for kw in USAGE_KEYWORDS:
        if kw in quote:
            found.append(kw)
    
    if not found:
        return None
    
    # 提取包含关键词的上下文
    sentences = re.split(r'[。；\n]', quote)
    usage_sentences = []
    for sent in sentences:
        for kw in found:
            if kw in sent:
                usage_sentences.append(sent.strip())
                break
    
    if not usage_sentences:
        return None
    
    return {
        "keywords": found[:5],  # 最多5个
        "context": "；".join(usage_sentences[:3])[:200],  # 最多3句，200字
    }


def build_usage_section(usage_info: Optional[Dict], source_refs: List[Dict]) -> str:
    """构建 usage 小节内容。"""
    lines = ["", "## 用法", ""]
    
    if usage_info:
        lines.append("**来源引用：**")
        lines.append(f"> {usage_info['context']}")
        lines.append("")
        lines.append(f"*关键词：{', '.join(usage_info['keywords'])}*")
        lines.append("")
        lines.append("**说明：** 以上用法信息来自现有来源引用中的煎服法描述。")
    else:
        lines.append("**说明：**")
        lines.append("> 现有 verified 来源未提供明确煎服法描述，待补充。")
        lines.append("")
        lines.append("**来源引用清单：**")
        for ref in source_refs[:2]:
            sf = ref.get('source_file', 'unknown')
            pn = ref.get('page_num', 0)
            lines.append(f"- {sf} 第{pn}页")
    
    lines.append("")
    return "\n".join(lines)


def insert_usage_before_ni_section(body: str, usage_section: str) -> str:
    """在 ## 🌿 倪师讲解 之前插入 usage 小节。"""
    marker = "## 🌿 倪师讲解"
    if marker in body:
        idx = body.find(marker)
        return body[:idx] + usage_section + body[idx:]
    # 如果没有倪师讲解，在文件末尾插入
    return body.rstrip() + "\n" + usage_section


def process_formula(item: Dict, verified_map: Dict[str, Dict]) -> Dict:
    """处理单个方剂，返回处理结果。"""
    file_path = ROOT / item["file"]
    if not file_path.exists():
        return {"item_id": item["item_id"], "status": "file_not_found"}
    
    text = file_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    verified_row = verified_map.get(item["item_id"], {})
    source_refs = verified_row.get("source_refs") or []
    # 兼容旧格式：verified_sources 可能是单条 source_file/page_num/quote
    if not source_refs and verified_row.get("quote"):
        source_refs = [verified_row]
    
    # 提取用法信息
    usage_info = None
    for ref in source_refs:
        quote = ref.get("quote", "")
        info = extract_usage_from_quote(quote)
        if info:
            usage_info = info
            usage_info["source_file"] = ref.get("source_file")
            usage_info["page_num"] = ref.get("page_num")
            break
    
    # 构建 usage 小节
    usage_section = build_usage_section(usage_info, source_refs)
    
    # 插入到正文
    new_body = insert_usage_before_ni_section(body, usage_section)
    
    # 写回文件
    new_text = text[:text.find("\n---", 4) + 5] + new_body
    file_path.write_text(new_text, encoding="utf-8")
    
    return {
        "item_id": item["item_id"],
        "title": item["title"],
        "status": "filled" if usage_info else "placeholder",
        "has_usage_quote": bool(usage_info),
        "keywords": usage_info["keywords"] if usage_info else [],
    }


def main():
    queue = load_jsonl(QUEUE_PATH)
    p0_items = [q for q in queue if q["priority"] == "P0" and q["kind"] == "formula"]
    verified_map = {r["item_id"]: r for r in load_jsonl(ROOT / "data" / "verified_sources.jsonl") if r.get("item_id")}
    
    results = []
    for item in p0_items:
        result = process_formula(item, verified_map)
        results.append(result)
    
    # 生成报告
    filled = sum(1 for r in results if r["status"] == "filled")
    placeholder = sum(1 for r in results if r["status"] == "placeholder")
    
    lines = [
        "# P11-B 方剂 usage 结构补全报告",
        "",
        f"- 处理条目: {len(results)}",
        f"- 有来源用法信息: {filled}",
        f"- 占位符待补充: {placeholder}",
        "",
        "## 明细",
        "",
        "| item_id | title | status | keywords |",
        "|---------|-------|--------|----------|",
    ]
    for r in results:
        kw = ", ".join(r.get("keywords", []))[:40]
        lines.append(f"| {r['item_id']} | {r.get('title', '')} | {r['status']} | {kw} |")
    
    OUT_REPORT.parent.mkdir(exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    
    print(json.dumps({
        "total": len(results),
        "filled": filled,
        "placeholder": placeholder,
        "report": str(OUT_REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
