#!/usr/bin/env python3
"""P13: Clean body placeholders in knowledge markdown.

User goal: every knowledge entry should not contain dangling "待补充/待考" content.
Rules:
- Do not invent medical content.
- If the placeholder is in source/commentary/original-text section and source_refs.quote exists, replace with a direct source excerpt.
- Otherwise remove placeholder line/row.
- Normalize literal \\n artifacts in body.
- Keep frontmatter and safety boundary intact.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report" / "p13_body_placeholder_clean_report.md"
PLACEHOLDER_RE = re.compile(r"(待考|待补充…|待补充|暂无|待完善|TODO|待查|待定|待确认|未提供明确|现有 verified 来源未提供)")
HEADER_RE = re.compile(r"^(#{2,4})\s+(.+)$")
SOURCE_SECTION_HINTS = ["倪师", "讲解", "来源", "原文", "经典", "文献", "注解"]
PRESERVE_HINTS = ["学习与安全边界", "来源追溯状态"]


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def load_quote_map() -> Dict[str, List[str]]:
    quotes: Dict[str, List[str]] = {}
    for path in [ROOT / "data" / "verified_sources.jsonl", ROOT / "data" / "herb_index.jsonl", ROOT / "data" / "acupoint_index.jsonl", ROOT / "data" / "formula_index.jsonl"]:
        for row in load_jsonl(path):
            rel = row.get("file")
            if not rel:
                continue
            for ref in row.get("source_refs") or []:
                q = (ref.get("quote") or "").strip()
                if q:
                    q = re.sub(r"\s+", " ", q)
                    if q not in quotes.setdefault(rel, []):
                        quotes[rel].append(q)
    return quotes


def split_frontmatter(text: str) -> Tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[:end + 5], text[end + 5:]
    return "", text


def section_is_source_related(section: str) -> bool:
    return any(h in section for h in SOURCE_SECTION_HINTS)


def section_is_preserved(section: str) -> bool:
    return any(h in section for h in PRESERVE_HINTS)


def best_quote(quotes: List[str]) -> str | None:
    if not quotes:
        return None
    # Prefer moderately rich quotes, not absurdly short.
    qs = sorted(quotes, key=lambda q: (len(q) < 40, -min(len(q), 500)))
    return qs[0][:500]


def clean_table_pipe(line: str) -> str:
    if line.startswith("|") and not line.rstrip().endswith("|"):
        return line.rstrip() + " |"
    return line


def clean_file(path: Path, quote_map: Dict[str, List[str]], apply: bool) -> Tuple[bool, List[str]]:
    original = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(original)
    rel = str(path.relative_to(ROOT))

    # Normalize literal \n only in body; frontmatter may legitimately contain escaped newlines in YAML strings.
    normalized = body.replace("\\n", "\n")
    quotes = quote_map.get(rel, [])
    q = best_quote(quotes)

    changes: List[str] = []
    if normalized != body:
        changes.append("normalized_literal_backslash_n")
    body = normalized

    lines = body.splitlines()
    out: List[str] = []
    current_section = ""
    inserted_quote_sections = set()

    for idx, line in enumerate(lines, start=1):
        hm = HEADER_RE.match(line)
        if hm:
            current_section = hm.group(2).strip()
            out.append(line)
            continue

        if not PLACEHOLDER_RE.search(line):
            out.append(clean_table_pipe(line))
            continue

        if section_is_preserved(current_section) or "不构成诊断" in line or "不作为针灸操作指导" in line:
            out.append(line)
            continue

        if section_is_source_related(current_section) and q and current_section not in inserted_quote_sections:
            out.append(f"> 来源摘录：{q}")
            inserted_quote_sections.add(current_section)
            changes.append(f"line {idx}: placeholder_replaced_by_source_quote in [{current_section}]")
        else:
            changes.append(f"line {idx}: placeholder_removed in [{current_section}]")
        # Otherwise drop the placeholder line/row.

    new_body = "\n".join(out).strip() + "\n"
    new_text = fm + new_body
    changed = new_text != original
    if changed and apply:
        path.write_text(new_text, encoding="utf-8")
    return changed, changes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    quote_map = load_quote_map()
    files = sorted((ROOT / "knowledge").rglob("*.md"))
    changed_files = 0
    replaced = 0
    removed = 0
    normalized = 0
    report = ["# P13 正文占位清理报告", "", f"apply: {args.apply}", ""]

    for path in files:
        changed, changes = clean_file(path, quote_map, args.apply)
        if changed:
            changed_files += 1
            for c in changes:
                report.append(f"- `{path.relative_to(ROOT)}`: {c}")
                if "replaced" in c:
                    replaced += 1
                elif "removed" in c:
                    removed += 1
                elif "normalized" in c:
                    normalized += 1

    report.extend([
        "",
        f"total_files: {len(files)}",
        f"changed_files: {changed_files}",
        f"normalized_literal_backslash_n_files: {normalized}",
        f"replaced_with_source_quote: {replaced}",
        f"removed_placeholder: {removed}",
        "",
        "原则：只用已有 source_refs.quote 补来源/讲解类占位；其他无明确来源的占位直接删除，不凭模型记忆补写。",
    ])
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({
        "apply": args.apply,
        "total_files": len(files),
        "changed_files": changed_files,
        "normalized_literal_backslash_n_files": normalized,
        "replaced_with_source_quote": replaced,
        "removed_placeholder": removed,
        "report": str(REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
