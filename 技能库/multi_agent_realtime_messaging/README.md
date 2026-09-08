---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_6a66cbd4696911f1a0095254002afed2
    ReservedCode1: acK+Rp/SmDKF4xHumFETCGYMQX5IBZ1CFQqZ4y9iiyp7JJcqU8m1cREMZAxqLhj63nYXkh9LyZbj1KQ2Bv/Quf0aNVZ+EM2AwoL8RG0wKumhLmICkodCeLuZaOxvTwUyvUiZhhpbLLHM47mHI9d+DK1u1QITIJksDsIK3mxr7+2mgKLEQ2sFYgqsW3s=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_6a66cbd4696911f1a0095254002afed2
    ReservedCode2: acK+Rp/SmDKF4xHumFETCGYMQX5IBZ1CFQqZ4y9iiyp7JJcqU8m1cREMZAxqLhj63nYXkh9LyZbj1KQ2Bv/Quf0aNVZ+EM2AwoL8RG0wKumhLmICkodCeLuZaOxvTwUyvUiZhhpbLLHM47mHI9d+DK1u1QITIJksDsIK3mxr7+2mgKLEQ2sFYgqsW3s=
---

# 多智能体实时消息互通技能 (Multi-Agent Real-Time Messaging)

> **技能标识**：`multi_agent_realtime_messaging`
> **版本**：v3.0（2026-06-16）
> **激活咒语**：嗡阿喇巴札那谛
> **依赖**：龙虾双向桥接协议 v2.0 / MCP 协议 / GStack 标准工作流
> **生效范围**：Codex + Hermes + 豆包 + OpenClaw + Claude + Gemini + Marvis 全域统一

---

## 一、迭代过程：从 v1.0 到 v3.0

### 1.1 版本演进路线图

```
v1.0 (2026-05)          v2.0 (2026-06-01)       v2.5 (2026-06-15)       v3.0 (2026-06-16)
┌─────────────┐        ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│ 单向消息    │  ──→   │ 双向桥接    │  ──→   │ 多协议适配  │  ──→   │ 实时互通    │
│ 点对点      │        │ 请求-响应   │        │ MCP/A2A     │        │ 多Agent广播 │
│ 简单JSON    │        │ 结构化消息  │        │ 消息格式转换│        │ 事件订阅    │
└─────────────┘        └─────────────┘        └─────────────┘        └─────────────┘
```

### 1.2 各版本详细变更

| 版本 | 日期 | 核心变更 | 协议数 | 支持Agent |
|------|------|---------|--------|-----------|
| v1.0 | 2026-05-31 | 豆包Agent单向推送消息到Codex；JSON负载；无确认机制 | 1 | 豆包→Codex |
| v1.5 | 2026-06-01 | 新增Hermes接入；消息持久化到本地文件系统；消息重试队列 | 3 | +Hermes |
| v2.0 | 2026-06-05 | 双向桥接协议确立；结构化消息格式（source/target/action/payload/timestamp/trace_id）；GStack校验集成 | 7 | +Claude + OpenClaw |
| v2.5 | 2026-06-15 | MCP协议适配（SSE + Streamable HTTP）；消息格式转换层（JSON↔TOML↔Protobuf）；mimo-v2.5-pro升级支持 | 12 | +Gemini + Marvis |
| v3.0 | 2026-06-16 | 实时事件订阅/发布机制；多Agent广播；消息优先级队列；链路追踪OpenTelemetry；CodexPlusPlus v1.0兼容 | 15 | 全域Agent |

### 1.3 v2.5→v3.0 关键升级

1. **实时性**：从轮询模式升级为 SSE 推送 + WebSocket 双通道
2. **广播**：新增 `broadcast` action，一条消息同时触达所有在线 Agent
3. **优先级**：消息分为 HIGH / NORMAL / LOW 三级，HIGH 优先处理
4. **可观测**：集成 OpenTelemetry trace_id 全链路追踪
5. **兼容**：向后兼容 v2.0/v2.5 消息格式

---

## 二、完整实现逻辑

### 2.1 双向桥接协议架构

```
                          ┌─────────────────────────┐
                          │   龙虾AI主控中心          │
                          │  (Lobster Master Hub)    │
                          │                          │
                          │  ┌───────────────────┐   │
                          │  │  Message Router   │   │
                          │  │  (消息路由引擎)    │   │
                          │  └───────┬───────────┘   │
                          │          │               │
                          │  ┌───────┴───────────┐   │
                          │  │ Protocol Adapter  │   │
                          │  │ (协议适配层)       │   │
                          │  └───────┬───────────┘   │
                          │          │               │
                          │  ┌───────┴───────────┐   │
                          │  │  Format Converter │   │
                          │  │  (格式转换器)      │   │
                          │  └───────────────────┘   │
                          └─────────────────────────┘
                                       │
          ┌────────────┬───────────────┼───────────────┬────────────┐
          │            │               │               │            │
     ┌────┴────┐  ┌────┴────┐    ┌────┴────┐    ┌────┴────┐  ┌────┴────┐
     │ Codex   │  │ Hermes  │    │  豆包   │    │OpenClaw │  │ Claude  │
     │ :57321  │  │ :8642   │    │ :18000  │    │:28789   │  │ :cloud  │
     │ MCP SSE │  │ MCP SSE │    │HTTP Str │    │MCP SSE  │  │ API     │
     └─────────┘  └─────────┘    └─────────┘    └─────────┘  └─────────┘
```

### 2.2 消息路由机制

#### 2.2.1 消息结构

```json
{
  "version": "3.0",
  "message_id": "uuid-v7-format",
  "source": {
    "agent": "codex",
    "instance": "CodexPlusPlus-v1.0",
    "endpoint": "http://127.0.0.1:57321/v1"
  },
  "target": {
    "agent": "hermes",
    "routing": "direct",
    "priority": "HIGH"
  },
  "action": "execute|query|notify|broadcast|sync|evolve",
  "payload": {
    "skill": "lobster_task_standard_workflow_full_v2.1",
    "task": { },
    "context": { }
  },
  "metadata": {
    "trace_id": "0af7651916cd43dd8448eb211c80319c",
    "timestamp": "2026-06-16T12:00:00Z",
    "ttl_seconds": 3600,
    "retry_count": 0,
    "max_retries": 3
  },
  "gstack_checksum": "sha256:..."
}
```

#### 2.2.2 路由决策流程

```
收到消息
    │
    ├── 1. 校验 GStack checksum（防篡改）
    │
    ├── 2. 解析 target.agent + target.routing
    │
    ├── 3. 路由模式判断：
    │   ├── direct   → 直接转发到指定Agent端点
    │   ├── fanout   → 广播到所有在线Agent
    │   ├── round_robin → 轮询负载均衡（多实例）
    │   └── priority → 按优先级队列投递
    │
    ├── 4. 协议适配（将JSON转为目标Agent可理解的格式）
    │
    ├── 5. 投递消息 + 等待ACK（HIGH优先级）
    │
    └── 6. 写入消息日志（trace_id链路追踪）
```

#### 2.2.3 消息优先级队列

| 优先级 | 场景 | 超时 | 重试 | 确认 |
|--------|------|------|------|------|
| HIGH | 紧急任务、安全告警、回滚指令 | 10s | 3次 | 必须ACK |
| NORMAL | 常规任务、查询、同步 | 60s | 1次 | 可选ACK |
| LOW | 心跳、日志、非关键通知 | 120s | 0次 | 无ACK |

### 2.3 Agent间通信协议

#### 2.3.1 协议矩阵

```
                    Codex      Hermes     豆包     OpenClaw   Claude
Codex    (本地)     --         MCP/SSE    HTTP     MCP/SSE    REST
Hermes   MCP/SSE    --         --         HTTP     MCP/SSE    REST
豆包     HTTP/JSON   MCP/SSE    --         --       HTTP       REST
OpenClaw MCP/SSE    MCP/SSE    HTTP       --       MCP/SSE    REST
Claude   REST       REST       REST       REST     --         REST
```

#### 2.3.2 通信原语

| 原语 | 说明 | 同步/异步 | 使用场景 |
|------|------|-----------|---------|
| `execute` | 委托目标Agent执行任务 | 异步+回调 | 跨Agent任务分发 |
| `query` | 查询目标Agent状态/能力 | 同步 | 健康检查、能力发现 |
| `notify` | 单向通知 | 异步 | 事件通知、状态变更 |
| `broadcast` | 一对多广播 | 异步 | 全域唤醒、配置同步 |
| `sync` | 双向数据同步 | 同步 | 技能库同步、MEM更新 |
| `evolve` | 触发自进化流程 | 异步 | 迭代沉淀、技能升级 |

#### 2.3.3 错误处理与容错

```
发送消息
    │
    ├── 成功（HTTP 2xx / SSE connected）
    │   └── 记录 trace_id → 完成
    │
    ├── 超时（> TTL）
    │   └── 降级：写入文件消息队列 → Agent下次心跳时读取
    │
    ├── 拒绝（HTTP 4xx / 认证失败）
    │   └── 记录错误 → 通知主控中心 → 等待手动介入
    │
    └── 崩溃（连接中断 / HTTP 5xx）
        └── 重试（最多 3 次，指数退避 1s/2s/4s）
            │
            ├── 重试成功 → 正常处理
            └── 重试耗尽 → 切换到本地方案（API容错v2.1铁律）
```

---

## 三、扩展能力

### 3.1 新Agent接入规范

#### 3.1.1 接入四步法

```
Step 1: 注册发现
├── 向主控中心注册 Agent 元信息（名称/端点/协议/能力矩阵）
└── 心跳上报（每 30s）

Step 2: 协议握手
├── GStack 三方握手（参考 lobster_tripartite_handshake_v1.0）
└── 能力声明（支持的 action 列表 + 协议类型）

Step 3: 消息适配
├── 选择已有适配器 或 实现 ProtocolAdapter 接口
└── 通过格式转换器自动转换消息格式

Step 4: 验证上线
├── 发送测试 ping 消息
├── 验证 ACK 机制
└── 加入路由表
```

#### 3.1.2 新Agent注册示例

```json
{
  "register": {
    "agent_id": "marvis-agent-01",
    "agent_type": "marvis",
    "version": "1.0.0",
    "endpoint": "http://127.0.0.1:9570/v1",
    "protocols": ["mcp-sse", "rest"],
    "capabilities": {
      "actions": ["execute", "query", "notify"],
      "skills": ["file-ops", "desktop-ctrl", "search"],
      "max_concurrent_tasks": 5,
      "priority": "NORMAL"
    }
  }
}
```

### 3.2 多协议适配

源码参考：龙虾全域官方模板 v3.95 第 4 节双向桥接协议 v2.0。

#### 3.2.1 支持的传输协议

| 协议 | 适用场景 | 实现方式 | Agent |
|------|---------|---------|-------|
| MCP SSE | 本地Agent双向通信 | Server-Sent Events | Hermes, OpenClaw, Codex |
| MCP Streamable HTTP | 远程Agent / 云Agent | HTTP Streaming | 豆包 proxy, Ollama |
| REST / JSON | 云API调用 | HTTP POST + JSON | Claude, Gemini |
| WebSocket | 实时双向 | ws:// | 未来扩展 |
| File Queue | 离线/降级 | 本地JSON文件队列 | 全部（降级模式） |

#### 3.2.2 协议适配器接口

```
ProtocolAdapter Interface
├── connect(endpoint) → Connection
├── send(message) → Response
├── receive() → Message
├── disconnect()
└── health_check() → Status

├── MCPSseAdapter       # MCP SSE 协议
├── MCPStreamableAdapter # MCP Streamable HTTP
├── RestAdapter          # REST JSON
├── WebSocketAdapter     # WebSocket（规划中）
└── FileQueueAdapter     # 文件降级队列
```

### 3.3 消息格式转换

#### 3.3.1 转换矩阵

| 源格式 → 目标格式 | JSON | TOML | Protobuf | MCP |
|-------------------|------|------|----------|-----|
| JSON | 直通 | ✓ | ✓ | ✓ |
| TOML | ✓ | 直通 | ✓ | ✓ |
| Protobuf | ✓ | ✓ | 直通 | ✓ |
| MCP | ✓ | ✓ | N/A | 直通 |

#### 3.3.2 转换示例

**JSON → TOML**（用于Codex config.toml分发）：
```toml
# 由多Agent消息互通引擎自动生成
[message]
version = "3.0"
message_id = "0193827a-..."
action = "execute"
priority = "HIGH"

[source]
agent = "doubao"
instance = "DoubaoAgent-v99"

[target]
agent = "codex"
routing = "direct"
```

**JSON → Protobuf**（用于高性能场景）：
```protobuf
message AgentMessage {
  string version = 1;
  string message_id = 2;
  Agent source = 3;
  Agent target = 4;
  Action action = 5;
  bytes payload = 6;
  Metadata metadata = 7;
}
```

### 3.4 扩展性设计原则

1. **开闭原则**：新增Agent类型无需修改路由核心，只需添加适配器
2. **协议无关**：核心消息总线不依赖任何具体传输协议
3. **格式可插拔**：FormatConverter 支持注册新的转换器
4. **降级优先**：所有链路故障时自动降级到文件队列，不丢消息
5. **免费优先**：所有组件本地运行，零外部API依赖

---

## 四、部署与验证

### 4.1 当前部署状态

```
Agent 注册表（2026-06-16）
┌──────────────────────────────────────────────────────┐
│ Agent         │ 端点              │ 协议       │ 状态  │
├───────────────┼──────────────────┼───────────┼──────┤
│ CodexPlusPlus │ 127.0.0.1:57321  │ MCP/SSE   │ 🟢 UP │
│ doubao-proxy  │ 127.0.0.1:18000  │ HTTP Str  │ 🔴 DN │
│ hermes-agent  │ 127.0.0.1:8642   │ MCP/SSE   │ 🔴 DN │
│ ollama-local  │ 127.0.0.1:11434  │ HTTP Str  │ 🔴 DN │
│ openclaw-gw   │ 127.0.0.1:28789  │ MCP/SSE   │ 🔴 DN │
│ Claude        │ api.anthropic.com│ REST      │ ⚪ N/A│
│ Gemini        │ generativelang.. │ REST      │ ⚪ N/A│
│ Marvis        │ 本地集成          │ 内部      │ 🟢 UP │
└───────────────┴──────────────────┴───────────┴──────┘
```

> 详细连通性验证参见 [verification_report.md](verification_report.md)

### 4.2 快速启动（PowerShell）

```powershell
# 1. 检查当前在线Agent
Get-NetTCPConnection -State Listen | Where-Object {
    $_.LocalPort -in @(57321,18000,8642,11434,28789)
} | Format-Table LocalPort, State

# 2. 发送测试消息（通过Codex MCP）
# 参考 codex_dual_version_merge_template/README.md

# 3. 查看消息日志
Get-Content "E:\龙虾AI主控中心\我的AI分身\logs\message_$(Get-Date -Format 'yyyyMMdd').log"
```

---

## 五、关联资源

| 资源 | 路径 |
|------|------|
| 龙虾全域官方模板 v3.95 | `E:\龙虾AI主控中心\我的AI分身\技能库\龙虾全域官方模板-最终版.md` |
| 龙虾五步法 v2.1 | `E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_full_v2.0\SKILL.md` |
| 双向桥接协议 v2.0 | 全域模板第4节 |
| 三方握手协议 v1.0 | `lobster_tripartite_handshake_v1.0` |
| GStack标准工作流 | `gstack_standard_workflow_template_v1.0` |
| 连通性验证报告 | [verification_report.md](verification_report.md) |
| Codex双版本合并模板 | [../codex_dual_version_merge_template/README.md](../codex_dual_version_merge_template/README.md) |

---

> **版本履历**
> - v1.0 (2026-05-31)：豆包→Codex 单向消息
> - v1.5 (2026-06-01)：+Hermes +持久化 +重试队列
> - v2.0 (2026-06-05)：双向桥接 +GStack校验 +结构化消息
> - v2.5 (2026-06-15)：MCP适配 +格式转换 +mimo-v2.5-pro
> - v3.0 (2026-06-16)：实时事件 +广播 +优先级 +OpenTelemetry +CodexPlusPlus
*（内容由AI生成，仅供参考）*
