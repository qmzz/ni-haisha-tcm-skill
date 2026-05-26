#!/usr/bin/env python3
"""P15: prune empty herb body sections and sync explicit frontmatter facts.

Rules:
- Do not invent medical content.
- If frontmatter already has explicit 性味/主治/功效, body may mirror it.
- Empty body sections are removed instead of retaining hollow headings.
- Do not add 归经 unless a source/frontmatter explicitly has it; this script does not fill 归经.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "p11_content_quality_queue.jsonl"
REPORT = ROOT / "report" / "p15_empty_herb_section_prune.md"

EMPTY_PRUNE_HEADERS = [
    "## 🎯 主治",
    "## ⚖️ 常用剂量范围",
    "## 🔥 炮制方法",
    "## ⚠️ 配伍禁忌",
    "## 🔍 鉴别要点",
]


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


def fm_scalar(fm: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(['\"]?)(.*?)\1\s*$", fm, re.M)
    if not m:
        return None
    val = m.group(2).strip()
    if not val or val in {"待考", "待补充", "暂无", "待完善"}:
        return None
    return val


def section_bounds(body: str, header: str) -> Tuple[int, int, int] | None:
    pos = body.find(header)
    if pos == -1:
        return None
    start = pos + len(header)
    m = re.search(r"\n## ", body[start:])
    end = start + m.start() if m else len(body)
    return pos, start, end


def section_content(body: str, header: str) -> str | None:
    b = section_bounds(body, header)
    if not b:
        return None
    _, start, end = b
    return body[start:end].strip()


def is_empty_content(content: str | None) -> bool:
    if content is None:
        return False
    cleaned = content.strip()
    cleaned = re.sub(r"^[\s\-—|:：]+$", "", cleaned)
    # Empty markdown tables like only header/separator count as empty.
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    if lines and all(set(ln) <= set("|-: ") or re.match(r"^\|?\s*项目\s*\|\s*说明\s*\|?$", ln) for ln in lines):
        return True
    return not cleaned


def replace_section(body: str, header: str, content: str) -> str:
    b = section_bounds(body, header)
    if not b:
        return body
    pos, start, end = b
    return body[:start].rstrip() + "\n\n" + content.strip() + "\n\n" + body[end:].lstrip()


def remove_section(body: str, header: str) -> str:
    b = section_bounds(body, header)
    if not b:
        return body
    pos, _, end = b
    return body[:pos].rstrip() + "\n\n" + body[end:].lstrip()


def insert_after(body: str, after_header: str, new_section: str) -> str:
    b = section_bounds(body, after_header)
    if not b:
        return body.rstrip() + "\n\n" + new_section.strip() + "\n"
    _, _, end = b
    return body[:end].rstrip() + "\n\n" + new_section.strip() + "\n\n" + body[end:].lstrip()


def process_file(path: Path, apply: bool) -> Dict:
    original = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(original)
    changes: List[str] = []
    new = body

    xingwei = fm_scalar(fm, "性味")
    zhuzhi = fm_scalar(fm, "主治")
    gongxiao = fm_scalar(fm, "功效")

    # Mirror explicit frontmatter 性味 if body lacks a 性味 section and 基础信息 does not already show it.
    base = section_content(new, "## 📌 基础信息") or ""
    if xingwei and "性味" not in base and "## 🌡️ 性味" not in new:
        new = insert_after(new, "## 📌 基础信息", f"## 🌡️ 性味\n\n{xingwei}")
        changes.append("sync_fm_xingwei")

    if zhuzhi and is_empty_content(section_content(new, "## 🎯 主治")):
        new = replace_section(new, "## 🎯 主治", zhuzhi)
        changes.append("sync_fm_zhuzhi")

    if gongxiao and is_empty_content(section_content(new, "## 💊 功效")):
        new = replace_section(new, "## 💊 功效", gongxiao)
        changes.append("sync_fm_gongxiao")

    for header in EMPTY_PRUNE_HEADERS:
        if is_empty_content(section_content(new, header)):
            new = remove_section(new, header)
            changes.append("remove_empty_" + re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]+", "", header))

    # Collapse excessive blank lines.
    new = re.sub(r"\n{4,}", "\n\n\n", new).rstrip() + "\n"
    new_text = fm + new
    if apply and new_text != original:
        path.write_text(new_text, encoding="utf-8")
    return {"file": str(path.relative_to(ROOT)), "changed": new_text != original, "changes": changes}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    queue = [r for r in load_jsonl(QUEUE) if r.get("task_type") == "fill_verified_missing_content_field" and r.get("kind") == "herb"]
    results = []
    for row in queue:
        p = ROOT / row["file"]
        if p.exists():
            results.append(process_file(p, args.apply))
    changed = [r for r in results if r["changed"]]
    by_change: Dict[str, int] = {}
    for r in changed:
        for c in r["changes"]:
            by_change[c] = by_change.get(c, 0) + 1

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# P15 药材空正文小节修剪报告",
        "",
        f"- apply: {args.apply}",
        f"- queue_items: {len(queue)}",
        f"- changed_files: {len(changed)}",
        f"- by_change: `{json.dumps(by_change, ensure_ascii=False)}`",
        "",
        "## 原则",
        "",
        "- frontmatter 中已有明确 `性味/主治/功效` 时，可同步到正文。",
        "- 无内容的小节直接删除，不保留空壳。",
        "- 不补无依据的 `归经`。",
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
