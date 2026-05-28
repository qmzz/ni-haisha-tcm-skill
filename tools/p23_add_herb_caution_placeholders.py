#!/usr/bin/env python3
"""P23/P3 add trace-safe herb caution placeholders.

This script does NOT invent contraindications. For herb markdown files that lack
any explicit contraindication/caution section, it appends a clearly marked
"禁忌与慎用（待考）" section that says the project has not found a traceable
source yet and actual use must be evaluated by a qualified professional.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERB_DIR = ROOT / "knowledge" / "herbs"
REPORT = ROOT / "report" / "p23_herb_caution_placeholders.md"

CAUTION_KEYWORDS = ["配伍禁忌", "禁忌", "注意事项", "慎用", "不宜"]
PLACEHOLDER_HEADING = "## ⚠️ 禁忌与慎用（待考）"
PLACEHOLDER_BLOCK = f"""
{PLACEHOLDER_HEADING}

本条目当前未在已治理来源中提取到明确、可追溯的禁忌或慎用原文；不得据此推定“无禁忌”。
涉及实际用药、剂量、配伍、孕产妇、儿童、老人、基础病或正在服用其他药物等情况，必须由合格专业人士结合实际情况判断。
""".strip()


def has_caution(text: str) -> bool:
    return any(k in text for k in CAUTION_KEYWORDS)


def insert_before_safety(text: str) -> str:
    marker = "\n## 学习与安全边界"
    if marker in text:
        return text.replace(marker, "\n" + PLACEHOLDER_BLOCK + "\n" + marker, 1)
    return text.rstrip() + "\n\n" + PLACEHOLDER_BLOCK + "\n"


def main() -> int:
    changed = []
    skipped = []
    for path in sorted(HERB_DIR.glob("*.md")):
        if "index" in path.name:
            continue
        text = path.read_text(encoding="utf-8")
        if has_caution(text):
            skipped.append(str(path.relative_to(ROOT)))
            continue
        new_text = insert_before_safety(text)
        path.write_text(new_text, encoding="utf-8")
        changed.append(str(path.relative_to(ROOT)))

    lines = [
        "# P23 / P3 Herb Caution Placeholder Rollout",
        "",
        "本报告记录 P3 对缺少显式禁忌/慎用文字的 herb 条目补充 trace-safe 待考边界。",
        "",
        "> 原则：不凭模型补写具体禁忌；只标记“未提取到可追溯禁忌原文”，并强化不得推定无禁忌。",
        "",
        f"- Changed herb files: {len(changed)}",
        f"- Skipped herb files already having caution text: {len(skipped)}",
        "",
        "## Changed files",
        "",
    ]
    lines.extend(f"- `{x}`" for x in changed)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"changed": len(changed), "skipped": len(skipped), "report": str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
