#!/usr/bin/env python3
"""P11-E: 为 no_source_found 条目补充明确 scope 边界。

不补医学正文，不改变 trace_status。仅在 frontmatter 中补充：
- source_scope: not_in_nihaixia_source
- external_reference_required: true
- no_source_policy: keep_boundary_until_traceable_source

用于明确：这些条目在当前倪海厦原始 JSON 与现有别名扩展检索中无明确命中，
后续若要提升必须引入可追溯外部来源，而不是凭模型记忆补全。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p11_e_no_source_scope_report.md"

MARKERS = {
    "source_scope": "not_in_nihaixia_source",
    "external_reference_required": True,
    "no_source_policy": "keep_boundary_until_traceable_source",
}


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def parse_frontmatter(text: str) -> Tuple[str, str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    return text[:4], text[4:end], text[end:]


def yaml_scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    return json.dumps(v, ensure_ascii=False)


def upsert_simple_keys(fm: str) -> Tuple[str, bool]:
    changed = False
    lines = fm.splitlines()
    for k, v in MARKERS.items():
        prefix = f"{k}:"
        new_line = f"{k}: {yaml_scalar(v)}"
        found = False
        for i, line in enumerate(lines):
            if line.startswith(prefix):
                found = True
                if line != new_line:
                    lines[i] = new_line
                    changed = True
                break
        if not found:
            lines.append(new_line)
            changed = True
    return "\n".join(lines) + "\n", changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    rows = [r for r in load_jsonl(DATA / "knowledge_completeness.jsonl") if r.get("trace_status") == "no_source_found"]
    changed_files = []
    errors = []
    by_kind = {}

    for r in rows:
        by_kind[r.get("kind")] = by_kind.get(r.get("kind"), 0) + 1
        rel = r.get("file")
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
            pre, fm, rest = parse_frontmatter(text)
            new_fm, changed = upsert_simple_keys(fm)
            if changed:
                changed_files.append(rel)
                if args.apply:
                    path.write_text(pre + new_fm + rest, encoding="utf-8")
        except Exception as e:
            errors.append({"file": rel, "error": str(e)})

    REPORT.parent.mkdir(exist_ok=True)
    lines = [
        "# P11-E no_source_found scope 边界报告",
        "",
        f"- apply: {args.apply}",
        f"- no_source_found total: {len(rows)}",
        f"- changed_files: {len(changed_files)}",
        f"- errors: {len(errors)}",
        "",
        "## 分类",
        "",
    ]
    for k in sorted(by_kind):
        lines.append(f"- {k}: {by_kind[k]}")
    lines += [
        "",
        "## 边界策略",
        "",
        "这些条目在当前倪海厦原始 JSON 与既有别名扩展检索中无明确命中。",
        "本阶段不凭模型记忆补写医学正文，不改变 trace_status；仅补充 frontmatter scope 元数据。",
        "若后续要提升，必须引入明确可追溯的外部来源。",
        "",
        "新增/规范化 frontmatter:",
        "",
        "```yaml",
        "source_scope: \"not_in_nihaixia_source\"",
        "external_reference_required: true",
        "no_source_policy: \"keep_boundary_until_traceable_source\"",
        "```",
        "",
        "## 变更文件",
        "",
    ]
    for rel in changed_files:
        lines.append(f"- `{rel}`")
    if errors:
        lines += ["", "## Errors", ""]
        for e in errors:
            lines.append(f"- `{e['file']}`: {e['error']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "apply": args.apply,
        "total": len(rows),
        "by_kind": by_kind,
        "changed_files": len(changed_files),
        "errors": errors,
        "report": str(REPORT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
