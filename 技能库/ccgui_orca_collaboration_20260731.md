---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_4a755b3d8cb811f19f65525400e6dd8f
    ReservedCode1: FBwIPRP8cYtGGnJcyJQYMncS5D2+/VghX0ORr9jUmMWxvZO1CeVwuhBtQjUsMqDlXnhP3S63pvjOw6C8sBDF7vWLQPwme5kXleXBV5UVPxXA6l+fps1XI30Pnja6gno+FNM5OJckektPMn0kUfo9CeZ43obP7jrldMNvR0Z1REDO7eUpaHVn1NwGZVc=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_4a755b3d8cb811f19f65525400e6dd8f
    ReservedCode2: FBwIPRP8cYtGGnJcyJQYMncS5D2+/VghX0ORr9jUmMWxvZO1CeVwuhBtQjUsMqDlXnhP3S63pvjOw6C8sBDF7vWLQPwme5kXleXBV5UVPxXA6l+fps1XI30Pnja6gno+FNM5OJckektPMn0kUfo9CeZ43obP7jrldMNvR0Z1REDO7eUpaHVn1NwGZVc=
---

# CCGUI × ORCA 联手方案：1+1>2

> 时间：2026-07-31 16:15
> 任务：分析 CCGUI 与 ORCA 优缺点，设计互补协作方案

---

## 一、CCGUI 与 ORCA 核心对比

| 维度 | CCGUI | ORCA |
|------|-------|------|
| **形态** | 桌面 GUI + WebView 界面 | 纯 CLI / 终端 Agent 舰队 |
| **优势** | 可视化对话框、插件扩展、截图、多引擎切换、项目管理 UI | 高并发（8+ 实例）、自动化编排、直接文件操作、无 UI 开销 |
| **劣势** | 配置脆弱易回写、WebView 交互不稳定、单线程交互 | 无可视化、需手动管理进程、不适合人工交互 |
| **引擎** | Claude Code / Codex CLI / OpenCode (Hermes) | Claude ×1 / Codex ×4 / Hermes ×3 |
| **适用场景** | 人工交互式开发、可视化项目管理、截图分享 | 批量自动化任务、后台持续运行、舰队协作 |
| **稳定性** | 依赖 settings.json 完整性，易被回写破坏 | 独立进程，配置修改不互扰 |

---

## 二、联手方案：1+1>2

### 2.1 三引擎对话 + 舰队执行
```
CCGUI（对话层）              ORCA（执行层）
    │                            │
    ├─ Claude Code ──────评审代码──→ Claude CLI
    ├─ Codex CLI ───────编写代码──→ Codex CLI ×4
    └─ OpenCode(Hermes) ──创意构思──→ Hermes ×3
```

**工作流**：
1. CCGUI 用 Claude Code 评审需求 → 输出任务拆解
2. CCGUI 用 OpenCode 构思方案 → 生成架构设计
3. ORCA Codex ×4 并行实现各模块
4. CCGUI 用 Codex 汇总验证 → 输出最终结果

### 2.2 插件 + 截图赋能
- CCGUI 插件生态（市场/拓展）可扩展 OCR、图片生成、数据库可视化等
- 对话框截图可直接分享给 ORCA Agent 做上下文参考
- ORCA 处理复杂的后台任务，CCGUI 负责前端展示和交互

### 2.3 一键拉起规范
```powershell
# 启动 ORCA（8个Agent舰队）→ 再启动 CCGUI → 正常可用
# ORCA 通过各自 CLI 独立运行，CCGUI 通过 settings.json 配置接入
# 两者共用同一个项目工作树：E:\龙虾AI主控中心\我的AI分身\
```

### 2.4 沙盒隔离原则
- CCGUI 修改 settings.json → 不影响 ORCA 的 CLI 进程
- ORCA 重启/配置变更 → 不影响 CCGUI 的 GUI 界面
- 共用模型（mimo-v2.5-pro）→ 无需额外配置

---

## 三、经验总结

1. **不要老修配置**：settings.json 修复集中在 modelId 锁定，一次性搞定后通过回滚节点固化为稳定快照。
2. **CCGUI 回写行为**：重启后可能清除非活跃引擎条目，需在修复时三引擎同步补齐。
3. **ORCA 保护**：settings.json 修改不涉及 ORCA 的任何 CLI 命令或进程。
4. **故障分级**：区分 CCGUI 前端问题（modelId 错误）和 Codex GitHub 同步问题（gh 未登录），不要混合处理。
*（内容由AI生成，仅供参考）*
