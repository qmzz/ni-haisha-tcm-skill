# P8 手工来源精修状态


## R15 p11_content_quality_queue 续跑（2026-07-07）

- **分支：** `p8-manual-source-refinement`
- **启动检查：** 初始 `git status --short` 干净；`.venv/bin/python -m pytest -q` → `38 passed`
- **本轮范围：** `data/p11_content_quality_queue.jsonl` 第 77-106 行，从 `jinyingzi` 到 `menghua`，共 30 条逐条人工复核。
- **下一条：** 第 107 行 `mengshi`，文件 `knowledge/herbs/mengshi.md`。

### R15 完成摘要

- 第 77-86 行：`jinyingzi`, `jinyinhua`, `jiucaizi`, `jixueteng`, `juhua`, `kulianpi`, `kushen`, `laifuzi`, `laoguancao`, `leigongteng`。
- 第 87-106 行：`leiwan`, `lianxu`, `lingzhi`, `liuhuang`, `liujinu`, `lizhihe`, `longdancao`, `lugen`, `luhui`, `lulutong`, `luobuma`, `luobumaye`, `luohanguo`, `luoshiteng`, `lvtuomei`, `mabo`, `machixian`, `madouling`, `maqianzi`, `menghua`。

### R15 重点发现

- `jinyingzi`：正文与 registry quote 已清理相邻条目（旋覆花/兰草/蛇床子）污染，收窄到金樱子实际命中窗口。index/verified_sources 仍需后续同步清理。
- `lugen`：已验证 source_ref 来自金匮要略原文食物中毒急救段落（非倪师人纪讲解），不支撑性味归经；建议后续降级为 external_source_required。
- `madouling`：已验证 source_ref 来自倪师讲解防己时顺带提及"马兜铃酸"，属旁及提及语境，非独立马兜铃药材讲解；不支撑性味归经。
- `luobuma`/`luobumaye`：疑似别名/重复条目，未查验到内部来源，建议后续合并或交叉索引。
- 其余 no_source 条目保持外部权威来源边界，未增补未验证医学内容。

### R15 测试与提交

- 初始基线：`38 passed`
- 第 77-86 行后：`38 passed`，commit `63e699b refine: manually review p11 quality jinyingzi-leigongteng`
- 第 87-106 行后：`38 passed`，commit `a287eaf refine: manually review p11 quality leiwan-menghua`

### R15 工作边界

- `jinyingzi` 正文清理：删除了 frontmatter quote、倪师讲解、来源摘录中的相邻条目污染；不补 properties/meridian。
- 其余条目均仅写 review note，不修改正文，no_source 保持边界。

## R15 p11_content_quality_queue 续跑（2026-07-07）

- **分支：** `p8-manual-source-refinement`
- **启动检查：** 初始 `git status --short` 干净；`.venv/bin/python -m pytest -q` → `38 passed`
- **本轮范围：** `data/p11_content_quality_queue.jsonl` 第 77-106 行，从 `jinyingzi` 到 `menghua`，共 30 条逐条人工复核。
- **下一条：** 第 107 行 `mengshi`，文件 `knowledge/herbs/mengshi.md`。

### R15 完成摘要

- 第 77-86 行：`jinying-zong`, `jinyinhua`, `jiucaizi`, `jixueteng`, `juhua`, `kulianpi`, `kushen`, `laifuzi`, `laoguancao`, `leigongteng`。
- 第 87-106 行：`leiwan`, `lianxu`, `lingzhi`, `liuhuang`, `liujinu`, `lizhihe`, `longdancao`, `lugen`, `luhui`, `lulutong`, `luobuma`, `luobumaye`, `luohanguo`, `luoshiteng`, `lvtuomei`, `mabo`, `machixian`, `madouling`, `maqianzi`, `menghua`。

### R15 重点发现

- `jinyingzi`：正文与 registry quote 已清理相邻条目（旋覆花/兰草/蛇床子）污染，收窄到金樱子实际命中窗口。index/verified_sources 仍需后续同步清理。
- `lugen`：已验证 source_ref 来自金匮要略原文食物中毒急救段落（非倪师人纪讲解），不支撑性味归经；建议后续降级为 external_source_required。
- `madouling`：已验证 source_ref 来自倪师讲解防己时顺带提及"马兜铃酸"，属旁及提及语境，非独立马兜铃药材讲解；不支撑性味归经。
- `luobuma`/`luobumaye`：疑似别名/重复条目，未查验到内部来源，建议后续合并或交叉索引。
- 其余 no_source 条目保持外部权威来源边界，未增补未验证医学内容。

### R15 测试与提交

- 初始基线：`38 passed`
- 第 77-86 行后：`38 passed`，commit `63e699b refine: manually review p11 quality jinyingzi-leigongteng`
- 第 87-106 行后：`38 passed`，commit `a287eaf refine: manually review p11 quality leiwan-menghua`

### R15 工作边界

- `jinyingzi` 正文清理：删除了 frontmatter quote、倪师讲解、来源摘录中的相邻条目污染；不补 properties/meridian。
- 其余条目均仅写 review note，不修改正文，no_source 保持边界。
