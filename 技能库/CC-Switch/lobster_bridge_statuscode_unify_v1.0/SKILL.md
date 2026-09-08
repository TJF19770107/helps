---
name: "lobster_bridge_statuscode_unify_v1.0"
description: "将 Hermes /v1/runs 上游 202 归一化为 200，避免桥接误判。Invoke when ai-bridge 调 Hermes 返回 202 导致流程中断或需要统一状态码口径。"
---

# 豆包桥接状态码归一化（202→200）

## 适用场景

- `ai-bridge` 调用 `Hermes WebUI(6060)` 的 `/v1/runs` 返回 202（Hermes 正常行为），但桥接侧仍按 `status_code == 200` 判定成功，导致误判失败/重试/中断。
- 要求最小改动，不改端口、不改容器拓扑、不改外部对接地址，只统一桥接内部状态码口径。

## 核心原则

- 上游行为不改：Hermes 仍可返回 202。
- 桥接侧归一化：将上游 202 在桥接内部统一映射为 200，然后只保留 `status_code == 200` 的唯一判定。
- 禁止泄露任何密钥：仅检查“是否已设置”，不输出值。

## 最小补丁（单行）

- 文件：`docker/doubao_bridge/bridge_service.py`
- 函数：`_start_hermes_run`
- 在发送 POST 后追加一行（可用分号合并到同一行）：
  - 将 `r.status_code == 202` 归一化为 `200`，其余保持不变。

## 验收口径

- `ai-bridge` 容器内调用 `_start_hermes_run(...)`：
  - `ok == True`
  - `detail["status_code"] == 200`
  - `detail["json"]["run_id"]` 存在
- `http://127.0.0.1:18091/bridge/health` 返回 200

## 回滚口径

- 将 `_start_hermes_run` 恢复为“未归一化”版本即可（仅撤销该单行改动）。
