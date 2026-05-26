import json
from collections import Counter, defaultdict

rows=[]
for path in ['data/herb_index.jsonl','data/acupoint_index.jsonl']:
    for l in open(path,encoding='utf-8'):
        if l.strip():
            r=json.loads(l)
            kind='herb' if 'herb_id' in r else 'acupoint'
            item_id=r.get('herb_id') or r.get('acupoint_id')
            if r.get('trace_status')=='candidate':
                hits=r.get('source_refs') or []
                scores=[h.get('quality_score',0) for h in hits]
                rows.append((kind,item_id,r.get('name'),max(scores) if scores else 0, len(hits)))

print('candidate total',len(rows),Counter(k for k,_,_,_,_ in rows))
for kind in ['herb','acupoint']:
    sub=[r for r in rows if r[0]==kind]
    print('\n',kind,len(sub))
    buckets=Counter()
    for _,_,_,score,_ in sub:
        if score>=95: buckets['>=95']+=1
        elif score>=90: buckets['90-94']+=1
        elif score>=80: buckets['80-89']+=1
        elif score>=70: buckets['70-79']+=1
        elif score>=60: buckets['60-69']+=1
        else: buckets['<60']+=1
    print(buckets)
    for r in sorted(sub, key=lambda x:-x[3])[:20]:
        print(r)
