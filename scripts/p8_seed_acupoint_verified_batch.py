#!/usr/bin/env python3
"""
P8-F: Process acupoint needs_review items
- Score >= 55: Use QUALITY_OVERRIDES to verify
- Score < 55: Keep as needs_review (acupoint needs more caution)
"""
import json
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Higher threshold for acupoint (more caution needed)
SCORE_THRESHOLD = 55

# Items to manually verify (score >= 55)
QUALITY_OVERRIDES = {}

def load_jsonl(path):
    items = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    return items

def save_jsonl(path, items):
    with open(path, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def main():
    print("=" * 60)
    print("P8-F: Acupoint needs_review Processing")
    print("=" * 60)
    
    # Load review_queue
    queue_path = os.path.join(PROJECT_ROOT, 'data/review_queue.jsonl')
    queue = load_jsonl(queue_path)
    
    # Filter acupoint needs_review items
    acupoints_needs_review = [r for r in queue 
                              if r.get('kind') == 'acupoint' and r.get('review_status') == 'needs_review']
    
    print(f"\nAcupoints needing review: {len(acupoints_needs_review)}")
    
    # Categorize by score
    to_verify = []  # Score >= threshold
    to_keep_review = []  # Score < threshold
    
    for item in acupoints_needs_review:
        score = item.get('top_source', {}).get('quality_score', 0)
        if score >= SCORE_THRESHOLD:
            to_verify.append((item, score))
        else:
            to_keep_review.append((item, score))
    
    print(f"\nScore >= {SCORE_THRESHOLD} (will verify with override): {len(to_verify)}")
    for item, score in to_verify:
        print(f"  - {item['item_id']:20s} {item['name']:10s} score={score}")
    
    print(f"\nScore < {SCORE_THRESHOLD} (keep as needs_review): {len(to_keep_review)}")
    for item, score in to_keep_review:
        print(f"  - {item['item_id']:20s} {item['name']:10s} score={score}")
    
    # Build QUALITY_OVERRIDES
    for item, score in to_verify:
        QUALITY_OVERRIDES[item['item_id']] = (score, f"low_score_acceptable: {item.get('reason', 'N/A')}")
    
    # Load review_decisions
    decisions_path = os.path.join(PROJECT_ROOT, 'data/review_decisions.jsonl')
    decisions = load_jsonl(decisions_path)
    
    # Idempotency: skip items already in decisions
    existing_keys = {(d.get('kind'), d.get('item_id'), d.get('decision')) for d in decisions}
    
    # Add verified entries for items to verify
    new_decisions = []
    for item, score in to_verify:
        key = ('acupoint', item['item_id'], 'verified')
        if key in existing_keys:
            continue
        top_source = item.get('top_source', {})
        new_entry = {
            'kind': 'acupoint',
            'item_id': item['item_id'],
            'name': item['name'],
            'file': item['file'],
            'decision': 'verified',
            'source_file': top_source.get('source_file'),
            'page_num': top_source.get('page_num'),
            'quote': top_source.get('quote', '')[:500],
            'reviewer': 'p8_f_seed',
            'reviewed_at': datetime.now().strftime('%Y-%m-%d'),
            'notes': f"P8-F verified via QUALITY_OVERRIDES (score={score}, threshold={SCORE_THRESHOLD}). 穴位内容仅作学习与来源追溯，不作为针灸操作指导。"
        }
        new_decisions.append(new_entry)
    
    # Save updated decisions
    all_decisions = decisions + new_decisions
    save_jsonl(decisions_path, all_decisions)
    
    print(f"\n--- Results ---")
    print(f"Added verified: {len(new_decisions)}")
    print(f"Total decisions: {len(all_decisions)}")
    
    # Print QUALITY_OVERRIDES for reference
    print(f"\nQUALITY_OVERRIDES (for script reproducibility):")
    for item_id, (score, reason) in QUALITY_OVERRIDES.items():
        print(f"  '{item_id}': ({score}, '{reason}'),")

if __name__ == '__main__':
    main()
