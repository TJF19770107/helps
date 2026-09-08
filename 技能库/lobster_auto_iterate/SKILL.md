---
name: "lobster_auto_iterate"
description: "龙虾全域强制迭代流水线 V1.0：任何任务/故障/商单交付完成后，自动执行「问题闭环校验→重复判定检索→软连接绑定→双端知识沉淀→多Agent同步」五步流水线，补齐龙虾五步法Step5缺失的自动触发逻辑。解决同类故障反复返工、历史案例无法留存复用的根因。触发词：迭代、沉淀、固化技能、重复故障、自动迭代、回执、知识沉淀、软连接更新"
version: "1.0"
date: "2026-07-19"
author: "WorkBuddy (lobster workflow)"
sync_mode: "forward"
primary_path: "E:\\龙虾AI主控中心\\我的AI分身\\技能库\\lobster_auto_iterate\\SKILL.md"
depends_on: ["lobster_task_standard_workflow_v2.7", "龙虾全域官方模板-最终版"]
consumed_by: "E:\\龙虾AI主控中心\\lobster_skill_solidify.py (每日00:10固化引擎)"
---

# 龙虾全域强制迭代流水线 V1.0

## 为什么需要本技能（根因说明）

龙虾五步法 V2.7 的 Step5「迭代沉淀」只是一段**描述性文字**，没有任何可执行触发器。
历史已存在固化消费端 `E:\龙虾AI主控中心\lobster_skill_solidify.py`（每日00:10运行，
读取 `state/issues_tracker.json` 的 `resolved` 列表并固化为 `skill_knowledge/*.json`），
但**生产者缺失**——没有任何逻辑在「问题修复完成」后把案例写入 `issues_tracker.json.resolved`。

结果：`issues_tracker.json.resolved` 自 2026-07-13 起长期为空，固化引擎无料可吃，
同类故障（如 cc-switch 404 转发缺 /v1 前缀）反复从零排查、反复推翻过往正确方案。

**本技能补齐生产者侧，形成完整闭环：**
```
问题修复完成 ──(本技能 Step1-2 写入)──▶ state/issues_tracker.json.resolved
                                        │
                          (每日00:10 固化引擎消费)
                                        ▼
                            skill_knowledge/*.json + 技能库软连接
```

---

## 流水线固定顺序（不可跳过）

### Step1 问题闭环校验（Producer 写入）
任务/故障交付后**立即**调用 `record_iteration.py`，将以下结构化数据写入
`E:\龙虾AI主控中心\state\issues_tracker.json` 的 `resolved` 数组：

```json
{
  "problem": "cc-switch 转发 Codex++ 请求到 4567 返回 404",
  "root_cause": "provider baseURL 缺 /v1 前缀，cc-switch 拼出 4567/responses 而非 4567/v1/responses",
  "solution": "UPDATE providers SET base_url='http://127.0.0.1:4567/v1' WHERE id='xiaomimimo20260612'",
  "category": "codex_link",
  "trigger_keywords": ["cc-switch 404", "127.0.0.1:4567转发", "baseURL缺失/v1", "provider_endpoints路由错误"],
  "tools": ["codex_fullchain_fix_v2.1.bat", "cc_switch_precheck"],
  "skill_package": "cc_switch_4567_autofix",
  "source_track": "WorkBuddy",
  "resolved_at": "2026-07-19T17:54:00",
  "iteration_required": true
}
```

**硬性约束**：不写 `issues_tracker.json` 视为任务未完成。禁止仅临时修复不固化。

### Step2 重复判定检索（Consumer 预判）
写入前先检索，判定场景：
- **场景A 全新问题**（知识库/技能库/Git 无同类）→ 生成独立技能包，存入技能库 + 追加至五步法/全域模板
- **场景B 历史同类但本次优化**（修正了过往错误方案）→ 覆盖迭代旧技能，更新历史文档，记录版本变更日志
- **场景C 完全重复无优化** → 直接调用存量技能自动处理，**禁止从零排查**

检索源（按优先级）：
1. `E:\龙虾AI主控中心\skill_knowledge\` (JSON 技能库)
2. `E:\龙虾AI主控中心\我的AI分身\技能库\` (技能库)
3. `E:\龙虾AI主控中心\Obsidian\` + `ObsidianVault\` (双 Obsidian 知识库)
4. 龙虾五步法 + 全域模板触发词索引
5. 私有 Git 仓库（共享技能库/分身技能库）

相似度 ≥ 80% 直接判定为重复，优先调用存量。

### Step3 软连接绑定更新
将新增/迭代的技能、脚本、配置与以下载体建立**永久软连接/索引**，使匹配关键词时自动联动：
- `lobster_task_standard_workflow_v2.7/SKILL.md`（五步法 Step5 引用）
- `龙虾全域官方模板-最终版.md`（触发词索引区）
- `E:\龙虾AI主控中心\我的AI分身\技能库\INDEX_技能库总索引_v1.0.txt`（总索引）
- `E:\龙虾AI主控中心\skill_knowledge\INDEX.jsonl`（机器可读索引）

绑定方式：在索引文件追加一行 `技能名|触发词|路径|版本`，而非复制文件（避免多副本漂移）。

### Step4 知识库双端沉淀
同步写入两端，生成可检索故障标签 + 触发关键词索引：
- **本地 Obsidian 双库**：`E:\龙虾AI主控中心\Obsidian\` 与 `E:\龙虾AI主控中心\ObsidianVault\`
  各新建/更新对应笔记，frontmatter 含 `tags: [cc-switch, 404, 4567, 龙虾五步法案例]`
- **私有 Git 仓库**：`E:\龙虾AI主控中心\技能库\` 或 `共享技能库\` 提交技能包
- 生成索引行写入 `skill_knowledge/INDEX.jsonl`

### Step5 多Agent同步
通知所有 Agent 加载迭代后内容（统一复用最新沉淀）：
- Codex / Claude Code / Hermes / OpenCode / OpenClaw / Marvis
- 同步机制：更新各 Agent 的 AGENTS.md / SOUL.md 引用指向最新技能版本
- 禁止各 Agent 私藏过期旧规则

---

## 配套脚本

### record_iteration.py（Producer 核心，补齐缺失环节）
位置：`E:\龙虾AI主控中心\我的AI分身\技能库\lobster_auto_iterate\record_iteration.py`

调用方式（在任务收尾时执行）：
```bash
python record_iteration.py \
  --problem "cc-switch 404 转发缺/v1" \
  --root_cause "baseURL缺/v1前缀" \
  --solution "UPDATE providers SET base_url='http://127.0.0.1:4567/v1' WHERE id='xiaomimimo20260612'" \
  --category codex_link \
  --keywords "cc-switch 404,127.0.0.1:4567转发,baseURL缺失/v1,provider_endpoints路由错误" \
  --skill_package cc_switch_4567_autofix \
  --tools "codex_fullchain_fix_v2.1.bat,cc_switch_precheck"
```
脚本自动：① 查重（场景A/B/C判定）② 写入 `resolved` ③ 输出迭代回执 ④ 提示固化引擎下次00:10消费。

### 固化引擎（已有，无需新建）
`E:\龙虾AI主控中心\lobster_skill_solidify.py` 每日00:10消费 `resolved` → `skill_knowledge/*.json`。

---

## 杜绝断片重复返工的硬性约束

1. **长上下文永久留存**：所有历史技能/迭代记录/案例日志禁止丢失；任务启动自动读取五步法+全域模板最新版，不加载过期旧规则
2. **重复拦截**：任务启动先检索匹配度≥80%历史案例，优先调用存量自动化工具；仅存量失效才重新排查，且修复后必须迭代更新原技能
3. **禁止无记录临时修复**：任何配置/脚本/路由修改必须同步写入 `issues_tracker.json` + 技能库 + 知识库

## 迭代回执标准

每次任务完成自动生成回执，确认以下全部 ✅ 才算闭环：
- [ ] 问题闭环校验 → `issues_tracker.json.resolved` 已写入
- [ ] 重复判定 → 场景A/B/C 已标注
- [ ] 软连接绑定 → 索引文件已追加
- [ ] 双端沉淀 → Obsidian双库 + Git 已写入
- [ ] 多Agent同步 → AGENTS.md/SOUL.md 引用已更新
- [ ] 固化待消费 → 固化引擎下次00:10将自动消费

---

## 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-07-19 | v1.0 | 初始版本。补齐龙虾五步法Step5缺失的自动迭代生产者触发器，定义五步强制流水线，修复cc-switch 404同类故障反复返工根因 |
