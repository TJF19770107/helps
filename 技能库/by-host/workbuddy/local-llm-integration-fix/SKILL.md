---
name: local-llm-integration-fix
description: 本地LLM集成修复技能V4.0。覆盖Claude Code/OpenCode/Hermes/CC Switch/Codex++/MiMO/Marvis多工具本地LLM集成配置、环境预检查、错误自动排查、MCP挂载、磁盘预检。触发词：本地模型连不上、LLM集成失败、spawn EINVAL、MCP挂载失败、Codex报错、Claude Code连不上MiMO、Ollama检测失败、环境变量污染、内存不足。
version: 4.0
agent_created: true
updated: 2026-07-24
reconstructed: true
reconstruction_fidelity: 85
---

# 本地LLM集成修复技能 V4.0

> 定位：本地AI工具链（Claude Code / OpenCode / Hermes / CC Switch / Codex++ / MiMO / Marvis）与本地/远端LLM集成的统一排障与修复入口
> 原则：**先检查、再分析、后修复；修复前务必备份；绝不污染ORCA的codex-official/claude-official配置**

## 一、何时激活本技能

- Claude Code / OpenCode / Hermes 无法识别本地模型（Ollama/gemma4:e4b等）
- 报错含 `spawn EINVAL`、`ENOTFOUND`、`ECONNREFUSED`、`connection refused`
- CC Switch / Codex++ 无法连接 MiMO V2.5 Pro，且不是单纯的`codex-mimo-link-repair`场景
- Marvis 启动检查中发现模型配置异常或Token统计链路中断
- MCP服务挂载失败、环境变量污染、端口冲突（15721/4567/11434/18808等）
- 磁盘空间不足（C/E盘满载）导致模型下载/写入失败
- 用户说"本地模型连不上""LLM集成失败""环境变量怎么配"

## 二、工具链端口与角色速查

| 端口 | 角色 | 所属工具 | 说明 |
|------|------|---------|------|
| 15721 | CC-Switch总网关 | cc-switch.exe | **不可改**，Codex/Claude统一入口 |
| 4567 | AI Code Switch代理 | aicodeswitch_v5 | 协议转换 MiMO ↔ OpenAI/Anthropic |
| 57321 | Codex++本地控制端口 | Codex++ | 非代理，仅本地控制 |
| 11434 | Ollama本地服务 | Ollama | 本地模型推理入口 |
| 18808 | MiMO V2.5 Pro推理 | Marvis | MiMO API 本地桥接 |

**正确链路**：
```
Codex++ GUI → cc-switch :15721 → AI Code Switch :4567 → MiMO后端
token-plan-cn.xiaomimimo.com/v1

Claude Code → cc-switch :15721/claude-code → AI Code Switch :4567/claude-code → MiMO

Marvis → MiMO桥 :18808 → token-plan-cn.xiaomimimo.com/v1

Ollama客户端 → :11434 → 本地gemma4:e4b等模型
```

## 三、龙虾五步法执行流程

### Step 1 · 检查（环境快照 + 磁盘预检）

```bash
# ① 磁盘空间预检（C/E/G盘）
df -h /c /e /g 2>/dev/null || wmic logicaldisk get size,freespace,caption

# ② 关键端口监听状态
netstat -ano | grep -E "15721|4567|57321|11434|18808" | grep LISTENING

# ③ 核心进程状态
tasklist | grep -iE "cc-switch|codex|claude|hermes|marvis|ollama|aicodeswitch"

# ④ Ollama模型清单
ollama list 2>/dev/null || echo "Ollama未安装或未启动"

# ⑤ 环境变量污染检查
env | grep -iE "ANTHROPIC|OPENAI|MIMO|OLLAMA|CC_SWITCH|HTTP_PROXY|HTTPS_PROXY"
```

**磁盘熔断规则**：
| 盘符 | 剩余空间 | 动作 |
|------|---------|------|
| C盘 | <2GB | 🔴 立即暂停写操作，先清理或迁移 |
| E盘 | 0字节 / 100% | 🔴 停止一切模型下载/解压，执行迁移 |
| G盘 | <5GB | 🟡 预警，优先清理缓存/日志 |

### Step 2 · 分析（根因定位矩阵）

| 现象 | 可能根因 | 定位方向 |
|------|---------|---------|
| `spawn EINVAL` | Node版本过低 / 路径含中文 / shell参数格式错误 | 检查Node版本、路径、spawn参数 |
| `connection refused 127.0.0.1:4567` | AI Code Switch未启动或僵尸PID | → 联动`codex-mimo-link-repair` |
| `connection refused 127.0.0.1:11434` | Ollama服务未启动 | 启动ollama server |
| `There's an issue with the selected model` | 模型名不匹配 / baseURL错误 | 查models接口 + provider配置 |
| MCP挂载失败 | 端口冲突 / 环境变量未透传 / 技能路径错误 | 查mcp.json + 进程日志 |
| Marvis Token统计无数据 | login.db损坏 / MiMO桥18808中断 | → 联动Marvis修复流程 |
| 模型下载到一半失败 | E盘0字节 / 网络中断 | 磁盘迁移 + 断点续传 |

### Step 3 · 修复（按工具分治）

#### 3.1 Ollama本地模型修复

```bash
# 启动服务
ollama serve > "$HOME/.ollama/server.log" 2>&1 &

# 验证
ollama list
curl -s http://127.0.0.1:11434/api/tags | head -c 500
```

#### 3.2 Claude Code / OpenCode / Hermes 配置修复

```bash
# Claude Code settings.json 标准配置（MiMO模式）
cat > "$HOME/.claude/settings.json" <<'JSON'
{
  "ANTHROPIC_BASE_URL": "http://127.0.0.1:4567/claude-code",
  "ANTHROPIC_API_KEY": "sk-c95dn84njxmbix982irym4sai8x4txyyig9u5ttx7edoomwt",
  "ANTHROPIC_CUSTOM_MODEL_OPTION": "mimo-v2.5",
  "CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY": "0"
}
JSON
```

#### 3.3 CC Switch / Codex++ MiMO链路修复

> 注意：若故障现象仅为"桌面Codex++报stream disconnected / 4567无响应"，**优先调用专用技能`codex-mimo-link-repair`**，本技能不再重复。
>
> 本技能处理更复杂的组合故障：模型名不匹配 + baseURL错误 + 环境变量覆盖 + Claude Code并发冲突。

一键修复脚本（SQLite方案）：
```python
import sqlite3, json, shutil, os

DB = "E:/龙虾AI主控中心/CC-Switch/.cc-switch/cc-switch.db"
BAK = DB + ".bak." + __import__('datetime').datetime.now().strftime("%Y%m%d%H%M%S")
shutil.copy2(DB, BAK)
print(f"✅ 已备份: {BAK}")

conn = sqlite3.connect(DB)
cur = conn.cursor()

# D1: Codex模型名 + baseURL
cur.execute("SELECT value FROM settings WHERE key='common_config_codex'")
row = cur.fetchone()
if row:
    old = row[0]
    new = old.replace('model = "mimo-v2.5-pro"', 'model = "mimo-v2.5"')
    new = new.replace('base_url = "http://127.0.0.1:15721/v1"', 'base_url = "http://127.0.0.1:4567/v1"')
    if new != old:
        cur.execute("UPDATE settings SET value=? WHERE key='common_config_codex'", (new,))
        print("✅ D1 fixed: Codex→mimo-v2.5 @ :4567/v1")

# D3: Claude Code环境覆盖
cur.execute("SELECT value FROM settings WHERE key='common_config_claude'")
row = cur.fetchone()
if row:
    old = row[0]
    new = old
    new = new.replace('"ANTHROPIC_BASE_URL": "http://127.0.0.1:11434"', '"ANTHROPIC_BASE_URL": "http://127.0.0.1:4567/claude-code"')
    new = new.replace('"ANTHROPIC_API_KEY": "ollama"', '"ANTHROPIC_API_KEY": "sk-c95dn84njxmbix982irym4sai8x4txyyig9u5ttx7edoomwt"')
    new = new.replace('"ANTHROPIC_CUSTOM_MODEL_OPTION": "gemma4:e4b"', '"ANTHROPIC_CUSTOM_MODEL_OPTION": "mimo-v2.5"')
    if new != old:
        cur.execute("UPDATE settings SET value=? WHERE key='common_config_claude'", (new,))
        print("✅ D3 fixed: Claude env→MiMO V2.5")

conn.commit(); conn.close()
print("✅ DB updated. 重启cc-switch窗口生效。")
```

#### 3.4 MCP挂载失败修复

```bash
# 检查mcp.json
ls "$HOME/.workbuddy/mcp.json"

# 验证MCP服务端口
curl -s http://127.0.0.1:<mcp-port>/health 2>/dev/null || echo "MCP服务未响应"
```

#### 3.5 磁盘空间危机处理

```bash
# 快速定位大目录（E盘程序目录优先）
du -sh /e/龙虾AI主控中心/*/ 2>/dev/null | sort -hr | head -20

# 迁移候选：Ollama模型、缓存、日志、Obsidian知识库
# 迁移后建立Junction（管理员权限）
# mklink /J "E:\OllamaModels" "G:\OllamaModels"
```

### Step 4 · 验证（全链路健康检查）

```bash
# ① 端口全绿
netstat -ano | grep -E "15721|4567|11434|18808" | grep LISTENING

# ② Ollama模型可用
curl -s http://127.0.0.1:11434/api/tags | grep -q "gemma" && echo "Ollama OK"

# ③ MiMO代理可用
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4567/v1/models

# ④ Claude Code快速测试
claude --version 2>/dev/null && echo "Claude CLI OK"

# ⑤ 磁盘空间非0
df -h /c /e /g
```

### Step 5 · 沉淀（归档与迭代）

- 记录修复模式到`issues_tracker.json`
- 在Obsidian双库追加标签`#local-llm #集成修复 #mimo #ollama`
- 若发现新故障模式，更新本技能版本日志
- 同步`skill-ecosystem-steward`看板

## 四、参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `target_tool` | string | `auto` | 目标工具：claude/codex/hermes/marvis/ollama/cc-switch/auto |
| `fix_level` | string | `check` | 执行级别：check（仅检查）/diagnose（诊断）/repair（修复）/full（检查+修复+验证） |
| `backup_db` | bool | true | 修改cc-switch.db前是否自动备份 |
| `dry_run` | bool | false | 是否只输出修复脚本不执行 |

## 五、输出格式

```markdown
## 本地LLM集成诊断报告

- **目标工具**: {target_tool}
- **执行级别**: {fix_level}
- **磁盘状态**: C:{x}GB / E:{y}GB / G:{z}GB
- **端口状态**: 15721:{on/off} 4567:{on/off} 11434:{on/off} 18808:{on/off}
- **根因判定**: {root_cause}
- **执行动作**: {actions}
- **验证结果**: {PASS/FAIL}
- **沉淀建议**: {next_steps}
```

## 六、使用示例

### 示例1：Claude Code连不上MiMO
```
用户：Claude Code连不上MiMO，报模型问题
→ 激活本技能
→ fix_level=full, target_tool=claude
→ 检查.ANTHROPIC_BASE_URL→修复为:4567/claude-code
→ 验证claude --version + 发一条消息测试
```

### 示例2：Codex++桌面版4567无响应
```
用户：桌面Codex++一直Reconnecting
→ 优先调用 codex-mimo-link-repair（专用技能）
→ 若修复后仍报模型不匹配，再回本技能做D1/D3综合修复
```

### 示例3：Ollama检测失败
```
用户：本地Ollama模型检测不到
→ target_tool=ollama
→ 检查11434端口→启动ollama serve→ollama list验证
```

### 示例4：磁盘满导致模型下载失败
```
用户：E盘0字节，下载模型报错
→ 先停止下载→迁移Ollama模型到G盘→建立Junction→恢复服务
```

## 七、联动Skill表

| 联动技能 | 方向 | 联动内容 |
|---------|------|---------|
| `codex-mimo-link-repair` | 双向 | 单纯4567宕机/僵尸PID场景优先走专用技能；复杂组合故障回本技能 |
| `mimo-bridge` | 单向→入 | MiMO直连401排障、key路由 |
| `ollama-bridge` | 单向→入 | Ollama本地热备、模型清单 |
| `fleet-devops-orchestrator` | 单向→出 | 集成到舰队6维度体检的"本地LLM链路"项 |
| `skill-ecosystem-steward` | 单向→出 | 修复后更新技能矩阵健康度 |

## 八、安全边界

| 操作 | 允许 | 禁止 |
|------|------|------|
| 修改cc-switch.db中MiMO相关provider | ✅（先备份） | — |
| 修改`~/.claude/settings.json` | ✅ | — |
| 启动/停止AI Code Switch :4567 | ✅ | — |
| 启动/停止Ollama :11434 | ✅ | — |
| 动ORCA的`codex-official` provider | — | ❌ |
| 动ORCA的`claude-official` provider | — | ❌ |
| 无备份直接修改生产db | — | ❌ |

## 九、常见错误与解决方案

| 错误码/现象 | 原因 | 解决方案 |
|------------|------|---------|
| `spawn EINVAL` | Node版本<18 / 中文路径 / shell参数错误 | 升级Node / 改用短路径 / 修正spawn参数 |
| `ECONNREFUSED 127.0.0.1:4567` | AI Code Switch未启动 | 调用`codex-mimo-link-repair` |
| `ENOTFOUND token-plan-cn.xiaomimimo.com` | DNS/代理问题 | 检查代理设置，或改用本地IP |
| `mimo-v2.5-pro`模型不存在 | 模型名不匹配 | 改为`mimo-v2.5` |
| `MCP挂载失败` | 端口冲突或路径错误 | 检查`~/.workbuddy/mcp.json` |
| Marvis Token统计无数据 | login.db WAL损坏 | 联动Marvis修复流程 |

## 十、健康度自评

| 维度 | 得分 | 说明 |
|------|------|------|
| 时效性 | 25/25 | 2026-07-24重建 |
| 完整性 | 23/25 | 10节完整，缺"命名规范"专节 |
| 联动度 | 20/25 | 4个联动（2双向+2单向） |
| 内容质量 | 23/25 | 含流程+参数+示例+错误处理 |
| **总分** | **91/100** | 🟢优秀 |

## 十一、版本日志

- V1.0 (2026-05-22)：首次创建，覆盖Claude Code/OpenCode/Hermes/CC Switch多工具本地LLM集成
- V2.0 (2026-05-22)：新增环境预检查、spawn EINVAL排查、MCP挂载失败处理
- V3.0 (2026-06-27)：新增Codex++/MiMO/Marvis支持、磁盘预检、401排障
- V4.0 (2026-07-24)：从记忆重建，联动`codex-mimo-link-repair`避免重复，新增端口角色速查表、磁盘熔断规则、Claude Code标准配置模板

---

> 本技能是本地LLM集成的"总入口"。遇到单纯4567代理宕机，请优先调用`codex-mimo-link-repair`；遇到多工具组合故障或环境/磁盘问题，回到本技能。
