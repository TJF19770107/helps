---
title: GLM-5_本地部署实操与踩坑
aliases: [GLM5部署, vLLM部署, SGLang部署, 显存计算]
tags: [P15, 部署, 量化, vLLM, SGLang, 实操, 模块1]
created: 2026-11-02
source_type: 官方 README + 工程推算
---

# GLM-5 本地部署实操与踩坑

> ⚠️ **先给结论**：**本机（无独立显卡 / 31.75GB 内存 / E 盘剩 34GB）跑不了 GLM-5 任何版本。**
> 本文的价值是：① 算得清需要什么资源 ② 有卡时能一次跑通 ③ 没卡时知道该走 API。

## 一、先算显存（这步算错，后面全白费）

**公式**（MoE 模型）：
```
显存 ≈ 权重 + KV Cache + 激活/临时区 + 框架开销
```

| 版本 | 精度 | 权重显存 | 最低卡配置 | 现实评价 |
|---|---|---|---|---|
| GLM-5/5.1/5.2/5.3 (744B-A40B) | BF16 | **≈1.49TB** | 8×H200 141G = 1.13TB ❌ 不够 | 需 16×H200 或 8×B200 |
| 同上 | FP8 | **≈745GB** | 8×H200 141G = 1.13TB ✅ 可行 | **这是主流选择** |
| 同上 | FP8 | ≈745GB | 8×H100 80G = 640GB ❌ | 单机八卡 H100 不够 |
| GLM-5.3-Flash (320B-A18B) | FP8 | ≈320GB | 4×H200 或 8×H100 ✅ | 门槛骤降 |
| GLM-5.3-Flash | BF16 | ≈640GB | 8×H100 ✅ 勉强 | — |

**几个容易算错的点**：
1. **MoE 不等于激活参数就是显存** —— 744B 全部专家都得驻留显存，激活 40B 只影响算力
2. **KV Cache 单独算**：`2 × 层数 × 头数 × head_dim × 序列长度 × batch × 精度字节`。202K 上下文时 KV 可能几十 GB
3. **不要按 100% 利用率分配** —— `--gpu-memory-utilization 0.85` 是安全线
4. **FP8 权重不自动意味着 FP8 KV** —— 要单独指定

## 二、标准部署命令（官方 README 原文）

### vLLM
```bash
docker pull vllm/vllm-openai:v0.20.2-cu129   # 或 :v0.20.2（CUDA 13.0）

vllm serve zai-org/GLM-5.1-FP8 \
  --tensor-parallel-size 8 \
  --gpu-memory-utilization 0.85 \
  --speculative-config.method mtp \
  --speculative-config.num_speculative_tokens 3 \
  --tool-call-parser glm47 \
  --reasoning-parser glm45 \
  --enable-auto-tool-choice \
  --chat-template-content-format=string \
  --served-model-name glm-5.1-fp8
```

### SGLang
```bash
docker pull lmsysorg/sglang:v0.5.11          # 或 -cu130

SGLANG_ENABLE_SPEC_V2=1 sglang serve \
  --model-path zai-org/GLM-5.1-FP8 \
  --tp-size 8 \
  --tool-call-parser glm47 \
  --reasoning-parser glm45 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4 \
  --mem-fraction-static 0.85 \
  --served-model-name glm-5.1-fp8 \
  --port 8000 --host 0.0.0.0
```

### 昇腾 NPU
- 支持 vLLM-Ascend / xLLM / SGLang
- 官方文档：`github.com/zai-org/GLM-5/blob/main/example/ascend.md`

## 三、五个已知坑（官方 + 实测）

| # | 坑 | 现象 | 解法 |
|---|---|---|---|
| 1 | **MTP + Tool Call 解析失败** | 开启 MTP 后工具调用报错 | 官方明示：改用 **vLLM main 分支** |
| 2 | **`reasoning_effort` 档位理解错** | GLM-5.2 只接受 `high`/`max`；5.3/5.3-Flash 有 `low`/`high`/`max` | 不传默认 `max`；**跑 benchmark 保持 max** |
| 3 | **`clear_thinking` 默认 false** | 聊天场景思维链残留，回答啰嗦 | 聊天显式传 `clear_thinking=true` |
| 4 | **以为 FP8 权重 = FP8 KV** | 显存算不够 | 单独加 `--kv-cache-dtype fp8` |
| 5 | **按 1.0 利用率分配** | OOM 或抢占 | `--gpu-memory-utilization 0.85` |

## 四、本机现实方案（没卡怎么办）

**我们有 = 没卡。所以只有三条路：**

| 路 | 做法 | 成本 | 适合 |
|---|---|---|---|
| **A. 官方 API** | `docs.bigmodel.cn` / `docs.z.ai`，`glm-5.1` 等模型名 | 按 token（$1/M 输入，$3.2/M 输出） | **首选**，接单交付就用这个 |
| **B. 租卡自建** | 云上 8×H200 按小时 | 约 ¥50-150/小时 | 只在大客户要求私有化时 |
| **C. 小模型本地** | 7B 级模型 + KTransformers CPU 推理 | 0 元，但慢 | 离线演示、学习 |

**切换成本评估**：从 API 切自建，不是改个 URL 的事——要重做部署、压测、监控、容灾。**报价时必须把这部分算进去**。

## 五、API 调用的最小可用代码

```python
from openai import OpenAI
client = OpenAI(api_key="<KEY>", base_url="https://open.bigmodel.cn/api/paas/v4/")

resp = client.chat.completions.create(
    model="glm-5.1",                       # 或 glm-4.6 等
    messages=[{"role": "user", "content": "把这段话压缩成 3 个要点：..."}],
    temperature=0.2,
    max_tokens=1024,
)
print(resp.choices[0].message.content)
```

> 密钥铁律：`<KEY>` 永不进 git、不进聊天记录、不进云端正文。

## 六、部署验收清单（有卡时照这个走）

- [ ] `nvidia-smi` 确认卡数与显存
- [ ] 权重完整性校验（sha256 / 分片数）
- [ ] 起服务，`curl /v1/models` 返 200
- [ ] 跑 **3 个真实业务 prompt**（不是 hello world）
- [ ] 测 **长上下文**（喂 100K token，看是否 OOM）
- [ ] 测 **并发**（10/50/100 并发，看 P95 延迟）
- [ ] 测 **工具调用**（MTP 开/关各一次）
- [ ] 记录基线：首 token 延迟、tokens/s、显存峰值

## 七、诚实的边界

- 上述显存数字是**按参数量推算**，未含 KV Cache 与实际框架开销，**真实需求会更高**
- 本机**未做任何部署实测**（无卡），所有命令来自官方 README，**未逐条验证**
- vLLM 镜像 tag（`v0.20.2-cu129`）是抓取时的版本，随时可能更新

## 关联

- [[GLM-5系列_架构与训练全解]]
- [[FP8量化技术全景_从SmoothQuant到GLM实践]]
- [[交易量化_用GLM做信号与研报]]
