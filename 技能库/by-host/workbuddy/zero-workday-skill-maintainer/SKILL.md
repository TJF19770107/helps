---
name: zero-workday-skill-maintainer
description: 零工作日Skill自维护技能V1.0。当用户连续多天(≥2天)无实际会话/零工作内容、但又触发"基于当天工作生成Skill"等自动化任务时，本Skill为最低开销的矩阵自维护方案：识别真正的元需求→审计抽样→轻量Patch→避免无意义新增。触发词：零工作日、无会话、零工作内容、auto maintain、skill自维护、最低开销audit、轻量patch、空闲日维护。
agent_created: true
version: 1.1
updated: 2026-08-21
cost_mode: strict
---

# zero-workday-skill-maintainer - 零工作日Skill自维护师

## 1. 技能本质（What）

**一个动词，为「零工作日」提供专属的Skill矩阵最低开销维护方案。**

解决的核心矛盾：自动化任务（每日05:00、每周复盘）按时间触发，但用户实际工作为零；此时不应强行"为生成而生成"，应识别可低成本维护的最高价值动作。

## 2. 何时使用（When）

### 显式触发
- 用户发出"基于当天工作生成/迭代Skill"但近≥2天零会话
- 用户发出"维护一下Skill矩阵"但未指定具体动作
- 自动化任务在零工作日执行（如05:00每日生成器）

### 隐式触发
- 距上次审计3天且无新会话
- Skill目录最近修改时间集中在≥7天前
- 工作记忆MEMORY.md缺失或长期未更新

### 不适用场景（应改用其他Skill）
- 有明确当天工作内容 → `auto-skill-generator`
- 仅识别"是否需要新Skill" → `daily-skill-evolution-engine`
- 仅审查与版本决策 → `skill-ecosystem-steward`
- 需要如何写Skill模板 → `skill-template-generator`

## 3. 核心执行逻辑（How）

### 3.1 五步最低开销流程

```
Step 0: 零工作日判定（必跑，1次工具调用）
   ├─ 标准：最近N次会话窗口 ≥ 2天零交互 → 进入本Skill路径
   ├─ 快速：用stat命令查今日 memory/YYYY-MM-DD.md 是否存在
   └─ 退出条件：检测到当日有实际工作内容 → 转auto-skill-generator

Step 1: 元需求识别（2-3次工具调用）
   ├─ 阅读最近1份skill-patrol报告
   ├─ 阅读最近1份skill-health-audit报告
   ├─ 识别可提炼的元需求，例如：
   │   · 用户反复指令相同 = 元Skill缺失
   │   · 连续N次🟡降级 = 合并/迭代候选
   │   · 长时间未触及 = 验证是否仍必要
   └─ 输出：1-2个具体动作（创建Skill / 迭代Skill / 仅审计）

Step 2: 成本预算（必跑，0次工具调用）
   ├─ 总预算 ≤ 15次工具调用（V2.3成本感知）
   ├─ 真实工作日：预算20次（auto-skill-generator）
   └─ 零工作日：本Skill路径上限15次

Step 3: 执行单个最高价值动作（5-8次工具调用）
   ├─ 仅做1个动作：新建1个Skill 或 迭代1个Skill
   ├─ 不同时新建+迭代（避免过度展开）
   └─ 选择标准：
       · 复用收益最大（影响后续多日）
       · 填补矩阵真实空白（不是凑数）
       · 与成本控制/自动维护相关（跨切面价值）

Step 4: 强制成本复盘（输出到response，0工具调用）
   ├─ 实际工具调用数 vs Step 2 预算
   ├─ 偏差原因（如有）
   └─ 优化点（如有）
```

### 3.2 决策优先级

| 信号 | 优先级 | 动作 |
|------|--------|------|
| 工作记忆MEMORY.md缺失 | P0 | 仅创建记忆 + 不动Skill |
| 关键Skill（meta层）跨阈值 | P1 | 迭代1个meta层Skill |
| 通用Skill跨阈值但非meta | P2 | 仅审计 + 记录到下次执行 |
| 全部🟢稳定 | P3 | 默认不动作 + 输出no-op报告 |
| 元需求被识别（如本次） | P1 | 创建1个新Skill填补 |

### 3.3 零工作日输出模板

```markdown
## 零工作日Skill自维护报告 (YYYY-MM-DD)

**零工作日判定**：连续N天无会话
**判定依据**：conversation_search=0 / 当日memory.md不存在

### 路径选择
- [ ] 转auto-skill-generator（不适用：有工作内容时）
- [x] 走本Skill路径（最小开销维护）

### 本次动作
- [x] 仅审计（健康度抽样）
- [x] 创建1个Skill：消除元需求
- [x] 迭代1个Skill：修复跨阈值降级
- [ ] 不动Skill（仅写记忆）

### 成本复盘
- 预算：≤15次工具调用
- 实际：X次（节省Y%）
```

## 4. 参数说明（Parameters）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `zero_session_threshold_days` | int | 2 | 零会话判定阈值 |
| `cost_budget_calls` | int | 15 | 零工作日工具调用预算上限 |
| `must_create_skill` | bool | false | 是否强制创建Skill（默认false） |
| `preserve_history_only` | bool | false | 仅写工作记忆，不动Skill目录 |
| `audit_sample_ratio` | float | 0.3 | 抽样审计比例（30%） |
| `meta_skill_priority` | bool | true | meta层Skill获得优先维护权 |

## 5. 使用步骤（Step by Step）

### 5.1 在auto-skill-generator前增加前置判定

```yaml
执行auto-skill-generator前:
  1. 检查当日 memory/$(date +%F).md 是否存在
  2. 若不存在 → 进一步检查最近3天会话
  3. 若≥2天零会话 → 改走zero-workday-skill-maintainer路径
  4. 否则 → 走auto-skill-generator常规路径
```

### 5.2 手动触发

```
用户：「零工作日怎么办 / 维护一下Skill矩阵 / 今天没做事但05:00想跑点事」
→ 加载本Skill → Step 0判定 → Step 1识别 → Step 3执行单动作
```

### 5.3 自动化（05:00 cron）

```bash
#!/bin/bash
# 嵌入 auto-skill-generator 的首段
TODAY=$(date +%F)
if [ ! -f ".workbuddy/memory/${TODAY}.md" ]; then
  # 进一步判定
  RECENT_COUNT=$(ls .workbuddy/memory/ | tail -3 | xargs grep -c "实际工作" | head -1)
  if [ "$RECENT_COUNT" -lt 1 ]; then
    echo "检测到零工作日 → 切换至 zero-workday-skill-maintainer"
    # 调用本Skill路径
  fi
fi
```

## 6. 与其他Skill的边界（联动表）

| 联动Skill | 方向 | 触发关系 |
|-----------|------|----------|
| `auto-skill-generator` | ↔ 双向 | 有工作时：本Skill路由回auto-skill-generator；auto-skill-generator在零工作日触发本Skill |
| `daily-skill-evolution-engine` | → 退出 | 仅判断需要新Skill时：路由到该Skill |
| `skill-ecosystem-steward` | ↔ 双向 | 手动审计时协作 |
| `skill-template-generator` | ← 引用 | 新建Skill时复用其模板 |
| `zero-cost-task-execution` | ↔ 双向 | 共享成本约束（≤15次预算） |
| `daily-market-dashboard` | 无关 | 量化领域，无联动 |

## 7. 错误处理

| 错误模式 | 检测 | 兜底 |
|----------|------|------|
| 当日突然有工作内容但已启动本Skill | Step 0.退出条件 | 中途切回auto-skill-generator |
| 元需求识别失败（无明确动作） | Step 1结束无输出 | 仅写工作记忆，不动Skill |
| 工具调用超预算 | 实时计数 | 立即停止，输出成本超支报告 |
| 用户期望与本Skill定位冲突 | 用户质疑 | 解释零工作日判定依据 |
| conversation_search不可用 | Step 0判定失败 | 退化为stat时间戳兜底 |

## 8. 健康度自评

| 维度 | 得分 | 说明 |
|------|------|------|
| 完整度 | 23/25 | 8章节+3模式+5步流程齐全，缺示例与FAQ |
| 准确性 | 22/25 | 与V2.3成本感知策略一致，措辞严谨 |
| 复用度 | 25/25 | 跨"零工作日"所有情形 |
| 时效性 | 24/25 | 2026-08-09新建，无衰减 |
| **总分** | **94/100 🟢优秀** | 一次性高分区 |

## 9. 版本日志

- **V1.0**（2026-08-09）首次创建
  - 来源：第45次auto-skill-generator执行中识别元需求
  - 触发：连续5天（8/5-8/9）零会话但每日05:00任务照常触发
  - 价值：将"无工作但要维护"场景从"空动作/无意义新增Skill"中解放出来
  - 替代：无（之前依靠auto-skill-generator降级输出，但无明确零工作日判定）
- **V1.1**（2026-08-21）零工作日链路闭环
  - 注入 `cost_mode: strict` frontmatter
  - 与 `auto-skill-generator` 的联动从"→退出"升级为"↔双向"
  - 明确 auto-skill-generator 在零工作日触发本Skill的调用关系

## 10. 给用户的快速说明

> **什么时候用我？**
> 当你（或自动化）在没有新工作的日子里，仍然想跑Skill矩阵维护时——
> 我帮你用≤15次工具调用完成：识别该做什么 + 做这一件 + 复盘成本。
>
> **什么时候不用我？**
> - 你今天确实做了事 → 走auto-skill-generator
> - 你只想知道"该不该建Skill" → 走daily-skill-evolution-engine
> - 你只想看看Skill矩阵状态 → 走skill-ecosystem-steward
