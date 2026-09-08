---
name: "hermes_awesome_v1.0"
description: "Hermes 生态全景导航、技能市场聚合、gstack 命令速查、技能安装向导。Invoke when 需要了解 Hermes/gstack 有哪些技能可用、如何安装新技能、快速查找已安装技能的用法，或需要技能推荐。"
tags: ["awesome", "hermes", "gstack", "skills", "marketplace", "navigation", "catalog", "lobster"]
---

# Hermes Awesome v1.0 — 生态导航与技能市场

## 核心能力

| 能力域 | 具体功能 |
|--------|---------|
| 技能目录 | 本地已安装技能全量列表与快速索引 |
| 生态导航 | gstack / lobster / openclaw / Trae 技能分类导航 |
| 安装向导 | 技能安装步骤、目录规范、格式校验 |
| 命令速查 | 所有 gstack-* 命令的触发词与功能说明 |
| 推荐引擎 | 根据任务类型推荐最合适的技能组合 |
| 版本管理 | 技能版本号规范、升级路径、兼容性说明 |

## 触发条件

- 不知道该用哪个技能完成当前任务
- 需要查找某个 gstack 命令的完整用法
- 需要安装新技能到全局技能库
- 需要了解 Hermes 生态的整体架构

## 全局技能库目录

**路径**：`C:\Users\Administrator\.claude\skills\`

### 🦞 Lobster 系列（平台核心）

| 技能名称 | 触发场景 |
|---------|---------|
| `lobster_codex_benchmark_v1.0` | 模型性能基准测试、能力评估 |
| `lobster_claude_mem_gstack_bridge_v1.0` | 持久记忆安装、claude-mem × gstack 接入 |
| `lobster_ai_bridge_universal_v1.0` | AI 服务桥接、202→200 状态码归一化 |
| `lobster_bridge_statuscode_unify_v1.0` | Hermes /v1/runs 状态码统一 |
| `lobster_bmad_team_v1.0` | BMAD 团队协作模式 |

### 🏗 G Stack 系列（工程工作流）

| 技能名称 | 触发场景 |
|---------|---------|
| `gstack` | 主体工作流框架 |
| `gstack-qa` | 质量保障、测试流程 |
| `gstack-review` | 代码审查 |
| `gstack-ship` | 发布上线 |
| `gstack-freeze` / `gstack-unfreeze` | 版本冻结/解冻 |
| `gstack-learn` | 知识学习与沉淀 |
| `gstack-health` | 系统健康检查 |
| `gstack-investigate` | 问题调查与根因分析 |
| `gstack-benchmark` | 性能基准测试 |
| `gstack-context-save` / `gstack-context-restore` | 上下文保存/恢复 |
| `gstack-browse` | 网页浏览与信息提取 |
| `gstack-design-html` | HTML 设计产物生成 |
| `gstack-pair-agent` | 双智能体协作 |
| `gstack-upgrade` | 技能/依赖升级 |
| `gstack-retro` | 复盘与改进 |

### 🦀 OpenClaw 系列（能力扩展）

| 技能名称 | 触发场景 |
|---------|---------|
| `openclaw_skill_creator_v1.0` | 创建新技能脚手架 |
| `openclaw_find_skill_v1.0` | 搜索匹配技能 |
| `openclaw_code_simplifier_v1.0` | 代码简化重构 |
| `openclaw_frontend_design_v1.0` | 前端设计系统 |
| `openclaw_document_skills_v1.0` | 文档生成 |
| `openclaw_rail_loop_v1.0` | 循环优化工作流 |
| `openclaw_bidirectional_v1.0` | 双向数据同步 |

### 🤖 Hermes 系列（本库新装）

| 技能名称 | 触发场景 |
|---------|---------|
| `hermes_gstack_v1.0` | Git 全生命周期管理 |
| `hermes_gbrain_v1.0` | 代码分析与架构理解 |
| `hermes_webui_v1.0` | Web 界面开发与 Docker 部署 |
| `hermes_awesome_v1.0` | **你正在使用此技能** — 生态导航 |
| `hermes_self_evolution_v1.0` | 自我学习与记忆持久化 |

### 🏦 垂直领域技能

| 技能名称 | 触发场景 |
|---------|---------|
| `vnpy_bidirectional_v1.0` | VeighNa Trader 双向操作 |
| `wechat_crawler_v1.1` | 微信内容采集 |
| `collector_five_in_one_v2.0` | 五合一数据采集器 |
| `agency-agents/` | 多智能体协作模板库 |

## 技能安装标准流程

### 1) 新建技能文件夹

```powershell
$SKILL_NAME = "my_skill_v1.0"
$SKILLS_DIR = "C:\Users\Administrator\.claude\skills"
New-Item -ItemType Directory -Path "$SKILLS_DIR\$SKILL_NAME" -Force
```

### 2) SKILL.md 格式规范

```markdown
---
name: "<skill_name>"
description: "<一句话描述>。Invoke when <何时调用>。"
tags: ["tag1", "tag2", "hermes"]
---

# <技能名> — <功能描述>

## 核心能力
...

## 触发条件
...

## 标准工作流
...

## 验收口径
...

## 回滚口径
...
```

### 3) 验证格式

```powershell
# 检查所有技能是否有 SKILL.md
Get-ChildItem "C:\Users\Administrator\.claude\skills" -Directory | ForEach-Object {
  $skill = $_.FullName
  $md = Join-Path $skill "SKILL.md"
  if (Test-Path $md) { "✅ $($_.Name)" } else { "❌ $($_.Name) — 缺少 SKILL.md" }
}
```

## gstack 命令速查

| 命令 | 功能 |
|------|------|
| `/qa` | 执行质量检查 |
| `/review` | 代码审查 |
| `/ship` | 发布流程 |
| `/freeze` | 冻结当前版本 |
| `/health` | 系统健康检查 |
| `/context-save` | 保存当前上下文 |
| `/context-restore` | 恢复上下文 |
| `/learn <topic>` | 学习特定主题 |
| `/investigate <issue>` | 问题调查 |
| `/retro` | 复盘改进 |

## 与 Trae 联动

- Trae 读取 `LOBSTER_CLAUDE_SKILLS_DIR` 环境变量定位本技能库。
- 本技能作为"元技能"，帮助 Trae 在不确定该用哪个技能时快速导航。
- 全局共享路径：`C:\Users\Administrator\.claude\skills\hermes_awesome_v1.0\SKILL.md`
