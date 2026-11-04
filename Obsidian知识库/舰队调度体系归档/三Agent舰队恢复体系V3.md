# 三Agent舰队恢复体系

> 沉淀日期：2026-07-30
> 版本：V3.0
> 关联技能：lobster-fleet-recovery

## 一、架构总览

| 实例 | 角色 | 端口 | 工具 | 工作分支 |
|------|------|------|------|----------|
| Hermes | 大脑/编排 | 8642 | hermes CLI | master |
| Codex | 执行器 | 15730 | codex CLI | codex/executor |
| Claude Code | 审核器 | 15721 | claude CLI | claude/reviewer |

## 二、常见故障

### 2.1 Codex MODULE_NOT_FOUND
**现象**：`Cannot find module ... codex.js`
**根因**：AppData/Roaming/npm 下 codex shim 缺失或路径错误
**修复**：
```bash
# 重建双格式 shim
cat > ~/AppData/Roaming/npm/codex << 'EOF'
#!/bin/sh
exec node "I:/npm/node_modules/@openai/codex/bin/codex.js" "$@"
EOF
cat > ~/AppData/Roaming/npm/codex.cmd << 'EOF'
@ECHO off
node "I:\npm\node_modules\@openai\codex\bin\codex.js" %*
EOF
chmod +x ~/AppData/Roaming/npm/codex
```

### 2.2 Claude Code API Error: ConnectionRefused
**现象**：`Unable to connect to API (ConnectionRefused)`
**根因**：代理端口 15721 未启动
**修复**：
```bash
start //min "Fix-15721" "C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe" "E:/龙虾AI主控中心/MCP服务/anthropic_proxy_15721.py"
```

### 2.3 Codex 配置被覆盖
**现象**：Codex 桌面版报 401 或无法连接
**根因**：config.toml 的 wire_api 被改成 responses
**修复**：确保 wire_api = "chat"，base_url = "http://127.0.0.1:15730/v1"

## 三、自动恢复机制

| 层级 | 文件 | 触发时机 |
|------|------|----------|
| 开机 | 计划任务 LobsterFleet_AutoRestore | 系统启动 |
| 项目级 | .orca/setup.sh | Orca 打开项目 |
| Agent级 | CLAUDE.md / CODEX.md | Claude/Codex 进入项目 |
| 手动 | bash scripts/launch_all_agents.sh | 命令行执行 |

## 四、关键路径

- 代理脚本：E:\龙虾AI主控中心\MCP服务\
- Python：C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe
- Codex 安装：I:\npm\node_modules\@openai\codex\
- Shim：~/AppData/Roaming/npm/codex(.cmd)
- 配置：~/.codex/config.toml
- Orca runtime：~/AppData/Roaming/Orca/codex-runtime-home/home/config.toml

## 五、龙虾五步法

1. **诊断**：全链路状态采集（端口+CLI+shim+health+配置）
2. **方案**：输出修复清单表格，标注 [OK]/[FIX]/[FAIL]
3. **实施**：按优先级修复（代理→shim→配置→分支同步）
4. **自测**：全链路验证，要求零错误
5. **沉淀**：文档+技能+Git提交
