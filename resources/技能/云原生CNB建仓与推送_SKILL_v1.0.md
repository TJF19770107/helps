---
title: 云原生CNB建仓与推送
version: v1.0
distilled_at: 2026-09-08
distilled_by: 汤小龙（WorkBuddy）· 实战蒸馏 · 源自 lobster-knowledge-base 建仓全流程
tags: [CNB, 云原生, 建仓, OpenAPI, git推送, 零成本]
cost_mode: P0-本地零积分
---

# 云原生 CNB 建仓与推送 SKILL v1.0

> 一句话：**git 令牌 ≠ API 令牌**；建仓走 `POST https://api.cnb.cool/{group}/-/repos`，推送走「完整 clone + 清代理直连」。

## 一、建仓（OpenAPI，账户级 PAT）

```
POST https://api.cnb.cool/{group}/-/repos
Authorization: Bearer <账户级访问令牌>
Content-Type: application/json
{"name": "仓库名", "description": "...", "visibility": "private"}
成功 = HTTP 201
```

- group = 组织名（如 TJF19770107）。CNB 里「用户名」和「组织名」是两回事：`GET /user` 返回的 username 可能是 `cnb.xxxxxx`（账号 slug），仓库挂在组织 `TJF19770107` 名下
- 验证：`GET https://api.cnb.cool/user/repos?page=1&page_size=30` 列仓确认

## 二、三条实测坑（2026-09-08 全踩过）

1. **git 令牌 ≠ API 令牌**：remote URL 里嵌的 git 凭证（`cnb_at_` 前缀、orca 系 `cnb:5Srj...`）调 `api.cnb.cool` 全部 401/403；只有账户级 PAT（如 orca-jiedan 用的 `3VZT...`）能过 `/user` 并建仓。**先 `GET /user` 验 token 再动手**
2. **shallow clone 不能 push**：`! [remote rejected] shallow update not allowed` → 必须 `git clone`（完整）或 `git fetch --unshallow` 后再推
3. **国内站清代理直连**：全局 git 代理（socks5）会把 cnb.cool 也捆死 → 推送必须 `git -c http.proxy= -c https.proxy= push`；GitHub 才走 `socks5://127.0.0.1:1081`

## 三、标准流程（可直接复用）

```bash
# 1) 验 token
curl -s -H "Authorization: Bearer $TOKEN" https://api.cnb.cool/user
# 2) 建仓（已存在则 400/409，幂等忽略）
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"REPO","visibility":"private"}' https://api.cnb.cool/GROUP/-/repos
# 3) 完整 clone（海外镜像走代理）
git -c http.proxy=socks5://127.0.0.1:1081 clone --no-checkout https://github.com/GROUP/REPO.git
# 4) 推 CNB（清代理直连）
git -c http.proxy= -c https.proxy= push "https://GROUP:3VZT***@cnb.cool/GROUP/REPO.git" fresh-main:fresh-main
```

## 四、WorkBuddy 宿主备注

- WorkBuddy 的 `cnb-api` 连接器：**会话中途连接的工具不注入当次会话**，需新开会话才可调用 → 紧急场景用本技能 HTTP 直调 API 绕过
- 本地仓 `G:\tmp\lobster-knowledge-base`（shallow）与 `G:\tmp\lkb_full`（完整，推 CNB 用）双仓并存；后续知识库推送用 lkb_full
