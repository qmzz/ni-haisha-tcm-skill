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
  python3 cli.py fts-search 桂枝汤
  python3 cli.py formula-source 桂枝汤
  python3 cli.py herb-source 麻黄
  python3 cli.py acupoint-source 百会
  python3 cli.py trace 桂枝汤
  python3 cli.py verified-source 桂枝汤

# P7 Agent 查询编排（均支持 --json）
python3 cli.py lookup 白头翁汤
python3 cli.py explain-trace 白头翁汤
python3 cli.py review-dashboard
python3 cli.py batch-trace 桂枝汤,白头翁汤,大敦

  python3 cli.py review-queue
  python3 cli.py stats
"""

import sys
import json
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from internal.diagnosis_engine import DiagnosisEngine
from internal.source_corpus import SourceCorpus
from internal.trace_service import TraceService
from internal.fts_search import FtsSearch

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


def trace_search(query: str, as_json: bool = False):
    """统一来源追溯查询"""
    service = TraceService()
    result = service.trace(query)
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"\n{'='*60}")
    print("🧭 来源追溯")
    print(f"{'='*60}")
    print(f"【查询】{query}")
    print(f"【状态】{result['trace_status']}")
    matches = result.get("matches", [])
    if not matches:
        print("未找到可追溯来源。")
        return
    for i, item in enumerate(matches, 1):
        if "source_refs" in item:
            print(f"\n[{i}] {item.get('kind')} · {item.get('name')} · {item.get('item_id')}")
            for j, ref in enumerate(item.get("source_refs") or [], 1):
                page = f"第 {ref['page_num']} 页" if ref.get("page_num") else "页码未知"
                print(f"  ({j}) {ref.get('source_file')} · {page}")
                print(f"      {ref.get('quote')}")
        elif "top_source" in item:
            print(f"\n[{i}] {item.get('kind')} · {item.get('name')} · {item.get('review_status')}")
            print(f"    {item.get('reason')}")
        else:
            page = f"第 {item['page_num']} 页" if item.get("page_num") else "页码未知"
            print(f"\n[{i}] {item.get('source_file')} · {page}")
            print(item.get("quote"))
    print(f"\n{'='*60}")


def verified_source_search(query: str, as_json: bool = False):
    """查询 verified 来源"""
    service = TraceService()
    result = service.trace(query)
    if result.get("trace_status") != "verified":
        result = {"query": query, "trace_status": "not_verified", "matches": []}
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"\n{'='*60}")
    print("✅ Verified 来源")
    print(f"{'='*60}")
    if not result["matches"]:
        print(f"未找到 verified 来源：{query}")
        return
    for item in result["matches"]:
        print(f"\n【{item['name']}】{item['kind']} · {item['item_id']}")
        for ref in item.get("source_refs", []):
            page = f"第 {ref['page_num']} 页" if ref.get("page_num") else "页码未知"
            print(f"- {ref['source_file']} · {page}")
            print(ref["quote"])
    print(f"\n{'='*60}")



def _load_tool_function(name: str):
    """Load a JSON tool function from tools/tcm_tools.py without shelling out."""
    tools_dir = SKILL_DIR / "tools"
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    from tcm_tools import TOOLS  # type: ignore
    return TOOLS[name]


def _print_json_or_summary(result, as_json: bool = False):
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return True
    return False


def lookup_show(query: str, as_json: bool = False):
    """P7 统一查询入口：markdown 预览 + trace 摘要 + 安全边界。"""
    result = _load_tool_function("tcm_lookup")({"query": query})
    if _print_json_or_summary(result, as_json):
        return
    print(f"\n{'='*60}")
    print("🔎 TCM Lookup")
    print(f"{'='*60}")
    print(f"【查询】{result.get('query')}")
    print(f"【类型】{result.get('kind')}")
    trace = result.get("trace", {})
    print(f"【来源状态】{trace.get('trace_status')}")
    print(f"【安全边界】{result.get('safety_boundary')}")
    for item in result.get("markdown", []):
        print(f"\n【文件】{item.get('file')}")
        preview = (item.get("preview") or "").strip()
        print(preview[:900])
    print(f"\n{'='*60}")


def explain_trace_show(query: str, as_json: bool = False):
    """解释来源治理状态。"""
    result = _load_tool_function("tcm_explain_trace")({"query": query})
    if _print_json_or_summary(result, as_json):
        return
    print(f"\n{'='*60}")
    print("🧭 Trace 状态解释")
    print(f"{'='*60}")
    print(f"【查询】{result.get('query')}")
    print(f"【状态】{result.get('trace_status')}")
    print(f"【解释】{result.get('explanation')}")
    print(f"【边界】{result.get('boundary')}")
    print(f"\n{'='*60}")


def review_dashboard_show(as_json: bool = False):
    """P7 来源治理看板。"""
    result = _load_tool_function("tcm_review_dashboard")({})
    if _print_json_or_summary(result, as_json):
        return
    verified = result.get("verified", {})
    queue = result.get("review_queue", {})
    print(f"\n{'='*60}")
    print("📊 TCM Review Dashboard")
    print(f"{'='*60}")
    print(f"verified: {verified.get('count')} {verified.get('by_kind')}")
    print(f"review_queue: {queue.get('count')} unresolved={queue.get('unresolved')}")
    print(f"by_status: {queue.get('by_status')}")
    if result.get("frontmatter_audit_head"):
        print("\nfrontmatter audit:")
        for line in result.get("frontmatter_audit_head"):
            print(f"  {line}")
    print(f"\n【边界】{result.get('boundary')}")
    print(f"\n{'='*60}")


def batch_trace_show(query: str, as_json: bool = False):
    """批量查询多个条目的来源治理状态。"""
    result = _load_tool_function("tcm_batch_trace")({"query": query})
    if _print_json_or_summary(result, as_json):
        return
    print(f"\n{'='*60}")
    print("🧭 Batch Trace")
    print(f"{'='*60}")
    for item in result.get("items", []):
        print(f"- {item.get('query')}: {item.get('trace_status')} ({item.get('match_count')} matches)")
    print(f"\n【边界】{result.get('boundary')}")
    print(f"\n{'='*60}")

def _cli_option(name: str, default=None):
    if name not in sys.argv:
        return default
    idx = sys.argv.index(name)
    if idx + 1 >= len(sys.argv):
        return default
    return sys.argv[idx + 1]


def review_next_show(as_json: bool = False):
    """查看下一批未决复核条目"""
    path = SKILL_DIR / "data" / "review_queue.jsonl"
    decisions_path = SKILL_DIR / "data" / "review_decisions.jsonl"
    items = []
    decided = set()
    if decisions_path.exists():
        with decisions_path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    decided.add((row.get("kind"), row.get("item_id")))
    if path.exists():
        with path.open(encoding="utf-8") as f:
            items = [json.loads(line) for line in f if line.strip()]
    kind_filter = _cli_option("--kind")
    status_filter = _cli_option("--status")
    limit = int(_cli_option("--limit", 10))
    filtered = []
    for item in items:
        if kind_filter and item.get("kind") != kind_filter:
            continue
        if status_filter and item.get("review_status") != status_filter:
            continue
        if (item.get("kind"), item.get("item_id")) in decided:
            continue
        filtered.append(item)
    if as_json:
        print(json.dumps({"count": len(filtered), "items": filtered[:limit]}, ensure_ascii=False, indent=2))
        return
    print(f"下一批复核条目：{len(filtered)}，展示 {min(limit, len(filtered))} 条")
    for item in filtered[:limit]:
        print(f"- {item.get('kind')} {item.get('item_id')} {item.get('name')} [{item.get('review_status')}] {item.get('reason')}")


def review_import(as_json: bool = False):
    """导入人工复核模板并更新 review_decisions.jsonl"""
    import subprocess
    input_path = _cli_option("--file") or (sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "data/review_decisions.template.jsonl")
    result = subprocess.run([sys.executable, str(SKILL_DIR / "scripts" / "review_import.py"), input_path], cwd=SKILL_DIR, check=True, capture_output=True, text=True)
    if as_json:
        print(json.dumps({"ok": True, "output": result.stdout}, ensure_ascii=False, indent=2))
    else:
        print(result.stdout.strip())


def review_apply(as_json: bool = False):
    """根据 review_decisions 重新生成 verified_sources 与 review progress"""
    import subprocess
    outputs = []
    for script in ["build_verified_sources.py", "build_review_progress.py"]:
        result = subprocess.run([sys.executable, str(SKILL_DIR / "scripts" / script)], cwd=SKILL_DIR, check=True, capture_output=True, text=True)
        outputs.append(result.stdout)
    if as_json:
        print(json.dumps({"ok": True, "outputs": outputs}, ensure_ascii=False, indent=2))
    else:
        print("".join(outputs).strip())


def review_stats(as_json: bool = False):
    """查看 review 决策统计"""
    path = SKILL_DIR / "data" / "review_decisions.jsonl"
    rows = []
    if path.exists():
        with path.open(encoding="utf-8") as f:
            rows = [json.loads(line) for line in f if line.strip()]
    counts = {}
    for row in rows:
        key = f"{row.get('kind')}:{row.get('decision')}"
        counts[key] = counts.get(key, 0) + 1
    result = {"count": len(rows), "counts": counts}
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"review_decisions: {len(rows)}")
        for key in sorted(counts):
            print(f"- {key}: {counts[key]}")


def review_export(as_json: bool = False):
    """导出人工复核模板"""
    path = SKILL_DIR / "data" / "review_queue.jsonl"
    out_path = SKILL_DIR / "data" / "review_decisions.template.jsonl"
    kind_filter = _cli_option("--kind")
    status_filter = _cli_option("--status")
    limit = int(_cli_option("--limit", 50))
    rows = []
    if path.exists():
        with path.open(encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                if kind_filter and item.get("kind") != kind_filter:
                    continue
                if status_filter and item.get("review_status") != status_filter:
                    continue
                rows.append({
                    "kind": item.get("kind"),
                    "item_id": item.get("item_id"),
                    "name": item.get("name"),
                    "decision": "pending",
                    "source_ref": None,
                    "reviewer_note": item.get("reason"),
                })
                if len(rows) >= limit:
                    break
    with out_path.open("w", encoding="utf-8") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    result = {"output": str(out_path), "count": len(rows)}
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"wrote {out_path}")
        print(f"items: {len(rows)}")


def review_queue_show(as_json: bool = False):
    """查看 P1/P2/P3 复核队列，支持 kind/status/limit 过滤"""
    path = SKILL_DIR / "data" / "review_queue.jsonl"
    items = []
    if path.exists():
        with path.open(encoding="utf-8") as f:
            items = [json.loads(line) for line in f if line.strip()]

    kind_filter = _cli_option("--kind")
    status_filter = _cli_option("--status")
    limit = int(_cli_option("--limit", 20))
    if kind_filter:
        items = [item for item in items if item.get("kind") == kind_filter]
    if status_filter:
        items = [item for item in items if item.get("review_status") == status_filter]

    if as_json:
        print(json.dumps({"count": len(items), "items": items[:limit]}, ensure_ascii=False, indent=2))
        return
    print(f"\n{'='*60}")
    print("🧾 来源复核队列")
    print(f"{'='*60}")
    print(f"总数：{len(items)}")
    if kind_filter or status_filter:
        print(f"过滤：kind={kind_filter or '*'} status={status_filter or '*'} limit={limit}")
    counts = {}
    for item in items:
        key = f"{item.get('kind')}:{item.get('review_status')}"
        counts[key] = counts.get(key, 0) + 1
    for key in sorted(counts):
        print(f"- {key}: {counts[key]}")
    print(f"\n前 {limit} 条：")
    for item in items[:limit]:
        print(f"- {item.get('kind')} {item.get('item_id')} {item.get('name')} [{item.get('review_status')}] {item.get('reason')}")
    print(f"\n{'='*60}")


def fts_search(keyword: str, as_json: bool = False):
    """SQLite FTS/LIKE 检索原始 JSON 来源"""
    searcher = FtsSearch()
    hits = searcher.search(keyword, limit=int(_cli_option("--limit", 10)))
    result = {"available": searcher.available(), "keyword": keyword, "hits": hits}
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"\n{'='*60}")
    print(f"🔎 SQLite 来源检索：{keyword}")
    print(f"{'='*60}")
    print(f"可用：{result['available']}，命中：{len(hits)}")
    for i, hit in enumerate(hits, 1):
        print(f"\n[{i}] {hit.get('source_file')} p.{hit.get('page_num')} mode={hit.get('search_mode')}")
        print(hit.get("quote", "")[:300])
    print(f"\n{'='*60}")


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
  python3 cli.py fts-search <关键词>       SQLite FTS/LIKE 来源检索
  python3 cli.py formula-source <方剂名>   查询方剂来源候选
  python3 cli.py herb-source <药材名>      查询药材来源候选
  python3 cli.py acupoint-source <穴位名>  查询穴位来源候选
  python3 cli.py trace <名称/ID>           统一来源追溯
  python3 cli.py verified-source <名称/ID> 查询 verified 来源
  python3 cli.py review-queue             查看来源复核队列
  python3 cli.py review-next              查看下一批未决复核条目
  python3 cli.py review-export            导出人工复核模板
  python3 cli.py lookup <名称>             P7 统一查询入口
  python3 cli.py explain-trace <名称>      解释来源治理状态
  python3 cli.py review-dashboard          P7 来源治理看板
  python3 cli.py batch-trace <名称列表>    批量来源治理状态
  python3 cli.py help                      显示帮助

示例：
  python3 cli.py diagnose "发热,恶寒,无汗,脉浮紧"
  python3 cli.py formula 桂枝汤
  python3 cli.py herb 麻黄
  python3 cli.py acupoint 合谷
  python3 cli.py case 001
  python3 cli.py source 桂枝汤
  python3 cli.py fts-search 桂枝汤
  python3 cli.py formula-source 桂枝汤
  python3 cli.py herb-source 麻黄
  python3 cli.py acupoint-source 百会
  python3 cli.py trace 桂枝汤
  python3 cli.py verified-source 桂枝汤

# P7 Agent 查询编排（均支持 --json）
python3 cli.py lookup 白头翁汤
python3 cli.py explain-trace 白头翁汤
python3 cli.py review-dashboard
python3 cli.py batch-trace 桂枝汤,白头翁汤,大敦

  python3 cli.py review-queue
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
        "source": lambda: source_search(" ".join(arg for arg in sys.argv[2:] if arg not in ["--json", "--limit"] and not arg.isdigit()), as_json="--json" in sys.argv),
        "fts-search": lambda: fts_search(" ".join(arg for arg in sys.argv[2:] if arg not in ["--json", "--limit"] and not arg.isdigit()), as_json="--json" in sys.argv),
        "sources": lambda: source_manifest(as_json="--json" in sys.argv),
        "formula-source": lambda: formula_source_search(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "herb-source": lambda: herb_source_search(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "acupoint-source": lambda: acupoint_source_search(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "trace": lambda: trace_search(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "verified-source": lambda: verified_source_search(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "review-queue": lambda: review_queue_show(as_json="--json" in sys.argv),
        "review-next": lambda: review_next_show(as_json="--json" in sys.argv),
        "review-export": lambda: review_export(as_json="--json" in sys.argv),
        "review-import": lambda: review_import(as_json="--json" in sys.argv),
        "review-apply": lambda: review_apply(as_json="--json" in sys.argv),
        "review-stats": lambda: review_stats(as_json="--json" in sys.argv),
        "lookup": lambda: lookup_show(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "explain-trace": lambda: explain_trace_show(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
        "review-dashboard": lambda: review_dashboard_show(as_json="--json" in sys.argv),
        "batch-trace": lambda: batch_trace_show(" ".join(arg for arg in sys.argv[2:] if arg != "--json"), as_json="--json" in sys.argv),
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
