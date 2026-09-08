---
name: "mimo-bridge"
description: "让 WorkBuddy / 任意 Agent 直接调用小米 MiMO V2.5 Pro API 或本地 Ollama 做推理，绕过 Hy3 积分消耗。适用于需要低成本长程推理、量化代码生成、Agent 自主多步执行、本地免费热备的场景。当用户说'用 MiMO 跑/分析/生成'或'用本地模型/离线跑/Ollama'时激活。"
version: "1.2"
date: "2026-07-29"
author: "WorkBuddy + 龙虾AI主控中心"
tags: ["mimo", "ollama", "bridge", "省钱", "api", "本地模型", "热备", "量化"]
primary_path: "~/.workbuddy/skills/mimo-bridge/SKILL.md"
shared_path: "E:/龙虾AI主控中心/我的AI分身/技能库/mimo-bridge/SKILL.md (待镜像)"
agent_created: true
updated: "2026-07-29"
merged_from: "ollama-bridge V1.0 (deprecated)"
---

# MiMO Bridge — 本地/远程 LLM 统一网关

> **目的**：把"重推理"从 WorkBuddy(Hy3) 的积分账单上摘下来，改走你已付费的 MiMO Token Plan；同时把本地 Ollama 作为零成本热备，形成统一入口。
> **核心引擎**：MiMO V2.5 Pro | **本地端点**：Ollama `http://localhost:11434/v1`

---

## 一、何时激活本技能

- 用户明确要求"用 MiMO 跑 / 分析 / 生成 / 回测"，或"用本地模型 / 离线跑 / Ollama"
- 任务需要 **长上下文(1M)**、**低成本 Token**、**Agent 自主多步工具调用**
- MiMO 链路健康（CC-Switch:15721 → AI Code Switch:4567 → MiMO:18808 通）
- 需要零成本/隐私敏感/离线场景的轻量推理后备

---

## 二、统一模型选择决策树

```
任务来了
  ├─ 要求明确"用 MiMO"？        → 走 MiMO V2.5 Pro（第三章）
  ├─ 要求"本地模型/离线/Ollama"？ → 走 Ollama（第四章）
  ├─ 长上下文 / 复杂代码 / Agent 多步 → 首选 MiMO
  ├─ 零成本 / 隐私敏感 / 轻量摘要    → 首选 Ollama
  └─ MiMO 不可用？                → 自动切 Ollama（第五章）
```

| 场景 | 推荐引擎 | 预期成本 | 速度 | 隐私 |
|------|---------|---------|------|------|
| 长程 Agent 任务 / 量化代码生成 | MiMO V2.5 Pro | 极低（Token Plan） | 中 | 出本机 |
| 轻量摘要、分类、简单生成 | Ollama qwen3.5:2b | 0 | 快 | 本地 |
| MiMO 401/宕机/到期 | Ollama 任意可用模型 | 0 | 看模型 | 本地 |
| 隐私敏感数据 | Ollama | 0 | 看模型 | 本地 |

---

## 三、MiMO 远程引擎

### 3.1 端点与鉴权

| 项 | 值 |
|----|---|
| Base URL | `https://token-plan-cn.xiaomimimo.com/v1` |
| 模型名 | `mimo-v2.5-pro` |
| 本地代理端口 | `18808`（CC-Switch 中转后） |
| 鉴权头 | `Authorization: Bearer $MIMO_API_KEY` |

**获取 API Key（不要硬编码到脚本）**：
- 从你的 CC-Switch / AI Code Switch 配置文件读取
- 或设置环境变量 `MIMO_API_KEY`（推荐）
- 位置参考：`E:\龙虾AI主控中心\我的AI分身\CODEX量化策略20260615\嘉盛\黄金黑马策略\Doc\` 下的链路排障报告

### 3.2 调用示例（curl）

```bash
curl https://token-plan-cn.xiaomimimo.com/v1/chat/completions \
  -H "Authorization: Bearer $MIMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [{"role":"user","content":"帮我写一个双均线黄金策略回测代码"}],
    "max_tokens": 4096,
    "temperature": 0.3
  }'
```

### 3.3 调用示例（Python，推荐用托管运行时）

```python
import os, requests
resp = requests.post(
    "https://token-plan-cn.xiaomimimo.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {os.environ['MIMO_API_KEY']}"},
    json={"model":"mimo-v2.5-pro",
          "messages":[{"role":"user","content":"总结这段回测日志并给优化建议"}],
          "max_tokens":4096},
    timeout=120,
)
print(resp.json()["choices"][0]["message"]["content"])
```

### 3.4 成本参考

| 维度 | MiMO V2.5 Pro | WorkBuddy(Hy3) 积分 |
|------|---------------|---------------------|
| 计费 | 输入 ¥1/百万 + 输出 ¥4/百万（缓存低至 ¥0.25） | 消耗 CodeBuddy 积分 |
| 长程 Agent 任务 | 极便宜（Token 效率高 40-60%） | 积分消耗可观 |
| 结论 | **重推理首选 MiMO** | 仅用于对话/编排/文档 |

---

## 四、Ollama 本地引擎

> 本章由原 `ollama-bridge` 技能合并而来，作为 MiMO 的统一本地热备。

### 4.1 何时使用本地引擎

- 不想花任何 Token/积分的轻量任务（摘要、分类、简单生成）
- MiMO 宕机 / 到期时的**热备**
- 隐私敏感数据（不出本机）
- 本地小模型能胜任的简单任务

### 4.2 端点与命令

| 操作 | 命令 |
|------|------|
| 列出模型 | `ollama list` 或 `curl http://localhost:11434/v1/models` |
| 对话生成 | `POST http://localhost:11434/v1/chat/completions` |
| 拉取模型 | `ollama pull <name>` |
| 本地注册 GGUF | `ollama create <name> -f Modelfile` |

### 4.3 当前已装模型（实测）

```
qwen3.5:2b | qwen3:0.6b | gpt-4o-mini | minimax-m2.7:cloud | kimi-k2.6:cloud
```

### 4.4 模型选择建议

| 任务类型 | 推荐模型 | 预期速度 | 备注 |
|---------|---------|---------|------|
| 中文轻量摘要 | qwen3.5:2b | 极快 | 默认首选 |
| 简单代码生成 | qwen3.5:2b | 快 | 复杂代码仍建议 MiMO |
| 英文推理 | qwen3.5:2b | 快 | 未专门测试，需实测 |

### 4.5 gemma4:e4b 状态（重要·已核实）

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

> 你之前说"不要重复拉取"——但本机已无该模型文件，若没有本地 GGUF，只能重新拉取。请确认你手头是否有 GGUF，或有授权执行 `ollama pull`。

### 4.6 调用示例

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.5:2b","messages":[{"role":"user","content":"总结这段日志"}],"stream":false}'
```

### 4.7 Ollama 运维检查清单

```bash
# 服务健康检查
ollama list
curl -s http://localhost:11434/v1/models | head -c 200

# Windows: 检查进程 + 端口11434占用
tasklist | findstr ollama
netstat -ano | findstr :11434

# 模型未找到时拉取
ollama pull qwen3.5:2b

# 强制CPU模式（CUDA不可用时）
set OLLAMA_CUDA=0
ollama run qwen3.5:2b
```

---

## 五、统一失败回退链

```
MiMO 不可达？
  ├─ 检查 CC-Switch:15721 / AI Code Switch:4567 / MiMO:18808 是否在跑
  ├─ 检查 MIMO_API_KEY 是否过期（注意区分 sk- 和 tp- key，Token Plan 必须用 tp-）
  ├─ 检查 config.toml 的 [model_providers.custom] 是否有 env_key = "OPENAI_API_KEY"
  └─ 仍不行 → 切本地 Ollama（本章第四章，免费热备）
       ├─ 检查 ollama 服务是否运行（localhost:11434）
       ├─ 检查目标模型是否在 `ollama list` 中
       ├─ 检查端口占用 / CUDA 可用性
       └─ 仍不行 → 提示用户检查端口/续费/拉模型，不要静默失败
```

---

## 六、Codex/ClaudeCode 接 MiMO 的必踩坑（401 终极排障）

> 让 Codex CLI（或 ORCA 内的 Codex 面板）走 MiMO 时，最隐蔽的坑是 **custom provider 缺 `env_key`**。
> 症状：`stream error: ... 401 Unauthorized; retrying 1/5...` 连重试 5 次全挂。
>
> ⚠️ **2026-07-15 重大发现**：ORCA 的真正配置在 **G 盘**，不在 C 盘 AppData！
> - ORCA 安装于 `G:\Orca\app\Orca.exe`
> - 真正的 config.toml 在 `G:\Orca\data\appdata\Orca\codex-runtime-home\home\config.toml`
> - 真正的 auth.json 在 `G:\Orca\data\appdata\Orca\codex-runtime-home\home\auth.json`
> - 真正的 orca-data.json 在 `G:\Orca\data\appdata\Orca\orca-data.json`
> - ⚠️ `C:\Users\Administrator\AppData\Roaming\Orca\` 是**副本/镜像**，改了不生效！
> - ORCA 自带的 Codex 路径 (`Local\OpenAI\Codex\bin\xxx`) 是残缺安装（缺 win32-x64），需将 CODEX_CLI_PATH 指向 npm 全局完整版

**根因排查顺序（从表到里）**：

1. **key 本身有效吗？** 直接 curl 验证（200=有效）：
   ```bash
   curl -s -w "\nHTTP:%{http_code}" -H "Authorization: Bearer $KEY" \
     https://token-plan-cn.xiaomimimo.com/v1/models
   ```
   - 200 → key 没问题，往下查配置
   - 401 → key 错/过期，去 MiMO 控制台核对（注意区分普通 `sk-` key 和 Token Plan 专属 `tp-` key，**订阅套餐必须用 tp- 那把**）

2. **★ config.toml 的 `[model_providers.custom]` 有没有 `env_key`？** ← 最容易漏
   ```toml
   [model_providers.custom]
   name = "xiaomi_mimo"
   base_url = "https://token-plan-cn.xiaomimimo.com/v1"
   wire_api = "responses"
   requires_openai_auth = false
   env_key = "OPENAI_API_KEY"   # ← 缺这行 = Codex 不知道去哪读 key = 空手鉴权 = 401
   ```
   秒验：`codex exec "回复ok" -c 'model_providers.custom.env_key="OPENAI_API_KEY"'`，若立刻回复=就是它。

3. **环境变量 `OPENAI_API_KEY` 的值对不对？** User 级优先：
   ```powershell
   [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY","User")   # 应是 tp-... 那把
   [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY","tp-...","User")
   ```

4. **auth.json 一致**（源头+runtime 两处）：`~/.codex/auth.json` 与 `%APPDATA%/Orca/codex-runtime-home/home/auth.json` 都写 `{"OPENAI_API_KEY":"tp-..."}`。

5. **ORCA 会覆盖 runtime 副本**：改完必须**完全退出 ORCA 再重开**，源头 `~/.codex/config.toml` 是它启动时复制的模板，两处都要改。

**win32 依赖缺失**（`Missing optional dependency @openai/codex-win32-x64`）：
```bash
npm install -g @openai/codex@latest --cache C:/Users/Administrator/.workbuddy/npm-cache --prefer-online
```
（若默认 npm 缓存在 D 盘被沙箱拦，用 --cache 指到 C 盘）

**一键兜底脚本**：`C:\Users\Administrator\WorkBuddy\2026-07-14-16-34-21\fix_orca_codex.ps1`（v4，含 env_key 自动补齐）

**Codex CLI 直连测试路径**：
```
$APPDATA/npm/node_modules/@openai/codex/vendor/x86_64-pc-windows-msvc/codex/codex.exe exec "你好" --model mimo-v2.5-pro --skip-git-repo-check
```

---

## 七、关联技能

| 技能 | 关系 |
|------|------|
| `ollama-bridge` | 已合并入本技能（deprecated，保留恢复入口） |
| `多智能体舰队编排` | 整体舰队架构与路由 |
| `fleet-devops-orchestrator` | 舰队30秒体检可纳入 Ollama 服务状态检查 |
| `龙虾五步法` | 变更前备份规范 |
| `local-llm-integration-fix` | Claude/Codex/Ollama 多工具集成修复 |

---

## 八、版本日志

- V1.0 (2026-07-14)：MiMO 直连技能创建
- V1.1 (2026-07-15)：新增 401 终极排障章节（G盘 config.toml / env_key 发现）
- V1.2 (2026-07-29)：合并 `ollama-bridge` V1.0，升级为本地/远程 LLM 统一网关，新增统一模型选择决策树、Ollama 运维检查清单、统一回退链
