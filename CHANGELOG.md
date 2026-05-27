# 更新日志

所有对本项目的重大更改都将记录在此文件中。

## [Unreleased]

### Skill 包瘦身与入口收敛

- 移除历史 CLI、测试脚本和 P0-P16 阶段性治理脚本，避免把维护流水线误当作 Agent 调用入口。
- 重写 `README.md` 与 `SKILL.md`：只保留 `tools/tcm_tools.py` JSON 工具入口、调用原则、安全边界和当前数据基线。
- 清理历史文档与报告中的可执行命令痕迹；历史阶段记录保留结论，不再展示旧维护命令。

### P16 内容质量定版收口

- 对 P15 后剩余 41 个 `body_short` 药材条目进行最终正文整理：
  - 41 个短正文中的长 `来源摘录` 按句读重排，短正文降至 19。
  - 对剩余 19 个短正文，从原始 JSON 中围绕条目中文名截取更宽来源窗口，作为 `P16 扩展摘录`，不转写成无依据结构字段。
  - 最终 `P9 quality issues: 0`，`p9_review_queue: 0`。
- 新增 `report/p16_content_release.md`，作为正文质量定版报告。
- 定版边界：`归经` 等未在当前来源明确出现的字段不凭模型记忆补写；3 条低质量 alias candidate 保持复核状态；133 条 no_source_found 保持来源范围边界。
- 测试：`84 passed`。

### P13-P15 正文质量主线

- P13：清理知识正文/frontmatter 占位词，`待考/待补充/暂无/待完善/TODO/待查/待定/待确认/未提供明确/现有 verified 来源未提供` 命中清零；清理 JSON patch/quote 残片。
- P14：仅从现有 `source_refs.quote` 抽取明确 `性味/主治/用量/禁忌` 等来源摘录补强药材正文，不硬补 `归经`。
- P15：删除 80 个 herb 无内容空壳小节，frontmatter 有明确字段时同步正文；不恢复无依据结构。

### P12 candidate 批量收口

- 对剩余 164 条 candidate 做一次性来源检索与分流：
  - 161 条在原始 JSON 中找到中文名命中，提取 source_refs 并纳入 verified。
  - 3 条 herb（白豆蔻、白扁豆、番泻叶）仅有低质量 alias 命中，保留 candidate/needs_review，不强行 verified。
- 当前指标：
  - `verified: 803 / 939`
  - `candidate: 3 / 939`
  - `no_source_found: 133 / 939`
  - `P9 quality issues: 0`
  - 测试：`84 passed`

### P11 内容质量与治理闭环

- P11-A/B：内容质量队列与方剂 usage 结构补全；方剂 complete: `113 / 113`。
- P11-C/D：穴位 candidate verified 小批量扩展；verified 总数：`512 -> 642`；穴位 verified：`107 -> 237`。
- P11-E：为 133 条 no_source_found 补充来源范围边界，不改变 trace_status，不补医学正文。
- 治理稳定性：追溯复核纳入测试与管线闭环；清理历史 JSON patch 残留，P9 quality audit issues 清零。

### P10 查询质量与可用性增强

- alias 查询闭环：`TraceService.trace()` 支持 alias redirect，Agent 可展示标准条目跳转说明。
- safety_boundary 全覆盖：`safety_boundary: 939 / 939`，`acupoint source_trace_notice: 411 / 411`。
- no_source_found 残余治理：133 条 no_source_found 在当前倪海厦原始 JSON 中无明确命中，保持 no_source_found，不凭模型记忆补内容。

### P9 数据质量治理

- 建立数据质量审计，从内容一致性、完整性、准确性等维度检查。
- 解决 verified registry 与 frontmatter 不一致、空 file、空 title、duplicate_title、低分 verified 复核等问题。
- 最终 error/warning/review 清零。

### P8 来源追溯扩展

- 方剂 verified 全覆盖。
- 药材和穴位 verified 扩展。
- no_source_found 扩展治理：仅对来源链路足够明确的条目升级 verified；其余保持边界。

### P0-P7 基础建设

- 建立知识库、来源索引、review 队列、alias 治理、frontmatter 规范、安全边界和 Agent JSON 工具入口。
- 明确：`verified` 仅代表来源追溯链路通过，不代表医学真实性、临床适用性或操作建议。

## [1.0.0] - 2026-05-26

### 初始完整版本

- 完成核心知识库整理：方剂、药材、穴位、概念、医案。
- 完成基础检索、来源追溯、安全声明和 Agent 工具雏形。
- 许可证：MIT。
