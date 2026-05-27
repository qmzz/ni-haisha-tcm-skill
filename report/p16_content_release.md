# P16 内容质量定版报告

## 定版结论

- P13-P16 已完成知识条目正文质量主线收口。
- 条目正文与 frontmatter 中的占位词已清零。
- P9 quality audit 已清零。
- 仍未补 `归经` 等字段的条目，原因是现有来源未明确提供，不做无依据扩写。
- 本版本可作为内容质量定版基线。

## 核心指标

- total: 939
- trace_status: `{'verified': 803, 'no_source_found': 133, 'candidate': 3}`
- P9 issues: 0 `{}`
- P11 queue: 216 `{'no_source_boundary_or_external_source': 133, 'review_candidate_source_refs': 3, 'fill_verified_missing_content_field': 80}`
- placeholder_files: 0
- json_fragment_files: 0

## 按类型分布

- acupoint: `{'verified': 396, 'no_source_found': 15}`
- formula: `{'verified': 113}`
- herb: `{'no_source_found': 118, 'verified': 294, 'candidate': 3}`

## P16 处理内容

- `scripts/p16_format_short_herb_quotes.py`：将 41 个短正文 herb 中的长来源摘录按句读重排，提升可读性。
- `scripts/p16_expand_short_herb_source_windows.py`：对剩余 19 个短正文从原始 JSON 中按中文名截取更宽来源窗口，作为 `P16 扩展摘录`，不转写为无依据结构字段。
- 最终 `body_short` 从 41 -> 19 -> 0。

## 定版边界

- `verified` 仅表示可追溯来源链路通过，不代表医学真实性、临床适用性或治疗建议。
- `candidate` 剩余 3 条：白豆蔻、白扁豆、番泻叶，因仅低质量 alias 命中，保持复核状态。
- `no_source_found` 133 条保持来源范围边界，不引入外部资料硬补。
- 药材 `归经` 等未明确出现在现有来源中的字段，不凭模型记忆补写。
- 穴位条目继续保持“仅作学习与来源追溯，不作为针灸操作指导”。

## 验证链

- `check_frontmatter_schema.py`: missing_required=0, warnings=0
- `build_p8_knowledge_audit.py`: stale_verified_frontmatter=0
- `p9_quality_audit.py`: issues=0
- `p9_build_review_queue.py`: 0 entries
- `python3 -m unittest discover -s tests -p test_*.py`: 84 tests OK
