#!/usr/bin/env python3
"""P9-B: 修复 frontmatter title 为空的问题。

优先级：
1. data/*_index.jsonl 中的 name
2. Markdown 正文第一个一级标题
3. 文件名 stem
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

KINDS = {
    "formula": (ROOT / "knowledge" / "formulas", DATA / "formula_index.jsonl", "formula_id"),
    "herb": (ROOT / "knowledge" / "herbs", DATA / "herb_index.jsonl", "herb_id"),
    "acupoint": (ROOT / "knowledge" / "acupoints", DATA / "acupoint_index.jsonl", "acupoint_id"),
}


def load_name_map(path: Path, id_key: str) -> dict[str, str]:
    if not path.exists():
        return {}
    out = {}
    for line in path.open(encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        file = r.get("file")
        name = r.get("name") or r.get("display_name")
        if file and name:
            out[file] = name
    return out


def first_heading(body: str) -> str | None:
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line.strip())
        if m:
            return m.group(1).strip()
    return None


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---", 4)
    if end < 0:
        return [], text
    return text[4:end].splitlines(), text[end + 4 :].lstrip("\n")


def upsert_title(lines: list[str], title: str):
    for i, line in enumerate(lines):
        if line.strip().startswith("title:"):
            lines[i] = f'title: "{title}"'
            return
    lines.insert(0, f'title: "{title}"')


def main():
    changed = []
    for kind, (folder, index_path, id_key) in KINDS.items():
        names = load_name_map(index_path, id_key)
        for path in sorted(folder.glob("*.md")):
            if "index" in path.name:
                continue
            rel = str(path.relative_to(ROOT))
            text = path.read_text(encoding="utf-8")
            lines, body = split_frontmatter(text)
            if not lines:
                continue
            title_line = next((l for l in lines if l.strip().startswith("title:")), "")
            raw = title_line.split(":", 1)[1].strip().strip('"') if ":" in title_line else ""
            if raw:
                continue
            title = names.get(rel) or first_heading(body) or path.stem
            old = text
            upsert_title(lines, title)
            new = "---\n" + "\n".join(lines).rstrip() + "\n---\n\n" + body.lstrip("\n")
            if new != old:
                path.write_text(new, encoding="utf-8")
                changed.append({"file": rel, "title": title})
    print(json.dumps({"changed": len(changed), "first": changed[:20]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
