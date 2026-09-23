---
name: lobster-llm-response-guard
description: >
  龙虾 LLM 响应守卫 v1.0。专治「HTTP 200 但正文是空的」—— 免费推理池（deepseek-v4-flash-free /
  glm-5.3-flash-free 等）的 reasoning_tokens 会吃光 max_tokens，导致 L3 传输层全绿、L4 内容层为空的
  典型假成功；同时静默超发 token 烧穿每日免费额度、静默替换 model 跳到收费档。
  触发词：LLM 返回空、content 为空、HTTP200 没内容、reasoning_tokens、max_tokens 超发、
  模型漂移、免费额度被烧、AI 写稿空白、推理模型、写完落盘是空的。
version: 1.0.0
agent_created: true
distilled_at: 2026-09-24
cost: 0（纯 stdlib，audit 模式完全不发请求）
---

# 龙虾 LLM 响应守卫 v1.0

> 归属：「假成功」**第 38 形态** —— 判定层错配在 LLM 调用面上的投影。
> 一句话：**HTTP 200 / rc=0 / JSON 合法，全都是 L3 传输层信号；正文内容才是 L4 结果态。用 L3 冒充 L4，就是假成功。**

## 一、什么时候必须用它

| 场景 | 不校验的后果 |
|---|---|
| 免费推理池写稿（Pixelle / 哪吒 / 改色 / 报价单） | 拿到空串继续往下跑，成片空白，交付事故 |
| 批量调用（批量出片 / 批量出图提示词） | 个别请求空白混进成品，抽检才发现 |
| 掐成本（零积分红线） | reasoning 超发 20~46 倍，每日免费额度半天烧穿，次日全部 402 |
| 换模型 / 网关故障转移 | 请求 `-free` 实际返回付费档，账单悄悄产生 |

**铁律：任何「拿 LLM 输出当交付物」的链路，落盘前必须过一次 L4 校验。**

## 二、七类反模式

| 码 | 名称 | 判据 | 级别 |
|---|---|---|---|
| V1 | EMPTY_CONTENT | HTTP 200 但 `content` 为空且无 tool_calls | **CRIT** |
| V2 | TRUNCATED | `finish_reason == "length"` | WARN |
| V3 | REASONING_OVERRUN | `reasoning_tokens / 请求max_tokens ≥ 10x` | **CRIT** |
| V3 | REASONING_DOMINANT | 推理占 `completion_tokens` ≥ 95% | WARN |
| V4 | MODEL_DRIFT | `resp_model` 跳出 `req_model` 家族（免费→付费） | **CRIT** |
| V4 | MODEL_SUBVERSION | 同族子版本变体（`-0731` / `-ga-260731`） | WARN |
| V5 | USAGE_MISSING / ZERO | 无 usage 或 completion_tokens=0 但正文非空 | WARN |
| V6 | NON_JSON_200 | HTTP 200 但 body 非 JSON（网关 HTML 伪装页） | **CRIT** |
| V7 | MOJIBAKE / ESCAPED | 正文含 ≥3 个替换符，或纯 `\uXXXX` 未解码 | WARN |

## 三、实测硬证据（2026-09-24，TeamoRouter 18091，`deepseek-v4-flash-free`）

同一句 prompt「用一句话说明什么是判定层错配。」，只改 max_tokens：

| max_tokens | HTTP | content | reasoning_tokens | completion_tokens | 耗时 | 判定 |
|---|---|---|---|---|---|---|
| 16 | 200 | **0 字（空）** | 16 | 16 | 3.9s | **CRIT：空正文** |
| 64 | 200 | 51 字 | 2918 | **2949（46.1x）** | 36.2s | **CRIT：超发** |
| 300 | 200 | 83 字 | 6754 | **6802（22.7x）** | 73.6s | 超发 |

额外抓到：`resp_model` 依次为 `deepseek-v4-flash-0731`、`deepseek-v4-flash-ga-260731`
—— **同一 slug 落到两个不同后端**，与请求名 `deepseek-v4-flash-free` 均不一致。

### 三条由此确立的结论

1. **推理模型的 `max_tokens` 是「输出上限」，不是「成本上限」。**
   reasoning_tokens 可以几十倍超发，且**同样计入免费额度**（额度按自然日刷新，耗尽返 402）。
2. **`max_tokens` 太小 → 推理直接吃光 → 返回空串还 HTTP 200。**
   这是最阴险的一种：不报错、不超时、退出码 0，只有 content 是空的。
3. **必须回读 `model` 字段。** 免费 slug 可能被换成同族变体（无害）或付费档（烧钱）。

## 四、用法

```bash
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
G="E:/龙虾AI主控中心/我的AI分身/企业微信群定制接单项目/scripts/llm_response_guard.py"

# 1) 在线体检（发一次真实请求，返回 CRIT 时退出码=1，可直接做 CI 门禁）
"$PY" "$G" check --model deepseek-v4-flash-free --max-tokens 16 \
        --json-out G:/WorkBuddy_Data/tmp/r.json

# 2) 离线判定已有响应（零成本，不发请求 —— 批量流水线推荐这条）
"$PY" "$G" audit --file r.json --req-model deepseek-v4-flash-free --req-max-tokens 16

# 3) 推理模型预算建议
"$PY" "$G" budget --expect-out 200

# 4) 自检（13 例，含 5 条防误报）
"$PY" "$G" selftest
```

参数：`--base`（默认 `http://127.0.0.1:18091/v1`）、`--key-env`（默认 `TEAMOROUTER_API_KEY`）、
`--min-content`（正文最短字数）、`--timeout`、`--json`（机器可读输出）。

**在流水线里挂载**（落盘前一道闸）：

```python
from llm_response_guard import judge
findings, verdict = judge(resp, req_model=model, req_max_tokens=mt)
if verdict == "CRIT":
    raise RuntimeError("L4 内容层校验失败，禁止落盘: %s" % findings)
```

## 五、防误报设计（第 11 形态：守卫自己造假失败）

守卫上线前必须先收敛自身误报，否则天天狼来了。本守卫 5 条豁免：

| 用例 | 处理 |
|---|---|
| content 空但存在 `tool_calls` | 函数调用场景合法 → 降级 INFO |
| `resp_model` 是 `req_model` 前缀延伸 | 同族子版本 → 只 WARN 不 CRIT |
| 非推理模型（无 reasoning 字段） | 不套 V3 超发规则 |
| reasoning 占比低的小预算调用 | 不报超发 |
| 完全健康的响应 | 零告警（OK） |

`selftest` **13/13 PASS**，其中 F01~F05 即上述防误报用例。
**改判据后必须重跑 selftest，且至少保留 3 条防误报用例。**

## 六、max_tokens 预算速查

| 期望正文 | 保守(20x) | 推荐(30x) | 实测上限(46x) |
|---|---|---|---|
| 100 token | 2000 | 3000 | 4600 |
| 200 token | 4000 | 6000 | 9200 |
| 500 token | 10000 | 15000 | 23000 |

反直觉但真实：**调大 max_tokens 不是浪费，调小才是**——小预算只会让你拿到空串，
且耗时随预算线性上升（实测 3.9s / 36.2s / 73.6s），要在「拿得到内容」和「别太慢」之间取平衡。

## 七、与其他守卫的联防

| 守卫 | 分工 |
|---|---|
| `verdict_layer_guard.py` | 通用判定层（L3/L4 抽象模型 + 代码反模式） |
| **`llm_response_guard.py`（本）** | **LLM 响应场景的具体化落地** |
| `cred_triage.py` | 凭据分层 —— 401/403 先跑它，别信报错文本 |
| `path_shadow_guard.py` | PATH 影子命令 —— `python` 必须用全路径 |

## 八、版本

- v1.0.0（2026-09-24）首版：七类反模式 + check/audit/budget/selftest 四子命令 + 13 例自检；
  沉淀第 38 形态；实测三条硬证据入库。
- 待办：接 `guard_receipt` 回执；批量模式（`audit --dir`）；把实测倍数做成可回灌的校准表。
