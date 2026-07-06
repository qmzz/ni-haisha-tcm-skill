# P8 手工来源精修状态


## R16 p11_content_quality_queue 收尾（2026-07-07）

- **分支：** `p8-manual-source-refinement`
- **启动检查：** 初始 `git status --short` 干净；`.venv/bin/python -m pytest -q` → `38 passed`
- **本轮范围：** `data/p11_content_quality_queue.jsonl` 第 107-216 行，从 `mengshi` 到 `zuwuli`；重点处理其中尚无 `report/p8_manual_reviews/<item_id>.md` 的 38 条。
- **完成状态：** p11 内容质量队列 `216/216 completed`；全队列均已有人工复核记录。
- **下一条：** p11 无下一条；建议下一阶段处理本轮标出的 source boundary 降级/字段同步候选。

### R16 完成摘要

- 新增 review notes 38 条：`mengshi`, `mingfan`, `mugua`, `qiancao`, `qianghuo`, `qingxiangzi`, `qinpi`, `sangzhi`, `sanleng`, `shashen`, `shechuangzi`, `shegan`, `shenjincao`, `shijunzi`, `songjie`, `suzi`, `wubeizi`, `wujiapi`, `wushaoshe`, `wuyi`, `xiakucao`, `xiangru`, `xiaoji`, `xiebai`, `xinyi`, `xionghuang`, `xuanfuhua`, `xuanshen`, `xueyutan`, `yangqishi`, `yinchen`, `yujin`, `yuyuliang`, `zaojia`, `zaojiaoci`, `zaoxintu`, `ziheche`, `zisu`。
- 已确认第 109-216 行中其余 no_source/acupoint 条目此前已有 review note；本轮未重复覆盖。

### R16 重点发现

- `mengshi`：来源仅旁及“礞石滚痰丸”，后文实际为天南星讲解，不支撑礞石性味归经。
- `sanleng`：source_ref 是玉竹/萎蕤“地下茎粗大有三棱”的形态描述，属于 false positive，不支撑三棱药材字段。
- `sangzhi`：source_ref 来自桑螵蛸“着生于桑枝上者”产地语境，不支撑桑枝性味归经。
- `shenjincao`, `shijunzi`, `wubeizi`, `wushaoshe`, `xiaoji`, `xueyutan`：均为旁及提及、方中药物或名物解释语境，不支撑缺失的结构字段。
- `ziheche`：发现同名异物风险；神农本草经命中指“蚤休/重楼/甘遂，今人谓之紫河车”，另有胎盘紫河车旁及语境，需后续单列复核。
- 可作为后续字段同步候选但本轮未同步：`qiancao` 性味，`shegan` 入肺线索，`wuyi` 性味，`xionghuang` 性味/毒性，`yinchen` 性味等；均需按字段同步规范另行处理。

### R16 测试与提交

- 初始基线：`38 passed`
- 第 107-159 行无 note 条目后：`38 passed`，commit `5f795d8 refine: manually review p11 quality mengshi-xiangru`
- 第 163-199 行无 note 条目及状态更新后：`38 passed`，commit 待本状态块提交。

### R16 工作边界

- 本轮只新增人工 review notes 和状态记录；未修改知识正文。
- 对缺字段只记录“后续可同步字段”候选，不直接补字段。
- 对 source boundary 不清、旁及提及、false positive 条目均在对应 review note 中标记，未新增未验证医学内容。


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
