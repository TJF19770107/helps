---
title: GLM-5 系列架构与训练全解
aliases: [GLM-5技术报告精读, GLM5架构, 智谱旗舰模型]
tags: [P15, 大模型, GLM, 智谱, 唐杰, MoE, DSA, 强化学习, 模块1量化]
created: 2026-11-02
source_type: 公开资料
sources:
  - https://github.com/zai-org/GLM-5
  - https://arxiv.org/abs/2602.15763
  - https://arxiv.org/abs/2603.12201
  - https://z.ai/blog/glm-5.2
  - https://z.ai/blog/glm-5.3
status: 已核实
---

# GLM-5 系列架构与训练全解

> 归属：**智谱 AI（Z.ai）· 清华 KEG 联合团队**，通讯作者含 **唐杰（Jie Tang）**。
> 技术报告：arXiv **2602.15763**《GLM-5: from Vibe Coding to Agentic Engineering》（2026-02-17 v1，02-24 v2）。
> 代码/权重：`github.com/zai-org/GLM-5`，MIT License。

## 一、四代同堂：版本差异一张表

| 版本 | 发布时间 | 总参/激活 | 基座 | 预训练数据 | 关键突破 |
|---|---|---|---|---|---|
| **GLM-5** | 2026-02-11 | 744B / 40B | 全新 | 28.5T | 引入 DSA 稀疏注意力；slime 异步 RL；Agentic 工程 SOTA |
| **GLM-5.1** | 2026-04-07 | 744B / 40B | 同 GLM-5 | 28.5T | 长程不早衰（hundreds of rounds / thousands of tool calls）；SWE-Bench Pro 58.4 |
| **GLM-5.2** | 2026-06-22 | 744B / 40B | 同 5.1 | — | **IndexShare**（1M 上下文每 token FLOPs 降 2.9×）；稳定 1M 上下文；MTP 接受长度 +20% |
| **GLM-5.3** | 2026-08 | 744B / 40B | **同 5.2（全提升来自后训练）** | — | 编程 +50%（Z.ai Code Bench）；CyberGym 漏洞挖掘 SOTA |
| **GLM-5.3-Flash** | 2026-08-27 | 320B / 18B | 全新训练 | 30T 多模态 | **GLM 首例稀疏+线性注意力混合架构**；mHC 流形约束超连接 |

**面试级要点**：GLM-5.3 和 GLM-5.3-Flash 是两条完全不同的路——5.3 是「后训练榨干老基座」，Flash 是「重造架构换效率」。

## 二、MoE 配置

- 总参数 **744B**，激活 **40B**（上一代 GLM-4.5：355B / 32B，激活占比从 9% 降到 5.4%）
- **256 个专家**，**80 层**（对比 GLM-4.5 更少层数，刻意压低专家并行通信开销）
- 训练语料：起步 **27T**，代码与推理优先；模糊去重后代码唯一 token **+28%**；总预算 **28.5T**

## 三、DSA（DeepSeek Sparse Attention）怎么接进来的

**核心问题**：传统注意力 O(L²)，长上下文成本爆炸；实测 **约 90% 的长上下文注意力条目是冗余的**。

**做法**：加一个轻量 **indexer**，先检索出 top-k 最相关的 KV 条目，只在这个子集上算注意力（内容驱动的动态细粒度选择，区别于滑动窗口这类固定模式）。

**关键工程选择——不从零训，靠继续预训练迁移**：
1. **稠密 warm-up**：1000 步，每步 14 条 × 202,752 token 序列，峰值学习率 5e-3
2. **稀疏适配**：仅 **20B token**（对比 DeepSeek-V3.2 的 943.7B，省了两个数量级）

**代价与验证**（这个细节最值钱）：
- 小型验证（GLM-4.7-Flash）：warm-up 后 128K RULER 从 **79.21 掉到 71.35**（掉点明显）
- 联合训练 150B token 后：4K–64K 全面反超基线，128K 只差 **0.35**
- → **结论：稀疏化会先掉长上下文能力，必须靠联合训练补回来，不能只做适配就交付**

**长上下文对比（MLA vs DSA）**：

| 基准（128k） | MLA | DSA |
|---|---|---|
| MQ-NIAH | 100.0 | 100.0 |
| MV-NIAH | 95.5 | **97.0** |
| SQuAD | 79.7 | **86.0** |
| HotpotQA | 66.3 | 63.0 |

长序列注意力计算减少 **1.5–2×**，128K 上下文 GPU 成本**减半**。

## 四、低精度与量化（模块1 核心）

> ✅ **2026-11-02 更新（已读 arXiv HTML 全文，本条从「未披露」升级为「已确认」）**：
> 技术报告正文**没有独立的「FP8 主训练」小节** —— 这是原文事实，不是漏看。
> 训练侧的低精度方案是 **INT4 QAT（用在 SFT 阶段）**；FP8 只出现在 **RL rollout 推理** 与 **中文芯片量化** 两处。
> 完整对照表与原文引证见 [[GLM-5_技术报告精读_官方全文版]] 第零节。

**报告里确认的**：
1. **INT4 QAT（量化感知训练）用于 SFT 阶段** —— 开发了训练与离线权重量化**共用量化内核**，保证训练与推理**逐位一致（bit-exact）**。这是「训推一体量化」的关键设计，避免 QAT 训完再转推理时精度漂移。
2. **推理侧 FP8 rollout** —— 降低单 token 延迟、缩短长轨迹完成时间（在 RL 里直接决定单位时间能采多少条轨迹）。

**工程侧确认的（来自 README / 部署文档）**：
- 全系发布 **BF16 与 FP8 双精度权重**，FP8 是官方一等公民而非社区魔改
- 显存换算：744B BF16 ≈ **1.49TB**，FP8 ≈ **减半（约 745GB）**
- vLLM 启动样例：`--tensor-parallel-size 8 --gpu-memory-utilization 0.85 --speculative-config.method mtp --speculative-config.num_speculative_tokens 3 --tool-call-parser glm47 --reasoning-parser glm45`
- SGLang 启动样例：`--tp-size 8 --speculative-algorithm EAGLE --speculative-num-steps 3 --speculative-eagle-topk 1 --speculative-num-draft-tokens 4 --mem-fraction-static 0.85`
- ⚠️ 已知坑：MTP 开启时 Tool Call Parse 失败 → 改用 vLLM main 分支

**2026-11-02 全文补全的部分**（原「还没拿到」的项，现已从 HTML 全文确认）：
- ✅ **中文芯片（Ascend Atlas 800T A3）**：Attention/MLP 用 **W8A8（INT8）**，MoE 专家压到 **W4A8（INT4）**；单中国节点性能可比双 GPU 国际集群，长序列部署成本降 **50%**
- ✅ **QAT 的 kernel 与推理 kernel 同源**，原文原话 *"ensures bitwise-identical behavior between training and inference"*
- ❌ 仍无：FP8 主训练的 per-tensor/per-block scaling 方案（原文确实没有此节）、KV cache FP8 的精度影响（原文未展开）

→ 详见 [[FP8量化技术全景_从SmoothQuant到GLM实践]]

## 五、slime：异步 RL 基础设施（GLM-5 真正的地基）

仓库：`github.com/THUDM/slime`（微调需 v0.3.0+）

**架构**：训练引擎与推理引擎**部署在不同 GPU**，彻底解耦

```
推理引擎 ──持续生成轨迹──> 缓冲区 ──累积到阈值──> 训练引擎
    ↑                                                  │
    └────── 每 K 次梯度更新，新权重同步回推理引擎 ──────┘
            （每次同步后【重置优化器】）
```

**五个工程细节**：
1. **多任务 Rollout**：Multi-Task Rollout Orchestrator，各任务作为独立微服务注册，统一为 message-list 表示，支持 **1000+ 并发 rollout**
2. **尾延迟优化**：多节点 DP-attention 免排队服务（EP64/DP64、8 节点）；FP8 + MTP；PD 分离避免 prefill/decode 互相干扰
3. **容错**：心跳驱动，故障服务器自动摘除并重路由
4. **DP-aware 路由**：一致性哈希把同一 rollout 的请求固定到同一 DP rank，最大化 KV 复用
5. **DSA 下的 RL**：用确定性 `torch.topk`（k=2048），**默认冻结 indexer 参数**（避免 RL 把检索器带偏）

## 六、异步 Agent RL 算法（比架构更值得学）

| 机制 | 做法 | 解决什么 |
|---|---|---|
| 组式策略优化 | 每问题采样 K 条轨迹，**只优化模型生成的 token**，环境反馈不计 loss | 防止把环境输出当模型输出学 |
| **TITO 网关** | 保留精确 token ID 与元数据 | 避免重分词导致 token 错位（长轨迹必踩） |
| **直接双边重要性采样** | r_t = π_θ/π_rollout，**丢弃 π_old**，信任域 [1−εℓ, 1+εh]，区间外 token 全屏蔽 | 异步带来的策略滞后 |
| 过时样本丢弃 | w′−w₀>τ 即弃；环境崩溃样本剔除；有效样本过半则重复补齐，否则整组丢 | 异步数据陈旧 |
| 异步 agent RL | 从复杂长程交互中学习 | 单轮 RL 学不会长程 |

## 七、基准成绩（GLM-5，可直接引用）

| 基准 | GLM-5 | 参照 |
|---|---|---|
| HLE / 带工具 | 30.5 / **50.4** | GPT-5.2 HLE 35.4 |
| AIME 2026 / HMMT Feb / Nov | 92.7 / 97.9 / 96.9 | |
| GPQA-Diamond | 86.0 | |
| SWE-bench Verified / Multilingual | **77.8** / 73.3 | Claude Opus 4.5 为 80.9 |
| Terminal-Bench 2.0 | 56.2 | |
| BrowseComp / 带上下文管理 / ZH | 62.0 / 75.9 / 72.7 | |
| τ²-Bench / MCP-Atlas | 89.7 / 67.8 | |
| Vending-Bench 2 | **$4,432**（开源第一） | 跑一年模拟售货机生意 |
| GDPval-AA Elo | 1,409 | |

**GLM-5.2 对比 GLM-5.1**：Terminal-Bench 2.1 **81.0 vs 62.0**；SWE-bench Pro **62.1 vs 58.4**；距 Claude Opus 4.8（85.0）只差几个点。

## 八、IndexShare（GLM-5.2 的架构创新，arXiv 2603.12201）

- 每 **4 个稀疏注意力层复用同一个 indexer**
- 1M 上下文下每 token FLOPs 降 **2.9×**
- MTP 层改进使投机解码接受长度最高 **+20%**
- → 这条路线和 DSA 叠加，是「超长上下文 + 低成本服务」的组合拳

## 九、对汤小龙（AI 分身）的用法

1. **接单讲方案时**：客户问「国产模型能不能打」→ 直接引用 SWE-bench 77.8 / Vending-Bench $4,432 / Terminal-Bench，比空谈"国产崛起"有力。
2. **本地部署评估**：744B 需要 8×H100 级（TP=8，FP8 约 745GB 显存）；**我们本机无独显，只能走 API 或租卡**，不要把 744B 当本地方案。
3. **小模型落地选型**：真要本地跑，看 **GLM-5.3-Flash（320B-A18B，FP8）**仍不现实；实际可用的是 GLM-4.x 系列或调用 bigmodel API。
4. **写技术方案引用架构时**：DSA 的「warm-up 掉点 → 联合训练补回」这段是最好的「工程诚实性」素材，证明方案不是 PPT。

## 关联

- [[FP8量化技术全景_从SmoothQuant到GLM实践]]
- [[量化_论文精读清单]]
- [[GLM-5_本地部署实操与踩坑]]
- [[唐杰_思维模型卡]]
- [[课程总览_16周大纲]]
