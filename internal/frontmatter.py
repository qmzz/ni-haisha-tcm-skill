#!/usr/bin/env python3
"""轻量 frontmatter 解析与校验。"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

REQUIRED_BY_KIND = {
    "formula": ["title", "kind", "trace_status"],
    "herb": ["title", "kind", "trace_status"],
    "acupoint": ["title", "kind", "trace_status"],
}


def parse_frontmatter(text: str) -> Tuple[Dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    raw = text[4:end].strip().splitlines()
    body = text[end + 4 :]
    data: Dict[str, object] = {}
    current_key = None
    for line in raw:
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


def audit_file(path: Path, kind: str) -> Dict[str, object]:
    text = path.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(text)
    missing = [key for key in REQUIRED_BY_KIND.get(kind, []) if key not in fm]
    warnings: List[str] = []
    if fm.get("trace_status") == "verified" and not fm.get("source_refs"):
        warnings.append("verified_without_source_refs")
    if fm.get("kind") and fm.get("kind") != kind:
        warnings.append("kind_mismatch")
    return {
        "file": str(path),
        "kind": kind,
        "has_frontmatter": bool(fm),
        "missing": missing,
        "warnings": warnings,
    }
