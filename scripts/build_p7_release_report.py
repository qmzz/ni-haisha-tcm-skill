#!/usr/bin/env python3
"""Build P7 release report for ni-haisha-tcm-skill."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    verified = load_jsonl(ROOT / "data" / "verified_sources.jsonl")
    review_queue = load_jsonl(ROOT / "data" / "review_queue.jsonl")
    no_source = load_jsonl(ROOT / "data" / "no_source_classification.jsonl")
    alias_review = load_jsonl(ROOT / "data" / "alias_review.jsonl")
    audit_head = (ROOT / "report" / "frontmatter_audit.md").read_text(encoding="utf-8").splitlines()[:12]

    verified_by_kind = Counter(row.get("kind") for row in verified)
    queue_by_status = Counter(row.get("review_status") for row in review_queue)
    alias_by_decision = Counter(row.get("decision") for row in alias_review)
    no_source_by_class = Counter(row.get("category") for row in no_source)

    content = f"""# P7 发布收口报告\n\n## 阶段定位\n\nP7 聚焦知识治理深水区与可用性产品化：在不凭模型记忆扩写医学内容的前提下，继续推进来源治理、alias 复核、第三批 verified 精修，并把 Agent 查询编排能力产品化到 CLI / 文档。\n\n## P7 完成项\n\n- [x] P7-A：no_source_found 分类治理，生成 `data/no_source_classification.jsonl` 与 `report/p7_no_source_classification.md`。\n- [x] P7-B：alias / synonym 治理增强，生成 `data/alias_review.jsonl` 与 `report/p7_alias_review.md`，safe_alias 可控应用。\n- [x] P7-C：第三批 verified 精修，新增 30 个 verified。\n- [x] P7-D：Agent 查询编排增强，新增 lookup、trace 解释、review dashboard、batch trace。\n- [x] P7-E：CLI / 文档产品化，CLI 对齐 P7-D 查询编排能力。\n- [x] P7-F：版本发布准备，补充 changelog、release notes 与阶段收口报告。\n\n## 当前累计指标\n\n### verified sources\n\n- 总数：{len(verified)}\n- 方剂：{verified_by_kind.get('formula', 0)}\n- 药材：{verified_by_kind.get('herb', 0)}\n- 穴位：{verified_by_kind.get('acupoint', 0)}\n\n> verified 仅表示来源追溯链路已复核通过，不代表医学真实性或临床适用性。\n\n### review queue\n\n- 总数：{len(review_queue)}\n"""
    for key in sorted(queue_by_status):
        content += f"- {key}: {queue_by_status[key]}\n"

    content += "\n### no_source_found 分类\n\n"
    for key in sorted(no_source_by_class):
        content += f"- {key}: {no_source_by_class[key]}\n"

    content += "\n### alias review\n\n"
    for key in sorted(alias_by_decision):
        content += f"- {key}: {alias_by_decision[key]}\n"

    content += "\n### frontmatter audit 摘要\n\n```text\n" + "\n".join(audit_head) + "\n```\n\n"

    content += """## P7 新增 CLI / Agent 入口\n\n### CLI\n\n```bash\npython3 cli.py lookup 白头翁汤\npython3 cli.py explain-trace 白头翁汤\npython3 cli.py review-dashboard\npython3 cli.py batch-trace 桂枝汤,白头翁汤,大敦\n```\n\n以上命令均支持 `--json`，便于 Agent 或外部系统消费。\n\n### Agent JSON tools\n\n```bash\npython3 tools/tcm_tools.py tcm_lookup '{"query":"白头翁汤"}'\npython3 tools/tcm_tools.py tcm_explain_trace '{"query":"白头翁汤"}'\npython3 tools/tcm_tools.py tcm_review_dashboard '{}'\npython3 tools/tcm_tools.py tcm_batch_trace '{"queries":["桂枝汤","白头翁汤"]}'\n```\n\n## 安全与治理边界\n\n- 不凭模型记忆补医学内容。\n- 所有医学知识补全必须来自原始 JSON、既有知识文件或明确可追溯来源。\n- 找不到依据只能标记 `待考`、`待补充`、`no_source_found` 或 `needs_review`。\n- `candidate` 不等于 `verified`。\n- `alias hit` 只能进入 candidate / needs_review，不自动 verified。\n- `quality_score` 只用于治理排序和复核优先级，不等于医学真实性判定。\n- 穴位内容仅作学习与来源追溯，不作为针灸操作指导。\n\n## 建议后续\n\n- P8 可继续围绕人工复核效率、CLI 打包、语义检索和 release tag 展开。\n- 对 `no_source_found` 的 herb/acupoint 条目继续坚持小批量、可追溯、人工白名单推进。\n"""

    out = ROOT / "report" / "p7_release_report.md"
    out.write_text(content, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
