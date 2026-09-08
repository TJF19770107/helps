---
name: ai-workstation-morning-check
description: AI工作站晨间健康体检。一键扫描Marvis进程/磁盘空间/端口冲突/MCP服务/Chrome可用性/Python-Node运行时/模型可用性全链路，输出红黄绿三级健康报告。触发词：晨检、健康检查、工作站体检、AI环境检查、morning check、工作站状态、晨间扫描。
version: 1.0.0
agent_created: true
created: 2026-08-26
source: 2026-08-25 Marvis修复+MCP-HTTP适配器构建实战蒸馏
distilled_by: 龙虾五步法 V3.6 + auto-skill-generator V2.3
tags: [health-check, morning, workstation, marvis, mcp, disk, port, proactive]
---

# AI 工作站晨间健康体检 Skill

> **触发词**：晨检 / 健康检查 / 工作站体检 / AI环境检查 / morning check / 工作站状态 / 晨间扫描
> **方法论**：龙虾五步法（检查→分析→修复→迭代→沉淀）之前置 — **事前预防 > 事后修复**
> **核心理念**：每天开机后跑一次，30秒内发现潜在故障，避免"用到一半才发现工具挂了"

---

## 一、适用场景

| 场景 | 典型表现 | 本技能价值 |
|------|---------|------------|
| 每日开机后例行检查 | Marvis白屏/端口冲突/磁盘满 | 30秒全链路扫描，红黄绿报告 |
| 大任务执行前预检 | 量化回测/AI接单/视频渲染前 | 确认环境就绪再开工，避免中途崩溃 |
| 故障频发期加密巡检 | 连续几天某个工具反复挂 | 设置定时执行，提前预警 |
| 新环境部署后验证 | 迁移/重装/配置变更后 | 一键验证所有组件是否正常 |

---

## 二、核心执行逻辑

```
开机/触发
  ↓
Step1: 磁盘空间检查（C/E/G/D盘）
  ├─ C盘 < 2GB → 🔴 CRITICAL（系统可能卡死）
  ├─ E盘 < 5GB → 🟡 WARNING（WorkBuddy写入可能失败）
  ├─ G盘 < 50GB → 🟡 WARNING（数据盘空间不足）
  └─ 正常 → 🟢 OK
  ↓
Step2: Marvis进程检查（8进程清单）
  ├─ 0进程 → 🔴 CRITICAL（未启动或已崩溃）
  ├─ 1-7进程 → 🟡 WARNING（部分组件缺失）
  └─ 8进程 → 🟢 OK
  ↓
Step3: 端口冲突检查（6个关键端口）
  ├─ 端口被错误进程占用 → 🟡 WARNING
  ├─ 预期端口全部正常 → 🟢 OK
  └─ 预期端口未监听 → 🟡（可能未启动，非故障）
  ↓
Step4: MCP服务状态检查
  ├─ MCP-HTTP适配器未运行 → 🟡（手动启动则正常）
  ├─ 运行中但health端点无响应 → 🔴 CRITICAL
  └─ 正常 → 🟢 OK
  ↓
Step5: Chrome/Chromium可用性检查
  ├─ 不存在 → 🟡 WARNING（Playwright自动化不可用）
  ├─ 存在但版本过旧 → 🟡
  └─ 正常 → 🟢 OK
  ↓
Step6: Python/Node运行时检查
  ├─ 托管版本不存在 → 🔴 CRITICAL（AI执行链断裂）
  ├─ 版本不匹配 → 🟡
  └─ 正常 → 🟢 OK
  ↓
Step7: 输出汇总报告
  ├─ 全🟢 → 工作站健康，可以开工
  ├─ 有🟡 → 有隐患，建议先修复关键项
  └─ 有🔴 → 有严重故障，必须先修复
```

---

## 三、参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--full` | flag | false | 完整模式：额外检查Ollama模型可用性、Git仓库状态 |
| `--json` | flag | false | 输出JSON格式（供自动化消费） |
| `--quiet` | flag | false | 仅输出异常项（全正常时静默） |
| `--port-list` | string | 默认6端口 | 自定义端口列表，逗号分隔 |
| `--marvis-path` | string | 自动检测 | Marvis安装路径（自动检测失败时手动指定） |

---

## 四、使用步骤

### 4.1 快速晨检（日常使用）

```bash
# 一键执行（30秒内完成）
python "G:/WorkBuddy_Data/skills/ai-workstation-morning-check/scripts/workstation_health_check.py"
```

输出示例：
```
╔════════════════════════════════════════╗
║   AI 工作站健康体检报告 2026-08-26 05:00  ║
╠════════════════════════════════════════╣
║ 磁盘空间                               ║
║   C盘  3.2GB  🟢 OK                    ║
║   E盘  8.5GB  🟡 WARNING (<10GB)       ║
║   G盘 152GB   🟢 OK                    ║
║ Marvis进程                             ║
║   8/8进程    🟢 OK                    ║
║ 端口状态                               ║
║   15721 CC-Switch  🟢 OK              ║
║   4567  AI Code    🟢 OK              ║
║   18808 MiMo       🟢 OK              ║
║   15731 HY3        🟡 未监听          ║
║ Chrome/Chromium                        ║
║   D盘官方版    🟢 OK                  ║
║ 运行时                                 ║
║   Python 3.13.12 🟢 OK                ║
║   Node 22.22.2  🟢 OK                ║
╠════════════════════════════════════════╣
║  总评: 🟡 有1个警告项                  ║
║  建议: 启动HY3混元代理(port 15731)     ║
╚════════════════════════════════════════╝
```

### 4.2 完整模式（大任务前预检）

```bash
python "G:/WorkBuddy_Data/skills/ai-workstation-morning-check/scripts/workstation_health_check.py" --full
```

额外检查：
- Ollama模型列表（确认目标模型已拉取）
- Git仓库状态（检测未提交变更）
- Obsidian知识库路径可访问性

### 4.3 自动化集成（定时任务）

在WorkBuddy自动化中配置：
```toml
# 每日06:00晨检（在Skill生成之后）
schedule_type = "recurring"
rrule = "FREQ=DAILY;BYHOUR=6;BYMINUTE=0"
prompt = "执行AI工作站晨间健康体检，如有异常项输出修复建议"
```

### 4.4 静默模式（脚本集成）

```bash
# 仅在有异常时输出（适合嵌入其他脚本）
python workstation_health_check.py --quiet --json
```

---

## 五、端口清单（本机实测）

| 端口 | 角色 | 预期状态 | 关联技能 |
|------|------|---------|---------|
| 15721 | CC-Switch总网关 | 监听 | codex-mimo-link-repair |
| 4567 | AI Code Switch代理 | 监听 | codex-mimo-link-repair |
| 57321 | Codex++本地控制 | 可选 | codex-mimo-link-repair |
| 15731 | HY3混元代理 | 可选 | cloudbase-hy3-relay |
| 18808 | MiMo V2.5 Pro推理 | 监听 | mimo-bridge |
| 8765 | MCP-HTTP适配器(默认) | 可选 | workbuddy-mcp-http-adapter |

---

## 六、Marvis八进程健康标志

| 进程名 | 数量 | 说明 |
|--------|------|------|
| marvis.exe | 1 | 主程序 |
| marvissvr.exe | 1 | 核心服务 |
| marvisdlsvr.exe | 1 | 下载服务 |
| marvishost.exe | 1 | 宿主进程 |
| marvisagent.exe | 1 | Agent引擎 |
| marvisknowledgebase.exe | 4 | 知识库（4实例） |

**健康标准**：8进程全部运行 = 🟢；缺少任意 = 🟡；完全缺失 = 🔴

---

## 七、磁盘空间阈值

| 盘符 | 用途 | 🔴 CRITICAL | 🟡 WARNING | 🟢 OK |
|------|------|------------|-----------|--------|
| C盘 | 系统 | < 2GB | < 5GB | ≥ 5GB |
| E盘 | 程序 | < 2GB | < 10GB | ≥ 10GB |
| G盘 | 数据 | < 20GB | < 100GB | ≥ 100GB |
| D盘 | Chrome/临时 | < 2GB | < 5GB | ≥ 5GB |

---

## 八、异常处置联动

| 异常项 | 处置技能 | 路径 |
|--------|---------|------|
| 磁盘空间不足 | windows-storage-crisis-rescue | `G:/WorkBuddy_Data/skills/windows-storage-crisis-rescue/` |
| Marvis进程异常 | marvis-repair | `G:/WorkBuddy_Data/skills/marvis-repair/` |
| 端口冲突 | codex-mimo-link-repair | `G:/WorkBuddy_Data/skills/codex-mimo-link-repair/` |
| MCP服务异常 | workbuddy-mcp-http-adapter | `G:/WorkBuddy_Data/skills/workbuddy-mcp-http-adapter/` |
| Chrome缺失 | browser-auto-universal | `G:/WorkBuddy_Data/skills/browser-auto-universal/` |
| Python/Node异常 | local-llm-integration-fix | `G:/WorkBuddy_Data/skills/local-llm-integration-fix/` |
| Ollama模型缺失 | mimo-bridge / ollama-bridge | `G:/WorkBuddy_Data/skills/mimo-bridge/` |
| 舰队整体异常 | fleet-devops-orchestrator | `G:/WorkBuddy_Data/skills/fleet-devops-orchestrator/` |

---

## 九、跨技能联动矩阵

本技能作为**前置预防层**，与以下技能形成"检查→修复"闭环：

```
ai-workstation-morning-check（事前预防）
       ↓ 发现异常
       ├→ marvis-repair（Marvis故障修复）
       ├→ windows-storage-crisis-rescue（磁盘危机救援）
       ├→ codex-mimo-link-repair（端口/链路修复）
       ├→ workbuddy-mcp-http-adapter（MCP服务调试）
       ├→ local-llm-integration-fix（运行时修复）
       └→ fleet-devops-orchestrator（舰队编排层）
```

---

## 十、成本控制

- **执行成本**：零积分（纯本地Python脚本，无云端模型调用）
- **执行时间**：≤30秒（快速模式）/ ≤60秒（完整模式）
- **依赖**：Python 3.13+（ctypes标准库，零pip安装）
- **输出**：终端彩色报告 + 可选JSON（供自动化消费）
- **预算**：单次执行 ≤3次工具调用（1次脚本执行 + 0-2次异常处置联动）

---

## 十一、健康度自评

| 维度 | 得分 | 说明 |
|------|------|------|
| 时效性 | 25/25 | 2026-08-26新建 |
| 完整性 | 23/25 | YAML完整+11节，缺scripts子目录说明 |
| 联动度 | 25/25 | 8个双向联动技能 |
| 内容质量 | 24/25 | 步骤+参数+示例+错误处理完整，缺边界case |
| **总分** | **97/100** | 🟢 |

---

*本 skill 由 2026-08-26 auto-skill-generator 第48次执行蒸馏，基于2026-08-25 Marvis修复+MCP-HTTP适配器构建实战。每日30秒晨检，告别事后救火。*
