#!/usr/bin/env python3
"""Remove placeholder fields from knowledge frontmatter.

If frontmatter contains values like 待考 / 待补充, remove those lines.
Do not infer or invent replacement values.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report" / "p13_frontmatter_placeholder_clean_report.md"
PLACEHOLDER_VALUE_RE = re.compile(r'^\s*[^:#][^:]*:\s*["\']?(待考|待补充|暂无|待完善|待查|待定|待确认)["\']?\s*$')


def split_frontmatter(text: str):
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---\n', 4)
    if end == -1:
        return None, text
    return text[4:end], text[end+5:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    changed_files = []
    removed = 0
    lines_report = ['# P13 frontmatter placeholder clean', '', f'apply: {args.apply}', '']

    for p in sorted((ROOT/'knowledge').rglob('*.md')):
        text = p.read_text(encoding='utf-8')
        fm, body = split_frontmatter(text)
        if fm is None:
            continue
        new_lines = []
        file_removed = []
        for i, line in enumerate(fm.splitlines(), start=1):
            if PLACEHOLDER_VALUE_RE.match(line):
                file_removed.append(f'line {i}: {line.strip()}')
                removed += 1
            else:
                new_lines.append(line)
        if file_removed:
            changed_files.append(str(p.relative_to(ROOT)))
            for x in file_removed:
                lines_report.append(f'- `{p.relative_to(ROOT)}`: {x}')
            if args.apply:
                p.write_text('---\n' + '\n'.join(new_lines).rstrip() + '\n---\n' + body, encoding='utf-8')

    lines_report += ['', f'changed_files: {len(changed_files)}', f'removed_frontmatter_placeholders: {removed}', '', '说明：frontmatter 中无来源依据的占位字段直接删除，不补写。']
    REPORT.write_text('\n'.join(lines_report)+'\n', encoding='utf-8')
    print(json.dumps({'apply': args.apply, 'changed_files': len(changed_files), 'removed_frontmatter_placeholders': removed, 'report': str(REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
