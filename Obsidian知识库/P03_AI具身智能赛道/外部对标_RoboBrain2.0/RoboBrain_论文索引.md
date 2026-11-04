---
title: RoboBrain_论文索引
aliases: [RoboBrain论文, 具身大脑论文, RoboOS论文]
tags: [P03, 具身智能, RoboBrain, 论文, 索引]
created: 2026-11-02
source_type: 公开索引（未下载PDF）
---

# RoboBrain 系列 · 论文索引

> 归属：**智源研究院 BAAI**（FlagOpen）。与唐杰/智谱无关，见 [[RoboBrain全系_具身大脑技术全解]]。
> ⚠️ 本次网络条件下 PDF 不可下，下面给全部 arXiv 号，有梯子可批量补。

## 一、主线（按版本）

| 论文 | arXiv | 年份 | 一句话 |
|---|---|---|---|
| RoboBrain 1.0 | **2502.21257** | 2025 | 统一大脑模型，从抽象到具体的机器人操作；**CVPR 2025** |
| RoboBrain 2.0 Technical Report | **2507.02029** | 2025 | 3B/7B/32B，空间+时序双 SOTA |
| RoboBrain 2.5 | **2601.14352** | 2026 | 《Depth in Sight, Time in Mind》，4B/8B/32B，原生 3D |

## 二、子项目（2.0→2.5 的能力扩展）

| 论文 | arXiv | 年份 | 解决什么 |
|---|---|---|---|
| **Reason-RFT** | **2503.20752** | 2025 | 视觉推理的强化微调，**NeurIPS 2025**，是 2.0 的核心后训练策略 |
| **RoboRefer** | **2506.04308** | 2025 | 空间指代 + 推理 |
| **RoboTracer** | **2512.13660** | 2025 | 原生 3D 空间推理（"Mastering Spatial Trace"） |
| **Robo-Dopamine** | **2512.23703** | 2025 | 通用过程奖励建模（GRM），稠密时序价值估计 |
| **RoboOS** | **2505.03673** | 2025 | 多机器人协同系统 |

## 三、配套框架（非论文，但必知）

| 组件 | 地址 | 作用 |
|---|---|---|
| FlagScale | BAAI Framework 团队 | 分布式训练（Megatron 路线，官方推荐） |
| FlagEvalMM | BAAI FlagEval 团队 | 多模态评测 |
| Qwen3VL finetune | `qwen-vl-finetune` | DeepSpeed 路线备选 |

## 四、评测基准（12 个）

**空间推理 9 个**：BLINK-Spatial、CV-Bench、EmbSpatial、RoboSpatial、RefSpatial、SAT、VSI-Bench、Where2Place、ShareRobot-Bench
**时序 3 个**：Multi-Robot-Planning、Ego-Plan2、RoboBench-Planning

## 五、阅读顺序

```
1. RoboBrain 1.0 (2502.21257)     → 理解"具身大脑"的定义
2. RoboBrain 2.0 (2507.02029)     → 三阶段训练 + 三大能力
3. Reason-RFT (2503.20752)        → 后训练怎么做
4. RoboTracer (2512.13660)        → 3D 空间推理
5. Robo-Dopamine (2512.23703)     → 过程奖励建模
6. RoboBrain 2.5 (2601.14352)     → 最新全貌
```

## 六、诚实边界

- 各版本的**逐项基准分数未拿到**，只有"多数 SOTA / 超过 Gemini 2.5 Pro 等闭源"的定性结论
- 2.0 的 README 已被 2.5 覆盖（原文件标 `RoboBrain2.0 Byebye!`），**2.0 的原始文档需查 `rb_v2.0` 分支**
- RoboBrain-X0-Preview（CoRL 2025，跨本体 VLA）**未见独立 arXiv 号**

## 关联

- [[RoboBrain全系_具身大脑技术全解]]
- [[P03_AI具身智能赛道]]
