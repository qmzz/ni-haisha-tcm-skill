# 倪海厦中医经方智能体体系 (Ni Haisha TCM Skill v3.0)

> *"治病必求于本，本于阴阳。水火气化，阳气为尊。"* —— 倪海厦

---

## 🏛️ 项目简介 (Overview)

本项目是基于倪海厦先生《人纪》（《针灸大成》《神农本草经》《伤寒论》《金匮要略》《黄帝内经》《天纪》）及汉唐经方体系全景语料，深度提纯重构的中医经方智能体与全景知识库。

已彻底剔除所有机械八股、免责声明及死板解剖占位，100% 还原倪海厦经方医学的**水火气化、四诊八纲、经方针灸一气贯通**的实战辨证心法。

---

## 📚 知识库全景架构 (Knowledge Architecture)

知识库全量收录 **1,077 篇** 高密度纯正 Markdown 文献，涵盖六大子库：

| 子库模块 | 路径 | 收录体量 | 结构规范与核心内容 |
| :--- | :--- | :---: | :--- |
| **经典经方库** | `knowledge/formulas/` | **113 首** | 经方原典 ➔ 倪师方义水火推演 ➔ 六经辨证抓手 ➔ 讲义医案实录 |
| **神农本草库** | `knowledge/herbs/` | **415 味** | 本草原意 ➔ 药性推演与破局心法 ➔ 配伍剂量法度 ➔ 讲义实录 |
| **针灸腧穴库** | `knowledge/acupoints/` | **411 穴** | 精准取穴 ➔ 经穴气化破局 ➔ 主治配穴手印 ➔ 针灸秘要实录 |
| **气化概念库** | `knowledge/concepts/` | **43 篇** | 阴阳脏腑本源 ➔ 水火物理模型 ➔ 病理传变规律 ➔ 讲义发挥 |
| **四诊辨证库** | `knowledge/diagnosis/` | **44 篇** | 诊断要诀 ➔ 望闻问切破局 ➔ 六经辨证抓手 ➔ 问诊实录秘要 |
| **实战医案库** | `knowledge/cases/` | **51 例** | 病案实录 ➔ 水火病机推演 ➔ 经方剂量配伍 ➔ 瞑眩转归 ➔ 倪师按语 |

---

## 🛠️ 知识库检索与工具入口 (Tooling & CLI)

项目提供轻量、毫秒级单例检索引擎（`internal/knowledge_query.py`）及统一 CLI 接口（`tools/tcm_tools.py`）：

### 1. 全文与语义检索 (`tcm_search`)
```bash
# 全库语义/关键词检索
python3 tools/tcm_tools.py tcm_search '{"query":"少阴水气凌心 心悸"}'

# 指定分类过滤 (formulas / herbs / acupoints / concepts / diagnosis / cases)
python3 tools/tcm_tools.py tcm_search '{"query":"太阳中风", "category":"formulas"}'
```

### 2. 精确文档读取 (`tcm_doc`)
```bash
python3 tools/tcm_tools.py tcm_doc '{"category":"herbs", "name":"附子"}'
python3 tools/tcm_tools.py tcm_doc '{"category":"formulas", "name":"真武汤"}'
python3 tools/tcm_tools.py tcm_doc '{"category":"diagnosis", "name":"十问歌"}'
```

---

## 🧭 问诊与交互流 (Clinical Flow)

- **模式一：经方 / 本草 / 腧穴 / 概念咨询**：直调知识库原典，输出四大标准板块；
- **模式二：临床十问与辨证求治**：
  - 动态调用倪师十问（睡眠、胃口、口渴、便溺、手足冷热、出汗、寒热）；
  - 定位六经病位（太阳/阳明/少阳/太阴/少阴/厥阴）与水火虚实；
  - 给出经方处方（汉制折算克数 + 煎服法）与针灸井荥输经合配穴。

---

## 📜 许可证 (License)

MIT License.
