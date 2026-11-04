---
title: RoboBrain 全系_具身大脑技术全解（2.0 → 2.5）
aliases: [RoboBrain2.0, RoboBrain2.5, 具身大脑, 机器人空间推理]
tags: [P03, 具身智能, VLA, 机器人, RoboBrain, 空间推理, 外部对标]
created: 2026-11-02
source_type: 公开资料
sources:
  - https://github.com/FlagOpen/RoboBrain2.0
  - https://superrobobrain.github.io/
  - https://arxiv.org/abs/2507.02029
  - https://arxiv.org/abs/2601.14352
  - https://arxiv.org/abs/2505.03673
status: 已核实
owner_line: BAAI 智源研究院（非唐杰/智谱）
---

# RoboBrain 全系：具身大脑技术全解

> ⚠️ **归属澄清（必须写清，不许张冠李戴）**
> RoboBrain 系列是 **北京智源人工智能研究院（BAAI）** 的成果，走 `FlagOpen` 开源品牌。
> **不是唐杰教授、也不是智谱 AI 的项目**。唐杰/智谱在多模态侧对应的是 CogView / CogVideo / GLM-4V / GLM-5.3-Flash。
> 本文件归 **P03 具身智能赛道 · 外部对标线**，与 P15「唐杰蒸馏」并列而非混装。

## 零、最新状态（2026-11-02 核实）

- `FlagOpen/RoboBrain2.0` 仓库 README 顶部已标 **`RoboBrain2.0 Byebye!`**，主线迁到 **RoboBrain 2.5**
- 2.5 已发布 **4B / 8B(两种：NV 与 MT) / 32B**；8B 的 NV 与 MT 是同架构同数据、**不同算力集群**（NVIDIA vs 摩尔线程）训练
- 2.5 技术报告：**arXiv 2601.14352**《RoboBrain 2.5: Depth in Sight, Time in Mind》
- 2.0 技术报告：**arXiv 2507.02029**（BAAI RoboBrain Team）

| 版本 | 基座 | 规格 | 备注 |
|---|---|---|---|
| RoboBrain 1.0 | — | — | CVPR 2025 |
| RoboBrain 2.0 | Qwen2.5-VL | 3B / 7B / 32B | 异构架构：视觉编码器 + LLM 解码器 |
| RoboBrain 2.5 | Qwen3-VL | 4B / 8B(NV/MT) / 32B | 新增原生 3D 空间推理 + 稠密时序价值估计 |
| RoboBrain-X0-Preview | 基于 2.0-3B | — | 跨本体 VLA，CoRL 2025 |

## 一、要解决的三件事（2.0 报告原话归纳）

| 瓶颈 | 现象 | 后果 |
|---|---|---|
| **空间理解不足** | 难以建模物体相对/绝对空间关系，识别不了可操作性（affordance） | 真实场景用不了 |
| **时间建模薄弱** | 对多阶段、跨智能体的时序依赖与反馈理解有限 | 长时序规划与闭环控制做不了 |
| **推理链断裂** | 复杂指令里提不出因果逻辑，无法与动态环境状态对齐 | 泛化到开放任务就崩 |

## 二、架构（2.0）

```
多视图图像 / 长视频 / 自然语言 / 结构化场景图
        ↓
视觉编码器（约 689M 参数，自适应位置编码 + 窗口注意力 + 帧级 token 化 + 多维 RoPE）
        ↓  MLP Projector 投影到语言 token 空间
LLM 解码器（7B / 32B，Qwen2.5-VL 初始化）
        ↓
输出四类：① 自由文本（任务分解、场景图更新）② 空间坐标（点/bbox）
          ③ 推理轨迹（分步决策） ④ 轨迹（未来位姿序列）
```

**多视图处理**：用「视角特定位置标识符」增强，保证跨视角空间一致性——这是它比通用 VLM 强的地方。

## 三、能力矩阵（2.5 延续 2.0 的三大核心）

| 能力 | 具体任务 | 2.5 的新增 |
|---|---|---|
| **交互推理** | 长程规划 + 闭环反馈 | — |
| **空间感知** | affordance 预测、空间指代（spatial referring）、轨迹预测 | **RoboTracer**：原生 3D 空间推理（arXiv 2512.13660） |
| **时序感知** | 未来轨迹估计 | **Robo-Dopamine**：稠密时序价值估计 / 通用过程奖励建模（arXiv 2512.23703） |
| **场景推理** | 实时结构化记忆构建与更新 | 3D 轨迹预测输出 `(x, y, depth)` 三元组 |

## 四、训练三阶段（2.0）

1. **基础时空学习** —— 打空间/时序表征底子
2. **具身时空增强** —— 注入具身场景数据
3. **具身情境推理链训练** —— 长链推理对齐真实任务

后训练核心策略：**Reason-RFT**（NeurIPS 2025，arXiv 2503.20752）—— 视觉推理的强化微调。

## 五、评测成绩（2.0-32B）

多数空间与时序基准达到 SOTA 或接近 SOTA，**超过 Cosmos-Reason1、Qwen2.5-VL 等开源模型，并超过 Gemini 2.5 Pro / o4-mini / Claude Sonnet 4 等闭源模型**。

9 个空间推理基准：BLINK-Spatial、CV-Bench、EmbSpatial、RoboSpatial、RefSpatial、SAT、VSI-Bench、Where2Place、ShareRobot-Bench
3 个时序基准：Multi-Robot-Planning、Ego-Plan2、RoboBench-Planning

> ⚠️ 诚实边界：具体分数没有拿到逐项数字，只有「SOTA/接近 SOTA」的定性结论。要看确切表，需读 arXiv 2507.02029 正文。

## 六、生态四件套（这是它真正的价值）

| 组件 | 作用 | 地址 |
|---|---|---|
| **RoboBrain** | 大脑（感知+推理+规划） | FlagOpen/RoboBrain2.5 |
| **RoboOS 2.0** | 多机器人协同系统（含单机轻量版 `stand-alone` 分支） | FlagOpen/RoboOS，arXiv 2505.03673 |
| **RoboSkill** | 技能商店，技能模块智能匹配、一键适配 | FlagOpen/RoboSkill |
| **FlagScale / FlagEvalMM** | 分布式训练框架 / 多模态评测框架（BAAI 自研） | — |

**部署**：官方提供开箱镜像，"三行指令"部署；FlagRelease 提供多芯片镜像（含 Ascend 版）。

## 七、可直接跑的推理代码（2.5）

```python
from inference import UnifiedInference
model = UnifiedInference("BAAI/RoboBrain2.5-8B-NV")

# 1) 通用 VQA
model.inference("What is shown in this image?", "img.jpg", task="general")

# 2) 视觉定位
model.inference("the person wearing a red hat", "img.jpg", task="grounding", plot=True)

# 3) Affordance 预测（抓取区域）
model.inference("the affordance area for holding the cup", "img.jpg", task="pointing", plot=True)

# 4) 空间指代（"两个杯子之间空位的点"）
model.inference("Identify spot within the vacant space that's between the two mugs",
                "img.jpg", task="pointing", plot=True)

# 5) 3D 轨迹预测 → 输出 [(x1,y1,d1), (x2,y2,d2), ...]
model.inference("reach for the banana on the plate", "img.jpg", task="trajectory", plot=True)
```

训练框架：**Megatron 路线用 FlagScale（官方推荐）**；DeepSpeed 路线兼容 Qwen3-VL 官方 `qwen-vl-finetune`。

## 八、对汤小龙（AI 分身）的用法

1. **赛道3 的"标尺"**：判断「机器人大脑」这个方向做到什么程度了，RoboBrain 就是公开最强基线之一。客户/合作方问「你们用什么大脑」，可以答"对标 RoboBrain 2.5-32B 的能力面"。
2. **能力边界**：它只解决**大脑**（感知+推理+规划），**小脑（运动控制）不含**。谈方案时必须说清「大脑 + 小脑 + 本体」三层，别承诺一体交付。
3. **本机可行性**：4B/8B 版本消费级卡可跑推理；32B 需专业卡。**本机无独显 → 只能读代码、跑不了权重**，如实标注。
4. **接单话术素材**：RoboSkill「技能商店 + 一键适配」这个设计，可直接类比到我们给企业做「技能即服务」的交付形态。

## 关联

- [[P03_AI具身智能赛道]]
- [[唐杰_思维模型卡]]（对照：唐杰走的是 LLM/多模态主线，不走具身）
- [[RoboBrain_论文索引]]
