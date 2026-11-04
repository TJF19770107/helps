---
title: 本地PDF与源码索引
aliases: [原始资料索引, PDF清单, 仓库快照]
tags: [P15, 存档, PDF, GitHub, 原始资料]
created: 2026-11-02
updated: 2026-11-02
source_type: 本地实下载（非索引页）
---

# 本地 PDF 与源码索引

> **这一份不是"链接清单"，是真文件清单。** 每个都验过字节数与文件魔数，能直接双击打开。
> 全部下载于 2026-11-02，走「空 ProxyHandler 绕死代理」通道。

## 一、arXiv PDF 原件（5 篇 / 22,247,016 B ≈ 22.2 MB）

**P15（量化 · 课程 · 对齐）**

| 论文 | arXiv | 大小 | 本地文件 | 为什么收 |
|---|---|---|---|---|
| **GLM-5 Technical Report** | 2602.15763 | **6,177,650 B** | `pdf/GLM-5_Technical_Report__2602.15763.pdf` | 智谱最新旗舰，MoE 744B-A40B + DSA + slime；精读见 [[GLM-5_技术报告精读_官方全文版]] |
| **Chinchilla**（Training Compute-Optimal LLMs） | 2203.15556 | **6,004,349 B** | `pdf/Chinchilla_Training_Compute-Optimal_LLMs__2203.15556.pdf` | scaling law 的**原始出处**，HW3 的理论依据；20 tokens/param 就是这篇定的 |
| **DPO**（Direct Preference Optimization） | 2305.18290 | **1,299,212 B** | `pdf/DPO_Direct_Preference_Optimization__2305.18290.pdf` | HW4 三路对照里的第二路，RLHF 的免强化学习替代 |
| **SmoothQuant** | 2210.17323 | **521,818 B** | `pdf/SmoothQuant_Accurate_and_Efficient_Post-Training_Quantization__2210.17323.pdf` | W8A8 的经典解法，见 [[FP8量化技术全景_从SmoothQuant到GLM实践]] |

**P03（具身智能 · 外部对标）**

| 论文 | arXiv | 大小 | 本地文件 |
|---|---|---|---|
| **RoboBrain 2.5 Technical Report** | 2601.14352 | **8,243,987 B** | `P03_AI具身智能赛道/外部对标_RoboBrain2.0/pdf/RoboBrain2.5_Technical_Report__2601.14352.pdf` |

> ⚠️ **注意版本**：`RoboBrain2.0` 仓库已改名为 `RoboBrain2.5`，官方 README 顶部写着 `RoboBrain2.0 Byebye!`。
> 收到的是 **2.5** 的技术报告（4B/8B/32B）。2.0 的存档见 [[RoboBrain全系_具身大脑技术全解]]。

**验收方式**：不是看文件名，是读前 5 字节 —— 全部 `%PDF-` 才算真下到。

## 二、GitHub 源码快照（11 个文件 / 约 100 KB）

**zai-org/GLM-5**（7,420 stars，默认分支 main）

| 文件 | 大小 | 用途 |
|---|---|---|
| `README.md` | 15,185 B | 主文档：规格表 / 部署命令 / benchmark |
| `README_zh.md` | 14,621 B | 中文版，术语对照用 |
| `LICENSE` | 11,343 B | **MIT** —— 商用无限制，接单可以直接交付 |
| `requirements.txt` | 58 B | 依赖极简（只是 OpenAI SDK 类） |
| `example/ascend.md` | 3,147 B | **昇腾 NPU 部署**，国产芯片替代路径 |
| **`skills/glm-master-skill/SKILL.md`** | **7,061 B** | ★ 智谱**官方技能目录**，14 个可直接接单的技能 —— 见 [[智谱官方技能目录_接单弹药]] |

**FlagOpen/RoboBrain2.5**（默认分支 main）

| 文件 | 大小 | 用途 |
|---|---|---|
| `README.md` | 19,461 B | 2.5 全系说明（4B/8B/32B + RoboTracer + Robo-Dopamine） |
| `LICENSE` | 11,357 B | Apache-2.0 |
| `inference.py` | 11,940 B | 根目录推理入口 |
| `requirements.txt` | 4,588 B | 依赖清单 |
| `rb_v2.0/requirements_rb2.txt` | 4,706 B | 2.0 兼容版依赖 |

另有 `_repo_meta.json` / `_tree.txt`（仓库元信息与完整文件树），可离线判断某文件是否真的存在。

## 三、没下的（诚实记录）

| 项 | 为什么没下 |
|---|---|
| 完整 `git clone` | 仓库含权重索引与大量图片，几百 MB；本机带宽 ~240 B/s（raw 通道实测），不现实。需要时用 `git clone --depth 1 --filter=blob:none` |
| `resources/*.png`（10 张 benchmark 图） | 图不参与推理，需要看分数直接读 README 里的表 |
| GLM-OCR / GLM-Image / GLM-V 三个仓库的 SKILL.md | 只有目录，**未安装**。要装走 `npx clawhub@latest install <skill-name>` |

## 四、通道教训（这条比文件值钱）

**同一个 GitHub 仓库，两条通道速度差 77 倍：**

| 通道 | 15 KB 的 README.md | 结论 |
|---|---|---|
| `raw.githubusercontent.com`（CDN） | **63 秒**，大文件直接 `TimeoutError` | 本机极慢，只能兜底 |
| `api.github.com/repos/{o}/{r}/contents/{path}` | **815 毫秒** | ✅ **首选**，返回 base64 |

> ⚠️ 上一轮把这 8 个文件的失败**误判成 404** —— 因为脚本 `except` 里只写了 `FAIL`，把错误信息丢了。
> **教训：失败分支必须落错误原文**，否则"没下到"和"不存在"分不清，会得出完全错误的结论。

**API 限流**：未认证 60 次/小时。本脚本 11 次请求，跑前先查 `/rate_limit`。

## 五、复现命令

```bash
# 1. PDF 批量补（含 arXiv）
python _tools/fetch_papers_repos.py

# 2. GitHub 文件补（contents API，快 77 倍）
python _tools/fetch_github_api.py --dry   # 先看要下什么
python _tools/fetch_github_api.py
```

两个脚本都已内置「空 ProxyHandler 绕死代理」，不需要先关系统代理。

## 关联

- [[00_🗺️P15总索引_MOC]] — 回总索引
- [[GLM-5_技术报告精读_官方全文版]] — PDF 的正文精读
- [[量化_论文精读清单]] — 这 4 篇 PDF 的读法与要点
- [[智谱官方技能目录_接单弹药]] — 官方 SKILL.md 的接单映射
