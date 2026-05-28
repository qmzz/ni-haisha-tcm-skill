#!/usr/bin/env python3
"""Audit complete P7 governance state."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p40_p7_completion_audit.md"


def load_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    comp=load_jsonl(DATA/'knowledge_completeness.jsonl')
    ver=load_jsonl(DATA/'verified_sources.jsonl')
    p36=load_jsonl(DATA/'p36_external_source_queue.jsonl')
    high=load_jsonl(DATA/'p39_high_risk_external_review_queue.jsonl')
    ns=[r for r in comp if r.get('source_quality_level')=='no_source']
    problems=[]
    # P7-A: contextual should be tiny and have rationale.
    contextual=[r for r in ver if r.get('source_quality_level')=='verified_contextual']
    for r in contextual:
        if not r.get('p7a_rationale'):
            problems.append({'type':'contextual_missing_p7a_rationale','key':(r.get('kind'),r.get('item_id'))})
    if len(contextual)>2:
        problems.append({'type':'too_many_contextual','count':len(contextual)})
    # P7-B: all no_source in external queue and review required.
    p36keys={(r.get('kind'),r.get('item_id')) for r in p36}
    nskeys={(r.get('kind'),r.get('item_id')) for r in ns}
    if p36keys != nskeys:
        problems.append({'type':'p36_mismatch','missing':sorted(nskeys-p36keys),'extra':sorted(p36keys-nskeys)})
    for r in ns:
        for f in ['p7b_category','p7b_phase','risk_tier','recommended_source_scopes','required_review']:
            if not r.get(f): problems.append({'type':'missing_p7b_field','key':(r.get('kind'),r.get('item_id')),'field':f})
    # P7-B-D: all high risk have safety template.
    high_keys={(r.get('kind'),r.get('item_id')) for r in p36 if r.get('risk_tier')=='high'}
    template_keys={(r.get('kind'),r.get('item_id')) for r in high}
    if high_keys != template_keys:
        problems.append({'type':'high_risk_template_mismatch','missing':sorted(high_keys-template_keys),'extra':sorted(template_keys-high_keys)})
    for r in high:
        if not r.get('required_safety_fields') or r.get('review_status')!='pending_human_review':
            problems.append({'type':'bad_high_risk_template','key':(r.get('kind'),r.get('item_id'))})
    levels=Counter(r.get('source_quality_level') for r in comp)
    p7b=Counter(r.get('p7b_category') for r in ns)
    risk=Counter(r.get('risk_tier') for r in ns)
    lines=['# P40 / P7 Completion Audit','',f'- Problems: {len(problems)}',f'- verified_contextual rows: {len(contextual)}',f'- no_source queue rows: {len(ns)}',f'- high-risk review rows: {len(high)}','','## Source quality levels','','| level | count |','|---|---:|']
    for k,v in sorted(levels.items()): lines.append(f'| `{k}` | {v} |')
    lines += ['','## P7-B categories','','| category | count |','|---|---:|']
    for k,v in sorted(p7b.items()): lines.append(f'| `{k}` | {v} |')
    lines += ['','## Risk tiers','','| risk | count |','|---|---:|']
    for k,v in sorted(risk.items()): lines.append(f'| `{k}` | {v} |')
    if problems:
        lines += ['', '## Problems', '']
        for p in problems[:100]: lines.append(f'- `{p}`')
    REPORT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'problems':len(problems),'verified_contextual':len(contextual),'no_source_rows':len(ns),'high_risk_rows':len(high),'source_quality_levels':dict(levels),'report':str(REPORT.relative_to(ROOT))},ensure_ascii=False,indent=2))
    return 1 if problems else 0

if __name__=='__main__': raise SystemExit(main())
