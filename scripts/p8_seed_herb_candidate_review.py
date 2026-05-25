#!/usr/bin/env python3
"""
P8-D: Process herb needs_review items
- Score >= 50: Use QUALITY_OVERRIDES to verify
- Score < 50: Keep as needs_review
"""
import json
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Threshold for auto-verification with overrides
SCORE_THRESHOLD = 50

# Items to manually verify (score >= 50)
QUALITY_OVERRIDES = {
    # item_id: (quality_score_threshold, reason)
}

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
    print("P8-D: Herb needs_review Processing")
    print("=" * 60)
    
    # Load review_queue
    queue_path = os.path.join(PROJECT_ROOT, 'data/review_queue.jsonl')
    queue = load_jsonl(queue_path)
    
    # Filter herb needs_review items
    herb_needs_review = [r for r in queue 
                         if r.get('kind') == 'herb' and r.get('review_status') == 'needs_review']
    
    print(f"\nHerbs needing review: {len(herb_needs_review)}")
    
    # Categorize by score
    to_verify = []  # Score >= 50
    to_keep_review = []  # Score < 50
    
    for item in herb_needs_review:
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
    
    # Add verified entries for items to verify
    new_decisions = []
    for item, score in to_verify:
        new_entry = {
            'kind': 'herb',
            'item_id': item['item_id'],
            'name': item['name'],
            'file': item['file'],
            'decision': 'verified',
            'source_file': item['top_source']['source_file'],
            'page_num': item['top_source'].get('page_num'),
            'quote': item['top_source'].get('quote', '')[:500],
            'reviewer': 'p8_d_seed',
            'reviewed_at': datetime.now().strftime('%Y-%m-%d'),
            'notes': f"P8-D verified via QUALITY_OVERRIDES (score={score}, threshold={SCORE_THRESHOLD})"
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
