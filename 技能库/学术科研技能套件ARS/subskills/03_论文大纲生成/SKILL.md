---
name: ARS论文大纲生成
description: 生成学术论文结构大纲与章节字数分配、证据映射（IMRaD 及各类型论文模板）。只出大纲与论证骨架，不代写正文，禁止学位论文整章/全文生成。
version: 1.0
parent: 学术科研技能套件ARS
lobster:
  cost_mode: low
  触发词: [论文大纲, 论文结构, 章节安排, 论文架构, 写作提纲, outline, 论文计划]
  上游入口: ars/academic-paper/WORKFLOW.md（outline-only 模式）
  上游命令: ars-outline
allowed-tools: Read, Grep
---

# 3. 论文大纲生成

## 用途
产出**结构级**成果：章节层级、每节字数分配、论点-证据映射、文献支撑点。
✅ 允许：大纲、提纲、章节逻辑、证据映射表
❌ 禁止：整章正文、完整段落、学位论文全文/整章代写

## 触发指令
```
论文大纲：AI 对高等教育质量保障的影响（IMRaD，8000字）
论文结构：少子化对私立大学经营策略之影响
写作提纲：已有一手访谈数据，质性研究
```

## 执行步骤
1. **先判题**：若用户只给了宽泛题目/方向（无明确可回答的研究问题），
   **必须先转 `01_文献检索` 做选题收敛**，不得直接出大纲
2. **定类型**：实证研究（IMRaD）/ 综述 / 理论 / 案例 / 会议论文
3. **读模板**：`templates/imrad_template.md`（~1.4k tok）+ `references/paper_structure_patterns.md`（~2.6k tok）
4. **出骨架**：读 `agents/structure_architect_agent.md`（~5.7k tok）
5. **配字数**：按总字数分配各节，标注每节所需证据来源
6. **交人工**：大纲须由作者确认研究问题可回答、数据可支撑

## 按需加载白名单
| 文件 | 体量 | 何时读 |
|------|------|--------|
| `templates/imrad_template.md` | ~1.4k tok | 实证论文（默认） |
| `references/paper_structure_patterns.md` | ~2.6k tok | 结构模式选择 |
| `agents/structure_architect_agent.md` | ~5.7k tok | 大纲生成主 agent |
| `agents/argument_builder_agent.md` | — | 论证链搭建 |
| `references/intro_title_rhetoric_guide.md` | — | 标题与引言修辞 |
| ⚠ `WORKFLOW.md` | ~14.8k tok | **需报备**（全 11 模式流程时才读） |

## token 消耗预估
| 模式 | 加载内容 | 预估 |
|------|----------|------|
| **标准大纲**（推荐） | 本 SKILL + IMRaD 模板 + 结构模式 + architect agent | **≈ 9–11k** |
| 精简大纲 | 模板 + 结构模式（不读 agent） | **≈ 4–5k** |
| 全模式写作流程 | + WORKFLOW.md | **≈ 25k（需报备）** |

## 合规红线（本技能重点）
- **禁止**生成学位论文（硕博）的完整章节或全文 —— 只提供大纲与写作建议
- **禁止**在大纲中编造「本研究将采集 N 份问卷」等未经确认的研究设计
- 大纲中的引用文献必须来自 `01_文献检索` 已核验清单
- 输出须附：⚠ 提示「本大纲为结构建议，全部论点与数据需作者自行补充与核实」
