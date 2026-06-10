#!/usr/bin/env python3
"""Normalize obvious OCR repeat residue in active knowledge/registry files.

P44 is intentionally mechanical and conservative: a line/string is changed only
when it already contains strong OCR-repeat features such as replacement
characters, repeated Chinese punctuation, or repeated brackets. It does not add
medical content, infer missing text, or rewrite clinical meaning.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p44_ocr_repeat_normalization.md"

DATA_FILES = [
    DATA / "verified_sources.jsonl",
    DATA / "herb_index.jsonl",
    DATA / "formula_index.jsonl",
    DATA / "acupoint_index.jsonl",
]

REPLACEMENT_RE = re.compile("\ufffd+")
REPEATED_BRACKETS = ["\u3010", "\u3011", "\u300a", "\u300b"]
REPEATED_PUNCT = ["\uff0c", "\u3002", "\uff0e", "\u3001", "\uff1b", "\uff1a"]
REPEATED_CJK_RE = re.compile(r"([\u4e00-\u9fff])\1{2,}")
TARGETED_RESIDUE_REPLACEMENTS = [
    ("\u52a0\u52a0\u52a0\u4e00\u4e9b", "\u52a0\u4e00\u4e9b"),
    ("\u9aa8\u9aa8\u9aa8\u3002", "\u9aa8\u3002"),
    ("\u866b\u866b\u866b\u3002", "\u866b\u3002"),
    ("\u901a\u901a\u901a", "\u901a"),
    ("\u901a\u901a\u901a\n\u7b2c", "\u901a\n\u7b2c"),
    ("\u52e4\u52e4\u52e4\u52e4\u6c42\u6c42\u6c42\u6c42\u53e4\u53e4\u53e4\u53e4\u8a13\u8a13\u8a13\u8a13", "\u52e4\u6c42\u53e4\u8a13"),
    ("\u535a\u535a\u535a\u535a\u91c7\u91c7\u91c7\u91c7\u773e\u773e\u773e\u773e\u65b9\u65b9\u65b9\u65b9", "\u535a\u91c7\u773e\u65b9"),
    ("\u5c0f\u5c0f\u5c0f\u5c0f\u6842\u6842\u6842\u6842\u679d\u679d\u679d\u679d\u00b7\u00b7\u00b7\u00b7\u7fa4\u7fa4\u7fa4\u7fa4\u9f99\u9f99\u9f99\u9f99\u65e0\u65e0\u65e0\u65e0\u9996\u9996\u9996\u9996", "\u5c0f\u6842\u679d\u00b7\u7fa4\u9f99\u65e0\u9996"),
]
TARGETED_RESIDUE_PATTERNS = [re.compile(re.escape(old)) for old, _ in TARGETED_RESIDUE_REPLACEMENTS]

TRIGGER_PATTERNS = [
    REPLACEMENT_RE,
    *[re.compile(re.escape(ch) + r"{2,}") for ch in REPEATED_BRACKETS],
    *[re.compile(re.escape(ch) + r"{3,}") for ch in REPEATED_PUNCT],
]
BAD_PATTERNS = [*TRIGGER_PATTERNS, *TARGETED_RESIDUE_PATTERNS]


def has_trigger(text: str) -> bool:
    return any(pattern.search(text) for pattern in [*TRIGGER_PATTERNS, *TARGETED_RESIDUE_PATTERNS])


def has_bad_repeat(text: str) -> bool:
    return any(pattern.search(text) for pattern in BAD_PATTERNS)


def normalize_text(text: str) -> tuple[str, bool]:
    if not has_trigger(text):
        return text, False
    original = text
    text = REPLACEMENT_RE.sub("", text)
    for old, new in TARGETED_RESIDUE_REPLACEMENTS:
        text = text.replace(old, new)
    for ch in REPEATED_BRACKETS:
        text = re.sub(re.escape(ch) + r"{2,}", ch, text)
    for ch in REPEATED_PUNCT:
        text = re.sub(re.escape(ch) + r"{3,}", ch, text)
    text = REPEATED_CJK_RE.sub(r"\1", text)
    return text, text != original


def normalize_markdown(path: Path) -> dict[str, Any] | None:
    original = path.read_text(encoding="utf-8")
    lines: list[str] = []
    changed_lines = 0
    for line in original.splitlines():
        new_line, changed = normalize_text(line)
        if changed:
            changed_lines += 1
        lines.append(new_line)
    updated = "\n".join(lines) + ("\n" if original.endswith("\n") else "")
    if updated == original:
        return None
    path.write_text(updated, encoding="utf-8")
    return {"file": path.relative_to(ROOT).as_posix(), "changed_lines": changed_lines}


def normalize_json_value(value: Any) -> tuple[Any, int]:
    if isinstance(value, str):
        updated, changed = normalize_text(value)
        return updated, int(changed)
    if isinstance(value, list):
        changed_count = 0
        updated_items = []
        for item in value:
            updated, changed = normalize_json_value(item)
            updated_items.append(updated)
            changed_count += changed
        return updated_items, changed_count
    if isinstance(value, dict):
        changed_count = 0
        updated_obj: dict[str, Any] = {}
        for key, item in value.items():
            updated, changed = normalize_json_value(item)
            updated_obj[key] = updated
            changed_count += changed
        return updated_obj, changed_count
    return value, 0


def normalize_jsonl(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed_rows = 0
    changed_strings = 0
    updated_rows = []
    for row in rows:
        updated, changed = normalize_json_value(row)
        if changed:
            changed_rows += 1
            changed_strings += changed
        updated_rows.append(updated)
    if changed_rows == 0:
        return None
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in updated_rows) + "\n", encoding="utf-8")
    return {
        "file": path.relative_to(ROOT).as_posix(),
        "changed_rows": changed_rows,
        "changed_strings": changed_strings,
    }


def remaining_hits() -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for path in sorted(KNOWLEDGE.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if has_bad_repeat(text):
            hits.append({"file": path.relative_to(ROOT).as_posix(), "scope": "knowledge"})
    for path in DATA_FILES:
        if not path.exists():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if has_bad_repeat(line):
                hits.append({"file": path.relative_to(ROOT).as_posix(), "scope": "data", "line": line_no})
                break
    return hits


def write_report(markdown_changes: list[dict[str, Any]], jsonl_changes: list[dict[str, Any]], remaining: list[dict[str, Any]]) -> None:
    lines = [
        "# P44 OCR Repeat Normalization",
        "",
        "Mechanically normalized repeated OCR residue in knowledge Markdown and current trace registry JSONL files.",
        "No new medical content was added; only lines/strings with strong OCR-repeat triggers were changed.",
        "",
        f"- Markdown files changed: {len(markdown_changes)}",
        f"- JSONL files changed: {len(jsonl_changes)}",
        f"- Remaining active-scope hits: {len(remaining)}",
    ]
    if markdown_changes:
        lines.extend(["", "## Markdown Changes"])
        lines.extend(f"- `{row['file']}`: {row['changed_lines']} lines" for row in markdown_changes)
    if jsonl_changes:
        lines.extend(["", "## JSONL Changes"])
        lines.extend(f"- `{row['file']}`: {row['changed_rows']} rows, {row['changed_strings']} strings" for row in jsonl_changes)
    if remaining:
        lines.extend(["", "## Remaining Active-Scope Hits"])
        lines.extend(f"- `{row['file']}` {row.get('scope')} {row.get('line', '')}" for row in remaining[:100])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    markdown_changes = [row for path in sorted(KNOWLEDGE.rglob("*.md")) if (row := normalize_markdown(path))]
    jsonl_changes = [row for path in DATA_FILES if (row := normalize_jsonl(path))]

    p43_report = ROOT / "report" / "p43_source_ref_residue_sync.md"
    if p43_report.exists():
        text = p43_report.read_text(encoding="utf-8")
        text = text.replace("\n## Synced This Run\n\n\n## Current Synced Rows\n", "\n## Current Synced Rows\n")
        p43_report.write_text(text, encoding="utf-8")

    remaining = remaining_hits()
    write_report(markdown_changes, jsonl_changes, remaining)
    print(json.dumps({
        "markdown_files_changed": len(markdown_changes),
        "jsonl_files_changed": len(jsonl_changes),
        "remaining_active_scope_hits": len(remaining),
        "report": str(REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))
    return 1 if remaining else 0


if __name__ == "__main__":
    raise SystemExit(main())
