# lobster_bmad_team_v1.0

将 BMAD-METHOD（BMad Method）在本地项目中完成安装初始化，并把“团队角色 + 敏捷工作流 + 目录与产物规范”固化为可复用的龙虾技能包。

## 真实性边界（如实汇报）

- 本机环境下 `git clone https://github.com/bmad-code-org/bmad-method` 多次失败（git 连接 443 中断/超时），因此“源码下载”改为使用 GitHub 的 `main.zip` 下载并解压到本地；已获取到 `main` 分支当前提交 SHA：`e36f219c81b6010d4aae423ba12f49edb5b6e31a`。
- 已按官方安装器成功执行一次非交互安装：`npx bmad-method install ... --yes`，在目标项目里完成 BMad Core + BMad Method（BMM）初始化，并生成 `.claude/skills` 42 个技能目录。
- “21 个 AI 角色团队”未在当前默认 BMM 安装产物中出现：本次安装生成的 `agents.*` 仅 6 个（Analyst/PM/UX/Architect/Dev/Tech Writer）。尝试安装额外官方模块（bmb/tea/bmgd/cis）时，安装器需要 `git clone` 外部模块仓库，受同一 git 网络问题影响失败（可复现日志见下文）。

## 快速开始（在任意项目目录启用 BMAD）

在你希望启用 BMAD 的项目根目录执行（官方安装器，非交互）：

```powershell
npx -y bmad-method install --modules bmm --tools claude-code --yes
```

验收（应出现 `_bmad/`、`.claude/skills/`、`_bmad-output/`）：

```powershell
ls . ; ls .\\_bmad ; ls .\\.claude\\skills
```

## 本次落地取证（可审计路径）

- BMAD-METHOD 源码（zip 解压）：`G:\\third_party\\bmad-method\\BMAD-METHOD-main`
- 安装初始化目标项目：`G:\\bmad_workspace\\bmad_team_init`
- 安装产物根：`G:\\bmad_workspace\\bmad_team_init\\_bmad`
- 生成的 Claude Code 技能目录（42 个）：`G:\\bmad_workspace\\bmad_team_init\\.claude\\skills`

## 团队架构（本次安装实际生成的 6 个角色）

来源：`G:\\bmad_workspace\\bmad_team_init\\_bmad\\config.toml`

- bmad-agent-analyst：Mary / Business Analyst
- bmad-agent-pm：John / Product Manager
- bmad-agent-ux-designer：Sally / UX Designer
- bmad-agent-architect：Winston / System Architect
- bmad-agent-dev：Amelia / Senior Software Engineer
- bmad-agent-tech-writer：Paige / Technical Writer

## 敏捷工作流技能清单（42 skills → .claude/skills）

来源：`G:\\bmad_workspace\\bmad_team_init\\.claude\\skills`

- bmad-advanced-elicitation
- bmad-agent-analyst
- bmad-agent-architect
- bmad-agent-dev
- bmad-agent-pm
- bmad-agent-tech-writer
- bmad-agent-ux-designer
- bmad-brainstorming
- bmad-check-implementation-readiness
- bmad-checkpoint-preview
- bmad-code-review
- bmad-correct-course
- bmad-create-architecture
- bmad-create-epics-and-stories
- bmad-create-prd
- bmad-create-story
- bmad-create-ux-design
- bmad-customize
- bmad-dev-story
- bmad-distillator
- bmad-document-project
- bmad-domain-research
- bmad-editorial-review-prose
- bmad-editorial-review-structure
- bmad-edit-prd
- bmad-generate-project-context
- bmad-help
- bmad-index-docs
- bmad-market-research
- bmad-party-mode
- bmad-prfaq
- bmad-product-brief
- bmad-qa-generate-e2e-tests
- bmad-quick-dev
- bmad-retrospective
- bmad-review-adversarial-general
- bmad-review-edge-case-hunter
- bmad-shard-doc
- bmad-sprint-planning
- bmad-sprint-status
- bmad-technical-research
- bmad-validate-prd

## 推荐用法（最小闭环）

1) 从“我该做什么”开始：调用 `bmad-help`
2) 出产品需求：`bmad-product-brief` → `bmad-create-prd` → `bmad-validate-prd`
3) 出体验与架构：`bmad-create-ux-design` → `bmad-create-architecture`
4) 拆解交付：`bmad-create-epics-and-stories` → `bmad-create-story` / `bmad-dev-story`
5) 进入迭代：`bmad-sprint-planning` → `bmad-sprint-status` → `bmad-code-review` → `bmad-retrospective`

## 失败复现与原因（安装扩展模块）

目标：安装官方扩展模块以扩大角色/流程覆盖：

```powershell
npx -y bmad-method install --directory G:\\bmad_workspace\\bmad_team_init --modules bmm,bmb,tea,bmgd,cis --tools claude-code --yes --action update
```

结果：安装器在拉取外部模块时调用 `git clone`，因 git 网络失败而终止；示例报错为：

- Failed to clone external module 'bmb' at v1.7.0
- fatal: unable to access 'https://github.com/bmad-code-org/bmad-builder/': Recv failure: Connection was aborted

## 交付与可见性

- Trae 显性入口：`E:\\龙虾AI主控中心\\.trae\\skills\\lobster_bmad_team_v1.0`
- 目标全局路径（如需供所有智能体直接加载）：`C:\\Users\\Administrator\\.claude\\skills\\lobster_bmad_team_v1.0`

