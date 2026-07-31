---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_9c8e43e1649a11f1b8945254007bceed
    ReservedCode1: DgHPhr1C6BehSdfE8UPHZ14iN9FwAn4grf7fTPoYQzbL5uHTlXpqpGLznvzDQqUR2a6eh2SJKaZF6cOEMOeG25/IK14Up4tC1WSOzAW09R6K/3SDWArDvRoA7rw/fGgFvkptrjFI1I5dUsPXE7s1IBZTrcHwYdFKuzKOIp3TTUJQxcCpDWjywlFc9fM=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_9c8e43e1649a11f1b8945254007bceed
    ReservedCode2: DgHPhr1C6BehSdfE8UPHZ14iN9FwAn4grf7fTPoYQzbL5uHTlXpqpGLznvzDQqUR2a6eh2SJKaZF6cOEMOeG25/IK14Up4tC1WSOzAW09R6K/3SDWArDvRoA7rw/fGgFvkptrjFI1I5dUsPXE7s1IBZTrcHwYdFKuzKOIp3TTUJQxcCpDWjywlFc9fM=
---



# IETF MCPS-AGW 多Agent协作协议 · 深度分析

## 协议概述
IETF DMSC工作组草案（中国电信主导），定义基于Agent Gateway的多Agent协作协议套件。2026年处于草案阶段。

## 架构核心
- **Agent Gateway (AGW)**：作为网络一级实体，承担控制面协调角色
- **控制面/数据面分离**：Gateway管理注册/认证/路由/编排；Agent间P2P语义通信
- **最小权限授权**：基于能力的细粒度权限
- **会话范围语义通信**：解析后Agent直接建立语义会话

## 五大协议组件
| 协议 | 作用 | 核心机制 |
|------|------|---------|
| ARP | Agent注册 | 向本地Gateway注册，获取全局唯一Agent Identifier |
| AAAP | 认证授权 | 中央认证服务验证身份+授权操作范围 |
| CSP | 能力同步 | Gateway间交换能力摘要（非完整状态），增量更新 |
| SRRP | 语义路由 | 语义请求→能力匹配→多跳路由→P2P直连 |
| TIP | 任务编排 | 任务分解→子任务Agent匹配→多Agent协同调用 |

## 与豆包Agent协议对标
| IETF标准 | 已有协议 | 覆盖度 |
|---------|---------|:---:|
| ARP+AAAP | #16 Gateway微内核+#66 MCP安全纵深 | 90% |
| CSP | #6多Agent协同看板+#14多Agent知识图谱 | 85% |
| SRRP | #3 A2A+MCP三层协议栈 | 80% |
| TIP | #42 Swarm拓扑调度+#54千级并行编排 | 85% |

## 自进化四类闭环框架
- **L1 内建上下文闭环**：Hermes Agent / Agent Zero
- **L2 技能资产化闭环**：Darwin Skill / JiuwenClaw / EvoSkill
- **L3 群体智能闭环**：Ultron / OpenSpace / SkillClaw
- **L4 参数/代码/工作流自修改**：OpenClaw-RL / Agent Lightning
*（内容由AI生成，仅供参考）*
