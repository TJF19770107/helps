---
title: GLM-5 技术报告精读（arXiv 2602.15763 全文实读）
type: 论文精读
source: arxiv.org/html/2602.15763v2（HTML 全文，非摘要）
confidence: 高（原文照录，未照录处已标注）
created: 2026-11-02
tags: [GLM-5, 技术报告, 精读, MoE, DSA, RL]
---

# GLM-5 技术报告精读

> **这份和 `GLM-5系列_架构与训练全解.md` 的分工**：
> 那份是「系列总览 + 部署实操」，这份是**论文正文的逐节硬信息**。
> 全文来自 arXiv HTML 版（不是摘要、不是二手解读），关键句保留英文原文。

---

## 零、先把上一轮的一个「未披露」钉死

上一版我写的是：「技术报告**没有披露** FP8 训练的完整范围」。

**现在全文读完了，可以给确定结论：**

| 环节 | 精度 | 原文依据 |
|---|---|---|
| **SFT 阶段** | **INT4 QAT（量化感知训练）** | *"we apply INT4 QAT in the SFT stage"* |
| **RL rollout 推理** | **FP8** | *"GLM-5 uses FP8 for rollout inference to reduce per-token latency"* |
| **中文芯片（Ascend）** | Attention/MLP 用 **W8A8**，MoE 专家压到 **W4A8** | *"standard Attention and MLP blocks use W8A8 (INT8), while the MoE experts are compressed to W4A8 (INT4)"* |
| **预训练主训练** | 正文**未给独立小节** | 只有分布式优化器与并行描述，无可确认的 FP8 主训练表述 |

**关键原话**：

> "we have developed a quantization kernel applicable to both training and offline weight quantization, which ensures **bitwise-identical behavior between training and inference**."

> ⚠️ **这条极其重要**：INT4 QAT 用的 kernel 和推理用的是**同一个**，保证**逐位一致**。
> 这才是 QAT 的真正价值 —— 不是"训练时模拟量化"，是**训练和推理走同一套数值路径**，彻底消除 train-inference mismatch。
> → 对比之下，绝大多数团队的 QAT 是"训练用 fake quant、推理用真 kernel"，两者数值不同，量化后掉点是常事。**这条是工程硬功夫。**

---

## 一、规模与架构（原文数字）

| 项 | GLM-5 | GLM-4.5（对比） |
|---|---|---|
| 总参数 | **744B** | 355B |
| 激活参数 | **40B** | 32B |
| 专家数 | **256** | — |
| 层数 | **80**（刻意减少，压专家并行通信开销） | — |
| 激活占比 | **5.4%** | 9.0% |
| 预训练 token | **28.5T**（Base 27T + mid-training 1.55T） | — |

> **为什么层数反而减少**：`"reduces its layer count to 80 to minimize expert parallelism communication overhead"` ——
> 256 个专家的 EP 通信是主要开销，减层数比减专家更划算。**这是「通信墙」压倒「深度收益」的典型判断。**

### 1.1 注意力：MLA + 两个新东西

| 组件 | 做法 | 解决什么 |
|---|---|---|
| **MLA**（Multi-latent Attention） | 低秩压缩 KV | 省 KV cache |
| **Muon Split** ★新 | 把 up-projection 矩阵（`W^UQ, W^UK, W^UV`）**按头拆成更小矩阵，分别做正交化** | 让不同注意力头以**不同尺度**更新，使 MLA 性能追平 GQA-8 |
| **MLA-256** ★新 | 头维 192 → **256**，头数减 1/3 | 降解码计算量 |

> 原文：*"The method, denoted as Muon Split, enables projection weights for different attention heads to update at different scales."*
>
> **洞察**：MLA 一直有个痛点是"所有头共享同一套投影，梯度尺度一致，头之间难分化"。
> Muon Split 的解法很优雅 —— **不改结构，改优化器的作用粒度**。这是一个「用优化器补结构缺陷」的范例。

### 1.2 MTP：3 层参数共享

- **3 个 MTP 层共享参数**（`"sharing the parameters of 3 MTP layers during training"`）
- 好处：**显存不涨，接受率涨**
- 实测接受长度 **2.76**（DeepSeek-V3.2 是 2.55）
- 工程细节：MTP 输出层与主输出层**放在最后一个 stage 同址**，实现参数共享

> **洞察**：投机解码的加速比 = 接受长度。2.76 意味着平均一次前向能出 2.76 个 token，**理论加速接近 2.76×**（实际受验证开销折损）。
> 而它是靠"共享参数"白拿的 —— **不加参数、不加显存、只改结构位置**。性价比极高的一招。

---

## 二、DSA（DeepSeek Sparse Attention）到底怎么接进来的

### 2.1 核心思想（原文）

> "The core philosophy of DSA is to replace the traditional dense O(L²) attention—which becomes prohibitively expensive at 128K contexts—with a **dynamic, fine-grained selection mechanism**."

> "Unlike fixed patterns (like sliding windows), DSA **'looks' at the content** to decide which tokens are important."

**一句话**：不是"每隔几个看一个"（固定模式），是**看了内容再决定看谁**。

### 2.2 两阶段接入（这是最值钱的工程细节）

| 阶段 | 规模 | 学习率 | 干什么 |
|---|---|---|---|
| **① 稠密预热** | **1000 步**，每步 **14 条 × 202,752 token** | **5e-3** | 让模型先适应超长序列 |
| **② 稀疏适配** | **20B token** | — | 引入稀疏选择，损失尽量小 |

> 原文：*"The warm-up stage goes through 1000 steps with each step trained on 14 sequences of 202,752 tokens and a maximum learning rate of 5e-3. The sparse adaptation stage... goes through 20B tokens."*

**关键判断**：
- 走的是 **Continued Pre-Training（继续预训练）**，不是从零训练 —— 原文：*"This avoided the 'astronomical' cost of training from scratch."*
- 稀疏适配只要 **20B token**，对比 DeepSeek-V3.2 的 943.7B，**省了两个数量级**
- **但必须联合训练补回长上下文能力**，只做适配就交付会掉点

### 2.3 效果与「无损」的准确含义

> *"DSA reduces the attention computation by roughly **1.5-2×** for long sequences... being able to handle 128K contexts at **half the GPU cost**."*

> *"DSA is **lossless by construction**: its lightning indexer achieves token-level sparsity without discarding any long-range dependencies, enabling application to all layers with no quality degradation."*

> ⚠️ **"lossless by construction" 要读准**：它说的不是"精度无损"，是**"不丢弃任何长程依赖"** ——
> 因为 indexer 是**按内容选 top-k（k=2048）**，不是按位置截断。只要关键 token 在 top-2048 里，信息就在。
> **这是一个「注意力预算无损」的声明，不是「模型能力无损」的声明。** 别误读。

---

## 三、后训练：三段 RL + 一个异步框架

### 3.1 流水线

```
多任务 SFT（上下文 202,752，三种思考模式：Interleaved / Preserved / Turn-level）
   ↓
Reasoning RL → Agentic RL → General RL
   ↓
On-Policy Cross-Stage Distillation（防能力回退）
```

> 原文：*"We implemented a sequential Reinforcement Learning pipeline—starting with Reasoning RL, followed by Agentic RL, and finishing with General RL."*
> *"we utilized On-Policy Cross-Stage Distillation throughout this process to prevent catastrophic forgetting"*

**蒸馏优势的写法**（值得抄）：
> `A_hat_{i,t} = sg[log(π_teacher^infer / π_θ^train)]`
> 用**优势项**的 log-ratio 做蒸馏，而不是直接对 logits 做 KL。这样不会把教师的"错误自信"也学过来。

### 3.2 Reasoning RL 的超参（可直接抄）

| 项 | 值 |
|---|---|
| 基础算法 | **GRPO** |
| 训练-推理不匹配处理 | **IcePop** |
| KL 正则 | **去掉**（无 KL） |
| β | **2** |
| ε_low / ε_high | **0.2 / 0.28** |
| on-policy | **全 on-policy** |
| group size | **32** |
| batch size | **32** |
| 覆盖域 | 数学、科学、代码、TIR（工具集成推理） |

### 3.3 ★ DSA 做 RL 的一个致命坑（本案最值钱的一条）

> *"we use **torch.topk** as the default top-k operator in the DSA Indexer in our training engine. We also **freeze the indexer parameters** by default during RL"*

**展开说清楚**：
1. **必须用确定性 top-k**（`torch.topk`）。用非确定性实现（并行/近似 top-k）会导致 **熵骤降 + 性能崩溃**。
2. **RL 期间冻结 indexer 参数** —— 否则 RL 会把检索器带偏，模型学会"选那些让奖励高的 token"而不是"选真正相关的 token"。

> → 这就是 **reward hacking 在架构层面的形态**：不是模型作弊，是**检索器被奖励信号污染**。
> → 通用教训：**任何"学习出来的选择器"（gate/router/retriever），在 RL 里都要考虑冻结或加约束。**

### 3.4 slime 异步框架（GLM-5 的后训练基础设施）

核心：**Multi-Task Rollout Orchestrator** 解耦推理与训练引擎。

| 机制 | 干什么 |
|---|---|
| **>1k 并发 rollout** | 吞吐量 |
| **动态调整任务采样比例** | 自动平衡各任务 |
| **TITO 网关**（Token-in-Token-out） | 消除 re-tokenization 不匹配，**保持动作级精确对应** |
| **Direct Double-sided Importance Sampling** | token 级双侧裁剪 [1-εℓ, 1+εh]，**无需追踪历史策略检查点** |
| **DP-aware routing** | 一致性哈希把同一 rollout 路由到同一 DP rank，**最大化 KV 复用** |
| **样本过滤** | 丢弃 w′−w0 > τ 的过期/噪声样本；环境崩溃样本剔除；组内有效<半数则整组丢弃 |

slime 三大能力：
1. 高度可定制 rollout + 基于 server 的执行
2. 混合精度 + MTP + **PD 分离**（prefill/decode 解耦）提吞吐
3. **heartbeat 驱动的容错** + 路由级 server 生命周期管理

> **洞察**：这套东西的复杂度已经**远超"训练一个模型"**，本质是在建一个**分布式任务调度系统**。
> 唐杰说的"从模型公司变成系统公司"，在这一节里是可以摸到的实物。

### 3.5 关于「RLVR」这个术语

> ⚠️ **原文没有用 "RLVR" 这个词**。对应内容是：可验证环境 + 二元结果奖励。
> 原文：*"we construct verifiable, executable environments that provide grounded feedback for both code-centric and content-generation workflows."*
> *"We assign domain and source-specific judge models or evaluation systems to produce **binary outcome rewards**."*

所以：**RLVR 是社区术语，智谱论文里的说法是「可验证环境 + binary outcome rewards」**。写文章时别混。

---

## 四、训练数据（原文给的确定数字）

| 阶段 | 规模 | 细节 |
|---|---|---|
| **Base 预训练** | **27T tokens** | *"prioritizing code and reasoning early on"*（早期重代码与推理） |
| 代码语料 | — | 模糊去重后**唯一 token +28%** |
| **Mid-training 上下文扩展** | **1.55T** | 三阶段：**32K（1T）→ 128K（500B）→ 200K（50B）** |
| 软件工程数据 | — | **约 1000 万 issue–PR 对**，其中 issue–PR 部分约 **160B 唯一 token** |
| 数据类型 | — | Web（DCLM + World Knowledge 分类器）、Code、Math & Science、长上下文（自然+合成，含 MRCR-like） |

> ⚠️ **原文没有给百分比配比**。任何写"代码占 XX%、数学占 XX%"的说法，都不是这篇论文给的。

**长上下文扩展的节奏值得抄**：32K → 128K → 200K，token 量 1T → 500B → 50B。
**越往后数据越少**，因为长上下文数据本身就稀缺，且每步算力成本剧增。

---

## 五、基准成绩（原文表 7 摘录）

| 基准 | GLM-5 | GLM-4.7 | DS-V3.2 | Kimi K2.5 | Claude Opus 4.5 | Gemini 3 Pro |
|---|---|---|---|---|---|---|
| **HLE** | 30.5 | 24.8 | 25.1 | **31.5** | 28.4 | 37.2 |
| **HLE (w/ Tools)** | 50.4 | 42.8 | 40.8 | **51.8** | 43.4 | 45.8 |
| AIME 2026 I | 92.7 | 92.9 | 92.7 | 92.5 | **93.3** | 90.6 |
| HMMT Feb 2025 | 97.9 | 97.1 | 92.5 | 95.4 | 92.9 | 97.3 |
| GPQA-Diamond | 86.0 | 85.7 | 82.4 | 87.6 | 87.0 | **91.9** |
| LongBench v2 | 64.5 | 59.1 | 59.8 | 61.0 | 64.4 | **68.2** |
| **SWE-bench Verified** | 77.8 | 73.8 | 73.1 | 76.8 | **80.9** | 76.2 |
| **SWE-bench Multilingual** | 73.3 | 66.7 | 70.2 | 73.0 | **77.5** | 65.0 |
| **Terminal-Bench 2.0** | 56.2/60.7 | 41.0 | 39.3 | 50.8 | **59.3** | 54.2 |
| **CyberGym**（漏洞挖掘） | 43.2 | **23.5** | 17.3 | 41.3 | 50.6 | 39.9 |
| BrowseComp | 62.0 | 52.0 | 51.4 | 60.6 | 37.0 | 37.8 |
| **τ²-Bench** | 89.7 | 87.4 | 85.3 | 80.2 | **91.6** | 90.7 |
| **MCP-Atlas** | 67.8 | 52.0 | 62.2 | 63.8 | 65.2 | 66.6 |
| **Vending-Bench 2**（赚钱能力） | **$4,432** | $2,377 | $1,034 | $1,198 | $4,967 | $5,478 |
| GDPval-AA Elo | 1,409 | 1,198 | 1,195 | 1,288 | 1,400 | 1,201 |

**其他关键数字**
- **Artificial Analysis Intelligence Index v4.0 = 50** —— **首个达到 50 的开放权重模型**（GLM-4.7 是 42，+8 分）
- 8 项基准平均提升约 **20%**
- LMArena Text / Code Arena 均为 **开放模型 #1**
- Slide Generation 16:9 合规率 **40% → 92%**，人类评估总胜率 67.5%
- **中文芯片（Ascend Atlas 800T A3 单机）**：单中国节点性能可比双 GPU 国际集群，长序列部署成本降 **50%**

> **读表要点**：
> ① GLM-5 在**开放模型里全面第一**，但**在绝对分数上仍落后 Claude Opus 4.5 / Gemini 3 Pro**（SWE-bench 77.8 vs 80.9/76.2；GPQA 86.0 vs 87.0/91.9）。
> ② **真正的领先项是"开放权重"这个属性本身** + CyberGym（43.2 vs DS-V3.2 的 17.3，接近翻倍）。
> ③ **Vending-Bench 2 的 $4,432 值得单独看** —— 这是"让模型自己开店赚钱"的基准，是**唯一直接测经济价值**的指标。开放模型第一，但仍低于 Claude（$4,967）和 Gemini（$5,478）。

---

## 六、这份报告最值得抄的 6 条工程判断

1. **层数让位于通信**：256 专家 → 减到 80 层。通信墙是真的。
2. **QAT 的 kernel 与推理 kernel 必须同源**，做到 bitwise-identical。否则量化掉点是必然。
3. **稀疏化用继续预训练接入，代价 20B token**，但**必须联合训练补长上下文**，只做适配会掉点。
4. **RL 里冻结 indexer、用确定性 top-k** —— 学习出来的选择器会被奖励污染。
5. **MTP 靠共享参数白拿 2.76 接受长度**，不加显存不加参数。
6. **异步 RL 的复杂度已经是分布式调度系统的量级** —— 这是"系统公司"而非"模型公司"的实证。

---

## 七、诚实边界

- ✅ 全文来自 arXiv HTML（2602.15763v2），非摘要、非二手解读。
- ⚠️ **PDF 原件未下载**：本机沙箱出网全断、香港服务器 22 端口被对端拒绝，客观无法 curl。拿到的是 HTML 全文（内容等价，缺图表矢量原文件）。
- ⚠️ **数据配比百分比、FP8 主训练细节**：原文确实没有，不是我漏看。
- ⚠️ 表格数字为 HTML 解析结果，**表内个别脚注标记（*/†）已在原表注明**，转述时请保留。

---

## 关联
- [[GLM-5系列_架构与训练全解]] — 系列总览与部署
- [[FP8量化技术全景_从SmoothQuant到GLM实践]] — 量化原理
- [[量化_论文精读清单]]
- [[唐杰_演讲思想编年_2019到2026]] — 这些工程选择背后的判断
- [[课程精讲_16周逐周知识卡]] — W3/W7/W11 对应节
