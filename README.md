# 倪海厦中医 Skill（ni-haisha-tcm-skill）

这是给 Agent 调用的中医资料检索 Skill，不是面向人工维护流水线的脚本仓库。

核心用途：基于已整理的倪海厦人纪系列知识库，给 Agent 提供结构化 JSON 工具，用于资料查询、来源追溯、学习参考和安全边界提示。

> ⚠️ 医学安全边界：本 Skill 仅用于中医理论学习、资料检索和来源追溯，不能替代合格医师面诊、诊断、处方、用药或针灸操作。穴位内容仅作学习与来源追溯，不作为针灸操作指导。

---

## Agent 首选入口

Agent 调用时优先使用：

```bash
python3 tools/tcm_tools.py <tool_name> '<json_payload>'
```

所有工具输出均为 JSON。

### 常用工具

```bash
# 安全检查：高风险症状会阻止继续给方剂参考
python3 tools/tcm_tools.py tcm_safety_check '{"text":"胸痛,呼吸困难"}'

# 统一查询：自动带来源状态、正文摘录和安全边界
python3 tools/tcm_tools.py tcm_lookup '{"query":"桂枝汤"}'

# 来源追溯：查看 verified / candidate / no_source_found 等状态
python3 tools/tcm_tools.py tcm_trace '{"query":"桂枝汤"}'

# 解释来源治理状态
python3 tools/tcm_tools.py tcm_explain_trace '{"query":"白豆蔻"}'

# 方剂 / 药材 / 穴位查询
python3 tools/tcm_tools.py tcm_formula_query '{"name":"桂枝汤"}'
python3 tools/tcm_tools.py tcm_herb_query '{"name":"麻黄"}'
python3 tools/tcm_tools.py tcm_acupoint_query '{"name":"百会"}'

# 辨证辅助：必须只作学习参考
python3 tools/tcm_tools.py tcm_diagnose_assist '{"symptoms":["发热","恶寒","无汗","脉浮紧"]}'

# 原始来源检索
python3 tools/tcm_tools.py tcm_source_search '{"keyword":"桂枝汤","limit":5}'
python3 tools/tcm_tools.py tcm_search_sources_fts '{"query":"桂枝汤","limit":5}'
```

未知工具名会返回 `available_tools`，可用来发现完整工具列表：

```bash
python3 tools/tcm_tools.py help '{}'
```

---

## Agent 调用原则

1. **先安全检查，再医学参考**  
   用户描述包含胸痛、呼吸困难、昏迷、大出血等高风险信号时，应优先提示及时就医，不继续给方剂建议。

2. **优先 `tcm_lookup` / `tcm_trace`**  
   普通查询不要直接读 Markdown 拼答案，先用 JSON 工具拿到来源状态和边界说明。

3. **不要把 trace 当医学背书**  
   `verified` 只表示来源追溯链路通过，不代表医学真实性、临床适用性或操作建议。

4. **不要凭模型记忆补医学内容**  
   如当前知识库或来源摘录没有明确写出，就不要补写剂量、归经、禁忌、针刺方法等医学细节。

5. **`candidate` 需要人工复核**  
   candidate 命中只说明可能相关，不应当作 verified 使用。

6. **`no_source_found` 保持边界**  
   当前倪海厦来源范围内未找到依据，不要硬补；如需扩展，必须引入新的可追溯来源。

---

## 知识库当前状态

当前基线：`v1.0.0-rc1`

```text
total: 939
verified: 803
no_source_found: 133
candidate: 3
P9 issues: 0
placeholder files: 0
JSON fragment files: 0
frontmatter warnings: 0
```

P16 内容质量定版已完成：

- 正文占位词已清零；
- JSON / patch 残片已清零；
- 短正文已通过来源摘录重排和原始 JSON 窗口扩展处理；
- 空壳章节已删除；
- 未明确来源的 `归经` 等字段未硬补。

详细报告见：

```text
report/p16_content_release.md
```

---

## 目录说明

```text
SKILL.md              # Skill 元信息与 Agent 使用说明
README.md             # 本文件：面向 Agent 的简洁入口说明
tools/tcm_tools.py    # Agent JSON 工具主入口
internal/             # 查询、诊断、安全、来源追溯内部模块
knowledge/            # 方剂、药材、穴位、概念、医案 Markdown 知识库
data/                 # 索引、来源、alias、治理状态数据
report/               # 治理与定版报告
```

`tools/tcm_tools.py` 是 Agent 调用主入口。

---

## 维护说明

本仓库曾包含大量 P0-P16 阶段性治理脚本和测试脚本。RC 定版后已清理，不再作为 Skill 运行路径的一部分，避免干扰 Agent 使用。

如未来维护知识库，建议新建独立维护分支或维护目录；不要把一次性治理命令堆进 README。

---

## License

MIT License
