#!/usr/bin/env python3
"""P8-Frontmatter: 为所有知识文件添加基础 frontmatter。

- 对于 verified 文件：已有完整 frontmatter，跳过
- 对于 candidate/no_source_found：添加基础 frontmatter (kind + trace_status)
- 对于其他文件：添加基础 frontmatter (kind + trace_status=unverified)

默认 dry-run；使用 --apply 写入。
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 加载 verified 状态
def load_verified_status():
    verified = set()
    with open(os.path.join(PROJECT_ROOT, 'data/verified_sources.jsonl'), 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                # 用 file 路径作为 key
                verified.add(item.get('file', ''))
    return verified

def load_review_queue_status():
    """加载 review_queue 中的状态"""
    status_map = {}  # file -> trace_status
    with open(os.path.join(PROJECT_ROOT, 'data/review_queue.jsonl'), 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                file_path = item.get('file', '')
                review_status = item.get('review_status', '')
                if review_status == 'needs_review':
                    status_map[file_path] = 'needs_review'
                elif review_status == 'no_source_found':
                    status_map[file_path] = 'no_source_found'
    return status_map

def parse_frontmatter(text):
    """解析 frontmatter"""
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---', 4)
    if end == -1:
        return None, text
    fm_lines = text[4:end].strip().split('\n')
    fm = {}
    for line in fm_lines:
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip().strip('"').strip("'")
    content = text[end+5:]
    return fm, content

def add_frontmatter(text, kind, trace_status):
    """添加 frontmatter"""
    fm = f"""---
title: ""
kind: {kind}
trace_status: {trace_status}
---

"""
    # 移除已有的 frontmatter
    if text.startswith('---\n'):
        end = text.find('\n---', 4)
        if end != -1:
            text = text[end+5:]
    return fm + text.lstrip('\n')

def main():
    dry_run = '--apply' not in sys.argv
    
    print(f"Mode: {'DRY-RUN' if dry_run else 'APPLY'}")
    
    # 加载状态
    verified_files = load_verified_status()
    queue_status = load_review_queue_status()
    
    print(f"Verified files: {len(verified_files)}")
    print(f"Queue status items: {len(queue_status)}")
    
    # 处理各类知识文件
    KINDS = {
        'herb': Path(PROJECT_ROOT) / 'knowledge' / 'herbs',
        'acupoint': Path(PROJECT_ROOT) / 'knowledge' / 'acupoints',
        'formula': Path(PROJECT_ROOT) / 'knowledge' / 'formulas',
    }
    
    changed = []
    
    for kind, folder in KINDS.items():
        if not folder.exists():
            continue
        
        for md_file in sorted(folder.glob('*.md')):
            if 'index' in md_file.name:
                continue
            
            file_path = str(md_file.relative_to(PROJECT_ROOT))
            text = md_file.read_text(encoding='utf-8')
            
            # 检查是否已有完整 frontmatter
            fm, _ = parse_frontmatter(text)
            
            if fm and fm.get('kind') and fm.get('trace_status'):
                # 已有完整 frontmatter，跳过
                continue
            
            # 确定 trace_status
            if file_path in verified_files:
                trace_status = 'verified'
            elif file_path in queue_status:
                trace_status = queue_status[file_path]
            else:
                trace_status = 'unverified'
            
            # 添加 frontmatter
            new_text = add_frontmatter(text, kind, trace_status)
            
            if not dry_run:
                md_file.write_text(new_text, encoding='utf-8')
            
            changed.append((file_path, kind, trace_status))
    
    print(f"\n{'Would change' if dry_run else 'Changed'}: {len(changed)} files")
    
    if changed:
        # 统计
        by_status = {}
        for f, k, s in changed:
            by_status[s] = by_status.get(s, 0) + 1
        print("By trace_status:")
        for s, c in sorted(by_status.items()):
            print(f"  {s}: {c}")
        
        # 显示前 10 个
        print("\nFirst 10 files:")
        for f, k, s in changed[:10]:
            print(f"  {f}: {k}, {s}")
    
    if dry_run:
        print("\n【DRY-RUN】Use --apply to write changes")

if __name__ == '__main__':
    main()
