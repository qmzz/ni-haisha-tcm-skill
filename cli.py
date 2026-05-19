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
  python3 cli.py stats
"""

import sys
import json
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from internal.diagnosis_engine import DiagnosisEngine

SKILL_DIR = Path(__file__).parent
KNOWLEDGE_DIR = SKILL_DIR / "knowledge"


def diagnose(symptoms_str: str):
    """诊断功能"""
    engine = DiagnosisEngine()
    symptoms = [s.strip() for s in symptoms_str.split(",") if s.strip()]
    result = engine.analyze(symptoms)
    
    print(f"\n{'='*60}")
    print(f"🩺 智能诊断结果")
    print(f"{'='*60}")
    print(f"【输入症状】{', '.join(symptoms)}")
    print(f"\n{result['analysis']}")
    
    formula = result['formula']
    print(f"\n【推荐方剂】{formula['name']}")
    if formula.get('ingredients'):
        print(f"  组成：{formula['ingredients']}")
    if formula.get('dosage'):
        print(f"  用法：{formula['dosage']}")
    if formula.get('ni_comment'):
        print(f"  倪师讲解：{formula['ni_comment']}")
    if formula.get('contraindications'):
        print(f"  禁忌：{formula['contraindications']}")
    if formula.get('modifications'):
        print(f"\n  加减建议：")
        for m in formula['modifications']:
            print(f"    - {m}")
    
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
  python3 cli.py diagnose "症状1,症状2,..."  智能诊断
  python3 cli.py formula <方剂名>          查询方剂
  python3 cli.py herb <药材名>             查询药材
  python3 cli.py acupoint <穴位名>         查询穴位
  python3 cli.py concept <概念名>          查询概念
  python3 cli.py case <编号>              查看医案
  python3 cli.py stats                     统计信息
  python3 cli.py help                      显示帮助

示例：
  python3 cli.py diagnose "发热,恶寒,无汗,脉浮紧"
  python3 cli.py formula 桂枝汤
  python3 cli.py herb 麻黄
  python3 cli.py acupoint 合谷
  python3 cli.py case 001
  python3 cli.py stats

{'='*60}
""")


def main():
    if len(sys.argv) < 2:
        help()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        "diagnose": lambda: diagnose(" ".join(sys.argv[2:])),
        "formula": lambda: formula_search(" ".join(sys.argv[2:])),
        "herb": lambda: herb_search(" ".join(sys.argv[2:])),
        "acupoint": lambda: acupoint_search(" ".join(sys.argv[2:])),
        "concept": lambda: concept_search(" ".join(sys.argv[2:])),
        "case": lambda: case_search(" ".join(sys.argv[2:])),
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
