#!/usr/bin/env python3
import os, re, sys, json, time, glob
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

CPA_BASE_URL = "http://192.168.110.10:8317/v1"
CPA_API_KEY = "sk-wnTOVEBVQFvlZVNkciXcDO1uiVpSNRl6g88X7HkSe5B8QKnO997u9l549AKZXMqw"
MODEL_NAME = "deepseek-v4.1-flash"

EXTRACTED_DIR = "/home/percy/.openclaw/workspace/archive/nihaixia/extracted"
PROJECT_DIR = "/home/percy/projects/ni-haisha-tcm-skill"

sys.stdout.reconfigure(line_buffering=True)

print("[1/3] 加载人纪文稿语料库（本草、伤寒、金匮）...", flush=True)

sources = {
    "bencao": ["02【视频同步文稿】人-神农本草经（可打印）.json", "倪海厦人纪系列之神农本草经.json", "神农本草经.json"],
    "shanghan": ["04【视频同步文稿】人-伤寒论（可打印）.json", "倪海厦人纪系列之伤寒论.json"],
    "jinkui": ["05【视频同步文稿】人-金匮要略（可打印）.json", "倪海厦人纪系列之金匮要略.json"]
}

CORPUS = {}
for cat, filenames in sources.items():
    CORPUS[cat] = []
    for fn in filenames:
        p = os.path.join(EXTRACTED_DIR, fn)
        if not os.path.exists(p):
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        txt = item.get("text") or item.get("content") or ""
                        if txt.strip():
                            CORPUS[cat].append(txt.strip())
                elif isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, str) and v.strip():
                            CORPUS[cat].append(v.strip())
                        elif isinstance(v, list):
                            for item in v:
                                if isinstance(item, str) and item.strip():
                                    CORPUS[cat].append(item.strip())
                                elif isinstance(item, dict):
                                    txt = item.get("text") or item.get("content") or ""
                                    if txt.strip():
                                        CORPUS[cat].append(txt.strip())
        except Exception as e:
            print(f"Error loading {fn}: {e}", flush=True)

for k, v in CORPUS.items():
    print(f"  - 分类 {k}: 载入 {len(v)} 个段落", flush=True)

def search_corpus(query, max_chars=7000):
    hits = []
    keywords = [query]
    if query.endswith("根") or query.endswith("皮") or query.endswith("子") or query.endswith("叶") or query.endswith("草"):
        if len(query) > 2:
            keywords.append(query[:-1])
    for cat in ("bencao", "shanghan", "jinkui"):
        for p in CORPUS.get(cat, []):
            score = 0
            for kw in keywords:
                if kw in p:
                    score += p.count(kw) * 5
            if score > 0:
                hits.append((score, p))
    hits.sort(key=lambda x: x[0], reverse=True)
    total_text = ""
    for score, p in hits[:12]:
        if len(total_text) + len(p) > max_chars:
            total_text += p[:max_chars - len(total_text)] + "\n...\n"
            break
        total_text += p + "\n---\n"
    return total_text

def call_llm(prompt):
    url = f"{CPA_BASE_URL}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CPA_API_KEY}"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "你是一位精通倪海厦经方医学与人纪神农本草经体系的资深中医导师。你必须严格按给定的Markdown标题输出纯净结构，严禁任何免责声明、P5_STANDARD、安全边界、学习参考、十八反死记、植物科属形态等工业八股。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 4096
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            time.sleep(2 * (attempt + 1))
            if attempt == 2:
                raise e

def process_herb(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        old_content = f.read()
    m = re.search(r'#\s+(.+)', old_content)
    title = m.group(1).strip() if m else filename.replace(".md", "")
    raw_evidence = search_corpus(title, max_chars=7000)
    prompt = f"""请根据以下【原始逐字稿证据池】以及《神农本草经》倪海厦人纪讲义，对中药材《{title}》进行彻底重构转写。
必须严格包含以下四个主二级标题（一个字不能改）：

# {title}

## 🌿 神农本草原意与性味气味
- 《神农本草经》原文字句（若神农未收载则引经典本草出处）
- 气味与阴阳升降属性（气厚气薄、味厚味薄、法象天地之生）

## 🫀 倪师药性推演与破局心法
- 倪师如何理解这味药的灵魂（如生附子破阴实 vs 炮附子固表阳；生姜散胃水 vs 干姜温肺饮；石膏清阳明大热；大黄推陈致新）
- 用通俗大白话与自然物理比喻讲透药理机理

## 🎯 临床用量法度与配伍抓手
- 倪师常用剂量法度（常规克数与急危重症重剂法）
- 经方经典药对配伍要诀（如桂枝配白芍、柴胡配黄芩、附子配干姜、麻黄配石膏等）
- 临证眼目与辨证使用禁忌

## 🗣️ 倪师讲义实录与发挥
- 视频讲义中倪师讲这味药的原汁原味金句、生动比喻或临床实战体会

【原始逐字稿证据池】：
{raw_evidence if raw_evidence else "以神农本草经与倪师人纪讲义为准"}
"""
    new_md = call_llm(prompt)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_md)
    return title

tasks = []
for fp in sorted(glob.glob(f"{PROJECT_DIR}/knowledge/herbs/*.md")):
    if os.path.basename(fp).startswith("herb_index"):
        continue
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    if "## 🌿 神农本草原意与性味气味" not in c or "## 🫀 倪师药性推演与破局心法" not in c:
        tasks.append(fp)

print(f"[2/3] 锁定待转写药材: {len(tasks)} 味，严格采用 10 并发 + deepseek-v4.1-flash 启动转写...", flush=True)

done = 0
t0 = time.time()
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = {ex.submit(process_herb, fp): fp for fp in tasks}
    for f in as_completed(futs):
        fp = futs[f]
        try:
            name = f.result()
            done += 1
            elapsed = time.time() - t0
            print(f"[{done}/{len(tasks)}] ({elapsed:.1f}s) ✅ 《{name}》 转写完成 ({os.path.basename(fp)})", flush=True)
        except Exception as e:
            print(f"[ERROR] ❌ {os.path.basename(fp)} 失败: {e}", flush=True)

print(f"[3/3] 全部药材转写完毕！耗时: {time.time()-t0:.1f}s", flush=True)
