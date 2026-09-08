---
name: opencode-third-path
version: "1.1"
description: 为龙虾舰队部署 OpenCode（OpenCodex）作为 Codex++ / CC Switch 之外的第三条独立模型切换通路。覆盖隔离部署（G 盘 XDG 隔离）、MiMo V2.5/V3.0 配置、与既有工具并行兼容、AI Code Switch 黑名单故障处理。触发词：OpenCodex、OpenCode 第三条通路、新增模型切换路径、部署 OpenCode、独立模型前端
agent_created: true
updated: 2026-08-06
---

# OpenCode 第三条独立通路部署技能 V1.1

> 定位：当 Codex++ / CC Switch 链路出现故障或需要模型热切换时，OpenCode 作为第三条独立通路保障业务连续性

## 一、何时用

- 需要 Codex++ / CC Switch 之外的第三个模型切换前端（独立进程、独立配置、可脚本/无头）
- 为 MiMo V2.5 → V3.0 升级准备独立、可热切换的通路
- 构建"三选一 / 多路径备份"的量化开发工具链
- Codex++ 或 CC Switch 出现故障时，快速切换到备用通路保持开发不中断

## 二、环境事实（本机已验证）

| 项目 | 值 |
|------|-----|
| OpenCode二进制 | `D:\Tools\OpenCodeCLI\opencode.exe` (v1.14.24) |
| 内置Provider | `@ai-sdk/openai-compatible`（无需npm install） |
| 模型后端 | MiMo 经 AI Code Switch `:4567/v1`（模型 `mimo-v2.5`） |
| CC Switch | `:15721`（总网关，不可改） |
| 隔离根目录 | `G:\LobsterAI\ThirdPath_OpenCodex\` |

## 三、部署步骤（五步法 Step2/Step3）

### 3.1 隔离目录（全在 G 盘，C/E 零写入）
```
G:\LobsterAI\ThirdPath_OpenCodex\{bin,config,data,cache,state,model_cache,logs,docs}
```
- `bin\opencode.exe`：从 `D:\Tools\OpenCodeCLI\` COPY（完整程序包在 G）
- `config\xdg\opencode\opencode.json`：模型配置

### 3.2 隔离启动器（PowerShell）
设 `XDG_CONFIG_HOME/DATA_HOME/CACHE_HOME/STATE_HOME` 全部指向 G 盘子目录，日志名带 `OpenCodex_ThirdPath_` 前缀。**绝不写系统环境变量。**

### 3.3 opencode.json 关键配置
```json
{
  "model": "mimo/mimo-v2.5",
  "provider": {
    "mimo": { "npm":"@ai-sdk/openai-compatible",
               "options":{"baseURL":"http://127.0.0.1:4567/v1",
                           "apiKey":"<AI Code Switch key>"},
               "models":{"mimo-v2.5":{"name":"MiMO V2.5 Pro (主)"},
                         "mimo-v3.0":{"name":"MiMO V3.0 (预留)"}} },
    "mimo_ccswitch": { "npm":"@ai-sdk/openai-compatible",
               "options":{"baseURL":"http://127.0.0.1:15721/v1",
                           "apiKey":"<同上的key>"},
               "models":{"mimo-v2.5":{"name":"MiMO V2.5 (回退)"}} }
  }
}
```

### 3.4 验证（实测通过）
```
.\bin\OpenCodex_ThirdPath.ps1 run "ping"
# 日志见: service=llm providerID=mimo modelID=mimo-v2.5 → 模型真实回复
```

### 3.5 无影响校验
启动后确认 `cc-switch.exe`(:15721)、AI Code Switch(:4567)、Codex++ 进程均原样在线；OpenCode 产物落在 G 盘 `data/`。

## 四、核心功能

1. **独立模型切换**：不依赖 Codex++ / CC Switch 进程，独立直连 AI Code Switch
2. **双链路冗余**：主链路 `:4567/v1`（AI Code Switch直连）+ 回退链路 `:15721/v1`（CC Switch代理）
3. **V3.0热切换**：仅需改 `model` 字段即可切换到 MiMo V3.0，不影响其他工具
4. **无头/脚本模式**：`opencode run "prompt"` 支持脚本化调用，可接入自动化流程
5. **XDG完全隔离**：配置/缓存/状态/日志全在G盘独立目录，不污染系统

## 五、参数说明

| 参数 | 位置 | 说明 |
|------|------|------|
| `model` | opencode.json | 主模型ID，如 `mimo/mimo-v2.5` |
| `baseURL` | provider.options | API端点，必须带 `/v1` 后缀 |
| `apiKey` | provider.options | AI Code Switch的API密钥 |
| `XDG_CONFIG_HOME` | 启动器PS1 | 配置目录路径（G盘） |
| `XDG_DATA_HOME` | 启动器PS1 | 数据目录路径（G盘） |
| `XDG_CACHE_HOME` | 启动器PS1 | 缓存目录路径（G盘） |
| `XDG_STATE_HOME` | 启动器PS1 | 状态目录路径（G盘） |

## 六、使用步骤

### 6.1 日常使用
```powershell
# 启动交互式会话
.\G:\LobsterAI\ThirdPath_OpenCodex\bin\OpenCodex_ThirdPath.ps1

# 单次运行
.\G:\LobsterAI\ThirdPath_OpenCodex\bin\OpenCodex_ThirdPath.ps1 run "你的prompt"

# 查看日志
Get-Content G:\LobsterAI\ThirdPath_OpenCodex\logs\OpenCodex_ThirdPath_*.log -Tail 20
```

### 6.2 模型切换（V2.5→V3.0）
```json
// 修改 opencode.json 中 model 字段
"model": "mimo/mimo-v3.0"
// 重启即可，无需改其他配置
```

### 6.3 链路回退（AI Code Switch故障时）
```json
// 修改 opencode.json 中 model 字段
"model": "mimo_ccswitch/mimo-v2.5"
// 自动走 CC Switch :15721 代理链路
```

## 七、使用示例

### 示例1：Codex++ 故障时快速切换
```
# Codex++ 突然无法连接 MiMo
# 诊断: CC-Switch 黑名单或 config.toml 被覆盖
# 应急: 直接启动 OpenCode 第三通路
.\OpenCodex_ThirdPath.ps1 run "继续之前的开发任务"
# OpenCode 独立连 AI Code Switch :4567，不受 CC-Switch 故障影响
```

### 示例2：批量脚本化调用
```powershell
# 批量生成代码注释
$files = Get-ChildItem -Path "E:\项目目录" -Filter "*.py"
foreach ($f in $files) {
    $prompt = "为以下代码生成注释: $(Get-Content $f.FullName -Raw)"
    .\OpenCodex_ThirdPath.ps1 run $prompt | Out-File "$($f.FullName).annotated"
}
```

### 示例3：V3.0灰度测试
```
# MiMo V3.0 发布后，先用 OpenCode 第三通路测试
# 改 model 为 mimo-v3.0 → 运行测试 → 确认无问题 → 再更新 Codex++/CC Switch
```

## 八、错误处理

| 错误场景 | 原因 | 解决方案 |
|---------|------|---------|
| `/opencode/v1` 路由500 | AI Code Switch错误转发到Ollama(:11434未开) | 必须走 `/v1`，不要走 `/opencode/v1` |
| 503 "All services failed" | MiMo "Coding Plan" 405被拉黑 | 重启AI Code Switch清黑名单 |
| GPT Sol 5.6 / Kimi K3 端点缺失 | cc-switch仅有ollama的kimi | 用户需补真实endpoint |
| `opencode.exe` 找不到 | D盘工具被清理 | 从备份恢复或从GitHub重新下载 |
| XDG路径不存在 | G盘目录未创建 | 手动创建8个子目录 |
| PowerShell执行策略阻止 | ExecutionPolicy Restricted | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| 模型回复超时 | MiMo后端负载高 | 切换回退链路 `mimo_ccswitch/mimo-v2.5` |

## 九、安全边界

- **零侵入**：不修改 Codex++ 核心、CC Switch 调度脚本、ORCA 舰队编排
- 新增 provider 仅写 G 盘独立 `opencode.json`，不动现有配置
- V3.0 升级只改 `model` 字段（加 `mimo-v3.0` 条目），不动其他工具
- 日志/缓存/状态全隔离在G盘，不写C盘系统目录

## 十、联动Skill表

| 联动技能 | 联动方向 | 联动内容 |
|---------|---------|---------|
| local-llm-integration-fix | 双向 | OpenCode作为第三通路纳入本地LLM集成修复链路；LLM集成故障时提供备用通路 |
| codex-mimo-link-repair | 双向 | Codex++链路修复的备用方案；OpenCode故障时回退到Codex++ |
| mimo-bridge | 单向→入 | MiMo统一网关提供模型路由；OpenCode作为网关下游消费者 |
| orca-fleet-dual-control | 单向→入 | 舰队双实例控制中OpenCode作为第三通路备份 |
| zero-cost-task-execution | 单向→出 | OpenCode无头脚本模式支持批量低成本执行 |

## 十一、健康度自评

| 维度 | 得分 | 说明 |
|------|------|------|
| 时效性 | 25/25 | 2026-08-06更新 |
| 完整性 | 23/25 | YAML完整+11节标准结构 |
| 联动度 | 20/25 | 2个双向+3个单向 |
| 内容质量 | 23/25 | 步骤+参数+3示例+错误处理+安全边界齐全 |
| **总分** | **91/100** | 🟢优秀 |

## 十二、版本日志

- V1.0 (2026-07-24)：首次创建，基础部署步骤+环境事实+必知坑
- V1.1 (2026-08-06)：补齐agent_created/updated字段；新增核心功能、参数说明、使用步骤、3个使用示例、错误处理表（7场景）、联动Skill表（5个）、健康度自评、安全边界扩展。从64行扩充至完整标准结构
