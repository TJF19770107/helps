---
name: "六端空间归位"
description: "把每一轮产物按内容自动归位到 P01~P13 十三个知识库空间，并刷新索引导航、写可审计台账。当任务涉及：产物归位、P01~P13、知识库空间、六端一一对应、每轮实时落、导航索引刷新、产物台账、GitHub/CNB 建 13 空间时使用。"
subject: 方法·知识库空间归位
belongs_to: 汤小龙 v3.0
version: v1.0.0
updated_at: 2026-10-24
owner: 汤小龙
trigger:
  - "产物归位 / 归位到 Pxx / 知识库空间"
  - "P01~P13 / 13 个空间 / 六端一一对应"
  - "每轮实时落 / 收尾归位 / 刷新索引"
  - "GitHub CNB 建空间"
---

# 六端空间归位

把「产物平铺在工作区根、13 个空间只有导航页」变成「每轮产物自动落进对应 Pxx 空间」。

## 一、13 个空间（本地正本）

根：`E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\`

| 编号 | 目录 | 放什么 |
|---|---|---|
| P01 | `P01_企业微信群定制接单项目` | 企微群定制接单、31 群、一人公司接单系统 |
| P02 | `P02_黄金黑马策略` | XAUUSD H4 / MT5 EA |
| P03 | `P03_AI具身智能赛道` | 机器人 / VLA / 仿真 |
| P04 | `P04_网盘课程资源知识萃取与沉淀体系建设` | 课程萃取、赛博书屋 |
| P05 | `P05_闲鱼自动化系统` | 闲鱼、拼豆图纸 |
| P06 | `P06_定时任务（3个自动化目录）` | 定时任务 / 调度 |
| P07 | `P07_博主学习库（D盘+E盘）` | 博主 / 对标账号 |
| P08 | `P08_赛事预测分析系统` | 体育赛事预测 |
| P09 | `P09_量化策略资产` | vnpy / backtrader / freqtrade / qlib 精读 |
| P10 | `P10_技能库` | 全部 SKILL.md 与脚本 |
| P11 | `P11_我的黑马策略` | 币安侧：K线、策略、回测、风控 |
| P12 | `P12_三赛道工作台` | 黑马量化 / 具身智能 / 接单交付 工作台 |
| P13 | `P13_小说20261018` | 小说总纲 / 细纲 / 伏笔 / 章节 |

## 二、三条命令

```bash
# 1) 记本轮清单（--auto 自动判归属，--space Pxx 强制指定）
python space_router.py --record --auto 报告.md 脚本.py

# 2) 收尾落地（落位 + 刷新索引）
python space_router.py --round

# 3) 只重建 13 个空间的索引段
python space_router.py --reindex
```

辅助：

```bash
python space_router.py --explain 文件.md     # 只解释归属判定，不落盘
python space_router.py --list-spaces          # 看 13 空间与关键词
python space_router.py --scan <目录> --since 12   # 扫最近 N 小时新产物
python ensure_space_dirs.py --dest <落点>      # 在 GitHub/CNB 侧建齐 13 个空间入口
```

双击入口：`本轮收尾_空间归位.cmd`

## 三、落位规则

- 目标：`<Pxx>/02_产物归档/YYYYMMDD/<原文件名>`
- **文档类**（md/html/pdf/docx/xlsx/pptx/txt）→ 复制进产物归档 + 进索引表
- **代码类**（py/js/sh/ps1/json/yaml…）→ **只登记不复制**（技能库有正本，复制 = 双份漂移）
- 同名不同内容 → 加 `_HHMMSS` 后缀，**绝不覆盖**
- 源文件默认**不删**（`--move` 才移动）

## 四、幂等与审计

- 台账：`Obsidian知识库\_空间归位台账.jsonl`（追加写，含 `sha256 / source / target / status / note`）
- 同一 sha256 + 同一空间 → `skipped-dup`，重复跑不会产生副本
- `--force` 可强制重放（谨慎）

## 五、导航页改写边界（硬约束）

- 只允许改 `<!-- 产物索引:auto:begin -->` 与 `<!-- 产物索引:auto:end -->` 之间
- 原换行符必须保持（CRLF/LF 不转换）
- 段外内容一字不动 —— 导航是六端同源单份

## 六、踩过的坑

| # | 坑 | 症状 | 修法 |
|---|---|---|---|
| 1 | `--explain` 多文件合并判定 | 三个不相关文件打平、结论看不出 | 改成逐文件判定 |
| 2 | 代码类也复制 | 知识库里出现 .py 第二份，两边内容漂移 | 加 `REGISTER_ONLY` 只登记 |
| 3 | 直接整篇重写导航 | 六端导航被机器覆盖，人工改的内容全丢 | 只替换 auto 段 |

## 七、与五步法的关系

第 5 步「沉淀」的两个必做动作：

```
5.1 space_router.py --record --auto <本轮产物>
5.2 space_router.py --round
```

**归位失败 = 本轮未完成**，不许写「已交付」。

## 八、云端对应（2026-10-24 建成）

| 端 | 落点 | 验证 |
|---|---|---|
| GitHub | `my-ai-clone` → `_六端同步/lobster-knowledge-base/P01~P13` | `git ls-tree -r origin/main` 数出 13 目录 + 26 入口 |
| CNB | `orca-quant-binance` → `六端知识库/P01~P13` | 同上 |

两处都是 13 目录 × (README.md + 00_本区导航.md) = 26 文件。
