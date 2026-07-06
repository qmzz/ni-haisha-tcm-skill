# P8 手工来源精修状态


## R20 高确定性 source-boundary / registry 同步修复（2026-07-07）

- **分支：** `p8-manual-source-refinement`
- **启动检查：** 初始 `git status --short --branch` 干净；`.venv/bin/python -m pytest -q` → `38 passed`
- **本轮范围：** 从既有 `report/p8_manual_reviews/*.md` 中选择证据边界清楚的小批修复；不做大规模字段同步、不做别名合并。
- **完成数量：** 4 项。

### R20 已完成修复

- `jinyingzi`：按已清理 Markdown 同步 `data/herb_index.jsonl` 与 `data/verified_sources.jsonl` 的 quote，移除相邻旋覆花/兰草等污染；不补 properties/meridian。
- `lugen`：确认当前来源仅为金匮食物中毒急救方中“芦根煮汁”，不支撑芦根独立性味归经；Markdown、`herb_index`、`verified_sources`、`knowledge_completeness` 降级为 needs_review / external_source_required。
- `madouling`：确认当前来源为防己讲解旁及“马兜铃/马兜铃酸”，不支撑马兜铃独立药材字段；Markdown、`herb_index`、`verified_sources`、`knowledge_completeness` 收紧为 needs_review / contextual_mention。
- `dongkuizi`：清理 `herb_index` 中 properties/meridian/effects 的 Markdown 字段串联污染；保留 direct source boundary，`meridian` 置空并在 `knowledge_completeness` 标为缺失。

### R20 暂缓 / 未做

- `sanleng`：review note 指出当前神农本草经 source_ref 为玉竹/萎蕤形态 false positive，但 FTS 另有金匮方中三棱用药线索；本轮未证成整体边界，继续暂缓。
- `sangzhi`：当前 source_ref 来自桑螵蛸产地语境，另有桑枝用药/部位旁及线索；需单独决定 contextual/weak/no_source，不在本轮强改。

### R20 测试与提交

- 基线：`38 passed`
- 修复后：`38 passed`
- 提交：待本轮提交后回填。

### R20 工作边界

- 逐项读取 review note、knowledge 文件、index / verified_sources / knowledge_completeness / source_fts.sqlite 后再修改。
- 未新增外部医学正文，未补未支撑字段，未处理 `xiamen` / `yangguan` / `yinjiao_ren` 已完成项。

## R19 高确定性专项修复（2026-07-07）

- **分支：** `p8-manual-source-refinement`
- **启动检查：** 初始 `git status --short` 干净；`.venv/bin/python -m pytest -q` → `38 passed`
- **本轮范围：** 基于既有 `report/p8_manual_reviews/*.md` 证据，只做 5-10 个高确定性数据一致性修复；不新增 review note 队列、不批量重写正文。
- **完成数量：** 6 项。

### R19 已完成修复

- `zhongshu`：清理伤寒论“中枢神经/生命中枢”等非穴位语境 false positive；Markdown、`acupoint_index`、`knowledge_completeness` 降级为 `no_source_found/no_source`，并从 `verified_sources` 移除。
- `ganlan`：清理 football/橄榄球语境 false positive；Markdown、`herb_index`、`knowledge_completeness` 降级为 `no_source_found/no_source`，并从 `verified_sources` 移除。
- `jianghuang`：清理“干姜黄连黄芩人参汤”跨词误切 false positive；Markdown、`herb_index`、`knowledge_completeness` 降级为 `no_source_found/no_source`，并从 `verified_sources` 移除。
- `xiamen`：title/alias 为侠白，归经从 `足阳明胃经` 修为 `手太阴肺经`；同步 `knowledge/acupoints/xiamen.md` 与 `acupoint_index`，未做别名合并或 source_ref 替换。
- `yangguan`/`yaoyangguan`：别名条目 `yangguan` 归经从 `足少阳胆经` 修为 `督脉`，与主条目 `yaoyangguan` 保持一致；两者仍保持 no-source 外部来源边界。
- `yinjiao_ren`：移除错误映射到 `yinjiao`（龈交）的 `canonical_item_id` / `verified_alias` 状态；统一降级为 `no_source_found/no_source` 并加入 no-source / external-source 后续队列。未直接补 p29 来源，留待单独核查 quote 后提升。

### R19 未做 / 暂缓原因

- `sanleng`：review note 指出神农本草经“地下茎粗大有三棱”为玉竹/萎蕤形态 false positive；但正文另含金匮消肿溃坚汤中直接出现“三棱”的片段，本轮未做整体降级，需单独判断药材条目 source boundary。
- `sangzhi`：当前 source_ref 来自桑螵蛸产地语境，不支撑桑枝归经；但 FTS 另有桑枝用药旁及线索，本轮未贸然整体降级，需后续决定 contextual/weak/no_source 边界。
- `huangbo`/`huangbai`：属黄柏重复/同源别名治理问题，影响面超过本轮少量高确定性修复；本轮只保留 review notes，不做合并。
- 其他 p11/p26 候选：继续保留 review note 证据，等待后续按字段同步、source boundary 或 alias 专项处理。

### R19 测试与提交

- 基线：`38 passed`
- 第一批 `zhongshu ganlan jianghuang` 后：`38 passed`，commit `974adfa fix: apply p8 reviewed source-boundary corrections zhongshu ganlan jianghuang`
- 第二批 `xiamen yangguan yinjiao_ren` 后：`38 passed`，commit `f3d986e fix: apply p8 reviewed source-boundary corrections xiamen yangguan yinjiao_ren`

### R19 工作边界

- 只使用既有人工复核证据做最小修复；未新增医学字段、未引入外部正文、未做批量清洗。
- 对降级项同步了 Markdown、index、`knowledge_completeness`、`verified_sources`、no-source/external-source 队列，避免状态分裂。
- 对证据不足或牵涉广的项目仅记录暂缓原因，不强改。


## R18 p26_needs_review_segments 收尾（2026-07-07）

- **分支：** `p8-manual-source-refinement`
- **启动检查：** `git status --short --branch` 干净；`.venv/bin/python -m pytest -q` → `38 passed`
- **本轮范围：** `data/p26_needs_review_segments.jsonl` 第 98-157 行中尚无 review note 的 50 条，从 `ejiao` 到 `puhuang`。
- **完成状态：** p26 队列 `160/160 completed`；已全清。
- **下一条：** p26 无下一条。

### R18 完成摘要

- 第一组 10 条：`ejiao`, `fangfeng`, `fuling`, `gancao`, `gansui`, `gongcao`, `gouqizi`, `gualou`, `gualue`, `guanzhong`。
- 第二组 10 条：`guiban`, `haizaomu`, `hehuanpi`, `heshouwu`, `honghua`, `houpo`, `huaihua`, `huaijiao`, `huajiao`, `huangbai`。
- 第三组 10 条：`huangbo`, `huangqi`, `hujiao`, `huomaren`, `hupo`, `jiegeng`, `jili`, `jineijin`, `kuandonghua`, `kunbu`。
- 第四组 10 条：`lianqiao`, `lingxiaohua`, `lingyangjiao`, `longyanrou`, `lujiao`, `mahuang`, `mahuanggen`, `maidong`, `maiya`, `meiguihua`。
- 第五组 10 条：`mengchong`, `moyao`, `mutong`, `muxiang`, `nanshashen`, `niuhuang`, `niuxi`, `paojiang`, `peilan`, `puhuang`。

### R18 重点发现

- 已有正文直接来源但 registry/verified_sources 未同步或错配：`ejiao`, `gancao`, `jiegeng`, `lingyangjiao`, `mahuang`, `moyao`, `puhuang`。
- 直接来源成立但 quote 前后跨相邻条目：`gongcao`, `gouqizi`, `hehuanpi`, `huaihua`, `huaijiao`, `huomaren`, `jili`, `kuandonghua`, `lingxiaohua`, `longyanrou`, `niuhuang`, `niuxi` 等。
- 旁及提及/方中组成误作 direct 的高风险条目：`gansui`, `heshouwu`, `huajiao`, `huangbai`, `huangbo`, `huangqi`, `hujiao`, `hupo`, `kunbu`, `lianqiao`, `mahuanggen`, `maidong`, `maiya`, `meiguihua`。
- 重复/别名规范候选：`gualou`/`gualue` 同为瓜蒌；`huangbai`/`huangbo` 同为黄柏；`peilan` 来自兰草/省头草同株解释，宜按 alias/contextual 处理；`nanshashen` 来自沙参条目分型说明。

### R18 测试与提交

- 初始基线：`38 passed`
- 第一组后：`38 passed`，commit `193f19a refine: manually review p26 segments ejiao-guanzhong`
- 第二组后：`38 passed`，commit `9b918b1 refine: manually review p26 segments guiban-huangbai`
- 第三组后：`38 passed`，commit `2c5426b refine: manually review p26 segments huangbo-kunbu`
- 第四组后：`38 passed`，commit `0713fe5 refine: manually review p26 segments lianqiao-meiguihua`
- 第五组与状态更新后：最终测试见本轮提交。

### R18 工作边界

- 本轮新增 50 条人工 review notes，未修改 knowledge 正文、index、sources 或 registry。
- 对 p26 的 needs_review segment 以记录证据边界为主；只有明确后续修复方向，未批量改正文。
- FTS exact MATCH 本轮多为空；主要依据 p26 行、knowledge 文件、`knowledge_completeness.jsonl`、`verified_sources.jsonl` 与 source quote 摘要判断。


## R17 p26_needs_review_segments 专项推进（2026-07-07）

- **分支：** `p8-manual-source-refinement`
- **启动检查：** 初始 `git status --short --branch` 干净；`.venv/bin/python -m pytest -q` → `38 passed`
- **本轮范围：** `data/p26_needs_review_segments.jsonl` 尚无 review note 的第 1-97 行，按文件顺序从 `benshen` 到 `duzhong`，新增 38 条人工复核记录。
- **完成状态：** p26 队列 `110/160 completed`；剩余 50 条。
- **下一条：** 第 98 行 `ejiao`（阿胶），文件 `knowledge/herbs/ejiao.md`。

### R17 完成摘要

- 第一组 10 条：`benshen`, `chengguang`, `dachangshu`, `dicang`, `dingchuan`, `gaohuangshu`, `guanmen`, `jiaji`, `luoque`, `luozhen`。
- 第二组 10 条：`qucha`, `quyuan`, `shuitu`, `tongtian`, `wuchu`, `xiabai`, `xiamen`, `xinhui`, `yishe`, `yutang`。
- 第三组 10 条：`bohe`, `chenpi`, `chenxiang`, `cheqianzi`, `chuanxiong`, `cishi`, `congbai`, `dahuang`, `daji`, `danggui`。
- 第四组 8 条：`dangshen`, `danshen`, `daqingye`, `dilong`, `dingxiang`, `dongkuizi`, `duhuo`, `duzhong`。

### R17 重点发现

- 穴位段多数为 source_ref 页码/JSON 边界污染：如 `benshen`, `tongtian`, `luozhen` 命中目录或整本 JSON 开头；`quyuan` frontmatter 仅残留版本号片段。多数正文已有针灸篇直接候选，建议后续同步 source_ref 而非改正文。
- `qucha`, `xinhui`, `yutang` 的现有证据偏相邻定位/异文/旁及，后续应考虑降级或补查更直接来源。
- `xiamen` 是重复/别名异常：title 为侠白且 `alias_of: xiabai`，但 index 归经为足阳明胃经；需后续单列别名和 registry 一致性修复。
- 草药段出现多条“旁及提及误升 verified_direct”：`bohe` 只是薄荷影响舌苔观察，`chenxiang` 仅为柏子仁丸方中旁及，`cishi` 来自丹砂“畏磁石”，`congbai` 来自防风“得葱白”，`dingxiang` 来自桂枝香料旁及，`duhuo` 来自麝香开窍段旁及独活羌活。
- 已有 P17 正文长讲解但 registry 仍 empty_quote 的条目：`chenpi`, `cheqianzi`, `chuanxiong`, `daji`, `dangshen`, `danshen`, `dilong`, `duzhong`；建议后续同步 source_refs/index/sources。
- `dongkuizi` 另发现结构字段污染：`herb_index` 的 `properties`/`meridian` 混入 Markdown 功效/主治文本，需专项字段清理。

### R17 测试与提交

- 初始基线：`38 passed`
- 第一组后：`38 passed`，commit `9759175 refine: manually review p26 segments benshen-luozhen`
- 第二组后：`38 passed`，commit `ad29485 refine: manually review p26 segments qucha-yutang`
- 第三组后：`38 passed`，commit `5d330dd refine: manually review p26 segments bohe-danggui`
- 第四组后：`38 passed`，commit `4ea9142 refine: manually review p26 segments dangshen-duzhong`

### R17 工作边界

- 本轮仅新增人工 review notes 与状态记录；未修改知识正文、index、sources 或 registry。
- 对明显 source boundary 错配、旁及提及、empty_quote 未同步的条目均只记录证据和后续修复建议。
- FTS exact MATCH 对本轮条目多为空；主要依据 p26 行、knowledge 文件、index/sources/knowledge_completeness 与候选 jsonl 摘要判断。


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
