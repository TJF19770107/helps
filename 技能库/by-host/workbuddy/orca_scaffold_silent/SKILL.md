---
name: "orca_scaffold_silent"
description: "ORCA 多 Agent 舰队脚手架静默一键初始化：零交互创建 Git 仓库 + 三层分支(hermes/brain 大脑 / codex/executor 执行 / claude/reviewer 核查) + 三层 git worktree 物理隔离 + 自动写入 .env，可选 GitHub 推送。专治脚本反复弹 read -p/pause/授权确认导致『老点运行』的痛点。触发词：静默初始化ORCA项目、一键搭建多Agent舰队、init_orca_silent、零交互建仓、脚手架静默部署、ORCA脚手架。"
version: "1.2.0"
date: "2026-07-20"
related: ["lobster_task_standard_workflow_v2.7", "龙虾全域官方模板-最终版.md(#289/#290/#291)"]
---

# ORCA 脚手架静默一键初始化

## 何时使用
- 新建任何需要多 Agent 协作的 ORCA 项目（复刻黄金黑马策略三层架构）
- 想一条命令完成「复制脚手架 → 占位符替换 → git init → 三层分支 → 三层 worktree → .env → 可选 GitHub 推送」
- 痛点为旧脚本里的 `read -p` / `pause` / 二次授权弹窗导致每次都要手动点「运行」

## 脚本位置
`E:/龙虾AI主控中心/我的AI分身/项目脚手架/orca_multi_agent_fleet_v1.0/init_orca_silent.sh`

## 用法
```bash
# 最简：仅项目名（基座默认 E:/龙虾AI主控中心/我的AI分身）
bash "E:/龙虾AI主控中心/我的AI分身/项目脚手架/orca_multi_agent_fleet_v1.0/init_orca_silent.sh" "项目名"

# 带 GitHub 用户名 + token（自动推送全部分支）
bash init_orca_silent.sh "项目名" TJF19770107 ghp_xxxx
```

环境变量覆盖：`ORCA_FLEET_BASE`（基座目录）、`GH_USER`、`GH_TOKEN`/`GITHUB_TOKEN`、`GIT_USER`、`GIT_EMAIL`。

## 静默设计（为何不再弹确认）
- 全程无 `read -p` / `pause` / 二次确认 / 授权弹窗
- 目标已存在且非空 → 静默跳过（exit 0），不覆盖、不报错，保证幂等
- GitHub 推送需 token；未提供则跳过并打印手动命令，绝不卡在网络确认
- 路径经 `cygpath -w` 归一化，兼容 Git Bash 的 `/c/` 写法与 Windows 的 `E:/` 写法
- `.env` 由脚本重新生成，`ORCA_ROOT_PATH` 自动指向新项目根（无密钥，可安全提交）

## 产出
- 分支：`master` / `hermes/brain` / `codex/executor` / `claude/reviewer`
- 工作树：`worktrees/{hermes,codex,claude}`（物理隔离，已加入 `.gitignore`）
- 占位符：脚手架内旧项目名/路径自动替换为新项目名/路径（兼容「重建」「建设」两种历史命名）
- ORCA 开箱即用：自动复制 `scripts/orca_setup_worktree.sh`、`config/orca/*.md`、`docs/ORCA工作树启动配置指南.md`，并在生成工作树后预生成每个工作树的 `.env`

## ORCA 工作树自动配置（全域模板 #290）

新建项目后，进入 ORCA，对每个工作树底部「添加设置脚本」框粘贴同一行：

```bash
bash ../../scripts/orca_setup_worktree.sh
```

脚本会自动识别当前目录是 `hermes` / `codex` / `claude` 并注入：
- `ORCA_ROOT_PATH`（项目根，Windows 反斜杠）
- `ORCA_WORKTREE_PATH`（当前工作树路径）
- `ORCA_WORKSPACE_NAME`（项目名）
- `AGENT_ROLE`（当前 Agent 角色）

随后将 `config/orca/hermes_system_prompt.md` / `codex_system_prompt.md` / `claude_system_prompt.md` 的角色提示词粘贴到对应 Agent 对话窗口，即可进入中文角色交互状态。

配套脚本：
- `scripts/orca_push_all.sh`：一键推送全部分支到 GitHub（走 gh-proxy）
- `scripts/orca_backup.sh`：非破坏性快照三个工作树到 `backups/`

## 版本治理（对齐全域模板 #290/#291 + 龙虾五步法 v2.7）

脚手架自带 `scaffold_version`，**绝不自动升级旧项目**。仅在「项目版本 ≠ 全域最新版本」时触发一次交互确认，日常一致零打扰。

### 核心规则
- **一致即静默**：`bash scripts/orca_scaffold_check.sh` 比对版本，一致直接通过，不弹窗（防冗余，根治「老点运行」）。
- **不一致即询问（不可跳过、不可静默升级）**：
  - **Y｜增量迭代**：仅补新参数/技能/配置，已存在文件不覆盖。
  - **N｜版本分叉**：保留旧版，写入 `fork_version.log`，新旧长期并行、互不干扰。
- **保护目录永远不覆盖**：`.env` `database` `conversations` `skills` `logs`。
- **非交互环境**（无 TTY）拒绝静默决策，输出手动命令后退出（exit 2），绝不偷偷升级。

### 用法
```bash
# 在已有项目根执行：版本一致则跳过；不一致则交互 Y 增量 / N 分叉
bash "E:/龙虾AI主控中心/我的AI分身/项目脚手架/orca_multi_agent_fleet_v1.0/scripts/orca_scaffold_check.sh"

# 或显式增量迭代（只新增缺失文件，跳过保护目录）
bash "E:/龙虾AI主控中心/我的AI分身/项目脚手架/orca_multi_agent_fleet_v1.0/scripts/upgrade_incremental.sh" "<项目根路径>"
```

> 新项目用 `init_orca_silent.sh` 创建时直接带最新 `scaffold_version`，故无需治理弹窗；旧项目用 `orca_scaffold_check.sh` 管理升级。

> **已固化（2026-07-20）**：上述规则已正式写入受管全域模板 `#290.10 脚手架版本治理强制规则` + 新建协议 `#291 Hermes 大脑层方案规范`（模板版本 v3.118），以及龙虾五步法 v2.7 SKILL.md 的「脚手架版本校验节点」。全域模板与五步法各自独立、不合并。

## 约束（龙虾五步法 V2.7 / 全域模板 #289 #290 #291）
- 禁止写死 C 盘；默认基座 `E:/龙虾AI主控中心/我的AI分身`
- 三层角色固定：`hermes/brain` 大脑层 / `codex/executor` 执行层 / `claude/reviewer` 核查层
- 关联协议 #289「ORCA 多 Agent 舰队搭建规范」、#290「ORCA 工作树自动填充配置规范」
- 需在 ORCA 中为三个工作树配置「设置脚本/存档脚本」自动填充（见脚手架 `docs/可视化标注指南.md`）

## 排错
- 若 `git worktree add` 报分支已占用：该分支已被其他工作树 checkout，脚本打印 warn 并继续
- 若 `.env` 路径异常：确认基座路径为 Windows 风格（`E:/` 或 `C:/`），勿用 `/e/` 或 `/c/` 形式
- 若 python 未找到：脚本会自动探测 `python` / `python3` / `py`
