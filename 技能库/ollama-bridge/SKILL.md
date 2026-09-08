---
name: "ollama-bridge"
description: "让 WorkBuddy / 任意 Agent 调用本地 Ollama 模型（localhost:11434）做免费/离线/隐私推理。适用于轻量任务、MiMO 宕机时的热备、敏感数据本地处理。支持 gemma4:e4b 等本地模型。当用户说'用本地模型/离线跑/Ollama'时激活。"
version: "1.0"
date: "2026-07-14"
author: "WorkBuddy + 龙虾AI主控中心"
tags: ["ollama", "local", "免费", "热备", "gemma"]
primary_path: "~/.workbuddy/skills/ollama-bridge/SKILL.md"
shared_path: "E:/龙虾AI主控中心/我的AI分身/技能库/ollama-bridge/SKILL.md (待镜像)"
---

# Ollama Bridge — 本地免费推理

> **目的**：零成本、零外网依赖的推理后备。MiMO 宕机/到期时舰队不至于停摆。
> **端点**：`http://localhost:11434/v1`（OpenAI 兼容）| **模型存储**：`E:\Ollama\models`

---

## 一、何时激活本技能

- 不想花任何 Token/积分的轻量任务（摘要、分类、简单生成）
- MiMO 宕机 / 到期时的**热备**
- 隐私敏感数据（不出本机）
- 本地小模型能胜任的简单任务

---

## 二、端点与命令

| 操作 | 命令 |
|------|------|
| 列出模型 | `ollama list` 或 `curl http://localhost:11434/v1/models` |
| 对话生成 | `POST http://localhost:11434/v1/chat/completions` |
| 拉取模型 | `ollama pull <name>` |
| 本地注册 GGUF | `ollama create <name> -f Modelfile` |

---

## 三、当前已装模型（实测）

```
qwen3.5:2b | qwen3:0.6b | gpt-4o-mini | minimax-m2.7:cloud | kimi-k2.6:cloud
```

---

## 四、gemma4:e4b 状态（重要·已核实）

⚠️ **当前本机未注册 gemma4:e4b**：
- Ollama 清单无此模型
- `E:\Ollama\models\gguf\` 为空，blobs 中无 gemma 权重
- 全盘（E/G）无 `.gguf` / `.safetensors` 权重文件

✅ **历史证据**：Marvis 备份（`backup_20260622`）里有 `gemma4_e4b_optimization_final_report.md` 和 `ollama_gemma4_adapter.py`，证明你曾成功装过并做过 Codex 适配。

🔧 **恢复方式二选一**：
1. **重新拉取**（联网下载，约数 GB）：`ollama pull gemma4:e4b`
2. **本地注册**（若有 GGUF 文件，免下载）：
   ```bash
   # Modelfile 内容：FROM 指向本地 .gguf 绝对路径
   echo 'FROM E:/path/to/gemma4-e4b.gguf' > Modelfile
   ollama create gemma4:e4b -f Modelfile
   ```

> 你之前说"不要重复拉取"——但本机已无该模型文件，若没有本地 GGUF，只能重新拉取。请确认你手头是否有 GGUF，或有授权我执行 `ollama pull`。

---

## 五、调用示例

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.5:2b","messages":[{"role":"user","content":"总结这段日志"}],"stream":false}'
```

---

## 六、关联技能

| 技能 | 关系 |
|------|------|
| `mimo-bridge` | 主引擎（联网、强推理） |
| `多智能体舰队编排` | 整体舰队架构与路由 |
