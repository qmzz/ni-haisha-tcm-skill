#!/usr/bin/env python3
"""
倪海厦中医 Skill CLI 入口工具
提供命令行诊断、查询、学习功能

用法：
  python3 cli.py diagnose "发热恶寒无汗脉浮紧"
  python3 cli.py formula 桂枝汤
  python3 cli.py herb 麻黄
  python3 cli.py acupoint 合谷
  python3 cli.py concept 阴阳
  python3 cli.py case 001
  python3 cli.py source 桂枝汤
  python3 cli.py formula-source 桂枝汤
  python3 cli.py herb-source 麻黄
  python3 cli.py acupoint-source 百会
  python3 cli.py stats
"""

import sys
import json
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from internal.diagnosis_engine import DiagnosisEngine
from internal.source_corpus import SourceCorpus

SKILL_DIR = Path(__file__).parent
KNOWLEDGE_DIR = SKILL_DIR / "knowledge"


def diagnose(symptoms_str: str, as_json: bool = False):
    """辨证辅助功能"""
    engine = DiagnosisEngine()
    symptoms = [s.strip() for s in symptoms_str.split(",") if s.strip()]
    result = engine.analyze(symptoms)

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"\n{'='*60}")
    print(f"🩺 中医辨证辅助结果（学习参考）")
    print(f"{'='*60}")
    print(f"【用途说明】{result['disclaimer']}")
    print(f"\n【输入症状】{', '.join(symptoms)}")

    safety = result.get('safety', {})
    if safety.get('red_flags'):
        print("\n【安全提醒】检测到高风险信号：")
        for item in safety['red_flags']:
            print(f"  - {item['keyword']}：{item['reason']}")
        print("  建议优先联系专业医师或及时就医；本系统不继续给出方剂参考。")
        print(f"\n{'='*60}")
        return

    print(f"\n{result['analysis']}")

    formula = result['formula']
    print(f"\n【相关方剂参考】{formula['name']}")
    if formula.get('ingredients'):
        print(f"  组成：{formula['ingredients']}")
    if formula.get('dosage'):
        print(f"  原文/资料用法参考：{formula['dosage']}")
    if formula.get('ni_comment'):
        print(f"  资料讲解：{formula['ni_comment']}")
    if formula.get('contraindications'):
        print(f"  禁忌/慎用：{formula['contraindications']}")
    if formula.get('modifications'):
        print(f"\n  加减线索：")
        for m in formula['modifications']:
            print(f"    - {m}")

    if result.get('missing_questions'):
        print("\n【建议补充问诊】")
        for q in result['missing_questions']:
            print(f"  - {q}")

    print(f"\n{'='*60}")


def formula_search(name: str):
    """方剂查询"""
    # 查找方剂文件
    formula_file = None
    for f in KNOWLEDGE_DIR.glob("formulas/*.md"):
        if name in f.stem or name in f.read_text(encoding='utf-8')[:200]:
            formula_file = f
            break
    
    if formula_file:
        content = formula_file.read_text(encoding='utf-8')
        print(f"\n{'='*60}")
        print(f"💊 方剂：{name}")
        print(f"{'='*60}")
        # 只显示倪师讲解部分
        if "## 🌿 倪师讲解" in content:
            start = content.find("## 🌿 倪师讲解")
            print(content[start:start+2000])
        else:
            print(content[:1500])
    else:
        print(f"❌ 未找到方剂：{name}")


def herb_search(name: str):
    """药材查询"""
    herb_file = None
    for f in KNOWLEDGE_DIR.glob("herbs/*.md"):
        if name in f.stem or name in f.read_text(encoding='utf-8')[:200]:
            herb_file = f
            break
    
    if herb_file:
        content = herb_file.read_text(encoding='utf-8')
        print(f"\n{'='*60}")
        print(f"🌿 药材：{name}")
        print(f"{'='*60}")
        print(content[:1500])
    else:
        print(f"❌ 未找到药材：{name}")


def acupoint_search(name: str):
    """穴位查询"""
    acupoint_file = None
    for f in KNOWLEDGE_DIR.glob("acupoints/*.md"):
        if name in f.stem or name in f.read_text(encoding='utf-8')[:200]:
            acupoint_file = f
            break
    
    if acupoint_file:
        content = acupoint_file.read_text(encoding='utf-8')
        print(f"\n{'='*60}")
        print(f"🪡 穴位：{name}")
        print(f"{'='*60}")
        print(content[:1500])
    else:
        print(f"❌ 未找到穴位：{name}")


def concept_search(name: str):
    """概念查询"""
    concept_file = None
    for f in KNOWLEDGE_DIR.glob("concepts/*.md"):
        if name in f.stem or name in f.read_text(encoding='utf-8')[:200]:
            concept_file = f
            break
    
    if concept_file:
        content = concept_file.read_text(encoding='utf-8')
        print(f"\n{'='*60}")
        print(f"📖 概念：{name}")
        print(f"{'='*60}")
        print(content[:2000])
    else:
        print(f"❌ 未找到概念：{name}")


def case_search(num: str):
    """医案查询"""
    case_file = KNOWLEDGE_DIR / "cases" / f"case_{num.zfill(3)}_*.md"
    matches = list(KNOWLEDGE_DIR.glob(f"cases/case_{num.zfill(3)}_*.md"))
    if matches:
        content = matches[0].read_text(encoding='utf-8')
        print(f"\n{'='*60}")
        print(f"📋 医案：{matches[0].name}")
        print(f"{'='*60}")
        print(content)
    else:
        print(f"❌ 未找到医案编号：{num}")


def _record_source_search(kind: str, data_file: str, id_key: str, name: str, as_json: bool = False):
    """查询结构化条目的原始来源候选。"""
    source_file = SKILL_DIR / "data" / data_file
    build_hint = {
        "formula_sources.jsonl": "python3 scripts/build_formula_sources.py",
        "herb_sources.jsonl": "python3 scripts/build_herb_sources.py",
        "acupoint_sources.jsonl": "python3 scripts/build_acupoint_sources.py",
    }.get(data_file, "对应 build_*_sources.py")
    if not source_file.exists():
        print(f"❌ 未找到 data/{data_file}，请先运行：{build_hint}")
        return

    matches = []
    with source_file.open("r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if name in record.get("name", "") or name == record.get(id_key):
                matches.append(record)

    exact_matches = [m for m in matches if name == m.get("name") or name == m.get(id_key)]
    if exact_matches:
        matches = exact_matches

    result = {"query": name, "kind": kind, "matches": matches}
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"\n{'='*60}")
    print(f"🔗 {kind}来源候选")
    print(f"{'='*60}")
    if not matches:
        print(f"未找到{kind}来源候选：{name}")
        return
    for record in matches:
        source_label = record.get('source') or record.get('meridian') or '来源未标注'
        print(f"\n【{record['name']}】{record[id_key]} · {source_label}")
        if not record.get("source_hits"):
            print("  暂无来源候选，需进入 review 队列人工核对。")
            continue
        for i, hit in enumerate(record.get("source_hits", [])[:5], 1):
            page = f"第 {hit['page_num']} 页" if hit.get("page_num") else "页码未知"
            print(f"\n[{i}] {hit['source_file']} · {page}")
            print(hit["quote"])
    print(f"\n{'='*60}")


def formula_source_search(name: str, as_json: bool = False):
    """查询方剂的原始来源候选"""
    _record_source_search("方剂", "formula_sources.jsonl", "formula_id", name, as_json)


def herb_source_search(name: str, as_json: bool = False):
    """查询药材的原始来源候选"""
    _record_source_search("药材", "herb_sources.jsonl", "herb_id", name, as_json)


def acupoint_source_search(name: str, as_json: bool = False):
    """查询穴位的原始来源候选"""
    _record_source_search("穴位", "acupoint_sources.jsonl", "acupoint_id", name, as_json)


def source_search(keyword: str, as_json: bool = False):
    """检索原始 JSON 来源"""
    corpus = SourceCorpus()
    result = {
        "source_dir": str(corpus.source_dir),
        "available": corpus.available(),
        "keyword": keyword,
        "hits": [hit.to_dict() for hit in corpus.search(keyword, limit=10)],
    }
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"\n{'='*60}")
    print("🔎 原始资料检索")
    print(f"{'='*60}")
    print(f"【来源目录】{result['source_dir']}")
    print(f"【关键词】{keyword}")
    if not result["available"]:
        print("❌ 原始 JSON 来源目录不可用，请设置 NIHAIXIA_SOURCE_DIR 或检查 project/nihaixia。")
        return
    if not result["hits"]:
        print("未检索到匹配原文。")
        return
    for i, hit in enumerate(result["hits"], 1):
        page = f"第 {hit['page_num']} 页" if hit.get("page_num") else "页码未知"
        print(f"\n[{i}] {hit['source_file']} · {page}")
        print(hit["quote"])
    print(f"\n{'='*60}")


def source_manifest(as_json: bool = False):
    """查看原始 JSON 来源清单"""
    corpus = SourceCorpus()
    items = corpus.manifest()
    if as_json:
        print(json.dumps({"source_dir": str(corpus.source_dir), "files": items}, ensure_ascii=False, indent=2))
        return

    print(f"\n{'='*60}")
    print("📚 原始 JSON 来源清单")
    print(f"{'='*60}")
    print(f"【来源目录】{corpus.source_dir}")
    for item in items:
        if "error" in item:
            print(f"- {item['source_file']}：ERROR {item['error']}")
        else:
            print(f"- {item['source_file']}：{item.get('pages')} 页 / {item.get('chars')} 字符 / {item.get('bytes')} bytes")
    print(f"\n{'='*60}")


def stats():
    """统计信息"""
    print(f"\n{'='*60}")
    print(f"📊 倪海厦中医 Skill 统计")
    print(f"{'='*60}")
    
    herbs = list(KNOWLEDGE_DIR.glob("herbs/*.md"))
    acupoints = list(KNOWLEDGE_DIR.glob("acupoints/*.md"))
    formulas = list(KNOWLEDGE_DIR.glob("formulas/*.md"))
    concepts = list(KNOWLEDGE_DIR.glob("concepts/*.md"))
    diagnosis = list(KNOWLEDGE_DIR.glob("diagnosis/*.md"))
    cases = list(KNOWLEDGE_DIR.glob("cases/*.md"))
    
    print(f"🌿 药材：{len(herbs)} 味")
    print(f"🪡 穴位：{len(acupoints)} 个")
    print(f"💊 方剂：{len(formulas)} 首")
    print(f"📖 概念：{len(concepts)} 个")
    print(f"🩺 诊断：{len(diagnosis)} 篇")
    print(f"📋 医案：{len(cases)} 篇")
    
    # 药材补全度
    complete_herbs = sum(1 for f in herbs if "待考" not in f.read_text(encoding='utf-8'))
    print(f"\n🌿 药材补全度：{complete_herbs}/{len(herbs)}")
    
    # 穴位补全度
    complete_acupoints = sum(1 for f in acupoints if "待补充" not in f.read_text(encoding='utf-8'))
    print(f"🪡 穴位补全度：{complete_acupoints}/{len(acupoints)}")
    
    # 方剂讲解
    formulas_with_commentary = sum(1 for f in formulas if "倪师讲解" in f.read_text(encoding='utf-8'))
    print(f"💊 方剂讲解：{formulas_with_commentary}/{len(formulas)}")
    
    print(f"\n{'='*60}")


def help():
    """帮助信息"""
    print(f"""
{'='*60}
🏛️ 倪海厦中医 Skill - CLI 工具
{'='*60}

用法：
  python3 cli.py diagnose "症状1,症状2,..."  辨证辅助（学习参考）
  python3 cli.py formula <方剂名>          查询方剂
  python3 cli.py herb <药材名>             查询药材
  python3 cli.py acupoint <穴位名>         查询穴位
  python3 cli.py concept <概念名>          查询概念
  python3 cli.py case <编号>              查看医案
  python3 cli.py stats                     统计信息
  python3 cli.py sources                   查看原始 JSON 来源清单
  python3 cli.py source <关键词>           检索原始 JSON 原文片段
  python3 cli.py formula-source <方剂名>   查询方剂来源候选
  python3 cli.py herb-source <药材名>      查询药材来源候选
  python3 cli.py acupoint-source <穴位名>  查询穴位来源候选
  python3 cli.py help                      显示帮助

示例：
  python3 cli.py diagnose "发热,恶寒,无汗,脉浮紧"
  python3 cli.py formula 桂枝汤
  python3 cli.py herb 麻黄
  python3 cli.py acupoint 合谷
  python3 cli.py case 001
  python3 cli.py source 桂枝汤
  python3 cli.py formula-source 桂枝汤
  python3 cli.py herb-source 麻黄
  python3 cli.py acupoint-source 百会
  python3 cli.py stats

{'='*60}
""")


def main():
    if len(sys.argv) < 2:
        help()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        "diagnose": lambda: diagnose(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "formula": lambda: formula_search(" ".join(sys.argv[2:])), 
        "herb": lambda: herb_search(" ".join(sys.argv[2:])),
        "acupoint": lambda: acupoint_search(" ".join(sys.argv[2:])),
        "concept": lambda: concept_search(" ".join(sys.argv[2:])),
        "case": lambda: case_search(" ".join(sys.argv[2:])),
        "source": lambda: source_search(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "sources": lambda: source_manifest(as_json="--json" in sys.argv),
        "formula-source": lambda: formula_source_search(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "herb-source": lambda: herb_source_search(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "acupoint-source": lambda: acupoint_source_search(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "stats": stats,
        "help": help,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ 未知命令：{command}")
        help()


if __name__ == "__main__":
    main()
