# Source Quality Levels

本文件定义来源追溯状态与质量等级。它只描述“资料链路可信度”，不判断医学真实性、临床适用性或治疗建议。

## Trace Status

| 状态 | 含义 | Agent 输出规则 |
|---|---|---|
| `verified` | 已进入 `verified_sources.jsonl`，且有人工/脚本治理记录与可追溯 source_refs | 可引用来源摘录，但必须保留学习参考与安全边界 |
| `candidate` | 有候选 source_refs，但存在 alias、上下文、质量分或人工复核不足问题 | 只能说“候选来源显示/可能相关”，不能当作已验证结论 |
| `needs_review` | 已进入复核队列，相关性或条目归属仍需人工确认 | 不输出确定医学结论；优先提示需复核 |
| `no_source_found` | 当前倪海厦来源范围内未找到可用来源 | 不硬补；不要凭模型记忆补剂量、归经、禁忌、针刺方法等 |
| `source_search` | 治理索引未命中，仅从原始语料关键词检索到片段 | 只能作为检索线索，不作为条目来源状态 |

## Verified Sub-levels

`verified` 不是医学背书。为了降低误用，建议在后续治理中将 verified 分为：

| 建议等级 | 判定标准 | 示例 |
|---|---|---|
| `verified_direct` | 来源片段以条目名为主题，包含专门讲解/本经原文/方剂组成/穴位定位等 | “桂枝汤”条目命中桂枝汤专节 |
| `verified_contextual` | 来源片段明确提到条目名，但主题可能是相关病案、其他方剂或上下文说明 | “板蓝根”在温病派误治上下文中被提及 |
| `verified_alias` | 通过别名/父级名/异名命中，经人工确认归属 | 川贝母 → 贝母，需说明 alias 关系 |
| `candidate_alias` | alias 命中但未人工确认 | 白豆蔻等低质量 alias 命中 |

当前仓库尚未全面落地 `verified_direct/contextual/alias` 字段；Agent 应默认保守处理所有 verified：只说明“来源追溯已登记”，不要自动升级为医学有效性结论。

## Registry Consistency Rules

1. `knowledge_completeness.trace_status=verified` 的条目必须存在于 `data/verified_sources.jsonl`。
2. `data/*_index.jsonl` 中 `trace_status=verified` 的行必须有非空 `source_refs`。
3. `trace_status=no_source_found` 的行不得携带 `source_refs`。
4. `candidate` 必须有候选 `source_refs`；无 source_refs 的候选应降级为 `no_source_found`。
5. Markdown frontmatter、index jsonl、verified registry 三者冲突时，优先采用更保守状态，除非有明确 source_refs 与复核记录。

## Agent Response Guidance

- 用户问资料：优先调用 `tcm_lookup` 或 `tcm_trace`。
- 用户问辨证：先 `tcm_safety_check`，再 `tcm_diagnose_assist`。
- 遇到 `candidate/no_source_found/source_search`：明确说明来源状态，不补写医学细节。
- 涉及急症、孕婴、用药、针灸操作：提示专业医师评估，不给操作指令。
