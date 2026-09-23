#!/usr/bin/env python3
import os, re, sys, json, time, glob, subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

CPA_BASE_URL = "http://192.168.110.10:8317/v1"
CPA_API_KEY = "sk-wnTOVEBVQFvlZVNkciXcDO1uiVpSNRl6g88X7HkSe5B8QKnO997u9l549AKZXMqw"
MODEL_NAME = "deepseek-v4.1-flash"

EXTRACTED_DIR = "/home/percy/.openclaw/workspace/archive/nihaixia/extracted"
PROJECT_DIR = "/home/percy/projects/ni-haisha-tcm-skill"
ACUPOINTS_DIR = os.path.join(PROJECT_DIR, "knowledge/acupoints")

sys.stdout.reconfigure(line_buffering=True)

print("[1/4] 加载人纪针灸视频文稿与经络原典语料库...", flush=True)

sources = {
    "zhenjiu": [
        "01【视频同步文稿】人-针灸篇（可打印）.json",
        "倪海厦人纪系列之针灸篇.json",
        "人纪-针灸大成.json"
    ],
    "shanghan_jinkui": [
        "04【视频同步文稿】人-伤寒论（可打印）.json",
        "05【视频同步文稿】人-金匮要略（可打印）.json"
    ]
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

print("[2/4] 从 git 初始版本恢复全量 411 个穴位中文名与经络归属映射...", flush=True)
all_files = [os.path.basename(f) for f in glob.glob(os.path.join(ACUPOINTS_DIR, "*.md")) if not os.path.basename(f).startswith("acupoint_index")]
NAME_MAP = {}
for fname in all_files:
    try:
        out = subprocess.check_output(["git", "-C", PROJECT_DIR, "show", f"6aed486:knowledge/acupoints/{fname}"], stderr=subprocess.DEVNULL).decode("utf-8", errors="ignore")
        m = re.search(r'#\s+([^\n\r#]+)', out)
        if m:
            NAME_MAP[fname] = m.group(1).strip()
    except Exception:
        pass
print(f"  - 成功映射 {len(NAME_MAP)} / {len(all_files)} 个穴位名称", flush=True)

def search_corpus(query, max_chars=6000):
    hits = []
    # 提取纯穴位名，如 "中脘"、"足三里"、"合谷"
    pure_name = query.split()[0].replace("穴", "").strip()
    keywords = [pure_name, query]
    for cat in ("zhenjiu", "shanghan_jinkui"):
        for p in CORPUS.get(cat, []):
            score = 0
            for kw in keywords:
                if kw in p:
                    score += p.count(kw) * 5
            if score > 0:
                hits.append((score, p))
    hits.sort(key=lambda x: x[0], reverse=True)
    total_text = ""
    for score, p in hits[:10]:
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
        "thinking": {"type": "disabled"},
        "messages": [
            {"role": "system", "content": "你是一位精通倪海厦人纪针灸大成、经络气血循行与五输穴子母补泻体系的资深针灸导师。你必须严格按给定的Markdown标题输出纯净结构，严禁任何免责声明、P5_STANDARD、安全边界、学习参考、解剖神经血管干瘪填表等工业八股。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 4096
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                choice = result["choices"][0]
                content = choice["message"].get("content", "").strip()
                if not content:
                    raise ValueError(f"Empty content returned (finish_reason: {choice.get('finish_reason')})")
                return content
        except Exception as e:
            time.sleep(2 * (attempt + 1))
            if attempt == 2:
                raise e

REQUIRED_HEADERS = [
    "## 📍 经络归属与精准取穴法",
    "## ⚡ 倪师经穴气化与破局心法",
    "## 🎯 临床主治与配穴组合手印",
    "## 🗣️ 倪师讲义实录与针灸秘要"
]

def check_file_valid(filepath):
    if not os.path.exists(filepath):
        return False, "文件不存在"
    size = os.path.getsize(filepath)
    if size < 600:
        return False, f"文件过短({size}B)"
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()
    missing = [h for h in REQUIRED_HEADERS if h not in c]
    if missing:
        return False, f"缺少结构: {missing}"
    return True, "达标"

def process_acupoint(filename):
    filepath = os.path.join(ACUPOINTS_DIR, filename)
    title = NAME_MAP.get(filename, filename.replace(".md", ""))
    raw_evidence = search_corpus(title, max_chars=6000)
    prompt = f"""请根据以下【原始逐字稿证据池】以及《人纪·针灸篇》《针灸大成》倪海厦讲义，对针灸腧穴《{title}》进行彻底重构转写。
必须严格包含以下四个主二级标题（一个字不能改）：

# {title}

## 📍 经络归属与精准取穴法
- 所属经络与五输穴/特定穴属性（如井荥输经合、原穴、络穴、郄穴、募穴、背俞穴、八会穴等五行生克定位）
- 倪师动态取穴与骨度折量法（大白话讲透怎么摸骨找穴、下针深度、禁针禁灸法则）

## ⚡ 倪师经穴气化与破局心法
- 倪师如何推演此穴的气血流注与开阖机理（如引火归元、健脾行水、升提中气、开窍醒神等自然机理）
- 子母补泻与五行生克运用心法（虚则补其母，实则泻其子）

## 🎯 临床主治与配穴组合手印
- 核心特效主治病症（急症救逆、慢性病调理、妇科/儿科/痛症特效）
- 倪师经典对穴与排针组合（如合谷配太冲开四关、足三里配三阴交、公孙配内关治胃心胸等）

## 🗣️ 倪师讲义实录与针灸秘要
- 视频讲义中倪师讲此穴的原汁原味逐字稿金句、实战手下针感体会、医案故事

【原始逐字稿证据池】：
{raw_evidence if raw_evidence else "以人纪针灸篇与倪师讲义为准"}
"""
    new_md = call_llm(prompt)
    if len(new_md.strip()) < 500:
        raise ValueError(f"生成内容过短: {len(new_md)} 字符")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_md)
    return title

# 扫描需转写/补全的文件
flawed_files = []
for fname in all_files:
    fp = os.path.join(ACUPOINTS_DIR, fname)
    valid, reason = check_file_valid(fp)
    if not valid:
        flawed_files.append((fname, reason))

print(f"[3/4] 扫描完成: 共 411 个穴位，其中待重构转写文件: {len(flawed_files)} 个", flush=True)

if not flawed_files:
    print("🎉 411 个穴位全部 100% 达标！", flush=True)
    sys.exit(0)

print(f"[4/4] 启动 10 并发精雕引擎 (deepseek-v4.1-flash + thinking disabled)...", flush=True)

done = 0
t0 = time.time()
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = {ex.submit(process_acupoint, item[0]): item[0] for item in flawed_files}
    for f in as_completed(futs):
        fname = futs[f]
        try:
            name = f.result()
            done += 1
            elapsed = time.time() - t0
            print(f"[{done}/{len(flawed_files)}] ({elapsed:.1f}s) ✅ 《{name}》 重构转写完成 ({fname})", flush=True)
        except Exception as e:
            print(f"[ERROR] ❌ {fname} 失败: {e}", flush=True)

print(f"全部穴位重构转写完毕！耗时: {time.time()-t0:.1f}s", flush=True)
