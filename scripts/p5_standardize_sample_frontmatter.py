#!/usr/bin/env python3
"""P5-D：对首批 10 个样板条目做 frontmatter / 安全边界结构标准化。"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SAMPLES = {
    "formula": [
        "knowledge/formulas/guizhi_tang.md",
        "knowledge/formulas/mahuang_tang.md",
        "knowledge/formulas/xiaochaihu_tang.md",
        "knowledge/formulas/wuling_san.md",
        "knowledge/formulas/banxia_xiexin.md",
    ],
    "herb": [
        "knowledge/herbs/mahuang.md",
        "knowledge/herbs/guizhi.md",
        "knowledge/herbs/gancao.md",
        "knowledge/herbs/fuzi.md",
        "knowledge/herbs/banxia.md",
    ],
}

NOTICE_START = "<!-- P5_STANDARD_NOTICE_START -->"
NOTICE_END = "<!-- P5_STANDARD_NOTICE_END -->"


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---", 4)
    if end < 0:
        return [], text
    lines = text[4:end].splitlines()
    body = text[end + 4 :].lstrip("\n")
    return lines, body


def upsert_scalar(lines, key: str, value: str):
    prefix = f"{key}:"
    for idx, line in enumerate(lines):
        if line.strip().startswith(prefix):
            lines[idx] = f'{key}: {value}'
            return
    insert_at = 1 if lines and lines[0].strip().startswith("title:") else len(lines)
    lines.insert(insert_at, f'{key}: {value}')


def notice(kind: str) -> str:
    item_name = "方剂" if kind == "formula" else "药材"
    return f"""{NOTICE_START}

## 学习与安全边界

本条目用于中医学习、资料检索与来源追溯。内容不构成诊断、处方、用药或治疗建议；涉及剂量、配伍、禁忌、针药操作等内容时，必须由合格专业人士结合实际情况判断。

## 来源追溯状态

- 条目类型：{item_name}
- 追溯状态：verified
- 来源引用：见本文 frontmatter 中的 `source_refs`
- 复核说明：P5 样板条目，优先统一治理元数据与安全边界，不自动改写正文医学内容。

{NOTICE_END}
"""


def insert_notice(body: str, kind: str) -> str:
    if NOTICE_START in body:
        return body
    marker = "\n## "
    idx = body.find(marker)
    block = notice(kind).rstrip() + "\n\n"
    if idx >= 0:
        return body[:idx].rstrip() + "\n\n" + block + body[idx:].lstrip("\n")
    return block + body


def standardize(path: Path, kind: str) -> bool:
    original = path.read_text(encoding="utf-8")
    lines, body = split_frontmatter(original)
    changed = False
    if not lines:
        title = path.stem
        lines = [f'title: "{title}"']
        changed = True
    before_lines = list(lines)
    upsert_scalar(lines, "kind", f'"{kind}"')
    upsert_scalar(lines, "review_status", "verified")
    upsert_scalar(lines, "reviewer", '"p5_sample_standardization"')
    upsert_scalar(lines, "safety_disclaimer_required", "true")
    upsert_scalar(lines, "content_scope", '"学习参考与资料检索，不作为诊断、处方或治疗建议"')
    if lines != before_lines:
        changed = True
    new_body = insert_notice(body, kind)
    if new_body != body:
        changed = True
    if changed:
        path.write_text("---\n" + "\n".join(lines).rstrip() + "\n---\n\n" + new_body.lstrip("\n"), encoding="utf-8")
    return changed


def main():
    changed_files = []
    for kind, rel_paths in SAMPLES.items():
        for rel in rel_paths:
            path = ROOT / rel
            if standardize(path, kind):
                changed_files.append(rel)
    print(f"changed_count: {len(changed_files)}")
    for rel in changed_files:
        print(f"- {rel}")


if __name__ == "__main__":
    main()
