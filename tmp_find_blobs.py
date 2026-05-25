import subprocess
out=subprocess.check_output(['git','fsck','--unreachable','--no-reflogs'], text=True, stderr=subprocess.STDOUT)
oids=[]
for line in out.splitlines():
    parts=line.split()
    if len(parts)>=3 and parts[0]=='unreachable' and parts[1]=='blob':
        oids.append(parts[2])
best=[]
for o in oids:
    try:
        raw=subprocess.check_output(['git','cat-file','-p',o], text=True, stderr=subprocess.DEVNULL)
    except Exception:
        continue
    if '"decision": "verified"' not in raw:
        continue
    lines=raw.splitlines()
    # jsonl decision file likely every line json and has many lines
    if len(lines) >= 400:
        # validate first few lines json-ish
        if all(l.strip().startswith('{') for l in lines[:5]):
            best.append((len(lines), o))
best.sort(reverse=True)
print(best[:20])
