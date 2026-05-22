# Agent Integration

本项目提供 `tools/tcm_tools.py` 作为 OpenClaw / QwenPaw / 其他 Agent 的 JSON 工具入口。

## 调用格式

```bash
python3 tools/tcm_tools.py <tool_name> '<json_payload>'
```

所有输出均为 JSON。

## 常用工具

```bash
python3 tools/tcm_tools.py tcm_safety_check '{"text":"胸痛,呼吸困难"}'
python3 tools/tcm_tools.py tcm_trace '{"query":"桂枝汤"}'
python3 tools/tcm_tools.py tcm_search_sources_fts '{"query":"桂枝汤","limit":5}'
python3 tools/tcm_tools.py tcm_review_next '{"kind":"herb","status":"needs_review","limit":5}'
python3 tools/tcm_tools.py tcm_review_stats '{}'
python3 tools/tcm_tools.py tcm_quality_report '{}'
python3 tools/tcm_tools.py tcm_compare_formulas '{"names":["桂枝汤","麻黄汤"]}'
python3 tools/tcm_tools.py tcm_compare_herbs '{"names":["麻黄","桂枝"]}'
python3 tools/tcm_tools.py tcm_trace_summary '{"query":"大柴胡汤"}'
python3 tools/tcm_tools.py tcm_verified_stats '{}'
python3 tools/tcm_tools.py tcm_no_source_report '{}'
python3 tools/tcm_tools.py tcm_lookup '{"query":"白头翁汤"}'
python3 tools/tcm_tools.py tcm_explain_trace '{"query":"白头翁汤"}'
python3 tools/tcm_tools.py tcm_review_dashboard '{}'
python3 tools/tcm_tools.py tcm_batch_trace '{"queries":["桂枝汤","白头翁汤"]}'
```

## P6 增强说明

- `tcm_trace_summary`：适合 Agent 回复前快速取得压缩来源摘要。
- `tcm_verified_stats`：查看 verified 覆盖总量与类别分布。
- `tcm_no_source_report`：查看 no_source_found 专项治理报告。
- `tcm_lookup`：统一查询入口，返回 markdown 预览、trace 摘要与安全边界。
- `tcm_explain_trace`：解释 verified / candidate / needs_review / no_source_found 等治理状态。
- `tcm_review_dashboard`：汇总 verified、review_queue、frontmatter audit 与报告入口。
- `tcm_batch_trace`：批量查询多个条目的来源治理状态。

> verified 仅表示来源已纳入复核链路，不代表医学真实性或临床适用性结论。

## 安全边界

- 医学相关输出必须包含免责声明或来源状态。
- 高风险症状由 `tcm_safety_check` 识别后，应停止方剂参考。
- `candidate` 不是 `verified`。
- Agent 不应把本工具输出包装成诊断或治疗建议。
