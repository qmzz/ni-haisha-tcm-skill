---
name: ni
description: "倪海厦中医资料检索 Skill：面向 Agent 的方剂、药材、穴位、辨证辅助与来源追溯 JSON 工具"
argument-hint: "<tool_name> <json_payload>"
version: "1.0.0-rc2-p18"
user-invocable: true
allowed-tools: Read, Bash
---

# 倪海厦中医 Skill

本 Skill 面向 Agent 调用，用于中医理论学习、资料检索和来源追溯。

> ⚠️ 安全边界：不能替代合格医师面诊、诊断、处方、用药或针灸操作。穴位内容仅作学习与来源追溯，不作为针灸操作指导。

## 首选调用方式

```bash
python3 tools/tcm_tools.py <tool_name> '<json_payload>'
```

所有输出均为 JSON。

## 常用工具

```bash
# 安全检查
python3 tools/tcm_tools.py tcm_safety_check '{"text":"胸痛,呼吸困难"}'

# 统一查询：优先使用
python3 tools/tcm_tools.py tcm_lookup '{"query":"桂枝汤"}'

# 来源追溯
python3 tools/tcm_tools.py tcm_trace '{"query":"桂枝汤"}'
python3 tools/tcm_tools.py tcm_explain_trace '{"query":"白豆蔻"}'

# 方剂 / 药材 / 穴位
python3 tools/tcm_tools.py tcm_formula_query '{"name":"桂枝汤"}'
python3 tools/tcm_tools.py tcm_herb_query '{"name":"麻黄"}'
python3 tools/tcm_tools.py tcm_acupoint_query '{"name":"百会"}'

# 辨证辅助：仅作学习参考
python3 tools/tcm_tools.py tcm_diagnose_assist '{"symptoms":["发热","恶寒","无汗","脉浮紧"]}'

# 来源检索
python3 tools/tcm_tools.py tcm_source_search '{"keyword":"桂枝汤","limit":5}'
python3 tools/tcm_tools.py tcm_search_sources_fts '{"query":"桂枝汤","limit":5}'
```

未知工具名会返回 `available_tools`。

## Agent 必须遵守

1. 先做安全判断；遇到高风险症状，提示及时就医，不继续给方剂建议。
2. 普通查询优先用 `tcm_lookup` 或 `tcm_trace`，不要直接拼 Markdown。
3. `verified` 只代表来源追溯链路通过，不代表医学真实性或临床适用性。
4. `candidate` 不可当作 verified 使用。
5. `no_source_found` 不要硬补；如需扩展，必须引入新的可追溯来源。
6. 不凭模型记忆补剂量、归经、禁忌、针刺方法等医学内容。

## 当前数据基线

```text
version: v1.0.0-rc2-p18
indexed medical items: 939
knowledge markdown files: 1083
knowledge_completeness trace_status: verified 803 / no_source_found 133 / candidate 3
verified_sources registry rows: 778
status: P17/P18 精修进行中，非最终稳定版
```

注意：P16 曾作为内容质量基线，但 P17 审计发现仍有内容治理问题。P18 只做机械清理，不凭模型记忆补写医学内容。

相关报告：`report/p16_content_release.md`、`report/p17_content_audit.md`

## 目录

```text
tools/tcm_tools.py    # Agent JSON 工具主入口
internal/             # 查询、诊断、安全、来源追溯模块
knowledge/            # Markdown 知识库
data/                 # 索引和治理状态数据
report/               # 治理与定版报告
```
