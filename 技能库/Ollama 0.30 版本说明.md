# Ollama 0.30 版本说明

> 发布日期：2026年
> 下载地址：https://ollama.com/download
> 底层引擎：llama.cpp（https://github.com/ggml-org/llama.cpp）

## 概述

Ollama 0.30 版本依托 llama.cpp 优化了运行性能与 GGUF 模型适配性。本次升级优化了苹果芯片专用的 MLX 加速引擎（https://ollama.com/blog/mlx），可在更多硬件设备上兼容运行各类模型。

---

## 一、多显卡性能优化

### NVIDIA 显卡推理速率提升

Ollama 0.30 整合英伟达与 llama.cpp 开发团队的优化方案，NVIDIA 显卡环境下模型吞吐性能最高提升 20%。

- 实测环境：RTX5090 显卡、Gemma 4 26B 模型、Q4_K_M 量化参数。

---

## 二、默认启用 Vulkan，拓宽硬件适配范围

软件默认开启 Vulkan 硬件加速，AMD、Intel 显卡均可原生启用 GPU 运算，无需额外安装厂商专属驱动，开箱即用显卡部署大模型。

---

## 三、新增大量模型兼容

Ollama 0.30 拓展 GGUF 模型生态适配，LFM、Prism 系列模型以及 Unsloth 出品的各类微调模型均可直接运行。

| 模型系列 | Hugging Face 链接 |
|---------|-------------------|
| LFM 模型 | https://huggingface.co/LiquidAI/LFM2-8B-A1B-GGUF |
| Prism 模型 | https://huggingface.co/prism-ml/Bonsai-8B-gguf |
| Unsloth 模型库 | https://unsloth.ai/docs/get-started/unsloth-model-catalog |

---

## 四、本地导入 Hugging Face GGUF 模型步骤

1. 下载单个 GGUF 模型文件或存放模型文件的文件夹；
2. 新建 Modelfile 文件，填写本地模型路径：

```
FROM ./my-model.Q4_K_M.gguf
```

3. 执行命令生成并启动自定义模型：

```bash
ollama create -f Modelfile my-model
ollama run my-model
```

---

## 五、代码智能体与助手对接功能

只要模型原生支持工具调用，Ollama 可直接继承该能力，单条命令对接多款智能助手：

| 助手 | 命令 |
|------|------|
| Claude 代码助手 | `ollama launch claude --model my-model` |
| Hermes 智能体 | `ollama launch hermes --model my-model` |
| OpenClaw 工具 | `ollama launch openclaw --model my-model` |

查询模型是否支持工具调用指令：

```bash
ollama show my-model
```