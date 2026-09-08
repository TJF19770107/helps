# CNB 免费 DeepSeek V4 Flash · 接入方案（2026-08-28）

## 目标
让 Codex / Claude / 汤小龙 免费用上 DeepSeek V4 Flash。

## 现状（实测）
- CNB git token 有效（cnb.cool 可达、鉴权过），但不是 OpenAI chat 格式端点（chat 400）。
- AtomCode 13460 代理能列出 deepseek-v4-flash，但调用 500（缺 CodingPlan/AtomGit 登录 token）。
- CNB @CodeBuddy NPC 是 issue/PR 评论交互，非本地工具直调 API。

## 方案A（推荐）：FreeLLMAPI 聚合 + 录入免费 Key
- 在 http://localhost:3001 面板录入含 DeepSeek 免费额度的厂商 Key。
- 生成 FreeLLMAPI API key → Codex 用 freellmapi provider（base_url 3001/v1，已加）。

## 方案B：AtomCode / CodingPlan 登录
- 运行 atomcode login 生成 CodingPlan/AtomGit token（需 CodingPlan 账号）。
- 用它启动 13460 代理 → 本地 Codex/Claude 指向 127.0.0.1:13460/v1，model=deepseek-v4-flash。

## 方案C：查 CNB 官方文档
- 到 cnb.cool 官方文档确认 DeepSeek V4 Flash 的 API 端点与格式（issue 评论 NPC 或 API 网关）。

## 待用户提供
- 方案A：在面板录入哪些免费 Key + 面板生成的 API key。
- 方案B：是否已有 CodingPlan 账号可登录。
- 方案C：CNB 官方文档链接或端点。