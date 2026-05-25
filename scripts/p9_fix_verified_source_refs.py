#!/usr/bin/env python3
"""P9-A fix: 为 verified frontmatter 补 source_refs。

只修治理元数据，不改医学正文。
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def build_source_refs(record: dict) -> list[str]:
    refs = record.get("source_refs") or []
    lines = ["source_refs:"]
    for ref in refs[:1]:
        quote = (ref.get("quote") or "").replace('"', '\\"')
        lines.append(f"  - source_file: \"{ref.get('source_file')}\"")
        lines.append(f"    page_num: {json.dumps(ref.get('page_num'), ensure_ascii=False)}")
        lines.append(f"    quote: \"{quote}\"")
    return lines


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---", 4)
    if end < 0:
        return [], text
    return text[4:end].splitlines(), text[end + 4 :].lstrip("\n")


def has_key(lines: list[str], key: str) -> bool:
    return any(line.strip().startswith(f"{key}:") for line in lines)


def insert_after_key(lines: list[str], key: str, block: list[str]):
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}:"):
            lines[i + 1:i + 1] = block
            return
    lines.extend(block)


def main():
    changed = []
    skipped = 0
    for record in load_jsonl(DATA / "verified_sources.jsonl"):
        rel = record.get("file")
        if not rel:
            skipped += 1
            continue
        path = ROOT / rel
        if not path.exists():
            skipped += 1
            continue
        old = path.read_text(encoding="utf-8")
        lines, body = split_frontmatter(old)
        if not lines:
            skipped += 1
            continue
        if has_key(lines, "source_refs"):
            continue
        block = build_source_refs(record)
        insert_after_key(lines, "trace_status", block)
        new = "---\n" + "\n".join(lines).rstrip() + "\n---\n\n" + body.lstrip("\n")
        if new != old:
            path.write_text(new, encoding="utf-8")
            changed.append(rel)
    print(json.dumps({"changed": len(changed), "skipped": skipped, "changed_files": changed[:20]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
