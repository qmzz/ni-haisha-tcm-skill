#!/usr/bin/env python3
"""P10-C acupoint source_trace_notice 全覆盖。

为所有穴位文件添加来源追溯声明。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from internal.frontmatter import parse_frontmatter

FOLDER = ROOT / "knowledge" / "acupoints"

SOURCE_TRACE_NOTICE = """## 来源追溯状态

本条目内容来源于倪海厦老师教学资料，已建立来源追溯索引。

- **追溯方式**: 通过 `source_refs` 字段关联原始视频/文稿
- **验证状态**: 见 frontmatter `trace_status`
- **用途**: 仅作学习与来源追溯，不作为针灸操作指导
"""


def has_source_trace_notice(text: str) -> bool:
    markers = [
        "来源追溯状态",
        "source_refs",
        "追溯状态",
        "追溯方式",
    ]
    return any(m in text for m in markers)


def add_notice(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    
    if has_source_trace_notice(text):
        return False
    
    # 追加到文件末尾
    new_text = text.rstrip() + "\n\n" + SOURCE_TRACE_NOTICE + "\n"
    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    added = 0
    skipped = 0
    
    for path in sorted(FOLDER.glob("*.md")):
        if "index" in path.name:
            continue
        
        if add_notice(path):
            added += 1
        else:
            skipped += 1
    
    print(json.dumps({"added": added, "skipped": skipped}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
