#!/usr/bin/env python3
"""P9-A: 数据质量审计。

目标：不再只看 verified 数，而是检查知识文件本身的数据质量。

检查项：
- 文件存在性
- frontmatter 基础字段
- 正文长度/空壳
- 安全边界
- source_refs / verified registry 一致性
- 重复中文名
- 低置信 verified 来源
- parent expand / alias expand verified 需要人工复核

输出：
- data/p9_quality_audit.jsonl
- report/p9_quality_audit.md
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p9_quality_audit.md"
OUT = DATA / "p9_quality_audit.jsonl"

KINDS = {
    "formula": ROOT / "knowledge" / "formulas",
    "herb": ROOT / "knowledge" / "herbs",
    "acupoint": ROOT / "knowledge" / "acupoints",
}

REQUIRED_FM = ["title", "kind", "trace_status"]


def load_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def parse_frontmatter(text: str) -> Tuple[Dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 5 :]
    fm: Dict[str, object] = {}
    key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", line):
            k, v = line.split(":", 1)
            key = k.strip()
            fm[key] = v.strip().strip('"')
        elif key:
            # 简单标记多行结构存在即可
            fm[key] = fm.get(key, "") or "__complex__"
    return fm, body


def clean_body_lines(body: str) -> List[str]:
    lines = []
    in_notice = False
    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        if "P5_STANDARD_NOTICE_START" in s:
            in_notice = True
            continue
        if "P5_STANDARD_NOTICE_END" in s:
            in_notice = False
            continue
        if in_notice:
            continue
        if s.startswith("---"):
            continue
        lines.append(s)
    return lines


def issue(file: str, kind: str, level: str, code: str, detail: str = "") -> Dict:
    return {"file": file, "kind": kind, "level": level, "code": code, "detail": detail}


def main():
    verified = load_jsonl(DATA / "verified_sources.jsonl")
    decisions = load_jsonl(DATA / "review_decisions.jsonl")

    verified_by_file = defaultdict(list)
    for v in verified:
        verified_by_file[v.get("file", "")].append(v)

    decision_by_file = defaultdict(list)
    for d in decisions:
        decision_by_file[d.get("file", "")].append(d)

    all_issues: List[Dict] = []
    name_index = defaultdict(list)

    for kind, folder in KINDS.items():
        for path in sorted(folder.glob("*.md")):
            if "index" in path.name:
                continue
            rel = str(path.relative_to(ROOT))
            text = path.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)
            lines = clean_body_lines(body)
            title = fm.get("title") or ""
            name_index[(kind, title)].append(rel)

            for key in REQUIRED_FM:
                if key not in fm:
                    all_issues.append(issue(rel, kind, "error", "missing_frontmatter_key", key))

            if fm.get("kind") and fm.get("kind") != kind:
                all_issues.append(issue(rel, kind, "error", "kind_mismatch", str(fm.get("kind"))))

            trace = fm.get("trace_status", "")
            if trace == "verified" and rel not in verified_by_file:
                all_issues.append(issue(rel, kind, "error", "verified_frontmatter_not_in_registry"))
            if rel in verified_by_file and trace != "verified":
                all_issues.append(issue(rel, kind, "error", "registry_verified_but_frontmatter_not_verified", str(trace)))

            if trace == "verified" and "source_refs" not in fm:
                all_issues.append(issue(rel, kind, "error", "verified_without_source_refs"))

            if len(lines) == 0:
                all_issues.append(issue(rel, kind, "error", "empty_body"))
            elif len(lines) < 5:
                all_issues.append(issue(rel, kind, "warning", "body_too_short", f"lines={len(lines)}"))
            elif len(lines) < 10:
                all_issues.append(issue(rel, kind, "info", "body_short", f"lines={len(lines)}"))

            has_notice = "P5_STANDARD_NOTICE_START" in text or "安全边界" in text
            if trace == "verified" and not has_notice:
                all_issues.append(issue(rel, kind, "warning", "verified_without_safety_notice"))

    # 重复中文名/标题
    for (kind, title), files in name_index.items():
        if title and len(files) > 1:
            for f in files:
                all_issues.append(issue(f, kind, "warning", "duplicate_title", ", ".join(files)))

    # 低置信 / parent expand verified 决策审计
    for d in decisions:
        notes = d.get("notes", "") or ""
        rel = d.get("file", "")
        kind = d.get("kind", "")
        if "parent name expand" in notes or "parent expand" in notes:
            all_issues.append(issue(rel, kind, "review", "parent_expand_verified_needs_human_review", notes))
        if "QUALITY_OVERRIDES" in notes or "score=" in notes:
            m = re.search(r"score=(\d+)", notes)
            if m and int(m.group(1)) < 70:
                all_issues.append(issue(rel, kind, "review", "low_score_verified_needs_review", notes))

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for row in all_issues:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    counter = Counter((r["level"], r["code"]) for r in all_issues)
    by_level = Counter(r["level"] for r in all_issues)
    by_kind = Counter(r["kind"] for r in all_issues)

    lines = [
        "# P9 数据质量审计报告",
        "",
        "## 定位",
        "",
        "本报告检查知识库内容质量，不修改医学正文，不自动提升 verified。",
        "",
        "## 总览",
        "",
        f"- issues: {len(all_issues)}",
        f"- by_level: {dict(by_level)}",
        f"- by_kind: {dict(by_kind)}",
        "",
        "## 问题类型 Top",
        "",
        "| level | code | count |",
        "|-------|------|-------|",
    ]
    for (level, code), count in counter.most_common(30):
        lines.append(f"| {level} | {code} | {count} |")

    lines += ["", "## 样例（前 100 条）", "", "| level | kind | code | file | detail |", "|-------|------|------|------|--------|"]
    for r in all_issues[:100]:
        detail = str(r.get("detail", "")).replace("|", "/")[:120]
        lines.append(f"| {r['level']} | {r['kind']} | {r['code']} | {r['file']} | {detail} |")

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"issues": len(all_issues), "by_level": dict(by_level), "by_kind": dict(by_kind)}, ensure_ascii=False))
    print(f"wrote {OUT}")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
