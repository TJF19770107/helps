---
name: "lobster_ai_bridge_universal_v1.0"
description: "通用AI服务桥接模板：归一化状态码/响应格式/超时，零侵入打通端到端链路。Invoke when 上游(如Hermes)返回202等导致下游(如豆包/桥接)误判失败。"
---

# 通用 AI 桥接标准化技能（Universal Bridge）

## 1) 【核心能力定义】

- 功能：作为中间桥接层，为下游客户端（如豆包）统一标准化上游 AI 服务（如 Hermes）的接口返回，解决状态码不匹配、响应格式差异、链路超时等问题。
- 目标：端口与拓扑不动，只通过“桥接层最小补丁”完成端到端闭环。
- 本次应用场景：Hermes `POST /v1/runs` 返回 `202 Accepted` 属正常语义（已受理异步执行），桥接侧将其归一化为 `200 OK`，确保下游无感知、无误判。

## 2) 【本次关键补丁：状态码归一化】

### 修复点

- 文件：`docker/doubao_bridge/bridge_service.py`
- 函数：`_start_hermes_run`
- 原逻辑（隐患）：只认 200，会把 202 误判为失败

```python
def _start_hermes_run(...):
    \"\"\"启动 Hermes run：POST /v1/runs，并返回 run_id。\"\"\"
    r = SESSION.post(url, headers=headers, json=payload, timeout=20)
    if r.status_code != 200:
        raise Exception(f\"上游请求失败，状态码：{r.status_code}\")
```

### 修复后逻辑（兼容并归一化）

```python
def _start_hermes_run(...):
    \"\"\"兼容上游 202，并在桥接侧归一化为 200，避免下游误判。\"\"\"
    r = SESSION.post(url, headers=headers, json=payload, timeout=20)
    if r.status_code not in (200, 202):
        raise Exception(f\"上游请求失败，状态码：{r.status_code}\")
    # 统一对外返回 200（桥接内部口径）
    r.status_code = 200
```

### 单行最小改动版本（推荐用于“只动一行”场景）

```python
def _start_hermes_run(...):
    \"\"\"单行补丁：将 202 直接映射为 200，保持后续只认 200 的唯一判定。\"\"\"
    r = SESSION.post(url, headers=headers, json=payload, timeout=20); r.status_code = 200 if r.status_code == 202 else r.status_code
    if r.status_code != 200:
        ...
```

## 通用扩展模块（模板）

### A. 响应格式归一化（Schema Normalize）

```python
def normalize_json(payload: dict) -> dict:
    \"\"\"将上游 JSON 映射为桥接层统一结构，避免下游绑定上游细节。\"\"\"
    run_id = payload.get('run_id') or payload.get('id') or ''
    return {'ok': True, 'id': run_id, 'data': payload}
```

### B. 超时与长连接（Timeout/SSE）

```python
def sse_timeouts(run_timeout_s: int) -> tuple[int, int]:
    \"\"\"返回 (connect_timeout_s, read_timeout_s)，用于 requests 的 timeout=(c,r) 形式。\"\"\"
    return 10, max(30, int(run_timeout_s) + 5)
```

## 验收口径（端到端）

- 上游保持原语义：`POST http://127.0.0.1:6060/v1/runs` 返回 202 允许存在。
- 桥接内部归一化后：桥接侧判定只保留 `status_code == 200` 且能取到 `run_id`。

## 回滚口径

- 只撤销 `_start_hermes_run` 中的“202→200”归一化单行，即回到原行为。
