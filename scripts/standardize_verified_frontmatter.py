#!/usr/bin/env python3
"""P6-A：将 frontmatter / 安全边界标准化扩展到 verified 条目。

默认 dry-run；使用 --apply 写入。
支持 --kind formula/herb/acupoint 与 --limit N。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

NOTICE_START = "<!-- P5_STANDARD_NOTICE_START -->"
NOTICE_END = "<!-- P5_STANDARD_NOTICE_END -->"

KIND_LABEL = {
    "formula": "方剂",
    "herb": "药材",
    "acupoint": "穴位",
}


def opt(name: str, default=None):
    if name not in sys.argv:
        return default
    idx = sys.argv.index(name)
    if idx + 1 >= len(sys.argv):
        return default
    return sys.argv[idx + 1]


def load_jsonl(path: Path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---", 4)
    if end < 0:
        return [], text
    return text[4:end].splitlines(), text[end + 4 :].lstrip("\n")


def upsert_scalar(lines, key: str, value: str):
    prefix = f"{key}:"
    for idx, line in enumerate(lines):
        if line.strip().startswith(prefix):
            lines[idx] = f"{key}: {value}"
            return
    insert_at = 1 if lines and lines[0].strip().startswith("title:") else len(lines)
    lines.insert(insert_at, f"{key}: {value}")


def notice(kind: str) -> str:
    label = KIND_LABEL.get(kind, kind)
    extra = "\n- 穴位内容仅作学习与来源追溯，不作为针灸操作指导。" if kind == "acupoint" else ""
    return f"""{NOTICE_START}

## 学习与安全边界

本条目用于中医学习、资料检索与来源追溯。内容不构成诊断、处方、用药、针灸操作或治疗建议；涉及剂量、配伍、禁忌、针药操作等内容时，必须由合格专业人士结合实际情况判断。

## 来源追溯状态

- 条目类型：{label}
- 追溯状态：verified
- 来源引用：见本文 frontmatter 中的 `source_refs`{extra}
- 复核说明：P6 verified 标准化条目，优先统一治理元数据与安全边界，不自动改写正文医学内容。

{NOTICE_END}
"""


def insert_notice(body: str, kind: str):
    block = notice(kind).rstrip() + "\n\n"
    if NOTICE_START in body and NOTICE_END in body:
        start = body.find(NOTICE_START)
        end = body.find(NOTICE_END, start)
        end += len(NOTICE_END)
        return body[:start].rstrip() + "\n\n" + block + body[end:].lstrip("\n")
    marker = "\n## "
    idx = body.find(marker)
    if idx >= 0:
        return body[:idx].rstrip() + "\n\n" + block + body[idx:].lstrip("\n")
    return block + body


def standardize(record: dict, apply: bool):
    rel = record.get("file")
    kind = record.get("kind")
    if not rel or not kind:
        return None
    path = ROOT / rel
    if not path.exists():
        return {"file": rel, "kind": kind, "changed": False, "error": "missing_file"}
    original = path.read_text(encoding="utf-8")
    lines, body = split_frontmatter(original)
    if not lines:
        lines = [f'title: "{record.get("name") or path.stem}"']
    before_lines = list(lines)
    upsert_scalar(lines, "title", f'"{record.get("name") or path.stem}"')
    upsert_scalar(lines, "kind", f'"{kind}"')
    upsert_scalar(lines, "trace_status", "verified")
    upsert_scalar(lines, "review_status", "verified")
    upsert_scalar(lines, "reviewer", '"p6_verified_standardization"')
    upsert_scalar(lines, "safety_disclaimer_required", "true")
    upsert_scalar(lines, "content_scope", '"学习参考与资料检索，不作为诊断、处方、针灸操作或治疗建议"')
    new_body = insert_notice(body, kind)
    new_text = "---\n" + "\n".join(lines).rstrip() + "\n---\n\n" + new_body.lstrip("\n")
    changed = new_text != original
    if changed and apply:
        path.write_text(new_text, encoding="utf-8")
    return {"file": rel, "kind": kind, "changed": changed, "error": None}


def main():
    apply = "--apply" in sys.argv
    kind_filter = opt("--kind")
    limit = opt("--limit")
    limit = int(limit) if limit else None
    records = load_jsonl(DATA / "verified_sources.jsonl")
    if kind_filter:
        records = [r for r in records if r.get("kind") == kind_filter]
    if limit:
        records = records[:limit]
    results = [standardize(record, apply=apply) for record in records]
    results = [r for r in results if r]
    changed = [r for r in results if r["changed"]]
    errors = [r for r in results if r["error"]]
    print(json.dumps({
        "apply": apply,
        "processed": len(results),
        "changed_count": len(changed),
        "errors": errors,
        "changed_files": [r["file"] for r in changed],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
