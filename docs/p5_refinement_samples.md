# P5-D 精修样板条目

P5-D 首批只标准化 10 个样板条目，避免一次性全量改写知识库正文。

## 方剂样板

- 桂枝汤
- 麻黄汤
- 小柴胡汤
- 五苓散
- 半夏泻心汤

## 药材样板

- 麻黄
- 桂枝
- 甘草
- 附子
- 半夏

## 标准化内容

frontmatter 增加：

```yaml
kind: "formula|herb"
review_status: verified
reviewer: "p5_sample_standardization"
safety_disclaimer_required: true
content_scope: "学习参考与资料检索，不作为诊断、处方或治疗建议"
```

正文插入：

```text
学习与安全边界
来源追溯状态
```

## 原则

- 不自动改写医学正文。
- 不新增未溯源的医学结论。
- 样板条目只统一治理元数据、安全边界和来源追溯提示。
- 后续扩展必须先复用样板，再小批量执行。
