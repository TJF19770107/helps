---
name: ARS实证SQL数据分析
description: 用 duckdb 在本地对 CSV/Parquet 执行 SQL 实证分析（描述性统计、分组聚合、回归前的数据准备），零积分、可复现；三级降级保证一定能跑。禁止书写脚本未产出的统计量。
version: 1.0
parent: 学术科研技能套件ARS
lobster:
  cost_mode: zero-credit
  触发词: [SQL分析, 实证分析, 跑数据, 描述性统计, 分组统计, 回归数据, 数据核对, 复现性验证]
  上游入口: ars/experiment-agent/WORKFLOW.md
  零积分脚本: scripts/ars_sql_query.py
  引擎: duckdb 优先 → stdlib sqlite 兜底
allowed-tools: Read, Bash(G:/g_venv_ars/Scripts/python.exe *)
---

# 2. 实证 SQL 数据分析

## 用途
本地零积分跑真实数据，产出**可复现**的描述性统计、分组聚合、变量构造与回归前数据准备。
**本技能负责「算出来」，不负责「解读成结论」**（解读需人工 + 参考上游统计指引）。

## 触发指令
```
SQL分析：对 data/raw.csv 按年份求均值与样本量
实证分析：比较实验组对照组前测后测差异
跑数据：复现论文 Table 3 的描述性统计
```

## 执行步骤
1. **确认数据**：路径、分隔符、编码（中文数据多为 `utf-8-sig` / GBK）、缺失值标记
2. **跑脚本**（零积分，必做）：
   ```bash
   G:/g_venv_ars/Scripts/python.exe scripts/ars_sql_query.py \
     --table main="E:/path/data.csv" \
     --sql "SELECT grp, COUNT(*) n, ROUND(AVG(score),2) m, ROUND(STDDEV(score),2) sd FROM main GROUP BY 1" \
     --out result.csv --show 50
   ```
   - 多表：`--table a=a.csv --table b=b.csv`，SQL 里直接 JOIN
   - Parquet 直接支持；**只读查询**（仅放行 SELECT / WITH / DESCRIBE）
3. **复现留痕**：把每条用过的 SQL 与 `--out` 结果文件一并归档，供审稿人复现
4. **解读**：读 `references/statistical_interpretation_guide.md`（~2.8k tok），**禁止**输出脚本未产出的数字

## 已实测（2026-09-09）
| 场景 | 结果 |
|------|------|
| duckdb 分组聚合 | ✅ A组 n=3 均值 86.3 / B组 n=3 均值 85.37 |
| stdlib sqlite 降级 | ✅ 年份计数正常 |
| 保留字列名（如 `group`） | ⚠ 需加双引号 `"group"`，否则语法错误 |

## 按需加载白名单
| 文件 | 体量 | 何时读 |
|------|------|--------|
| `experiment-agent/WORKFLOW.md` | ~3.6k tok | 需要完整实验流程 |
| `agents/code_runner_agent.md` | ~1.5k tok | 跑代码实验 |
| `references/statistical_interpretation_guide.md` | ~2.8k tok | 统计结果解读 |
| `templates/code_experiment_plan.md` | ~0.5k tok | 实验计划 |
| `references/reproducibility_protocol.md` | — | 复现性验证 |

## token 消耗预估
| 模式 | 加载内容 | 预估 |
|------|----------|------|
| **纯脚本分析**（默认，推荐） | 本 SKILL + 脚本，`--out` 结果回读 | **≈ 1–2k** |
| 分析 + 解读 | + 统计解读指引 | **≈ 4–5k** |
| 完整实验流程 | + WORKFLOW + code_runner | **≈ 6–8k** |

> 数据量大时**把结果落 CSV 再回读摘要**，不要把整表塞进上下文——这是本技能最大的 token 陷阱。

## 人工核验点（强制）
- [ ] 论文中的**每个数字**都能在脚本输出里找到出处
- [ ] 样本量口径（缺失值/异常值剔除规则）由人工确认
- [ ] 显著性与效应量必须来自真实统计检验，不得由模型「估算」
- [ ] 随机种子 / 数据版本已记录，保证可复现
