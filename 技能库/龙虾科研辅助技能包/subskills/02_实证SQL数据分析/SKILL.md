---
name: 龙虾实证SQL数据分析
description: duckdb 本地零积分跑描述性统计/分组聚合/复现验证，三级降级保证能跑。禁止书写脚本未产出的统计量。
version: 1.0
parent: 龙虾科研辅助技能包
lobster:
  cost_mode: zero-credit
  触发词: [SQL分析, 实证分析, 跑数据, 描述性统计, 分组统计, 回归数据, 复现性验证]
allowed-tools: Read, Bash(G:/g_venv_ars/Scripts/python.exe *)
---

# 2. 实证 SQL 数据分析（自研）

## 用途
本地实跑真实数据，产出可复现的统计结果。**负责"算出来"，不负责"解读成结论"。**

## 触发指令
```
SQL分析：对 data/raw.csv 按年份求均值与样本量
跑数据：复现论文 Table 3 的描述性统计
```

## 执行步骤
1. **确认数据**：路径、分隔符、编码（中文常见 utf-8-sig/GBK）、缺失值标记
2. **跑脚本**：
   ```bash
   G:/g_venv_ars/Scripts/python.exe scripts/lobster_sql_query.py \
     --table main="E:/path/data.csv" \
     --sql "SELECT grp, COUNT(*) n, ROUND(AVG(score),2) m FROM main GROUP BY 1" \
     --out result.csv --show 50
   ```
   duckdb 主路径（直读 CSV/Parquet）→ stdlib sqlite 自动降级；仅放行只读查询
3. **复现留痕**：SQL + 输出文件一并归档
4. **解读**：显著性/效应量必须来自真实检验；**禁止**输出脚本未产出的数字

## 已知坑（实测）
- 保留字列名（如 `group`）必须加双引号 `"group"`
- 大表先 `--out` 落盘再回读摘要，不要把整表塞进上下文

## token 预估
| 模式 | 预估 |
|------|------|
| 纯脚本分析（默认） | **≈ 1–2k** |
| 分析+解读 | ≈ 4–5k |

## 人工核验点
- [ ] 论文中每个数字都能在脚本输出中定位
- [ ] 样本量口径、缺失值剔除规则由人工确认
- [ ] 随机种子/数据版本已记录
