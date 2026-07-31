# OpenClaw Gateway 控制面架构

> **来源**: BayesianPersuasion + OpenClaw官方文档, 2026-05
> **豆包关联**: R02深度迭代报告
> **MOC**: [[_MOC_网关与协议]]

---

## Gateway核心架构

```
Gateway (ws://127.0.0.1:18789)
  ├── Channel Layer: 23+ 消息渠道 (WhatsApp/Telegram/Slack/Discord/...)
  ├── Binding Rules: 确定性路由 (channel, accountId, peer/guild → Agent)
  │     → 零LLM参与路由决策
  └── Agent Definition: SOUL.md + openclaw.json (声明式，无类继承)
```

## 关键设计决策

| 要素 | OpenClaw实现 | 可复用性 |
|------|-------------|---------|
| Agent声明式定义 | openclaw.json + SOUL.md | ✅ YAML配置 |
| 多Agent协调 | sub-agent (maxDepth 1-2, maxConcurrent 8) | ✅ 并行增强 |
| P2P通信 | agentToAgent + allow-lists | ✅ 白名单 |
| 记忆子系统 | SQLite FTS5 → LanceDB → 混合检索 | ✅ 三层对齐 |
| 插件系统 | 类型化/版本化/独占槽位 | ✅ 受控注册 |
| MCP集成 | v2026.3.25 MCP Host, 已验证7 Server | ✅ 立即对齐 |
| 技能市场 | ClawHub 5,400+ 技能 + VirusTotal安全扫描 | ✅ 参考 |

## 4100x性能飞跃核心

- **预缓存映射表**: 启动时预缓存provider auth-state, `/v1/models` 20s → 5ms
- **增量索引更新**: 非全量重建
- **Per-Sender Tool Policies**: 按发送者维度差异化策略

---

**标签**: #AI/网关 #OpenClaw #Gateway #MCP #agentToAgent