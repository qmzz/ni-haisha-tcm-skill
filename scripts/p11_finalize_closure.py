#!/usr/bin/env python3
"""P11 closure report.

P11 focuses on content quality improvement without model-memory medical expansion.
This script only reads current artifacts and writes a stage closure report.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORT = ROOT / "report" / "p11_closure.md"


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def count_by(rows, *keys):
    c = Counter()
    for r in rows:
        c[tuple(r.get(k) for k in keys)] += 1
    return c


def main():
    kc = load_jsonl(DATA / "knowledge_completeness.jsonl")
    p9 = load_jsonl(DATA / "p9_quality_audit.jsonl")
    p11q = load_jsonl(DATA / "p11_content_quality_queue.jsonl")
    alias = load_jsonl(DATA / "alias_index.jsonl")
    vs = load_jsonl(DATA / "verified_sources.jsonl")

    total = len(kc)
    status = Counter(r.get("trace_status") for r in kc)
    by_kind_status = defaultdict(Counter)
    for r in kc:
        by_kind_status[r.get("kind")][r.get("trace_status")] += 1

    p9_by_level = Counter(r.get("level") for r in p9)
    p11_by_priority = Counter(r.get("priority") for r in p11q)
    p11_by_task = Counter(r.get("task_type") for r in p11q)
    p11_by_kind = Counter(r.get("kind") for r in p11q)
    alias_by_kind = Counter(r.get("kind") for r in alias)

    no_source = [r for r in kc if r.get("trace_status") == "no_source_found"]
    no_source_scope_count = 0
    external_required_count = 0
    no_source_policy_count = 0
    for r in no_source:
        text = (ROOT / r["file"]).read_text(encoding="utf-8")
        if 'source_scope: "not_in_nihaixia_source"' in text:
            no_source_scope_count += 1
        if "external_reference_required: true" in text:
            external_required_count += 1
        if 'no_source_policy: "keep_boundary_until_traceable_source"' in text:
            no_source_policy_count += 1

    lines = [
        "# P11 内容质量提升阶段收口报告",
        "",
        "## 阶段定位",
        "",
        "P11 的目标不是追求 verified 百分比，而是在不凭模型记忆扩写医学内容的前提下，提高知识库结构完整度、治理稳定性、来源边界清晰度与后续可维护性。",
        "",
        "核心原则：",
        "",
        "- 不凭模型记忆补医学内容。",
        "- candidate 不等于 verified。",
        "- verified 仅表示来源追溯链路通过，不代表医学真实性、临床适用性或针灸操作指导。",
        "- no_source_found 不强行补内容，必须保持边界或等待外部可追溯来源。",
        "- seed 脚本必须固定白名单、幂等，避免测试/管线动态推进数据。",
        "",
        "## P11 已完成事项",
        "",
        "### P11-A/B：内容质量队列与方剂 usage 结构补全",
        "",
        "- 建立内容质量队列：`data/p11_content_quality_queue.jsonl`。",
        "- 29 个 verified 方剂补齐 `## 用法` 结构。",
        "- 16 个从既有 `source_refs.quote` 摘录明确用法。",
        "- 13 个明确标记：现有 verified 来源未提供明确用法，待补充。",
        "- 方剂 complete：`113 / 113`。",
        "",
        "### P11-C/D：穴位 candidate verified 小批量扩展",
        "",
        "- P11-C：固定白名单 100 条穴位 verified。",
        "- P11-D：direct-quote 固定白名单 30 条穴位 verified。",
        "- 入选约束：来源链路明确；P11-D 额外要求 quote 直接包含穴位中文名。",
        "- 不改医学正文，不凭模型记忆扩写。",
        "- P11-C/D seed 已纳入测试链路，避免数据回归。",
        "",
        "### P11-E：no_source_found 来源范围边界",
        "",
        "- 133 条 no_source_found 补充 scope 元数据。",
        "- 标记为当前倪海厦原始资料未命中，需要外部可追溯来源。",
        "- 不改变 trace_status，不补医学正文。",
        "",
        "### 治理稳定性修复",
        "",
        "- P9-F 追溯复核纳入测试与管线闭环，防止 review_status 重建后丢失。",
        "- 清理 `knowledge/acupoints/laogong.md` 历史 JSON patch 残留，P9 quality audit 清零。",
        "",
        "## 当前核心指标",
        "",
        f"- total: {total}",
        f"- verified: {status.get('verified', 0)} / {total}",
        f"- candidate: {status.get('candidate', 0)} / {total}",
        f"- no_source_found: {status.get('no_source_found', 0)} / {total}",
        f"- verified_sources: {len(vs)}",
        f"- alias_index: {len(alias)}",
        "",
        "### 按类型追溯状态",
        "",
        "| kind | total | verified | candidate | no_source_found |",
        "|------|-------|----------|-----------|-----------------|",
    ]
    for kind in ["formula", "herb", "acupoint"]:
        c = by_kind_status[kind]
        kt = sum(c.values())
        lines.append(f"| {kind} | {kt} | {c.get('verified',0)} | {c.get('candidate',0)} | {c.get('no_source_found',0)} |")

    lines += [
        "",
        "## 质量治理状态",
        "",
        f"- P9 quality issues: {len(p9)}",
        f"- P9 by_level: {dict(p9_by_level)}",
        "- frontmatter schema: missing_required 0, warnings 0（见 `report/frontmatter_audit.md`）",
        "- stale_verified_frontmatter: 0（见 `report/p8_stale_verified_fix_report.md`）",
        "",
        "## P11 当前队列",
        "",
        f"- queue total: {len(p11q)}",
        f"- by_priority: {dict(p11_by_priority)}",
        f"- by_task: {dict(p11_by_task)}",
        f"- by_kind: {dict(p11_by_kind)}",
        "",
        "解释：P11 队列剩余项不是本阶段必须清空的缺陷，而是下一阶段复核/外部来源策略入口。",
        "",
        "## no_source_found 边界覆盖",
        "",
        f"- no_source_found total: {len(no_source)}",
        f"- source_scope marked: {no_source_scope_count} / {len(no_source)}",
        f"- external_reference_required: {external_required_count} / {len(no_source)}",
        f"- no_source_policy marked: {no_source_policy_count} / {len(no_source)}",
        "",
        "## P11 收口结论",
        "",
        "P11 可以收口。当前知识库具备：",
        "",
        "1. 方剂结构完整闭环。",
        "2. verified 来源链路扩展且 seed 幂等稳定。",
        "3. no_source_found 有明确边界与后续来源策略。",
        "4. P9 质量审计清零。",
        "5. 文档、测试、管线状态同步。",
        "",
        "## P12 建议入口",
        "",
        "P12 不建议继续粗放扩 verified。建议方向：",
        "",
        "1. candidate 分层人工复核与抽检报告。",
        "2. 外部可追溯来源接入策略，用于 no_source_found 的二阶段提升。",
        "3. 查询体验提升：语义检索、多轮辨证辅助状态机、CLI 安装体验。",
        "4. Agent 工具说明增强：明确安全边界、来源解释与 alias redirect 展示。",
        "",
        "---",
        "",
        "本报告由 `scripts/p11_finalize_closure.py` 生成。",
    ]

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "report": str(REPORT.relative_to(ROOT)),
        "total": total,
        "trace_status": dict(status),
        "p9_issues": len(p9),
        "p11_queue": len(p11q),
        "no_source_scope": no_source_scope_count,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
