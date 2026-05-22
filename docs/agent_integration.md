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
```

## 安全边界

- 医学相关输出必须包含免责声明或来源状态。
- 高风险症状由 `tcm_safety_check` 识别后，应停止方剂参考。
- `candidate` 不是 `verified`。
- Agent 不应把本工具输出包装成诊断或治疗建议。
