---
name: "lobster_local_lobster_publish_v1.0"
description: "【本地龙虾】闭环发布：固化本地技能列表接口(18091)的调用与验收，输出可审计取证报告；不涉及任何云端/Coze。"
---

# 本地龙虾闭环发布（标准版）

## 目标

- 固定本地接口：`http://127.0.0.1:18091/api/trae/skills/list`
- 锁定返回结构：必须满足 `ok: true` 且 `skills` 为数组
- 生成本地验收报告与取证文件（不记录任何 Token 明文）

## 环境变量（只允许出现变量名）

- 鉴权（2 选 1）：
  - `TRAE_API_TOKEN`（优先）
  - `DOUBAO_USER_TRIGGER_TOKEN`（备选）
- 可选：自定义 base_url
  - `LOBSTER_LOCAL_BRIDGE_BASE_URL`（默认 `http://127.0.0.1:18091`）

## 对外接口（函数）

- `skill_local_lobster_skills_list()`：调用 `/api/trae/skills/list` 并校验 `skills` 为数组，落盘取证
- `skill_local_lobster_skills_health()`：调用 `/api/trae/skills/health`，落盘取证
- `skill_local_lobster_publish_acceptance()`：一键跑 health + list，并生成验收摘要（JSON）

## 审计与产物

- 落盘目录：本技能目录下 `.lobster_state/reports/`
- 审计内容：时间戳、URL、authorization_present、HTTP 状态码、响应体摘要、校验结果（不含任何 Token 明文）

