---
name: ARS审稿回复生成
description: 依据审稿意见逐条生成学术回复（rebuttal / response to reviewers）与修改说明，含「接受-部分接受-反驳」三态策略。所有引用的补充数据须为真实可提供的材料。
version: 1.0
parent: 学术科研技能套件ARS
lobster:
  cost_mode: low
  触发词: [审稿回复, 回复审稿人, rebuttal, 逐条回应, 修改说明, 审稿意见, response to reviewers]
  上游入口: ars/academic-paper-reviewer/WORKFLOW.md
  上游命令: ars-revision / ars-rebuttal-audit
allowed-tools: Read, Grep
---

# 4. 审稿回复生成

## 用途
把审稿意见拆解为可执行的修改项，生成**学术规范**的逐条回应信（Response to Reviewers）。
✅ 允许：回应结构、措辞、修改计划、论证补强建议
❌ 禁止：编造「已补充实验」而实际未做、伪造数据、杜撰引用

## 触发指令
```
审稿回复：以下是三位审稿人意见……（附原文）
逐条回应：R2 第 3 条质疑样本量不足，如何回复
修改说明：按 major revision 要求整理回复信
```

## 执行步骤
1. **分类**：把每条意见归入 ①方法 ②结果 ③论述 ④文献 ⑤格式/语言
2. **定态**：每条标注 **接受 / 部分接受 / 有理反驳**（反驳须给出方法学依据，不得情绪化）
3. **读模板**：`templates/revision_response_template.md`（~2.4k tok）
4. **对齐标准**：`references/review_criteria_framework.md`（~2.0k tok）
5. **补证据**：若需补数据 → 转 `02_实证SQL数据分析` 实跑；若需补文献 → 转 `01_文献检索`
6. **写回信**：逐条「审稿人意见 → 作者回应 → 修改位置（页码/行号）」
7. **自检**：已承诺的补充分析/数据，凡是**尚未真正做出来的，一律不得写入**

## 按需加载白名单
| 文件 | 体量 | 何时读 |
|------|------|--------|
| `templates/revision_response_template.md` | ~2.4k tok | **默认必读** |
| `references/review_criteria_framework.md` | ~2.0k tok | 判断意见性质 |
| `references/editorial_decision_standards.md` | — | 涉及 major/minor 判定 |
| `agents/methodology_reviewer_agent.md` | ⚠ ~14.0k tok | **需报备** |
| `agents/domain_reviewer_agent.md` | ⚠ ~10.3k tok | **需报备**（需领域深评） |
| ⚠ `WORKFLOW.md` | ~11.8k tok | **需报备**（五席全评审流程） |

## token 消耗预估
| 模式 | 加载内容 | 预估 |
|------|----------|------|
| **标准回复**（推荐） | 本 SKILL + 回复模板 + 评审标准 | **≈ 5–7k** |
| 精简回复 | 仅模板 | **≈ 3k** |
| 深度反驳（方法学） | + methodology reviewer agent | **≈ 20k（需报备）** |

> 若需先「模拟审稿」再回复，走完整评审面板会用到 5 个 reviewer agent，
> 合计 **40k+ tokens**，**必须事先报备**。

## 人工核验点（强制）
- [ ] 每条「已修改/已补充」必须由作者实际完成，不得虚构
- [ ] 反驳意见的方法学依据须出自可引用的规范或文献
- [ ] 修改位置（页码/行号）与最终稿件一致
- [ ] 语言不得出现对审稿人的贬损或情绪化表达
