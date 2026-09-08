# lobster_doubao_cloud_v1.0

## 目标

开发「豆包云上龙虾」独立智能体的最小可验收闭环：纯云对云（豆包→Coze 插件→公网→CNB 云原生），并固化为可复用模板与验收口径。

## 固定链路（硬门禁）

豆包 → Coze（工作流强制工具调用）→ 自定义插件（OpenAPI）→ CNB 云原生服务 → CNB Issue（审计落点）

## 交付物（本仓库内）

- CNB 云原生插件网关（Node 无依赖）：
  - [serve_doubao_cloud_lobster_v1.js](file:///e:/%E9%BE%99%E8%99%BEAI%E4%B8%BB%E6%8E%A7%E4%B8%AD%E5%BF%83/cnb_repos/NPC_Hermes_Gateway/scripts/serve_doubao_cloud_lobster_v1.js)
- Coze 导入用 OpenAPI：
  - [doubao_cloud_lobster_v1.yaml](file:///e:/%E9%BE%99%E8%99%BEAI%E4%B8%BB%E6%8E%A7%E4%B8%AD%E5%BF%83/cnb_repos/NPC_Hermes_Gateway/openapi/doubao_cloud_lobster_v1.yaml)
- 配置与验收 Runbook：
  - [doubao_cloud_lobster_v1.md](file:///e:/%E9%BE%99%E8%99%BEAI%E4%B8%BB%E6%8E%A7%E4%B8%AD%E5%BF%83/cnb_repos/NPC_Hermes_Gateway/.workflow/doubao_cloud_lobster_v1.md)
- 云端技能目录（注册表）：
  - [cloud_skills_registry_v1.md](file:///e:/%E9%BE%99%E8%99%BEAI%E4%B8%BB%E6%8E%A7%E4%B8%AD%E5%BF%83/cnb_repos/NPC_Hermes_Gateway/.workflow/cloud_skills_registry_v1.md)

## 环境变量（只写变量名）

- Coze 插件鉴权：`COZE_PLUGIN_TOKEN`
- CNB 调用：`CNB_API_TOKEN`、`CNB_TARGET_REPO`
- 技能目录（可选）：`SKILLS_CATALOG_PATH` 或 `SKILLS_CATALOG_URL`
- 可选：`CNB_API_BASE`、`CNB_DRY_RUN`、`TIMEOUT_MS`、`RETRY_MAX`、`RETRY_BASE_DELAY_MS`、`BODY_LIMIT_BYTES`、`HOST`、`PORT`

## 使用方式（最短路径）

1) 在 CNB 云原生部署网关：运行 `node scripts/serve_doubao_cloud_lobster_v1.js` 并配置上述环境变量。  
2) 在 Coze 创建自定义插件：导入 OpenAPI（`doubao_cloud_lobster_v1.yaml`），设置 Bearer Token。  
3) 在 Coze Bot 中锁定工作流：所有用户输入强制走 `POST /v1/skills/run`。  
4) 发布到豆包：选择豆包渠道发布（以 Coze 控制台发布页为准）。  

## 验收口径（真实链路）

- `GET /health` 返回 2xx 且 body 为 `{"ok":true}`
- Coze 工具调用 `skills.run` 返回 `accepted:true` 与 `run_id`
- CNB 目标仓库出现新 Issue：
  - `skill_id=cnb.issue.create`：Issue 标题为你传入的 title（或由 user_input 自动生成）
  - 其他 skill_id：Issue 标题前缀 `lobster_run:`

## 回滚

- 下线 CNB 网关服务；在 Coze 停用/解绑插件；取消豆包渠道发布或回退到上一发布版本。

## 真实性边界（如实）

- 本版本把“云端技能执行”先固化为 **CNB Issue 审计落点**，用于证明云对云链路已通；不在云端直接执行任意代码。
- “永久在线”取决于 CNB 云原生的部署与配额，本技能仅提供可验收的最小闭环与门禁。

## 来源说明（平台内置 vs 项目迭代）

- 平台内置：Coze 的插件（OpenAPI 导入）与工作流编排、发布到豆包渠道（以平台实际 UI 为准）。
- 项目迭代：本仓库提供的 CNB 云原生网关脚本与 OpenAPI/Runbook（上述交付物路径）。
