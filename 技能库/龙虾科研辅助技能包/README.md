# 龙虾科研辅助技能包（Lobster Research Assist Kit）v1.0

> 龙虾AI主控中心自有版权 · MIT 许可 · **可商用、可转售、可交付客户**
> 2026-09-09 由汤小龙分身按「融合 MIT 开源 + 自研升级」路线组装

## 一句话

把「文献检索 → SQL 实证 → 写作流水线 → 审稿回复 → 引用校验」封装成一轨到底的科研辅助体系；
三个核心脚本完全自研，写作素材与质量门禁来自三个 MIT 项目（合法 vendored，声明齐全），**零 NC 内容**。

## 商业化能力（相对上一代 ARS 套件的关键升级）

| 项 | ARS 套件（上一代） | 本包 |
|----|--------------------|------|
| 许可 | CC BY-NC 4.0 **非商用** | **MIT 可商用** |
| 能否交付客户 | ❌（NC + 交付代写双重风险） | ✅（守合规红线的前提下） |
| 能否打包进产品转售 | ❌ | ✅（保留 THIRD_PARTY.md 即可） |
| 核心脚本 | — | 3 个全自研（检索/SQL/引用校验） |
| NC 依赖 | 深度耦合上游 agent 文件 | **零依赖**（写作素材全部换 MIT 来源） |

## 目录结构

```
龙虾科研辅助技能包/
├── SKILL.md                # 路由器（入口）
├── subskills/              # 5 个自研子技能
│   ├── 01_文献检索/         ├── 02_实证SQL数据分析/
│   ├── 03_论文写作与大纲/    ├── 04_审稿回复/    └── 05_引用校验/
├── scripts/                # 3 个自研零积分脚本
├── 参考文献写作素材/         # 12 个 MIT vendored 素材
├── 质量门禁/                # 4 个 MIT vendored Python 门禁脚本
├── LICENSE                 # MIT（本包）
├── THIRD_PARTY.md          # 第三方声明（分发必带）
└── README.md
```

## 快速上手

```bash
PY=G:/g_venv_ars/Scripts/python.exe
# 文献检索（免费学术 API 直连）
$PY scripts/lobster_lit_search.py --source all --q "large language model education" --limit 10
# SQL 实证
$PY scripts/lobster_sql_query.py --table main=data.csv --sql "SELECT grp, AVG(score) FROM main GROUP BY 1"
# 引用校验（防幻觉）
$PY scripts/lobster_citation_check.py draft.md --verify
```

依赖：`pyyaml`、`markdown`、`duckdb`（装于 `G:\g_venv_ars`）；未装时 SQL 自动降级 stdlib sqlite。

## 合规红线（必须随包传达）

1. 禁止论文全文/整章代写交付 —— 卖辅助，不卖代写
2. 所有文献与统计结果必须人工核验 —— 每个数字能在脚本输出中定位
3. 对外话术：科研效率辅助，永不承诺「包写包过包发表」

## 来源与验证记录（2026-09-09 实测）

| 来源 | LICENSE 验证 | 方式 |
|------|--------------|------|
| Liuyuan999/claude-skill-paper-writing | MIT ✅ | clone 后读 LICENSE 文件原文 |
| SNL-UCSB/paper-writing-skill | MIT ✅ | 同上 |
| lishix520/academic-paper-skills | MIT ✅ | 同上 |
| kchemorion/academic-manuscript-skill | ⚠ 无 LICENSE 文件 | 未复制代码，仅借鉴思路 |
| Imbad0202/academic-research-skills（ARS 原版） | **CC BY-NC 4.0** ❌ | raw LICENSE 实测（博客称 MIT 系误传） |
| `gap_analysis.py --help` | 可运行 ✅ | 本机实跑 |
