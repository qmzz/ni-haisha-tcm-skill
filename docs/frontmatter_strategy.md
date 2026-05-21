# P1 Frontmatter 回写策略

本文件定义 `ni-haisha-tcm-skill` P1 阶段把来源索引回写到知识 Markdown 的策略。

## 原则

1. **不直接批量覆盖正文**：来源候选先进入 `data/*_sources.jsonl` 与 `data/*_index.jsonl`，不自动改正文内容。
2. **候选不等于确认**：`trace_status: candidate` 只表示检索到可能相关片段，需要人工或规则复核。
3. **只回写最小元数据**：不把大段原文塞进 frontmatter，避免 Markdown 膨胀与误导。
4. **医学安全优先**：方剂剂量、针灸操作、禁忌等高风险内容，不因索引命中就自动补全。

## 建议 frontmatter 字段

### 方剂 / 药材 / 穴位通用

```yaml
trace_status: candidate        # candidate / verified / no_source_found / needs_review
source_refs:
  - source_file: "04【视频同步文稿】人-伤寒论（可打印）.json"
    page_num: 11
    quote: "桂枝汤主之。现在进入伤寒论第一个方，桂枝汤。"
```

## 状态说明

| 状态 | 含义 | 是否可用于知识补全 |
|------|------|--------------------|
| `candidate` | 检索命中候选片段，尚未人工复核 | 否，只可提示来源候选 |
| `verified` | 已人工核对来源与条目一致 | 可用于补全，但仍需注明来源 |
| `no_source_found` | 原始 JSON 未检索到可靠来源 | 不补全，标记待考 |
| `needs_review` | 命中片段存在同名/歧义/上下文不足 | 不补全，需复核 |

## 回写流程

1. 运行索引脚本：

```bash
python3 scripts/build_formula_sources.py
python3 scripts/build_formula_index.py
python3 scripts/build_herb_sources.py
python3 scripts/build_herb_index.py
python3 scripts/build_acupoint_sources.py
python3 scripts/build_acupoint_index.py
```

2. 抽样核对高频条目：

```bash
python3 cli.py formula-source 桂枝汤
```

3. 先对少量确定条目试点回写，例如：

```text
knowledge/formulas/guizhi_tang.md
knowledge/formulas/mahuang_tang.md
knowledge/herbs/mahuang.md
knowledge/acupoints/baihui.md
```

4. 回写后运行测试：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## 禁止事项

- 禁止根据模型记忆补写中医内容。
- 禁止把 `candidate` 直接当成医学事实。
- 禁止自动生成剂量建议或针灸操作建议。
- 禁止对全部 800+ Markdown 文件无复核批量回写。

## 后续可做

- 增加 `scripts/apply_verified_refs.py`，只回写人工确认的 `verified` 条目。
- 增加 `data/review_queue.jsonl`，专门记录歧义项与未命中项。
- 为 CLI 增加 `source-review` 命令，辅助人工审核候选片段。
