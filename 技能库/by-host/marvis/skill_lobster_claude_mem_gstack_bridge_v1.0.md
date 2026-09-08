# lobster_claude_mem_gstack_bridge_v1.0
# 记忆栈桥接同步技能

---
name: lobster_claude_mem_gstack_bridge_v1.0
version: "1.0"
description: |
  龙虾AI记忆栈桥接同步技能。管理 WorkBuddy / Claude Code 与本地
  mem_gstack 知识库之间的双向记忆同步，实现跨会话长期记忆持久化。
  覆盖：记忆读写、四层记忆架构管理、双智能体同步、Bridge健康检查、
  记忆蒸馏与归档。
tags:
  - lobster
  - memory
  - bridge
  - persistence
  - mem_gstack
agent_created: true
---

## 记忆栈桥接同步技能 — lobster_claude_mem_gstack_bridge_v1.0

---

### 0. 技能概述

本技能是龙虾AI主控中心的**记忆持久化核心**，解决AI会话结束后知识丢失的问题：

```
会话开始 → 读取历史记忆 → 执行任务 → 写入新记忆 → 会话结束
              ↑                                    ↓
         Bridge/MEMORY.md ←─────────── 记忆蒸馏归档
```

---

### 1. 记忆四层架构（完整版）

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: 工作记忆（Session Working Memory）                  │
│  范围: 当前会话，内存中，会话结束即销毁                          │
│  工具: 对话上下文                                              │
│  触发持久化: 任务完成/用户要求/会话结束前                         │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: 日常记忆（Daily Log）                                │
│  路径: .workbuddy/memory/YYYY-MM-DD.md                       │
│  格式: Append-only Markdown，按时间倒序                        │
│  保留: 30天，超期自动蒸馏至 Layer 3                             │
│  写入规则: 追加(append)，禁止覆盖历史条目                        │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: 长期记忆（Curated Long-term Memory）                │
│  路径: .workbuddy/memory/MEMORY.md                           │
│  格式: 主题化精华，按类别组织                                    │
│  更新规则: In-place 更新，记录变更原因和日期                     │
│  内容: 技术决策、用户偏好、踩坑经验、架构规范                     │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: 知识库（mem_gstack Vector Store）                   │
│  服务: Bridge Server (port 18091)                            │
│  能力: 语义向量检索，跨智能体共享                                │
│  路径: E:\大道量化\一人一公司\云端知识库\                        │
└─────────────────────────────────────────────────────────────┘
```

---

### 2. Bridge 服务配置（本机自适配）

```yaml
bridge_url: http://localhost:18091
qr_endpoint: http://localhost:18091/qrcode
welcome_page: http://localhost:18091/welcome.html
health_check: http://localhost:18091/health
service_dir: C:\Users\Administrator\bridge_service\
startup_cmd: python bridge_server.py
```

**Bridge 状态检查**：
```bash
# 检查服务是否在线
curl -s http://localhost:18091/health

# 如未启动，进入目录启动
cd C:\Users\Administrator\bridge_service
python bridge_server.py

# 验证二维码页面可访问
start http://localhost:18091/welcome.html
```

---

### 3. 记忆读写操作规范

#### 3.1 读取记忆（Session Start）

```bash
# 优先读取顺序：
1. .workbuddy/memory/MEMORY.md       (长期记忆)
2. .workbuddy/memory/YYYY-MM-DD.md   (今日日志)
3. .workbuddy/memory/YYYY-MM-[DD-1].md (昨日日志，如相关)

# Bridge API 语义检索（如服务在线）
GET http://localhost:18091/memory/query?q=<关键词>&limit=10
```

#### 3.2 写入记忆（Session End / Task Complete）

**日常记录（追加到今日文件）**：
```markdown
## HH:MM — <任务标题>

**执行内容**: <一句话描述>
**关键产出**: <文件路径/数量/指标>
**踩坑/决策**: <如有>
**后续**: <下次需要继续的内容>
```

**长期知识更新（MEMORY.md in-place）**：
```markdown
## 更新 YYYY-MM-DD

### <主题>
- <知识点>: <内容>（更新原因: <xxx>）
```

#### 3.3 记忆写入触发条件

| 条件 | 优先级 | 目标文件 |
|------|--------|---------|
| 工具调用 ≥ 8 次的复杂任务 | 必须 | 今日日志 |
| 发现新技术规律/踩坑经验 | 必须 | MEMORY.md |
| 用户明确要求记录 | 必须 | 用户指定 |
| 修改了关键配置（端口/路径/密钥） | 必须 | MEMORY.md |
| 安装了新工具或依赖 | 建议 | 今日日志 |
| 轻量查询/简单问答 | 跳过 | — |

---

### 4. 双智能体同步协议（WorkBuddy ↔ 豆包）

```
同步场景:
  WorkBuddy 完成策略迭代 → 写入知识库 → 豆包下次读取时获得
  豆包生成策略参数 → 写入知识库 → WorkBuddy 执行时读取

同步机制:
  共享路径: E:\大道量化\一人一公司\云端知识库\
  同步文件格式: <智能体名>_<日期>_<主题>.md
  示例: workbuddy_2026-05-22_btc_strategy_iteration.md

冲突处理:
  同一文件同时写入 → 后写者追加，不覆盖
  版本标识: 每条记录头部加 [WorkBuddy|Doubao] 标签
```

---

### 5. 记忆蒸馏规则（30天归档）

**触发条件**：日常记录文件超过30天

**蒸馏步骤**：
```
1. 读取所有超期日志文件（*.md，日期 < 今日-30天）
2. 按主题分类提取核心知识点
3. 合并写入 MEMORY.md 对应章节（in-place更新）
4. 验证 MEMORY.md 内容完整性
5. 删除已蒸馏的原始日志文件（先备份至 archive/）
```

**蒸馏分类模板**：
```markdown
## 技术配置与环境
## 量化策略知识
## 工具链操作经验
## 踩坑记录与解决方案
## 用户偏好与约定
```

---

### 6. 记忆优先级评分（1-5分，用于 Bridge 向量库）

| 分值 | 分类 | 保留期 | 示例 |
|------|------|--------|------|
| 5 ⭐⭐⭐⭐⭐ | 架构决策 | 永久 | 端口变更、服务迁移、系统重构 |
| 4 ⭐⭐⭐⭐ | 踩坑经验 | 1年 | 调试根因、错误解决方案 |
| 3 ⭐⭐⭐ | 配置偏好 | 6个月 | 用户习惯、工具设置、路径约定 |
| 2 ⭐⭐ | 任务记录 | 30天 | 今日完成的具体工作 |
| 1 ⭐ | 临时信息 | 7天 | 中间结果、临时路径、一次性数据 |

---

### 7. 故障排查树（完整版）

```
记忆读取失败？
├── 日常文件不存在
│   └── 创建 .workbuddy/memory/YYYY-MM-DD.md → 写入初始内容
├── MEMORY.md 损坏/乱码
│   └── 检查备份 → 从最近日志重新蒸馏
├── Bridge 服务不在线 (18091)
│   ├── 检查进程: netstat -ano | findstr :18091
│   ├── 启动服务: cd bridge_service && python bridge_server.py
│   └── 服务目录不存在 → 提示晋峰确认 bridge_service 路径
└── Bridge Token 过期
    └── 打开 http://localhost:18091/welcome.html 重新扫码

记忆写入失败？
├── 文件路径不存在
│   └── mkdir -p 创建目录 → 重新写入
├── 文件权限错误
│   └── 提示以管理员运行 → 检查 NTFS 权限
└── 磁盘空间不足
    └── 报告 E: 盘剩余空间 → 建议清理旧日志
```

---

### 8. 关键路径汇总（本机自适配）

```yaml
# 工作记忆目录（动态，随任务workspace变化）
working_memory: <workspace>\.workbuddy\memory\

# 固定路径
long_term_memory: C:\Users\Administrator\.workbuddy\memory\MEMORY.md
cloud_knowledge_base: E:\大道量化\一人一公司\云端知识库\
bridge_service: C:\Users\Administrator\bridge_service\
archive_dir: C:\Users\Administrator\.workbuddy\memory\archive\

# 文件命名规范
daily_log: YYYY-MM-DD.md         # 例: 2026-05-22.md
sync_file: <agent>_<date>_<topic>.md  # 例: workbuddy_2026-05-22_deploy.md
```
