# P6-A Verified 条目标准化报告

## 范围

- 阶段：P6-A
- 目标：将 P5-D 样板标准化扩展到全部 verified 条目
- 覆盖 verified 条目：72
  - 方剂：25
  - 药材：22
  - 穴位：25

## 标准化内容

每个 verified 条目统一补齐或更新：

- `title`
- `kind`
- `review_status: verified`
- `reviewer: "p6_verified_standardization"`
- `safety_disclaimer_required: true`
- `content_scope`
- 安全边界正文块：`P5_STANDARD_NOTICE_START` / `P5_STANDARD_NOTICE_END`

> 注：P6-A 复用 P5 标记块名称，仅用于保持兼容；本阶段不自动改写医学正文内容。

## 审计结果

当前 frontmatter 审计：

```text
files: 939
missing_required: 867
warnings: 0
```

相较 P5-D 样板阶段：

```text
missing_required: 929 -> 867
```

## 测试

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

结果：

```text
Ran 57 tests
OK
```

## 安全边界

- 所有条目仍仅用于中医学习、资料检索与来源追溯。
- 不构成诊断、处方、用药、针灸操作或治疗建议。
- 穴位内容仅作学习与来源追溯，不作为针灸操作指导。
