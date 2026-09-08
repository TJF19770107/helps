---
name: 学术科研技能套件ARS
description: >
  学术科研五合一技能套件（本地适配版）。覆盖：文献检索、实证SQL数据分析、论文大纲生成、
  审稿回复生成、引用校验。基于开源 ARS-Codex v0.1.28 适配，全部检索/统计走本地零积分脚本，
  禁止整包加载、禁止学位论文完整代写、所有文献与统计结果必须人工核验。
version: 1.0
agent_created: true
lobster:
  cost_mode: zero-credit
  上游来源: Imbad0202/academic-research-skills-codex (ARS-Codex v0.1.28)
  上游许可: CC BY-NC 4.0（非商用，商用需另行取得授权）
  上游路径: E:\龙虾AI主控中心\我的AI分身\企业微信群定制接单项目\skills\research-suite
  Python: G:\g_venv_ars\Scripts\python.exe
  依赖: pyyaml / markdown / duckdb（已装于 G:\g_venv_ars）
  触发词:
    - 学术科研
    - 文献检索
    - 论文大纲
    - 审稿回复
    - 引用校验
    - SQL实证分析
    - 文献综述
    - ARS
allowed-tools: Read, Glob, Grep, Bash(python *), Bash(G:/g_venv_ars/Scripts/python.exe *)
---

# 学术科研技能套件 ARS（龙虾适配版 v1.0）

## 铁律 0：先路由，后加载（最高优先级，防 token 爆炸）

上游套件内含 **30+ 个 agent 文件**，单个 agent 动辄 5,000–10,000 tokens
（`synthesis_agent.md` ≈ 8.6k、`domain_reviewer_agent.md` ≈ 10.3k）。
**严禁一次性读取整个 `ars/` 目录或整篇 WORKFLOW.md 全文。**

执行顺序（每次调用必须遵守）：
1. 由下方路由表定位到**唯一**一个子技能目录
2. 只读该子技能的 `SKILL.md`（本目录下的）
3. 只按需读取它指明的**那 1–3 个**上游 agent / reference 文件
4. 需要检索或计算时，**先跑本地脚本**，再让模型做归纳

违规成本：一次全量加载 ≈ 80,000+ tokens，等同静默烧掉一天额度。

## 五技能路由表

| # | 子技能 | 触发场景 | 目录 | 上游入口 |
|---|--------|----------|------|----------|
| 1 | 文献检索 | 找文献、文献综述、系统性回顾、事实核查、研究方向收敛 | `subskills/01_文献检索/` | `ars/deep-research/WORKFLOW.md` |
| 2 | 实证SQL数据分析 | 跑数据、回归、分组统计、描述性统计、复现性验证 | `subskills/02_实证SQL数据分析/` | `ars/experiment-agent/WORKFLOW.md` |
| 3 | 论文大纲生成 | 论文架构、章节分配、证据映射、IMRaD 结构 | `subskills/03_论文大纲生成/` | `ars/academic-paper/WORKFLOW.md` |
| 4 | 审稿回复生成 | 回复审稿意见、rebuttal、逐条回应、修改说明 | `subskills/04_审稿回复生成/` | `ars/academic-paper-reviewer/WORKFLOW.md` |
| 5 | 引用校验 | 正文引用↔参考文献比对、APA7 格式、文献真实性核对 | `subskills/05_引用校验/` | `ars/academic-paper/agents/citation_compliance_agent.md` |

**跨阶段任务**（如「从选题到成稿」）：必须拆成多个子技能依次调用，**不得**启用端到端流水线。

## 已禁用（禁止调用，token 黑洞）

| 目录 | 状态 | 原因 |
|------|------|------|
| `ars/academic-pipeline/` | **禁用**（已改名 `ars/.disabled_academic-pipeline`） | WORKFLOW.md 达 51,865 字符 ≈ 16.2k tokens，端到端全链最重 |
| `ars/audits/`、`ars/evals/`、`ars/tests/` | 不加载 | 上游测试与审计资产，非生产路径 |
| `deep-research/agents/*`（13 个） | **按需单取** | 禁止 `Glob` 全量读取 |

## 零积分脚本（本套件自带，本地执行，不耗积分）

| 脚本 | 用途 | 最小调用 |
|------|------|----------|
| `scripts/ars_lit_search.py` | arXiv / CrossRef / OpenAlex / Semantic Scholar 检索（免费 API，无需密钥） | `python ars_lit_search.py --source arxiv --q "关键词" --limit 10` |
| `scripts/ars_sql_query.py` | duckdb 直查 CSV/Parquet，失败降级 stdlib sqlite | `python ars_sql_query.py --table main=data.csv --sql "SELECT ..."` |
| `scripts/ars_citation_check.py` | 三层引用校验（结构/格式/**存在性**），可联网核对文献真伪 | `python ars_citation_check.py draft.md --verify` |

统一使用：`G:\g_venv_ars\Scripts\python.exe`（已装 pyyaml、markdown、duckdb）
备用：`C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`（无 yaml/markdown/duckdb，仅脚本 --engine sqlite 可用）

## 成本红线（七铁律在本套件的落地）

1. **免费先用**：检索一律先跑 `ars_lit_search.py`，**不得**直接开 WebSearch
2. **切换必报**：确需 WebSearch 兜底时，必须先向汤哥报备模型与预估消耗
3. **付费须确认**：任何调用付费模型的动作，必须停下请示
4. **回答必报**：每次交付须汇报本次实际加载的文件数与 token 量级
5. 检索结果优先落本地 JSON 缓存（`--cache`），同一课题不重复联网

## 合规红线（强制，详见 `风险提示与合规红线.md`）

- **禁止**学位论文/课程论文的完整代写与整章生成
- **禁止**凭空补全任何文献的作者、年份、DOI、页码
- **禁止**书写脚本未实际产出的统计量（系数、p 值、样本量、效应量）
- **所有** AI 产出必须经人工核验后方可进入正式稿件

## 版本与来源

- 本地适配版：v1.0（2026-09-09）
- 上游：ARS-Codex v0.1.28，内嵌 ARS 套件 source commit `9443623`（上游 metadata 3.21.1）
- 上游许可：**CC BY-NC 4.0 非商用** —— 若用于商业接单交付，须另行确认授权
