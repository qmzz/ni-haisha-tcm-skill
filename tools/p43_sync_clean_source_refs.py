#!/usr/bin/env python3
"""Sync cleaned source_refs from Markdown frontmatter into JSONL indexes.

P42 cleaned obvious OCR tails in knowledge Markdown. Some registry/index rows
still carried older source_refs with the same OCR residue, so this script copies
the already-clean frontmatter source_refs back into the JSONL data files. It
does not create new medical content or invent source quotes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
KNOWLEDGE = ROOT / "knowledge"
REPORT = ROOT / "report" / "p43_source_ref_residue_sync.md"

DATA_FILES = [
    DATA / "verified_sources.jsonl",
    DATA / "herb_index.jsonl",
]

BAD_PATTERNS = [
    re.compile(r"\uFFFD{2,}"),
    re.compile(r"【【"),
    re.compile(r"】】"),
    re.compile(r"[一二三四五六七八九十〇○零]{4,}[、，,]"),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    return text[4:end] if end >= 0 else ""


def source_refs(fm: str) -> list[dict[str, Any]]:
    if re.search(r"^\s*source_refs:\s*\[\]\s*$", fm, re.M):
        return []
    refs: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    in_refs = False
    for line in fm.splitlines():
        stripped = line.strip()
        if stripped.startswith("source_refs:"):
            in_refs = True
            continue
        if not in_refs:
            continue
        if stripped.startswith("- source_file:"):
            if current and current.get("source_file") and current.get("quote"):
                refs.append(current)
            current = {"source_file": quoted_value(stripped), "page_num": None, "quote": ""}
            continue
        if current is None:
            continue
        if stripped.startswith("page_num:"):
            raw = stripped.split(":", 1)[1].strip()
            current["page_num"] = None if raw == "null" else int(raw)
            continue
        if stripped.startswith("quote:"):
            current["quote"] = quoted_value(stripped)
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:\s*", stripped):
            break
    if current and current.get("source_file") and current.get("quote"):
        refs.append(current)
    return refs


def quoted_value(line: str) -> str:
    raw = line.split(":", 1)[1].strip()
    if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
        return raw[1:-1]
    return raw.strip('"')


def quote_text(refs: list[dict[str, Any]]) -> str:
    return "\n".join((ref.get("quote") or "") for ref in refs)


def has_bad_quote(refs: list[dict[str, Any]]) -> bool:
    text = quote_text(refs)
    return any(pattern.search(text) for pattern in BAD_PATTERNS)


def row_id(row: dict[str, Any]) -> str:
    return str(row.get("item_id") or row.get("herb_id") or row.get("formula_id") or row.get("acupoint_id") or "")


def load_clean_markdown_refs() -> dict[str, list[dict[str, Any]]]:
    refs_by_id: dict[str, list[dict[str, Any]]] = {}
    for path in sorted((KNOWLEDGE / "herbs").glob("*.md")):
        item_id = path.stem
        fm = frontmatter(path.read_text(encoding="utf-8"))
        refs = source_refs(fm)
        if refs and not has_bad_quote(refs):
            refs_by_id[item_id] = refs
    return refs_by_id


def sync_file(path: Path, clean_refs: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = load_jsonl(path)
    changes: list[dict[str, Any]] = []
    for row in rows:
        refs = row.get("source_refs") or []
        if not refs or not has_bad_quote(refs):
            continue
        item_id = row_id(row)
        replacement = clean_refs.get(item_id)
        if not replacement:
            changes.append({"file": path.name, "item_id": item_id, "name": row.get("name"), "action": "missing_clean_frontmatter_refs"})
            continue
        old_quote_len = len(quote_text(refs))
        row["source_refs"] = replacement
        row["p43_source_ref_sync"] = "synced_from_clean_markdown_frontmatter"
        changes.append(
            {
                "file": path.name,
                "item_id": item_id,
                "name": row.get("name"),
                "action": "synced",
                "old_quote_len": old_quote_len,
                "new_quote_len": len(quote_text(replacement)),
            }
        )
    return rows, changes


def current_sync_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in DATA_FILES:
        for row in load_jsonl(path):
            if row.get("p43_source_ref_sync") != "synced_from_clean_markdown_frontmatter":
                continue
            refs = row.get("source_refs") or []
            rows.append(
                {
                    "file": path.name,
                    "item_id": row_id(row),
                    "name": row.get("name"),
                    "quote_len": len(quote_text(refs)),
                }
            )
    return rows


def remaining_bad_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in DATA_FILES:
        for row in load_jsonl(path):
            refs = row.get("source_refs") or []
            if refs and has_bad_quote(refs):
                rows.append({"file": path.name, "item_id": row_id(row), "name": row.get("name")})
    return rows


def main() -> int:
    clean_refs = load_clean_markdown_refs()
    all_changes: list[dict[str, Any]] = []
    for path in DATA_FILES:
        rows, changes = sync_file(path, clean_refs)
        write_jsonl(path, rows)
        all_changes.extend(changes)

    synced = [row for row in all_changes if row["action"] == "synced"]
    missing = [row for row in all_changes if row["action"] != "synced"]
    current_synced = current_sync_rows()
    remaining_bad = remaining_bad_rows()
    REPORT.write_text(
        "\n".join(
            [
                "# P43 Source Ref Residue Sync",
                "",
                "同步已清理 Markdown frontmatter 中的 source_refs 到 JSONL 注册表，清除追溯结果中的 OCR 尾巴残留。",
                "",
                f"- Synced refs this run: {len(synced)}",
                f"- Current P43 synced rows: {len(current_synced)}",
                f"- Missing clean refs: {len(missing)}",
                f"- Remaining bad source_refs: {len(remaining_bad)}",
                "",
                "## Synced This Run",
                "",
                *[f"- `{row['file']}` `{row['item_id']}` {row['name']}: {row['old_quote_len']} -> {row['new_quote_len']} chars" for row in synced],
                *(["", "## Missing"] + [f"- `{row['file']}` `{row['item_id']}` {row['name']}: {row['action']}" for row in missing] if missing else []),
                *(["", "## Current Synced Rows"] + [f"- `{row['file']}` `{row['item_id']}` {row['name']}: {row['quote_len']} chars" for row in current_synced] if current_synced else []),
                *(["", "## Remaining Bad Rows"] + [f"- `{row['file']}` `{row['item_id']}` {row['name']}" for row in remaining_bad] if remaining_bad else []),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "synced_this_run": len(synced),
                "current_synced_rows": len(current_synced),
                "missing": len(missing),
                "remaining_bad_source_refs": len(remaining_bad),
                "report": str(REPORT.relative_to(ROOT)),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if missing or remaining_bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
