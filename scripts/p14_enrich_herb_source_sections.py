#!/usr/bin/env python3
"""P14: Enrich verified herb entries using existing source_refs.quote only.

Goal: improve real body quality after P13 placeholder cleanup.
Rules:
- Do not invent medical content.
- Only add structured sections when explicit text exists in current source_refs.quote.
- Do not fill meridian/归经 unless the quote explicitly contains 归经.
- Empty operational sections may receive source excerpts; otherwise remain empty rather than using placeholders.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "p11_content_quality_queue.jsonl"
REPORT = ROOT / "report" / "p14_herb_source_section_enrichment.md"

SECTION_ORDER = [
    "## 📌 基础信息",
    "## 🌡️ 性味",
    "## 💊 功效",
    "## 🎯 主治",
    "## ⚖️ 常用剂量范围",
    "## 🔥 炮制方法",
    "## ⚠️ 配伍禁忌",
    "## 🔍 鉴别要点",
    "## 🌿 倪师讲解",
]

EXTRACT_PATTERNS = {
    "xingwei": re.compile(r"【性味】\s*([^【]{2,140})"),
    "xingwei_alt": re.compile(r"(味[酸苦甘辛咸、]{1,6}[，,]?性[寒热温凉平]{1,2}[，,]?(?:无毒|有[毒小毒]毒)?[^【。]{0,20})"),
    "zhuzhi": re.compile(r"【主治】\s*([^【]{2,180})"),
    "zhuzhi_alt": re.compile(r"(主治[呢：:]\s*[^【。]{2,120})"),
    "yongliang": re.compile(r"【用量】\s*([^【]{2,140})"),
    "jinji": re.compile(r"【禁忌】\s*([^【]{2,180})"),
    "benjing": re.compile(r"【本经原文】\s*([^【]{2,220})"),
    "guijing": re.compile(r"归经[：:】]?\s*([^【。；\n]{2,80})"),
}


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def split_frontmatter(text: str) -> Tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[: end + 5], text[end + 5 :]
    return "", text


def extract_quote_from_frontmatter(fm: str) -> str:
    # Current files use one-line JSON/YAML quoted source_refs.quote after standardization.
    qs = []
    for m in re.finditer(r"^\s*quote:\s*(['\"])(.*)\1\s*$", fm, re.M):
        raw = m.group(2)
        raw = raw.replace('\\n', ' ')
        qs.append(raw)
    return " ".join(qs)


def clean_excerpt(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    # Remove obvious bleed into next numbered herb caused by OCR/page window overlap.
    text = re.sub(r"\s+[一二三四五六七八九十百〇零]{1,6}[、，].*$", "", text).strip()
    return text


def extract_fields(quote: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for key, pat in EXTRACT_PATTERNS.items():
        m = pat.search(quote)
        if m:
            val = clean_excerpt(m.group(1))
            if val:
                out[key] = val
    return out


def section_body(body: str, header: str) -> str | None:
    pos = body.find(header)
    if pos == -1:
        return None
    start = pos + len(header)
    m = re.search(r"\n## ", body[start:])
    end = start + m.start() if m else len(body)
    return body[start:end].strip()


def section_empty(body: str, header: str) -> bool:
    content = section_body(body, header)
    return content is not None and not content.strip("\n -—")


def insert_after(body: str, after_header: str, new_section: str) -> str:
    pos = body.find(after_header)
    if pos == -1:
        return body.rstrip() + "\n\n" + new_section.strip() + "\n"
    start = pos + len(after_header)
    m = re.search(r"\n## ", body[start:])
    end = start + m.start() if m else len(body)
    return body[:end].rstrip() + "\n\n" + new_section.strip() + "\n\n" + body[end:].lstrip()


def replace_empty_section(body: str, header: str, content: str) -> str:
    pos = body.find(header)
    if pos == -1:
        return body
    start = pos + len(header)
    m = re.search(r"\n## ", body[start:])
    end = start + m.start() if m else len(body)
    return body[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + body[end:].lstrip()


def has_source_section(body: str, header: str) -> bool:
    return header in body and bool(section_body(body, header))


def enrich_file(path: Path, apply: bool) -> Dict:
    original = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(original)
    quote = extract_quote_from_frontmatter(fm)
    fields = extract_fields(quote)
    changes: List[str] = []
    new_body = body

    xingwei_val = fields.get("xingwei") or fields.get("xingwei_alt")
    if xingwei_val and not ("## 🌡️ 性味" in new_body or "性味" in section_body(new_body, "## 📌 基础信息") if section_body(new_body, "## 📌 基础信息") is not None else False):
        new_body = insert_after(new_body, "## 📌 基础信息", f"## 🌡️ 性味\n\n> 来源摘录：{xingwei_val}")
        changes.append("add_xingwei")

    if fields.get("yongliang"):
        if section_empty(new_body, "## ⚖️ 常用剂量范围"):
            new_body = replace_empty_section(new_body, "## ⚖️ 常用剂量范围", f"> 来源摘录：{fields['yongliang']}")
            changes.append("fill_yongliang")
        elif "## ⚖️ 常用剂量范围" not in new_body:
            new_body = insert_after(new_body, "## 🎯 主治" if "## 🎯 主治" in new_body else "## 💊 功效", f"## ⚖️ 常用剂量范围\n\n> 来源摘录：{fields['yongliang']}")
            changes.append("add_yongliang")

    if fields.get("jinji"):
        if section_empty(new_body, "## ⚠️ 配伍禁忌"):
            new_body = replace_empty_section(new_body, "## ⚠️ 配伍禁忌", f"> 来源摘录：{fields['jinji']}")
            changes.append("fill_jinji")
        elif "## ⚠️ 配伍禁忌" not in new_body:
            new_body = insert_after(new_body, "## ⚖️ 常用剂量范围" if "## ⚖️ 常用剂量范围" in new_body else "## 💊 功效", f"## ⚠️ 配伍禁忌\n\n> 来源摘录：{fields['jinji']}")
            changes.append("add_jinji")

    # Preserve existing 功效/主治 if present; only add source quote under empty 主治 section.
    zhuzhi_val = fields.get("zhuzhi") or fields.get("zhuzhi_alt")
    if zhuzhi_val and section_empty(new_body, "## 🎯 主治"):
        new_body = replace_empty_section(new_body, "## 🎯 主治", f"> 来源摘录：{zhuzhi_val}")
        changes.append("fill_zhuzhi")

    # Do not fill meridian unless explicit 归经 exists. If found, add source excerpt under 基础信息.
    if fields.get("guijing") and "归经" not in new_body:
        new_body = insert_after(new_body, "## 📌 基础信息", f"## 🧭 归经\n\n> 来源摘录：归经：{fields['guijing']}")
        changes.append("add_guijing")

    new_text = fm + new_body
    if new_text != original and apply:
        path.write_text(new_text, encoding="utf-8")
    return {"file": str(path.relative_to(ROOT)), "changed": new_text != original, "changes": changes, "fields": sorted(fields)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    queue = [r for r in load_jsonl(QUEUE) if r.get("task_type") == "fill_verified_missing_content_field" and r.get("kind") == "herb"]
    results = []
    for row in queue:
        p = ROOT / row["file"]
        if p.exists():
            results.append(enrich_file(p, args.apply))

    changed = [r for r in results if r["changed"]]
    by_change: Dict[str, int] = {}
    for r in changed:
        for c in r["changes"]:
            by_change[c] = by_change.get(c, 0) + 1

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# P14 药材正文来源摘录补强报告",
        "",
        f"- apply: {args.apply}",
        f"- queue_items: {len(queue)}",
        f"- changed_files: {len(changed)}",
        f"- by_change: `{json.dumps(by_change, ensure_ascii=False)}`",
        "",
        "## 原则",
        "",
        "- 只使用现有 `source_refs.quote`。",
        "- 不凭模型记忆补中药性味、归经、剂量或禁忌。",
        "- quote 未明确提供 `归经` 时，不补归经。",
        "",
        "## 变更文件",
        "",
    ]
    for r in changed:
        lines.append(f"- `{r['file']}`: {', '.join(r['changes'])}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"apply": args.apply, "queue_items": len(queue), "changed_files": len(changed), "by_change": by_change, "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
