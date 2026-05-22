#!/usr/bin/env python3
"""将 verified 来源试点回写到 Markdown frontmatter。

默认 dry-run，不修改文件；加 --apply 才写入。
只处理 data/verified_sources.jsonl 中的条目。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


ALLOWED_KEYS = {"trace_status", "source_refs"}


def load_verified() -> List[Dict]:
    path = DATA_DIR / "verified_sources.jsonl"
    if not path.exists():
        raise SystemExit("missing data/verified_sources.jsonl, run: python3 scripts/build_verified_sources.py")
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def build_trace_block(item: Dict) -> str:
    refs = item.get("source_refs") or []
    lines = ["trace_status: verified", "source_refs:"]
    for ref in refs[:1]:
        quote = (ref.get("quote") or "").replace('"', '\\"')
        lines.extend([
            f"  - source_file: \"{ref.get('source_file')}\"",
            f"    page_num: {json.dumps(ref.get('page_num'), ensure_ascii=False)}",
            f"    quote: \"{quote}\"",
        ])
    return "\n".join(lines)


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") and "\n---" in text[4:]


def update_text(text: str, item: Dict) -> str:
    block = build_trace_block(item)
    if has_frontmatter(text):
        end = text.find("\n---", 4)
        fm = text[4:end]
        rest = text[end:]
        # 试点回写只处理尚无 trace 字段的文件，避免重复/覆盖人工内容。
        if "trace_status:" in fm or "source_refs:" in fm:
            return text
        return "---\n" + fm.rstrip() + "\n" + block + rest
    return "---\n" + block + "\n---\n\n" + text


def main():
    apply = "--apply" in sys.argv
    changed = []
    for item in load_verified():
        rel = item.get("file")
        if not rel:
            continue
        path = ROOT / rel
        if not path.exists():
            continue
        old = path.read_text(encoding="utf-8")
        new = update_text(old, item)
        if new != old:
            changed.append(str(path.relative_to(ROOT)))
            if apply:
                path.write_text(new, encoding="utf-8")
    print(json.dumps({"apply": apply, "changed_count": len(changed), "changed_files": changed}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
