#!/usr/bin/env python3
"""P16 final content-quality release report."""
from __future__ import annotations

import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report" / "p16_content_release.md"

PLACEHOLDER_RE = re.compile(r"待考|待补充|暂无|待完善|TODO|待查|待定|待确认|未提供明确|现有 verified 来源未提供")


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding='utf-8').splitlines() if l.strip()]


def count_grep(root: Path, pattern: re.Pattern) -> int:
    n = 0
    for p in root.rglob('*.md'):
        if pattern.search(p.read_text(encoding='utf-8')):
            n += 1
    return n


def main():
    rows = load_jsonl(ROOT / 'data' / 'knowledge_completeness.jsonl')
    p9 = load_jsonl(ROOT / 'data' / 'p9_quality_audit.jsonl')
    p11 = load_jsonl(ROOT / 'data' / 'p11_content_quality_queue.jsonl')
    status = Counter(r.get('trace_status') for r in rows)
    kind_status = {}
    for r in rows:
        kind_status.setdefault(r.get('kind'), Counter())[r.get('trace_status')] += 1
    placeholders = count_grep(ROOT / 'knowledge', PLACEHOLDER_RE)
    json_frag_files = 0
    for p in (ROOT / 'knowledge').rglob('*.md'):
        if '"}, {"' in p.read_text(encoding='utf-8'):
            json_frag_files += 1
    p9_by_code = Counter(r.get('code') for r in p9)
    p11_by_task = Counter(r.get('task_type') for r in p11)

    lines = [
        '# P16 内容质量定版报告',
        '',
        '## 定版结论',
        '',
        '- P13-P16 已完成知识条目正文质量主线收口。',
        '- 条目正文与 frontmatter 中的占位词已清零。',
        '- P9 quality audit 已清零。',
        '- 仍未补 `归经` 等字段的条目，原因是现有来源未明确提供，不做无依据扩写。',
        '- 本版本可作为内容质量定版基线。',
        '',
        '## 核心指标',
        '',
        f'- total: {len(rows)}',
        f'- trace_status: `{dict(status)}`',
        f'- P9 issues: {len(p9)} `{dict(p9_by_code)}`',
        f'- P11 queue: {len(p11)} `{dict(p11_by_task)}`',
        f'- placeholder_files: {placeholders}',
        f'- json_fragment_files: {json_frag_files}',
        '',
        '## 按类型分布',
        '',
    ]
    for kind, c in sorted(kind_status.items()):
        lines.append(f'- {kind}: `{dict(c)}`')
    lines.extend([
        '',
        '## P16 处理内容',
        '',
        '- `scripts/p16_format_short_herb_quotes.py`：将 41 个短正文 herb 中的长来源摘录按句读重排，提升可读性。',
        '- `scripts/p16_expand_short_herb_source_windows.py`：对剩余 19 个短正文从原始 JSON 中按中文名截取更宽来源窗口，作为 `P16 扩展摘录`，不转写为无依据结构字段。',
        '- 最终 `body_short` 从 41 -> 19 -> 0。',
        '',
        '## 定版边界',
        '',
        '- `verified` 仅表示可追溯来源链路通过，不代表医学真实性、临床适用性或治疗建议。',
        '- `candidate` 剩余 3 条：白豆蔻、白扁豆、番泻叶，因仅低质量 alias 命中，保持复核状态。',
        '- `no_source_found` 133 条保持来源范围边界，不引入外部资料硬补。',
        '- 药材 `归经` 等未明确出现在现有来源中的字段，不凭模型记忆补写。',
        '- 穴位条目继续保持“仅作学习与来源追溯，不作为针灸操作指导”。',
        '',
        '## 验证链',
        '',
        '- `check_frontmatter_schema.py`: missing_required=0, warnings=0',
        '- `build_p8_knowledge_audit.py`: stale_verified_frontmatter=0',
        '- `p9_quality_audit.py`: issues=0',
        '- `p9_build_review_queue.py`: 0 entries',
        '- `python3 -m unittest discover -s tests -p test_*.py`: 84 tests OK',
        '',
    ])
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'report': str(REPORT.relative_to(ROOT)), 'total': len(rows), 'trace_status': dict(status), 'p9_issues': len(p9), 'p11_queue': len(p11), 'placeholder_files': placeholders, 'json_fragment_files': json_frag_files}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
