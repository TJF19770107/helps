---
name: "lobster_claude_mem_gstack_bridge_v1.0"
description: "为 Claude Code 的 claude-mem 持久记忆做本地化安装/验收/回滚，并对齐 gstack/Hermes skills 注入链路。Invoke when 需要“持久记忆/超长上下文/claude-mem 安装与接入 gstack”。"
---

# claude-mem × gstack 接入（合规版）

## 重要结论（先说清楚）

- 你给的仓库地址 `https://github.com/mehmetcanfarsak/claude-mem` 当前为 404（Page not found），无法作为“官方源”完成安装。
- 可用替代源：`https://github.com/thedotmack/claude-mem`（文档公开提供 `npx claude-mem install` 安装方式）。
- 本技能只提供“本地安装 + 验收 + 回滚 + gstack/Hermes 接入”的标准流程；不会擅自绕过系统确认、也不会把“所有确认弹窗自动同意”固化为规则。
- 若涉及联网下载/安装依赖，必须由你显式设置环境变量门禁 `LOBSTER_ALLOW_NET_INSTALL=1` 才允许继续。

## 触发条件

- 你明确要求：安装/修复/迁移 Claude Code 的持久记忆（claude-mem 或同类），并且要纳入 gstack/Hermes 工作流。
- 你明确要求：需要一个“可回滚”的一键化脚本流程（但仍遵守门禁与验收）。

## 预检（必须通过）

1) Node 与 npm 可用（Windows PowerShell）：

```powershell
node -e "process.stdout.write(process.version)" ; "`nOK"
npm -v
```

2) gstack 注入链路存在（Hermes 通过宿主 `~/.claude/skills` 注入）：

```powershell
Test-Path "$env:USERPROFILE\.claude\skills\gstack" ; Test-Path "$env:USERPROFILE\.claude\skills\gstack-qa\SKILL.md"
```

## 安装（门禁控制）

### 0) 开门禁（仅当你允许联网安装时才做）

```powershell
$env:LOBSTER_ALLOW_NET_INSTALL="1"
```

### 1) 安装 claude-mem（推荐：thedotmack 版本）

仅当 `LOBSTER_ALLOW_NET_INSTALL=1` 时执行：

```powershell
if ($env:LOBSTER_ALLOW_NET_INSTALL -ne "1") { throw "NET_INSTALL_BLOCKED: set LOBSTER_ALLOW_NET_INSTALL=1 to proceed" }
npx -y claude-mem install
```

说明：
- 该方式会自动注册 Claude Code 的 hooks/worker（区别于 `npm i -g` 只装 SDK）。

### 2) 基础验收

- 预期：本地会出现 Web Viewer（默认 `http://localhost:37777`），并且新会话能注入历史摘要上下文。

```powershell
try { (Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:37777").StatusCode } catch { "viewer_not_ready" }
```

## gstack/Hermes 接入策略（不破坏现有环境）

### 目标

- claude-mem 负责“跨会话持久记忆”（Claude Code 内）。
- gstack 负责“方法论工作流 + 规则注入 + 会话闭环”（你当前体系内）。
- Hermes 只负责把宿主机 `LOBSTER_CLAUDE_SKILLS_DIR` 下的 `gstack-*` 技能注入到容器侧 `/home/agent/.hermes/skills/`，不改动 Docker/WSL 结构。

### 实操建议

1) 继续使用 gstack 的 `/context-save` 与 `/context-restore` 做“可控的、可审计的”上下文保存/恢复。
2) claude-mem 作为补充：用于自动压缩工具输出与会话观测，降低 token 负担并增强连续性。
3) 若你需要把“龙虾规则”稳定注入 Claude Code，会优先走 gstack 的 preamble 注入与 skills 机制，而不是让插件改写全局行为。

## 回滚（必须可一键撤销）

优先使用 claude-mem 自带卸载命令（以其文档为准）。若无法确定命令，采用“最小破坏回滚”：

1) 停止 worker（如果有对应进程/服务）。
2) 移除 Claude Code 的插件/marketplace 安装项（保留数据目录可选）。
3) 验收：不再监听 37777 且 Claude Code 启动不再注入 memory。

本技能不在此硬编码卸载命令，避免因版本差异误删数据；执行前先以 `npx claude-mem --help` 或官方文档确认支持的 uninstall 选项。

## 常见问题

- gstack 与 claude-mem 是否冲突：通常不冲突；一个偏“工作流方法论”，一个偏“跨会话记忆压缩/检索”。
- 你提供的仓库为什么不能装：仓库 404 时无法拉取源码或 release，因此不能作为安装依据。
