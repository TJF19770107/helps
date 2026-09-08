---
name: "cc_switch_precheck"
description: "cc-switch 启动前强制预检技能：自动遍历 cc-switch.db(provider_endpoints/providers/proxy_live_backup)、各 config.json、启动 BAT 脚本，检测所有 127.0.0.1:4567 本地转发地址是否携带 /v1 前缀，异常自动修复，前置拦截 404 故障。作为 cc_switch_4567_autofix 的预防性前置钩子。触发词：cc-switch预检、4567地址校验、/v1前缀检查、启动前校验、precheck"
version: "1.0"
date: "2026-07-19"
author: "WorkBuddy (lobster workflow)"
sync_mode: "forward"
primary_path: "E:\\龙虾AI主控中心\\我的AI分身\\技能库\\cc_switch_precheck\\SKILL.md"
depends_on: ["cc_switch_4567_autofix", "lobster_auto_iterate"]
---

# cc-switch 启动前强制预检技能 V1.0

## 目的
在 cc-switch 启动**之前**拦截导致 404 的根因：本地 4567 转发地址缺 `/v1` 前缀。
把"事后救火"变为"事前拦截"，杜绝同类故障重复发生。

## 校验规则（权威）
所有指向 AI Code Switch 的本地地址**必须**为 `http://127.0.0.1:4567/v1`：
- ✅ 正确：`http://127.0.0.1:4567/v1`
- ❌ 错误：`http://127.0.0.1:4567`（缺 /v1）
- ❌ 错误：`http://127.0.0.1:4567/opencode/v1`（多余路径）

## 自动校验脚本
位置：`E:\龙虾AI主控中心\我的AI分身\技能库\cc_switch_precheck\precheck.py`

```bash
python precheck.py --fix
```
- 不带 `--fix`：仅报告异常（dry-run）
- 带 `--fix`：发现异常自动修复并输出修复项

### 校验覆盖源
1. `E:\龙虾AI主控中心\CC-Switch\.cc-switch\cc-switch.db`
   - `provider_endpoints.url`
   - `providers.settings_config` (JSON 中 base_url / baseURL 字段)
   - `proxy_live_backup.original_config`
2. `E:\龙虾AI主控中心\CC-Switch\config.json`
3. `E:\龙虾AI主控中心\CC-Switch\.cc-switch\config.json`
4. 启动 BAT 脚本中出现的 `127.0.0.1:4567` 字样（提示人工核对）

### 退出码
- `0`：全部合规，可安全启动 cc-switch
- `1`：发现异常（dry-run 模式）
- `2`：已自动修复，需重启 cc-switch 生效

## 集成方式
作为 cc-switch 启动的**前置钩子**：任何启动脚本(BAT/计划任务)先调用
`precheck.py --fix`，退出码为 0/2 才继续启动 cc-switch。

---

## 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-07-19 | v1.0 | 从 cc-switch 404 故障专项补漏。启动前遍历DB/配置/BAT检测4567地址/v1前缀，异常自动修复前置拦截 |
