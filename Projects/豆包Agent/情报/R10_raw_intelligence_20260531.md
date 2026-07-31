# R10 原始情报采集 · 2026-05-31
## 12路情报源 · 6大方向 · 40+信源覆盖

---

## 一、多Agent架构最新进展（2026年5月）

### 1.1 Hermes v0.15.0（2026-05-29 · NousResearch）

| 维度 | 详情 |
|------|------|
| 代码精简 | 16083行 → 3821行（76%），14个高内聚模块 |
| 冷启动 | Termux 0.8s，hermes --version 258ms（↑63%） |
| 会话搜索 | session_search 20ms（4500x加速），零成本本地过滤 |
| Kanban Swarm | 协调者+并行工作者+独立校验+合成节点，单任务模型覆盖，定时启动 |
| 安全防御 | Brainworm主动威胁防御，3卡口流量过滤+边界标记 |
| 密钥管理 | Bitwarden统一托管所有云端API密钥 |
| MCP目录 | Nous官方MCP服务目录交互式安装面板 |
| xAI生态 | xAI Web Search插件，hermes proxy打通Grok执行引导 |
| v0.15.1补丁 | 401无限重载修复，Docker npx路径修复，SIGTERM看板终止修复 |

**对标启示**：76%代码精简标杆，脑虫防御三卡口机制可直接移植。

### 1.2 Claude Agent Teams（2026-05-15 · Anthropic）

| 组件 | 职责 |
|------|------|
| Team Lead | 主会话创建团队、生成队友、协调 |
| Teammates | 独立Claude实例，自己认领任务 |
| Shared Task List | 自协调任务列表 |
| Mailbox | 队友间直接消息传递 |

- 显示模式：auto / in-process / tmux
- 每个teammate独立上下文窗口
- Token成本更高，适合需Agent间讨论的复杂工作

### 1.3 多Agent新玩法：Hermes引擎（2026-05-01）

- 一套代码运行多个互相隔离Agent实例
- 每个Agent独立profile目录（配置/记忆/会话）
- systemd service各自独立运行
- 多Agent互相看守：改错网关→另一个Agent修复

---

## 二、MCP/ACP/A2A网关协议（2026 Q1-Q2）

### 2.1 三层协议架构（Zylos Research · 2026-03-26）

| 层级 | 协议 | 厂商 | 用途 |
|------|------|------|------|
| L1 工具集成（垂直） | MCP | Anthropic | Agent↔工具/数据源 |
| L2 Agent协调（水平） | A2A | Google | Agent↔Agent跨框架 |
| L3 身份信任（横切） | OAuth2.1+DID | 多厂商 | 身份、审计、凭据 |

- 全部纳入Linux Foundation AAIF治理
- MCP: 18,000+社区服务器，月下载量数千万
- A2A: 企业伙伴广泛参与
- ACP(IBM/AGNTCY): REST原生，最小摩擦

### 2.2 MCP关键更新

- **Streamable HTTP**：单端点/mcp，支持无状态部署（K8s/Serverless/Cloudflare Workers）
- **OAuth 2.1 + Resource Indicators (RFC 8707)**：防令牌泄露
- **Tool Annotations**：readOnly/destructive/idempotent/openWorld 标注
- **Q3 2026**：MCP/A2A联合规范计划

### 2.3 战略架构决策

```
MCP（垂直工具层）  +  A2A（水平协调层）
     ↓                      ↓
  Agent↔工具              Agent↔Agent
     ↓                      ↓
  同一个Agent同时运行MCP和A2A = 生产基线
```

---

## 三、Workfoz劳动力市场（2026-05）

### 3.1 Workfoz核心机制

- 全球首个自主AI劳动力市场
- 雇主发布任务 → AI代理自动读取需求 → 竞标协商 → 完成交付
- 免费发布/寻找工作
- OpenClaw skill可下载
- 相比传统外包：效率更高、成本更低、无人力瓶颈

### 3.2 架构要点

| 要素 | 描述 |
|------|------|
| 任务发布 | Job vacancy: title + scope + daily tasks |
| 竞标 | AI Agent提交Bid，包含期望薪资 |
| 支付 | One-time payment，Confidence评分 |
| 技能 | 一键OpenClaw skill让AI代理自主工作 |

---

## 四、OpenClaw沙箱部署方案

### 4.1 四种沙箱方案对比

| 方案 | 隔离度 | 性能 | 复杂度 | 适用场景 |
|------|--------|------|--------|----------|
| Docker | 高 | 良好 | 中 | 通用Agent执行 |
| Firecracker MicroVM | 最高 | 一般 | 中 | 金融/敏感数据 |
| firejail/bubblewrap | 中 | 最好 | 低 | 轻量隔离 |
| WebAssembly | 高 | 好 | 中 | 浏览器端 |

### 4.2 Firecracker性能指标

- 启动 < 125ms
- 内存 < 5MB 开销
- 完全隔离
- 快照重置支持

### 4.3 安全配置要点

- 文件系统隔离（只读挂载+私有tmp）
- 网络白名单
- CPU/内存/执行时间限制
- 快照回滚：每次重置到干净状态

---

## 五、复杂任务调度与长周期管理

### 5.1 Temporal.io Replay 2026

- **Durable Execution**：代码永不失败
- 自动捕获每步状态
- 故障后从断点继续，无进度丢失
- Workflow + Activities 模式
- 原生SDK支持多语言
- 新特性：AI Agent构建、治理、可靠性

### 5.2 核心模式

```
Workflow（业务逻辑）
  ├── Activity 1（API调用） → 自动重试
  ├── Activity 2（数据处理） → 状态持久化
  ├── sleep(30天) → 可恢复
  └── Activity 3（结果聚合）
  
任何节点故障 → 从最近检查点恢复，无手动干预
```

---

## 六、自进化闭环系统

### 6.1 FORGE协议（2026-05-15 · arXiv 2605.16233）

| 维度 | 描述 |
|------|------|
| 全称 | Failure-Optimized Reflective Graduation and Evolution |
| 核心机制 | 群体广播式记忆进化，无权重更新 |
| 内循环 | Reflexion风格：失败→反思→生成规则/示例→重试 |
| 外循环 | 冠军记忆广播给所有实例（PBT exploit） |
| 毕业机制 | 超阈值→冻结记忆→退出训练→节省资源 |
| 验证任务 | CybORG CAGE-2网络防御（POMDP，30步） |

### 6.2 Group-Evolving Agents (GEA)（arXiv 2602.04837）

- 群体级元学习，自主发现高性能Agent配置
- 经验聚合和重用
- 无需人类干预
- 超越SOTA自进化方法，匹敌/超越人工设计框架
- 核心洞察：AI Agent可直接交换知识/工具/执行痕迹，不受生物生殖限制

### 6.3 群体进化 vs 个体进化

| 维度 | 个体进化 | 群体进化(GEA/FORGE) |
|------|----------|---------------------|
| 知识共享 | 无 | 冠军广播/经验池 |
| 探索效率 | 低（独立搜索） | 高（并行探索+共享） |
| 过拟合风险 | 高（单轨迹） | 低（多轨迹交叉验证） |
| 计算效率 | 可毕业冻结 | FORGE毕业+冻结双保险 |

---

## 七、NVIDIA Verified Skills（2026-05-19）

### 7.1 技能卡四步验证流程

```
编目(Catalog) → 扫描(Scan) → 评估(Assess) → 签名(Sign)
     ↓               ↓              ↓              ↓
  技能元数据      安全风险       能力有效性      加密签名
```

### 7.2 跨平台兼容

- 同一SKILL.md文件在Claude Code / Codex / Cursor均可运行
- 基于agentskill.io开放技能规范
- 技能卡记录：透明度、来源、安全验证、真实性

### 7.3 对标启示

- 豆包Agent技能库可直接对齐NVIDIA验证流程
- Skill Card标准化 = GAP-004可直接加速关闭
- agentskill.io规范为行业标准雏形

---

## 八、情报统计

| 维度 | 数值 |
|------|------|
| 核心情报源 | 12路并行检索 |
| 覆盖信源 | 40+ |
| 深度文章抓取 | 3篇（Zylos协议全景/NVIDIA技能验证/OpenClaw沙箱） |
| 学术论文 | 2篇（FORGE / GEA） |
| 产品发布 | 4个（Hermes v0.15 / Claude Agent Teams / Workfoz / Temporal Replay 2026） |
| 新识别缺口 | 待R10复盘确定 |

---
*采集时间：2026-05-31 · R10循环*