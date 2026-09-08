---
name: 龙虾科研辅助技能包
description: >
  龙虾AI主控中心自有版权科研辅助体系 v1.0。融合三个 MIT 开源技能的可商用组件 +
  三个自研零积分脚本，覆盖：文献检索、实证SQL数据分析、论文写作与大纲、审稿回复、引用校验。
  可商用、可转售、可交付客户。禁止用于论文全文代写；所有文献与统计结果须人工核验。
version: 1.0
agent_created: true
lobster:
  cost_mode: zero-credit
  许可: MIT（本包原创部分）；MIT 组件见 THIRD_PARTY.md；本包无 NC 内容
  Python: G:\g_venv_ars\Scripts\python.exe（或 workbuddy 3.13.12 兜底）
  触发词: [科研辅助, 龙虾科研, 文献检索, 论文写作, 论文大纲, 审稿回复, 引用校验, SQL实证分析]
allowed-tools: Read, Glob, Grep, Bash(python *), Bash(G:/g_venv_ars/Scripts/python.exe *)
---

# 龙虾科研辅助技能包 v1.0（自有版权 · 可商用）

## 版权结构（先读，决定你能拿它干什么）

| 组成 | 版权 | 可否商用/转售 |
|------|------|--------------|
| `scripts/` 3 个脚本（lobster_lit_search / lobster_sql_query / lobster_citation_check） | **龙虾原创** | ✅ 无任何限制 |
| 5 个子技能 SKILL.md（`subskills/`） | **龙虾原创** | ✅ 无任何限制 |
| `参考文献写作素材/`、`质量门禁/` | **MIT 组件 vendored**（Liuyuan999 / Arpit Gupta / Li Shixiong 原作，保留其版权） | ✅ MIT 允许，须保留声明（见 THIRD_PARTY.md） |
| 上游 ARS 套件（CC BY-NC） | **不在本包内**。仅存在于内部参考目录，禁止随本包分发 | — |

## 铁律 0：按需加载（防 token 爆炸）

素材目录里单文件最大 30k+ 字符。**每次调用只进 1 个子技能，只读该子技能白名单内的文件。**
禁止 Glob 全量扫描 `参考文献写作素材/`。

## 五技能路由表

| # | 子技能 | 触发场景 | 目录 |
|---|--------|----------|------|
| 1 | 文献检索 | 找文献、文献综述、系统性回顾、研究方向收敛 | `subskills/01_文献检索/` |
| 2 | 实证SQL数据分析 | 跑数据、分组统计、描述统计、复现验证 | `subskills/02_实证SQL数据分析/` |
| 3 | 论文写作与大纲 | 选题头脑风暴、大纲、章节起草、压缩润色、质量门禁 | `subskills/03_论文写作与大纲/` |
| 4 | 审稿回复 | Response to Reviewers、逐条回应、修改说明 | `subskills/04_审稿回复/` |
| 5 | 引用校验 | 引文比对、格式、文献真实性核对 | `subskills/05_引用校验/` |

## 零积分脚本（自有版权）

统一解释器：`G:\g_venv_ars\Scripts\python.exe`（已装 pyyaml/markdown/duckdb）

```bash
# 文献检索（arXiv/CrossRef/OpenAlex/S2 免费直连，实测 200）
python scripts/lobster_lit_search.py --source all --q "关键词" --limit 20 --out refs.json

# SQL 实证分析（duckdb→stdlib 三级降级；保留字列名加双引号）
python scripts/lobster_sql_query.py --table main=data.csv --sql "SELECT ..." --out result.csv

# 三层引用校验（--verify 联网核对文献真伪，专治幻觉）
python scripts/lobster_citation_check.py draft.md --verify
```

## 合规红线（与《科研辅助商业化合规路线图》一致）

1. **禁止**论文全文/整章代写交付；交付物=报告/数据/建议/骨架
2. **禁止**编造文献、数据、统计量；每个数字必须能在脚本输出中定位
3. 定稿前必跑 `lobster_citation_check.py --verify`，未命中文献逐条人工核实
4. 对外话术：科研效率辅助，永不承诺「包写包过包发表」

## 版本

- v1.0（2026-09-09）：首版。3 自研脚本 + 5 自研子技能 + 12 个 MIT 素材文件 + 4 个 MIT 门禁脚本
