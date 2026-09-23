# CHANGELOG

## [3.0.0] - 2026-09-23

### 🚀 重大重构与突破 (Major Refactor)
- **知识库 100% 纯正全量重构**：
  - 基于《人纪》与汉唐原文，完成全量 1,077 篇核心文档重构（经方 113 首、本草 415 味、针灸 411 穴、气化概念 43 篇、辨证诊断 44 篇、实战医案 51 例）。
  - 全量销毁历史遗留的 `<!-- P5_STANDARD_NOTICE_START -->`、`review_status` 等机械八股与免责套话。
  - 标准化四大/五大二级标题 emoji 板块，纯正还原倪海厦水火气化物理模型。
- **全新检索引擎与工具体系**：
  - 重构 `internal/knowledge_query.py` 与 `tools/tcm_tools.py`，支持全库毫秒级多维度语义/关键词检索与精确文献调取。
  - 更新 `SKILL.md` 规范交互状态机与输出标准。
- **工程瘦身与深度清理**：
  - 清理历史 `p18~p56` 补丁脚本、临时 JSONL、构建目录及失效的旧规范文档。
  - 同步部署至 OpenClaw skills 工作区（`~/.openclaw/workspace/skills/ni-haisha/`）。
