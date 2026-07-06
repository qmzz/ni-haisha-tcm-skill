# P8 Manual Source Refinement Status

Updated: 2026-07-06 21:36 Asia/Shanghai
Branch: `p8-manual-source-refinement`

## 已完成条目

已按 `data/p39_high_risk_external_review_queue.jsonl` 顺序完成前 6 个高风险条目的人工复核、知识文件边界精修与 review note：

1. `fanxieye` / 番泻叶
   - 确认 `review_queue` 中“泻叶”仅为低分别名命中，不能作为番泻叶来源。
   - 保持 `trace_status: no_source_found`，增加高风险外部来源复核边界。
   - note: `report/p8_manual_reviews/fanxieye.md`
2. `haima` / 海马
   - `herb_sources`、`review_queue`、FTS 均无可追溯来源。
   - 按 `herb_animal_or_restricted` 高风险边界处理。
   - note: `report/p8_manual_reviews/haima.md`
3. `hamayou` / 哈蟆油
   - “哈蟆油 / 蛤蟆油 / 雪蛤”FTS 均无命中。
   - 按 `herb_animal_or_restricted` 高风险边界处理。
   - note: `report/p8_manual_reviews/hamayou.md`
4. `huangyaozi` / 黄药子
   - `herb_sources`、`review_queue`、FTS 均无可追溯来源。
   - 保持 `no_source_found`，标记需要外部权威资料。
   - note: `report/p8_manual_reviews/huangyaozi.md`
5. `leigongteng` / 雷公藤
   - 内部语料无命中；既有功效/讲解种子内容来源不明。
   - 将种子功效/讲解降级为“待外部来源核验”，不作为用药依据。
   - note: `report/p8_manual_reviews/leigongteng.md`
6. `luhui` / 芦荟
   - `p30` / completeness 显示 P6-C `internal_research_exhausted`。
   - 保持 `no_source_found` 与 P6-C 边界，标记需要外部权威资料。
   - note: `report/p8_manual_reviews/luhui.md`

## 正在处理 / 下一条

- 下一条：`maqianzi` / 马钱子。
- 已只读检索初步确认：`herb_sources`、`review_queue`、source FTS 对“马钱子 / 番木鳖”无可追溯命中；尚未编辑文件或写 review note。

## 测试状态

- 初始基线：`.venv/bin/python -m pytest -q` → `38 passed`。
- 第一批 3 条后：`38 passed`。
- 第二批 3 条后：`38 passed`。

## Commits

- `39ebfa6 refine: manually review fanxieye haima hamayou`
- `b379c90 refine: manually review huangyaozi leigongteng luhui`

## 工作边界

- 未使用脚本批量生成或批量修改知识正文；一次误用只读 Python 后又尝试批量编辑 3 个文件，已立即 `git checkout --` 回滚，未纳入成果。
- 本轮正式知识正文修改均通过人工阅读当前文件、registry/queue/FTS 结果后逐条编辑完成。
- 所有高风险条目均保守处理：无权威来源时不补剂量、禁忌、妊娠/儿童、毒性、现代相互作用或法定状态。