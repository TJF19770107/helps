
---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: hermes_seven_layer_20260615
---
# Hermes 七层可编程架构

> **版本**：v1.0 · 2026-06-15
> **生效范围**：Hermes 容器化 AI 服务
> **依赖**：龙虾全域官方模板 v3.85 · 龙虾五步法 v2.1 · 克劳德七层可编程架构官方标准
> **注意**：本文档为 Hermes 的七层架构描述，不修改 Hermes 运行配置

---

## Hermes 角色定位

Hermes 是**容器化 AI 推理服务**，运行在 Docker 环境中，通过 MCP/gRPC 协议对外提供批量模型推理、数据分析、隔离环境执行等能力。在三系统（Codex / Claude Code / Hermes）协作中，Hermes 承担**计算密集型处理 + 隔离沙箱执行**角色。

---

## Layer 7: Verifiers — 验证闭环

> **五步法映射**：S6 ITERATE 迭代反馈 + S7 ARCHIVE 归档验证

### 7.1 Hermes 验证职责

| 验证维度 | 校验方法 | 触发时机 | 不通过动作 |
|---------|---------|---------|-----------|
| **推理结果一致性** | 多次推理交叉验证 | 每次推理完成 | 标记低置信度 |
| **资源使用合规** | CPU/内存/GPU 监控 | 每次任务执行 | 超限告警 → 限流 |
| **输出格式合规** | Schema 校验 | 结果返回前 | 拒绝输出 + 重试 |
| **安全合规** | 输出内容安全扫描 | 结果返回前 | 拦截 + 脱敏 |

### 7.2 容器健康检查

```
Health Check 周期: 30秒
检查项:
  - 服务存活 (HTTP 200)
  - GPU 显存使用率 ≤90%
  - 推理队列深度 ≤100
  - 平均推理延迟 ≤目标值 120%
```

---

## Layer 6: Subagents — 隔离工作者

> **五步法映射**：S4 EXECUTE — 多 Agent 协作

### 6.1 Hermes 子服务矩阵

| 子服务 | 职责 | 容器化方式 | 资源配额 |
|-------|------|-----------|---------|
| **Inference Worker** | 模型推理执行 | Docker Container ×N | GPU 1卡 / 内存 16GB |
| **Data Processor** | 批量数据预处理 | Docker Container ×2 | CPU 4核 / 内存 8GB |
| **Result Aggregator** | 结果聚合与格式化 | 主容器内含 | CPU 2核 / 内存 4GB |
| **Health Monitor** | 健康检查与自动重启 | Sidecar | CPU 1核 / 内存 1GB |

### 6.2 调度策略

```
请求入站
    ↓
负载均衡 (Round-Robin)
    ↓
├─→ Inference Worker 1  (GPU 0)
├─→ Inference Worker 2  (GPU 1)
└─→ Inference Worker 3  (GPU 2)
    ↓
Result Aggregator
    ↓
响应出站
```

---

## Layer 5: Hooks — 拦截回调器

> **五步法映射**：安全/风控全流程拦截

### 5.1 Hermes 安全 Hook

| Hook 注入点 | 拦截规则 | 触发动作 |
|------------|---------|---------|
| **请求入站前** | 认证 Token 校验 | 无有效Token → 401 |
| **推理执行前** | 输入内容安全扫描 | 含敏感指令 → 拒绝 |
| **结果输出前** | 输出内容合规检查 | 含违规内容 → 脱敏/阻断 |
| **资源超限时** | CPU/GPU/内存阈值 | 自动限流 → 告警 |
| **容器异常时** | 崩溃/僵死检测 | 自动重启 → 日志记录 |

### 5.2 访问控制

| 角色 | 权限 | 鉴权方式 |
|------|------|---------|
| **Master** (龙虾主控) | 全量推理 + 管理 | API Key + IP 白名单 |
| **Codex** | 策略推理请求 | API Key |
| **Claude Code** | 技术分析请求 | API Key |
| **External** | 受限推理 | API Key + 速率限制 |

---

## Layer 4: Skills — 按需加载方法论

> **五步法映射**：S3 GENERATE — 方案生成方法库

### 4.1 Hermes 内置能力模块

| 能力模块 | 加载方式 | 适用场景 |
|---------|---------|---------|
| **Batch Inference** | 请求参数指定 `mode=batch` | 大批量数据推理 |
| **Streaming Response** | 请求参数指定 `stream=true` | 流式输出场景 |
| **Multi-Model Ensemble** | 请求参数指定 `models=[...]` | 多模型投票/融合 |
| **Sandbox Execution** | 独立容器执行 | 不受信任代码隔离运行 |

---

## Layer 3: Tools / MCP — 赋予动作能力

> **五步法映射**：S2 COLLECT — 数据采集与工具调用

### 3.1 Hermes 对外接口

| 接口协议 | 端点 | 功能 | 调用方 |
|---------|------|------|-------|
| **gRPC** | `hermes:50051` | 高性能推理请求 | Codex / Claude Code |
| **REST API** | `hermes:8080/api/v1/infer` | 标准推理接口 | 外部系统 |
| **MCP** | `hermes-mcp` | MCP协议工具接入 | CC Switch |

### 3.2 MCP 工具接入

| MCP 工具 | 提供方 | 功能 |
|---------|-------|------|
| `hermes.infer` | Hermes | 发起推理请求 |
| `hermes.status` | Hermes | 查询服务状态 |
| `hermes.models` | Hermes | 列出可用模型 |
| `hermes.sandbox` | Hermes | 创建隔离执行环境 |

---

## Layer 2: CLAUDE.md / Rules — 行为规范

> **五步法映射**：S1 DEFINE — 角色与规则定义

### 2.1 Hermes 运行规则

| 规则类别 | 具体约束 |
|---------|---------|
| **端口绑定** | gRPC:50051 / HTTP:8080 / Metrics:9090 |
| **资源上限** | GPU ≤4卡 / 内存 ≤64GB / CPU ≤16核 |
| **请求限制** | 单次推理 max_tokens ≤32768 / batch_size ≤128 |
| **超时设置** | 推理超时 300秒 / 连接超时 60秒 |
| **日志保留** | 标准输出 7天 / 错误日志 30天 |
| **自动重启** | 健康检查失败3次 → Docker restart |

---

## Layer 1: 对话写代码 — 表层交互入口

> **五步法映射**：S1 DEFINE — 入口
> ⚠️ Hermes 作为后端服务，Layer 1 由调用方（Codex / Claude Code）的对话层提供，Hermes 自身不暴露对话界面

### 1.1 Hermes 的"入口"特质

Hermes 的 Layer 1 不是传统意义上的对话界面，而是**API 入口**：

| 入口形式 | 调用方 | 典型请求 |
|---------|-------|---------|
| gRPC 调用 | Codex 回测子Agent | "执行这组策略参数的回测" |
| REST API | Claude Code 分析Agent | "分析这段代码的安全风险" |
| MCP 工具 | CC Switch | "创建隔离沙箱执行不可信代码" |

---

## 五步法嵌入映射

| 五步法步骤 | Hermes 角色 | 核心动作 |
|-----------|-----------|---------|
| S1 DEFINE | 接收来自主控中心的任务定义 | 解析请求参数 |
| S2 COLLECT | 数据预处理 + 信息汇聚 | 批量数据清洗 |
| S3 GENERATE | 多模型推理 → 方案生成 | 模型推理执行 |
| S4 EXECUTE | 隔离沙箱执行 + 子Agent并行 | 容器化并行推理 |
| S5 SOLIDIFY | 推理日志 + 经验固化 | 结果持久化存储 |
| S6 ITERATE | 一致性校验 + 反馈闭环 | 多次推理交叉验证 |
| S7 ARCHIVE | 推理结果归档 | 四层归档存储 |

---

**版本信息**
- 版本: v1.0
- 创建日期: 2026-06-15
- 维护者: 龙虾AI主控中心
- 兼容平台: Hermes (Docker Containerized)
- 参考标准: 克劳德七层可编程架构官方标准 + 龙虾全域官方模板 v3.85
