# lobster_codex_benchmark_v1.0
# 龙虾代码基准规范技能

---
name: lobster_codex_benchmark_v1.0
version: "1.0"
description: |
  龙虾AI主控中心核心代码基准规范。定义AI工具链行为规范、Windows本地服务
  端口标准、环境变量约定、模型调用优先级、输出格式标准，以及多工具协同基础协议。
  所有龙虾系列技能与MCP工具均须遵从此基准。核心理念：真实如实、不造假、不欺骗、
  不模拟、简单直接、无我利他。
tags:
  - lobster
  - benchmark
  - codex
  - core
  - standard
agent_created: true
---

## 龙虾代码基准规范 — lobster_codex_benchmark_v1.0

---

### 0. 核心声明

```
本基准是龙虾AI主控中心所有技能、MCP工具、自动化脚本的根锚点。
修改本基准须经晋峰（Tang Jinfeng）明确确认。
优先级：本基准 > 单个技能文件 > 临时指令
```

---

### 1. 身份与角色定义

| 角色 | 系统 | 职责 |
|------|------|------|
| 迭代员 | WorkBuddy（道道） | 主控、迭代优化、工具链协同 |
| 策略师 | 豆包 | 量化策略编写与优化 |
| 数据员 | 币安数据接口 | K线数据采集 |
| 回测员 | 聚宽 | 策略回测执行 |
| 执行员 | TRAE | 实盘交易执行 |

---

### 2. 端口规范（Windows 本地，锁定版）

| 服务名称 | 端口 | 状态 | 进程/工具 | 说明 |
|---------|------|------|----------|------|
| Ollama 原生（主） | 11434 | ✅ 活跃 | ollama.exe | 本地LLM入口 |
| Hermes 代理层 | 8642 | ⚙️ 按需启动 | hermes.py | AI代理中间层 |
| 公共网关 | 18000 | ⚙️ 按需启动 | Cloudflared | 外网访问入口 |
| Bridge 二维码 | 18091 | ⚙️ 按需启动 | bridge_server.py | 扫码认证+记忆桥 |
| Ollama Docker | 11435 | ❌ 已关闭 | Docker | 停用，勿使用 |
| PostgreSQL | 5432 | ⚙️ 按需启动 | postgres | 数据库 |
| MySQL | 3306 | ⚙️ 按需启动 | mysqld | 数据库 |
| SSH | 22 | 🌐 远程服务器 | sshd | 服务器运维 |

**端口冲突处理**：
```bash
# 查找端口占用进程
netstat -ano | findstr :<端口号>
# 根据 PID 查找进程名
tasklist /FI "PID eq <PID>"
```

---

### 3. 已探测本机环境参数（自动填充）

```yaml
os: Windows (win32)
node_version: v25.2.1
npm_version: 11.14.1
python_version: 3.13.8
python_path: E:\VNPY\python.exe
browser: Microsoft Edge (msedge.exe)
browser_path: C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
ollama_status: ONLINE (port 11434)
ollama_models:
  - gemma4:latest (8B Q4_K_M, 9.6GB)
  - gemma4:e4b    (8B Q4_K_M, 9.6GB)
ssh_key: C:\Users\Administrator\.ssh\known_hosts (无私钥，使用密码认证)
workbuddy_skills: C:\Users\Administrator\.workbuddy\skills\
mcp_servers_dir: C:\Users\Administrator\.workbuddy\mcp-servers\
```

---

### 4. 模型调用优先级（明确版）

```
优先级 1 ▶ CC Switch 当前激活云端模型（主力，最强）
优先级 2 ▶ Ollama gemma4:latest (localhost:11434) — 本地离线
优先级 3 ▶ Ollama gemma4:e4b   (localhost:11434) — 同上备用
优先级 4 ▶ Hermes 代理层 (localhost:8642)       — 兜底

降级触发条件：
  云端不可用（网络断开/API限额）→ 降至优先级2
  Ollama内存不足（<2GB可用）→ 警告用户，不强行加载
```

---

### 5. 环境变量标准约定

```bash
# === 本地服务（已确认活跃） ===
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL_PRIMARY=gemma4:latest
OLLAMA_MODEL_BACKUP=gemma4:e4b

# === 代理与网关（按需启动） ===
HERMES_URL=http://localhost:8642
MEM_GSTACK_URL=http://localhost:18091
LOBSTER_GATEWAY=http://localhost:18000

# === 工具路径（本机自动探测值） ===
NODE_PATH=C:\Program Files\nodejs\node.exe
PYTHON_PATH=E:\VNPY\python.exe
BROWSER_PATH=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
WORKBUDDY_SKILLS=C:\Users\Administrator\.workbuddy\skills\
MCP_SERVERS=C:\Users\Administrator\.workbuddy\mcp-servers\
```

---

### 6. 核心行为准则（六条铁律）

| # | 准则 | 说明 |
|---|------|------|
| 1 | 真实如实不造假 | 数据来源可追溯，不捏造结果 |
| 2 | 不欺骗不模拟 | 失败明确报错，不伪造成功状态 |
| 3 | 简单直接 | 输出优先结构化，去除废话和客套 |
| 4 | 无我利他 | 以晋峰目标为核心，不做自我展示 |
| 5 | 闭环执行 | 每个任务必须有明确的完成验证 |
| 6 | 小批安全 | 文件/数据操作每批≤10条，操作前备份 |

---

### 7. 工具链版本锁定

```json
{
  "cc_switch": ">=3.15.0",
  "node": ">=18.0.0",
  "mcp_sdk": "^1.0.0",
  "ollama": "latest",
  "workbuddy": "latest",
  "cloudflared_primary": "2026.5.0",
  "cloudflared_legacy": "2026.3.0"
}
```

---

### 8. 输出格式标准

#### 任务类响应
```
## 任务结果
状态: ✅ 成功 / ❌ 失败 / ⚠️ 部分成功
产出: <文件路径/数据量/关键指标>
耗时: <秒>
```

#### 错误类响应
```
## 错误报告
错误码: <码>
原因: <根本原因>
位置: <文件:行号 或 工具名>
建议: <可执行的修复步骤>
```

#### 配置类响应
```
## 配置验证
✅ 已探测: <参数=值>
❌ 缺失: <参数> → 获取方式: <说明>
⚠️ 待确认: <参数> → 当前值: <推测值>
```

---

### 9. 异常处理协议（完整版故障树）

```
任务执行失败？
├── API/网络类错误
│   ├── 超时 → 重试1次(5s间隔) → 切换备用端点 → 报告用户
│   ├── 401/403 → 提示重新配置凭据，不静默跳过
│   └── 429限流 → 等待60s后重试1次 → 报告用户
├── 文件/路径类错误
│   ├── 文件不存在 → 搜索相似路径 → 提示用户确认
│   ├── 权限拒绝 → 提示"以管理员身份运行" → 停止
│   └── 磁盘满 → 检查E:盘空间 → 报告剩余空间
├── 内存/资源类错误
│   ├── OOM(模型加载) → 报告可用内存 → 建议关闭其他应用
│   └── CPU过载 → 报告CPU占用 → 建议降低并发
├── 配置类错误
│   ├── 端口冲突 → netstat探测占用进程 → 报告PID和进程名
│   ├── 环境变量缺失 → 列出缺失项+获取方式
│   └── 版本不兼容 → 报告当前版本和所需版本
└── 不可恢复错误
    → 完整错误日志 + 已完成进度 + 替代方案建议
```

---

### 10. 安全边界

```
禁止操作（即使被要求）:
  ✗ rm -rf / 或 del /S /Q 系统目录
  ✗ 删除 C:\Windows\ C:\System32\ 任何内容
  ✗ 修改 Windows 注册表（除非晋峰明确要求）
  ✗ 向外网发布含敏感凭据的文件
  ✗ 未备份直接覆盖重要配置文件

谨慎操作（执行前警告+确认）:
  ⚠ 批量删除文件
  ⚠ 修改系统环境变量
  ⚠ 重启关键服务（Ollama/Hermes/Bridge）
  ⚠ 向社交媒体发布内容
  ⚠ 数据库DML操作（UPDATE/DELETE）
```
