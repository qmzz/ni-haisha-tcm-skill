import os, glob, json, time, re
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request

API_BASE = "http://192.168.110.10:8317/v1/chat/completions"
MODEL = "deepseek-v4.1-flash"
CPA_API_KEY = "sk-wnTOVEBVQFvlZVNkciXcDO1uiVpSNRl6g88X7HkSe5B8QKnO997u9l549AKZXMqw"

CONCEPTS_DIR = "/home/percy/projects/ni-haisha-tcm-skill/knowledge/concepts"
DIAGNOSIS_DIR = "/home/percy/projects/ni-haisha-tcm-skill/knowledge/diagnosis"
CASES_DIR = "/home/percy/projects/ni-haisha-tcm-skill/knowledge/cases"

# 载入人纪全套语料库
CORPUS_FILES = [
    '/home/percy/.openclaw/workspace/archive/nihaixia/extracted/01【视频同步文稿】人-针灸篇（可打印）.json',
    '/home/percy/.openclaw/workspace/archive/nihaixia/extracted/02【视频同步文稿】人-神农本草经（可打印）.json',
    '/home/percy/.openclaw/workspace/archive/nihaixia/extracted/04【视频同步文稿】人-伤寒论（可打印）.json',
    '/home/percy/.openclaw/workspace/archive/nihaixia/extracted/05【视频同步文稿】人-金匮要略（可打印）.json',
    '/home/percy/projects/ni-haisha-tcm-skill/倪海厦人纪系列之针灸篇.json',
    '/home/percy/projects/ni-haisha-tcm-skill/倪海厦人纪系列之神农本草经.json',
    '/home/percy/projects/ni-haisha-tcm-skill/倪海厦人纪系列之伤寒论.json',
    '/home/percy/projects/ni-haisha-tcm-skill/倪海厦人纪系列之金匮要略.json'
]

print("[1/4] 载入人纪全景原典语料库...")
corpus_texts = []
for cp in CORPUS_FILES:
    if os.path.exists(cp):
        try:
            with open(cp, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                if isinstance(data, list):
                    for item in data:
                        text = item.get('content') or item.get('text') or str(item)
                        corpus_texts.append(text)
                elif isinstance(data, dict):
                    for k, v in data.items():
                        corpus_texts.append(str(v))
        except Exception as e:
            print(f"载入语料 {cp} 失败: {e}")

print(f"语料库加载完成，有效片段共 {len(corpus_texts)} 节")

def search_corpus(keyword, max_snippets=4):
    hits = []
    kw = keyword.replace("篇", "").replace("证", "").replace("病", "").replace("辩证", "").replace("辨证", "")
    for text in corpus_texts:
        if keyword in text or (len(kw) >= 2 and kw in text):
            hits.append(text[:2000])
            if len(hits) >= max_snippets:
                break
    return "\n\n---\n\n".join(hits)

NAME_MAP = {
    # Concepts
    "bafa.md": "八法（汗吐下和温清消补）",
    "bagang.md": "八纲（阴阳表里寒热虚实）",
    "bingyin_bingji.md": "病因病机与内生五邪",
    "dachang.md": "大肠（传导之官与肺之表里）",
    "dan.md": "胆（中正之官与少阳枢纽）",
    "fanzhifa.md": "反治法与从治法",
    "fei.md": "肺（相傅之官与气之本）",
    "gan.md": "肝（将军之官与罢极之本）",
    "jing.md": "精（先天之精与后天之精）",
    "jingluo.md": "经络（经脉络脉与气血通道）",
    "jinye.md": "津液（津液生成输布与水饮转化）",
    "jinye_xiedai.md": "津液代谢与水热互结",
    "liujing.md": "六经（太阳阳明少阳太阴少阴厥阴）",
    "liuyin.md": "六淫（风寒暑湿燥火外感病因）",
    "neisheng_wuxie.md": "内生五邪（风寒湿燥火）",
    "pangguang.md": "膀胱（州都之官与气化出焉）",
    "pi.md": "脾（谏议之官与后天之本）",
    "qi.md": "气（元气宗气营气卫气与升降出入）",
    "qiqing.md": "七情（喜怒忧思悲恐惊致病）",
    "qixue_jinye.md": "气血津液辨证总要",
    "qixue_shichang.md": "气血失常（气虚气滞血虚血瘀）",
    "sanjiao.md": "三焦（决渎之官与水火气化通道）",
    "shen.md": "肾（作强之官与先天之本）",
    "tanyin.md": "痰饮（悬饮溢饮支饮与水气病）",
    "wangwenwenqie.md": "望闻问切四诊总纲",
    "wei.md": "胃（仓廪之官与水谷气血之海）",
    "weiqi.md": "卫气（卫外阳气与开合固表）",
    "wuxing.md": "五行（木火土金水生克制化与象数）",
    "xiao chang.md": "小肠（受盛之官与心火下移之源）",
    "xin.md": "心（君主之官与神明之舍）",
    "xinbao.md": "心包（臣使之官与代心受邪）",
    "xue.md": "血（营血运行脉道与生化之源）",
    "yingqi.md": "营气（化生血液行于脉中之精气）",
    "yinyang.md": "阴阳（天地之道万物之纲纪）",
    "yinyang_shitiao.md": "阴阳失调（阴阳偏盛偏衰与亡阴亡阳）",
    "yuanqi.md": "元气（命门真火与先天根源）",
    "yuxue.md": "瘀血（离经之血与癥瘕积聚）",
    "zangfu.md": "脏腑（五脏六腑表里奇恒之腑）",
    "zhengxiangzhengdu.md": "真假寒热与真假虚实",
    "zhengxie.md": "正邪相争与扶正祛邪",
    "zhihe_zhifa.md": "治病求本与标本缓急",
    "zhize_zhifa.md": "治则治法（因时因地因人制宜）",
    "zongqi.md": "宗气（积于胸中贯心脉行呼吸）",

    # Diagnosis
    "bagang_bianzheng.md": "八纲辨证（阴阳表里寒热虚实鉴别法）",
    "baoli_bianzheng.md": "表里辨证与半表半里",
    "bianzheng_gangyao.md": "辨证纲要与六经八纲互参",
    "bianzheng_zonglun.md": "辨证总论（倪海厦经方辨证核心心法）",
    "bingyin_bianzheng.md": "病因辨证（外感六淫与内伤七情）",
    "fei_bianzheng.md": "肺系病辨证（肺寒肺热肺阴虚与水饮射肺）",
    "feixi_bianzheng.md": "肺系脏腑相兼辨证（肺胃肺肾合病）",
    "gan_bianzheng.md": "肝胆病辨证（肝郁肝火肝风与阴寒滞肝）",
    "ganxin_bianzheng.md": "肝心合病辨证（木火刑金与血虚心神不宁）",
    "hanre_bianzheng.md": "寒热辨证（真热假寒与真寒假热鉴别）",
    "jingluo_bianzheng.md": "经络辨证（十二经脉与奇经八脉循行病候）",
    "jueyin_bing.md": "厥阴病辨证（寒热错杂厥热胜复与消渴吐蛔）",
    "liujing_bianzheng.md": "六经辨证（伤寒传变与方证对应体系）",
    "liuyin_bianzheng.md": "六淫外感辨证（风寒暑湿燥火伤人法度）",
    "pi_bianzheng.md": "脾病辨证（太阴湿寒中焦不运与水湿泛滥）",
    "piwei_bianzheng.md": "脾胃合病辨证（中焦虚寒虚痞与升降失调）",
    "qiezhen.md": "切诊心法（寸口人迎脉法与寸关尺辨病）",
    "qiezhen_muban.md": "切脉法度与二十八脉主病真髓",
    "qiqing_bianzheng.md": "七情内伤辨证与脏腑气机逆乱",
    "qixue_jinye_bianzheng.md": "气血津液辨证（气虚血瘀津枯水停）",
    "sanjiao_bianzheng.md": "三焦辨证（上焦中焦下焦传变与决渎水道）",
    "shaoyang_bing.md": "少阳病辨证（口苦咽干目眩往来寒热枢机不利）",
    "shaoyin_bing.md": "少阴病辨证（但欲寐脉微细从寒化从热化）",
    "shen_bianzheng.md": "肾病辨证（肾阳虚命门火衰水饮凌心与肾阴竭）",
    "shenxi_bianzheng.md": "肾系合病辨证（心肾不交水火未济与金水相生）",
    "shiwenge.md": "倪海厦十问歌与问诊抓手（寒热汗头身便饮食渴睡等）",
    "taiyang_bing.md": "太阳病辨证（中风伤寒温病与经腑传变）",
    "taiyin_bing.md": "太阴病辨证（腹满而吐食不下自利益甚）",
    "tan_yin_bianzheng.md": "痰饮水湿辨证（四饮分类与温阳化饮）",
    "wangzhen.md": "望诊心法（望神望色望目望舌与形体动态）",
    "wangzhen_muban.md": "望诊秘要（眼诊辨五脏与舌苔辨寒热真假）",
    "weiqi_yingxue.md": "卫气营血辨证与温病传变规律",
    "weiqi_yingxue_bianzheng.md": "卫气营血深度辨证与经方温病对照",
    "wenzhen.md": "闻诊心法（听声音闻气味辨虚实寒热）",
    "wenzhen_ask.md": "问诊十大纲目与倪师临证抓手",
    "wenzhen_muban.md": "倪师问诊模板与动态辨证流程",
    "wenzhen_muban2.md": "问诊深度鉴别模板与方证推演",
    "xin_bianzheng.md": "心病辨证（心阳虚心血瘀阻心阴虚与水气凌心）",
    "xixin_bianzheng.md": "心系相兼辨证（心脾两虚心肾水火不交）",
    "xushi_bianzheng.md": "虚实辨证（邪气盛则实精气夺则虚）",
    "yangming_bing.md": "阳明病辨证（经证大热大渴大汗脉洪大与腑证痞满燥实坚）",
    "yinyang_bianzheng.md": "阴阳辨证（阴阳离决亡阳亡阴与阴阳互根）",
    "yu_xue_bianzheng.md": "瘀血辨证（蓄血证桃核承气抵当汤与癥瘕）",
    "zangfu_bianzheng.md": "脏腑辨证总纲（五脏六腑生克制化与表里合治）"
}

PROMPT_CONCEPTS = """你是由倪海厦经方中医体系严格训练的中医精雕宗师。
任务：请根据提供的概念名称及倪师原典语料，重构撰写极其纯正、高密度、直击本质的倪海厦中医核心概念解析 Markdown。

【输出结构严格要求】：
必须严格且只包含以下四个标准的二级标题（保持 emoji 与字样完全一致）：
## ☯️ 阴阳五行与脏腑本源
## 🫀 倪师水火气化推演心法
## 🎯 临床病理演变与传变规律
## 🗣️ 倪师讲义实录与发挥

【写作原则】：
1. 坚决剔除任何免责声明、工业套话、机械占位符。
2. 彻底还原倪海厦经方体系的水火气化、物理模型（如心脏如火、小肠如热炉、肺如天幕地覆、肾如水库）。
3. 语言极富穿透力，大白话讲透至理。
"""

PROMPT_DIAGNOSIS = """你是由倪海厦经方中医体系严格训练的中医精雕宗师。
任务：请根据提供的诊断/辨证条目名称及倪师语料，重构撰写极其纯正、高密度、直击本质的倪海厦经方诊断与辨证 Markdown。

【输出结构严格要求】：
必须严格且只包含以下四个标准的二级标题（保持 emoji 与字样完全一致）：
## 👁️ 诊断要诀与原典法度
## ⚡ 倪师望闻问切破局心法
## 🎯 六经辨证抓手与鉴别要点
## 🗣️ 倪师讲义实录与问诊秘要

【写作原则】：
1. 坚决剔除任何免责声明、工业套话、机械占位符。
2. 还原倪师极具特色的临床实战抓手：眼诊看五脏、十问歌辨生死、摸手脚冷热辨阴阳、寸口人迎脉法。
3. 突出方证鉴别，怎么一击必中。
"""

PROMPT_CASES = """你是由倪海厦经方中医体系严格训练的中医精雕宗师。
任务：请根据提供的医案名称和现有病例信息，重构撰写极其纯正、跌宕起伏、病机严密的倪海厦经方实战医案解析 Markdown。

【输出结构严格要求】：
必须严格且只包含以下五个标准的二级标题（保持 emoji 与字样完全一致）：
## 📋 病案实录与四诊信息
## 🫀 倪师水火病机深层推演
## 💊 经方法度处方与剂量配伍
## 📈 瞑眩反应与转归追踪
## 💡 倪师按语与画龙点睛

【写作原则】：
1. 坚决剔除任何免责声明、工业套话、现代医学病理解剖说明。
2. 处方用量使用经典汉制折算或实战克数，讲透为什么用此方、为什么重用某药。
3. 倪师按语必须入木三分，讲清生克与破局。
"""

def process_file(task_type, file_path):
    fname = os.path.basename(file_path)
    title = NAME_MAP.get(fname, fname.replace('.md', ''))
    
    # 提取现有文件的一些内容（特别是医案）
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
        raw_c = fp.read()
    
    snippets = search_corpus(title, max_snippets=4)
    
    if task_type == 'concept':
        sys_prompt = PROMPT_CONCEPTS
        user_prompt = f"核心概念名称：{title}\n\n相关倪师原典语料：\n{snippets}\n\n请按四大标准二级标题输出纯正概念 Markdown。"
    elif task_type == 'diagnosis':
        sys_prompt = PROMPT_DIAGNOSIS
        user_prompt = f"诊断辨证条目：{title}\n\n相关倪师原典语料：\n{snippets}\n\n请按四大标准二级标题输出纯正诊断辨证 Markdown。"
    else: # case
        sys_prompt = PROMPT_CASES
        user_prompt = f"医案标题：{title}\n\n现有病例参考：\n{raw_c[:1500]}\n\n相关倪师语料：\n{snippets}\n\n请按五大标准二级标题输出纯正经方医案 Markdown。"
    
    req_body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 4096,
        "thinking": {"type": "disabled"}
    }
    
    req = urllib.request.Request(
        API_BASE,
        data=json.dumps(req_body).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CPA_API_KEY}"
        }
    )
    
    with urllib.request.urlopen(req, timeout=90) as response:
        res = json.loads(response.read().decode('utf-8'))
        content = res['choices'][0]['message']['content'].strip()
    
    final_content = f"# {title}\n\n" + content
    with open(file_path, 'w', encoding='utf-8') as fp:
        fp.write(final_content)
    return title, fname, len(final_content)

all_tasks = []

# Concepts
for f in glob.glob(f"{CONCEPTS_DIR}/*.md"):
    fn = os.path.basename(f)
    if fn.endswith('_index.md') or fn.endswith('_plan.md'): continue
    all_tasks.append(('concept', f))

# Diagnosis
for f in glob.glob(f"{DIAGNOSIS_DIR}/*.md"):
    fn = os.path.basename(f)
    if fn.endswith('_index.md'): continue
    all_tasks.append(('diagnosis', f))

# Cases
for f in glob.glob(f"{CASES_DIR}/*.md"):
    fn = os.path.basename(f)
    if fn.endswith('_index.md'): continue
    all_tasks.append(('case', f))

print(f"[3/4] 扫描全量待重构任务共: {len(all_tasks)} 个 (Concepts: 43, Diagnosis: 44, Cases: 51)")
print("[4/4] 启动 10 并发重构流水线...")

start_time = time.time()
completed = 0
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(process_file, t_type, fp): (t_type, fp) for t_type, fp in all_tasks}
    for future in as_completed(futures):
        t_type, fp = futures[future]
        completed += 1
        elapsed = time.time() - start_time
        try:
            t, fn, size = future.result()
            print(f"[{completed}/{len(all_tasks)}] ({elapsed:.1f}s) ✅ [{t_type}] 《{t}》 重构完成 ({fn}, {size}B)")
        except Exception as e:
            print(f"[{completed}/{len(all_tasks)}] ❌ [{t_type}] 失败 {os.path.basename(fp)}: {e}")

print(f"🎉 全部 {len(all_tasks)} 个文件重构完毕，总耗时 {time.time()-start_time:.1f}s")
