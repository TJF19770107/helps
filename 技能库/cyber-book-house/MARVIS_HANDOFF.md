# Marvis 协作交接说明

> 写入时间：2026-08-06 00:35 | 写入者：WorkBuddy（Claude Code审核层）
> 汤哥授权：全自动化修复，Marvis 与 WorkBuddy "哥俩好"协作

---

## 一、WorkBuddy 已修复的问题（3项）

### 1. orca_bridge.py 路径修复 [P0]
- **问题**：`scripts/orca_bridge.py` 调用 `src/cyber_ingest.py --orca-bridge <file>`，但 src/ 版本没有 `--orca-bridge` 参数，会直接报错
- **修复**：改为调用根目录 `cyber_ingest.py pan <file_path>`（位置参数），与 v1.5 引擎 CLI 接口对齐
- **新增**：磁盘空间硬约束校验、结构化日志输出
- **版本**：v1.0 → v1.1

### 2. src/cyber_ingest.py 职责标注 [P1]
- **问题**：根目录和 src/ 两个文件同名，orca_bridge 指错了路径
- **处理**：未删除/重命名 src/ 版本（避免破坏引用），但在文件头加了明确标注：
  - 根目录 `cyber_ingest.py` = **主入口**（v1.5引擎：抓取 + Obsidian写入 + CLI）
  - `src/cyber_ingest.py` = **基础设施层**（磁盘校验/积分校验/缓存清理/版本归档）
- **Marvis 注意**：以后新增功能请分清写到哪个文件

### 3. cangjie_bridge.py 最后一公里补完 [P1]
- **问题**：`run_distill_pipeline()` 把 JSON 放到 `cangjie-skill/input/` 就结束了，没有指令让 Agent 执行蒸馏
- **修复**：新增 `_generate_distill_instruction()` 函数，自动生成 `INSTRUCTION_<hash>.md` 指令文件
- **指令内容**：包含 RIA-TV++ 五阶段执行步骤、输入文件路径、输出位置
- **Marvis 注意**：蒸馏流水线现在完整了：扫描 → 格式化 → 写入JSON → 生成指令 → Agent执行

---

## 二、WorkBuddy 修复的全域模板 [P0]

### 龙虾全域官方模板-最终版.md 乱码修复
- **问题**：第119行后出现乱码（工作区文件被改坏，非 git 提交）
- **修复**：`git checkout -- 技能库/龙虾全域官方模板-最终版.md` 恢复 HEAD 干净版本
- **验证**：第119行内容正常（"回滚流程"段落完整）
- **Marvis 注意**：不要再直接编辑这个文件，如需修改请先 git stash

---

## 三、职责边界（哥俩好分工）

| 方向 | Marvis 负责 | WorkBuddy 负责 |
|------|-------------|---------------|
| 内容抓取、新平台接入 | ✅ 主外 | ❌ 不碰 |
| Obsidian 笔记生成 | ✅ | ❌ |
| 仓颉蒸馏 extractor 调用 | ✅ 执行蒸馏 | ❌ 不碰 |
| ORCA 桥接维护 | ❌ | ✅ 已修复 |
| 仓颉桥接补完 | ❌ | ✅ 已补完 |
| 全域模板损坏修复 | ❌ | ✅ 已修复 |
| 磁盘/积分/缓存基础设施 | ❌ | ✅ 校验兜底 |
| 缺失配置/脚本校验 | 你写启动脚本 | 我写自检+验收脚本 |
| 四化迭代知识库 | 共建 | 共建 |

**原则**：Marvis 主外（抓内容、扩功能、跑蒸馏），WorkBuddy 主内（修集成、补校验、兜底）。

---

## 四、Marvis 下一步该干的

1. **跑通一次完整流水线**：赛博书屋抓取 → Obsidian写入 → cangjie_bridge 扫描 → 生成蒸馏指令 → Agent 执行仓颉提取
2. **验证 cangjie-skill/input/ 目录**：确认 `INSTRUCTION_*.md` 文件能被 Agent 正确读取
3. **补齐龙虾五步法引用的缺失脚本**：
   - `fleet_start_cnb_free.bat`（CNB Free V4已过期，建议改为 `fleet_start_ollama.bat`）
   - `config/fleet_profiles/*.env`
   - `vision_router_mcp`
4. **不要碰** `scripts/orca_bridge.py`（WorkBuddy 维护）
5. **不要碰** `龙虾全域官方模板-最终版.md`（git HEAD 版本为准）

---

## 五、文件变更清单

| 文件 | 操作 | 版本 |
|------|------|------|
| `scripts/orca_bridge.py` | 修复（路径+参数+硬约束+日志） | v1.0→v1.1 |
| `src/cyber_ingest.py` | 头注释标注职责边界 | v1.0→v1.1 |
| `cangjie_bridge.py` | 补完蒸馏指令生成 | v1.0→v1.1 |
| `龙虾全域官方模板-最终版.md` | git restore 恢复 | HEAD |
| `MARVIS_HANDOFF.md` | 新建（本文件） | v1.0 |

---

## 六、术语映射（汤哥确认）

- **"龙虾"** / **"龙虾五步法"** = `lobster_task_standard_workflow_v3.0/SKILL.md`
- **"全域模板"** = `龙虾全域官方模板-最终版.md`（排第一位）
- **"四化迭代知识库"** = 龙虾五步法中的四化标准（智能化、定制化、全自动化、自我净化）
- 汤哥一提"龙虾"就是龙虾五步法，一提"全域模板"就是那个模板，不要乱猜

---

_WorkBuddy & Marvis 哥俩好，形成战斗力。_
